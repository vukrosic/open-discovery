---
name: optimize-agent
description: Improve an existing AI agent, system prompt, tool set, model choice, retrieval configuration, or agent workflow against user-provided or agent-built evaluations while protecting quality and safety. Use when the user asks to tune, optimize, compare, or reduce the cost or latency of an agentic system and wants measured, reproducible evidence rather than subjective edits. Route generic program-performance evolution to $evolve-program and substantial evaluator construction to $build-benchmark.
---

# Optimize Agent

Improve agent behavior only when comparable evidence supports the change. Adapt
the search and measurements to the target; do not impose a universal harness or
scorecard.

## Route and bound the task

Inspect the target, its current configuration, available evaluations, usage
evidence, constraints, and allowed resources before editing.

- Use `$evolve-program` when the main target is generic source-code or runtime
  performance against an external evaluator.
- Use `$build-benchmark` first when constructing or repairing a trustworthy
  evaluator is the main work. Resume optimization only after its contract is
  frozen.
- Stay here when the meaningful interventions concern agent prompts, tools,
  models, retrieval, orchestration, or workflow policy.

Define which surfaces candidates may change. Do not mutate production state,
spend money, access private systems, or expand authority merely because an
optimization would benefit from it.

## Freeze the claim before tuning

Preserve an untouched, runnable baseline and record the exact prompt,
configuration, tools, model identifiers, retrieval inputs, code, environment,
and evaluator version needed to reproduce it.

Before examining candidate outcomes, define:

- the real capability the evaluation is intended to represent;
- quality and safety invariants that no candidate may violate;
- representative cases, failure checks, and important operating regimes;
- relevant quality, latency, cost, and reliability measures;
- the uncertainty, practical improvement threshold, and decision rule;
- a development surface and protected held-out confirmation when repeated
  tuning could overfit.

Measure the untouched baseline under the frozen contract. Repeat stochastic or
noisy measurements enough to estimate decision-relevant variation. Distinguish
measured cost from estimates, warm from cold latency when material, and hard
failures from output-quality variation. If the available evaluation cannot
support the requested claim, narrow the claim or route to `$build-benchmark`.

## Search without gaming the evaluation

Diagnose baseline failures and form explicit improvement hypotheses. Prioritize
cheap, reversible interventions, but compare model, prompt, tool, retrieval,
and workflow changes when the evidence makes them plausible. Change one factor
at a time when attribution matters; test coherent bundles when interactions are
the hypothesis.

Keep each candidate isolated from the baseline and protected evaluation
surfaces. Preserve enough candidate-local evidence to reconstruct and compare
it: parent, exact changes, rationale, environment, per-case results, aggregate
metrics, traces or errors needed for diagnosis, and rejection reason. Retain
negative candidates; do not rewrite history around the winner.

Actively test how a candidate could raise the score without improving the
intended capability. Check for memorization, leaked answers, evaluator
detection, skipped work, invalid output, selective abstention, hidden human
labor, shifted resource costs, benchmark-specific phrasing, and tool or
retrieval shortcuts as relevant. Reject invalid candidates before ranking
them. Never tune the evaluator to rescue a candidate or silently compare
results across changed evaluation versions.

Use development feedback adaptively, favoring informative mechanisms over a
fixed trial count. Avoid repeatedly exposing or tuning on confirmation cases.
Add adversarial, distribution-shift, blinded, or human checks when they address
a credible exploit or validity gap, not as ceremony. Stop when a candidate
clears the frozen rule, plausible mechanisms are exhausted, evidence cannot
resolve the difference, or the next test is not worth its cost and risk.

## Confirm and report

Reconstruct any prospective winner from the untouched baseline using only its
recorded changes. Rerun correctness and safety checks, then use the protected
held-out set or another fresh confirmation procedure when feasible. Compare
quality, latency, cost, and reliability under matched conditions and report
uncertainty and material tradeoffs; keep Pareto alternatives when no single
candidate dominates.

Return an improvement only when confirmation satisfies the frozen decision
rule and every invariant. Report the verified scope, exact change, baseline and
winner evidence, regressions checked, resource tradeoffs, and limitations. If
no candidate qualifies, return an honest negative or inconclusive result with
the strongest evidence and failed mechanisms. Never label a development-only
gain, exposed holdout, proxy-score increase, or safety regression as an
improvement.
