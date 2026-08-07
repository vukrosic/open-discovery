# Evidence standard

Open Discovery does not impose one scientific method on every field. It does
require that the project state what counts as evidence before making a claim.

## Every claim needs one of three labels

- **Observed:** directly supported by the preserved record.
- **Inferred:** a reasoned interpretation of observed evidence.
- **Unknown:** not established by the current work.

## Freeze gates before outcomes

A protocol should define:

- the comparison or reference point;
- the required observations or arguments;
- relevant controls or counterexamples;
- success, rejection, and inconclusive conditions;
- case-level requirements that an average must not hide;
- resource and stopping limits.

If a gate is discovered to be wrong, preserve the original outcome and record
a correction. Do not retroactively describe the run as having passed.

## Match evidence to the claim

| Claim | Minimum appropriate evidence |
| --- | --- |
| A component dominates cost | A transparent profile; no end-to-end speed claim |
| A change is locally promising | Direct paired screen on representative inputs |
| A method improves the project baseline | Full frozen validation against that baseline |
| A result generalizes | Held-out cases, replications, or field-appropriate external evidence |
| A mechanism explains the result | Evidence that distinguishes it from alternatives |
| A negative direction is closed | A valid failed gate with enough evidence to rule out the intended use |

## Preserve negative results

A useful negative result records:

- what was attempted;
- why it was plausible;
- the exact gate it failed;
- raw evidence and environment;
- whether the mechanism is closed or only this implementation failed;
- what should not be repeated.

## Timing and quantitative work

When timing or measuring software, record warmups, repetitions, pairing order,
raw trials, aggregate statistics, case-level floors, environment, versions,
memory, and exactness or quality checks. Do not report only the best trial.

## Qualitative and interpretive work

Record source selection, provenance, inclusion and exclusion choices, coding or
interpretive method, counterevidence, researcher position, uncertainty, and
the limits of transfer beyond the studied material.

## The final test

A reviewer should be able to answer:

1. What was known before the run?
2. What was decided before seeing the outcome?
3. What evidence was produced?
4. Which claim does that evidence support?
5. What remains unresolved?
