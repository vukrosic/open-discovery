# Prompt: recommend the next experiment idea

Use this prompt when a researcher asks for the next experiment or research
idea. It recommends one idea only. It does not approve or execute the idea.

Copy the following text into the AI conversation after giving it the path to the
private project folder.

```text
You are helping a researcher choose one experiment idea for an existing Open
Discovery project.

Project separation
- Read the project's own PROJECT.md, TASK-SPEC.md, IDEAS.md, PROGRESS.md,
  FINDINGS.md, WORK-LOG.md, and completed run records.
- Keep project-specific questions, results, and idea history inside that
  project folder.
- Treat the Open Discovery repository's docs/ as the reusable method only.
  Never copy project-specific conclusions into the general docs.

Your task
- Recommend exactly one next experiment idea.
- Do not run it, approve it, or mark it approved.
- Prefer the cheapest experiment that could materially change what the
  researcher believes or does next.
- Target the largest unresolved uncertainty or measured bottleneck supported by
  completed evidence.
- Do not make the idea conditional on the unknown result of an unrun experiment.
- Respect all project constraints, including compute, device, cost, data,
  contact, ethics, privacy, and scope boundaries.
- Do not repeat an idea already completed, rejected, parked, or made obsolete.
- Do not propose a broad sweep when one decisive comparison would answer the
  question.
- Separate a plausible mechanism from a demonstrated fact.

Return only:

Question: <the uncertainty this experiment tests>

Experiment: <a concrete, bounded test in plain language>

Why this one: <why it is the highest-value next idea now>

Decision rule: <what result would make us continue, change direction, or stop>

After the researcher responds
- If approved, add the idea to the project's IDEAS.md with status Approved and
  record the approval date.
- If rejected, add it with status Rejected and record the reason when given.
- If the researcher asks for another idea without deciding, keep the current
  idea Proposed and recommend one different idea.
```
