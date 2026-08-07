# Changelog

## 0.2.0 — 2026-08-07

- Focused the product on literature-review and experiment automation.
- Added a shared research-memory contract connecting both loops.
- Added an approved-experiment execution prompt.
- Added literature-review guidance, an agent prompt, and reusable review
  templates.
- Removed repository-level research eligibility categories so each project can
  define its own methods and constraints.
- Added a Git-ignored `projects/<project-slug>/` workspace so the public clone
  can be dogfooded without mixing research artifacts into releases.
- Required every new or parallel research request to use a unique project
  folder and prevented the repository root from becoming a live project.
- Added an attach-without-moving workflow for existing local folders and remote
  repositories.
- Added shared research tools and dedicated operating modes for AI/ML,
  mathematics, and biology.
- Named the user-facing Open Discovery research partner Starberry.
- Tested independent AI/ML, mathematics, biology, external-project, duplicate,
  and Full Auto routing scenarios before release.

## 0.1.0 — 2026-08-07

- Released a Markdown-only research collaboration contract.
- Added project, task, idea, progress, findings, and work-log templates.
- Added frozen experiment protocol and result templates.
- Added human–AI authority, state-separation, evidence, and bounded-loop docs.
- Added an agent operating contract and a next-idea recommendation prompt.
- Added a copy-paste AI kickoff prompt and a complete synthetic worked example.
- Added explicit project scope and authority recording.
- Kept project-specific research and artifacts outside the public Git history.
