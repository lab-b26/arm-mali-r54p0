# Execution State

OpenCode must update this file **only after the corresponding verification checklist in `plan.md` succeeds**.

Current state:

```text
QEMU_BOOT_OK
```

`NOT_STARTED` is repository metadata, not an execution checkpoint. The first verified checkpoint is `PREFLIGHT_OK`.

## Verified transitions

| Timestamp | State | Evidence |
|---|---|---|
| 2026-09-28T21:21:42+00:00 | `PREFLIGHT_OK` | `plan.md` 0.0, 2, 3.1, 3.2, 3.3 checklist — 84/84 checks passed. Host record `logs/host.txt`; repository verification `logs/verify-repository.txt` (exit 0); B1/B2/B3 recorded in `research/decisions.md`. |
| 2026-09-28T21:31:46+00:00 | `SOURCES_VERIFIED` | `plan.md` 4.1/4.2. r54p0 archive MD5 `3bcd3870b58f83442b16b83e432e2f97` **matches** the official Arm listing; SHA-256 `3b2049aa…c121`, 1098708 bytes. Recorded in `logs/download.txt`. |
| 2026-09-28T21:32:00+00:00 | `PATCHES_VERIFIED` | `plan.md` 5. ZIP `992f92f1…2b60` holds exactly the six expected Arm patches; all six tracked copies are byte-identical to the ZIP and unmodified vs Git. Hashes recorded in `logs/patch.txt`. |
| 2026-09-28T21:51:35+00:00 | `KERNEL_SOURCE_READY` | `plan.md` 6.2. `linux-6.18.54.tar.xz` downloaded (154801608 bytes, SHA-256 `9df30b02…eacac`), `xz -t` clean, independent re-download byte-identical, unpacked to a 91153-file clean tree self-reporting `6.18.54`. Authenticity confirmed against kernel.org's clearsigned `sha256sums.asc` (VALID, key `B8868C80…65DA6B1`). The per-file `.tar.sign` does **not** validate either archive — recorded as an upstream kernel.org anomaly, mitigated by the valid signed manifest. See `research/versions.md` and the three `KERNEL_SOURCE_READY` decision rows. |
| 2026-09-28T21:58:08+00:00 | `MALI_INTEGRATED` | `plan.md` 7, 8, 9. r54p0 unpacked to `source/mali-r54p0-unpacked` (441 files); Kbase located at `driver/product/kernel`; `MALI_RELEASE_NAME` = `r54p0-01eac0` (`Kbuild:66`, J-1 honoured). Integrated tree built by fresh `cp -a` of the clean tree (91594 files) then Arm's documented sequence: Kbase copied to `drivers/gpu/arm` (368 files), `obj-$(CONFIG_MALI_MIDGARD) += arm/` appended at `drivers/gpu/Makefile:11`, `source "drivers/gpu/arm/Kconfig"` inserted at `drivers/video/Kconfig:93`. **Both edits verified to occur exactly once.** The clean tree is verifiably untouched. |
| 2026-09-28T21:59:18+00:00 | `PATCHES_APPLIED` | `plan.md` 10.1, 10.2, for 6.18.54. Sequential preflight on a disposable copy **and** real application: all six Arm x86 patches `exit=0`, **0 `.rej` files, no fuzz, no hunk offsets**; all 10 touched files differed from the clean tree; clean tree still unpatched. Arm patches byte-identical to committed copies. Transcript: `logs/patch-apply.txt` (per deviation from plan §10.2's literal `logs/patch.txt`, which holds the SHA-256s from §5). |
| 2026-09-28T22:08:56+00:00 | `BASELINE_CONFIG_VALID` | `plan.md` 11. `x86_64_defconfig` → `scripts/config` → `olddefconfig`, output in the transient root per B3. **Audit 10/10** against `.config`: `MALI_MIDGARD=m`, `MALI_CSF_SUPPORT=y`, `MALI_EXPERT=y`, `MALI_NO_MALI=y`, `MALI_REAL_HW=n`, `MALI_DEBUG=n` (present as `# CONFIG_MALI_DEBUG is not set` at line 3484), `MALI_NO_MALI_DEFAULT_GPU="tKRx"`, `MALI_PLATFORM_NAME="vexpress"`, `OF=n`, `COMMON_CLK=y` (D-11). `CONFIG_LARGE_PAGE_SUPPORT=y`, matching Arm's guide note. Snapshot: `logs/config-baseline.txt` (5535 lines). On this kernel `scripts/config -s/--state` prints only `n\|y\|m\|undef`, so string values were read from `.config` directly per `plan.md` 11.4's no-guessing rule. |
| 2026-09-28T22:32:37+00:00 | `KERNEL_SOURCE_READY` | `plan.md` 6.2, **re-attained for `KVER=6.12.111`**. `linux-6.12.111.tar.xz` (148583092 B) from cdn.kernel.org, `xz -t` clean, SHA-256 `9e59dc67…49810`, independent re-download byte-identical, unpacked to an 86642-file clean tree self-reporting `VERSION=6 PATCHLEVEL=12 SUBLEVEL=111`. Authenticity: clearsigned `sha256sums.asc` **VALID** (key `632D3A06589DA6B1`), and the manifest attests exactly the SHA-256 of the bytes in use. Pre-flight confirms `__SetPageMovable`/`__ClearPageMovable` present in `include/linux/migrate.h` (2 and 3 occurrences) — the static reason 6.12.111 was chosen. Verifier hardened to a three-way verdict (0/1/2), 9/9 control matrix. Evidence: `logs/kernel-6.12.111-source.txt`. |
| 2026-09-28T22:34:06+00:00 | `MALI_INTEGRATED` | `plan.md` 7, 8, 9, **re-run for 6.12.111**. Fresh `cp -a` of the 6.12.111 clean tree (87083 files) then Arm's documented sequence; Kbase copied to `drivers/gpu/arm` (368 files), `obj-$(CONFIG_MALI_MIDGARD) += arm/` at `drivers/gpu/Makefile:10`, `source "drivers/gpu/arm/Kconfig"` at `drivers/video/Kconfig:74`. **Both edits verified to occur exactly once.** `MALI_RELEASE_NAME` = `r54p0-01eac0` (J-1 honoured). Clean tree verifiably untouched. |
| 2026-09-28T22:34:06+00:00 | `PATCHES_APPLIED` | `plan.md` 10.1, 10.2, **re-run for 6.12.111**. Sequential preflight on a disposable copy **and** real application: all six Arm x86 patches `exit=0`, **0 `.rej` files, no fuzz, no hunk offsets**. Arm patches byte-identical to committed copies. Transcript: `logs/patch-apply-6.12.111.txt`. |
| 2026-09-28T22:34:06+00:00 | `BASELINE_CONFIG_VALID` | `plan.md` 11, **re-run for 6.12.111**. `x86_64_defconfig` → `scripts/config` → `olddefconfig`. **Audit 10/10** against `.config`: `MALI_MIDGARD=m`, `MALI_CSF_SUPPORT=y`, `MALI_EXPERT=y`, `MALI_NO_MALI=y`, `MALI_REAL_HW=n`, `MALI_DEBUG=n` (`# CONFIG_MALI_DEBUG is not set` at line 3389), `MALI_NO_MALI_DEFAULT_GPU="tKRx"`, `MALI_PLATFORM_NAME="vexpress"`, `OF=n`, `COMMON_CLK=y` (D-11, audited as a non-conforming deviation). `CONFIG_LARGE_PAGE_SUPPORT=y`. Snapshot: `logs/config-baseline-6.12.111.txt` (5438 lines). |
| 2026-09-28T22:49:22+00:00 | `BASELINE_BUILD_OK` | `plan.md` 12, for `KVER=6.12.111`. `make O=<O> -j4 bzImage modules` **exit 0**, 15m13s, with **0 `error:` and 0 `warning:` lines** in the whole transcript. Verified on **artefacts, not on absence of errors**: `bzImage` (14M) and `vmlinux` (50M) both present, `bzImage is ready (#1)` in the transcript, and `mali_kbase.ko` (2394272 B, ELF 64-bit relocatable x86-64, 5207 defined symbols) present — satisfying plan §12's "do not continue to QEMU unless `mali_kbase.ko` exists". All **129** Kbase translation units compiled, including `mali_kbase_mem_migrate.o` at line 2605 — the exact file that refuted 6.18.54. Release string compiled in as `version=r54p0-01eac0 (UK version 1.36)`, matching `Kbuild` (J-1 honoured, guide's `r54p0-00eac0` sample not adopted). Config **re-audited 10/10** against the exact `.config` that built this kernel, restating D-11 (`CONFIG_COMMON_CLK=y`): baseline is `SUBMISSION_SHAPED_NON_CONFORMING`. Artefacts + `SHA256SUMS` staged in `artifacts/baseline/`. Evidence: `logs/build-baseline-6.12.111.txt`, `logs/build-6.12.111-ok.txt`. |
| 2026-09-28T23:08:36+00:00 | `INITRAMFS_OK` | `plan.md` 13. Static BusyBox initramfs: 16 applet symlinks, `mali_kbase.ko` copied in, `init` mode 0755 and **byte-identical to plan §13's heredoc** (diffed), packed `cpio --null -o --format=newc \| gzip -9` → 1.6M, `gzip -t` OK, 26 entries. Two cross-checks so the initramfs cannot carry a stale module: `mali_kbase.ko` extracted back out of the cpio is byte-identical (`ce3165d2…2996e`) to the one built at `BASELINE_BUILD_OK`, and busybox re-checked after extraction is still statically linked. **Deviation:** `find` added to the applet list — plan §13's init script calls `find` but §13's symlink loop omits it, and the `2>/dev/null \|\| true` guard would have hidden the failure. cpio embeds mtimes, so its SHA-256 identifies this artefact and is not a reproducible-build claim. Host-side well-formedness only; the guest is unproven. Evidence: `logs/initramfs-6.12.111.txt`. |
| 2026-09-28T23:21:15+00:00 | `QEMU_BOOT_OK` | `plan.md` 14. Kernel boots under QEMU 8.2.2, initramfs `/init` runs to completion, guest reaches a working BusyBox `ash` prompt; `uname -a` = `Linux (none) 6.12.111 #1 SMP PREEMPT_DYNAMIC … x86_64`, matching the selected `KVER`. Two independent boots agreed. **Deviation (pre-authorised by `plan.md` 14 itself):** `-accel kvm` and `-cpu host` dropped, TCG used. KVM unavailability **verified, not assumed** — `/dev/kvm` is mode 0620 root:root, `os.open` raises `PermissionError [Errno 13]`, and the `kvm` module is not loaded (QEMU *does* list `kvm`, so the blocker is the device, not the binary). Recorded before the run, not after. Exactly two flags dropped; the runner was diffed against `plan.md` 14's literal heredoc. **Run 1's stdin-fed §15 checks were silently lost** (bytes written to the serial before the guest tty existed) and were **not** counted as a pass; run 2 delays the feed 120 s and carries the evidence. The guest cannot self-terminate (`poweroff` is not a `plan.md` 13 applet) and the applet was deliberately not added, so the run ended via QEMU's own Ctrl-A x — exit 0, image untouched. **New defect found:** `plan.md` 13's sysfs block is inert for a *second* reason (`find` follows no symlink); see the decision rows. Scoped to `plan.md` 14 only — Mali bring-up evidence is withheld for `MALI_PROBE_OK`. Evidence: `qemu/logs/baseline-boot.log`, `qemu/logs/baseline-boot2.log`, `logs/qemu-boot-6.12.111.txt`. |

