#!/usr/bin/env python3
"""Verify OpenPGP RSA signatures over a file without requiring a key user ID.

Why this exists
---------------
`gpg` and `gpgv` both refuse to use a public key that carries no user ID
("new key but contains no user ID - skipped" / "Can't check signature: No
public key"). Public keys fetched by fingerprint from keys.openpgp.org are
returned with user IDs stripped until they carry third-party verification, and
the kernel.org release keys are in exactly that state. This tool therefore
performs the verification itself, using only the standard library.

What it implements
------------------
* ASCII armor / binary OpenPGP packet parsing (RFC 4880 section 4, 6).
* v4 signature hashing (RFC 4880 section 5.2.4) for detached (sigtype 0x00)
  and cleartext (sigtype 0x01) signatures.
* PKCS#1 v1.5 signature recovery and verification (RFC 8017).

Hash input, confirmed empirically against gpg-produced signatures:

    data || hashed_area || 0x04 0xFF || uint32(len(hashed_area))

where `hashed_area` is the signature packet's version, signature type, public
key algorithm, hash algorithm, hashed-subpacket length, and hashed subpackets.

Usage
-----
    scripts/verify_openpgp.py KEY SIG FILE
        Verify a detached (binary) signature over FILE.

    scripts/verify_openpgp.py --clearsign KEY FILE
        Verify an RFC 4880 section 7 cleartext-signed FILE.

Exit status is 0 when the signature is valid, 1 otherwise.
"""
import base64
import hashlib
import sys

# hash algorithm id -> (name, constructor, DER DigestInfo prefix for the digest)
HASHES = {
    2:  ("sha256", hashlib.sha256, "3031300d060960864801650304020105000420"),
    8:  ("sha256", hashlib.sha256, "3031300d060960864801650304020105000420"),
    9:  ("sha384", hashlib.sha384, "3041300d060960864801650304020205000430"),
    10: ("sha512", hashlib.sha512, "3051300d060960864801650304020305000440"),
    11: ("sha256", hashlib.sha256, "3031300d060960864801650304020105000420"),
}


def dearmor_bytes(data):
    """Return the binary OpenPGP payload of an armored (or binary) blob."""
    lines = data.split(b"\n")
    if not lines[0].startswith(b"-----BEGIN PGP"):
        return data
    body = []
    for line in lines[1:]:
        if line.startswith(b"-----END PGP"):
            break
        if line.startswith(b"="):     # CRC24 checksum line
            continue
        if b":" in line:              # armor header
            continue
        line = line.strip()
        if line:
            body.append(line)
    return base64.b64decode(b"".join(body))


def dearmor(path):
    with open(path, "rb") as fh:
        return dearmor_bytes(fh.read())


def read_mpi(buf, off):
    """Read a multi-precision integer; returns (value, new offset)."""
    bits = int.from_bytes(buf[off:off + 2], "big")
    nbytes = (bits + 7) // 8
    return int.from_bytes(buf[off + 2:off + 2 + nbytes], "big"), off + 2 + nbytes


def parse_packets(buf):
    """Yield (tag, body) for each OpenPGP packet in buf.

    RFC 4880 section 4.2. Bit 7 of the tag octet is a validity marker and must
    be set. Bit 6 selects the framing: when set, the packet is NEW format and
    the tag is the low 6 bits with the body length given by the partial-length
    encoding; when clear, the packet is OLD format and the tag is bits 5..2
    with the body length width given by bits 1..0. Bits 1..0 are a length-type
    field and must never be folded into the tag. Verified against
    `gpg --list-packets` for both a new-format public-key packet and an
    old-format v4 signature packet.
    """
    off = 0
    while off < len(buf):
        ctb = buf[off]
        if not ctb & 0x80:
            raise ValueError("bad packet tag byte at offset %d" % off)
        if ctb & 0x40:                                  # new format
            tag = ctb & 0x3F
            off += 1
            first = buf[off]
            if first < 192:
                plen, off = first, off + 1
            elif first < 224:
                plen = ((first - 192) << 8) + buf[off + 1] + 192
                off += 2
            elif first == 255:
                plen = int.from_bytes(buf[off + 1:off + 5], "big")
                off += 5
            else:
                raise ValueError("partial body lengths are not supported")
        else:                                          # old format
            tag = (ctb & 0x3C) >> 2
            ltype = ctb & 0x03
            off += 1
            if ltype == 0:
                plen, off = buf[off], off + 1
            elif ltype == 1:
                plen, off = int.from_bytes(buf[off:off + 2], "big"), off + 2
            elif ltype == 2:
                plen, off = int.from_bytes(buf[off:off + 4], "big"), off + 4
            else:
                raise ValueError("indeterminate length is not supported")
        if off + plen > len(buf):
            raise ValueError("truncated packet body at offset %d" % off)
        yield tag, buf[off:off + plen]
        off += plen


def load_public_key(path):
    """Return (n, e, key_id) from an armored or binary public key block."""
    for tag, body in parse_packets(dearmor(path)):
        if tag != 6:                     # 6 = public key packet
            continue
        if body[0] != 4:
            raise ValueError("only v4 keys are supported")
        if body[5] != 1:
            raise ValueError("only RSA keys are supported")
        n, off = read_mpi(body, 6)
        e, _ = read_mpi(body, off)
        # v4 key ID = low 8 octets of SHA-1(0x99 || uint16(len(body)) || body).
        fpr = hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).digest()
        return n, e, fpr[-8:].hex().upper()
    raise ValueError("no public key packet found in %s" % path)


