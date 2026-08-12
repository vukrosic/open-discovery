---
name: auto-optimize
description: Analyze and optimize a codebase or repository for a stated performance, memory, cost, or other engineering objective while preserving a frozen baseline and validating every candidate.
---

# Auto-optimize

Use this skill when the user asks to make existing code faster, smaller, cheaper,
more memory-efficient, or otherwise better under a measurable engineering
objective.

Use judgment throughout. Adapt the depth of analysis, search, and validation to
the size, risk, and ambiguity of the task. The points below are reminders, not a
mandatory checklist; a small function may need only a small trustworthy test,
while a complex system may justify profiling, decomposition, and parallel search.

## 1. Establish the target and objective

- Identify the exact repository, file, function, command, or workload in scope.
- If the user did not identify the target (for example, no path or name), or it
  cannot be found, ask for clarification before editing.
- Identify the primary objective: latency, throughput, memory, startup time,
  energy, cost, or another metric. If no objective was provided, ask the user;
  do not silently choose one.
- Discover constraints from the request, code, tests, and environment. Ask only
  about missing constraints that could materially change the optimization, such
  as compatibility, numerical tolerance, deployment hardware, dependencies, or
  acceptable complexity.
- Unless the user specifies otherwise, state that optimization will target the
  current execution environment and hardware. Record the environment details
  needed to interpret or reproduce the eventual claim.

## 2. Inspect before editing

- Read repository instructions, ownership/status files, and existing tests.
- Locate the real hot path using the lightest useful evidence: inspection may be
  enough for a tiny function; use profiling, tracing, or representative
  benchmarks when the bottleneck is uncertain or system interactions matter.
- Understand the inputs and behavior that matter, including relevant edge cases,
  side effects, determinism, and resource limits.
- Understand the parts of the execution system that could shape the solution,
  such as hardware and accelerators, memory and data movement, concurrency,
  runtimes and compilers, available extension mechanisms, and deployment
  constraints. Verify important capability assumptions from the current
  environment or authoritative documentation before choosing or dismissing a
  path.
- Freeze the original implementation as an immutable baseline. Never edit or
  overwrite that baseline while exploring candidates. If a baseline is absent,
  copy the exact source and record its content hash.

## 3. Choose the search structure

Choose whichever search structure best fits the target:

- optimize the whole target at once;
- split it into independently measurable units (functions, kernels, stages,
  data movement, or I/O) and optimize those units separately; or
- run both approaches when interactions may matter.

Prefer a useful decomposition when it exposes independent bottlenecks, but do
not split code merely to satisfy the workflow. Whole-system and unit-level
search may both be useful when interactions matter.

When delegation would improve the search, consider parallelizing independent
hypotheses or using agents as a branching search tree: explore different paths,
deepen the promising ones, and stop weak branches when evidence warrants it.
This is optional; do not create agents merely to satisfy a quota. Keep ownership
clear enough that agents do not overwrite the baseline or one another's
candidates.

## 4. Design the evaluator before trusting candidates

Create or reuse an evaluator independent of the candidate. Make it proportionate
to the claim. Select relevant checks such as:

- exact API/signature and side-effect checks;
- deterministic correctness tests plus seeded randomized tests;
- representative, boundary, adversarial, and held-out inputs;
- numerical comparisons with tolerances justified by the baseline and dtype;
- gradient/state/serialization/concurrency checks when applicable;
- mutation, aliasing, non-contiguous, empty, and error-path checks where relevant;
- performance measurement after warmup, with synchronization appropriate to the
  hardware, resident inputs, repeated trials, median and tail statistics, and
  randomized/interleaved candidate-vs-baseline order;
- awareness of possible measurement interference such as competing CPU or
  accelerator work, memory pressure, thermal or power state, lingering workers,
  compilation, warmup, caching, and synchronization. Check, control, or report
  these when they could materially affect the result;
- an environment and dependency receipt, source hashes, seeds, and raw timings.

The evaluator should not reward a candidate for changing the problem, skipping
work, caching test answers, detecting benchmark fixtures, calling the original
implementation as a hidden fallback, or weakening correctness criteria. Keep
these failure modes in mind and add targeted checks when plausible.
Separate correctness failure, speed regression, noisy/inconclusive timing, and
unsupported-regime results. Do not promote a candidate on a single noisy run.

## 5. Explore and verify

- Explore the most promising mechanisms for the target, whether that means one
  obvious candidate or several distinct hypotheses involving the algorithm,
  data layout, batching, parallelism, compiler, kernel, memory movement, or
  language/runtime.
- Run correctness first; discard or preserve failed candidates with their
  evidence rather than hiding them.
- Benchmark promising candidates against the frozen baseline on the declared
  target regime and useful nearby or held-out regimes. Use enough repetitions
  and statistics to support the strength of the claim; distinguish a narrow win
  from a general win.
- Confirm promising wins with rigor proportional to the claim. Investigate
  outliers or environmental effects when they could change the decision.
- During longer searches, preserve useful candidates and evidence as work
  progresses so an interruption does not erase the learning.
- Keep enough provenance to reproduce and understand the result; use hashes and
  raw evidence when the claim warrants them.

## 6. Handoff

Report the winning candidate (if any), supported regime, measured change,
correctness result, important limitations, enough detail to reproduce it, and
whether it is safe to promote. If no candidate beats the baseline with sufficient
evidence, report the bounded result and best next hypothesis. Never call an
optimization successful merely because it compiles or passes a single example.
