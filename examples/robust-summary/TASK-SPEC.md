# Task specification

## Objective

Find a simple summary rule that lowers absolute error relative to the arithmetic
mean in every frozen positive- and negative-spike case.

## Current baseline or point of comparison

The arithmetic mean of all five readings in each case.

## Success criteria

Before replacing the baseline, a candidate must satisfy every condition:

1. Produce lower absolute error than the arithmetic mean in all four cases.
2. Use one unchanged rule for positive and negative spikes.
3. Preserve inputs and calculations so every result can be checked by hand.

## Validation stages

### Entry screen

Check one positive-spike and one negative-spike case. Stop the candidate if
either has error greater than or equal to the baseline.

### Main validation

Compare the candidate with the baseline on all four frozen cases.

### Robustness or transfer

Require case-level improvement in both spike directions. A lower average error
cannot hide a failed required case.

## Evidence contract

- Preserve the constructed inputs and exact calculations.
- Separate arithmetic results from interpretation.
- Record the rule before applying it.
- Do not change or exclude cases after seeing the outcome.
- Do not imply that this teaching example establishes real sensor performance.

## Iteration rules

- Base the next idea on completed evidence.
- Test one estimator at a time.
- Stop at the first frozen failure gate.
- After two stale iterations, change mechanism.
- Update every project ledger before another run.

## Session boundary

- Maximum iterations: 1.
- Maximum active time: 30 minutes.
- Review required when: the run is complete or any frozen case fails.

## Completion rule

The project is complete when one estimator passes all three success criteria or
the researcher stops the search and records why.
