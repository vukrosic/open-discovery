---
name: package-research
description: Turn inspected research, experiment, reproduction, or optimization artifacts into one clear, runnable, GitHub-ready local repository package with an outcome-first README, claim-linked evidence, reproducibility commands, provenance, useful negative findings, and fresh-reader verification. Use when asked to package, consolidate, polish, hand off, or prepare completed or inconclusive technical work for a repository; do not use it to perform the underlying research or publish a remote repository.
---

# Package Research

Convert existing evidence and code into the smallest repository another person
can understand, run, check, and continue without chat history.

When working inside Open Discovery, first read
`agents/REPOSITORY-ARTIFACT-BUILDER.md` and its linked repository guidance when
present. Treat those as canonical; apply this skill as the packaging workflow
rather than restating their broader policy.

## Establish the package boundary

Inspect repository instructions, current state, the governing request or brief,
the actual source artifacts, and any review or acceptance decision. Do not rely
on chat summaries for consequential claims. Identify:

- the strongest accepted claim or honest negative conclusion;
- the exact evidence, code, configuration, and commands that support it;
- material limits, contradictions, failed approaches, and unresolved gaps;
- source, dataset, model, dependency, prompt, environment, and authorship
  provenance;
- the recorded canonical package folder, if one exists.

Use one package for the coherent initiative or body of work. Update its recorded
canonical folder instead of creating competing or project-by-project packages.
Treat canonical research artifacts as read-only unless the user explicitly
authorized changing them. If the destination remains materially ambiguous
after inspection, ask one concise question before writing.

Packaging may clarify a claim but cannot strengthen it. Do not rewrite weak
science as a success, invent missing evidence, silently drop contradictory
results, or run new research merely to make the package look complete. Record a
missing check as a limitation or release blocker.

## Build the smallest useful repository

Choose structure from the work rather than a template. Copy or adapt only the
files needed to understand, reproduce, verify, or continue the accepted result.
Keep the first screen of `README.md` outcome-first:

1. say what was tested or built;
2. state what happened and the supported claim boundary;
3. explain why the result is useful;
4. give the shortest working setup or run path;
5. link to deeper evidence, reproduction, provenance, limitations, or
   continuation material only when those deserve separate files.

Preserve exact runnable commands and enough environment detail to repeat the
material checks. Carry forward evidence identifiers and source versions or
hashes where available. For large, licensed, private, or machine-specific
dependencies, provide lawful retrieval or regeneration instructions rather
than copying them. State unresolved license status instead of inventing a
license.

Include failed or negative work when it changes interpretation, explains an
important design choice, rules out a tempting dead end, or gives the next
researcher a useful continuation point. Keep routine abandoned exploration out
of the main path. A negative or inconclusive result can be the package's honest
headline outcome.

## Exclude and clean safely

Keep secrets, credentials, private data, unrelated lab state, local caches,
large downloads, transient logs, generated junk, and machine-specific absolute
paths out of the package.

Before deleting anything, resolve its exact path and confirm from provenance or
the current run that it is disposable and test-owned. Remove only garbage owned
by the package or its isolated verification. Otherwise leave the source intact,
exclude the item from the package, add a narrow ignore rule when useful, and
report it. Never clean canonical source artifacts merely because they are not
part of the public package.

## Verify as a fresh reader

Inspect every packaged file, then exercise the repository from its documented
entry point in a clean temporary copy or isolated environment when practical.
Use the cheapest checks that genuinely test the package, adapted to its
contents. Confirm that:

- README links, relative paths, setup steps, and commands work;
- headline claims and numbers match preserved evidence;
- required code, configuration, small evidence, and provenance are present;
- the package does not depend silently on the source workspace or chat history;
- secret, absolute-path, cache, junk, and unexpectedly large-file scans are
  clean;
- any unrun expensive, external, or unavailable reproduction is named exactly.

Verification tests packaging and documented reproducibility; it does not
authorize new measurements, spending, private access, or external actions.
Remove only the isolated temporary material created by this verification.

## Hand off honestly

Return the local package path, its accepted claim boundary, the main contents,
the exact validation performed and observed result, anything intentionally
excluded or cleaned, and remaining limitations or release blockers. Do not
create a GitHub repository, remote, commit, push, publish, or send external
messages without explicit authorization.
