---
name: optimize-inference
description: Optimize an existing model or inference application for a specified workload and hardware target while preserving user-defined output quality. Use when asked to reduce inference latency, memory, or cost; increase throughput; profile an inference stack; tune serving, batching, caching, kernels, runtimes, quantization, model execution, or surrounding application code; or compare deployment configurations on CPU, Apple Silicon/MLX, NVIDIA, or another concrete target.
---

# Optimize Inference

Produce a reproducible end-to-end gain on the user's actual target, not an
isolated benchmark win or an assumed cross-platform improvement.

## Fix the contract

Inspect the application, model and weights, runtime, serving path, existing
tests, representative traffic or inputs, and target hardware before changing
anything. Record:

- the workload distribution, input and output shapes, concurrency, generation
  settings, and service boundaries that matter;
- output-quality invariants and unacceptable regressions, including numerical,
  semantic, safety, schema, and stochastic-behavior requirements as relevant;
- primary performance goals and constraints for latency, throughput, memory,
  cost, startup, or power;
- the exact hardware, OS, drivers, libraries, model and weight identity,
  precision, runtime configuration, and application revision.

Freeze representative development inputs, a protected confirmation sample,
quality gates, and an acceptance rule before optimization. If no defensible
quality evaluator or representative workload exists, use `$build-benchmark`
to create one first. Do not infer that closeness on a few convenient prompts
preserves quality.

## Measure the untouched baseline

Measure the real end-to-end path as well as useful stage timings such as load,
preprocessing, prefill, decode, postprocessing, and queueing. Include the
metrics relevant to the request: cold start, steady-state latency distribution,
time to first output, per-output latency, throughput at target concurrency,
peak host and accelerator memory, and attributable cost.

Use explicit warmup and repeated measured runs. Synchronize asynchronous
accelerators before timing, control or record competing load and power state,
retain per-run results, and report variability rather than only the best run.
Keep cold and warm behavior separate. Confirm that the baseline passes every
quality invariant before treating it as the reference.

## Find the bottleneck

Profile before choosing changes. Determine whether the limiting resource is
model compute, memory bandwidth or capacity, transfers, compilation, launch
overhead, Python or application work, tokenization, I/O, queueing, or serving
policy. Use the target's native profilers when available, but keep measurement
overhead out of acceptance runs.

Interpret target-specific evidence locally:

- On CPU, inspect threading, vectorized kernels, memory layout, NUMA or affinity
  effects, and runtime libraries only when the machine supports them.
- On Apple Silicon or MLX, account for lazy execution, synchronization, Metal
  compilation warmup, unified-memory pressure, and the installed MLX version.
- On NVIDIA, account for CUDA synchronization, driver and toolkit versions,
  kernel selection, compilation, transfers, and available serving engines.
- On other targets, use their native runtime and counters and label unsupported
  measurements plainly.

Never present a gain on one device, precision, runtime, shape, or concurrency
level as portable to another without measuring it there.

## Test bounded changes

Choose the smallest plausible changes from the measured bottleneck. Consider,
as appropriate:

- model execution: precision, quantization, pruning, distillation, speculative
  decoding, sequence handling, or architecture-compatible substitutions;
- runtime and kernels: graph or model compilation, operator fusion, optimized
  attention, allocator settings, layout, threading, and target-native kernels;
- serving: request scheduling, continuous or static batching, concurrency,
  sharding, replicas, streaming, and admission control;
- caching and data movement: prefix or key-value caches, memoization, buffer
  reuse, transfer reduction, preprocessing, and serialization;
- application code: remove duplicated work, unnecessary conversions, blocking
  boundaries, excessive copies, and avoidable I/O.

Treat lossy changes such as quantization or model substitution as quality-risk
changes, not mere runtime switches. Check calibration representativeness and
important slices. Avoid combining many mechanisms before their individual
effects are understood; preserve each candidate's configuration, patch,
measurement, and rejection reason.

If the task is generic evaluator-driven code evolution rather than
inference-specific diagnosis, route candidate search to `$evolve-program` and
keep this skill's workload, quality, and hardware contract as its evaluator.
If profiling isolates a standalone GPU operation and the requested work is to
author or tune its low-level implementation, route that bounded subproblem to
`$optimize-gpu-kernel`, then confirm the result again in this end-to-end
inference workflow.

## Accept only verified gains

Reject candidates that fail any quality invariant, skip required work, alter
the workload, shift cost outside the measured boundary, rely on invalid cache
state, or improve only an unrepresentative microbenchmark. Re-measure promising
candidates against the untouched baseline with the same harness and controlled
conditions. Use fresh processes or reset state when initialization and caches
matter, enough repetitions to exceed observed noise, and fresh confirmation
inputs not used to select the change.

Accept a change only when its end-to-end gain is reproducible, practically
meaningful under the target load, and carries no detected quality regression.
Report the baseline and winner, per-metric uncertainty or run distribution,
quality evidence, hardware and software context, exact changes, rejected
approaches, and remaining coverage limits. State narrowly which workload and
target the result supports. Do not spend money, provision hardware, or mutate
production traffic without explicit authority.
