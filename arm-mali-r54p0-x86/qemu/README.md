# QEMU

The baseline launcher is generated at:

```text
qemu/run-baseline.sh
```

It prefers KVM when `/dev/kvm` is readable/writable by the current user and otherwise falls back to QEMU TCG.

The launcher boots the baseline artifact:

```text
artifacts/baseline/bzImage
artifacts/baseline/mali-initramfs.cpio.gz
```

Do not start fuzzing before the QEMU and Mali-probe checkpoints in `plan.md` pass.
