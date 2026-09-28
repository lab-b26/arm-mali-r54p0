# Changelog

## v1.3 — 2026-09-28

- Reclassified `CONFIG_COMMON_CLK=y` as a **non-conforming baseline build-enablement deviation** rather than investigation-only instrumentation.
- Added explicit D-11 documentation and baseline status tracking.
- Standardized the actual verified r54p0 release string to `r54p0-01eac0`; retained the Arm-guide `00eac0` sample only as a documented discrepancy.
- Added hard `COMMON_CLK=y` and `LARGE_PAGE_SUPPORT=y` configuration assertions.
- Standardized generated QEMU launcher path to `qemu/run-baseline.sh`.
- Standardized r54p0 unpack path to `source/mali-r54p0-unpacked/`.
- Corrected the out-of-tree `scripts/config --file` examples.
- Added repository/package hygiene verification and byte-identity checks for the six Arm patches.
- Kept the driver tarball external to the repository/bundle.
