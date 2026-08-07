# Open Discovery

Open Discovery is an open-source, Markdown-first research harness for coding
agents. Its research partner, **Starberry**, turns a question or existing
project into a durable research loop.

## Start

Open this repository with Codex, Claude, or another file-capable agent and
paste one of these:

`Do research and write a paper fully autonomously on [your topic].`

`Do research and write a paper fully autonomously; choose the field and topic for me.`

`Chat with me first and help me choose a research idea and direction.`

`Add my existing project to Open Discovery: [folder path or repository URL].`

## What it does

- reviews literature and preserves exact searches and sources;
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

## What is included

- [`AGENTS.md`](AGENTS.md) — Starberry’s operating instructions
- [`templates/`](templates/) — project, literature-review, and experiment records
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — complete workflow
- [`docs/EVIDENCE-STANDARD.md`](docs/EVIDENCE-STANDARD.md) — evidence rules
- [`docs/HUMAN-AI-COLLABORATION.md`](docs/HUMAN-AI-COLLABORATION.md) — human and AI roles
- [`examples/robust-summary/`](examples/robust-summary/) — completed worked example

## Limits

Version 0.2.1 is a Markdown harness, not a server or agent framework. The agent
must have file access and the tools required by the research. A completed paper
is not automatically correct, peer reviewed, or published; its claims remain
limited by the preserved evidence.

## License

[MIT](LICENSE.md)
