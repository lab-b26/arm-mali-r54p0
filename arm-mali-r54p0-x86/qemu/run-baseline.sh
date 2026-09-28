#!/usr/bin/env bash
set -euo pipefail

LAB="${LAB:-$HOME/arm-mali-r54p0-x86}"

# plan.md 14 specifies `-accel kvm -cpu host` and then, verbatim, sanctions the
# fallback: "If KVM is unavailable, use the same command without `-accel kvm`
# and `-cpu host`, then record the slower non-accelerated mode."
#
# KVM is unavailable here and this was verified, not assumed:
#   /dev/kvm        crw-rw---- root:root  (mode 0620, not in our group)
#   os.open(RDWR)   PermissionError [Errno 13]
#   kvm module      not loaded
# So both flags are dropped and QEMU uses TCG. The `-cpu host` drop is required
# too: `host` is only meaningful for KVM and TCG has no notion of it.
# Under TCG QEMU also takes only 1 host thread per vCPU; TCG boot is markedly
# slower than Arm's guide implies. Do not read a slow boot as a hang.
exec qemu-system-x86_64 \
  -machine pc \
  -m 4096 \
  -smp 4 \
  -kernel "$LAB/artifacts/baseline/bzImage" \
  -initrd "$LAB/artifacts/baseline/mali-initramfs.cpio.gz" \
  -append 'console=ttyS0' \
  -nographic \
  -no-reboot