`INITRAMFS_OK` **passed** (2026-09-28T23:08:36+00:00). The next gate is `QEMU_BOOT_OK`
(`plan.md` 14, 15): boot the kernel under QEMU and confirm the mandatory bring-up checks. Nothing
about the guest is verified yet — `insmod` success, `/dev/mali0`, the Arm dmesg signature,
`libGPUCounters`, and Mali device behaviour are all later checkpoints.

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
- A `KVER` change re-opens every kernel-tree-dependent state (`KERNEL_SOURCE_READY` onward) for the
  new kernel. Re-attained states are appended to `state.log` again; earlier entries are historical.
  The preceding attempt is **never** deleted from the evidence logs.

## Baseline label

`kernel/baseline` is **SUBMISSION_SHAPED_NON_CONFORMING** because `CONFIG_COMMON_CLK=y` is a documented build-enablement deviation outside the Arm DCG allow-list. Do not relabel this as an instrumentation-only build. This label applies to the baseline for **both** kernels attempted, and must be restated in every baseline audit.

## Kernel version re-selection (2026-09-28T22:32:37+00:00) — KVER is now 6.12.111

`6.18.54` was refuted at `BASELINE_BUILD_OK` and is **no longer the working KVER**. On explicit
operator authorization, `KVER` was re-selected to **6.12.111** (kernel.org `longterm`): the newest
LTS that still contains `__SetPageMovable` and that sits at/below r54p0's own newest
`KERNEL_VERSION(6, 13, 0)` guard. The 6.18.54 evidence is retained, not deleted, in
`logs/build-failure-6.18.54.txt` and `logs/build-baseline.txt`.

