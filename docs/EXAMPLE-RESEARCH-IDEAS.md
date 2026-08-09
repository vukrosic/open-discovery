# Example research ideas

These examples show the kinds of starting directions a researcher can bring to
Open Discovery. They are starting points, not claims of novelty. An autonomous
initiative may select, sharpen, reject, or replace them from evidence.

## Faster LLM reinforcement-learning rollouts

Can speculative decoding reduce the time and cost of generating rollouts during
LLM reinforcement-learning post-training without changing the training signal
or final model quality?

Possible first step: measure rollout throughput, acceptance rate, reward
distribution, and training compatibility against ordinary autoregressive
generation on one bounded setup.

## OpenBMB inference optimization

Which inference bottleneck should be optimized to make an OpenBMB model run
faster while preserving output quality?

Possible first step: profile one fixed model and workload, identify the largest
measured bottleneck, and test one targeted optimization against the unchanged
baseline.
