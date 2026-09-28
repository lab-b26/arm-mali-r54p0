# Execution State

OpenCode must update this file **only after the corresponding verification checklist in `plan.md` succeeds**.

Current state:

```text
NOT_STARTED
```

`NOT_STARTED` is repository metadata, not an execution checkpoint. The first verified checkpoint is `PREFLIGHT_OK`.

## Allowed states (ordered)

```text
PREFLIGHT_OK
SOURCES_VERIFIED
PATCHES_VERIFIED
KERNEL_SOURCE_READY
MALI_INTEGRATED
PATCHES_APPLIED
BASELINE_CONFIG_VALID
BASELINE_BUILD_OK
INITRAMFS_OK
QEMU_BOOT_OK
MALI_PROBE_OK
MALIGPUCOUNTERS_OK
UAPI_MAPPED
INVESTIGATION_BUILD_OK
FUZZER_READY
SEEDS_VALID
FUZZING_ACTIVE
CANDIDATE_FOUND
TRIAGE_COMPLETE
REAL_DEVICE_VALIDATED
REPORT_READY
```

## Rules

- Start a fresh run at the first applicable state and record the transition timestamp in `research/state.log`.
- Never skip a failed state.
- If a later step fails, leave this file at the last verified state.
- A state is not verified merely because a command returned zero; the checklist in `plan.md` must be satisfied.
- Record significant failures and deviations in `research/decisions.md`.

## Baseline label

`kernel/baseline` is **SUBMISSION_SHAPED_NON_CONFORMING** because `CONFIG_COMMON_CLK=y` is a documented build-enablement deviation outside the Arm DCG allow-list. Do not relabel this as an instrumentation-only build.
