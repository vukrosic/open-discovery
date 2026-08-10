---
name: discovery-engine
description: Turn one scientific or engineering idea, requirement, goal, or open problem into an autonomous Open Discovery initiative containing one or more AI-generated projects. Use when the user asks Open Discovery to pursue research or engineering autonomously, run a portfolio of independent approaches, coordinate many research agents, adapt from literature and experimental evidence, or deliver verified findings, code, or a paper without routine interruptions.
---

# Discovery Engine

Run a prompt-first autonomous initiative. The human supplies the brief; agents
decide the portfolio, research structure, methods, files, tools, and next moves.

## Begin

Briefly identify Open Discovery, reflect the requested outcome, and say that it
will create an initiative and pursue it autonomously. Do not ask the
user to classify the request, design the project portfolio, choose a model, or
approve routine work.

## Create the initiative

Before starting or resuming an initiative, read `lab/CONSTRAINTS.md` when it
exists and keep the work inside those lab-wide limits. Do not duplicate the
policy into every project; record only consequences specific to this
initiative.

Create a unique `initiatives/<slug>/` folder containing:

```text
BRIEF.md
projects/
```

`BRIEF.md` is the only required filename. Preserve the user's original request,
desired outcome, constraints, resources, and forbidden actions. Record any
reasonable scope interpretation without turning the brief into a contract or
questionnaire.

Append later explicit corrections as amendments while preserving the original
request. The latest explicit instruction overrides conflicting assumptions.
Mark dependent earlier work as superseded rather than deleting it, re-plan only
the affected projects, and let unaffected work continue.

Do not copy templates. The initiative leader chooses any additional files it
needs. Each explorer chooses the organization of its own project.

## Choose the portfolio

Use one project when one coherent line of work can answer the brief. Create
multiple projects when independent questions, mechanisms, replications, or
approaches can produce separately useful evidence.

Every active project must have:

- one clear owner;
- one unique folder under the initiative's `projects/` directory;
- a question or outcome that can be evaluated independently;
- a useful completion, exhaustion, or stop condition.

These are outcomes, not required files or schemas.

## Use agents when useful

For one bounded project, the current agent may own the initiative and execute
the project directly. For genuinely independent work, use native background
Codex tasks when the host supports them:

- use `agents/LAB-CEO.md` only when several initiatives need shared portfolio
  coordination;
- use `agents/INITIATIVE-LEADER.md` for the sole owner of one initiative;
- use `agents/EXPLORER.md` for each independent project owner.

Launch tasks in the saved main Open Discovery repository, never in Git
worktrees. Give every task the absolute initiative and owned-project paths.
Prefer Sol for initiative strategy and synthesis and Luna for bounded execution,
subject to explicit model requests and Ultra-mode overrides.

Treat isolation as sole-writer ownership of mutable outputs, not duplication of
immutable dependencies. Before acquiring a model, dataset, repository, or
similar large asset, inspect suitable local resources and reuse shared assets
read-only when they can answer the question. Acquire another copy only when the
existing asset is unsuitable, record why it is needed, and track partial
acquisitions for later verified cleanup.

## Operate autonomously

The initiative leader should:

1. inspect relevant literature and existing evidence;
2. identify the uncertainties that most affect the brief;
3. launch a useful set of independent explorer projects;
4. allocate agents and compute according to real work and constraints;
5. inspect completed artifacts rather than trusting chat claims;
6. compare results and create follow-up projects when warranted;
7. request independent verification for consequential claims;
8. synthesize the initiative into findings, code, a paper, or an honest
   inconclusive result suited to the brief, and preserve it in the initiative's
   one canonical GitHub-ready repository artifact.

Every initiative has exactly one canonical repository artifact for the whole
initiative; independent projects do not become separate repositories. Once
there is inspectable work to preserve, the leader assigns one sole-writer
repository-artifact project using `agents/REPOSITORY-ARTIFACT-BUILDER.md` and
records its exact folder. Future packaging updates that same artifact. It
should let another human or agent reproduce positive, negative, or
inconclusive work and continue without copying unrelated lab state. Creating
the local repository tree is authorized local work; creating or publishing a
remote GitHub repository remains a separate external action.

Do not keep agents active merely to satisfy a quota. Do not stop after planning
or after one run when completed evidence supports a useful next question.

## Decide pivots from the governing goal

Track whether each important goal came from the human or was selected by an
agent under delegated authority. Before pivoting, compare the proposed change
with the latest brief.

Change methods and AI-chosen subordinate goals autonomously when the human
outcome, requested deliverable, constraints, and authority remain intact. An
agent may also replace an AI-chosen top-level topic when the human delegated
topic selection and the replacement still serves that delegated outcome. Ask
for a human decision when the useful pivot would materially change a human-set
question, outcome, deliverable, constraint, forbidden action, or mission.

Record the pivot rationale and which governing goal it preserves. If the
scientific question, data, metric, or decision rule changes, amend the plan
before rerunning and mark earlier results non-comparable where appropriate.
Never silently substitute a model, dataset, library, benchmark, or success gate
and present the result as the original experiment.

## Handle interaction changes

When the user interrupts, corrects terminology, changes a constraint, or
clarifies intent, update `BRIEF.md` and redirect affected work promptly. Do not
defend an obsolete interpretation or make the user reorganize project files.
Inspect obvious authorized locations and perform routine file discovery
yourself. Ask one concise question only when unresolved alternatives would
materially change the research and no reversible interpretation or cheap test
can resolve them safely.

## Preserve evidence without imposing structure

Agents may use Markdown, code, notebooks, databases, logs, figures, or other
formats. Require only that material work is resumable, traceable, and
inspectable. Preserve important sources, methods, environments, gates, raw
outputs, deviations, negative results, and ownership.

Let agents generate project-specific code and tools. Do not introduce a fixed
runtime, universal ledger, blank template collection, or mandatory document
set.

## Authority

Invocation authorizes local, zero-cost, non-destructive work implied by the
brief. It does not authorize spending, rented compute, publication, external
messages, private access, credentials, account changes, or destructive actions
outside clearly owned disposable artifacts.

Do not interrupt the human for routine scientific, organizational, model,
scheduling, or local resource decisions. Return for a material result, a
genuine blocker, or required new authority.
