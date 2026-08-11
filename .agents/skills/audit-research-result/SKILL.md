---
name: audit-research-result
description: Independently assess whether an existing scientific finding, engineering result, optimization, paper, report, experiment, or repository is supported by its primary artifacts. Use when asked to audit, validate, challenge, review, falsify, reproduce-check, or judge the evidence, methods, claims, novelty, limitations, or readiness of a claimed result. Use Feature Tester instead when the main task is exercising product behavior rather than evaluating a research claim.
---

# Audit a Research Result

Assess the result from its primary artifacts and return an evidence-backed
judgment. Treat chat messages, summaries, and owner conclusions as leads, not
evidence.

## Establish the audit target

Identify the exact consequential claim, contribution type, governing question,
conditions, and intended audience or decision. Resolve the artifact location
from the request and available workspace before asking the user to find it.
Ask one concise question only when the target itself remains ambiguous.

Read the governing brief or protocol and the claim-bearing artifacts. These may
include source data, code, configurations, environments, logs, raw outputs,
analysis, figures, reports, negative results, deviations, and version records.
Use fresh reasoning rather than inheriting the project's verdict. State when
the audit is a same-owner review rather than independent verification.

Review existing artifacts read-only by default. Do not silently edit the work,
repair its evidence, widen the mission, acquire costly resources, rerun
expensive or long work, publish, or communicate externally. Run a cheap,
bounded, non-destructive check only when it is within the user's authority,
cannot contaminate the target, and can materially change the judgment;
otherwise recommend it as follow-up. Keep any temporary material isolated and
remove only what this audit created.

## Trace claims to evidence

For each claim that could change the verdict, locate the primary artifact that
directly supports it and follow the derivation far enough to test the reported
result. Reconcile report prose, tables, figures, code, and raw outputs rather
than assuming they agree. Distinguish missing evidence, inaccessible evidence,
and contradictory evidence.

Choose only the checks relevant to the field and claim. Consider, when useful:

- provenance, protocol timing, exclusions, deviations, selective reporting,
  and preservation of counterexamples or negative outcomes;
- construct validity, assumptions, controls, confounders, alternative
  explanations, edge cases, and boundary conditions;
- leakage, split contamination, repeated holdout use, metric gaming, post-hoc
  thresholds, or evaluator changes;
- baseline strength and fairness, implementation correctness, benchmark
  comparability, resource accounting, regressions, and operational tradeoffs;
- units, denominators, uncertainty, statistical design, multiple comparisons,
  practical significance, and whether the data support the stated scope;
- exact inputs, dependencies, versions, commands, seeds, and whether another
  party could reproduce the material result;
- nearest prior work and the precise novelty boundary when novelty matters;
  search primary literature as needed, but never treat a limited search or an
  absence of matches as proof of novelty;
- whether wording confuses finite evidence with proof, association with cause,
  simulation with real-world validation, or constrained improvement with a
  universal advantage.

Actively seek the strongest plausible counterexample or alternative
explanation. Prefer a decisive falsification attempt over a broad checklist.
Stop when the evidence determines the judgment or when the next useful check
requires new authority, material cost, or a separate reproduction effort.

## Return the judgment

Lead with a plain verdict such as supported as stated, supported only with a
narrower claim, inconclusive pending specific evidence, or not supported. Adapt
the wording to the field and intended use rather than forcing a universal
scorecard.

Report:

- the exact claim, artifact identity or version, and scope audited;
- the strongest direct support and the few decisive weaknesses or failed
  falsification attempts;
- the narrowest claim the evidence does support, if different;
- correctness, reproducibility, novelty, and importance separately when those
  distinctions matter;
- confidence and limitations, including artifacts not inspected and checks not
  run;
- the single smallest useful follow-up verification, what uncertainty it
  resolves, and whether it needs additional authority or resources.

Do not hide a negative or inconclusive result behind a long recommendation
list. Do not call a same-implementation rerun independent verification, a
partial run a reproduction, or a search result a novelty finding.
