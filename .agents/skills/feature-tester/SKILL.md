---
name: feature-tester
description: Run and robustly evaluate a feature, prompt, agent, skill, workflow, tool, code path, or user experience in a separate isolated task; simulate realistic intents and edge cases; inspect behavior and artifacts independently; report readiness honestly; and clean only proven test-owned temporary material. Use for testing, dogfooding, QA, stress testing, user simulation, or release-readiness requests.
---

# Feature Tester

Run the test in a separate background Codex task so the calling conversation
remains available. Prefer `gpt-5.6-luna` with high reasoning unless an explicit
model request or Ultra mode overrides it.

Create a unique test initiative with `BRIEF.md` and an isolated project under
its `projects/` directory. Do not copy templates. Let the tester choose the
smallest useful structure for its cases, evidence, report, and cleanup record.

In the first response, name the target and say that the tester will run
realistic isolated cases, inspect behavior and artifacts, report defects and
readiness honestly, and clean temporary artifacts afterward. Do not ask the
user to design routine cases when the target is clear.

The tester should:

- inspect the real target and its promises;
- freeze a small set of normal, ambiguous, adversarial, recovery, concurrency,
  and cleanup cases relevant to the risk;
- run the real feature in isolated state rather than merely reviewing prose;
- distinguish implemented, partially implemented, simulated, and unavailable
  behavior;
- independently verify important outputs and cleanup;
- preserve a concise evidence-backed report;
- remove only agents, downloads, caches, clones, and generated material that
  the test created and can prove it owns.

## Continuous testing

When the user asks for permanent, recurring, or always-on testing, use
`agents/CONTINUOUS-TEST-LEADER.md` to run a continuing dogfooding program.
Maintain lightweight coordination state under `lab/continuous-testing/` and
create every real test as a fresh disposable initiative under `initiatives/`.

Keep a small useful set of independent tests active. Vary user intent, field,
ambiguity, portfolio size, failure mode, resource pressure, resumption, and
authority boundaries over time. Derive the next mutation from observed defects
and uncovered risk rather than replaying an unchanged suite forever.

An implementation task must never grade itself. After test initiatives finish,
use a separate evaluator to inspect their artifacts, compare observed behavior
with the current harness promises, preserve concise durable findings, and only
then authorize cleanup of exact test-owned disposable material. Harness changes
remain a separate development action: test agents report defects and proposed
repairs but do not silently edit the feature they are evaluating.

Never delete source, user data, shared caches, live-service state, or ambiguous
paths. Invocation authorizes zero-cost local testing, disposable public
downloads, fresh test agents, and cleanup of exact test-owned artifacts. It does
not authorize spending, private access, publication, external messages, live
account changes, or destructive testing against user data.
