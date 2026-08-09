# State model

Open Discovery uses flexible durable state rather than a mandatory document
schema.

## Fixed state

Each initiative has one fixed human-facing file:

```text
initiatives/<slug>/BRIEF.md
```

The brief preserves the original request, expected outcome, constraints,
resources, and forbidden actions. Agents may clarify or annotate it but must
not silently replace the human's intent.

Each initiative also contains `projects/`. Every active project has one owner
and one unique folder. Everything inside that folder is chosen by its explorer.

## Semantic states

Agents should distinguish these meanings even when they choose different file
formats or labels:

- proposed: not yet selected for work;
- active: currently owned and being pursued;
- paused: intentionally stopped with a possible resume condition;
- completed: its stated question or outcome was resolved;
- inconclusive: work ended without resolving it;
- rejected: evidence does not justify pursuing it;
- blocked: no useful action remains inside current authority or resources.

Do not infer one state from another. A folder is not an active project, an
agent message is not a result, and a completed run is not necessarily a
completed project.

## Minimum durable information

The chosen project structure must make it possible to recover:

- what question or outcome was pursued;
- who owns active work;
- what evidence was observed;
- how important results were produced;
- what failed or changed;
- what the conclusion does and does not support;
- what should happen next.

This information may live in Markdown, code, logs, databases, notebooks, or
other inspectable artifacts. No universal filenames are required.
