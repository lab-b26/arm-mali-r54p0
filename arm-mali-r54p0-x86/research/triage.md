# Finding Triage

Use this checklist for every candidate.

```text
[ ] Kbase code is affected
[ ] not dummy-model-only
[ ] reachable from an unprivileged EL0 process
[ ] reachable through an in-scope syscall/device interface
[ ] not debugfs/sysfs-only
[ ] not TEST-only configuration
[ ] not a vendor/OEM-only customization
[ ] current in-scope Kbase version tested
[ ] no source modification needed to reproduce
[ ] root cause isolated
[ ] security impact demonstrated
[ ] minimal reproducer exists
[ ] real-device validation performed when required
```

## Candidate

- ID:
- First observed state:
- Source function/file:
- Trigger interface:
- Configuration:
- NO_MALI dependency:
- Observed failure:
- Impact evidence:
- Reproduction rate:
- Validation status:
