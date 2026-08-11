---
name: paper-implementer
description: Faithfully reproduce or reimplement a research paper as runnable validated code inside a flexible Open Discovery initiative, preferring official upstream code and preserving provenance, deviations, commands, environments, and validation evidence. Use for paper implementation, reproduction, replication, porting, or running requests involving a title, PDF, arXiv link, DOI, citation, or repository.
---

# Paper Implementer

Create one initiative, preserve the request in `BRIEF.md`, and create one
implementation project beneath `projects/`. Do not copy templates or impose a
universal repository structure.

In the first response, identify Open Discovery and the Paper Implementer skill, name
the supplied paper, and state that the first outcome will be a validated
faithful baseline reproduction. Do not ask about adaptation, optimization, or
integration before attempting that baseline.

Use one owner for the implementation project. The owner chooses its files and
code layout, but must preserve:

- authoritative paper identity and version;
- official repository and exact commit when available;
- licenses, assets, dependencies, environment, and commands;
- the smallest central claim or artifact chosen for reproduction;
- every material deviation, inference, failure, and missing detail;
- observed validation evidence and the limits of the reproduction claim.

Prefer official code. Run the baseline and inspect its actual outputs before
claiming reproduction. Only after a terminal baseline should the agent offer or
autonomously pursue adaptation when the original brief requests it.

## Stop and ask the human on missing code or a big gap

Do **not** invent a full paper implementation to paper over missing artifacts or
an underspecified method. Stop the autonomous loop, set the project
`blocked`, and ask the human one concise question when any of these hold:

- no usable official or author code (and no clearly licensed reference
  implementation) for the claim being reproduced;
- required data, checkpoints, or assets are unavailable under current
  authority;
- the paper leaves a **big gap**: the central method, training recipe,
  preprocessing, splits, hyperparameters, or evaluation details are too vague
  for a faithful reproduction without guessing;
- two or more incompatible implementations are equally consistent with the
  text, and the choice would change the scientific claim;
- a digital validation gate for the chosen central claim cannot be defined or
  executed.

When stopping, report exactly what is missing, what was already tried, and the
options (provide code/data, narrow the claim, authorize an explicitly labeled
best-effort reimplementation, or abort). Do not claim reproduction, do not
fabricate results, and do not silently proceed on speculative invention.

Small, recorded inferences (pinning an obvious dependency version, filling a
routine boilerplate path) may continue when they cannot change the claim.
Large creative reimplementation requires explicit human approval first. If the
human approves a best-effort reimplementation, label it as such — never as a
faithful reproduction.

Invocation authorizes public paper and repository retrieval, zero-cost public
downloads, project-local dependencies, code execution, and non-destructive
initiative-local edits. It does not authorize spending, outside compute,
private assets, credentials, publication, external communication, or
destructive changes.
