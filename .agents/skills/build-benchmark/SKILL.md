---
name: build-benchmark
description: Turn an existing repository, system, algorithm, model, workflow, or desired outcome into a trustworthy runnable evaluation setup before optimization or research. Use when the user asks to define correctness, build a benchmark or evaluator, choose representative workloads and metrics, establish baselines and measurement noise, protect held-out checks, detect reward hacking, or prepare an evaluation contract for $evolve-program or another experiment loop.
---

# Build Benchmark

Build the smallest evaluation setup that can distinguish real improvement from
bugs, noise, overfitting, and metric exploitation. Adapt the evaluator to the
target and use the repository's existing test and measurement conventions when
they are sound.

## Establish what success means

Inspect the target, surrounding tests, documentation, usage evidence, data,
constraints, and existing evaluators before writing benchmark code. Infer
routine details from those artifacts and the user's requested outcome.

Identify:

- the real capability or outcome the score is meant to represent;
- correctness invariants and unacceptable regressions;
- important operating regimes, edge cases, and resource constraints;
- the decision the evaluation must support and what difference would matter.

Separate requirements supported by domain truth from plausible assumptions.
Ask one concise question only when genuinely unavailable information would
materially determine correctness and no safe conservative interpretation or
cheap discriminator exists. If representative data or authoritative truth is
missing, build only the defensible partial evaluation and label the resulting
validity gap; do not call it a trustworthy benchmark.

## Design representative evidence

Choose workloads that cover the target's real use distribution and important
failure modes without imposing a fixed suite size or format. Prefer observed
inputs, accepted reference outputs, domain laws, independent implementations,
or expert-reviewed cases over convenient synthetic proxies. Use synthetic or
microbenchmark cases when they isolate a useful mechanism, and state what they
cannot establish.

Choose metrics only after defining the represented outcome. Include all of:

- a correctness gate or explicit validity classification where correctness is
  not binary;
- primary metrics tied to the intended capability;
- regression and safety checks for important invariants;
- cost, latency, memory, throughput, or robustness measures when relevant;
- simple baselines that reveal whether the task or metric is trivial.

Measure the untouched current system and at least one meaningful naive,
reference, or prior baseline when available. Preserve failures as evidence.

## Control noise and optimization leakage

Estimate variability from the actual sources of noise: repeated runs, input
sampling, seeds, warmup, machine state, raters, stochastic services, or timing
order as applicable. Select repetitions and aggregation from observed
variance and decision risk rather than a universal count. Report uncertainty,
run conditions, and the smallest improvement the setup can resolve.

Before optimization begins, actively list ways an optimizer could raise the
score without improving the intended outcome. Check for hard-coding,
memorization, data leakage, skipped work, evaluator detection, invalid output,
resource shifting, cherry-picked subsets, and metric-specific shortcuts as
relevant to the target. Add invariants, adversarial cases, cross-checks, or
secondary metrics that expose credible exploits.

When repeated tuning could overfit the evaluation, separate fast development
feedback from a protected confirmation set or procedure. Keep confirmation
cases inaccessible to candidate authors when feasible, limit their use, and
record any exposure. Do not describe reused or revealed cases as held out.

## Implement a runnable evaluator

Place the evaluator beside the target's existing test or benchmark machinery
unless the user specifies another location. Reuse dependencies already present
where practical. Make one documented command or entry point run the evaluation
non-interactively and return machine-readable results suitable for an
experiment loop.

Make the evaluator:

- reject invalid candidates before scoring performance;
- keep evaluation code and immutable inputs outside candidate-owned writes;
- record enough environment, workload, metric, and version identity to compare
  runs honestly;
- preserve per-case or sufficiently granular results for diagnosis;
- use clear exit behavior and actionable failure messages;
- avoid silently changing the benchmark when a dependency or case fails.

Adapt the result schema to existing repository conventions. At minimum expose
validity, primary score or outcome, relevant secondary metrics, and the
benchmark identity. Do not create a new framework when a small script, test
target, configuration, or adapter makes the existing machinery runnable.

## Verify and hand off

Run the evaluator against the untouched target and the chosen baselines.
Deliberately exercise an invalid candidate and at least one credible
score-hacking attempt when safe and feasible. Repeat enough measurements to
confirm that observed ordering is larger than relevant noise. Inspect emitted
artifacts rather than trusting terminal summaries.

Freeze the evaluator, workloads, metric definitions, baseline results, and
decision rule before handing them to `$evolve-program` or another experiment
loop. Explain which surfaces candidates may modify and which evaluation
surfaces are protected. If the benchmark must change later, version it and
mark results across incompatible versions as non-comparable.

Report separately:

- whether the evaluator runs and distinguishes the tested systems;
- what scientific or operational claim the evidence supports;
- what remains unvalidated because of missing truth, coverage, power, or
  representativeness;
- how an optimization loop should invoke it without contaminating confirmation.

Never equate a higher benchmark score with real-world or scientific validity
unless the evaluation evidence supports that link.
