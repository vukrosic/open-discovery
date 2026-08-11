# Open Discovery workflows

Open Discovery is a free, open-source collection of research and optimization
workflows for coding agents. Start with whatever you already have: a question,
idea, paper, repository, feature, baseline program, or benchmark.

## Choose a workflow

The workflows are grouped by the outcome you need. You can name one directly,
or describe the task normally and let the agent route it.

## Start here

### Optimize a program — `$evolve-program`

Provide code, an evaluation script or benchmark, and what should improve. The
agent locks the starting point, searches candidate changes, rejects regressions,
and returns only externally measured improvements.

> Optimize this image-processing code. `pytest` must still pass, and
> `python benchmark.py` should become faster.

### Run autonomous research — `$discovery-engine`

Provide a scientific or engineering question or desired outcome. The agent
creates and runs the independent investigations needed, preserves evidence,
and returns verified findings, code, or an honest negative result.

> Investigate ways to make small language models faster on my MacBook.

### Answer a strategic decision — `$deep-strategy-research`

Provide a difficult business, technology, policy, market, or organizational
question. The agent investigates autonomously, reconciles conflicting evidence,
compares options and scenarios, and returns a sourced recommendation plus a
concise executive summary.

> Should we build, buy, or partner for an enterprise AI support product over
> the next two years, and what evidence should trigger a change of course?

### Review literature — `$literature-review`

Provide a research question. The agent conducts a source-tracked review and
delivers a checked PDF report without routine interruptions.

> Review current methods for detecting batch effects in single-cell RNA-seq.

### Reproduce a paper — `$paper-implementer`

Provide a paper, DOI, arXiv link, or repository. The agent first builds and
validates a faithful implementation before offering adaptations.

> Reproduce this paper as runnable code: ...

### Find an AI research direction — `$find-ai-research-direction`

Describe your interests, constraints, or available hardware. The agent helps
you compare AI research directions and choose a concrete question before
research begins.

> Help me choose a useful post-training experiment I can finish on a MacBook.

## Design and analyze research

### Design a scientific study — `$design-scientific-study`

Provide a question, hypothesis, available resources, and constraints. The agent
produces an execution-ready study design, including the target, controls,
sampling, measurements, analysis, stopping rules, and validity risks relevant
to the field. It does not pretend the proposed study has already been run.

> Design a small, credible study to test whether this intervention changes
> recovery time, given our available subjects and instruments.

### Curate a research dataset — `$curate-research-dataset`

Provide source data and its intended research use. The agent builds an
auditable dataset package with provenance, rights and privacy limits, semantic
schema, explicit transformations, quality checks, leakage-resistant splits,
an integrity manifest, and a data card.

> Prepare these measurements for model evaluation without leaking subjects
> between train and test.

### Analyze scientific data — `$analyze-scientific-data`

Provide data and a research question. The agent creates and runs a reproducible
analysis, checks its tables and figures, respects the study design, separates
exploration from confirmation, and reports uncertainty and limitations.

> Analyze whether treatment changed the outcome while respecting repeated
> measurements from the same subject.

### Formalize mathematics — `$formalize-math`

Provide a theorem, conjecture, or informal proof. The agent translates it into
a faithful formal statement, searches for counterexamples when useful, and
attempts verification with an available proof assistant. It distinguishes a
machine-checked result from an unverified formalization.

> Formalize this theorem in Lean and tell me exactly what is verified.

## Build and optimize

### Build a benchmark — `$build-benchmark`

Provide a system or desired outcome that needs trustworthy measurement. The
agent defines correctness and representative workloads, measures the baseline
and noise, protects confirmation cases, checks for evaluator gaming, and leaves
a runnable evaluation contract for later optimization.

> Build a benchmark for optimizing this parser without changing accepted or
> rejected inputs.

### Write or optimize a GPU kernel — `$optimize-gpu-kernel`

