# Kbase UAPI Map

This file is generated/filled during the `UAPI_MAPPED` checkpoint. Keep all entries tied to the exact r54p0 source tree.

**Provenance of every number in this file.** Nothing below is hand-derived or recalled from
memory. The macro list is read out of the r54p0 UAPI headers, and every command value, direction
bit, encoded size and `sizeof(argument)` is produced by **compiling against those exact headers**
(`plan.md` 18 forbids inventing struct layout from a newer Kbase, so the layouts are the headers',
not mine). Three machine-readable companions sit beside this file:

| file | what it is |
|---|---|
| `uapi-map-raw.txt` | `plan.md` 17's extraction command, run verbatim (263 lines) |
| `uapi-map-derived.tsv` | the compiled-out table: value, dir, type, nr, ioc_size, sizeof(arg), status, header, line |
| `uapi-map-phases.tsv` | the same rows joined to which dispatcher phase handles them |

Source tree: `linux-6.12.111-integrated` (the tree that actually built the verified module).
UAPI root: `include/uapi/gpu/arm/midgard/` (18 files). Release string: `r54p0-01eac0`.

## Device entry

- Device node: `/dev/mali0` — a **misc** device, char `10, 258`, observed in the guest as
  `crw-rw-rw-` (0666). Registered by `kbase_device_misc_register()` via `misc_register()` with no
  explicit `.mode`, so the kernel default applies.
- Main interface: `ioctl()`
- Additional interfaces: `poll()`, `read()`, `mmap()`
- `kbase_fops` (`mali_kbase_core_linux.c:2047`): `open`, `release`, `read`, `poll`,
  `unlocked_ioctl`, `compat_ioctl`, `mmap`, `check_flags`, `get_unmapped_area`.
- **`.compat_ioctl = kbase_ioctl`** — the 32-bit compat path calls the *same* function, so there is
  **no struct-layout translation layer**. A 32-bit process must therefore build 32-bit-correct
  structs itself; the encoded `_IOC_SIZE` in the command value is what the driver validates.
- **`.fop_flags = FOP_UNSIGNED_OFFSET`** is set under `#if (KERNEL_VERSION(6, 12, 0) <= LINUX_VERSION_CODE)`.
  We are on 6.12.111, so that guard is **active**. This is one of the few places where the `KVER`
  choice reaches the driver's own code path.

## Initial state sequence

```text
open("/dev/mali0", O_RDWR | O_CLOEXEC)      <-- O_CLOEXEC is MANDATORY, see below
  -> KBASE_IOCTL_VERSION_CHECK
  -> KBASE_IOCTL_SET_FLAGS
  -> subsequent interface-specific operations
```

This is not merely Arm's prose: it is the literal structure of the dispatcher
(`kbase_ioctl`, `mali_kbase_core_linux.c:1646`). There are **two** `switch (cmd)` statements with
one guard between them:

```c
switch (cmd) {                 /* switch #1, line 1654 -- 6 cases, NO context needed */
case KBASE_IOCTL_VERSION_CHECK: ... case KBASE_IOCTL_GET_GPUPROPS: ...
}
kctx = kbase_file_get_kctx_if_setup_complete(kfile);
if (unlikely(!kctx))
        return -EPERM;         /* <-- the gate */
switch (cmd) {                 /* switch #2, line 1693 -- 50 cases, context required */
case KBASE_IOCTL_MEM_ALLOC: ... }
```

Two consequences the seed program must respect:

1. **`open()` must pass `O_CLOEXEC`.** `kbase_check_flags()` returns `-EINVAL` if the flag is absent:
   *"Enforce that the driver keeps the O_CLOEXEC flag so that execve() always closes the file
   descriptor in a child process."* A seed program that opens without `O_CLOEXEC` fails at `open`,
   not at the first ioctl.
2. **`mmap()` is a phase-2 operation.** `kbase_mmap()` applies the same
   `kbase_file_get_kctx_if_setup_complete()` / `-EPERM` gate before calling
   `kbase_context_mmap()`, so memory must be allocated (which is itself phase 2) before it can be
   mapped. The mmap relationship is therefore: `MEM_ALLOC*` produces a handle, and that handle is
   the thing `mmap()` consumes.

