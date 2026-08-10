# Program Evolution

Program Evolution improves a human-supplied baseline program against a
human-supplied evaluation script. It is Open Discovery's machine-gradable
optimization path: agents propose code changes, but external code decides
whether each candidate is correct and better.

## Inputs

The user supplies:

1. a baseline file or directory;
2. an evaluator script;
3. a plain-language goal naming what should improve.

The evaluator receives the candidate path as its only positional argument. It
must exit successfully and print exactly one JSON object to standard output.
The recommended result shape is:

```json
{
  "valid": true,
  "improved": true,
  "objective": {
    "name": "speedup",
    "value": 1.24,
    "baseline_value": 1.0,
    "direction": "maximize"
  },
  "metrics": {},
  "failures": []
}
```

The evaluator owns correctness, quality tolerances, representative workloads,
and the objective. It should measure candidates externally rather than trust
candidate-reported timing or scores. Keep final confirmation cases separate
from the examples repeatedly used during search whenever practical.

## First step: lock the starting point

```bash
python3 program-evolution/scripts/lock_baseline.py \
  --baseline path/to/program \
  --evaluator path/to/evaluate.py \
  --goal "reduce runtime without changing outputs" \
  --output path/to/project/baseline-lock
```

This copies and hashes the baseline and evaluator, evaluates the copied
baseline, and records the result in `lock.json`. It refuses to overwrite an
existing lock and fails if evaluation mutates the baseline or evaluator.

## Candidate loop

After the lock succeeds, an initiative may run independent candidate workers.
Each worker receives a parent program, relevant prior evidence, and
[`prompts/propose-candidate.md`](prompts/propose-candidate.md). Workers write to
separate candidate folders and cannot edit the evaluator. Evaluate inexpensive
correctness gates first, then spend more compute only on valid candidates.

Keep candidate lineage, patches, evaluator output, and failures. Select both
strong candidates and meaningfully different candidates; repeatedly editing
only the current winner can trap the search in one mechanism. Reconstruct any
claimed winner from the locked baseline and rerun it on fresh confirmation
cases before presenting it.

This directory currently supplies the reliable input, evaluation, and
measurement layer. It does not yet contain a permanent cloud scheduler or a
fully automatic evolutionary database.

## Recording an agent run

```bash
python3 program-evolution/scripts/run_benchmark.py \
  --benchmark program-evolution/benchmarks/pillow-histogram \
  --candidate path/to/candidate.py \
  --model gpt-5.6-luna \
  --track blind \
  --agent-duration-seconds 180 \
  --tokens 12000 \
  --results path/to/results.jsonl
```

Summarize accumulated runs with:

```bash
python3 program-evolution/scripts/summarize_results.py path/to/results.jsonl
```

Track performance over time using validity rate, improvement rate, objective
value, time to result, token use, and cost. Record whether a run was `blind` or
`open-book`; those tracks are not comparable. Always retain benchmark and
evaluator hashes: an apparent model improvement after the benchmark changed is
not a comparable result.

## Included benchmarks

- **NetworkX bounded cycles:** a pinned current-upstream cycle-enumeration hot
  path with an open worst-case performance problem. It requires exact cycles,
  tests generated graphs against an independent oracle, measures two
  adversarial families, and guards ordinary-case runtime.
- **Pillow histogram:** exact scientific-image pixel histogram. It rewards
  removing Python-level image loops while requiring identical counts.
- **Power economic dispatch:** a simplified integer generator-dispatch problem
  that minimizes generation cost under capacity and demand constraints. It is
  representative of a power-system optimization pattern, not production grid
  software.

The Pillow and power-dispatch tasks are small local development benchmarks.
The NetworkX task is a pinned frontier benchmark derived from a current open
upstream problem, but success still establishes only the behavior covered by
its evaluator—not general scientific or industrial capability. Each benchmark
defines its own conservative `improved` threshold and exposes raw paired
measurements for analysis.
