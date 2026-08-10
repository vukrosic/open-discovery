# Open Discovery

Open Discovery is an open-source experiment automation harness for coding agents. It turns
one human idea into an autonomous initiative containing as many independent
projects as the work needs.

Our goal is to automate scientific and engineering experimentation—from a
question or hypothesis through independent investigations, execution,
evidence, and reproducible results. We are looking to raise capital to scale
development, hosted execution, and compute while keeping the core open-source.

I am also looking for technical cofounders who want to apply to Y Combinator
and build Open Discovery with me — people who can conduct scientific research or build systems.

## Start

Open this repository with Codex, Claude, or another file-capable agent and say:

`Investigate ways to make small language models faster on my MacBook.`

`Try to solve or make progress on this mathematics problem: ...`

`Reproduce this paper: ...`

`Review the literature on ... and write a PDF report.`

`Choose a worthwhile AI research direction and pursue it autonomously.`

## Examples

[Qwen3 Prompt Lookup Robustness](https://github.com/vukrosic/qwen3-prompt-lookup-robustness)
is a research repository produced by AI agents using Open Discovery. The system autonomously investigated how to run Qwen3-0.6B faster
on an Apple-Silicon MacBook, executed reproducible benchmarks, and found that
fixed two-token prompt lookup was 30.4% faster than ordinary greedy decoding while producing exactly the same tokens.

Open Discovery records the request once and handles routine research decisions
without making the researcher manage forms, files, agents, or approvals.

## Architecture

```text
Human brief
└── Initiative
    ├── Project A
    │   └── reviews, code, experiments, evidence, verification
    ├── Project B
    ├── Project C ...
    └── One canonical GitHub-ready repository artifact
```

An **initiative** is everything generated from one human request. A **project**
is one independently testable question or engineering approach. Initiative
leaders generate and compare projects; explorer agents own individual
projects. A separate Scientific Reviewer can judge mature results using
field-appropriate criteria, and a Research Communicator can turn accepted
claims into accurate public drafts without publishing them.

Each initiative produces one canonical GitHub-ready repository artifact for the
initiative as a whole, not one repository per project. A Repository Artifact
Builder assembles inspected project outputs into that single package and keeps
updating it as the initiative develops. It may include runnable setup,
representative positive and negative results, prompts, provenance, and guidance
for another human or agent to reproduce and continue the work. Local packaging
does not automatically create or publish a GitHub remote.

Live work is organized as:

```text
initiatives/<initiative>/
├── BRIEF.md
└── projects/
    └── <project>/
```

`BRIEF.md` is the only required research filename. Agents choose the remaining
files, tools, code, and project organization according to the work. Open
Discovery deliberately has no blank research templates and no fixed runtime.

## What the harness provides

- [`AGENTS.md`](AGENTS.md) — the harness's operating behavior
- [`agents/`](agents/) — research hierarchy, review, communication, and
  repository-artifact prompts
- [`.agents/skills/`](.agents/skills/) — autonomous research and focused skills
- [`docs/`](docs/) — evidence, collaboration, and operating guidance
- [`research-modes/`](research-modes/) — optional field-specific guidance

The harness provides prompts, responsibility boundaries, evidence standards,
and durable-state principles. Agents generate the actual research structure and
code they need.

For a continuing multi-initiative lab, local ignored files such as
`lab/MISSION.md` and `lab/CONSTRAINTS.md` can define that lab's purpose and
resource limits. They configure one lab instance and do not change Open
Discovery's general behavior for other researchers.

## Default autonomy

Auto mode is the default for local, zero-cost, non-destructive research implied
by the user's request. Spending, outside compute, publication, external
communication, private access, credentials, and destructive actions still
require explicit authority.

## Current fields

Open Discovery includes guidance for AI and machine learning, mathematics, and
biology. The architecture also supports engineering and other evidence-driven
work without pretending specialized guidance exists where it does not.

## Limits

Open Discovery is a prompt-driven harness, not a server or cloud scheduler. A
completed paper or result is not automatically correct, peer reviewed, novel,
or published; claims remain limited by their preserved evidence.

## License

[MIT](LICENSE.md)