Provide a reference operation, target hardware, representative shapes, and
required semantics. The agent writes, ports, fuses, or tunes a CUDA, Triton,
Metal/MLX, HIP, OpenCL, or other target-native kernel and accepts it only after
correctness checks and reproducible measurements on the actual target.

> Replace these framework operations with a faster Triton kernel while
> preserving outputs and gradients across the supported shapes.

### Optimize model inference — `$optimize-inference`

Provide a model or inference application, representative workload, and target
hardware. The agent profiles the real path and accepts only reproducible
latency, throughput, memory, or cost gains that preserve the required output
quality on that target.

> Make this model serve faster on Apple Silicon without reducing answer
> quality.

### Optimize an AI agent — `$optimize-agent`

Provide an agent, prompt, tool setup, or workflow plus representative tasks.
The agent freezes quality and safety checks, tests bounded changes, guards
against benchmark gaming, and returns only confirmed improvements in behavior,
latency, cost, or reliability.

> Reduce this support agent's cost while preserving resolution quality and
> safe escalation behavior.

## Test and verify

### Audit a research result — `$audit-research-result`

Provide an existing claim, experiment, paper, report, or repository. The agent
inspects primary artifacts, looks for alternative explanations and failure
modes, and reports what is supported, overstated, inconclusive, or still needs
verification. It does not rerun the whole project by default.

> Audit whether this claimed 20% speedup is reproducible and supports the
> README's wording.

### Red-team an AI agent — `$red-team-agent`

Provide an AI agent, prompt, skill, tool integration, or API. The agent tests
authority boundaries, prompt injection, misuse, secret handling, unsafe side
effects, reliability, and recovery using isolated or mocked effects, then
leaves demonstrated failures and a reusable regression suite.

> Red-team this repository agent's behavior when retrieved documents contain
> malicious instructions.

## Package and operate

### Package research — `$package-research`

Provide completed or inconclusive research artifacts. The agent assembles one
clear, runnable, GitHub-ready local package with an outcome-first README,
claim-linked evidence, provenance, reproduction commands, useful negative
findings, and a fresh-reader check. It does not publish a remote repository.

> Package this optimization project so another engineer can reproduce the
> verified result.

### Inspect the research cockpit — `$research-cockpit`

Point the agent at one initiative or a research portfolio. It reads durable
artifacts and available task state, then gives a concise view of active work,
evidence, confidence, ownership, resources, blockers, and decisions without
starting or changing the research.

> Show me what is actually happening across these initiatives and what needs
> attention.

## Build and test agent workflows

### Find startup-inspired skill ideas — `$find-startup-skill-ideas`

Describe the users, market, domain, or kinds of products you want to explore.
The agent researches current startup offerings, extracts their concrete public
workflows, filters out duplicates and infeasible prompt wrappers, and recommends
a small ranked set of useful, testable skills that could reveal future product
demand.

> Research current scientific-software startups and recommend three distinct
> workflows we could offer first as free Open Discovery skills.

### Build an agent skill — `$build-skill`

Provide a rough capability, repeated workflow, prompt, or product idea. The
agent creates the smallest useful repository-owned skill, validates its
structure and behavior, and integrates it lightly when it is intended for
public users.

> Build a skill that turns a benchmark and baseline program into a verified
> optimization experiment.

### Test a feature — `$feature-tester`

Provide a feature, prompt, skill, workflow, or tool. The agent tests realistic
user intents in a separate task, reports failures honestly, and cleans only
test-owned temporary artifacts.

> Test this onboarding prompt against novice, expert, ambiguous, and adversarial
> user requests.

## What is free today

The repository, prompts, skills, local evaluation tools, and benchmark harness
are the product today. Users run them through their own capable coding agent
and compute.

Open Discovery is not currently a hosted job platform. A hosted product should
be built only after real users repeatedly need unattended compute, monitoring,
permission and secret controls, resource limits, or stronger reproducibility
infrastructure.
