# Open Discovery

Open Discovery is a Markdown-first harness for human–AI research.

Its user-facing AI research partner is **Starberry**.

It helps a researcher turn one uncertain question into a sequence of small,
reviewable investigations. The AI can recommend and run work inside the scope
the human grants, but the question, evidence standard, constraints, and
consequential decisions remain explicit.

The core loop is:

> question → evidence → one next idea → approval → protocol → run → result → next question

> “We believe the biggest positive impacts of AI will be in biology and
> medicine.”
>
> — Anthropic, [AI for Science Program](https://www.anthropic.com/news/ai-for-science-program)

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

The current field focus is **AI and machine learning, mathematics, and
biology**. Each field has a practical mode guide with its own evidence checks
and research tools, while all three use the same durable research loop.
Users may work step by step or request Full Auto mode through a finished paper.

## Coding-agent compatibility

Open Discovery is designed to be used with file-capable coding agents such as
**OpenAI Codex**, **Claude Code**, and open-source coding harnesses. It is not
tied to one model provider, agent runtime, or proprietary integration.

The Markdown files are the interface. A compatible agent must be able to read
the project record, edit Markdown, preserve evidence, run only authorized work,
and stop at the written approval boundaries. Point the agent to `AGENTS.md` and
the active project's files before beginning a research loop.

## What this release contains

Version 0.2 deliberately keeps the operating system in Markdown. There is no
package, server, database, agent framework, or hidden automation. The only
supporting repository file is `.gitignore`, which keeps locally generated
research projects out of the public Git history.

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

1. Open the cloned repository with Codex, Claude, or another file-capable agent
   and give it a question, topic, field, or Full Auto command.
2. The agent creates a unique local `projects/<project-slug>/` folder, copies
   [`templates/project/`](templates/project/), and fills in `PROJECT.md` and
   `TASK-SPEC.md` with the researcher.
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

## Local research projects

Real research lives under `projects/<project-slug>/` inside the clone. That
directory is ignored by Git: the released harness stays clean while project
questions, evidence, experiments, and papers remain local. Each new or parallel
request gets its own folder, and an existing project is resumed only when the
researcher asks for it.

Existing work may remain in a sibling folder, elsewhere on the computer, or in
a remote repository. Open Discovery creates a local record under `projects/`
that stores the original path or URL and navigation notes; it does not move or
edit the original project automatically.

Because these projects live inside the local clone, deleting the clone also
deletes them. Back up or export important projects before removing the folder.

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

- [`AGENTS.md`](AGENTS.md) — operating contract for AI agents.
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — first project walkthrough.
- [`docs/KICKOFF-PROMPT.md`](docs/KICKOFF-PROMPT.md) — copy-paste prompt for
  initializing a project with an AI agent.
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
- [`docs/EXAMPLE-RESEARCH-IDEAS.md`](docs/EXAMPLE-RESEARCH-IDEAS.md) — sample
  directions a researcher can bring to Open Discovery.
- [`research-modes/`](research-modes/) — shared tools and field-specific guides
  for AI/ML, mathematics, and biology.
- [`docs/experiment-idea-generation/PROMPT.md`](docs/experiment-idea-generation/PROMPT.md)
  — reusable prompt for recommending one next experiment.
- [`templates/`](templates/) — files to copy into each real project and run.
- [`templates/literature-review/`](templates/literature-review/) — files for a
  reproducible search, evidence table, and synthesis.
- `projects/` — locally generated, Git-ignored research workspaces.
- [`examples/robust-summary/`](examples/robust-summary/) — completed teaching
  project with a frozen protocol, transparent calculations, a negative result,
  and a next decision.
- [`CHANGELOG.md`](CHANGELOG.md) — released changes by version.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules.
- [`SECURITY.md`](SECURITY.md) — security and private-data guidance.

## What is intentionally absent

The public Git history contains no project-specific experiments, model files,
datasets, benchmark outputs, private prompts, or conclusions. A user's local,
ignored `projects/` directory may contain all of these as their research
requires.

## Status

Version 0.2: Starberry-powered project initialization, AI/ML, mathematics, and
biology research modes, existing-project attachment, literature review,
approved experiment execution, Full Auto routing, and durable research memory.
