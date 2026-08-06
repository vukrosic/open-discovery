# Open Discovery

Open Discovery is an open project for helping researchers move from an important question to validated results faster.

> “Our strategy is not to decide which scientific problems deserve attention or try to solve them all ourselves. It is to put capable tools in the hands of the research community and let researchers pursue the questions they know best.”
>
> — [OpenAI](https://openai.com/index/chatgpt-for-academic-researchers/)

This is our main strategy too.

The long-term idea is similar to Discovery Loop: build systems that automate the repetitive experimental loop of science and engineering.

> propose an experiment → implement and run it → examine the result → learn → try the next experiment

## Goal

Help a researcher turn one uncertain question into the next trustworthy experiment, then preserve what was learned.

Open Discovery is not trying to replace scientific judgment. It should remove the repetitive work around turning a question into a controlled, reproducible test.

## First feature: Research Problem Intake

A researcher submits the question they know best. Open Discovery turns it into a precise, reviewable problem brief: the uncertainty, why it matters, current evidence, constraints, baseline, and definition of success. The researcher approves that brief before literature search, hypothesis generation, or experimentation begins.

## First goal

Use the smallest version ourselves while talking to researchers. The first version captures a question, establishes a baseline, proposes one cheap decisive experiment, records the outcome, and recommends what to do next.

We want to learn:

- which parts of research are slow, repetitive, or difficult to scale;
- how researchers currently choose ideas and experiments;
- where AI assistance is genuinely useful;
- what evidence, controls, and review are required before trusting a result;
- which small workflow would be worth building first.

## Product direction

Open Discovery may eventually help researchers:

1. define a research question;
2. find and organize relevant evidence;
3. generate testable hypotheses;
4. design reproducible experiments;
5. run experiments with available tools and compute;
6. evaluate results against explicit metrics and controls;
7. record wins, losses, confounds, and inconclusive results;
8. decide what to investigate next;
9. produce a clear, reviewable research report.

The long-term product is intentionally undecided. We will earn it by completing real loops and talking to researchers.

## Principles

- Researchers remain responsible for the question, judgment, and scientific validity.
- Every claim should have evidence, a measurable acceptance target, or an explicit uncertainty.
- Baselines, controls, seeds, data versions, and compute should be recorded.
- Negative and inconclusive results are useful outputs.
- Open protocols and reproducible artifacts matter more than impressive demos.
- Start with the smallest useful experiment and earn the right to automate more.

## Start here

- [`GOAL.md`](GOAL.md) — the product contract
- [`FIRST-CUSTOMER.md`](FIRST-CUSTOMER.md) — how we dogfood it
- [`protocol/`](protocol/) — the version-zero research loop

## Status

Version zero: a testable research protocol, ready for its first real loop.

## Background

Discovery Loop describes its mission as automating experimental loops to accelerate science and engineering, initially focusing on machine-learning research. Open Discovery explores a similar direction as an open, researcher-centered project.
