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

Prefer official code. If none exists, clearly label the result a
reimplementation. Run the baseline and inspect its actual outputs before
claiming reproduction. Only after a terminal baseline should the agent offer or
autonomously pursue adaptation when the original brief requests it.

Invocation authorizes public paper and repository retrieval, zero-cost public
downloads, project-local dependencies, code execution, and non-destructive
initiative-local edits. It does not authorize spending, outside compute,
private assets, credentials, publication, external communication, or
destructive changes.