`KERNEL_SOURCE_READY`, `MALI_INTEGRATED`, `PATCHES_APPLIED` and `BASELINE_CONFIG_VALID` are all
**re-attained for 6.12.111** and therefore appear twice in `state.log`. Earlier entries describe the
6.18.54 attempt and are historical.

| Item | 6.18.54 (refuted) | 6.12.111 (current) |
|---|---|---|
| Archive | 154801608 B, SHA-256 `9df30b02…eacac` | 148583092 B, SHA-256 `9e59dc67…49810` |
| Authenticity | signed `sha256sums.asc` **VALID** | signed `sha256sums.asc` **VALID**, attested SHA-256 matches |
| `.tar.sign` | INVALID (re-verified, real negative) | INVALID (real negative) |
| Clean tree | `linux-6.18.54-clean` (91153 files) | `linux-6.12.111-clean` (86642 files) |
| Integrated tree | `linux-6.18.54-integrated` | `linux-6.12.111-integrated` (87083 files) |
| Integration edits | exactly once each | exactly once each (`gpu/Makefile:10`, `video/Kconfig:74`) |
| Six Arm patches | all clean, in sequence | all clean, in sequence, 0 `.rej` |
| Config audit | 10/10 | 10/10 |
| Build | **FAILED** (`__SetPageMovable`), aborted at 4th Kbase object | **PASSED** — exit 0, 0 errors, 0 warnings, 129/129 Kbase units, `mali_kbase.ko` produced |

