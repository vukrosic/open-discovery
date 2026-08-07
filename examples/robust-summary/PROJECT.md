# Project

> Teaching example only. The data are constructed, not real sensor readings.

## Research question

Which simple summary, if any, estimates a known center of `10.0` more reliably
than the arithmetic mean when exactly one of five readings contains a sensor
spike of unknown direction?

## Why it matters

Choosing a summary rule changes whether a small measurement pipeline reports a
stable central value or is pulled toward a faulty reading.

## Current evidence

### Direct evidence

- Four constructed five-reading cases are frozen before evaluation.
- Two contain a positive spike and two contain a negative spike.
- The known center is `10.0` in every case.

### Assumptions

- One reading per case is contaminated.
- The spike direction is not known when the summary rule is chosen.
- Absolute error from `10.0` is the relevant loss.

### Unknowns

- Whether dropping the largest reading works across both spike directions.
- Which symmetric rule should be tested if the one-sided rule fails.

## Research context

- Discipline or community: introductory measurement and robust statistics.
- Object, population, system, text, archive, phenomenon, or body of work:
  constructed five-reading batches with one contaminated value.
- Available sources, materials, data, tools, or access: the values and exact
  arithmetic preserved in this project.

## Constraints

- Compute and device: arithmetic that can be checked by hand.
- Time: one bounded comparison per iteration.
- Cost: zero.
- Research constraints: constructed teaching data only.
- Data constraints: no personal or restricted data.
- Access and external contact: none.
- Actions that are forbidden: replacing cases after seeing the result or
  presenting constructed values as real observations.

## Human–AI authority

- Collaboration mode: approval per experiment.
- The AI may do without asking: inspect files, verify arithmetic, and draft one
  evidence-based next idea.
- The AI must ask before: approving or running another experiment, changing a
  frozen gate, expanding the dataset, or making an external claim.
- Session limit: one experiment.
- Immediate stop conditions: inconsistent source values, ambiguous decision
  rule, or missing human approval.

## Researcher judgment

- Current suspicion: dropping the largest value will handle positive spikes
  but fail when the spike is negative.
- A surprising outcome would be: the rule improves all four cases.
- A useful result would change: which estimator is tested next.
