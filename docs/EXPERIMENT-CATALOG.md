# Experiment catalog

Open Discovery is first building a diverse catalog of experiments. The point
is to understand the tasks users and companies actually want to set before we
automate the full solving loop.

## What different customers experiment on

### AI and machine-learning companies

- model architectures, training recipes, data mixtures, and fine-tuning;
- evaluation, robustness, safety, and red-team suites;
- inference latency, memory, serving, and cost;
- optimizers, kernels, compilers, and reinforcement-learning settings.

### Semiconductor, compiler, and hardware companies

- chip and accelerator architecture simulations;
- compiler passes, kernels, scheduling, and memory layouts;
- throughput, latency, power, area, and thermal tradeoffs;
- design-space searches over thousands of configurations.

### Pharmaceutical, biotech, and chemistry companies

- omics and public biomedical-data analysis;
- protein or molecular structure analysis;
- virtual screening, QSAR, and property prediction;
- simulation and assay-data analysis.

These remain computational experiments. The system stops before claiming a
wet-lab, animal, or clinical result.

### Industrial R&D and simulation organizations

- automotive and aerospace design sweeps;
- robotics policies, controls, and planning;
- energy, materials, and manufacturing simulations;
- reliability, maintenance, and process optimization;
- parameter calibration against test or simulator data.

### Investment and technical-diligence teams

- reproduce a startup's public benchmark;
- test whether a claimed improvement survives a fair comparison;
- audit data, metrics, baselines, and missing evidence;
- compare technical approaches before an investment decision.

### Universities, institutes, and national laboratories

- reproduce published analyses;
- explore simulation parameters and competing models;
- analyze shared datasets;
- run ablations, robustness checks, and negative controls.

## Cross-cutting experiment families

Across these customers, the reusable experiment types are optimization,
comparison, simulation, prediction, calibration, robustness testing, failure
search, reproduction, and evidence auditing. The domain changes; the digital
experiment loop stays recognizable.

## What a user might ask

Typical requests should look like:

> Does change X improve metric Y on workload Z without breaking constraint W?

Examples:

- “Can this aircraft design meet the strength target with less material?”
- “Which compiler schedule gives the best throughput under the power limit?”
- “Does this molecule rank well in a virtual screen?”
- “Can this controller reduce energy use in the simulator?”
- “Does this public omics method separate the two cohorts?”
- “Can you reproduce the central table from this paper or company claim?”

## Shared contract

Every experiment only needs to answer the seven questions in the
[experiment contract](EXPERIMENT-CONTRACT.md). The internal design remains
domain-specific and can be as messy as the real research or engineering task.

The current phase is experiment design and collection. A later autonomous
harness will select candidates, run the protocol, diagnose failures, and search
for improvements. If code, data, or methods are missing beyond a material
gap, the harness must stop and ask the human rather than invent a result.