## IOCTL inventory

Scale: **57** ioctl macros in the r54p0 UAPI headers; **56** are compiled into this build and
**1** (`KBASE_IOCTL_TLSTREAM_STATS`) is behind `#if MALI_UNIT_TEST`, which is not defined anywhere,
so it is absent from the shipped module. Directions of the 56 built ioctls: 28 `_IOW`, 23 `_IOWR`,
3 `_IOR`, 2 `_IO` (28+23+3+2 = 56). The two `_IO`s take no argument at all and are
`KBASE_IOCTL_TLSTREAM_FLUSH` and `KBASE_IOCTL_CS_EVENT_SIGNAL`.

Phase 1 = usable immediately after `open()`. Phase 2 = requires a context, else `-EPERM`.
`-` = not part of `/dev/mali0`'s `unlocked_ioctl`.

| nr | ioctl name | command value | dir | sizeof(arg) | phase | family |
|---|---|---|---|---|---|---|
| 0x00 | `KBASE_IOCTL_VERSION_CHECK_RESERVED` | `0xc0048000` | RW | 4 | 1 | handshake |
| 0x01 | `KBASE_IOCTL_SET_FLAGS` | `0x40048001` | W | 4 | 1 | handshake |
| 0x03 | `KBASE_IOCTL_GET_GPUPROPS` | `0x40108003` | W | 16 | 1 | info |
| 0x34 | `KBASE_IOCTL_VERSION_CHECK` | `0xc0048034` | RW | 4 | 1 | handshake |
| 0x38 | `KBASE_IOCTL_KINSTR_PRFCNT_ENUM_INFO` | `0xc0108038` | RW | 16 | 1 | prfcnt |
| 0x39 | `KBASE_IOCTL_KINSTR_PRFCNT_SETUP` | `0xc0108039` | RW | 16 | 1 | prfcnt |
| 0x05 | `KBASE_IOCTL_MEM_ALLOC` | `0xc0208005` | RW | 32 | 2 | memory |
| 0x06 | `KBASE_IOCTL_MEM_QUERY` | `0xc0108006` | RW | 16 | 2 | memory |
| 0x07 | `KBASE_IOCTL_MEM_FREE` | `0x40088007` | W | 8 | 2 | memory |
| 0x08 | `KBASE_IOCTL_HWCNT_READER_SETUP` | `0x40148008` | W | 20 | 2 | hwcnt |
| 0x0c | `KBASE_IOCTL_DISJOINT_QUERY` | `0x8004800c` | R | 4 | 2 | disjoint |
| 0x0d | `KBASE_IOCTL_GET_DDK_VERSION` | `0x4010800d` | W | 16 | 2 | info |
| 0x0e | `KBASE_IOCTL_MEM_JIT_INIT` | `0x4018800e` | W | 24 | 2 | memory |
| 0x0f | `KBASE_IOCTL_MEM_SYNC` | `0x4020800f` | W | 32 | 2 | memory |
| 0x10 | `KBASE_IOCTL_MEM_FIND_CPU_OFFSET` | `0xc0188010` | RW | 24 | 2 | memory |
| 0x11 | `KBASE_IOCTL_GET_CONTEXT_ID` | `0x80048011` | R | 4 | 2 | info |
| 0x12 | `KBASE_IOCTL_TLSTREAM_ACQUIRE` | `0x40048012` | W | 4 | 2 | tlstream |
| 0x13 | `KBASE_IOCTL_TLSTREAM_FLUSH` | `0x00008013` | none | 0 | 2 | tlstream |
| 0x14 | `KBASE_IOCTL_MEM_COMMIT` | `0x40108014` | W | 16 | 2 | memory |
| 0x15 | `KBASE_IOCTL_MEM_ALIAS` | `0xc0208015` | RW | 32 | 2 | memory |
| 0x16 | `KBASE_IOCTL_MEM_IMPORT` | `0xc0188016` | RW | 24 | 2 | memory |
| 0x17 | `KBASE_IOCTL_MEM_FLAGS_CHANGE` | `0x40188017` | W | 24 | 2 | memory |
| 0x18 | `KBASE_IOCTL_STREAM_CREATE` | `0x40208018` | W | 32 | 2 | other |
| 0x19 | `KBASE_IOCTL_FENCE_VALIDATE` | `0x40048019` | W | 4 | 2 | other |
| 0x1b | `KBASE_IOCTL_MEM_PROFILE_ADD` | `0x4010801b` | W | 16 | 2 | memory |
| 0x1d | `KBASE_IOCTL_STICKY_RESOURCE_MAP` | `0x4010801d` | W | 16 | 2 | other |
| 0x1e | `KBASE_IOCTL_STICKY_RESOURCE_UNMAP` | `0x4010801e` | W | 16 | 2 | other |
| 0x1f | `KBASE_IOCTL_MEM_FIND_GPU_START_AND_OFFSET` | `0xc010801f` | RW | 16 | 2 | memory |
| 0x20 | `KBASE_IOCTL_HWCNT_SET` | `0x40108020` | W | 16 | 2 | hwcnt |
| 0x24 | `KBASE_IOCTL_CS_QUEUE_REGISTER` | `0x40108024` | W | 16 | 2 | csf |
| 0x25 | `KBASE_IOCTL_CS_QUEUE_KICK` | `0x40088025` | W | 8 | 2 | csf |
| 0x26 | `KBASE_IOCTL_MEM_EXEC_INIT` | `0x40088026` | W | 8 | 2 | memory |
| 0x27 | `KBASE_IOCTL_CS_QUEUE_BIND` | `0xc0108027` | RW | 16 | 2 | csf |
| 0x28 | `KBASE_IOCTL_CS_QUEUE_REGISTER_EX` | `0x40288028` | W | 40 | 2 | csf |
| 0x29 | `KBASE_IOCTL_CS_QUEUE_TERMINATE` | `0x40088029` | W | 8 | 2 | csf |
| 0x2a | `KBASE_IOCTL_CS_QUEUE_GROUP_CREATE_1_6` | `0xc020802a` | RW | 32 | 2 | csf |
| 0x2b | `KBASE_IOCTL_CS_QUEUE_GROUP_TERMINATE` | `0x4008802b` | W | 8 | 2 | csf |
| 0x2c | `KBASE_IOCTL_CS_EVENT_SIGNAL` | `0x0000802c` | none | 0 | 2 | csf |
| 0x2d | `KBASE_IOCTL_KCPU_QUEUE_CREATE` | `0x8008802d` | R | 8 | 2 | csf |
| 0x2e | `KBASE_IOCTL_KCPU_QUEUE_DELETE` | `0x4008802e` | W | 8 | 2 | csf |
| 0x2f | `KBASE_IOCTL_KCPU_QUEUE_ENQUEUE` | `0x4010802f` | W | 16 | 2 | csf |
| 0x30 | `KBASE_IOCTL_CS_TILER_HEAP_INIT` | `0xc0188030` | RW | 24 | 2 | csf |
| 0x30 | `KBASE_IOCTL_CS_TILER_HEAP_INIT_1_13` | `0xc0108030` | RW | 16 | 2 | csf |
| 0x31 | `KBASE_IOCTL_CS_TILER_HEAP_TERM` | `0x40088031` | W | 8 | 2 | csf |
| 0x32 | `KBASE_IOCTL_GET_CPU_GPU_TIMEINFO` | `0xc0208032` | RW | 32 | 2 | info |
| 0x33 | `KBASE_IOCTL_CS_GET_GLB_IFACE` | `0xc0188033` | RW | 24 | 2 | csf |
| 0x35 | `KBASE_IOCTL_CS_CPU_QUEUE_DUMP` | `0x40108035` | W | 16 | 2 | csf |
| 0x36 | `KBASE_IOCTL_CONTEXT_PRIORITY_CHECK` | `0xc0018036` | RW | 1 | 2 | other |
| 0x37 | `KBASE_IOCTL_SET_LIMITED_CORE_COUNT` | `0x40018037` | W | 1 | 2 | other |
| 0x3a | `KBASE_IOCTL_CS_QUEUE_GROUP_CREATE_1_18` | `0xc028803a` | RW | 40 | 2 | csf |
| 0x3a | `KBASE_IOCTL_CS_QUEUE_GROUP_CREATE_1_35` | `0xc070803a` | RW | 112 | 2 | csf |
| 0x3b | `KBASE_IOCTL_MEM_ALLOC_EX` | `0xc040803b` | RW | 64 | 2 | memory |
| 0x3c | `KBASE_IOCTL_READ_USER_PAGE` | `0xc008803c` | RW | 8 | 2 | other |
| 0x3d | `KBASE_IOCTL_QUEUE_GROUP_CLEAR_FAULTS` | `0x4010803d` | W | 16 | 2 | other |
| 0x3e | `KBASE_IOCTL_CS_TILER_HEAP_SIZE` | `0xc010803e` | RW | 16 | 2 | csf |
| 0x3f | `KBASE_IOCTL_CS_QUEUE_GROUP_CREATE` | `0xc078803f` | RW | 120 | 2 | csf |
| - | `KBASE_IOCTL_TLSTREAM_STATS` | **not built** (`MALI_UNIT_TEST` off) | - | - | not built (MALI_UNIT_TEST) | tlstream |

