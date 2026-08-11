# Auto lab operating rule

## Main rule

Open Discovery’s auto lab only runs work that has a **full cycle on a computer**
— work an AI agent can complete end-to-end without human hands, wet-lab
pipetting, fieldwork, clinic time, or facility operators.

If any required step cannot be finished digitally under current authority, that
step is **out of scope** for the auto lab. Do not fake it, simulate a physical
result as if it were observed, or claim a full discovery cycle that still needs
manual execution.

## What “full cycle” means

A valid auto-lab cycle is:

```text
question / claim
  → plan
  → digital execution (code, data, simulation, formal check, optimization)
  → frozen evaluator / gate
  → evidence
  → conclusion or next digital experiment
```

Every material step in that loop must be runnable by the agent on a computer
(local machine, approved cloud compute, public APIs/data, simulators, proof
checkers, evaluators).

## In scope (including “hard” sciences, dry only)

Include any scientific or engineering process that is fully computational, even
when the broader field also has wet or physical work:

- literature review, hypothesis ranking, study design for digital tests
- paper reimplementation and computational reproduction
- bioinformatics, computational genomics, sequence/structure analysis
- drug / therapeutics **in silico** work: target/literature triage, docking,
  virtual screening, QSAR, simulation, assay-*data* analysis when data already
  exists digitally
- chemistry / materials **simulation** and computational design
- physics / astro / climate / economics pipelines on data and models
- ML / algorithm research, program optimization against evaluators
- formal mathematics and machine-checked proofs
- benchmark building, auditing, packaging of digital results

The field name does not matter. The test is: **can the agent finish the loop
without a human body?**

## Out of scope (until a digital substitute exists)

- wet-lab protocol execution, animal work, manufacturing floor work
- clinical procedures and human-subjects intervention
- field collection, hardware fab, telescope/beamtime operation by humans
- anything whose decisive evidence is a physical action or sensory judgment
  the agent cannot perform

Drafting a protocol, analysis plan, or robot script is allowed **only as a
digital artifact**. It does not count as completing an experiment unless the
auto lab can also run and check it fully on computer.

## How to handle mixed fields (e.g. therapeutics)

For domains like drug discovery:

- **Do:** every dry subprocess that closes digitally — literature, data mining,
  model building, virtual screens, computational ADMET, analysis of already
  deposited assay/omics data, reproduction of computational papers.
- **Do not:** claim wet validation, animal results, or clinical effect from
  work the auto lab did not digitally execute and gate.
- **Record explicitly:** “physical / wet validation required; auto lab stops
  here” when the next decisive step leaves the computer.

Partial progress is success when labeled honestly. Crossing into hand-work is
failure of scope control, not ambition.

## Evidence rule under this constraint

- Only computer-produced, inspectable artifacts upgrade claims.
- Missing physical steps → status `blocked` or `external-pending`, never
  `reproduced` for the physical claim.
- Irreproducible digital runs are first-class negative evidence inside the
  auto lab; they do not authorize inventing a wet result.

## Stop and ask on missing code or big gaps

For paper reproduction and similar digital science work: if usable code is
missing, required data/assets are unavailable, or the method has a **big gap**
(underspecified central recipe such that faithful reproduction needs guessing),
**stop and ask the human**. Do not invent the implementation and call it a
reproduction. Offer clear options: provide artifacts, narrow the claim,
authorize an explicitly labeled best-effort reimplementation, or abort.
Routine tiny inferences that cannot change the claim may continue; large
creative gaps may not.

## Local lab binding

Public harness behavior is described here. A continuing lab binds the rule in
ignored `lab/CONSTRAINTS.md` and records each request in
`initiatives/<slug>/BRIEF.md`. Live runs stay out of git; this document and
[AUTO-LAB-TEST-CASES.md](./AUTO-LAB-TEST-CASES.md) stay in git.
