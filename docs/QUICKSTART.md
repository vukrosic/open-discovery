# Quick start

This walkthrough creates one local Open Discovery project through an AI chat.

For an AI-assisted start, copy the prompt in
[`KICKOFF-PROMPT.md`](KICKOFF-PROMPT.md). For a completed reference, inspect
the [`robust-summary example`](../examples/robust-summary/README.md).

## 1. Start through the agent

For an autonomous literature review with a PDF deliverable, use:

`Use $literature-review to review [your topic] and deliver a PDF report.`

Starberry creates the project, uses one research worker by default, records the
scope and search method internally, and returns when the verified report is
complete. You do not need to approve individual search steps or fill out the
project templates.

Open the cloned Open Discovery repository with Codex, Claude, or another
file-capable agent and state a question, topic, field, or Full Auto request. The
agent creates a unique `projects/<project-slug>/` folder and copies every file
from `templates/project/` into it.

The repository root is never a research project. Do not place `PROJECT.md`,
project evidence, or conclusions at the root or in `docs/`. New parallel
requests must use different project folders. The `projects/` directory is
ignored by Git, so local research is not included in releases.

### Add an existing project

You can also give the agent the path or repository URL of work that already
exists, including a sibling folder or a project elsewhere on the computer. The
agent creates a lightweight Open Discovery record under `projects/`, writes the
original location and useful navigation notes into `PROJECT.md`, initializes
the remaining project ledgers, and leaves the original project in place. A
single pointer file is not enough because the project must remain resumable.

The record does not grant permission to modify the original project. The agent
first inspects it read-only and edits it only when the researcher explicitly
authorizes that work. If an Open Discovery record already points to the same
location, the agent should resume it instead of creating a duplicate.

Copy-paste example:

`Add my existing project to Open Discovery: [folder path or repository URL].`

## 2. Define the project with the human

Skip this section when using `$literature-review`; the skill completes and
freezes the project and review records autonomously.

Inside the generated project folder, complete `PROJECT.md` first. Write:

- one concrete research question;
- why answering it changes a decision or belief;
- direct evidence, assumptions, and unknowns;
- whether this is new research or an existing project, including its location;
- constraints and forbidden actions;
- exactly what the AI may do without asking again.

Then complete `TASK-SPEC.md`. Freeze the baseline, success criteria, evidence
requirements, session limit, and stopping rule.

## 3. Record one next idea

Use the prompt in
[`experiment-idea-generation/PROMPT.md`](experiment-idea-generation/PROMPT.md).
Add the returned idea to `IDEAS.md` with status **Proposed**.

The human then records **Approved**, **Rejected**, or **Parked**. Do not hide
rejected ideas; they prevent repetition.

## Choose the next loop

- To map existing evidence, copy `templates/literature-review/` into a numbered
  folder such as `reviews/REV-001/` and use
  [`LITERATURE-REVIEW-PROMPT.md`](LITERATURE-REVIEW-PROMPT.md), or invoke
  `$literature-review` for the autonomous one-worker workflow.
- To execute an approved experiment, continue below or use
  [`EXPERIMENT-LOOP-PROMPT.md`](EXPERIMENT-LOOP-PROMPT.md).

A literature review and an experiment use the same `PROJECT.md`, `TASK-SPEC.md`,
`IDEAS.md`, `PROGRESS.md`, `FINDINGS.md`, and `WORK-LOG.md`. They are two ways
of updating one research memory.

## 4. Freeze the run

For an approved idea:

1. create a numbered folder such as `runs/EXP-001/`;
2. copy `templates/experiment/PROTOCOL.md` and `RESULT.md` into it;
3. fill in the question, method, evidence, constraints, and decision rule;
4. mark the idea **Running** only when execution actually starts;
5. update `PROGRESS.md`.

Do not change the success gate after seeing the result. If the protocol was
wrong, preserve the original decision and write a clearly labeled correction.

## 5. Run the smallest decisive test

Start with a cheap screen that can reject the direction. Preserve raw outputs,
inputs, sources, logs, versions, environment details, and deviations.

If the screen fails its gate, stop that direction. A negative result is a
complete result when it rules something out.

## 6. Record the result before continuing

Complete the run's `RESULT.md`, then update:

- `FINDINGS.md` with the reusable lesson and evidence link;
- `IDEAS.md` with the terminal run state;
- `PROGRESS.md` with the current baseline, stale count, and resume point;
- `WORK-LOG.md` with the decision and reason.

Only then recommend or start another run.

## 7. End or reset the bounded session

When the round or time limit is reached, stop execution and review the evidence.
Start a new bounded session only after writing a fresh scope and resume point in
`PROGRESS.md`.

## Minimum viable loop

A valid first loop needs only:

1. a completed project brief;
2. one approved idea;
3. one frozen protocol;
4. one preserved result, including a negative result;
5. one evidence-based next decision.

The worked example shows all five parts, including an experiment that improved
the average result but was still rejected because it failed required cases.