## Blocking finding at `BASELINE_BUILD_OK` for 6.18.54 (2026-09-28T22:21:29+00:00) — resolved by re-selection

`BASELINE_BUILD_OK` failed for `6.18.54` and was never reached. `make bzImage modules` exited 2.
Exactly two errors were emitted, both in `drivers/gpu/arm/midgard/mali_kbase_mem_migrate.c`:

```text
mali_kbase_mem_migrate.c:83:9: error: implicit declaration of function ‘__SetPageMovable’; did you mean ‘__SetPageTable’? [-Werror=implicit-function-declaration]
mali_kbase_mem_migrate.c:158:25: error: implicit declaration of function ‘__ClearPageMovable’; did you mean ‘__ClearPageTable’? [-Werror=implicit-function-declaration]
```

Why this was not a configuration mistake and could not be configured away:

- Neither symbol exists anywhere in 6.18.54; `define PG_movable` occurs in 0 files.
- The file is an **unconditional** member of `mali_kbase-y` (`Kbuild:145`).
- **Both** arms of the driver's own `#if (KERNEL_VERSION(6,0,0) <= LINUX_VERSION_CODE)` guard call
  the removed symbol (lines 83 and 104), and `__ClearPageMovable` at line 158 is unguarded — so no
  kernel version reaches a working path inside this file.
