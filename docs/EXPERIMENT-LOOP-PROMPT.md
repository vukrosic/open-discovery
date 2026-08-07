# Approved experiment loop prompt

Use this only after the human has recorded an experiment idea as **Approved**
in the project's `IDEAS.md`. Replace the bracketed paths before pasting it into
an AI agent that can inspect the project and perform the authorized work.

```text
Continue this Open Discovery project through one approved experiment.

Open Discovery harness:
[ABSOLUTE PATH TO open-discovery]

Project folder:
[ABSOLUTE PATH TO PROJECT]

Read the harness AGENTS.md, docs/SUPPORTED-RESEARCH.md,
docs/EVIDENCE-STANDARD.md, docs/STATE-MODEL.md, and
docs/AUTONOMOUS-LOOP.md. Then read the complete project record and all evidence
for any active work.

Before changing state, verify:
1. Exactly one idea is explicitly Approved in IDEAS.md.
2. No conflicting experiment or review is Running.
3. The work is supported, safe, and inside PROJECT.md authority and limits.
4. The inputs, baseline, success gate, rejection gate, evidence requirements,
   costs, and stopping rule can be frozen before execution.

If any check fails, do not execute. Record the blocker in PROGRESS.md and tell
me the smallest decision or missing information needed.

If all checks pass:
1. Create the next numbered runs/EXP-###/ folder from
   templates/experiment/.
2. Complete PROTOCOL.md before execution. Copy every applicable constraint and
   authority boundary into it.
3. If completing the protocol introduces a method, cost, risk, download,
   external action, or decision not covered by the recorded approval, stop for
   human review. Do not check an approval box that is not true.
4. Mark the idea and project Running only when execution actually starts.
5. Run the smallest decisive test. Preserve raw inputs, outputs, logs,
   versions, environment details, deviations, failures, and costs.
6. Stop at the first frozen rejection or safety gate. Do not weaken a gate
   after seeing the result.
7. Complete RESULT.md with the narrowest accurate verdict.
8. Update IDEAS.md, PROGRESS.md, FINDINGS.md, and WORK-LOG.md before any new
   work begins.
9. Recommend at most one next idea based only on completed evidence and mark it
   Proposed. Do not approve or execute it.

Run exactly one experiment unless PROJECT.md explicitly grants a bounded
autonomous session. Even in that mode, obey the written iteration/time limit,
persist each completed run before continuing, and stop before any external or
scope-changing action not explicitly authorized.

When finished, report:
- experiment ID and final state;
- the frozen gate and whether it passed;
- the strongest direct evidence;
- what is established and still unknown;
- the exact next human decision.
```

Approval of an idea does not erase protocol, safety, cost, or external-action
boundaries. If the method cannot be frozen inside the existing approval, the
correct output is a reviewable protocol and a stop—not an unapproved run.
