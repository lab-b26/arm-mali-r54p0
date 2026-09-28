#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fail(){ echo "ERROR: $*" >&2; exit 1; }

for f in AGENTS.md README.md plan.md setup_arm_r54p0_x86.sh research/state.md research/decisions.md; do
  [[ -f "$ROOT/$f" ]] || fail "missing $f"
done

for f in \
  documents/arm_gpu_bug_bounty_faq.pdf \
  documents/arm_gpu_bug_bounty_how_to_guide.pdf \
  documents/arm_gpu_virtual_platform_how_to_guide.pdf \
  documents/arm_gpu_bug_bounty_device_configuration_guidelines.pdf \
  patches/patches_for_virtual_device.zip; do
  [[ -f "$ROOT/$f" ]] || fail "missing $f"
done

expected=(
  0001-mali-fix-build-error-for-CONFIG_OF-n-for-4.1-kernels.patch
  0002-Fix-x86-build-error-for-missing-asm-arch_timer.h.patch
  0003-Workaround-arch_timer-funcs-undefined-for-NO_MALI.patch
  0004-Workaround-no-definition-of-dmb-in-non-Arm-platforms.patch
  0005-Fix-unused-function-warnings.patch
  0006-Fix-make-clean-when-no-arbitration-code-present.patch
)
for p in "${expected[@]}"; do [[ -f "$ROOT/patches/arm-virtual-device/$p" ]] || fail "missing patch $p"; done
[[ "$(find "$ROOT/patches/arm-virtual-device" -maxdepth 1 -type f -name '*.patch' | wc -l)" -eq 6 ]] || fail "patch directory does not contain exactly six .patch files"

bash -n "$ROOT/setup_arm_r54p0_x86.sh"

echo "Repository structure and shell syntax: OK"

# Plan/repository policy checks.
rg -q 'CONFIG_COMMON_CLK=y' "$ROOT/plan.md" || fail "plan.md missing D-11 COMMON_CLK policy"
rg -q 'r54p0-01eac0' "$ROOT/plan.md" || fail "plan.md missing verified r54p0-01eac0 release string"
rg -q 'SUBMISSION_SHAPED_NON_CONFORMING' "$ROOT/research/state.md" || fail "state.md missing baseline classification"

echo "D-11/release/state policy checks: OK"

# Packaging hygiene checks.
[[ ! -f "$ROOT/AX504X08X-SW-99002-r54p0-01eac0.tar.gz" ]] || fail "driver tarball must not be packaged"
[[ ! -f "$ROOT/patches_for_virtual_device.zip" ]] || fail "stray root patch ZIP must be removed"
[[ -f "$ROOT/patches/patches_for_virtual_device.zip" ]] || fail "canonical patch ZIP missing"

# Verify the extracted tracked patches are byte-identical to the supplied ZIP.
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
unzip -q "$ROOT/patches/patches_for_virtual_device.zip" -d "$tmpdir"
for p in "${expected[@]}"; do
  cmp -s "$tmpdir/$p" "$ROOT/patches/arm-virtual-device/$p" || fail "tracked patch differs from ZIP: $p"
done

echo "Packaging hygiene and patch-byte-identity checks: OK"
