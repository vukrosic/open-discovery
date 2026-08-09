# Publishing a research repository on GitHub

This is operational guidance for Open Discovery agents.

Open Discovery creates one canonical repository artifact for an initiative,
not one repository for every small project. Publish it only after the evidence
or engineering work is mature enough to help another person.

This is guidance, not a rigid template. Adapt the files to the research.

## Make the first screen simple

The beginning of `README.md` should let a new reader understand the work in
under a minute. Use plain language and answer these questions in order:

1. What did we test or build?
2. What happened?
3. Why does it matter?

Lead with the strongest reproducible result that worked and the usefulness it
creates. Do not turn the README into a diary of abandoned ideas or failed
exploratory runs. Do not begin with an abstract, internal agent language,
protocol terminology, or a large table. Explain unavoidable technical terms
in one sentence.

Keep the README short. Move exact statistics, methods, provenance, and lengthy
setup instructions into focused files such as `RESULTS.md`, `PROTOCOL.md`,
`PROVENANCE.md`, or `REPRODUCE.md`. Link to them from the README.

## Package what another person needs

A useful research repository usually includes:

- concise code and setup instructions;
- the strongest supported result and its limits;
- enough raw or representative evidence to check the claim;
- model, dataset, dependency, prompt, and source provenance;
- material limitations, uncertainties, and useful next questions;
- continuation guidance for a human or AI agent.

Do not copy model weights, private data, credentials, local caches, session
logs, generated junk, or machine-specific absolute paths. Do not invent a
license. State clearly when no license has been selected.

## Validate before publishing

Before creating or updating a GitHub repository:

- inspect the source evidence instead of trusting chat claims;
- run the documented tests and analysis from the canonical package;
- scan for secrets, local paths, caches, and oversized files;
- confirm that every headline number matches the preserved evidence;
- ensure the README links and commands work;
- keep publication separate from local packaging unless the human explicitly
  authorizes the external action.

After publishing, make a fresh clone from GitHub and run the lightweight checks
again. Confirm the repository visibility, default branch, commit, file list,
and public URL. Then record the URL and commit in the initiative state and
remove temporary publishing or test copies.

## Focus the public artifact without weakening the claim

Keep routine failed experiments and abandoned branches in the initiative's
internal evidence rather than foregrounding them on GitHub. If a failed or
inconclusive result materially limits the working result, disclose that limit
where readers need it to interpret the claim. Never hide contradictory
evidence or make the public claim stronger than the evidence supports.

A short note about alternative or failed approaches is useful when it explains
why the working method was chosen or helps readers avoid a specific dead end.
Keep that note concise and subordinate to the useful result; do not turn the
README into a chronological experiment log.
