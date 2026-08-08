# Open Discovery

Open Discovery is an open-source, Markdown-first research harness for coding
agents. Its research partner, **Starberry**, turns a question or existing
project into a durable research loop.

## Start

Open this repository with Codex, Claude, or another file-capable agent and
paste one of these:

`Use $literature-review to review [your topic] and deliver a PDF report.`

`Use $paper-implementer to reproduce [paper title, URL, DOI, or PDF] as verified code.`

`Use $feature-tester to run and test [feature, prompt, skill, workflow, or idea].`

`Run the Hierarchy of Agents Research Model on [research goal] and choose useful directions autonomously.`

`Do research and write a paper fully autonomously on [your topic].`

`Do research and write a paper fully autonomously; choose the field and topic for me.`

`Chat with me first and help me choose a research idea and direction.`

`Add my existing project to Open Discovery: [folder path or repository URL].`

## What it does

- reviews literature and preserves exact searches and sources;
- runs the Literature Review skill autonomously with one research worker and
  delivers a source-tracked PDF report;
- reproduces a paper as runnable, validated code before offering environment
  adaptation, optimization, or extension;
- runs realistic isolated feature tests, reports readiness, and cleans its
  temporary agents, downloads, caches, and generated artifacts;
- proposes, freezes, and runs experiments or proof investigations;
- records evidence, failures, negative results, and decisions;
- keeps work resumable from files instead of chat history;
- can turn the resulting record into a report or paper.

The loop is:

> question → literature → idea → experiment or proof → evidence → paper

## Current fields

Open Discovery currently includes dedicated modes for:

- [AI and machine learning](research-modes/AI-MACHINE-LEARNING.md)
- [Mathematics](research-modes/MATHEMATICS.md)
- [Biology](research-modes/BIOLOGY.md)

> “We believe the biggest positive impacts of AI will be in biology and
> medicine.”
>
> — Anthropic, [AI for Science Program](https://www.anthropic.com/news/ai-for-science-program)

## How projects work

Starberry creates each project under `projects/<project-slug>/`. That directory
is ignored by Git, so questions, experiments, data, and papers stay local and
do not enter the public harness history.

Existing work can remain elsewhere. Starberry creates a local record pointing
to its folder or repository without moving or modifying the original unless
you request it.

## Hierarchy of Agents Research Model

This experimental model supports continuous multi-project discovery using
three agent levels:

1. A Lab CEO coordinates the portfolio and shared resources.
2. One direction leader compares evidence and steers each research direction.
3. Direction leaders start with three independent explorers testing distinct
   ideas in separate project folders, then adjust the pool when useful.

Luna with high reasoning is the preferred runtime when available; other
capable agents may be used without changing the architecture.

When an explorer finishes, its evidence is preserved and the leader starts the
next evidence-grounded project. The CEO normally steers through leaders, but
may contact an explorer directly to resolve a concrete stall, evidence problem,
or resource conflict. Live programs and projects remain local and ignored by
Git; the released repository contains only reusable prompts and templates.

## What is included

- [`AGENTS.md`](AGENTS.md) — Starberry’s operating instructions
- [`agents/`](agents/) — Hierarchy of Agents Research Model roles
- [`.agents/skills/literature-review/`](.agents/skills/literature-review/) —
  autonomous one-worker literature review and PDF-report workflow
- [`.agents/skills/paper-implementer/`](.agents/skills/paper-implementer/) —
  faithful paper-to-code reproduction and validation workflow
- [`.agents/skills/feature-tester/`](.agents/skills/feature-tester/) — isolated
  testing for features, prompts, agents, skills, workflows, and ideas
- [`templates/`](templates/) — project, review, implementation, and experiment records
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — complete workflow
- [`docs/EVIDENCE-STANDARD.md`](docs/EVIDENCE-STANDARD.md) — evidence rules
- [`docs/HUMAN-AI-COLLABORATION.md`](docs/HUMAN-AI-COLLABORATION.md) — human and AI roles
- [`examples/robust-summary/`](examples/robust-summary/) — completed worked example

## Limits

Version 0.3.0 is a Markdown harness, not a server or agent framework. The agent
must have file access and the tools required by the research. A completed paper
is not automatically correct, peer reviewed, or published; its claims remain
limited by the preserved evidence.

## License

[MIT](LICENSE.md)
