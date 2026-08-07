---
name: literature-review
description: Autonomously create or resume an Open Discovery project, run a reproducible literature review with one research worker, preserve exact searches and claim-level evidence, and deliver a verified PDF report. Use only when the user clearly asks for a literature review, evidence review, research landscape, state-of-the-art review, related-work review, or a review report from existing sources. Do not use for casual research questions, fact-finding, source lookup, experiments, or general autonomous research.
---

# Literature Review

Complete the review without making the user manage scope forms, approve search
steps, or answer routine questions.

This workflow adapts
[Deli_AutoResearch](https://victorchen96.github.io/auto_research/framework.html)'s
file persistence, uninterrupted-work, and structural-pivot principles to a
single-worker literature review. It deliberately omits the original
framework's agent swarms and watchdog layers.

## User-facing promise

In the first response, name this skill and state the outcome:

> I’ll use the Literature Review skill to create an Open Discovery project and
> complete the review autonomously. One research worker will search and verify
> the literature, preserve the evidence, and deliver a PDF report. I’ll return
> when it is complete or if a hard blocker makes completion impossible.

Adapt the wording to the supplied topic. Do not ask for confirmation. If the
topic is broad, choose and record a useful, defensible scope. If no topic is
provided, choose one concrete review question and explain the choice in the
project record.

## Initialize the project

1. Find the Open Discovery repository root.
2. Read `AGENTS.md`, `docs/EVIDENCE-STANDARD.md`,
   `docs/STATE-MODEL.md`, and `docs/LITERATURE-REVIEW-LOOP.md`.
3. Create a new unique `projects/<project-slug>/` folder unless the user
   explicitly asks to resume an existing project. Copy every file from
   `templates/project/` into it.
4. Complete the project record yourself. Set collaboration mode to
   `autonomous literature review`. Treat invocation of this skill as authority
   for local, zero-cost, non-destructive review work, public-source searching,
   ordinary research downloads, and project-local dependency installation.
5. Exclude spending, publication, external messages, account or credential
   changes, private-data access, and destructive changes outside the project.
   Work around unavailable actions instead of asking for broader authority.

## Use one worker

Use exactly one research worker by default.

- If the current agent is doing the research directly, it is the worker. Do
  not launch another agent.
- If the host supports a user-facing orchestrator plus background workers,
  launch exactly one native Codex worker using `gpt-5.6-luna` with maximum
  reasoning effort when that model choice is available. Give it the prompt in
  `references/worker-prompt.md`.
- If Luna or worker launching is unavailable, continue with the strongest
  available current agent. Do not stop or ask the user to select a model.
- Do not launch parallel searchers, guardians, reviewers, or agent swarms
  unless the user explicitly requests multiple agents.
- If the worker crashes or stalls, resume or replace that same single-worker
  lane from the project files. Never run the old and replacement workers at the
  same time.

## Execute the review

1. Create `reviews/REV-001/` or the next unused review ID and copy every file
   from `templates/literature-review/` into it.
2. Complete and freeze `REVIEW-SPEC.md`; mark the review Running. The skill
   invocation is the authorization record, so do not stop for approval.
3. Search reproducibly. Before downloading or extracting a source batch,
   record the exact queries, dates, filters, visible result counts, candidate
   identifiers, initial screening decisions, and access limits in
   `SEARCH-LOG.md`. Process no more than five new candidate sources per batch;
   do not bulk-download unlogged candidates.
4. Prefer primary and authoritative sources. Open the actual source before
   relying on it. Never treat a search snippet as source evidence.
5. Add claim-level evidence, stable identifiers, methods, limitations, and
   verification status to `EVIDENCE-TABLE.md` as the review proceeds. Before
   starting another search or download batch, checkpoint both the search log
   and evidence table. Never let downloaded evidence get more than one batch
   ahead of the durable ledgers, and never rely on chat history as the only
   record.
6. Use citation chaining and varied queries when useful. When a direction
   produces no new material evidence, change the search mechanism rather than
   repeating nearby wording.
7. Complete `SYNTHESIS.md` with established, disputed, unsupported, and unknown
   findings. Separate direct source evidence from interpretation.
8. Update `FINDINGS.md`, `PROGRESS.md`, `IDEAS.md`, and `WORK-LOG.md` before
   finishing. Record gaps or possible experiments as unexecuted future work.
   Do not run experiments under this skill.

## Deliver the PDF report

Complete `REPORT.md` as the reader-facing report, then render
`REPORT.pdf` in the same review folder. Include:

- the review question and concise executive summary;
- scope, search method, coverage, and stopping rule;
- the strongest findings and their evidence strength;
- conflicting evidence and unresolved gaps;
- limitations and access constraints;
- full references with stable links or identifiers.

Use the host's PDF/document capability or an available local renderer. Install
a zero-cost project-local dependency when needed. Verify the final PDF by
checking that it exists, is non-empty, opens as a valid PDF, contains the
expected pages and text, and has no visibly clipped or broken content. Repair
the report before declaring completion.

If any dependency is installed, record its name, version, installation
location, and purpose in `WORK-LOG.md`. Explicitly tell the user about the
installation in the final handoff. Never describe an existing tool as newly
installed.

## Avoid interruptions

Do not ask the user to choose databases, date ranges, source limits, wording,
or report structure. Make conservative decisions and log them.

- If one source is inaccessible, find an accessible primary source or record
  the limitation and continue.
- If the topic is too broad, narrow it to a coherent decision-relevant review.
- If evidence is sparse, complete an honest negative or inconclusive review.
- If a tool fails, diagnose it, use a safe fallback, and continue.

Return early only when no safe route can produce a defensible report. A hard
blocker is not ordinary ambiguity, a failed query, an inaccessible paper, or a
missing preferred tool.

## Finish

Return only after `REPORT.pdf` and the durable review record are complete, or
after exhausting safe alternatives. Report the project path, review ID,
included-source count, narrowest conclusion, largest limitation, and clickable
links to `REPORT.pdf`, `REPORT.md`, `SYNTHESIS.md`, and `EVIDENCE-TABLE.md`.
Also report every project-local dependency installed during the review,
including its version, location, and purpose.
