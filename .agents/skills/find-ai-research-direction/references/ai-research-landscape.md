# AI research landscape

Use this map to avoid blind spots while selecting relevant directions. Combine
areas when the interaction creates a sharper question.

## Foundations and learning theory

- optimization, generalization, scaling laws, representation and information;
- uncertainty, causality, robustness, distribution shift, and continual
  learning;
- alternatives to current objectives, architectures, and learning assumptions.

## Models and representations

- language, vision, audio, video, multimodal, world, and scientific models;
- architecture, memory, recurrence, sparsity, modularity, retrieval, and
  long-context mechanisms;
- compositional, neuro-symbolic, structured, and probabilistic approaches.

## Large language models

- tokenizer and representation choices, architecture, attention, recurrence,
  memory, mixture-of-experts, modularity, retrieval, and long context;
- data composition, quality, contamination, synthetic data, curricula,
  pretraining objectives, optimizers, scaling behavior, and compute efficiency;
- supervised fine-tuning, parameter-efficient adaptation, preference learning,
  reinforcement learning, distillation, continual learning, and model merging;
- reasoning, planning, test-time compute, search, self-correction, uncertainty,
  calibration, factuality, and knowledge updating;
- tool use, code execution, retrieval, memory, agents, multi-agent systems, and
  long-horizon reliability;
- decoding, speculative generation, caching, quantization, sparsity, routing,
  compilation, batching, serving, local inference, and hardware co-design;
- evaluation validity, benchmark saturation and contamination, robustness,
  interpretability, privacy, security, alignment, control, and misuse;
- small language models, domain models, multilingual and low-resource models,
  multimodal language systems, and model interaction with scientific tools;
- which limitations are architectural or data-bound versus likely to change
  through capability scaling, cheaper inference, or better research agents.

Prefer questions that isolate a mechanism rather than merely comparing another
model on another benchmark. Distinguish adapter-side or component-level savings
from true end-to-end gains, and test whether improvements survive different
models, seeds, workloads, context lengths, and deployment conditions.

## Data and training

- data quality, mixtures, filtering, synthetic data, curricula, and
  contamination;
- pretraining objectives, optimizers, schedules, initialization, and
  distributed training;
- small-data, low-resource, online, federated, and continual settings.

## Adaptation and post-training

- fine-tuning, parameter-efficient adaptation, distillation, preference
  learning, reinforcement learning, and test-time adaptation;
- reasoning, planning, self-correction, feedback, personalization, and skill
  acquisition;
- stability, reward hacking, forgetting, transfer, and alignment trade-offs.

## Inference and computer systems

- serving, decoding, caching, compilation, quantization, sparsity, routing,
  batching, and speculative methods;
- hardware-software co-design, local and edge inference, distributed systems,
  energy, latency, memory, and cost;
- reliable deployment, monitoring, recovery, and reproducible performance.

## Agents and autonomous systems

- tool use, search, memory, planning, delegation, multi-agent coordination, and
  long-horizon execution;
- evidence tracking, verification, recovery, resource allocation, and human
  collaboration;
- autonomous science, coding, engineering, and improvement loops.

## Evaluation, interpretability, reliability, and safety

- valid benchmarks, contamination, elicitation, calibration, uncertainty, and
  real-world evaluation;
- mechanisms, circuits, attribution, representation analysis, and causal
  interventions;
- adversarial robustness, privacy, security, control, oversight, misuse, and
  societal effects.

## Embodied and interactive intelligence

- robotics, control, simulation, spatial intelligence, interaction, and
  adaptation in physical environments;
- human-AI teams, interfaces, education, creativity, accessibility, and
  decision support.

## AI for science and high-value domains

- mathematics, biology, medicine, chemistry, materials, physics, climate, and
  engineering;
- hypothesis generation, experimental design, simulation, theorem discovery,
  mechanistic explanation, and trustworthy scientific evidence;
- domain-specific constraints, expert collaboration, and validation against
  reality rather than benchmark proxies.

## Research about AI progress itself

- capability and economic scaling, algorithmic efficiency, compute and data
  bottlenecks, evaluation forecasting, and research automation;
- which present limitations are structural versus likely to disappear with
  stronger or cheaper models;
- interfaces worth preserving now for systems that become feasible later.
