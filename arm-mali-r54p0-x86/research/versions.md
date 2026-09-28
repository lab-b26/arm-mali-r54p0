# Versions and Source Provenance

Record exact versions before using them. Never rely on memory.

| Component | Version | Source URL/path | SHA-256/MD5 | Notes |
|---|---|---|---|---|
| Arm Mali Kbase | r54p0-01eac0 | Arm official download | MD5 `3bcd3870b58f83442b16b83e432e2f97`; SHA-256 `3b2049aa9b41b540850e23e5a86613f796c6f2f6878ee8233e2c03e5c2acc121` | Source archive external to Git. `MALI_RELEASE_NAME ?= '"r54p0-01eac0"'` confirmed in `drivers/gpu/arm/midgard/Kbuild:66` |
| Linux kernel | **6.12.111 — CURRENT KVER, builds** | `https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.12.111.tar.xz` | SHA-256 `9e59dc67624188fa12a6601f9598499cd6662a9066be572b59f935e3d7849810`; 148583092 bytes | `KVER=6.12.111`, selected on operator authorization (2026-09-28) after 6.18.54 was refuted at the build checkpoint. kernel.org moniker `longterm`. Chosen because it is the newest LTS that still contains `__SetPageMovable` **and** sits at/below r54p0's own newest `KERNEL_VERSION(6, 13, 0)` guard. Downloaded 2026-09-28, `xz -t` clean, independent re-download byte-identical, unpacked tree self-reports `VERSION=6 PATCHLEVEL=12 SUBLEVEL=111` (86642 files). **Patch-level compatibility established** at `PATCHES_APPLIED` (2026-09-28T22:34:06+00:00) — all six Arm x86 patches clean, in sequence, 0 `.rej`. **Config audit 10/10** at `BASELINE_CONFIG_VALID` (2026-09-28T22:34:06+00:00). **Build-level compatibility ESTABLISHED** at `BASELINE_BUILD_OK` (2026-09-28T22:49:22+00:00): `make bzImage modules` exit 0, 0 errors, 0 warnings, 129/129 Kbase units, `bzImage` + `vmlinux` + `mali_kbase.ko` all produced. Since Arm publishes no compatibility matrix ("not publicly documented"), **this observed build is the entire justification for the version choice**. Runtime compatibility (insmod, `/dev/mali0`, dmesg signature, QEMU boot) still unverified. Authenticity: clearsigned `sha256sums.asc` **VALID**, and the manifest attests exactly the SHA-256 of the bytes in use. Evidence: `logs/kernel-6.12.111-source.txt`, `logs/patch-apply-6.12.111.txt`, `logs/config-baseline-6.12.111.txt`, `logs/build-6.12.111-ok.txt`, `artifacts/baseline/SHA256SUMS` |
| Linux kernel (previous candidate) | **6.18.54 — REJECTED, does not build** | `https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.18.54.tar.xz` | SHA-256 `9df30b02dd8102bbd0be52556288ef6889ddbe7f1ddb96fbf847d0becf3eacac`; MD5 `7993a33ad0c09f9344c931695b9c50a1`; 154801608 bytes | `KVER=6.18.54`. kernel.org moniker `longterm`, released 2026-09-25, `iseol=false`. **Patch-level compatibility established** at `PATCHES_APPLIED` (2026-09-28T21:59:18+00:00) — all six Arm x86 patches apply cleanly and in sequence. **Build-level compatibility REFUTED** at 2026-09-28T22:21:29+00:00: `mali_kbase_mem_migrate.c` calls `__SetPageMovable`/`__ClearPageMovable`, which Linux removed in **6.17**. `make bzImage modules` exited 2; no `bzImage`, `vmlinux`, or `mali_kbase.ko`. Not mandated by Arm. Downloaded 2026-09-28, `xz -t` clean, second independent download byte-identical, unpacked tree self-reports `VERSION=6 PATCHLEVEL=18 SUBLEVEL=54` (91153 files). Authenticity confirmed against kernel.org's **signed** `sha256sums.asc`. Full evidence in `logs/build-failure-6.18.54.txt`; see decision rows "KVER=6.18.54", "kernel source authenticity", "r54p0 is patch-compatible with Linux 6.18.54", and "r54p0 cannot build against any Linux >= 6.17" |
| Linux kernel detached signature | 6.18.54 | `https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.18.54.tar.sign` | — | Signed by key `647F28654894E3BD457199BE38DBBDC86092693E` (Linus release key), created 2026-09-25T14:36:40Z. **Does NOT validate** `linux-6.18.54.tar.xz` or `linux-6.18.54.tar.gz`. Re-verified 2026-09-28 with the corrected three-way verifier: a genuine `SIGNATURE INVALID` (exit 1), over both archives, **not** a parse failure — the recorded anomaly **stands**. See decision row "kernel `.tar.sign` anomaly" and the re-verification row |
| Linux kernel detached signature | 6.12.111 | `https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.12.111.tar.sign` | — | Signed by the same key `647F28654894E3BD457199BE38DBBDC86092693E`, issuer key id `38DBBDC86092693E`, SHA-512, binary sigtype. **Does NOT validate** `linux-6.12.111.tar.xz` — the same upstream kernel.org anomaly as 6.18.54, now observed on two independent releases. Authenticity rests on the signed manifest instead |
| kernel.org signed manifest | 6.12.111 and 6.18.54 | `https://cdn.kernel.org/pub/linux/kernel/v6.x/sha256sums.asc` | — | Clearsigned (sigtype `0x01`, SHA-256) by key `632D3A06589DA6B1` (kernel.org archives key, fingerprint `B8868C80BA62A1FFFAF5FDA9632D3A06589DA6B1`). Signature **VALID**, re-confirmed 2026-09-28 for the 6.12.111 fetch. The single manifest attests every `linux-v6.x` artefact, so it covers **both** kernels. Re-checked that it attests exactly the bytes in use: 6.12.111 `.tar.xz` `9e59dc67…49810`, 6.18.54 `.tar.xz` `9df30b02…eacac`, 6.18.54 `.tar.gz` `ac748eb6…43af9`. This manifest is the authenticity anchor for the whole lab |
| QEMU | 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.18) | host package `qemu-system-x86` | n/a | `qemu-img` 8.2.2 same build. Instaged 2026-09-28 |
| GCC | 13.3.0 | host package `build-essential` | n/a | `gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` |
| Clang | 18.1.3 | host package `clang` | n/a | `Ubuntu clang version 18.1.3 (1ubuntu1)` |
| Go | go1.27.1 linux/amd64 | host toolchain | n/a | Needed for Syzkaller at `FUZZER_READY` |
| Syzkaller | `<not yet cloned>` | `https://github.com/google/syzkaller.git` | `<record>` | Deferred to `FUZZER_READY` per plan.md 20 |

