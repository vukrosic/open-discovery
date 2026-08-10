#!/usr/bin/env python3
"""Check bounded-cycle correctness and measure adversarial search performance."""

from __future__ import annotations

import contextlib
import gc
import importlib.util
import io
import json
import math
import random
import statistics
import sys
import time
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
MAX_CYCLES = 100_000


def candidate_file(path: Path) -> Path:
    return path / "solution.py" if path.is_dir() else path


def load_search(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, candidate_file(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load candidate: {path}")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    function = getattr(module, "bounded_cycle_search", None)
    if not callable(function):
        raise TypeError("candidate must define bounded_cycle_search(graph, path, length_bound)")
    return function


def freeze_graph(graph):
    return {node: tuple(neighbors) for node, neighbors in graph.items()}


def brute_force_cycles(graph, prefix, length_bound):
    """Independent exhaustive oracle used only on small correctness cases."""

    start = prefix[0]
    route = list(prefix)
    visited = set(route)
    found = []

    def search(node):
        for neighbor in graph[node]:
            if neighbor == start:
                if len(route) <= length_bound:
                    found.append(tuple(route))
            elif len(route) < length_bound and neighbor not in visited:
                visited.add(neighbor)
                route.append(neighbor)
                search(neighbor)
                route.pop()
                visited.remove(neighbor)

    search(route[-1])
    return Counter(found)


def collect_cycles(function, graph, prefix, length_bound):
    graph_before = freeze_graph(graph)
    working_path = list(prefix)
    cycles = []
    with contextlib.redirect_stdout(io.StringIO()):
        for index, cycle in enumerate(function(graph, working_path, length_bound)):
            if index >= MAX_CYCLES:
                raise ValueError(f"candidate exceeded {MAX_CYCLES} cycles")
            if not isinstance(cycle, (list, tuple)):
                raise TypeError("every cycle must be a list or tuple")
            cycles.append(tuple(cycle))

    if freeze_graph(graph) != graph_before:
        raise ValueError("candidate mutated the graph")

    for cycle in cycles:
        if not cycle or len(cycle) > length_bound:
            raise ValueError("candidate returned an empty or over-bound cycle")
        if cycle[: len(prefix)] != tuple(prefix):
            raise ValueError("candidate returned a cycle outside the supplied prefix")
        if len(set(cycle)) != len(cycle):
            raise ValueError("candidate returned a non-simple cycle")
        closed = cycle[1:] + (cycle[0],)
        if any(target not in graph[source] for source, target in zip(cycle, closed)):
            raise ValueError("candidate returned a path containing a missing edge")

    counts = Counter(cycles)
    if any(count != 1 for count in counts.values()):
        raise ValueError("candidate returned a duplicate cycle")
    return counts


def explicit_cases():
    mixed = {"s": (1, ("x", 2)), 1: (("x", 2), "s"), ("x", 2): ("s",)}
    return [
        ({0: (0,)}, [0], 1),
        ({0: (1,), 1: (0,)}, [0], 2),
        ({0: (1, 2), 1: (2, 0), 2: (0, 1)}, [0], 3),
        ({0: (1,), 1: (2, 3), 2: (0,), 3: (2,), 4: ()}, [0, 1], 4),
        (mixed, ["s"], 3),
    ]


def random_cases():
    cases = []
    for seed in range(36):
        rng = random.Random(710_000 + seed)
        size = 3 + seed % 7
        probability = 0.12 + 0.05 * (seed % 6)
        graph = {
            source: tuple(
                target
                for target in range(size)
                if rng.random() < probability
            )
            for source in range(size)
        }
        start = rng.randrange(size)
        cases.append((graph, [start], 1 + seed % min(size, 6)))

        outgoing = graph[start]
        if outgoing:
            second = outgoing[0]
            if second != start:
                cases.append((graph, [start, second], min(size, 5)))
    return cases


def diamond_chain(size):
    graph = {}

    def add_edge(source, target):
        graph.setdefault(source, []).append(target)
        graph.setdefault(target, [])

    for index in range(size):
        root = f"d{index}"
        left = f"a{index}"
        right = f"b{index}"
        next_root = f"d{index + 1}"
        add_edge(root, left)
        add_edge(root, right)
        add_edge(left, next_root)
        add_edge(right, next_root)
    add_edge(f"d{size}", "d0")
    return freeze_graph(graph), ["d0"], 2 * size


def wave_gadget(size):
    graph = {}

    def add_edge(source, target):
        graph.setdefault(source, []).append(target)
        graph.setdefault(target, [])

    start = "S"
    q_nodes = [f"Q{index}" for index in range(1, size + 1)]
    d_nodes = [f"D{index}" for index in range(size + 1)]
    x_nodes = [f"X{index}" for index in range(size)]
    add_edge(start, q_nodes[0])
    for index in range(size - 1):
        add_edge(q_nodes[index], q_nodes[index + 1])
    add_edge(q_nodes[-1], start)
    for index in range(size):
        add_edge(q_nodes[index], d_nodes[0])
    for index in range(size):
        add_edge(d_nodes[index], x_nodes[index])
        add_edge(x_nodes[index], d_nodes[index + 1])
        add_edge(d_nodes[index], d_nodes[index + 1])
    for index in range(1, size + 1):
        add_edge(d_nodes[index], q_nodes[index - 1])
    return freeze_graph(graph), [start], size + 1


def ordinary_workload():
    cases = explicit_cases() + random_cases()
    return cases * 128


def execute_workload(function, workload):
    total = 0
    for graph, prefix, length_bound in workload:
        with contextlib.redirect_stdout(io.StringIO()):
            total += sum(1 for _ in function(graph, list(prefix), length_bound))
    return total


def paired_runtime(baseline, candidate, workload, pairs=5):
    expected_count = execute_workload(baseline, workload)
    observed_count = execute_workload(candidate, workload)
    if observed_count != expected_count:
        raise ValueError("candidate changed output count on a timing workload")

    baseline_samples = []
    candidate_samples = []
    gc.disable()
    try:
        for pair in range(pairs):
            order = ((baseline, baseline_samples), (candidate, candidate_samples))
            if pair % 2:
                order = tuple(reversed(order))
            for function, samples in order:
                started = time.perf_counter()
                count = execute_workload(function, workload)
                samples.append(time.perf_counter() - started)
                if count != expected_count:
                    raise ValueError("candidate changed output during timing")
    finally:
        gc.enable()

    speedups = [
        baseline_seconds / candidate_seconds
        for baseline_seconds, candidate_seconds in zip(
            baseline_samples, candidate_samples
        )
    ]
    return {
        "baseline_seconds": statistics.median(baseline_samples),
        "candidate_seconds": statistics.median(candidate_samples),
        "speedup": statistics.median(speedups),
        "paired_speedups": speedups,
        "candidate_wins": sum(speedup > 1.0 for speedup in speedups),
        "cycles_per_run": expected_count,
    }


def invalid(reason):
    print(json.dumps({"valid": False, "improved": False, "failures": [reason]}))
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        return invalid("usage: evaluate.py CANDIDATE")
    try:
        candidate = load_search(Path(sys.argv[1]).resolve(), "candidate_cycles")
        baseline = load_search(HERE / "baseline.py", "baseline_cycles")
    except Exception as error:
        return invalid(f"candidate load failed: {type(error).__name__}: {error}")

    cases = explicit_cases() + random_cases()
    try:
        for index, (graph, prefix, length_bound) in enumerate(cases):
            expected = brute_force_cycles(graph, prefix, length_bound)
            observed = collect_cycles(candidate, graph, prefix, length_bound)
            if observed != expected:
                return invalid(
                    {
                        "case": index,
                        "reason": "cycle set mismatch",
                        "expected_count": sum(expected.values()),
                        "observed_count": sum(observed.values()),
                    }
                )

        for name, case in (("diamond", diamond_chain(9)), ("wave", wave_gadget(7))):
            graph, prefix, length_bound = case
            expected = brute_force_cycles(graph, prefix, length_bound)
            observed = collect_cycles(candidate, graph, prefix, length_bound)
            if observed != expected:
                return invalid({"case": name, "reason": "adversarial cycle mismatch"})

        timings = {
            "ordinary": paired_runtime(baseline, candidate, ordinary_workload()),
            "diamond": paired_runtime(baseline, candidate, [diamond_chain(18)]),
            "wave": paired_runtime(baseline, candidate, [wave_gadget(40)]),
        }
    except Exception as error:
        return invalid(f"candidate evaluation failed: {type(error).__name__}: {error}")

    adversarial_speedup = math.sqrt(
        timings["diamond"]["speedup"] * timings["wave"]["speedup"]
    )
    ordinary_speedup = timings["ordinary"]["speedup"]
    score = adversarial_speedup * min(1.0, ordinary_speedup)
    improved = (
        score > 1.5
        and min(timings["diamond"]["speedup"], timings["wave"]["speedup"]) > 1.25
        and ordinary_speedup > 0.75
        and timings["diamond"]["candidate_wins"] >= 4
        and timings["wave"]["candidate_wins"] >= 4
    )
    print(
        json.dumps(
            {
                "valid": True,
                "improved": improved,
                "objective": {
                    "name": "regression_guarded_adversarial_speedup",
                    "value": score,
                    "baseline_value": 1.0,
                    "direction": "maximize",
                },
                "metrics": {
                    "exact_cases": len(cases) + 2,
                    "adversarial_geomean_speedup": adversarial_speedup,
                    "ordinary_speedup": ordinary_speedup,
                    "workloads": timings,
                },
                "failures": [],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
