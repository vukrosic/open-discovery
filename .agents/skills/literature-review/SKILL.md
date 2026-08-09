---
name: literature-review
description: Autonomously review existing literature for a scientific or engineering question using one research worker by default, preserve source provenance and exact searches in a flexible initiative project, and deliver a verified source-tracked PDF report. Use only for explicit literature, evidence, state-of-the-art, landscape, or related-work review requests.
---

# Literature Review

Create one Open Discovery initiative from the request, write its `BRIEF.md`, and
create one review project beneath `projects/`. Do not copy templates or require
the user to fill out a scope form.

In the first response, identify Starberry and the Literature Review skill, say
that one worker will complete the review autonomously, and promise a
source-tracked PDF report.

Use one worker by default. If a user-facing orchestrator can launch a native
Codex task, prefer `gpt-5.6-luna` and choose reasoning effort from the review's
difficulty and consequence; otherwise work directly with the strongest
available agent. Do not launch a swarm unless the user explicitly requests one.

Before searching, decide and preserve a defensible review question, scope,
cutoff, source types, inclusion logic, search approach, and stopping rule in
whatever project-local form is clearest. Then:

- search primary and authoritative sources across relevant terminology;
- preserve exact queries, dates, identifiers, access limits, and screening
  decisions;
- connect important claims to sources;
- separate established evidence, disagreement, uncertainty, and inferred gaps;
- never invent a citation, quotation, result, or access claim;
- produce and visually verify `REPORT.pdf` inside the project.

The worker chooses its own supporting files and organization. The required
outcome is a reproducible evidence trail and verified PDF, not a prescribed set
of Markdown documents.

Invocation authorizes public-source search, zero-cost downloads, project-local
dependencies, and non-destructive initiative-local edits. It does not authorize
spending, publication, external messages, private access, credentials, account
changes, or destructive changes outside owned disposable material.

Ordinary ambiguity, unavailable papers, failed queries, or model substitution
are not reasons to interrupt the user. Narrow honestly, use safe alternatives,
and finish an inconclusive review when necessary.
