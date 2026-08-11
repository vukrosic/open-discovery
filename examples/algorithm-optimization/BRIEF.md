# Algorithm optimization experiment

## 1. What question is being asked?

Can an agent generate a faster implementation of connected-component
detection without changing its exact output?

## 2. What inputs and permissions exist?

The input is a graph with `n` vertices and an edge list. `baseline.py`, the
fixtures, and the evaluator are available as the reference. The work is fully
digital and has no external access, network, or wet-lab step. The baseline and
earlier candidates are read-only.

## 3. What can be changed?

The agent may create new implementations under
`candidates/candidate-NNN/solution.py` with the same
`connected_components(n, edges)` interface. It may not overwrite the baseline,
the evaluator, fixtures, or an earlier candidate.

## 4. How is success measured?

The candidate must exactly match the baseline on every fixture and have any
positive paired median runtime improvement on the large fixture. Correctness
failure rejects the candidate. Unstable timing is reported as
`STOCHASTIC-OPEN`, not as an improvement.

## 5. What evidence was produced?

Each candidate preserves its source, notes, and structured `RESULT.json` with
correctness checks, timings, and the final decision.

## 6. What is missing or uncertain?

The benchmark is a bounded graph fixture, so a measured speedup may not
generalize to other graph sizes, shapes, hardware, or workloads.

## 7. When must the agent stop and ask a human?

Stop if the required interface, evaluator, fixtures, or comparison procedure is
missing or materially unclear. Do not invent a reproduction or change the
reference to make a candidate pass.
