# OpenCode Big Pickle Agent Instructions

This repository builds and verifies the Arm Mali 5th Gen **r54p0 x86 “Simulated Platform Device”** virtual lab described by the supplied Arm Bug Bounty documents.

## Read first

1. Read `plan.md` before executing commands.
2. Inspect the files under `documents/`.
3. Inspect `patches/patches_for_virtual_device.zip` and the extracted six patches.
4. Inspect `setup_arm_r54p0_x86.sh` and `README.md`.

## Authority

When documents disagree, use this order:

1. Arm-provided PDFs in `documents/`.
2. Arm-supplied virtual-device patch bundle in `patches/`.
3. `plan.md`.
4. `setup_arm_r54p0_x86.sh`.
5. `README.md`.
6. Other local implementation choices.

Record any implementation choice or deviation in `research/decisions.md`.

## Kernel version policy

`KVER` is an explicit execution-time choice. Arm's Device Configuration Guidelines recommend a current stable/LTS or Android Common Kernel for a new virtual environment but do not pin a specific Linux release. OpenCode must select, test, and record the exact version before building.

## Canonical workspace

Use:

```text
$HOME/arm-mali-r54p0-x86
```

Do not silently switch to another workspace path.

## Reproducibility rules

- Work inside the canonical lab workspace except for package installation and explicitly required external downloads.
- Never modify the untouched Arm patch copies under `patches/arm-virtual-device/`. If the ZIP and tracked copies differ, stop and report the mismatch.
- Never overwrite the original r54p0 source archive.
- Keep clean source trees and integrated/modified trees separate.
- Do not apply the six Arm patches twice to the same tree.
- Before destructive operations, use a disposable copy or a known-fresh directory.
- Record exact source versions, checksums, compiler versions, kernel config, QEMU version, and important commands.
- A checkpoint passes only after its verification commands pass.
- If an Arm patch does not apply cleanly, stop at that checkpoint and record the complete error. Do not invent or silently substitute a patch.
- `CONFIG_MALI_DEBUG` must remain disabled.
- The x86 research configuration uses `CONFIG_MALI_NO_MALI=y`; dummy-model-only bugs are not final bounty findings.
- Do not claim that the NO_MALI model emulates real GPU hardware or GPU firmware.
- Do not run a final reachability test only as root and then claim unprivileged EL0 reachability.
- Do not treat a KASAN/KCSAN crash by itself as proof of a bounty-eligible vulnerability.
- Do not modify Kbase source merely to manufacture a crash.
- Keep virtual-platform build-enablement patches separate from vulnerability analysis.

## Required x86 baseline

```text
CONFIG_MALI_MIDGARD=m
CONFIG_MALI_CSF_SUPPORT=y
CONFIG_MALI_EXPERT=y
CONFIG_MALI_NO_MALI=y
# CONFIG_MALI_REAL_HW is not set
CONFIG_MALI_NO_MALI_DEFAULT_GPU="tKRx"
CONFIG_MALI_PLATFORM_NAME="vexpress"
# CONFIG_MALI_DEBUG is not set
```

The Mali driver is 64-bit only. The baseline includes the documented `CONFIG_COMMON_CLK=y` build-enablement deviation because r54p0 requires the generic clock framework to link on this x86 configuration. `CONFIG_COMMON_CLK` is outside the Arm Device Configuration Guidelines allow-list, so the baseline is submission-shaped but non-conforming. KASAN/UBSAN changes are separate instrumentation and must obey the Arm Device Configuration Guidelines.

## Patch handling

The six Arm x86 patches must be validated and applied sequentially with `patch -p3 -i`. A dry-run of each patch independently against the pristine tree is not sufficient.

## Checkpoint discipline

Maintain `research/state.md` and/or the state log designated by `plan.md`. Do not skip a failed checkpoint merely to begin fuzzing.

## Release-string discrepancy

Do not normalize the r54p0 release string to the sample dmesg in the Arm virtual-platform guide. The verified archive filename and Kbuild report `r54p0-01eac0`, while the guide's sample dmesg displays `r54p0-00eac0`. Record the discrepancy and validate against the source/Kbuild value.

## Baseline deviation D-11

`CONFIG_COMMON_CLK=y` is a **non-conforming baseline build-enablement deviation**. It is not instrumentation and it does not belong in the separate instrumented build solely because it is a deviation. Keep it in the baseline, audit it explicitly, and require independent DCG-conforming validation for any submission candidate.
