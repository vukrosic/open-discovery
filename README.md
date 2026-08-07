# Open Discovery

Open Discovery is a Markdown-first harness for human–AI research.

It helps a researcher turn one uncertain question into a sequence of small,
reviewable investigations. The AI can recommend and run work inside the scope
the human grants, but the question, evidence standard, constraints, and
consequential decisions remain explicit.

The core loop is:

> question → evidence → one next idea → approval → protocol → run → result → next question

## Current product focus

Open Discovery currently has two automation loops and one shared control layer:

1. **Literature review loop:** search, screen, extract, compare, synthesize, and
   identify the strongest unresolved gap.
2. **Experiment loop:** propose, approve, freeze, run, evaluate, preserve the
   result, and recommend one next experiment.
3. **Research memory:** keep sources, protocols, evidence, negative results,
   permissions, and the current strongest finding recoverable from files.

The literature loop summarizes existing evidence. The experiment loop creates
new evidence. The shared record prevents both loops from repeating work or
quietly changing the question.

## What this release contains

Version 0.1 is deliberately only Markdown files. There is no package, server,
database, agent framework, or hidden automation.

The repository provides:

- a project brief that defines the question and authority boundaries;
- a task specification with success criteria and stopping rules;
- an idea ledger that separates proposed, approved, rejected, and parked work;
- a progress record that makes the current state resumable;
- experiment protocol and result templates;
- literature-review specification, search, evidence, and synthesis templates;
- append-only-style findings and work logs;
- copy-paste operating prompts for AI-assisted reviews and experiments;
- rules for evidence, negative results, pivots, and bounded autonomy.

The files are the system. They can be read, reviewed, diffed, copied into any
project, and versioned with Git.

## Why Markdown first

The first problem is not orchestration software. It is making the research
state legible enough that a human and an AI can work together without losing:

- what was actually approved;
- what was actually run;
- which evidence supports a claim;
- which directions already failed;
- what the current strongest result is;
- what the AI may do next without asking again.

Software should automate this only after the document contract survives real
research loops.

## Quick start

1. Copy [`templates/project/`](templates/project/) into a new project folder.
2. Fill in `PROJECT.md` and `TASK-SPEC.md` with the researcher.
3. Record ideas in `IDEAS.md`; do not treat a proposal as approval.
4. When an idea is approved, copy [`templates/experiment/`](templates/experiment/)
   into a new numbered run folder.
5. Complete `PROTOCOL.md` before doing the work.
6. Preserve the raw evidence and write `RESULT.md`, including negative or
   inconclusive outcomes.
7. Update `PROGRESS.md`, `FINDINGS.md`, and `WORK-LOG.md` before choosing the
   next direction.

Read [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for a complete walkthrough.

If you are working with an AI agent, start with the copy-paste
[`KICKOFF-PROMPT.md`](docs/KICKOFF-PROMPT.md). To see what a completed loop
looks like, read the fully worked
[`robust-summary example`](examples/robust-summary/README.md).

After initialization, use the
[`LITERATURE-REVIEW-PROMPT.md`](docs/LITERATURE-REVIEW-PROMPT.md) to map existing
evidence or the
[`EXPERIMENT-LOOP-PROMPT.md`](docs/EXPERIMENT-LOOP-PROMPT.md) after an
experiment has been explicitly approved.

Before starting real work, check
[`SUPPORTED-RESEARCH.md`](docs/SUPPORTED-RESEARCH.md). It states which research
workflows version 0.1 supports, which require additional institutional controls,
and which must not be executed through this harness.

## The important state boundaries

- **Proposed** is not approved.
- **Approved** is not running.
- **Running** is not completed.
- **Completed** is not successful.
- **Measured locally** is not reproduced elsewhere.
- **Written** is not published.
- **A profile estimate** is not an end-to-end improvement.

These distinctions prevent the research record from becoming more confident
than the evidence.

## Repository map

- [`GOAL.md`](GOAL.md) — product promise and scope.
- [`AGENTS.md`](AGENTS.md) — operating contract for AI agents.
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — first project walkthrough.
- [`docs/KICKOFF-PROMPT.md`](docs/KICKOFF-PROMPT.md) — copy-paste prompt for
  initializing a project with an AI agent.
- [`docs/PRODUCT-FOCUS.md`](docs/PRODUCT-FOCUS.md) — the two automation loops,
  shared research memory, and near-term exclusions.
- [`docs/LITERATURE-REVIEW-LOOP.md`](docs/LITERATURE-REVIEW-LOOP.md) — durable
  source-search and synthesis workflow.
- [`docs/LITERATURE-REVIEW-PROMPT.md`](docs/LITERATURE-REVIEW-PROMPT.md) —
  copy-paste prompt for an AI-assisted review.
- [`docs/EXPERIMENT-LOOP-PROMPT.md`](docs/EXPERIMENT-LOOP-PROMPT.md) —
  copy-paste prompt for executing an approved experiment.
- [`docs/HUMAN-AI-COLLABORATION.md`](docs/HUMAN-AI-COLLABORATION.md) — authority
  and responsibility model.
- [`docs/AUTONOMOUS-LOOP.md`](docs/AUTONOMOUS-LOOP.md) — bounded repeated work.
- [`docs/EVIDENCE-STANDARD.md`](docs/EVIDENCE-STANDARD.md) — claim and evidence rules.
- [`docs/STATE-MODEL.md`](docs/STATE-MODEL.md) — canonical document states.
- [`docs/SUPPORTED-RESEARCH.md`](docs/SUPPORTED-RESEARCH.md) — current scientist,
  discipline, safety, and execution boundaries.
- [`docs/experiment-idea-generation/PROMPT.md`](docs/experiment-idea-generation/PROMPT.md)
  — reusable prompt for recommending one next experiment.
- [`protocol/`](protocol/) — general research intake and result protocol.
- [`templates/`](templates/) — files to copy into each real project and run.
- [`templates/literature-review/`](templates/literature-review/) — files for a
  reproducible search, evidence table, and synthesis.
- [`examples/robust-summary/`](examples/robust-summary/) — completed teaching
  project with a frozen protocol, transparent calculations, a negative result,
  and a next decision.

## What is intentionally absent

This public repository contains no project-specific experiments, model files,
datasets, benchmark outputs, private prompts, or conclusions from the research
used to develop the method.

## Status

Version 0.1: operational Markdown contracts for AI-assisted literature review,
approved experiment execution, and durable research memory.
