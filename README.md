# Open Discovery

## Auto-optimize any code

The `auto-optimize` skill helps a coding agent optimize any system, algorithm,
or codebase to run faster while preserving correctness and measuring the real
hardware/workload tradeoffs.

Copy and paste this prompt into your coding agent:

> Install and use the `auto-optimize` skill from this repository:
>
> https://github.com/vukrosic/open-discovery/blob/main/.agents/skills/auto-optimize/SKILL.md
>
> Read it and start.

Open Discovery is a free, open-source collection of research and optimization
workflows for coding agents. It turns one human idea, question, paper, feature,
or system to improve into evidence-producing work.

Our immediate goal is to collect and design useful, fully digital experiments
across science and engineering. We are building the library of questions,
protocols, measurements, and evidence standards first. The next stage is an
autonomous harness that can run these experiments, solve them, or search for
improvements without losing track of what it actually proved.

The clearest product today is simple: open Open Discovery in Codex, Claude
Code, or another capable coding agent; provide code plus a benchmark; and let
the agent search for verified improvements. The repository and workflows are
free. We will consider hosted execution only after real usage shows which
operational problems people repeatedly need solved.

## Install

```bash
git clone https://github.com/vukrosic/open-discovery.git
cd open-discovery
```

Open the cloned folder in Codex or start Claude Code from that folder. No Open
Discovery server or package installation is required; individual workflows may
use project-local dependencies when their task needs them.

## Choose a workflow

Open this repository with a file-capable coding agent and choose a workflow:

- **Discover:** `$discovery-engine`, `$find-ai-research-direction`,
  `$literature-review`, `$deep-strategy-research`
- **Design and analyze:** `$design-scientific-study`,
  `$curate-research-dataset`, `$analyze-scientific-data`, `$formalize-math`
- **Build and optimize:** `$paper-implementer`, `$build-benchmark`,
  `$evolve-program`, `$optimize-gpu-kernel`, `$optimize-inference`,
  `$optimize-agent`
- **Test and verify:** `$feature-tester`, `$red-team-agent`,
  `$audit-research-result`
- **Operate and extend:** `$package-research`, `$research-cockpit`,
  `$find-startup-skill-ideas`, `$build-skill`

See [all workflows and examples](WORKFLOWS.md), or simply describe what you
want in ordinary language. For example:

> Optimize this code without changing its outputs. `pytest` must pass and
> `python benchmark.py` should become faster.

## Examples

### Current autonomous experiments

These small examples show the kinds of computer-only experiments Open
Discovery is collecting and designing:

- **[Algorithm optimization](examples/algorithm-optimization/README.md):** try
  a new version of an algorithm and measure whether it is faster while still
  giving the right answer.
- **[Computational biology](examples/computational-biology/README.md):** test
  a data-analysis method on gene-like data and check whether its predictions
  improve.
- **[2D Ising physics simulation](examples/physics-ising/README.md):** simulate
  a simple magnetic system and compare two computer methods for sampling it.
- **[Public-assay hit triage](examples/drug-discovery-hit-triage/README.md):**
  rank compounds from public EGFR assay data for a hypothetical follow-up
  screen and measure top-list enrichment.
- **[PID robotics control](examples/robotics-pid/README.md):** tune a simulated
  robot controller and compare accuracy and stability on held-out disturbances.

Each example keeps the question, protocol, code, measurements, and generated
results together. These are digital demonstrations, not claims about real
materials, patients, or production systems.

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
- [`WORKFLOWS.md`](WORKFLOWS.md) — user-facing workflow catalog and examples
- [`agents/`](agents/) — research hierarchy, review, communication, and
  repository-artifact prompts
- [`.agents/skills/`](.agents/skills/) — autonomous research and focused skills
- [`skill-lab/`](skill-lab/) — experimental skills loaded explicitly by path
- [`docs/`](docs/) — evidence, collaboration, and operating guidance
- [`docs/AUTO-LAB.md`](docs/AUTO-LAB.md) — full computer-cycle auto-lab rule
- [`docs/AUTO-LAB-TEST-CASES.md`](docs/AUTO-LAB-TEST-CASES.md) — digital
  closed-loop dogfood case specs (runs stay out of git)
- [`docs/EXPERIMENT-CATALOG.md`](docs/EXPERIMENT-CATALOG.md) — experiment
  families and example tasks users and companies can set
- [`docs/EXPERIMENT-CONTRACT.md`](docs/EXPERIMENT-CONTRACT.md) — the seven
  questions every experiment must answer
- [`research-modes/`](research-modes/) — optional field-specific guidance

The harness provides prompts, responsibility boundaries, evidence standards,
and durable-state principles. Agents generate the actual research structure and
code they need.

For a continuing multi-initiative lab, local ignored files such as
`lab/MISSION.md` and `lab/CONSTRAINTS.md` can define that lab's purpose and
resource limits. They configure one lab instance and do not change Open
Discovery's general behavior for other researchers. This workspace lab binds
the auto-lab computer-only rule there; live initiatives under `initiatives/`
remain gitignored.

## Default autonomy

Auto mode is the default for local, zero-cost, non-destructive research implied
by the user's request. Spending, outside compute, publication, external
communication, private access, credentials, and destructive actions still
require explicit authority.

## Current modes

Open Discovery includes guidance for AI and machine learning, mathematics,
biology, cross-domain algorithm optimization, and evaluator-driven
[program evolution](program-evolution/README.md). The architecture also
supports engineering and other evidence-driven work without pretending
specialized guidance exists where it does not.

## Limits

Open Discovery is a prompt-driven harness, not a server or cloud scheduler. A
completed paper or result is not automatically correct, peer reviewed, novel,
or published; claims remain limited by their preserved evidence.

## License

[MIT](LICENSE.md)
