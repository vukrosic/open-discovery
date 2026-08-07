# Literature review prompt

Use this for one bounded literature review. Copy
`templates/literature-review/` into the project's next numbered review folder,
then replace the bracketed paths below.

```text
Run one bounded Open Discovery literature review.

Open Discovery harness:
[ABSOLUTE PATH TO open-discovery]

Project folder:
[ABSOLUTE PATH TO PROJECT]

Review folder:
[ABSOLUTE PATH TO PROJECT/reviews/REV-###]

Read the harness AGENTS.md, docs/EVIDENCE-STANDARD.md, docs/STATE-MODEL.md, and
docs/LITERATURE-REVIEW-LOOP.md. Then read the complete project record and every
file already in the review folder.

Before searching:
1. Verify that the related review idea is explicitly Approved in IDEAS.md or
   falls inside a bounded review session explicitly authorized in PROJECT.md.
   Otherwise, draft REVIEW-SPEC.md as Proposed and stop for human approval.
2. Complete REVIEW-SPEC.md with the exact question, decision, review type,
   scope, inclusion and exclusion rules, source access, evidence standard,
   synthesis method, limits, and stopping rule.
3. Verify that the review is inside the recorded authority.
4. Stop for human input if any choice could materially change which evidence
   is included or what conclusion would follow.

During the review:
1. Search only the approved databases, sites, archives, or corpora.
2. Record every exact query, date, filter, result count, and access limitation
   in SEARCH-LOG.md.
3. Record important inclusion, exclusion, duplicate, and unresolved decisions.
4. Prefer primary sources for claims about methods and results.
5. Add each included source to EVIDENCE-TABLE.md with a real citation or stable
   identifier, direct evidence, limitations, and relevance.
6. Never invent a source, citation, quotation, full-text access claim, result,
   or bibliographic detail. If good evidence cannot be found, report that
   negative result directly.
7. Respect copyright, privacy, licensing, source-count, and time limits. Do not
   reproduce full copyrighted works.

At completion:
1. Write SYNTHESIS.md separating observed source evidence from interpretation.
2. State what is established, disputed, unsupported, and still unknown.
3. Describe search and access limitations; do not call the review exhaustive
   unless the frozen method justifies that claim.
4. Update FINDINGS.md, PROGRESS.md, IDEAS.md, and WORK-LOG.md.
5. Recommend at most one next research idea grounded in included evidence and
   mark it Proposed. Do not approve or execute it.

Stop when the frozen rule is met or a listed limit is reached. Report the review
ID, search coverage, included-source count, strongest finding, most important
limitation, and exact next human decision.
```