- Bisected against upstream tags: the API is present v5.4→**v6.16** and removed in **v6.17**. The
  ceiling is a property of r54p0, not of 6.18.54.
- Corroborating: the newest `KERNEL_VERSION()` guard in Kbase is `KERNEL_VERSION(6, 13, 0)`.

**Limit on that result:** the build aborted at the 4th object of `mali_kbase-y`, leaving ~364 Kbase
files uncompiled. It was a lower bound on 6.18.54 breakage, not a full inventory. No `bzImage`,
`vmlinux`, or `mali_kbase.ko` was produced. Nothing was worked around: no Kbase source modified, no
Arm patch edited, no kernel version changed without authorization.

## Pending inputs

- **`QEMU_BOOT_OK` is the next gate** (`plan.md` 14, 15). `bzImage` and `mali-initramfs.cpio.gz`
  are staged in `artifacts/baseline/` with recorded SHA-256s, so the guest has everything §13 needs.
- **QEMU must run under TCG, not KVM.** `/dev/kvm` is unreadable and unwritable by this session, so
  `plan.md` 14's `-accel kvm -cpu host` cannot be used. `plan.md` 14 explicitly sanctions dropping
  both flags and recording the slower non-accelerated mode; that deviation must be recorded before
  the QEMU run, not after. Expect TCG boot to be markedly slower than the 4-vCPU KVM baseline in
  Arm's guide, so a generous timeout is required and a slow boot must not be misread as a hang.
- `plan.md` 14's runner ends in `exec /bin/sh`, so the guest will **not** exit on its own. The run
  needs either a bounded timeout or a `poweroff` fed on stdin, and a timeout must not be mistaken
  for a boot failure.
- The 6.18.54 attempt aborted at the 4th of 129 Kbase objects, so **what 6.18.54 would have hit
  next is still unmeasured** and is not claimed. What is established is narrower and positive: 6.12.111
  compiles and links all 129 units and modposts `mali_kbase.ko` with 0 errors and 0 warnings.
- Per `D-11`, `CONFIG_COMMON_CLK=y` is a non-conforming deviation and this baseline is
  **SUBMISSION_SHAPED_NON_CONFORMING**. It was re-audited against the exact `.config` that produced
  the build, and must reappear in every baseline audit. Arm's DCG allow-list is `CONFIG_COMPAT`,
  `CONFIG_ARM64_4K_PAGES`/`CONFIG_ARM64_16K_PAGES`, `CONFIG_KASAN*`, `CONFIG_UBSAN*` only — which
  independently confirms `CONFIG_COMMON_CLK` is outside it. Any submission candidate needs separate
  DCG-conforming validation.
- `CONFIG_MALI_NO_MALI=y` means this is the dummy model. Do **not** describe it as emulating real GPU
  hardware or firmware, and do not treat dummy-model-only bugs as final bounty findings.
- Arm publishes **no** per-driver kernel matrix ("not publicly documented"), so 6.12.111 is justified
  only by the build actually observed here — which is now recorded.
- The clean tree `linux-6.12.111-clean` stays unpatched; all work is in `linux-6.12.111-integrated`
  (patched). Build output is transient (B3) but the four artefacts and `SHA256SUMS` are staged in
  `artifacts/baseline/` as durable evidence. The 6.18.54 trees remain in the transient root as
  evidence; they are regenerable and may be deleted freely.
