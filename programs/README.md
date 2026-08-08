# Hierarchy of Agents Research Model programs

`programs/` holds lightweight coordination state for research-direction
leaders. It is not where experiments run.

The hierarchy is:

1. The Lab CEO coordinates the whole portfolio.
2. One direction leader maintains `programs/<direction-slug>/` and compares
   the evidence from its explorers.
3. Independent explorer agents each own a distinct
   `projects/<project-slug>/` research project. Prefer Luna with high reasoning
   when available, with practical fallback to another capable agent.

Explorer projects are siblings, not nested inside the program folder. This
keeps ownership, evidence, and lifecycle independent. No two active agents may
write to the same project folder.

Copy `templates/program/` when a durable direction record is useful. Keep it
small: active approaches, agent ownership, real resource conflicts, evidence
comparison, and the next direction. Directions in the Hierarchy of Agents
Research Model start with three active background explorers and may adjust the
pool when useful. When one finishes, the leader preserves its result and starts
the next project when continued exploration is warranted. There is no scoring
system, meeting cadence, or routine human approval requirement.