def load_signature(blob):
    """Return the first signature packet body found in blob."""
    for tag, body in parse_packets(blob):
        if tag == 2:                     # 2 = signature packet
            return body
    raise ValueError("no signature packet found")


def verify(keypath, sigblob, data):
    """Verify sigblob over data. Returns (ok, detail-dict)."""
    n, e, key_id = load_public_key(keypath)
    sig = load_signature(sigblob)

    version, sigtype, pubalgo, hashalgo = sig[0], sig[1], sig[2], sig[3]
    if version != 4:
        raise ValueError("only v4 signatures are supported (got v%d)" % version)
    if pubalgo != 1:
        raise ValueError("only RSA signatures are supported (algo %d)" % pubalgo)
    if hashalgo not in HASHES:
        raise ValueError("unsupported hash algorithm %d" % hashalgo)
    name, ctor, digestinfo = HASHES[hashalgo]

    hashed_len = int.from_bytes(sig[4:6], "big")
    hashed_area = sig[0:6 + hashed_len]

    # The signature MPI is the packet's final field; find the offset whose
    # declared bit length makes the MPI end exactly at the end of the packet.
    body_len = len(sig)
    pos = None
    for cand in range(6, body_len - 2):
        bits = int.from_bytes(sig[cand:cand + 2], "big")
        if 1024 <= bits <= 8192 and cand + 2 + (bits + 7) // 8 == body_len:
            pos = cand
    if pos is None:
        raise ValueError("could not locate the signature MPI")
    s, _ = read_mpi(sig, pos)

    h = ctor()
    h.update(data)
    h.update(hashed_area)
    h.update(b"\x04\xff" + len(hashed_area).to_bytes(4, "big"))
    computed = h.digest()

    t = bytes.fromhex(digestinfo) + computed
    k = (n.bit_length() + 7) // 8
    if k < len(t) + 11:
        raise ValueError("DigestInfo does not fit in the modulus")
    expected = b"\x00\x01" + b"\xff" * (k - 3 - len(t)) + b"\x00" + t
    recovered = pow(s, e, n).to_bytes(k, "big")

    return recovered == expected, {
        "key_id": key_id,
        "sigtype": sigtype,
        "hash": name,
        "computed": computed.hex(),
        "recovered": recovered[-len(computed):].hex(),
    }


def verify_detached(keypath, sigpath, target):
    with open(target, "rb") as fh:
        data = fh.read()
    ok, d = verify(keypath, dearmor(sigpath), data)
    _report(ok, d, "detached signature")
    return ok


def verify_clearsign(keypath, path):
    """Verify an RFC 4880 section 7 cleartext-signed document.

    The signed text is canonicalised: trailing whitespace is stripped from
    every line, lines are joined with CRLF, and the final CRLF before the
    signature marker is not part of the signed data.
    """
    with open(path, "rb") as fh:
        raw = fh.read()
    lines = raw.split(b"\n")
    try:
        start = next(i for i, l in enumerate(lines)
                     if l.startswith(b"-----BEGIN PGP SIGNATURE-----"))
    except StopIteration:
        raise ValueError("no signature block found in %s" % path)
    sigblob = dearmor_bytes(b"\n".join(lines[start:]))

    hidx = next((i for i, l in enumerate(lines) if l.startswith(b"Hash:")), None)
    if hidx is None:
        raise ValueError("no Hash: armor header found in %s" % path)
    body = hidx + 1
    while body < len(lines) and not lines[body].strip():
        body += 1
    text = b"\r\n".join(l.rstrip() for l in lines[body:start])

    ok, d = verify(keypath, sigblob, text)
    _report(ok, d, "clearsigned document")
    return ok


def _report(ok, d, what):
    print("file/signature under test: %s" % what)
    print("  issuer key id         : %s" % d["key_id"])
    print("  signature type        : 0x%02x%s" % (
        d["sigtype"], " (text)" if d["sigtype"] == 1 else " (binary)"))
    print("  digest algorithm      : %s" % d["hash"])
    print("  computed  digest      : %s" % d["computed"])
    print("  digest from signature : %s" % d["recovered"])
    print("  RESULT: %s" % ("SIGNATURE VALID" if ok else "SIGNATURE INVALID"))


def main(argv):
    """Exit codes are a three-way verdict and must never be conflated:

      0 = SIGNATURE VALID
      1 = SIGNATURE INVALID (a real, determined negative)
      2 = COULD NOT DETERMINE (bad usage, unreadable input, unsupported packet)

    Exit 2 exists so that a crash can never be mistaken for a negative result,
    which is the failure mode that once produced a false "INVALID" reading.
    """
    args = argv[1:]
    try:
        if args and args[0] == "--clearsign":
            if len(args) != 3:
                print(__doc__.strip())
                return 2
            return 0 if verify_clearsign(args[1], args[2]) else 1
        if len(args) != 3:
            print(__doc__.strip())
            return 2
        return 0 if verify_detached(args[0], args[1], args[2]) else 1
    except Exception as exc:                            # noqa: BLE001
        print("COULD NOT DETERMINE: %s: %s" % (type(exc).__name__, exc))
        print("Usage: %s KEY SIG FILE   |   %s --clearsign KEY FILE"
              % (argv[0], argv[0]))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
