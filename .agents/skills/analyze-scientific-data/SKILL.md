---
name: analyze-scientific-data
description: Analyze scientific datasets against a research question and produce reproducible code or notebooks, checked tables and figures, evidence-bounded findings, uncertainty, and limitations. Use when asked to explore, clean, visualize, statistically analyze, model, compare, or interpret experimental, observational, longitudinal, survey, simulation, or measurement data. Do not use this skill merely to audit an already completed result without performing analysis; use Audit Research Result instead.
---

# Analyze Scientific Data

Answer the research question from the supplied data without outrunning the
study design. Produce an executable analysis and inspected outputs, not only a
prose interpretation.

## Establish the scientific meaning

Inspect the governing question, protocol, data dictionary, collection notes,
source files, prior processing, and repository conventions. Identify:

- the population, sampling or assignment process, experimental conditions,
  measurement timing, and intended scope;
- the observational unit, independent unit, repeated or nested structure, and
  any batch, site, subject, family, device, or time dependencies;
- outcomes, exposures or interventions, predictors, covariates, controls,
  units, coding conventions, and missing-value meanings;
- data and processing provenance, file identity or version, and whether the
  supplied data are raw, derived, filtered, or previously analyzed.

Resolve routine details from artifacts. Ask one concise question only when
missing scientific meaning would materially change the analysis, or when data
access, sensitive-data use, destructive changes, external compute, or another
action needs authority. Otherwise state the narrow assumption and proceed. Do
not infer variable meaning from a convenient column name when the distinction
could change the result, and never fabricate rows, labels, measurements, or
metadata.

## Define the analysis before chasing results

Translate the question into the target contrast, estimand, prediction target,
or descriptive quantity. Record the analysis unit, eligible observations,
outcome, predictors, adjustment variables, primary comparisons, uncertainty
method, and decision-relevant effect scale before inspecting result-bearing
comparisons when confirmation is intended.

Distinguish preregistered or genuinely prespecified tests from analyses chosen
after seeing the data. Label all post-hoc hypotheses, subgroup searches,
transformations, cutoffs, feature selection, and model changes as exploratory.
Do not present exploration as confirmation. If the data have already informed
choices, use untouched data or a defensible split for confirmation when
feasible; otherwise narrow the claim.

## Audit structure and cleaning

Profile schema, dimensions, identifiers, types, units, ranges, missingness,
duplicates, impossible values, censoring, imbalance, attrition, and collection
order. Reconcile counts across raw input, exclusions, analysis sets, groups,
and model rows.

Keep source data immutable. Make every exclusion, recode, merge, aggregation,
outlier rule, transformation, and imputation explicit in executable code and
summarize its effect on row and unit counts. Preserve unexpected observations
unless a scientifically justified rule excludes them. Never silently coerce,
drop, winsorize, impute, or select a convenient subset. Treat missingness and
failed measurements as evidence about the collection process, not merely a
software nuisance.

## Match methods to the design

Choose the simplest method that answers the question while respecting the
sampling and dependency structure. Check relevant assumptions and report when
they are weak. In particular:

- preserve randomization, pairing, blocking, stratification, clustering, and
  survey weights when the design created them;
- model or aggregate at the independent-unit level as scientifically
  justified; do not treat repeated measurements or nested observations as
  independent replicates;
- keep subject, group, site, family, time, and future information from leaking
  across training, validation, or test partitions; fit preprocessing and
  feature selection inside each training partition;
- address temporal ordering, autocorrelation, batch effects, censoring,
  compositional constraints, unequal variance, and multiplicity when they
  matter;
- separate prediction from explanation and association from intervention.
  Make causal claims only when identification assumptions and design support
  them, and state those assumptions;
- emphasize effect sizes, uncertainty intervals, practical relevance, and
  data support. Do not equate non-significance with no effect or use a p-value
  as the scientific conclusion.

Use sensitivity analyses or alternative specifications only when they probe a
credible assumption or failure mode. Correct or clearly account for multiple
comparisons; do not search analyses until one crosses a threshold.

## Build a reproducible analysis

Follow the repository's existing language and dependency conventions when
sound. Create the smallest coherent script, package entry point, or notebook
that regenerates every material table and figure from identified inputs. Use a
notebook when its narrative flow is useful, but make it restart-and-run-all
clean with no hidden state. Keep reusable transformations and calculations in
testable code rather than manually edited cells.

Record input paths and identities, parameters, random seeds, dependency and
runtime versions, and one exact execution command. Make randomness explicit.
Write derived tables in a machine-readable form as well as a readable one when
useful. Label figures with units, denominators, groups, and uncertainty; do not
hide observations or distributional structure behind a summary alone.

## Verify material results

Run the analysis from a clean state. Inspect generated artifacts rather than
trusting a successful exit. Add targeted assertions for joins, uniqueness,
group counts, split isolation, and transformations that could silently change
the conclusion. Independently spot-check consequential table values and the
data behind figures. Reconcile prose claims with code outputs.

Probe the strongest plausible alternative explanation or analysis failure:
for example pseudoreplication, leakage, one influential unit, batch or time
confounding, missingness, model misspecification, or a fragile cleaning rule.
Keep robustness checks distinct from the primary analysis. If a check fails,
fix the implementation or narrow the claim; do not conceal the failure.

## Report what the data support

Deliver:

- reproducible analysis code or notebook and its exact run command;
- checked tables and figures with clear population, units, sample counts, and
  uncertainty;
- the answer to the research question, including magnitude and direction,
  not only statistical significance;
- confirmatory and exploratory findings labeled separately, including null,
  negative, and inconclusive results;
- cleaning and exclusion decisions, design assumptions, diagnostics,
  sensitivity results, and material deviations from the intended analysis;
- limitations and the narrowest defensible interpretation, especially for
  generalization and causality;
- a compact reproducibility receipt covering data identity, environment,
  command, parameters or seeds, and generated outputs.

If data meaning, power, validity, or provenance prevents a defensible answer,
return the reproducible partial analysis and state exactly what remains
unresolved. Never invent data, certainty, causal identification, or a result.
