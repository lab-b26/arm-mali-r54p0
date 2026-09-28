# OpenCode Big Pickle quick start

1. Clone/copy this repository to `$HOME/arm-mali-r54p0-x86`.
2. Read `AGENTS.md` and obey its authority/stop rules.
3. Read `plan.md`.
4. Read the four PDFs in `documents/`.
5. Inspect `patches/patches_for_virtual_device.zip` and the six extracted patches.
6. Obtain the exact r54p0 driver archive separately and put it under `downloads/`.
7. Select a current stable/LTS Linux kernel, set `KVER`, and record the decision.
8. Run `./scripts/verify_repository.sh`.
9. Execute `setup_arm_r54p0_x86.sh` only after the preflight and source checkpoints in `plan.md` are understood.
10. Use `research/state.md` as the checkpoint ledger. The baseline is submission-shaped but non-conforming due to D-11 `CONFIG_COMMON_CLK=y`; any finding must later be revalidated under a DCG-conforming configuration.

Example:

```bash
cd "$HOME/arm-mali-r54p0-x86"
./scripts/verify_repository.sh
KVER=<selected-stable-or-LTS-release> ./setup_arm_r54p0_x86.sh
```
