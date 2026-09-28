# Kbase UAPI Map

This file is generated/filled during the `UAPI_MAPPED` checkpoint. Keep all entries tied to the exact r54p0 source tree.

## Device entry

- Device node: `/dev/mali0`
- Main interface: `ioctl()`
- Additional interfaces: `poll()`, `read()`, `mmap()`

## Initial state sequence

```text
open
  -> KBASE_IOCTL_VERSION_CHECK
  -> KBASE_IOCTL_SET_FLAGS
  -> subsequent interface-specific operations
```

## IOCTL inventory

| IOCTL | Header | Argument structure | Required state | Notes |
|---|---|---|---|---|
| `KBASE_IOCTL_VERSION_CHECK` | `mali_kbase_ioctl.h` | `kbase_ioctl_version_check` | open | required before other general IOCTLs |
| `KBASE_IOCTL_SET_FLAGS` | `mali_kbase_ioctl.h` / common headers | record exact struct | after VERSION_CHECK | context flags |
| `<fill>` | | | | |

## Memory interfaces

Map the exact r54p0 definitions for allocation, import, alias, free, sync, commit, flags change, and `mmap()` special handles.

## CSF interfaces

Map queue/group registration, bind, kick, termination, global-interface querying, notifications, and KCPU queue interfaces.

## Safety notes

- Keep this map descriptive; do not invent argument layouts.
- Record version-suffixed compatibility IOCTLs separately.
- Distinguish privileged/debug-only interfaces from unprivileged EL0-reachable interfaces.
