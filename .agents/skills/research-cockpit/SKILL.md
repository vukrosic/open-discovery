---
name: research-cockpit
description: Inspect one or many Open Discovery initiatives and summarize their real state from durable project artifacts and available task state. Use when a researcher asks for a cockpit, portfolio overview, status check, progress report, ownership map, evidence or confidence summary, blocker review, resource or cost view, or help deciding what needs attention across active research work.
---

# Research Cockpit

Give the researcher an at-a-glance, evidence-backed view of the work without
making them navigate its internal files. Adapt the depth and format to the
number of initiatives and the decision they need to make.

## Set the scope

Infer the target from the request, supplied paths, and current workspace. For a
single named initiative, focus on it. For a lab or portfolio request, discover
the relevant initiatives and summarize the whole set. Ask one concise question
only when materially different scopes remain plausible after inspection.

Work read-only by default. Do not edit research state, rerun experiments,
provision a dashboard or monitoring system, start or contact agents, query
external systems, or create a recurring cadence unless the user separately
authorizes it. A status request does not authorize new research.

## Inspect the work

Read the governing brief and local constraints first when they exist. Do not
assume a fixed project layout or required filenames: discover the artifacts
the work actually uses. Inspect enough primary material to establish:

- the human-set outcome and each active question;
- experiments or investigations that are planned, running, completed, failed,
  paused, or superseded;
- direct evidence, negative results, deviations, and important missing checks;
- current owner or sole writer where recorded;
- resource and cost use that is documented in ledgers, logs, receipts, or run
  metadata;
- blockers, dependencies, decisions already made, and pending decisions.

Use efficient inventory and targeted reads rather than opening every file.
Trace consequential status or result claims to the artifacts that support
them. Inspect raw outputs, protocols, code, logs, reports, and version records
when they can change the summary. Treat task state as operational evidence of
whether work is queued, running, finished, failed, or awaiting attention; it
does not prove a scientific result. Do not wake, message, or otherwise alter a
task merely to obtain status.

## Reconcile the evidence

Prefer primary artifacts over summaries and both over chat claims. Compare
claims, recorded status, timestamps, task state, and outputs rather than
silently choosing one. Call out conflicts, stale status, inaccessible
artifacts, and unknown ownership explicitly.

Distinguish:

- observed results from interpretation and speculation;
- completed execution from planned work;
- a same-owner check from independent verification;
- recorded spending from estimates or possible future cost;
- a blocked project from one that is merely idle, slow, or finished.

Calibrate confidence in plain language to evidence quality, agreement,
coverage, and verification. Explain the decisive reason for low or high
confidence; do not impose a universal score, rubric, traffic-light gate, or
completion percentage. Never infer precision that the artifacts do not
support.

## Present the cockpit

Lead with the answer the researcher most needs: what is happening, what the
evidence currently supports, and what needs a decision. Keep the default view
concise and expand only where uncertainty or consequence warrants it.

For one small initiative, use a short narrative or compact bullets. For
several initiatives, use a compact comparison table followed by only the
important evidence, conflicts, or decisions. Cover, as applicable:

- goal and current question;
- status and owner;
- latest material experiment or evidence;
- supported conclusion and confidence;
- resources or cost actually recorded;
- blocker or uncertainty;
- decision made, recommended next action, or authority needed.

Separate facts from recommendations. Make every important limitation visible,
including initiatives or artifacts not inspected. If nothing requires action,
say so. If a decision is needed, name the smallest decision and why it matters.
Link or cite local artifacts when provenance would help, without burying the
researcher in paths.

Return the cockpit in chat by default. Offer or create a self-contained local
HTML view only when the scale or requested use makes it materially clearer and
the user has authorized writing an output; keep it a view over inspected state,
not new monitoring infrastructure.
