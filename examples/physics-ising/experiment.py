"""Reproducible 2D Ising sampler comparison using only the Python standard library."""

from __future__ import annotations

import csv
import json
import math
import platform
import random
import statistics
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SIZES = (16, 32)
TEMPERATURES = (2.0, 2.2, 2.269, 2.4, 2.6)
SAMPLERS = ("metropolis", "wolff")
SEEDS = (7, 11, 13)
BURN_IN = 200
SAMPLES = 500
CRITICAL_TEMPERATURE = 2.269


class Ising2D:
    def __init__(self, size: int, temperature: float, rng: random.Random):
        self.size = size
        self.temperature = temperature
        self.rng = rng
        self.spins = [1 if rng.random() < 0.5 else -1 for _ in range(size * size)]

    def _index(self, row: int, col: int) -> int:
        return (row % self.size) * self.size + (col % self.size)

    def _neighbor_sum(self, row: int, col: int) -> int:
        return (
            self.spins[self._index(row - 1, col)]
            + self.spins[self._index(row + 1, col)]
            + self.spins[self._index(row, col - 1)]
            + self.spins[self._index(row, col + 1)]
        )

    def metropolis_sweep(self) -> None:
        for _ in range(self.size * self.size):
            row = self.rng.randrange(self.size)
            col = self.rng.randrange(self.size)
            index = self._index(row, col)
            delta_energy = 2 * self.spins[index] * self._neighbor_sum(row, col)
            if delta_energy <= 0 or self.rng.random() < math.exp(-delta_energy / self.temperature):
                self.spins[index] *= -1

    def wolff_sweep(self) -> int:
        flipped = 0
        bond_probability = 1.0 - math.exp(-2.0 / self.temperature)
        while flipped < self.size * self.size:
            seed_row = self.rng.randrange(self.size)
            seed_col = self.rng.randrange(self.size)
            seed_index = self._index(seed_row, seed_col)
            old_spin = self.spins[seed_index]
            cluster = {seed_index}
            stack = [(seed_row, seed_col)]
            while stack:
                row, col = stack.pop()
                for next_row, next_col in (
                    (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)
                ):
                    index = self._index(next_row, next_col)
                    if index not in cluster and self.spins[index] == old_spin:
                        if self.rng.random() < bond_probability:
                            cluster.add(index)
                            stack.append((next_row % self.size, next_col % self.size))
            for index in cluster:
                self.spins[index] *= -1
            flipped += len(cluster)
        return flipped

    def magnetization(self) -> float:
        return sum(self.spins) / len(self.spins)

    def energy(self) -> float:
        total = 0
        for row in range(self.size):
            for col in range(self.size):
                index = self._index(row, col)
                total -= self.spins[index] * (
                    self.spins[self._index(row, col + 1)]
                    + self.spins[self._index(row + 1, col)]
                )
        return total / len(self.spins)