## Auxiliary host packages (installed 2026-09-28, authorized as B2)

| Package | Version | Provides |
|---|---|---|
| `bc` | 1.07.1-3ubuntu4 | `bc` |
| `flex` | 2.6.4-8.2build1 | `flex` |
| `cpio` | 2.15+dfsg-1ubuntu2.1 | `cpio` (initramfs packing) |
| `busybox-static` | 1:1.36.1-6ubuntu3.1 | `busybox` — verified **statically linked** ELF x86-64, required for a bare initramfs |
| `qemu-system-x86` | 1:8.2.2+ds-0ubuntu1.18 | `qemu-system-x86_64` |
| `qemu-utils` | 1:8.2.2+ds-0ubuntu1.18 | `qemu-img` |
| `ripgrep` | 14.1.0-1 | `rg` (required by `scripts/verify_repository.sh`) |

## Deferred build dependency

`libelf-dev` is **not installed**. `x86_64_defconfig` selects `CONFIG_UNWINDER_ORC=y` and
`objtool` links against `libelf`, so this is strictly required at `BASELINE_BUILD_OK`. It is
not required for `PREFLIGHT_OK` and was not in the authorized package list. Must be installed
before the build checkpoint.

## Host tool re-verification at PREFLIGHT_OK (2026-09-28)

