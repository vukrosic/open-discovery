# Public-assay hit triage

This is a dry virtual-screening experiment modeled on a real drug-discovery
workflow: use historical public assay data to choose a small shortlist for a
hypothetical follow-up assay. The committed `data/activity_snapshot.csv` is
the frozen input for repeatable agent evaluation; it is separate from the
optional live retrieval path in the original experiment script.

Run it from this directory:

```bash
python3 experiment.py
```

The script loads the pinned bounded ChEMBL EGFR activity snapshot, creates a
time-based holdout, compares a prevalence baseline with a nearest-known-active
similarity ranker, and writes checked tables, plots, and a run receipt under
`results/`. Live retrieval is only a fallback when the pinned file is absent.
For the frozen candidate interface, copy
`candidate_template.py` to `candidates/candidate-NNN/solution.py` and run:

```bash
mkdir -p candidates/candidate-001
cp candidate_template.py candidates/candidate-001/solution.py
python3 evaluator.py candidates/candidate-001/solution.py \
  --evidence-dir candidates/candidate-001/evidence
```

The evaluator uses only the pinned snapshot, gives candidates labels for
training rows but not hold-out activity, and emits structured `PASS`, `FAIL`,
or `BLOCKED` JSON with a preserved `RESULT.json`.

This does not perform docking, wet-lab testing, or drug discovery. Its result
is only evidence about ranking public historical measurements on this target
and split.
