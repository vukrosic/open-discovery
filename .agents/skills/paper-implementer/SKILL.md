---
name: paper-implementer
description: Faithfully reproduce a research paper as runnable, tested code inside an Open Discovery project, using the official repository when available and preserving exact upstream provenance, deviations, commands, and validation evidence. Use when a human or agent asks to implement, reimplement, reproduce, replicate, port, or run code from an academic paper, paper PDF, arXiv link, DOI, citation, or paper repository. Complete the baseline reproduction before offering environment adaptation, optimization, extension, or integration.
---

# Paper Implementer

Turn one paper into a faithful, runnable, evidence-backed implementation. Treat
reproduction and later adaptation as separate phases.

## Start without unnecessary questions

In the first response, identify the skill, name the paper or supplied reference,
and state that the first outcome will be a validated baseline reproduction.
Do not ask about preferred frameworks, hardware, optimization, or integration
before attempting the faithful baseline.

If the paper identity is ambiguous, resolve it from the supplied title, URL,
PDF, DOI, or citation. Ask only when multiple plausible papers remain and the
choice would materially change the implementation.

Invocation authorizes zero-cost public-source research, public paper and code
downloads, cloning a public repository into the project, project-local
dependencies, code execution, and non-destructive project-local edits. It does
not authorize spending, outside compute, private repositories or data,
credentials, publication, external communication, or destructive changes.

## Initialize the project

1. Find the Open Discovery root and read `AGENTS.md` plus the relevant research
   mode guide.
2. Create a unique `projects/<paper-slug>-implementation/` folder and copy
   `templates/project/` into it, unless explicitly resuming an existing project.
3. Create `implementation/` and copy the files from
   `templates/paper-implementation/` into it.
4. Record the paper identity, source locations, target claims, environment,
   authority, and exact project path in the durable project files.

## Use one implementation worker

- If already operating as the assigned explorer for this implementation,
  execute the workflow directly.
- If operating as a user-facing orchestrator with native workers available,
  launch one `gpt-5.6-luna` worker with `xhigh` reasoning and the complete
  prompt in `references/worker-prompt.md`.
- Do not launch a swarm by default. Add a specialist only when a concrete,
  separable blocker justifies it or the human explicitly requests parallelism.
- Keep one writer for the implementation project.

## Establish paper and upstream provenance

1. Obtain the paper from an authoritative source and preserve its stable URL,
   identifier, version, and access date.
2. Search for official author or organization code, supplementary material,
   model artifacts, data, issues, and documented environment details.
3. Prefer the official implementation when available. Clone it inside the
   project, record the remote URL and exact commit, inspect its license, and
   verify that it actually corresponds to the paper.
4. If no trustworthy official code exists, implement from the paper and mark
   the result as a reimplementation rather than official code.
5. Never invent missing hyperparameters, code provenance, results, or artifact
   availability. Record necessary inferences and uncertainty.

## Freeze the reproduction target

Complete `implementation/IMPLEMENTATION-SPEC.md` before substantive execution:

- the smallest central paper claim or artifact that demonstrates fidelity;
- what will be implemented or run;
- upstream commit and required assets;
- acceptance checks and comparison tolerances;
- current environment and expected commands;
- unavoidable deviations, scale reductions, or unavailable resources.

Choose a useful faithful target rather than promising every experiment in a
large paper. Minimal compatibility changes needed to run on the current machine
are allowed when recorded; elective redesign or optimization is not part of
the baseline.

## Implement and reproduce

1. Make the smallest implementation that exercises the paper's defining
   mechanism. Keep code readable and structurally aligned with the paper.
2. Reuse official code and artifacts when trustworthy; do not rewrite merely
   to appear independent.
3. Pin or record dependencies and capture environment details. Prefer a
   project-local environment when installing packages.
4. Add focused tests for shape, invariants, algorithmic behavior, data flow,
   and one end-to-end path as applicable.
5. Run the exact recorded commands. Preserve logs, raw outputs, checkpoints,
   failures, fixes, runtime, and resource use inside the project.
6. Compare observed behavior with the frozen target. Separate exact
   reproduction, close reproduction, scaled reproduction, structural
   implementation only, inconclusive, and blocked outcomes.
7. Update `UPSTREAM.md`, `VALIDATION.md`, `FINDINGS.md`, `PROGRESS.md`, and
   `WORK-LOG.md` before declaring completion.

Do not claim reproduction from code that merely imports, a passing smoke test,
an unexecuted notebook, copied upstream claims, or visual similarity alone.

## Handle constraints autonomously

Use the current environment and reasonable portable defaults first. Do not ask
the user to choose an environment before the baseline attempt.

- If full-scale reproduction exceeds available compute or data, reproduce the
  mechanism at the largest defensible local scale and state what remains
  unverified.
- If the official repository is broken, diagnose and make minimal recorded
  compatibility fixes.
- If no code exists, implement from the paper and test against derivable
  invariants or reported small examples.
- Stop early only for a genuine authority or access blocker after safe
  alternatives are exhausted.

## Offer the next phase only after reproduction

After the baseline reaches a truthful terminal state, summarize the result and
ask one concise question with relevant choices, such as:

- adapt it to the user's environment or existing codebase;
- optimize speed, memory, or usability;
- extend or ablate the method;
- compare it with another implementation;
- stop with the faithful reproduction.

Do not begin those follow-on changes until the user or calling agent chooses
one. A failed or bounded reproduction may instead offer the most useful next
diagnostic or adaptation.

## Finish

Return the project path, paper and upstream identifiers, reproduction status,
main command, strongest validation result, important deviations, installed
dependencies, and links to `IMPLEMENTATION-SPEC.md`, `UPSTREAM.md`,
`VALIDATION.md`, and the runnable code. Then offer exactly one next-phase
question unless the calling agent requested machine-only handoff.