Every version in the tables above was re-measured on the live host while completing the
`PREFLIGHT_OK` checklist; all values still match, and the full evidence is in `logs/host.txt`
(written 2026-09-28T21:20:13+00:00, 168 lines). Specifically re-confirmed: Ubuntu 24.04.5 LTS,
GCC 13.3.0, Clang 18.1.3, GNU Make 4.3, Bison 3.8.2, Flex 2.6.4, bc 1.07.1, cpio 2.15,
QEMU/qemu-img 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.18), ripgrep 14.1.0, Go 1.27.1, CMake 3.28.3,
BusyBox 1.36.1 verified again as a **statically linked** x86-64 ELF, and GNU patch 2.7.6.
All 20 programs required by `plan.md` 3.2 resolve on `PATH` with zero missing.

The r54p0 archive is **verified** as of `SOURCES_VERIFIED` (2026-09-28T21:31:46+00:00): MD5
`3bcd3870b58f83442b16b83e432e2f97` matches Arm's official listing exactly, SHA-256
`3b2049aa9b41b540850e23e5a86613f796c6f2f6878ee8233e2c03e5c2acc121`, 1098708 bytes, recorded in
`logs/download.txt`. The archive is present at
`downloads/AX504X08X-SW-99002-r54p0-01eac0.tar.gz` and is correctly untracked by Git per
`plan.md` 0.0.

The `KVER=6.18.54` archive has been downloaded, verified, and unpacked as of
`KERNEL_SOURCE_READY` (2026-09-28T21:51:35+00:00). KVER is an execution-time choice, not an Arm
requirement. r54p0's **patch-level** compatibility with 6.18.54 was then established at
`PATCHES_APPLIED` (2026-09-28T21:59:18+00:00): all six Arm x86 patches apply cleanly, in sequence,
with no rejects, fuzz, or hunk offsets.

**Build-level compatibility was then refuted** (2026-09-28T22:21:29+00:00). `BASELINE_BUILD_OK` is
**not** reached. r54p0 does not compile against 6.18.54: `mali_kbase_mem_migrate.c` calls
`__SetPageMovable`/`__ClearPageMovable` at 14 sites, and both symbols were removed from Linux in
**6.17**. The file is an unconditional member of `mali_kbase-y` and **both** arms of the driver's
own version guard call the removed symbol, so no configuration or code-path choice avoids it. Full
diagnostic, bisect table, and candidate lines are in `logs/build-failure-6.18.54.txt`.

## Kernel candidates that still contain the removed API (added after the failed build)

`__SetPageMovable`/`__ClearPageMovable` are declared in `include/linux/migrate.h` in every upstream
tag from v5.4 through **v6.16** and are gone in **v6.17**. Independently, the newest
`KERNEL_VERSION()` guard anywhere in r54p0 Kbase is `KERNEL_VERSION(6, 13, 0)`, so the driver was
maintained against the 6.13 series. Both signals point at the newest LTS below 6.13.

| Candidate | kernel.org moniker | Status | Rationale |
|---|---|---|---|
| **6.12.111** | `longterm` | **recommended, UNTESTED** | Newest LTS that still has the required API **and** sits at/below the driver's own newest guard (6.13.0) |
| 6.6.157 | `longterm` | viable fallback, UNTESTED | Has the API; older than the driver's guard horizon |
| 6.1.188 | `longterm` | viable fallback, UNTESTED | Has the API; oldest LTS still listed |
| 6.18.54 | `longterm` | **REJECTED** | API removed in 6.17; build fails |

Latest stable overall at the time of writing is 7.2.8. Selecting any of these is a **decision for
the operator**: `plan.md` 6.2 supplies no kernel-downgrade instruction, so no version was changed
without authorisation. No claim is made that any candidate builds — the failed attempt is the first
empirical data point, not the last.

