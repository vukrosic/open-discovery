---
name: curate-research-dataset
description: Turn raw, inherited, or partially processed data plus an intended research use into a trustworthy, reproducible dataset package with source provenance, rights and privacy constraints, semantic schema and units, quality evidence, auditable transformations, deduplication, leakage-resistant splits, integrity manifests, and a data card. Use when asked to collect, consolidate, clean, label, de-identify, version, split, document, audit, or prepare data for scientific analysis, benchmarking, model training, evaluation, or release; do not use merely to analyze a finished dataset against a research question.
---

# Curate Research Dataset

Produce the smallest dataset package that supports the intended research use
without obscuring where the data came from, what changed, or what remains
unknown. Adapt files, checks, and documentation to the domain rather than
forcing a universal schema.

## Establish the use and authority

Inspect the governing request, repository rules, source files, collection
notes, prior transformations, and any protocol or data-management plan. Define:

- the research decision, analysis, training, or evaluation the data must support;
- the population or system represented, observational unit, independent unit,
  sampling or collection process, time coverage, and expected exclusions;
- the fields, labels, measurements, units, resolution, and metadata needed for
  that use;
- the authorized local actions and intended access or distribution audience.

Resolve routine implementation choices from evidence. Ask one concise question
only when missing scientific meaning or authority would materially change the
package and no conservative partial result is useful. Unknown rights, consent,
privacy status, label meaning, or provenance are unresolved facts, not
permission to infer or distribute. Never upload, publish, or reveal private data
without explicit authority.

## Preserve sources and provenance

Treat source data as immutable. Work in a separate derived location and retain
the original bytes when lawful and practical. When source data cannot be copied,
record a stable identifier and lawful retrieval or access procedure without
embedding credentials or sensitive locations in a public artifact.

For each materially distinct source, capture what evidence supports:

- creator or custodian, origin, collection method, acquisition date, version,
  and exact file or object identity;
- license or terms, consent and ethics constraints, privacy classification,
  permitted uses, redistribution limits, and required attribution;
- known filtering, annotation, conversion, sampling, or prior processing;
- gaps, conflicts, and claims that could not be verified.

Keep confirmed facts separate from interpretations and unknowns. Preserve
source-specific restrictions through merges; combining sources never creates
broader rights than their inputs.

## Define semantic contracts

Describe the schema at the level required to prevent scientific mistakes. State
what one record represents, identifier scope, relationships among tables or
objects, label origin, measurement method, units, coordinate or timezone
conventions, categorical meanings, missing-value semantics, censoring, and
known valid ranges. Do not infer consequential meaning from names or values
alone.

Choose storage formats and normalization from scale, fidelity, portability,
access controls, and downstream use. Preserve precision and raw representations
when conversion could change meaning. Version incompatible schema or semantic
changes instead of silently overwriting them.

## Profile before changing

Create reproducible checks suited to the data. Examine dimensions, types,
missingness, uniqueness, exact and near duplicates, ranges, impossible values,
class or subgroup coverage, temporal order, batch or site effects, annotation
agreement, corrupt files, and cross-file consistency where relevant. Reconcile
counts from source through every derived stage.

Distinguish a suspicious observation from a proven error. Preserve unexpected
data unless evidence or a frozen rule justifies correction or exclusion. For
images, text, audio, signals, graphs, spatial data, or domain formats, add
format-aware integrity and semantic checks rather than reducing quality to a
tabular checklist.

## Build an auditable transformation

Implement a deterministic raw-to-derived pipeline using the repository's
existing language and dependency conventions when sound. Make every filter,
join, recode, normalization, unit conversion, annotation, imputation,
aggregation, and redaction explicit. Record parameters, tool and dependency
versions, random seeds, and before/after counts. Never silently repair labels,
invent measurements, or fill unknown provenance.

Prefer reversible mappings and stable identifiers. Keep sensitive linkage keys
separate and access-controlled. Test joins, cardinality, uniqueness, units, and
row or object retention at the point where failures could enter. Fit learned
preprocessing only on the training portion and serialize the fitted state.

## Deduplicate and split for the intended claim

Define the independent unit and credible leakage paths before finalizing splits.
Deduplicate or link related observations before assigning partitions. Keep the
same person, subject, source document, device, site, family, event, time future,
or transformed derivative together whenever separation would leak information.
Use temporal, grouped, geographic, stratified, or other domain-aware assignment
as the intended generalization claim requires.

Freeze split logic and randomness before result-driven tuning. Preserve explicit
split assignments and verify isolation using stable IDs plus content or
similarity checks appropriate to the modality. Keep protected confirmation data
separate from exploratory feedback; if it was viewed or repeatedly tuned on,
record the exposure and stop calling it held out.

Use `scripts/audit_dataset.py splits` for delimited tables when exact record,
group, or selected-content overlap is a useful check. Supply only columns whose
scientific meaning is established. The tool hashes reported values by default
so diagnostics do not echo identifiers; do not enable raw-value output without
authority to expose those values in the current environment. For other formats
or near-duplicate risks, implement an equivalent domain-specific check.

## Assemble and verify the package

Choose a layout that fits the repository and access constraints. Include or
point to, as applicable:

- immutable source snapshots or retrieval receipts and their identities;
- executable transformation code, configuration, and one exact run command;
- derived data and explicit split assignments;
- schema and semantic documentation, quality checks, exclusions, and count flow;
- a cryptographic inventory of package files;
- a data card describing purpose, composition, provenance, collection and
  processing, rights and access, privacy and consent, quality evidence, splits,
  known biases, limitations, prohibited or unsupported uses, and maintenance.

Generate and verify a portable file inventory with:

```bash
python3 <skill-dir>/scripts/audit_dataset.py manifest create <package-root> --output <manifest.json>
python3 <skill-dir>/scripts/audit_dataset.py manifest verify <package-root> <manifest.json>
```

Run the pipeline from identified inputs in clean state when practical. Inspect
the actual outputs, manually sample consequential transformations, and exercise
at least one failure path for a fragile check. Confirm that manifests match,
split leakage checks pass, documentation agrees with data, and private or
restricted material is absent from any wider-access surface.

Report what is ready for which use and audience, what remains restricted or
unresolved, exact validation performed, known quality or representativeness
limits, and how to reproduce the package. A reproducible package with unresolved
rights, privacy, label validity, or leakage is not release-ready; preserve the
work and state the blocker precisely.
