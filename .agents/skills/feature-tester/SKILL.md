---
name: feature-tester
description: Run and robustly evaluate a feature, feature idea, prompt, agent, skill, workflow, tool, code path, or user experience using realistic isolated scenarios; inspect behavior and artifacts independently; return or preserve a concise evidence-backed report; and safely remove temporary agents, clones, downloads, caches, and generated test garbage. Use when a human or agent asks to test, dogfood, evaluate, validate, stress-test, simulate users for, QA, or determine release readiness of a feature or idea.
---

# Feature Tester

Test the feature as a real user or calling agent would encounter it. Run the
test in a separate background task so development and the calling conversation
remain available. Preserve a small report; remove disposable test material.

## Execution model

Do not run the feature test inline in the calling development or research
conversation. The caller or Lab CEO launches one dedicated native Codex task
for the complete test using `gpt-5.6-luna` with `xhigh` reasoning by default.
If that model is unavailable, use the strongest suitable available agent and
record the substitution. The dedicated tester may launch additional fresh test
agents only when isolated conversations or useful parallel comparison require
them.

The calling conversation returns immediately after dispatch and remains free
for development, experiments, and other work. The Lab CEO, when present,
records the tester task ID, target, project path, resource use, and status;
checks material progress without micromanaging; receives the final report; and
confirms that test-owned processes and artifacts were cleaned up. A standalone
caller performs the same lightweight supervision when no Lab CEO exists.

## Start

In the first response, name the feature being tested and say that the tester
will run realistic isolated cases, inspect the results, report defects and
readiness honestly, and clean temporary artifacts afterward. Do not ask the
user to design the test plan when the target and intended outcome are clear.

The invocation authorizes zero-cost local test execution, temporary public
downloads needed by the feature, disposable test data, fresh native test agents,
and deletion of artifacts created and registered by this test. It does not
authorize spending, publication, external messages, private access, changes to
live accounts, destructive testing against user data, or deletion of anything
whose ownership is uncertain.

## Establish the target

Inspect the feature's actual prompt, code, skill, workflow, documentation, and
current state. Record:

- what the feature promises and who calls it;
- its normal entry points and important boundaries;
- what must be observed to call it useful or ready;
- risks that deserve negative, recovery, concurrency, or cleanup testing;
- whether the target is executable, partially implemented, or only an idea.

For an idea, test its assumptions and, when useful and authorized, a disposable
minimal prototype. Never report a simulated or specification-only test as a
working implementation.

## Create isolated test state

Create a unique ignored project under `projects/<feature-slug>-feature-test/`
and copy both `templates/project/` and `templates/feature-test/` into it. This
folder preserves the project record, test spec, small supporting evidence,
cleanup receipt, and final report.

Create disposable execution state with `scripts/test_sandbox.py create`. Keep
temporary clones, downloads, generated projects, caches, logs, and fixtures
inside that returned sandbox whenever practical. Record any test-created path
outside it in `ARTIFACTS.md` immediately, with its owner and cleanup rule.

Never use Git worktrees. Never let test agents mutate the released harness or
the user's source unless the request explicitly includes fixing the feature.
For mutation tests, use a disposable copy or feature-provided test environment.

## Select useful cases

Freeze `TEST-SPEC.md` before launching cases. Choose the smallest set that can
expose meaningful defects; do not apply a fixed checklist mechanically.
Consider:

- normal explicit and natural-language entry;
- missing, broad, malformed, or conflicting input;
- a nearby request that should not activate the feature;
- interrupted execution, resume, repeated invocation, or tool failure;
- authority, cost, privacy, destructive-action, concurrency, and cleanup edges;
- artifact correctness and truthful final reporting.

Use natural prompts and do not leak expected behavior to test workers. Define
observable acceptance checks before seeing results.

## Run independent tests

When additional native test agents are useful, launch them using
`gpt-5.6-luna` with `xhigh` reasoning by default. Use separate agents only where
clean conversation state or genuine parallel comparison matters; do not create
an arbitrary swarm. Give each agent its own sandbox subdirectory and no
writable access to another case's state. Use
`references/test-worker-prompt.md` as the base assignment.

When fresh agents are unavailable, run cases sequentially with explicit state
reset and mark conversation-isolation coverage accurately.

For every case, preserve enough raw evidence to verify:

- exact input, environment, model, and start state;
- activation and first response;
- actions, interruptions, side effects, and final response;
- promised versus actual artifacts;
- validation commands and observed outputs;
- remaining files, processes, downloads, and caches.

Do not pass a case from the tested agent's self-report alone. Inspect outputs,
filesystem state, processes, and external state independently as applicable.

## Classify and report

Use plain statuses: Passed, Failed, Blocked, or Untested. Explain impact rather
than relying on a complicated score. Distinguish unsafe or corrupting defects,
core workflow failures, misleading behavior, and minor usability issues.

If the request includes fixing, change only confirmed defects, then rerun the
failed case plus a relevant happy path and negative control. Otherwise report
the defect to the calling human or agent without modifying the feature.

Complete `REPORT.md` with:

- what was tested and what was not;
- the most important observed behavior;
- defects and evidence;
- readiness: Ready, Ready with limitations, Not ready, or Blocked;
- the smallest useful next action.

## Clean up

Stop or finish every test agent and process before cleanup. Preserve the report,
test specification, compact evidence needed to support conclusions, and the
cleanup receipt in the ignored feature-test project.

Then:

1. Compare `ARTIFACTS.md` with actual created paths and active processes.
2. Keep only evidence explicitly referenced by `REPORT.md`.
3. Remove exact test-owned paths. Use `scripts/test_sandbox.py cleanup --path`
   for its marked sandbox.
4. Remove test-created dependencies, caches, downloads, generated projects, and
   disposable copies only when ownership is proven and no process uses them.
5. Never delete source files, pre-existing artifacts, shared caches, credentials,
   user data, or ambiguous paths.
6. Record what was removed, what was deliberately preserved, and any cleanup
   failure in `CLEANUP.md`.

If safe cleanup cannot be proven, preserve the uncertain item and report its
exact path instead of guessing.

## Finish

Return a short readiness verdict, the strongest evidence, the most important
defect or limitation, the report path when one was created, and cleanup status.
When called by another agent, provide the same concise machine-usable handoff.
