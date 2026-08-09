# Autonomous research system

Open Discovery turns one human brief into an autonomous initiative containing
one or more independently owned projects.

```text
Human
└── Lab CEO
    └── Initiative leader
        ├── Project explorer
        ├── Project explorer
        └── Project explorer ...
```

## Storage

```text
initiatives/<initiative>/
├── BRIEF.md
└── projects/
    ├── <project-a>/
    └── <project-b>/
```

`BRIEF.md` is the only required research filename. It preserves the human's
request, desired outcome, constraints, resources, and forbidden actions.

The brief is living but append-only in meaning: preserve the original request
and record later corrections as amendments. The latest explicit instruction
controls conflicting earlier assumptions. Work that depends on an obsolete
interpretation is preserved as superseded, while unaffected projects continue.

All other structure is adaptive. Leaders and explorers create the notes, code,
reviews, databases, experiment records, evidence, reports, and folders their
work actually needs. Open Discovery does not provide blank templates or a fixed
runtime.

## Ownership

- The Lab CEO writes only its chosen state under `lab/`.
- One initiative leader owns an initiative root.
- One explorer owns each project folder.
- Managers read child evidence but do not rewrite it.
- Two active agents never share a writable folder.

Ownership prevents concurrent corruption without forcing one universal file
schema.

## Portfolio behavior

The initiative leader decides whether the brief needs one project or many. A
project is one independently testable question or coherent engineering path.
Projects may review literature, generate code, run experiments, attempt proofs,
simulate systems, reproduce papers, or verify another project's result.

At each meaningful checkpoint, the leader:

1. inspects completed artifacts;
2. identifies which uncertainty now matters most;
3. decides whether literature, a cheap test, deeper validation, replication,
   branching, pivoting, or closure has the greatest value;
4. creates or redirects projects accordingly;
5. synthesizes results back to the brief.

More agents are useful only when there are independent useful questions and
resources to support them. Agent counts are not quotas.

## Goal provenance and pivots

The latest human brief governs the initiative. Agents may autonomously change
methods, projects, and goals they selected themselves when the human outcome,
requested deliverable, constraints, and authority remain intact. If the human
delegated topic selection, the system may replace its chosen topic while still
serving that delegated outcome.

A pivot that materially changes a human-set question, outcome, deliverable,
constraint, forbidden action, or mission requires a human decision. Every
pivot records which governing goal it preserves. Changes to the scientific
question, data, metric, decision rule, model, dataset, library, benchmark, or
success gate are amendments, not silent retries; earlier evidence remains
available and is marked non-comparable when equivalence is unproven.

## Evidence

Structure is flexible; evidence standards are not. Material claims should be
traceable to inspectable sources or outputs. Preserve enough information to
understand methods, environments, decisive criteria, deviations, failures, and
limits. Keep negative results. Separate observations from interpretations and
speculation.

## Default autonomy

The system acts autonomously on local, zero-cost, non-destructive research
implied by the brief. It does not request routine approval for project
selection, organization, searches, agent allocation, or reversible local work.

Spending, outside compute, publication, external communication, private access,
credentials, account changes, destructive actions, and mission changes require
new human authority.

## Prompt-first implementation

Agent prompts describe responsibilities, outcomes, ownership, evidence, and
authority. They do not prescribe fixed files or research procedures. Explorers
generate the project-specific code and tools they need. A deterministic runtime
should be added only if repeated real failures demonstrate that prompting is
insufficient.

## Continuous dogfooding

Open Discovery can test itself through a permanent program led by
`agents/CONTINUOUS-TEST-LEADER.md`. The program stores coordination state under
ignored `lab/continuous-testing/` and runs each realistic test as a separate
ignored initiative. Test initiatives use the current harness but cannot edit
it. An independent evaluator inspects their artifacts before any cleanup or
release-readiness claim.

The suite is evolutionary rather than fixed: successful cases become
regression checks, while defects and newly added features generate the next
test mutations. This keeps development grounded in observed agent behavior
without turning the prompt-first research system into a rigid test runtime.

The permanent lab has two tracks. The discovery track runs actual AI, biology,
mathematics, and engineering initiatives and judges their evidence by the
standards of the relevant field. The scientist-experience track simulates
researchers with different expertise, patience, uncertainty, constraints, and
interaction styles. These simulations use short multi-turn conversations with
corrections, interruptions, challenges to evidence, and authority boundaries.

Scientist simulations measure the interface and agent behavior: whether the
system understood the request, avoided unnecessary intake, explained work
clearly, preserved corrections, recovered from failure, and asked only for
genuine human decisions. They do not count as scientific evidence. Scientific
claims must come from the real discovery initiatives and their inspectable
artifacts.
