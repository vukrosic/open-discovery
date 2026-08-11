# Open Discovery: Product Customers

## Product premise

Open Discovery is a general system for autonomous, fully digital
experimentation. It is not an “AI scientist” that promises to reproduce every
paper or solve every scientific problem.

The product is a capability-aware agent loop:

```text
human hypothesis or engineering question
  → plan and freeze the evaluator
  → run controlled digital experiments
  → inspect and verify outputs
  → preserve code, provenance, failures, and limitations
  → report a supported result or stop and ask the human
```

The hard boundary is part of the product. If the agent lacks usable code,
data, authority, or a sufficiently specified method, it must stop rather than
invent a result. Physical, wet-lab, clinical, field, or otherwise non-digital
steps are explicitly marked as external and are never presented as completed.

## Who pays

The buyer is an organization that already spends heavily on experiments and
loses time to slow iteration, unreliable evaluations, environment setup, or
poor evidence packaging. The user is usually a research engineer, scientist,
performance engineer, or technical lead. The economic buyer is usually the
head of research, engineering, infrastructure, or R&D.

## Customer ranking

### 1. AI and machine-learning companies — first market

Examples: OpenAI, Anthropic, Google DeepMind, Meta AI, xAI, Mistral AI, and
well-funded model or applied-AI startups.

They run repeated digital experiments involving models, data mixtures,
optimizers, fine-tuning, reinforcement learning, inference, evaluation, and
systems performance. Their bottleneck is often researcher time and experiment
coordination, not the ability to write one more script.

Initial offer:

> Define a hypothesis and evaluator; Open Discovery runs controlled overnight
> experiments and returns a verified evidence package.

Example: test whether a sparse-attention change improves a model under fixed
quality, cost, and latency gates.

Why first: short feedback cycles, measurable outcomes, naturally digital
workflows, and strong fit with the existing optimization and benchmark skills.

### 2. Semiconductor, compiler, and hardware companies

Examples: NVIDIA, AMD, Intel, Arm, Qualcomm, Broadcom, and advanced chip or
systems startups.

Experiments include kernels, compilers, scheduling, architecture simulation,
memory systems, and design-space searches. A small improvement in engineer
iteration speed or compute efficiency can have substantial value.

Initial offer: private experiment runners that optimize code or kernels against
customer-owned correctness, latency, throughput, power, or cost evaluators.

Why second: high willingness to pay and clear evaluators, but greater
integration, confidentiality, and hardware-environment requirements.

### 3. Pharmaceutical, biotech, and computational chemistry companies

Examples: Roche/Genentech, AstraZeneca, Pfizer, Moderna, Novartis, Recursion,
and computational drug-discovery startups.

Use cases include public-data analysis, omics, structure analysis, virtual
screening, QSAR, simulation, and analysis of deposited assay data.

Initial offer:

> Reproducible computational experiment infrastructure with provenance,
> validation gates, and explicit handoff when wet or clinical validation is
> required.

Do not initially sell “AI discovers drugs.” Sell reliable digital analysis and
experiment execution. This market has high value but requires stronger
validation, security, compliance, and domain integration.

### 4. Industrial R&D and simulation organizations

Examples: automotive, aerospace, robotics, energy, materials, and
manufacturing companies with simulation-heavy engineering teams.

Experiments include design optimization, simulation sweeps, control policies,
materials models, testing pipelines, and reliability analysis.

Initial offer: connect an existing simulator and evaluator to an autonomous
search-and-report loop without changing the customer’s source of truth.

Why attractive: many workflows are fully digital, but sales are more
domain-specific and integrations may be substantial.

### 5. Investment and technical diligence firms

Examples: specialist VC funds, biotech investors, deep-tech funds, and
technical diligence groups.

Use case: test whether a company’s computational claim can be reproduced from
public artifacts, identify missing evidence, and produce a bounded diligence
report.

This is a useful secondary product, not the first core market. It depends on
excellent audit quality and must never imply that a failed reproduction proves
the underlying company is fraudulent.

### 6. Research institutes, universities, and national laboratories

Examples: Allen Institute for AI, major universities, and public research
laboratories.

They are strong adoption, evaluation, and credibility partners. Purchasing is
usually slower and budgets may come from grants, so they are better early design
partners than the first revenue segment.

## Product wedge

The first commercial wedge is **autonomous experiment infrastructure**, not a
general chatbot and not a claim of autonomous scientific discovery.

The initial customer promise:

> Your researchers stop babysitting digital experiments. They state the
> question and constraints; Open Discovery runs the loop, checks the result,
> and asks for help only when a real human decision or missing capability is
> reached.

## Open-source and paid boundary

Open source should contain the trust and research core:

- workflow skills, prompts, and state model
- evaluators, evidence standards, and stop rules
- local execution and artifact formats
- reproducibility checkers and example cases
- support for user-selected agents and models

The paid product can provide the operational layer:

- managed execution and scheduling
- private runners in a customer environment
- artifact storage, search, provenance, and review history
- team permissions, budgets, approvals, and handoffs
- GitHub, data, CI, and experiment-tracker integrations
- checkpointing, retries, resource controls, and flaky-run detection
- setup and domain-integration services

## Commercial sequence

1. Prove AL-01 and AL-03 locally, then use AL-06–08 to prove honest stopping.
2. Package the resulting evidence bundle and verifier into a simple runnable
   interface.
3. Run design-partner pilots with small AI labs and systems teams.
4. Measure saved researcher time, reproducibility, intervention rate, and
   experiment throughput before choosing hosted pricing.
5. Add private execution and team workflow features only after repeated users
   identify them as the bottleneck.

## Claims we should not sell

- universal paper reproduction
- guaranteed novelty or scientific truth
- wet-lab, clinical, or field validation from digital work
- replacement of researchers
- guaranteed improvement without a valid evaluator

The defensible promise is narrower and more valuable: **faster, more
reproducible, evidence-bounded digital experimentation.**