### Cross-checks that make this table trustworthy

Three independent checks were run, and all three agree with the table:

1. **Header vs. built module.** The `switch` cases in `kbase_ioctl` (6 + 50 = 56) match the 56
   header-declared ioctls 1:1, with no case in the source that the headers do not declare.
2. **Built module vs. command values.** Searching `kbase_ioctl`'s own bytes for each command value
   as a 32-bit little-endian constant finds **55 of 56**. The single exception is
   `KBASE_IOCTL_HWCNT_READER_SETUP`, which is *not* `/dev/mali0`'s ioctl at all: it belongs to a
   separate `file_operations` for the hwcnt-reader device
   (`mali_kbase_kinstr_prfcnt.c:1140`, `kbasep_kinstr_prfcnt_hwcnt_reader_ioctl`). A textual scan
   for `cmp $imm,%esi` finds only 53, because two values are compared in a form that scan does not
   match; the byte-level search is the stronger evidence and is what the 55 figure comes from.
3. **Nothing invented.** The one ioctl that is in the source switches but not in the binary is the
   `MALI_UNIT_TEST`-gated one, which is the expected result rather than a discrepancy.

### Version-suffixed compatibility IOCTLs (recorded separately, per the safety notes)

Two ioctl **numbers are reused with different argument layouts**, so the command value alone does
not identify the struct — this is exactly why `VERSION_CHECK` must come first:

