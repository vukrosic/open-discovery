# Supported research in version 0.1

Open Discovery is a Markdown workflow, not a laboratory, ethics board, safety
system, secure data environment, or regulatory compliance product.

Support depends more on the **research activity and risk** than on the name of
the discipline. A biologist analyzing a public dataset may be supported now;
the same biologist culturing a pathogen is not.

## What “supported” means

**Supported now** means the researcher can use the complete question → idea →
approval → protocol → result loop using ordinary files, while the work remains
low-risk, reviewable, and inside explicit human authority.

It does not mean that Open Discovery certifies the method, result, researcher,
or compliance with a field's standards.

## Supported now

| Scientist or research mode | Examples of suitable work | Current boundary |
| --- | --- | --- |
| Software, systems, and ML researchers | Local benchmarks, ablations, profiling, algorithm comparisons, prompt experiments | Preserve code, versions, seeds, raw trials, quality checks, and compute limits outside or alongside the Markdown record. |
| Data scientists and statisticians | Analysis of public, synthetic, or properly de-identified datasets; estimator comparisons; sensitivity checks | The researcher must verify data rights, provenance, leakage, assumptions, and statistical validity. |
| Mathematicians and theoretical researchers | Proof attempts, counterexamples, derivations, model comparisons, assumption audits | AI-generated reasoning is a proposal until checked; a plausible argument is not a verified proof. |
| Computational natural scientists | Simulation, archived astronomy data, climate-data analysis, computational chemistry on safe existing data, bioinformatics on approved non-sensitive data | Open Discovery records the loop but does not supply compute, licensed datasets, or domain validation. |
| Low-risk engineering researchers | Simulation, design comparisons, software-defined prototypes, non-hazardous benchtop measurements | Physical tests remain human-run and require appropriate equipment and safety review. |
| Historians, linguists, and humanities scholars | Archive questions, source comparison, textual analysis, interpretive coding, provenance and counterevidence tracking | Record source selection, access limits, researcher position, and competing interpretations. |
| Literature and evidence researchers | Small scoping searches, evidence maps, claim audits, source comparison | Preserve exact queries and inclusion decisions; this is not yet a full systematic-review or citation-management system. |
| Quantitative social scientists using existing data | Analysis of public, licensed, synthetic, or approved de-identified datasets | No participant contact, re-identification, or unapproved sensitive-data processing. |
| Low-risk independent and citizen scientists | Safe, reversible observations or measurements with no people, animals, hazards, restricted sites, or sensitive locations | The researcher is responsible for local laws, permits, equipment, and field safety. |

## Usable only with additional controls

For these researchers, Open Discovery may organize plans and records, but the
harness is not sufficient by itself. Work may proceed only inside the relevant
institutional, ethical, safety, legal, and technical systems.

| Scientist or research mode | Additional controls required |
| --- | --- |
| Wet-lab biologists, chemists, and materials scientists | Laboratory supervision, risk assessment, approved protocols, training, waste handling, inventory, and instrument records. |
| Experimental physicists, roboticists, and hardware engineers | Independent equipment safety, interlocks, calibrated instrumentation, operating procedures, and qualified human supervision. |
| Ecologists, geologists, and field scientists | Permits, site access, field safety, conservation rules, weather planning, and protection of sensitive locations. |
| Psychologists, sociologists, education researchers, and anthropologists | Ethics or IRB review where applicable, consent, recruitment controls, privacy protections, and approved data handling. |
| Biomedical and health researchers using non-clinical data | Approved data access, privacy controls, clinical or statistical oversight, and a prohibition on using the output for individual care decisions. |
| Researchers using confidential, culturally sensitive, export-controlled, or proprietary material | An approved secure environment, access controls, data-governance review, and field-specific handling rules. |
| Researchers conducting publication-grade systematic reviews or meta-analyses | Registered protocol where appropriate, database-specific searches, deduplication, dual screening, bias assessment, citation management, and reporting standards. |
| Researchers running expensive or large-compute experiments | Explicit budgets, infrastructure controls, monitoring, reproducible environments, and approval before spending or launching jobs. |

In these cases, Open Discovery can be a supplementary research record. It must
not replace the required system of record.

## Not supported for execution in version 0.1

Do not use this harness to authorize or autonomously execute:

- diagnosis, treatment, triage, dosing, or individual patient-care decisions;
- clinical trials or medical interventions;
- recruitment, consent, deception, intervention, or surveillance of human
  participants without the required independent approval;
- animal procedures or experiments;
- pathogen work, high-risk genetic modification, uncontrolled biological
  culture, or other biohazardous procedures;
- work involving explosives, weapons, toxic releases, dangerous chemicals,
  high voltage, ionizing radiation, or other serious physical hazards;
- autonomous laboratory robots, machinery, vehicles, or physical actuators
  where an error could injure people, animals, property, or the environment;
- collection, exposure, re-identification, or movement of personal, medical,
  confidential, or restricted data outside an approved secure system;
- actions requiring a permit, professional license, ethics approval, safety
  approval, or legal authorization that has not already been obtained;
- autonomous spending, publication, participant contact, account changes, or
  destructive external actions unless separately and explicitly authorized;
- claims that a result is peer reviewed, independently reproduced, ethics
  approved, regulatory compliant, or publication ready when it is not.

The Markdown files may document that such work exists or record a decision to
stop and seek qualified review. They do not make the work safe or authorized.

## Capabilities version 0.1 does not provide

Open Discovery currently provides no:

- laboratory information management system or certified electronic lab
  notebook;
- secure storage, encryption, permissions, audit service, or data-retention
  enforcement;
- instrument, robot, sensor, or laboratory automation integration;
- automatic literature database search, citation manager, or deduplication;
- compute scheduler, cloud budget control, or experiment monitor;
- statistical, methodological, ethics, safety, legal, or regulatory approval;
- automatic independent replication or peer review.

## Quick eligibility test

A project is suitable for version 0.1 only when every answer below is **yes**:

1. Can a failed run end safely without harming a person, animal, property, or
   the environment?
2. Can the researcher legally and ethically access every input?
3. Can the evidence be preserved without exposing restricted information?
4. Can a qualified human review consequential decisions before execution?
5. Are costs, compute, time, and external actions explicitly bounded?
6. Does another required institutional system remain the source of truth where
   applicable?

If any answer is **no** or **unknown**, stop at planning and obtain the missing
review, approval, or infrastructure.
