# Literature review loop

This loop maps existing evidence and ends with a source-tracked PDF report. It
supports bounded scoping and evidence reviews. It does not run experiments or
claim to be a publication-grade systematic review unless the project supplies
and meets the relevant field standard.

## 1. Freeze the review specification

Before searching, record:

- the exact question and decision the review should change;
- review type and required level of completeness;
- included populations, systems, methods, outcomes, dates, languages, and
  source types;
- explicit exclusions;
- databases, sites, archives, or corpora available;
- evidence-quality rules and synthesis method;
- time, source-count, access, and stopping limits.

## 2. Search reproducibly

For every search, preserve the source, date, exact query, filters, result count,
and access limitations. Do not describe a review as exhaustive when important
databases, dates, languages, or full texts were unavailable.

Prefer primary sources for claims about methods and results. Secondary sources
may provide context or discover primary work, but they must not silently replace
the underlying evidence.

## 3. Screen transparently

Record why each serious candidate was included, excluded, or left unresolved.
Deduplicate sources without losing identifiers. Never invent a citation or
pretend to have read inaccessible material.

## 4. Extract claim-level evidence

Link each extracted claim to one source and distinguish:

- what the source directly reports;
- the reviewer's interpretation;
- relevant method, sample, comparison, and outcome;
- limitations, conflicts, and applicability to the project.

## 5. Synthesize without vote counting

Do not treat the number of papers as the strength of evidence. Compare source
quality, methods, populations, outcomes, effect direction, uncertainty, and
conflicts. Record established findings, disputed findings, and remaining gaps.

## 6. Update the shared research memory

Complete `SYNTHESIS.md`, then update `FINDINGS.md`, `PROGRESS.md`, `IDEAS.md`,
and `WORK-LOG.md`. The next idea must follow from reviewed evidence, not from an
unverified search snippet.

## 7. Deliver the report

Complete `REPORT.md`, render `REPORT.pdf`, and verify the final PDF opens,
contains the expected text and pages, and has no visibly clipped or broken
content. The report must summarize the review question, method, coverage,
findings, conflicts, gaps, limitations, and full references.

## Autonomous completion rule

When invoked through the Literature Review skill, do not stop to ask the user
to choose scope, databases, dates, source counts, or report structure. Choose
conservative defaults and record them. Use exactly one research worker unless
the user explicitly asks for multiple agents.

Finish when the frozen stopping rule is met and the PDF and durable evidence
record are complete. If sources are inaccessible, use accessible alternatives
and record the limitation. If the scope is too broad, narrow it. If evidence is
sparse, complete an honest negative or inconclusive report. Return Blocked only
after safe alternatives are genuinely exhausted.
