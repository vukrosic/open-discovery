# Quick start

This walkthrough creates one Open Discovery project using only Markdown.

For an AI-assisted start, copy the prompt in
[`KICKOFF-PROMPT.md`](KICKOFF-PROMPT.md). For a completed reference, inspect
the [`robust-summary example`](../examples/robust-summary/README.md).

## 0. Check whether the work is supported

Read [`SUPPORTED-RESEARCH.md`](SUPPORTED-RESEARCH.md). If the project requires
additional controls, identify the real institutional system and qualified human
review before continuing. If the work is unsupported or eligibility is unknown,
stop at planning.

## 1. Create a separate project folder

Copy every file from `templates/project/` into a new folder outside this public
harness repository, or into a private project repository.

Do not place project-specific evidence or conclusions in `docs/` here.

## 2. Define the project with the human

Complete `PROJECT.md` first. Write:

- one concrete research question;
- why answering it changes a decision or belief;
- direct evidence, assumptions, and unknowns;
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
