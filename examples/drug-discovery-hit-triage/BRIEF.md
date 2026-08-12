# Public-assay hit-triage experiment

## 1. What question is being asked?

Given historical EGFR activity measurements and a limited follow-up assay
budget, can a ligand-similarity ranking enrich active compounds in the top-K
virtual-screening shortlist over a prevalence-only baseline?

## 2. What inputs and permissions exist?

The experiment reads a pinned ChEMBL REST query for human EGFR (`CHEMBL203`),
standard IC50 measurements in nM, canonical SMILES, and document years. It has
local compute and read-only internet access to retrieve the public snapshot. No
wet-lab, animal, clinical, proprietary, or patient data are available.

## 3. What can be changed?

The candidate may change the computational ranking method. The target, assay
type, activity threshold, temporal holdout, top-K budget, and evaluation code
remain fixed for a comparison. The baseline ranks by the training active rate;
the candidate ranks compounds by similarity to the most similar known active
training molecule using transparent SMILES fingerprints.

## 4. How is success measured?

The primary measure is enrichment factor at the top-K shortlist on the temporal
holdout. Secondary measures are recall@K, precision@K, ROC AUC, and the number
of compounds retrieved. A candidate succeeds only when its primary enrichment
is higher than the baseline and the snapshot and split checks pass.

## 5. What evidence was produced?

The run preserves the downloaded activity snapshot, split summary, per-method
rankings and metrics, a JSON run receipt, and SVG plots of enrichment and score
distributions. The receipt records the exact query URL, snapshot hash, code
revision information available locally, and parameters.

## 6. What is missing or uncertain?

ChEMBL measurements combine heterogeneous assays and are not a prospective
clinical endpoint. SMILES fingerprints are a lightweight demonstration rather
than a validated medicinal-chemistry representation. A temporal holdout does
not prove performance on a future campaign or a different target.

## 7. When must the agent stop and ask a human?

Stop if the public data cannot be retrieved or interpreted, the assay endpoint
or target identity is ambiguous, the split leaks compounds across time, or the
requested claim requires wet-lab, animal, clinical, or proprietary validation.
Never call a computationally prioritized compound a confirmed hit or drug.
