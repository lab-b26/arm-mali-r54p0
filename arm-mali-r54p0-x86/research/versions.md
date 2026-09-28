# Versions and Source Provenance

Record exact versions before using them. Never rely on memory.

| Component | Version | Source URL/path | SHA-256/MD5 | Notes |
|---|---|---|---|---|
| Arm Mali Kbase | r54p0-01eac0 | Arm official download | MD5 `3bcd3870b58f83442b16b83e432e2f97`; SHA-256 `3b2049aa9b41b540850e23e5a86613f796c6f2f6878ee8233e2c03e5c2acc121` | Source archive external to Git. `MALI_RELEASE_NAME ?= '"r54p0-01eac0"'` confirmed in `drivers/gpu/arm/midgard/Kbuild:66` |
| Linux kernel | **6.18.54** | `https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.18.54.tar.xz` | *not yet downloaded — record at `SOURCES_VERIFIED`* | `KVER=6.18.54`. kernel.org moniker `longterm`, released 2026-09-25, `iseol=false`. **First** compatibility candidate; r54p0 compatibility NOT yet established. Not mandated by Arm. See decision row "KVER=6.18.54" |
| Linux kernel signature | 6.18.54 | `https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.18.54.tar.sign` | — | PGP signature available for source verification |
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
