# AI kickoff prompt

Use this to initialize a named project manually. The agent creates the folder
under `open-discovery/projects/`, copies `templates/project/`, and fills the
files. For normal use, simply open the repository and state your question.

```text
Help me initialize an Open Discovery research project.

Open Discovery harness:
[ABSOLUTE PATH TO open-discovery]

My project folder:
[ABSOLUTE PATH TO open-discovery/projects/PROJECT-SLUG]

Read these harness files first:
- AGENTS.md
- docs/EVIDENCE-STANDARD.md
- docs/STATE-MODEL.md
- docs/HUMAN-AI-COLLABORATION.md

Create a unique project folder if it does not exist, copy every file from
templates/project/ into it, then read every Markdown file in that folder.

Your task is initialization only:
1. Help make the research question concrete and decision-relevant.
2. Fill PROJECT.md and TASK-SPEC.md from information I have already provided.
3. Ask me only for missing information that materially changes the question,
   evidence standard, constraints, authority, or success criteria.
4. Initialize PROGRESS.md, FINDINGS.md, and WORK-LOG.md truthfully.
5. Recommend exactly one smallest decisive experiment in IDEAS.md and mark it
   Proposed.

Do not approve the idea for me. Do not create a run, perform research, contact
anyone, download large files, spend money, publish anything, or change external
state. A proposal is not approval.

When finished, summarize:
- the frozen research question;
- what evidence would count;
- the proposed first experiment;
- the decision I need to make next.
```

The prompt intentionally stops at a proposed experiment. After reviewing it,
the human records **Approved**, **Rejected**, or **Parked** in `IDEAS.md`.
