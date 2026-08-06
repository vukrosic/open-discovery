# Becoming Our Own First Customer

We do not need to already be a laboratory. We become the first customer by putting one real, uncertain research question through the complete Open Discovery loop.

## First dogfood question

**Can a structured Open Discovery brief produce a more useful next experiment than giving an AI agent the same research question as a plain prompt?**

This is a real research question about the product itself. It is cheap, measurable, and immediately improves what we are building.

## Experiment

Choose three small computational research problems with existing code and a measurable outcome.

For each problem:

1. Give one agent only the raw research question.
2. Give another agent the same question plus the Open Discovery research brief.
3. Ask both for the single best next experiment.
4. Hide which method produced each proposal.
5. Have a researcher score both proposals.

## Score each proposal from 0–2

- **Decisive:** Could the result change what the researcher believes or does next?
- **Executable:** Are the code change, data, metric, and run procedure concrete?
- **Controlled:** Does it identify a baseline and the main confound?
- **Efficient:** Is it the cheapest meaningful test?
- **Reproducible:** Could another person rerun it from the record?

Maximum score: 10.

## Win condition

The structured protocol wins if it improves the average blinded score by at least 2 points without taking more than 15 extra minutes per proposal.

## What this teaches us

- whether the first product should be a research-intake tool;
- which fields in the brief actually improve experiment quality;
- where AI needs researcher input;
- whether researchers would use this before running an experiment.

## After this test

Interview five researchers. Show them the two anonymized proposals and the experiment record, then ask where this workflow would save time or fail in their field.
