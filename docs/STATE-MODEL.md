# Markdown state model

Every project uses ordinary Markdown files.

```text
project-name/
├── PROJECT.md
├── TASK-SPEC.md
├── IDEAS.md
├── PROGRESS.md
├── FINDINGS.md
├── WORK-LOG.md
├── evidence/
└── runs/
    └── EXP-001/
        ├── PROTOCOL.md
        └── RESULT.md
```

The `evidence/` directory may contain whatever the real project needs. Those
artifacts belong to the project, not to this public harness repository.

## Source of truth for each question

| Question | Source of truth |
| --- | --- |
| What are we trying to learn? | `PROJECT.md` |
| What counts as success? | `TASK-SPEC.md` |
| Which ideas exist and what is their state? | `IDEAS.md` |
| What is happening now? | `PROGRESS.md` |
| What have we learned across runs? | `FINDINGS.md` |
| Why did the project change direction? | `WORK-LOG.md` |
| What was planned before a run? | `runs/<id>/PROTOCOL.md` |
| What actually happened? | `runs/<id>/RESULT.md` |

## Idea states

- **Proposed:** recommended but not approved.
- **Approved:** the human accepted the idea for execution.
- **Rejected:** the human or completed evidence ruled it out.
- **Parked:** potentially useful, but deliberately deferred.
- **Obsolete:** later evidence removed the reason to run it.

## Run states

- **Approved:** protocol may be prepared, but execution has not started.
- **Running:** authorized work is currently underway.
- **Completed:** the method finished; this says nothing about whether it won.
- **Rejected:** it failed a frozen gate or produced decisive negative evidence.
- **Inconclusive:** the method ran but could not resolve the uncertainty.
- **Successful:** it passed every frozen success criterion.

## Project states

- **Ready:** no run is active and a next decision can be made.
- **Running:** exactly one run is active.
- **Paused:** work was deliberately suspended with a clear resume point.
- **Blocked:** work cannot continue inside current authority or resources.
- **Complete:** the stated project objective has actually been achieved.

## Required invariants

- At most one run is active.
- Every started run has a protocol and a result document.
- The progress document names the same active run as the idea ledger.
- A finding links to evidence or states why no durable artifact exists.
- The strongest result changes only after all written gates pass.
- Negative and inconclusive results remain in the record.
- Existing run records are corrected transparently, never silently rewritten.