def integrated_autocorrelation(values: list[float]) -> float:
    if len(values) < 3:
        return float("nan")
    mean = statistics.mean(values)
    centered = [value - mean for value in values]
    variance = sum(value * value for value in centered) / len(centered)
    if variance == 0:
        return 0.5
    tau = 0.5
    for lag in range(1, min(len(values) // 2, 200)):
        covariance = sum(
            centered[index] * centered[index + lag]
            for index in range(len(centered) - lag)
        ) / (len(centered) - lag)
        correlation = covariance / variance
        if correlation <= 0:
            break
        tau += correlation
    return tau


def simulate(size: int, temperature: float, sampler: str, seed: int) -> dict:
    rng = random.Random(seed)
    model = Ising2D(size, temperature, rng)
    started = time.perf_counter()
    for _ in range(BURN_IN):
        if sampler == "metropolis":
            model.metropolis_sweep()
        else:
            model.wolff_sweep()
    magnetizations, energies = [], []
    for _ in range(SAMPLES):
        if sampler == "metropolis":
            model.metropolis_sweep()
        else:
            model.wolff_sweep()
        magnetizations.append(model.magnetization())
        energies.append(model.energy())
    elapsed = time.perf_counter() - started
    mean_magnetization = statistics.mean(magnetizations)
    mean_abs_magnetization = statistics.mean(abs(value) for value in magnetizations)
    mean_energy = statistics.mean(energies)
    susceptibility = size * size * (
        statistics.mean(value * value for value in magnetizations)
        - mean_magnetization * mean_magnetization
    ) / temperature
    tau = integrated_autocorrelation(magnetizations)
    return {
        "size": size,
        "temperature": temperature,
        "sampler": sampler,
        "seed": seed,
        "burn_in": BURN_IN,
        "samples": SAMPLES,
        "mean_abs_magnetization": mean_abs_magnetization,
        "mean_energy": mean_energy,
        "susceptibility": susceptibility,
        "tau_int_magnetization": tau,
        "runtime_seconds": elapsed,
        "effective_independent_samples": SAMPLES / (2.0 * tau) if tau > 0 else float("nan"),
    }


def svg_line_plot(path: Path, title: str, x_label: str, y_label: str, series: dict[str, list[tuple[float, float]]]) -> None:
    width, height = 860, 480
    left, right, top, bottom = 80, 30, 55, 70
    points = [point for values in series.values() for point in values]
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    if x_min == x_max:
        x_max += 1
    if y_min == y_max:
        y_max += 1
    def project(point: tuple[float, float]) -> tuple[float, float]:
        x, y = point
        px = left + (x - x_min) / (x_max - x_min) * (width - left - right)
        py = height - bottom - (y - y_min) / (y_max - y_min) * (height - top - bottom)
        return px, py
    colors = ("#2166ac", "#b2182b", "#4d9221", "#762a83")
    body = [f'<rect width="{width}" height="{height}" fill="white"/>', f'<text x="{left}" y="30" font-size="20">{title}</text>']
    body.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="black"/>')
    body.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="black"/>')
    body.append(f'<text x="{width/2}" y="{height-20}" text-anchor="middle" font-size="14">{x_label}</text>')
    body.append(f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" text-anchor="middle" font-size="14">{y_label}</text>')
    for color, (label, values) in zip(colors, series.items()):
        projected = [project(point) for point in sorted(values)]
        points_text = " ".join(f"{x:.1f},{y:.1f}" for x, y in projected)
        body.append(f'<polyline points="{points_text}" fill="none" stroke="{color}" stroke-width="2"/>')
        lx, ly = width - 175, top + 20 * list(series).index(label)
        body.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+24}" y2="{ly}" stroke="{color}" stroke-width="3"/>')
        body.append(f'<text x="{lx+30}" y="{ly+5}" font-size="12">{label}</text>')
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg">' + "".join(body) + "</svg>", encoding="utf-8")


def write_outputs(rows: list[dict]) -> None:
    RESULTS.mkdir(exist_ok=True)
    fields = list(rows[0])
    with (RESULTS / "results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    critical = [row for row in rows if row["temperature"] == CRITICAL_TEMPERATURE]
    summary = {
        "protocol": "BRIEF.md",
        "primary_outcome": "tau_int_magnetization",
        "critical_temperature": CRITICAL_TEMPERATURE,
        "critical_summary": {
            sampler: {
                "mean_tau": statistics.mean(row["tau_int_magnetization"] for row in critical if row["sampler"] == sampler),
                "mean_runtime_seconds": statistics.mean(row["runtime_seconds"] for row in critical if row["sampler"] == sampler),
            }
            for sampler in SAMPLERS
        },
        "rows": len(rows),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    phase_series = {}
    for sampler in SAMPLERS:
        phase_series[f"{sampler} L=32"] = [
            (row["temperature"], row["mean_abs_magnetization"])
            for row in rows if row["sampler"] == sampler and row["size"] == 32
        ]
    svg_line_plot(RESULTS / "phase-transition.svg", "Finite-size Ising transition", "temperature", "mean |magnetization|", phase_series)
    auto_series = {}
    for sampler in SAMPLERS:
        auto_series[sampler] = [
            (row["size"], row["tau_int_magnetization"])
            for row in critical if row["sampler"] == sampler
        ]
    svg_line_plot(RESULTS / "autocorrelation.svg", "Critical-point magnetization autocorrelation", "lattice size", "integrated autocorrelation time", auto_series)
    receipt = {
        "python": platform.python_version(),
        "command": "python3 experiment.py",
        "sizes": SIZES,
        "temperatures": TEMPERATURES,
        "samplers": SAMPLERS,
        "seeds": SEEDS,
        "burn_in": BURN_IN,
        "samples": SAMPLES,
    }
    (RESULTS / "run_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    rows = []
    for size in SIZES:
        for temperature in TEMPERATURES:
            for sampler in SAMPLERS:
                for seed in SEEDS:
                    rows.append(simulate(size, temperature, sampler, seed))
    write_outputs(rows)
    assert len(rows) == len(SIZES) * len(TEMPERATURES) * len(SAMPLERS) * len(SEEDS)
    assert all(row["tau_int_magnetization"] > 0 for row in rows)
    print(json.dumps({"status": "COMPLETE", "rows": len(rows), "results": str(RESULTS)}))


if __name__ == "__main__":
    main()

