# AI kickoff prompt

Use this after copying `templates/project/` into a new project folder. Replace
the bracketed paths, then paste the prompt into an AI agent that can read and
edit local files.

```text
Help me initialize an Open Discovery research project.

Open Discovery harness:
[ABSOLUTE PATH TO open-discovery]

My project folder:
[ABSOLUTE PATH TO MY PROJECT]

Read these harness files first:
- AGENTS.md
- docs/EVIDENCE-STANDARD.md
- docs/STATE-MODEL.md
- docs/HUMAN-AI-COLLABORATION.md
- docs/SUPPORTED-RESEARCH.md

Then read every Markdown file already present in my project folder.

Your task is initialization only:
1. Classify the project as Supported now, Additional controls required, Not
   supported for execution, or Unknown. Stop at planning unless it is supported
   or the required external controls are confirmed.
2. Help make the research question concrete and decision-relevant.
3. Fill PROJECT.md and TASK-SPEC.md from information I have already provided.
4. Ask me only for missing information that materially changes the question,
   evidence standard, constraints, authority, or success criteria.
5. Initialize PROGRESS.md, FINDINGS.md, and WORK-LOG.md truthfully.
6. Recommend exactly one smallest decisive experiment in IDEAS.md and mark it
   Proposed.

Do not approve the idea for me. Do not create a run, perform research, contact
anyone, download large files, spend money, publish anything, or change external
state. A proposal is not approval.

When finished, summarize:
- the frozen research question;
- the support classification and any required controls;
- what evidence would count;
- the proposed first experiment;
- the decision I need to make next.
```

The prompt intentionally stops at a proposed experiment. After reviewing it,
the human records **Approved**, **Rejected**, or **Parked** in `IDEAS.md`.