| nr | macro | ioc_size |
|---|---|---|
| `0x30` | `KBASE_IOCTL_CS_TILER_HEAP_INIT` | 24 |
| `0x30` | `KBASE_IOCTL_CS_TILER_HEAP_INIT_1_13` | 16 |
| `0x3a` | `KBASE_IOCTL_CS_QUEUE_GROUP_CREATE_1_18` | 40 |
| `0x3a` | `KBASE_IOCTL_CS_QUEUE_GROUP_CREATE_1_35` | 112 |

All four are compiled in this build, so the value alone is ambiguous; selection is by API version
at runtime.

### The type constants are not IOCTLs

`KBASE_IOCTL_TYPE` (`0x80`), `KBASE_IOCTL_TEST_TYPE` (`0x81`) and `KBASE_IOCTL_EXTRA_TYPE`
(`0x82`) are type bytes, not commands. An extraction filter of `"_IO" in expr` wrongly admits all
three, because `_IO` also occurs inside the identifier `KBASE_IOCTL_TYPE`; the filter used here
requires a real `_IO[A-Z]*(` encoding. This is recorded because it silently inflated an earlier
draft of this table from 57 macros to 59, adding two non-ioctls.

## Memory interfaces

14 memory-family ioctls, **all phase 2** (they need a context):

