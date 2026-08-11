---
name: build-skill
description: Turn a rough capability, workflow, repeated task, prompt, or product idea into a concise, discoverable, and tested agent skill inside Open Discovery or another repository. Use when the user asks to create, design, scaffold, improve, package, or validate a skill for Codex, Claude Code, or another skill-compatible coding agent.
---

# Build a Skill

Turn the user's desired outcome into the smallest skill that reliably helps an
agent produce it. Keep the design flexible where judgment matters and add
deterministic machinery only where mistakes are costly or repetition justifies
it.

## Understand the job

Inspect the repository rules, nearby skills, and relevant tooling before
editing. Infer routine details from the request and local conventions. Do not
make the user design file structure, metadata, tests, or agent instructions.
Ask one concise question only when an unresolved choice would materially change
the capability, audience, or installation location and cannot be handled with a
safe reversible default.

Privately establish:

- what users will ask for and what useful outcome they expect;
- what should trigger the skill and what adjacent skill should handle instead;
- which decisions require agent judgment and which operations need reliable
  scripts or fixed checks;
- what authority the invocation grants and what still requires approval.

Use concrete example requests to clarify behavior when useful, but do not force
a questionnaire or permanent specification document.

Before building from scratch, search nearby catalogs and relevant public skill
repositories when current external research is appropriate. If a close skill
already exists, prefer testing, adapting, or improving it. Copy or derive files
only when the source license permits it; preserve required attribution and
license notices and record the source URL and pinned revision. Treat unlicensed,
proprietary, or unclear material only as public-behavior inspiration.
Treat copied scripts as untrusted dependencies: inspect their network, secret,
filesystem, subprocess, and destructive behavior before running them.

## Design the smallest useful skill

Choose a short verb-led lowercase hyphenated name. Honor an explicit location.
Otherwise, place a new or experimental repository-owned skill under
`skill-lab/<skill-name>/`. This keeps unfinished ideas available for explicit
use and testing without adding their metadata to every Codex session.

Treat `.agents/skills/` as the installed, automatically discovered catalog.
Use it directly only when updating an existing installed skill or when the user
explicitly asks to install, promote, or release a validated prototype.

Create only what the capability needs:

```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml       # when supported
├── scripts/                 # only for repeatable deterministic operations
├── references/              # only for detailed material loaded on demand
└── assets/                  # only for files reused in outputs
```

Keep `SKILL.md` concise. Put only `name` and `description` in its YAML
frontmatter. Make the description explain both the capability and its trigger
contexts because discovery depends on it. Write the body as instructions for
the future agent, not as maintainer commentary.

Do not create a skill-specific README, changelog, installation guide, blank
templates, or speculative helpers. Prefer instructions with high freedom for
judgment-heavy work, bounded choices for repeatable workflows, and scripts only
for fragile operations that benefit from deterministic execution.

Use an available skill scaffolder and metadata generator when they fit the
environment. Otherwise create the standard files directly while following the
local repository's conventions. Never depend on one vendor-specific helper
when the resulting skill is intended to work across coding agents.

## Build and integrate

Reuse nearby conventions without copying redundant policy into the new skill.
Keep durable authority, safety, and repository rules in their canonical parent
documents; include only consequences specific to this capability.

Keep prototypes in `skill-lab/` unlisted in public catalogs and onboarding by
default. They may still be invoked explicitly by path, used in delegated tasks,
and iterated with realistic evaluations.

Promote a prototype only after its behavior has been inspected on realistic
inputs and the user explicitly asks to install, expose, or release it. Promotion
means moving the finished skill into `.agents/skills/`, validating it there,
and adding one concise entry to the repository's existing workflow catalog or
onboarding surface. Link to the skill instead of repeating its instructions.
Use judgment about evidence quality rather than imposing a universal score or
fixed test count.

For adapted public skills, verify that attribution, notices, and source-version
receipts remain present at promotion time. Do not imply Open Discovery authored
third-party work.

Do not install the skill globally, publish it, create a remote repository,
commit, or push unless the user explicitly authorizes that action.

## Validate behavior

Run the strongest suitable structural validator available and inspect every
created file. Check at minimum that:

- metadata parses and the folder name matches the skill name;
- no scaffold placeholders remain;
- the description will trigger on realistic requests without swallowing
  unrelated work;
- references and metadata paths resolve;
- the instructions can reach the promised output within their authority.

For behaviorally complex skills, forward-test one or more realistic requests in
clean state. Prefer a separate test task when delegation is authorized; do not
launch one merely because this skill was invoked. Give the tester the raw skill
and natural request rather than the intended answer. Inspect actual outputs,
record material failures, improve the skill, and remove only proven test-owned
temporary artifacts.

Choose test depth from risk and complexity rather than a fixed suite. A simple
formatting skill may need only validation and one dry run; a long-running,
destructive, external, or high-stakes workflow needs stronger isolation and
independent evaluation.

## Finish

Report the skill name, what it enables, where it lives, whether it is a lab
prototype or an installed skill, what was validated, and any honest limitation.
Keep implementation detail brief unless the user asks.
