---
name: design-scientific-study
description: Turn a scientific question, hypothesis, available resources, and constraints into an execution-ready study or experiment plan with an explicit target, design, controls, sampling, measurements, analysis, stopping rules, failure checks, and reproducibility details. Use before conducting experimental, observational, computational, field, survey, or human-subject research, including feasibility and pilot studies. Do not use to analyze an already collected dataset or audit a completed finding; use Analyze Scientific Data or Audit Research Result instead.
---

# Design a Scientific Study

Produce the smallest credible plan that can answer the scientific question or
support the intended decision. Adapt the design to the field, evidence stage,
resources, and consequences of error. Treat the output as a proposed study,
never as evidence that the study was conducted.

## Frame the target

Inspect the question, hypothesis, prior evidence, available materials,
constraints, and repository conventions. Establish:

- the decision the evidence must support and the claim that a positive,
  negative, or inconclusive result could justify;
- the population or system, intervention or exposure, comparator, outcome,
  and relevant time horizon;
- the estimand, prediction target, mechanistic contrast, descriptive quantity,
  or other decision target, including its unit and direction;
- the smallest effect, precision, capability difference, or qualitative
  distinction that would matter;
- what is known, assumed, unavailable, and outside the study's authority.

Convert a broad hypothesis into one primary answerable question. Keep secondary
or exploratory questions separate. Do not force a causal estimand when the
available design can support only description, association, prediction, or
feasibility.

Resolve routine choices with conservative, reversible assumptions and label
them. Ask one concise question only when missing information would change the
primary target, design family, ethical feasibility, or resource envelope and
cannot be resolved from supplied artifacts. If the gap does not prevent a
useful plan, provide a conditional branch instead of interrupting.

## Choose a design that can identify the target

Select the simplest design that can distinguish the proposed explanation from
its strongest plausible alternative. Consider experimental, quasi-experimental,
observational, longitudinal, cross-sectional, computational, simulation,
measurement, qualitative, or mixed designs as appropriate.

Define the experimental or observational unit and the independent unit of
replication. Specify eligibility, sampling frame, recruitment or case selection,
conditions, controls or comparators, allocation ratio, timing, follow-up, and
the number and placement of repeated measurements. Do not count technical
replicates, repeated observations, patches, cells, trials, or outputs as
independent samples when assignment occurs at a higher level.

Use randomization, blocking, stratification, counterbalancing, concealment, or
blinding only where they address a real bias source and are operationally
possible. State exactly who or what is randomized and when. For observational
work, state the identification assumptions and the measured variables needed
to make the target interpretable; narrow the claim when key confounders cannot
be controlled.

Trace condition assignment against batch, site, time, operator, device,
subject, order, and preprocessing. If the focal condition is perfectly
confounded with one of them, mark the proposed contrast as non-identifiable.
Recover by changing assignment, crossing conditions within blocks, adding an
appropriate comparator, or narrowing the target. Do not promise that a later
statistical adjustment will repair a design with no overlap or independent
variation.

## Specify measurements and quality controls

Define the primary outcome and only the secondary outcomes that materially
improve interpretation. For each material measurement, specify operational
definition, unit, instrument or rubric, timing, aggregation, calibration or
quality control, missingness or failure meaning, and assessor masking when
relevant. Prefer validated or directly interpretable measures; explain the
construct gap when a proxy is necessary.

Include positive, negative, sham, baseline, reference, manipulation, or process
controls only when they diagnose a credible failure. Distinguish a true null
effect from failed delivery, failed measurement, contamination, drift, or an
underpowered study.

## Justify the amount of evidence

Give a transparent sample or run rationale tied to the independent unit and
decision target. Use a power or precision calculation when its assumptions are
defensible, naming the effect scale, variance or event-rate basis, error rates,
allocation, clustering or repeated-measure structure, expected attrition, and
calculation method. When inputs are unknown, propose a bounded pilot that
estimates feasibility or variance without pretending to test the final claim,
then state how the main-study size will be recalculated.

For simulation, benchmark, rare-event, or qualitative work, replace formulaic
power with the appropriate coverage, uncertainty, replication, saturation, or
information rationale. Never invent a convenient effect size or claim that an
arbitrary sample count is adequate.

## Prespecify analysis and decisions

Map each primary question to its analysis before result-bearing observations
are inspected. Specify the analysis population, exclusions, unit of analysis,
contrast or model, covariates fixed in advance, dependency structure,
uncertainty method, missing-data handling, multiplicity treatment, diagnostics,
and sensitivity check for the leading assumption or confound. Preserve pairing,
blocking, clustering, repeated measures, censoring, and temporal ordering.

Freeze outcome definitions, important transformations, exclusion rules,
primary comparisons, and success or failure criteria before confirmation.
Label flexible model development, subgroup search, threshold selection, and
mechanism exploration as exploratory. Reserve untouched data, seeds, sites, or
runs for confirmation when iterative tuning could leak into evaluation.

Define outcomes that lead to distinct decisions: success, informative failure,
inconclusive evidence, and design or measurement failure. Set stopping rules
for completion, precision, futility, safety, feasibility, resource exhaustion,
or sequential looks only where relevant, including who applies them and what
happens next. Do not use optional stopping or revise thresholds after seeing
results without recording the deviation and changing the claim status.

## Stress-test feasibility and validity

Identify the few failure modes most likely to invalidate the result, such as
selection bias, attrition, noncompliance, contamination, carryover, batch or
site effects, temporal drift, leakage, pseudoreplication, instrument limits,
observer effects, unmeasured confounding, model misspecification, or metric
gaming. For each decisive risk, add a prevention, diagnostic, recovery, or
explicit limit. Run a paper walkthrough from assignment through measurement,
analysis, and decision; repair contradictions before calling the plan ready.

Check that the proposed resources, schedule, dependencies, skills, and data
access are plausible. Mark ethics review, consent, biosafety, privacy review,
permissions, preregistration, specialized facilities, procurement, or external
services as prerequisites when applicable. Never claim that approval, consent,
access, staffing, equipment, or funding exists unless documented.

## Make execution and reproduction unambiguous

Deliver one coherent protocol in the format appropriate to the repository or
user. Include, when material:

- the primary question, target, scope, and proposed-study status;
- design diagram or sequence, units, sample rationale, groups, allocation,
  controls, and masking;
- measurements, data provenance, quality checks, and collection schedule;
- frozen analysis, decision rules, stopping criteria, and confirmatory versus
  exploratory boundary;
- confounds, assumptions, failure modes, mitigations, and remaining limits;
- resources and prerequisites, roles, versioned materials or code, random-seed
  handling, environment, data schema, and exact execution order;
- a brief readiness verdict: ready to execute, ready only after named
  prerequisites, or not yet identifiable or feasible.

Make enough detail durable for another qualified researcher to execute and
audit the plan without chat history, but do not bury the scientific logic in a
universal form or checklist. State unresolved choices and the trigger for each
conditional branch.

This skill designs studies. Do not perform physical experiments, recruit or
contact participants, procure materials, spend money, start external services,
or claim results. Do not describe simulated examples, pilot intentions, or
planned checks as completed observations. If asked to execute the study, hand
off only the authorized computational or operational portion to the appropriate
workflow and keep the distinction between planned and observed evidence clear.