```text
MEM_ALLOC  MEM_ALLOC_EX  MEM_QUERY  MEM_FREE  MEM_SYNC  MEM_COMMIT  MEM_ALIAS
MEM_IMPORT  MEM_EXEC_INIT  MEM_JIT_INIT  MEM_FIND_CPU_OFFSET
MEM_FIND_GPU_START_AND_OFFSET  MEM_JIT_DUMP  READ_USER_PAGE
```

- **Allocation:** `MEM_ALLOC` (32 bytes) and `MEM_ALLOC_EX` (64 bytes).
- **mmap relationship:** as above — allocation yields a handle, `mmap()` consumes it, and `mmap()`
  carries the same `-EPERM` context gate.
- **Cleanup:** `MEM_FREE` is the counterpart to the allocation ioctls. No cleanup ioctl was
  individually traced beyond its name; the per-ioctl handle-dependency column is **not** claimed.
- `MEM_FIND_CPU_OFFSET` / `MEM_FIND_GPU_START_AND_OFFSET` are the pointers-to-buffer relationships
  that link an allocation to a CPU mapping.

## CSF interfaces

20 CSF-family ioctls, all phase 2. `CONFIG_MALI_CSF_SUPPORT=y` in this build, so the CSF surface
is compiled in — but note the driver is running the **dummy model**, which is not a CSF-capable
GPU, so CSF ioctls are present in the UAPI without necessarily being exercisable. The
queue/group lifecycle (`CS_QUEUE_GROUP_CREATE` 120 bytes -> `CS_QUEUE_GROUP_TERM`,
`CS_QUEUE_GROUP_BIND` -> `CS_QUEUE_KICK`, `CS_EVENT_SIGNAL`) is mapped by name and value only; the
binding and handle-dependency semantics have **not** been individually analysed.

## Privilege

- The main `/dev/mali0` ioctl surface is **unprivileged by construction**: the node is created
  world-writable (0666, observed in the guest) and there is **no POSIX capability check anywhere in
  the main ioctl path**.
- A whole-tree search for `capable(` / `CAP_*` in `.c` files found **exactly one** hit, and it is
  not on this path: `tl/mali_kbase_timeline_io.c:94`,
  `return kbase_unprivileged_global_profiling || capable(CAP_SYS_ADMIN);` — the timeline/profiling
  ioctl.
- `mali_kbase_caps.h` (54 textual hits) is Kbase's own utilisation-caps framework and is unrelated
  to POSIX capabilities. It must not be mistaken for a privilege check.
- `kbase_check_flags()` enforces `O_CLOEXEC`, which is a **correctness** requirement, not a
  privilege gate.

**Consequence for later stages:** because the surface is unprivileged, a root-only test proves
nothing about unprivileged EL0 reachability. Per `AGENTS.md`, any reachability claim must be
exercised as an unprivileged user; the guest so far runs everything as root, so **no reachability
is claimed at this checkpoint**.

## Safety notes

- Keep this map descriptive; do not invent argument layouts. — **Honoured.** Every value, direction
  and size is compiler output from the r54p0 headers. Where a semantic field (per-ioctl handle
  dependency, CSF binding rules) was not traced, it is marked as not analysed rather than filled in.
- Record version-suffixed compatibility IOCTLs separately. — **Done**, in the table above.
- Distinguish privileged/debug-only interfaces from unprivileged EL0-reachable interfaces. — **Done**
  in the Privilege section, with the one `capable(CAP_SYS_ADMIN)` site identified as *not* being on
  the `/dev/mali0` path.

`CONFIG_MALI_DEBUG` is off, so the debug-only ioctls are not part of the shipped surface, and the
`MALI_UNIT_TEST` ioctl is absent. Both facts are recorded above rather than assumed.
