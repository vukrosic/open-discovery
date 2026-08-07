# Release checklist

Use this checklist before releasing a version of the Markdown harness.

## Content

- [ ] `README.md` explains what is usable now and what is not.
- [ ] `AGENTS.md` states the AI operating and stopping rules.
- [ ] Project and experiment templates are complete.
- [ ] State boundaries are explicit.
- [ ] Evidence and negative-result rules are present.
- [ ] Human authority and external-action limits are explicit.

## Separation

- [ ] No project-specific experiments are included.
- [ ] No model files, datasets, benchmark outputs, secrets, or private prompts
      are included.
- [ ] General docs contain no project conclusions.
- [ ] Example content is synthetic or clearly generic.

## Review

- [ ] Every internal Markdown link resolves.
- [ ] The repository contains only the intended file types.
- [ ] Templates do not claim that an unrun action has happened.
- [ ] The release date and version are recorded in `CHANGELOG.md`.
- [ ] A fresh researcher can complete the minimum viable loop from the README.

## Publication boundary

- [ ] A human reviewed the final file list.
- [ ] The repository is committed locally.
- [ ] Any remote push or public announcement has separate explicit approval.
