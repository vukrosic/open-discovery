---
name: optimize-gpu-kernel
description: Write, port, fuse, debug, or optimize GPU kernels and verify their correctness and performance on concrete target hardware. Use for CUDA, Triton, Metal, MLX custom kernels, HIP/ROCm, OpenCL, shader-compute, or another accelerator kernel when the user asks to replace framework operations, reduce kernel latency or launches, improve memory movement, tune tiling or occupancy, or create a faster low-level implementation without changing required semantics. Route end-to-end model-serving optimization to $optimize-inference and generic evaluator-driven program evolution to $evolve-program.
---

# Optimize GPU Kernel

Produce a working target-native kernel with measured evidence, not a plausible
code sketch or a speed claim copied from another device.

## Fix the contract

Inspect the reference operation, call site, build system, available hardware,
runtime, existing tests, and representative shapes before editing. Establish:

- exact semantics, accepted dtypes, layouts, strides, shapes, devices, and
  numerical behavior;
- aliasing, mutation, synchronization, determinism, gradient, and error-handling
  requirements where relevant;
- the target accelerator, architecture, toolchain, driver, framework, and
  compilation mode;
- representative workloads and the metric that matters, such as isolated
  kernel time, launch count, memory traffic, peak memory, or end-to-end time.

Preserve an untouched runnable reference and freeze correctness cases,
development shapes, protected confirmation shapes, tolerances, and the
acceptance rule before tuning. Use exact equality when semantics require it;
otherwise justify tolerances from dtype and accumulation behavior rather than
loosening them until a candidate passes.

Use `$build-benchmark` first when the main missing piece is a trustworthy
correctness or performance evaluator. Use `$optimize-inference` when the real
goal is model-serving performance and kernel work is only one possible
mechanism.

## Establish the baseline

Run the reference on the actual target. Include adversarial and boundary cases
appropriate to the operation: empty and singleton dimensions, odd and large
sizes, non-contiguous inputs, unusual strides, tails, alignment boundaries,
mixed signs, extreme values, NaNs or infinities, and unsupported combinations.
Check forward outputs and backward gradients when the operation participates in
autodiff.

Measure using the target runtime's correct synchronization and timing method.
Separate compilation and warmup from steady-state execution unless startup is
part of the requested metric. Retain per-run timings across representative
shapes; do not report only the fastest sample. Profile enough to identify
whether work is limited by memory traffic, arithmetic, launch overhead,
synchronization, occupancy, register pressure, or another concrete mechanism.

If the target device or toolchain is unavailable, source may still be written
or reviewed when useful, but label it uncompiled and unbenchmarked. Never
simulate CUDA, Metal, or another backend and report that as target-hardware
verification.

## Build bounded candidates

Choose the implementation stack that fits the repository and target rather
than assuming one universal kernel language. Keep the framework fallback until
the new path is verified. Candidate mechanisms may include:

- eliminating redundant launches or fusing compatible operations;
- coalescing accesses, changing layout, reusing buffers, or reducing transfers;
- tiling, vectorization, shared or threadgroup memory, warp or subgroup
  primitives, asynchronous copies, and double buffering;
- specializing bounded shape or dtype regimes while retaining a correct
  fallback for everything else;
- reducing synchronization, divergence, atomics, recomputation, register
  pressure, or unnecessary precision conversions;
- tuning launch geometry or compiler parameters against development shapes.

Keep each candidate's code, compile configuration, rationale, supported domain,
correctness results, profile, timings, and rejection reason. Change one major
mechanism at a time when attribution matters. Autotuning may explore the
development surface, but do not expose protected confirmation cases or select
parameters on them.

Do not use undefined behavior, unsafe out-of-bounds access, architecture
assumptions that are not guarded, hidden host work, stale outputs, skipped
computation, hard-coded benchmark answers, altered precision, or narrower
semantics to manufacture a win. Treat intermittent failures, race conditions,
and unexplained nondeterminism as correctness failures.

## Verify integration and performance

For a prospective winner:

1. rebuild it from the untouched baseline and recorded patch;
2. compile with warnings visible on the target toolchain;
3. compare against the reference across frozen correctness cases and protected
   shapes, including gradients and repeated runs when relevant;
4. use sanitizers, race checkers, validation layers, or memory tools supported
   by the backend when they address credible risks;
5. benchmark under matched clocks, load, synchronization, warmup, allocation,
   and input conditions;
6. measure the real call site or end-to-end path when the requested claim
   extends beyond an isolated kernel.

Accept only a reproducible, practically meaningful gain that passes every
semantic requirement. A faster microbenchmark does not establish application
speedup, and a result on one GPU, dtype, shape family, or software stack does
not generalize to another.

Return the implementation, integration change, exact build and run commands,
target hardware and software receipt, supported and fallback domains,
correctness evidence, baseline and candidate timing distributions, profile
explanation, rejected mechanisms, and remaining limitations. If no candidate
qualifies, preserve the strongest negative evidence and report no verified
improvement.

Do not provision accelerators, rent cloud compute, install large toolchains, or
change production deployments without explicit authority.