## Arm's published position on kernel version (verbatim, from `documents/`)

From `arm_gpu_bug_bounty_device_configuration_guidelines.pdf`, "Supported OS Versions", document
version `20250623-1.0`:

> Each version of the Arm® Mali™ Kernel Driver is compatible with specific Kernel versions. As these
> versions are **not publicly documented** and will change over time, Arm provides the following
> guidance: If you are configuring a new virtual environment for testing, we recommend you always
> use the latest Android Common Kernel or the latest Linux Kernel stable or longterm release before
> testing.

The Virtual Platform How-To Guide names no kernel release either. This confirms `plan.md` 6.1 and
is the reason the compatibility matrix had to be established by testing: Arm publishes no matrix
to consult, and its "use the latest LTS" guidance selects a release that provably does not build.

The same DCG section, "Supported Kernel Config Options", permits changes only to `CONFIG_COMPAT`,
`CONFIG_ARM64_4K_PAGES`/`CONFIG_ARM64_16K_PAGES`, `CONFIG_KASAN*`, and `CONFIG_UBSAN*`. This
independently confirms that `CONFIG_COMMON_CLK` (D-11) is outside the allow-list, and that the
driver is 64-bit only.

## Kernel source authenticity (added at `KERNEL_SOURCE_READY`)

The kernel tarball's authenticity was established with OpenPGP signatures, not merely a
checksum comparison against the same host that served the file.

`sha256sums.asc` in the kernel.org `v6.x` directory is a clearsigned manifest of every file in
that directory. Its signature verifies against the kernel.org archives key
`B8868C80BA62A1FFFAF5FDA9632D3A06589DA6B1`, and the manifest attests
`9df30b02…eacac` for `linux-6.18.54.tar.xz` — exactly the SHA-256 of the archive obtained here.
The `.tar.gz` was cross-checked the same way and also matches. The unpacked tree independently
self-reports `6.18.54` in its `Makefile`.

`linux-6.18.54.tar.sign` is a *separate*, detached signature from Linus Torvalds' release key
`647F28654894E3BD457199BE38DBBDC86092693E`. It does **not** validate either the `.tar.xz` or the
`.tar.gz`. The signature was created at 14:36:40 UTC while the archive's `Last-Modified` is
14:47:58 UTC, i.e. the archive was served with a timestamp ~11 minutes *after* the signature was
made, which is consistent with a server-side re-upload. This is recorded as an upstream
(kernel.org) anomaly, **not** as a defect in this lab, and it does not block
`KERNEL_SOURCE_READY`: the signed manifest provides an independent, valid attestation of the
exact bytes in use.

### Verification tooling

`gpg` and `gpgv` both refuse a public key that carries no user ID
(`new key but contains no user ID - skipped`), and keys.openpgp.org returns the kernel.org release
keys with user IDs stripped, so neither tool can be used directly here. `scripts/verify_openpgp.py`
was therefore written to perform RFC 4880 v4 signature verification and PKCS#1 v1.5 recovery using
only the Python standard library.

Because a hand-written crypto verifier that reports "invalid" is worthless without a control, the
tool is gated on a five-case matrix, all passing:

| Case | Expected | Result |
|---|---|---|
| gpg-produced signature over the correct file | valid | valid |
| same signature over an unrelated file | invalid | invalid |
| same signature over a file with one byte flipped | invalid | invalid |
| kernel.org `sha256sums.asc` with the archives key | valid | valid |
| kernel.org `sha256sums.asc` with the wrong (Linus) key | invalid | invalid |

The tool's computed key IDs (`38DBBDC86092693E`, `632D3A06589DA6B1`) also match the values
`gpg --list-packets` reports for the same packets, cross-validating the packet parser. An early
version of this tool reported the kernel tarball as "invalid" while also failing its own positive
control; the control is what exposed the bug, and no conclusion was drawn from the tool until it
passed.
