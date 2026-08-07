# Experiment protocol

## Identity

- Experiment ID: EXP-001
- Idea ID: IDEA-001
- Status: Approved
- Date frozen: 2026-08-07 09:10
- Researcher or owner: Example researcher

## Question

Does removing the largest reading and averaging the other four produce lower
absolute error than the five-reading arithmetic mean in every frozen case?

## Mechanism or rationale

A positive spike pulls the arithmetic mean upward. Removing the largest value
could reduce this distortion. It is unknown whether the same rule remains
useful when the spike is negative.

## Current baseline

The arithmetic mean of all five readings, evaluated by absolute error from the
known center `10.0`.

## Method

For cases A through D:

1. Calculate the arithmetic mean of all five readings.
2. Remove exactly one largest reading and average the remaining four.
3. Calculate both absolute errors from `10.0`.
4. Compare errors case by case.
5. Stop and reject at the first case where candidate error is greater than or
   equal to baseline error, while preserving all planned calculations.

## Inputs and scope

- Sources, data, materials, prompts, participants, or objects: four constructed
  cases in [`../../evidence/EXP-001-calculations.md`](../../evidence/EXP-001-calculations.md).
- Inclusion and exclusion rules: include all four frozen cases; exclude none.
- Versions and environment: decimal arithmetic shown directly in Markdown.
- Seeds or ordering, when relevant: fixed order A, B, C, D.

## Evidence to preserve

- Raw inputs: all 20 constructed values.
- Raw outputs: baseline and candidate summaries and errors.
- Logs and measurements: exact calculations for each case.
- Provenance and versions: identify the data as constructed teaching values.
- Deviations: record any changed value, rule, or case order.

## Decision rule

### Continue or call successful when

- Candidate absolute error is strictly lower than baseline error in all four
  cases.

### Reject when

- Candidate error is greater than or equal to baseline error in any case.

### Call inconclusive when

- An input or calculation cannot be recovered or independently checked.

## Constraints and authority

- One experiment, zero cost, no external data or contact.
- Do not alter cases or gates after calculation begins.
- Do not present the constructed values as real observations.
- Human approval is required before any follow-up experiment.

## Stop conditions

Stop if the source values conflict, the decision rule becomes ambiguous, or a
required calculation cannot be preserved.

## Approval

- [x] The question is the one the researcher intends to test.
- [x] The method and evidence standard are appropriate.
- [x] The decision rule was frozen before execution.
- [x] The costs, risks, and authority boundaries are acceptable.
