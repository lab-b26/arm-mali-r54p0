# Baseline Status

## Classification

The r54p0 x86 Simulated Platform build is:

```text
SUBMISSION_SHAPED_NON_CONFORMING
```

It is not an instrumentation-only build. It is the primary Kbase triage/analysis baseline for the x86 virtual platform.

## Why non-conforming?

The build requires:

```text
CONFIG_COMMON_CLK=y
```

because the r54p0 source path contains an unguarded use of the generic clock framework (`__clk_is_enabled()`) and the module link otherwise fails. `CONFIG_COMMON_CLK` is not among the KConfig option groups permitted by the Arm Device Configuration Guidelines.

## Consequence

A candidate observed in this lab is **not yet a submission candidate**. It must be independently reproduced using a DCG-conforming configuration and the appropriate in-scope hardware/driver conditions.

## Release string

The verified r54p0 archive/Kbuild reports:

```text
r54p0-01eac0
```

The supplied Arm virtual-platform guide contains a sample dmesg line showing `r54p0-00eac0`. This discrepancy is recorded in `research/decisions.md`; the verified source value is not altered.
