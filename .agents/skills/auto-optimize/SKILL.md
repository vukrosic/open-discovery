---
name: auto-optimize
description: Analyze and optimize a codebase or repository for a stated performance, memory, cost, or other engineering objective while preserving a frozen baseline and validating every candidate.
---

# Auto-optimize

Use this skill when the user asks to make existing code faster, smaller, cheaper,
more memory-efficient, or otherwise better under a measurable engineering
objective.

## 1. Establish the target and objective

- Identify the exact repository, file, function, command, or workload in scope.
- If the user did not identify the target (for example, no path or name), or it
  cannot be found, ask for clarification before editing.
- Identify the primary objective: latency, throughput, memory, startup time,
  energy, cost, or another metric. If no objective was provided, ask the user;
  do not silently choose one.
- Ask for hard constraints that could change the design: API/behavior
  compatibility, numerical tolerance, supported versions, deployment target,
  hardware, language/runtime restrictions, dependencies, concurrency, and
  maximum acceptable complexity.
- Unless the user specifies otherwise, state that optimization will target the
  current execution environment and hardware, and record OS, hardware, runtime,
  compiler/interpreter, dependency versions, and relevant environment flags.

## 2. Inspect before editing

- Read repository instructions, ownership/status files, and existing tests.
- Locate the real hot path with profiling, tracing, or a representative benchmark;
  do not optimize names or intuition alone.
- Record input shapes, distributions, representative and adversarial cases,
  side effects, determinism requirements, and resource limits.
- Freeze the original implementation as an immutable baseline. Never edit or
  overwrite that baseline while exploring candidates. If a baseline is absent,
  copy the exact source and record its content hash.

## 3. Choose the search structure

Decide explicitly whether to:

- optimize the whole target at once;
- split it into independently measurable units (functions, kernels, stages,
  data movement, or I/O) and optimize those units separately; or
- run both approaches when interactions may matter.

Prefer the smallest decomposition that exposes independent bottlenecks. Record
dependencies between units and avoid combining changes until each component has
its own correctness and performance evidence.

When delegation is available, parallelize independent hypotheses with agents.
Give each agent a bounded unit, immutable baseline reference, constraints, and a
required evidence format. Agents must not overwrite one another's candidates or
the baseline.

## 4. Design the evaluator before trusting candidates

Create or reuse an evaluator that is independent of the candidate and includes:

- exact API/signature and side-effect checks;
- deterministic correctness tests plus seeded randomized tests;
- representative, boundary, adversarial, and held-out inputs;
- numerical comparisons with tolerances justified by the baseline and dtype;
- gradient/state/serialization/concurrency checks when applicable;
- mutation, aliasing, non-contiguous, empty, and error-path checks where relevant;
- performance measurement after warmup, with synchronization appropriate to the
  hardware, resident inputs, repeated trials, median and tail statistics, and
  randomized/interleaved candidate-vs-baseline order;
- an environment and dependency receipt, source hashes, seeds, and raw timings.

The evaluator must not reward a candidate for changing the problem, skipping
work, caching test answers, detecting benchmark fixtures, calling the original
implementation as a hidden fallback, or weakening correctness criteria. Add
static scans and mutation/input-independence probes for these traps when useful.
Separate correctness failure, speed regression, noisy/inconclusive timing, and
unsupported-regime results. Do not promote a candidate on a single noisy run.

## 5. Explore and verify

- Generate multiple candidates from distinct hypotheses (algorithm, data layout,
  batching, parallelism, compiler, specialized kernel, memory movement, or
  language/runtime changes) only when each remains within the constraints.
- Run correctness first; discard or preserve failed candidates with their
  evidence rather than hiding them.
- Benchmark promising candidates against the frozen baseline on the declared
  target regime and nearby held-out regimes. Report median, mean, dispersion,
  tails, trial count, and uncertainty; distinguish a narrow win from a general
  win.
- Re-run promising wins independently. Investigate outliers, thermal/load
  effects, compilation/warmup costs, synchronization, and measurement overhead.
- Keep baseline, evaluator, candidates, raw evidence, and decision notes
  traceable by content hash.

## 6. Handoff

Report the winning candidate (if any), exact supported regime, measured change,
correctness result, limitations, reproduction command, and whether it is safe to
promote. If no candidate beats the baseline with sufficient evidence, report a
bounded negative result and the best next hypothesis. Never call an optimization
successful merely because it compiles or passes a single example.
