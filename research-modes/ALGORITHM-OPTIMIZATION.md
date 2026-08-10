# Algorithm optimization mode

Use this mode for autonomously finding and validating improvements to
algorithms, libraries, runtimes, and engineering systems. It is not limited to
AI or machine learning.

These are adaptable principles, not a mandatory checklist. The responsible
agent should choose the evidence and depth appropriate to the algorithm,
stakes, resources, and intended claim.

## General principles

- Start from a real workload and a measured bottleneck; optimize what matters
  to users rather than whatever code is easiest to change.
- Preserve the capability people rely on. Depending on the task, that may mean
  exact output, a justified numerical tolerance, or a frozen quality measure.
- Compare against a strong practical baseline and include setup, conversion,
  memory, and other end-to-end costs when they affect actual use.
- Explore broadly and cheaply, then confirm only promising changes on fresh or
  held-out workloads. Look for counterexamples and cases where the change
  merely moves cost elsewhere.
- Prefer simple, maintainable improvements when performance is similar, while
  allowing deeper changes when the evidence justifies their complexity.
- Publish conservative, reproducible, workload-scoped improvements. A local
  win can be useful without implying that every machine, input, or caller will
  improve.

## When behavior should remain unchanged

- Freeze useful behavioral oracles before timing, including outputs, errors,
  metadata, mutation, and important boundary cases.
- Benchmark the intended hot path and representative untouched paths, using
  enough repeated work to distinguish improvement from noise.
- Independently reconstruct promising candidates from clean pinned source and
  rerun correctness, relevant tests, and a fresh benchmark.
- Revalidate the combined build before packaging multiple accepted changes.

For a public optimization repository or post, include only the specific paths
with independently verified improvement and no observed behavioral regression.
State that scope plainly and retain limitations that qualify the accepted
claim. Keep rejected, noisy, and inconclusive experiments in local research
evidence instead of presenting them as public features.

When an optimization belongs to a scientific field, use this guide together
with that field's research mode where useful.
