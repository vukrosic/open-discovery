# Markdown state model

Open Discovery keeps the released harness and local research in one clone while
separating them through the Git-ignored `projects/` directory.

```text
open-discovery/
├── AGENTS.md
├── docs/
├── templates/
├── examples/
└── projects/                         # generated locally; ignored by Git
    └── project-name/
        ├── PROJECT.md
        ├── TASK-SPEC.md
        ├── IDEAS.md
        ├── PROGRESS.md
        ├── FINDINGS.md
        ├── WORK-LOG.md
        ├── evidence/
        ├── reviews/
        │   └── REV-001/
        │       ├── REVIEW-SPEC.md
        │       ├── SEARCH-LOG.md
        │       ├── EVIDENCE-TABLE.md
        │       ├── SYNTHESIS.md
        │       ├── REPORT.md
        │       └── REPORT.pdf
        └── runs/
            └── EXP-001/
                ├── PROTOCOL.md
                └── RESULT.md
```

The `evidence/` directory may contain whatever the real project needs. Those
artifacts belong to the local project and are not part of the released Git
history. Each active agent uses a different project folder.

For existing work, the Open Discovery folder is a research record, not a copy
of the original project. `PROJECT.md` stores the original folder path or
repository URL, relevant entry points, and whether later work may edit the
original. The existing project can live in a sibling directory, elsewhere on
the computer, or in a remote repository.

## Source of truth for each question

| Question | Source of truth |
| --- | --- |
| What are we trying to learn? | `PROJECT.md` |
| Where does existing project work live? | `PROJECT.md` |
| What counts as success? | `TASK-SPEC.md` |
| Which ideas exist and what is their state? | `IDEAS.md` |
| What is happening now? | `PROGRESS.md` |
| What have we learned across runs? | `FINDINGS.md` |
| Why did the project change direction? | `WORK-LOG.md` |
| What was planned before a run? | `runs/<id>/PROTOCOL.md` |
| What actually happened? | `runs/<id>/RESULT.md` |
| What literature scope was frozen? | `reviews/<id>/REVIEW-SPEC.md` |
| What searches and screening decisions occurred? | `reviews/<id>/SEARCH-LOG.md` |
| Which source supports each extracted claim? | `reviews/<id>/EVIDENCE-TABLE.md` |
| What does the reviewed evidence establish? | `reviews/<id>/SYNTHESIS.md` |
| What is the reader-facing literature report? | `reviews/<id>/REPORT.md` and `REPORT.pdf` |

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

Literature reviews use the same separation between **Proposed**, **Approved**,
**Running**, and a terminal state. `SYNTHESIS.md` records whether the bounded
review was **Completed**, **Inconclusive**, or **Blocked**; completion does not
mean the literature is exhaustive.

When the Literature Review skill is invoked, the invocation is the approval
record: the AI freezes the specification and may move directly to **Running**.
This shortcut applies only to that local review and does not approve an
experiment or any external action.

## Project states

- **Ready:** no run is active and a next decision can be made.
- **Running:** exactly one run is active.
- **Paused:** work was deliberately suspended with a clear resume point.
- **Blocked:** work cannot continue inside current authority or resources.
- **Complete:** the stated project objective has actually been achieved.

## Required invariants

- At most one run is active.
- A Proposed idea has no run folder or protocol; those are created only after
  approval.
- `PROTOCOL.md` and `RESULT.md` live inside `runs/<id>/`, never at the project
  root.
- Every started run has a protocol and a result document.
- Every started review has a frozen specification, search log, evidence table,
  synthesis document, and reader-facing Markdown report. A completed review
  also has a verified PDF report.
- The progress document names the same active run as the idea ledger.
- A finding links to evidence or states why no durable artifact exists.
- The strongest result changes only after all written gates pass.
- Negative and inconclusive results remain in the record.
- Existing run records are corrected transparently, never silently rewritten.
