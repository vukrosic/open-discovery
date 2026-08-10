---
name: evolve-program
description: Improve a baseline program against a human-supplied evaluation script using independent AI-generated candidates, external correctness and performance measurement, preserved candidate evidence, and clean winner verification. Use when the user provides or identifies baseline code plus an evaluator, requests AlphaEvolve-style program evolution, asks agents to optimize code against a measurable objective, or wants to compare optimization ability across AI models over time.
---

# Evolve Program

Read `program-evolution/README.md` completely before acting. Use its scripts and
evaluator contract rather than inventing another layout or measurement format.

## Start safely

Use the supplied baseline, evaluator, and goal. If paths already belong to an
Open Discovery initiative, work there. Otherwise create one initiative and one
owned project while preserving the request in `BRIEF.md`.

Never modify the original baseline or evaluator. Run
`program-evolution/scripts/lock_baseline.py` first. Treat a failed lock as a
setup problem; do not begin candidate search until the untouched baseline is
valid and measurable.

If the user asked only to prepare or lock the inputs, stop after this step.

## Evolve candidates

Use `program-evolution/prompts/propose-candidate.md` for bounded mutation work.
Give each concurrent worker a unique candidate folder. Let workers inspect the
parent code and relevant prior evidence, but do not expose confirmation cases
or allow writes to evaluation code.

Balance exploitation of strong parents with independent mechanisms and
occasional restarts. Reject invalid candidates. Preserve concise lineage,
patches, metrics, and failure reasons. Do not treat repeated edits by one owner
as independent verification.

Use the model and reasoning guidance in `AGENTS.md`; do not assume maximum
reasoning is useful for every mechanical mutation. Serialize only genuinely
exclusive compute.

## Measure and finish

Record comparable runs with `program-evolution/scripts/run_benchmark.py` when
evaluating agent capability over time. Compare only records with the same
benchmark and evaluator hashes.

Reconstruct a promising winner from the locked baseline, apply only its
recorded patch, and rerun correctness plus fresh confirmation workloads. Report
the verified scope, end-to-end improvement, regressions checked, environment,
and limitations. A candidate that only improves a microbenchmark is not an
end-to-end improvement.

Local, zero-cost, non-destructive work implied by the request is allowed.
Spending, cloud compute, publication, external communication, private access,
credentials, or destructive actions require explicit authority.
