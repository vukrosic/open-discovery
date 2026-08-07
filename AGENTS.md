# AI agent operating contract

This repository is a Markdown-only research harness. The files in each project
are the durable source of truth; chat history is not.

## Before doing research work

Read, in order:

1. `PROJECT.md`
2. `TASK-SPEC.md`
3. `IDEAS.md`
4. `PROGRESS.md`
5. `FINDINGS.md`
6. the most recent entries in `WORK-LOG.md`

Then inspect the protocol and evidence for any active run.

## Required behavior

1. Keep project-specific questions, evidence, and conclusions inside that
   project's folder. Keep this repository's `docs/` general.
2. Treat proposed, approved, running, completed, rejected, inconclusive, and
   published as different states. Never infer one from another.
3. Recommend only one next idea and base it on completed evidence.
4. Do not make a proposal depend on the unknown result of an experiment that
   has not run.
5. Freeze the run's `PROTOCOL.md` and decision rule before executing it.
6. Run the cheapest test that could decide whether the direction deserves more
   work.
7. Preserve raw evidence, versions, environment details, deviations, failures,
   and negative results.
8. Separate direct observations from interpretation and speculation.
9. Do not claim success from a profile, partial run, average that hides a failed
   required case, or a result that violates its own gate.
10. After two stale iterations, change mechanism instead of micro-tuning the
    same failed direction.
11. Update `RESULT.md`, `FINDINGS.md`, `PROGRESS.md`, `IDEAS.md`, and
    `WORK-LOG.md` before beginning another run.
12. Respect the session limit and every human authority, cost, compute, safety,
    privacy, ethics, legal, access, and external-action boundary.
13. Check `docs/SUPPORTED-RESEARCH.md` before execution. If the work requires
    controls that are not confirmed, is unsupported, or has unknown eligibility,
    stop at planning and return to the human.

## Authority rule

The harness records authority; it does not create authority.

An AI may continue without asking only when `PROJECT.md` explicitly grants
bounded autonomous execution and the next action remains inside those written
limits. Downloads, spending, publication, messages, destructive changes,
account changes, human-subjects work, and scope expansion require the authority
defined by the human and the surrounding environment.

## Stopping rule

Stop and return to the human when:

- the protocol requires a decision only the researcher can make;
- the next action exceeds the written authority;
- safety, ethics, privacy, legal, access, or cost conditions are uncertain;
- the evidence contract cannot be satisfied;
- the bounded session ends;
- the researcher asks the system to stop.
