# Literature review prompt

The preferred route is the repository skill:

`Use $literature-review to review [your topic] and deliver a PDF report.`

The skill creates a unique Open Discovery project, uses one research worker by
default, completes the source-tracked review without routine approval stops,
and returns a verified `REPORT.pdf`.

Use the standalone prompt below only when the host cannot discover repository
skills. Replace the bracketed topic.

```text
Run one complete Open Discovery literature review on [TOPIC OR QUESTION].

Create a unique project under projects/ and copy in templates/project/. Create
reviews/REV-001/ and copy in templates/literature-review/. Treat this request
as authorization for local, zero-cost, non-destructive review work and public
source retrieval. Do not ask me to fill out forms, approve the review, choose
databases, or select a model.

Use one research worker. Prefer gpt-5.6-luna with maximum reasoning effort when
the host supports that selection; otherwise use the strongest available agent
and continue. Do not launch subagents or run experiments.

Read AGENTS.md, docs/EVIDENCE-STANDARD.md, docs/STATE-MODEL.md, and
docs/LITERATURE-REVIEW-LOOP.md. Freeze a defensible review specification, log
exact searches and screening decisions, verify actual sources, extract
claim-level evidence, synthesize established/conflicting/unsupported/unknown
findings, and update every project ledger.

Complete REPORT.md and render a verified REPORT.pdf in the review folder. Work
around inaccessible sources and failed tools. If you install a project-local
dependency, record its name, version, location, and purpose in WORK-LOG.md and
tell me about it in the final response. Return only when the PDF and durable
review record are complete, or when all safe alternatives are genuinely
blocked.
```
