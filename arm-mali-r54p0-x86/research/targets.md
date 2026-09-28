# Investigation Targets

Maintain prioritized, evidence-backed research targets here. This is not a vulnerability list.

## Target classes

### Lifetime/state transitions

- create -> use -> destroy
- map -> unmap -> free
- queue register -> bind -> kick -> terminate
- KCPU enqueue -> completion/delete
- CQS/fence synchronization across lifecycle changes

### Memory-management transitions

- SAME_VA allocation and `mmap()` cookie handling
- import/sticky map/unmap/free
- alias/subrange/gap/stride handling
- JIT initialization and allocation lifecycle
- Tiler heap init/size/term

### Concurrency

- asynchronous worker versus teardown
- simultaneous queue/context cleanup
- reference-counted objects across threads
- notification/read/poll versus object destruction

## Target selection rules

1. Prefer code reachable from the documented U/K interface.
2. Exclude dummy-model-only implementation code from bounty conclusions.
3. Do not treat a crash alone as proof of security impact.
4. Link every target to exact source files/functions and UAPI operations.
