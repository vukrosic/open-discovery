#!/usr/bin/env python3
"""Run the frozen, standard-library-only robotics PID experiment.

The experiment compares a fixed hand-tuned PID controller with gains selected
from a small development grid.  The selected gains are evaluated only after
selection on the frozen hold-out episodes in BRIEF.md.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
BRIEF_PATH = ROOT / "BRIEF.md"

DT = 0.01
HORIZON_STEPS = 500
INERTIA = 1.0
DAMPING = 1.2
TORQUE_LIMIT = 8.0
ANGLE_LIMIT = 10.0
INTEGRAL_LIMIT = 4.0
SETTLING_TOLERANCE = 0.02

BASELINE_GAINS = (4.0, 1.0, 0.15)
KP_GRID = (2.5, 4.0, 5.5)
KI_GRID = (0.4, 1.0, 1.6)
KD_GRID = (0.05, 0.15, 0.30)


@dataclass(frozen=True)
class Episode:
    name: str
    split: str
    target: float
    pulses: tuple[tuple[float, float, float], ...]


DEV_EPISODES = (
    Episode(
        "dev-1",
        "development",
        1.0,
        ((1.5, 0.20, 1.5), (3.2, 0.15, -1.0)),
    ),
    Episode(
        "dev-2",
        "development",
        1.0,
        ((0.8, 0.25, -1.2), (2.7, 0.20, 1.3)),
    ),
)

HOLDOUT_EPISODES = (
    Episode(
        "holdout-1",
        "holdout",
        0.75,
        ((1.2, 0.18, 1.0), (3.6, 0.22, -1.4)),
    ),
    Episode(
        "holdout-2",
        "holdout",
        1.25,
        ((0.9, 0.20, -1.4), (3.0, 0.18, 1.6)),
    ),
    Episode(
        "holdout-3",
        "holdout",
        1.0,
        ((2.0, 0.30, 1.8),),
    ),
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def external_torque(time_s: float, pulses: Sequence[tuple[float, float, float]]) -> float:
    """Return the sum of rectangular disturbance pulses active at time_s."""

    total = 0.0
    for start, duration, magnitude in pulses:
        if start <= time_s < start + duration:
            total += magnitude
    return total


def simulate(episode: Episode, gains: tuple[float, float, float]) -> dict[str, object]:
    """Simulate one episode and return the trajectory plus checked metrics."""

    kp, ki, kd = gains
    angle = 0.0
    velocity = 0.0
    integral = 0.0
    previous_error = episode.target
    times: list[float] = []
    positions: list[float] = []
    torques: list[float] = []
    errors: list[float] = []
    unstable = False

    for step in range(HORIZON_STEPS):
        time_s = step * DT
        error = episode.target - angle
        integral = clamp(integral + error * DT, -INTEGRAL_LIMIT, INTEGRAL_LIMIT)
        derivative = 0.0 if step == 0 else (error - previous_error) / DT
        requested_torque = kp * error + ki * integral + kd * derivative
        torque = clamp(requested_torque, -TORQUE_LIMIT, TORQUE_LIMIT)

        acceleration = (torque + external_torque(time_s, episode.pulses) - DAMPING * velocity) / INERTIA
        velocity += DT * acceleration
        angle += DT * velocity

        times.append(time_s)
        positions.append(angle)
        torques.append(torque)
        errors.append(error)
        previous_error = error

        if not (math.isfinite(angle) and math.isfinite(velocity) and math.isfinite(torque)):
            unstable = True
        if abs(angle) > ANGLE_LIMIT:
            unstable = True

    rmse = math.sqrt(sum(error * error for error in errors) / len(errors))
    overshoot = max(0.0, max(positions) - episode.target)
    settling_time = float(HORIZON_STEPS * DT)
    for index in range(len(errors)):
        if all(abs(error) <= SETTLING_TOLERANCE for error in errors[index:]):
            settling_time = times[index]
            break
    energy = sum(torque * torque for torque in torques) * DT
    return {
        "times": times,
        "positions": positions,
        "torques": torques,
        "errors": errors,
        "rmse": rmse,
        "overshoot": overshoot,
        "settling_time": settling_time,
        "energy": energy,
        "unstable": unstable,
    }


def mean_metric(records: Iterable[dict[str, object]], key: str) -> float:
    values = [float(record[key]) for record in records]
    return sum(values) / len(values)


def evaluate_gains(
    episodes: Sequence[Episode], gains: tuple[float, float, float]
) -> tuple[list[dict[str, object]], dict[str, float | int | bool]]:
    records: list[dict[str, object]] = []
    for episode in episodes:
        metrics = simulate(episode, gains)
        records.append({"episode": episode, "metrics": metrics})
    aggregate: dict[str, float | int | bool] = {
        "rmse": mean_metric((record["metrics"] for record in records), "rmse"),
        "overshoot": mean_metric((record["metrics"] for record in records), "overshoot"),
        "settling_time": mean_metric((record["metrics"] for record in records), "settling_time"),
        "energy": mean_metric((record["metrics"] for record in records), "energy"),
        "stable_episodes": sum(not bool(record["metrics"]["unstable"]) for record in records),
        "episode_count": len(records),
        "stable": all(not bool(record["metrics"]["unstable"]) for record in records),
    }
    return records, aggregate


def format_float(value: float) -> str:
    return f"{value:.8f}"


def write_csv(path: Path, rows: Sequence[dict[str, object]], fieldnames: Sequence[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def svg_header(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2:.1f}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18" fill="#111">{title}</text>',
    ]


def trajectory_svg(path: Path, episode: Episode, baseline: dict[str, object], tuned: dict[str, object]) -> None:
    width, height = 820, 440
    left, right, top, bottom = 72, 24, 52, 62
    plot_width, plot_height = width - left - right, height - top - bottom
    all_positions = list(baseline["positions"]) + list(tuned["positions"])
    y_min = min(0.0, min(all_positions))
    y_max = max(episode.target, max(all_positions))
    margin = max(0.05, 0.08 * (y_max - y_min))
    y_min -= margin
    y_max += margin

    def x_for(time_s: float) -> float:
        return left + (time_s / (HORIZON_STEPS * DT)) * plot_width

    def y_for(position: float) -> float:
        return top + (y_max - position) / (y_max - y_min) * plot_height

    lines = svg_header(width, height, f"PID tracking on {episode.name}")
    lines += [
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" stroke="#222"/>',
        f'<line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" stroke="#222"/>',
        f'<line x1="{left}" y1="{y_for(episode.target):.2f}" x2="{width - right}" y2="{y_for(episode.target):.2f}" stroke="#777" stroke-dasharray="6 4"/>',
        f'<text x="{width - right - 4}" y="{y_for(episode.target) - 6:.2f}" text-anchor="end" font-family="sans-serif" font-size="12" fill="#555">target {episode.target:.2f} rad</text>',
        f'<text x="{width / 2:.1f}" y="{height - 16}" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#333">time (s)</text>',
        f'<text x="18" y="{height / 2:.1f}" text-anchor="middle" transform="rotate(-90 18 {height / 2:.1f})" font-family="sans-serif" font-size="13" fill="#333">angle (rad)</text>',
    ]

    for tick in (0, 1, 2, 3, 4, 5):
        x = x_for(float(tick))
        lines.append(f'<line x1="{x:.2f}" y1="{height - bottom}" x2="{x:.2f}" y2="{height - bottom + 5}" stroke="#222"/>')
        lines.append(f'<text x="{x:.2f}" y="{height - bottom + 21}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#444">{tick}</text>')

    for fraction in (0, 0.5, 1):
        value = y_min + fraction * (y_max - y_min)
        y = y_for(value)
        lines.append(f'<line x1="{left - 5}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="#222"/>')
        lines.append(f'<text x="{left - 9}" y="{y + 4:.2f}" text-anchor="end" font-family="sans-serif" font-size="11" fill="#444">{value:.2f}</text>')

    def points(values: Sequence[float]) -> str:
        return " ".join(f"{x_for(index * DT):.2f},{y_for(value):.2f}" for index, value in enumerate(values))

    lines += [
        f'<polyline points="{points(baseline["positions"])}" fill="none" stroke="#d95f02" stroke-width="2"/>',
        f'<polyline points="{points(tuned["positions"])}" fill="none" stroke="#1b9e77" stroke-width="2"/>',
        f'<line x1="{width - 180}" y1="48" x2="{width - 150}" y2="48" stroke="#d95f02" stroke-width="3"/><text x="{width - 143}" y="52" font-family="sans-serif" font-size="12">baseline</text>',
        f'<line x1="{width - 180}" y1="68" x2="{width - 150}" y2="68" stroke="#1b9e77" stroke-width="3"/><text x="{width - 143}" y="72" font-family="sans-serif" font-size="12">searched gains</text>',
        "</svg>",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def comparison_svg(path: Path, baseline_rmse: float, tuned_rmse: float) -> None:
    width, height = 620, 380
    left, right, top, bottom = 78, 36, 54, 70
    plot_width, plot_height = width - left - right, height - top - bottom
    max_value = max(baseline_rmse, tuned_rmse) * 1.25
    bar_width = 130
    baseline_x = left + plot_width * 0.25 - bar_width / 2
    tuned_x = left + plot_width * 0.75 - bar_width / 2

    def y_for(value: float) -> float:
        return height - bottom - value / max_value * plot_height

    lines = svg_header(width, height, "Hold-out tracking error")
    lines += [
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" stroke="#222"/>',
        f'<line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" stroke="#222"/>',
        f'<text x="18" y="{height / 2:.1f}" text-anchor="middle" transform="rotate(-90 18 {height / 2:.1f})" font-family="sans-serif" font-size="13" fill="#333">mean RMSE (rad)</text>',
    ]
    for fraction in (0, 0.5, 1):
        value = fraction * max_value
        y = y_for(value)
        lines.append(f'<line x1="{left - 5}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="#222"/>')
        lines.append(f'<text x="{left - 9}" y="{y + 4:.2f}" text-anchor="end" font-family="sans-serif" font-size="11" fill="#444">{value:.3f}</text>')

    for x, value, label, color in (
        (baseline_x, baseline_rmse, "baseline", "#d95f02"),
        (tuned_x, tuned_rmse, "searched gains", "#1b9e77"),
    ):
        y = y_for(value)
        lines.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width}" height="{height - bottom - y:.2f}" fill="{color}"/>')
        lines.append(f'<text x="{x + bar_width / 2:.2f}" y="{y - 8:.2f}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#333">{value:.4f}</text>')
        lines.append(f'<text x="{x + bar_width / 2:.2f}" y="{height - bottom + 28}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#333">{label}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def protocol_hash() -> str:
    return hashlib.sha256(BRIEF_PATH.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    RESULTS.mkdir(parents=True, exist_ok=True)

    development_candidates: list[dict[str, object]] = []
    for kp, ki, kd in itertools.product(KP_GRID, KI_GRID, KD_GRID):
        gains = (kp, ki, kd)
        records, aggregate = evaluate_gains(DEV_EPISODES, gains)
        development_candidates.append(
            {
                "gains": gains,
                "records": records,
                "aggregate": aggregate,
            }
        )

    stable_candidates = [candidate for candidate in development_candidates if candidate["aggregate"]["stable"]]
    assert stable_candidates, "the frozen development grid must contain a stable candidate"
    selected = min(stable_candidates, key=lambda candidate: (candidate["aggregate"]["rmse"], candidate["gains"]))
    selected_gains = tuple(float(value) for value in selected["gains"])

    baseline_dev_records, baseline_dev = evaluate_gains(DEV_EPISODES, BASELINE_GAINS)
    baseline_holdout_records, baseline_holdout = evaluate_gains(HOLDOUT_EPISODES, BASELINE_GAINS)
    tuned_dev_records, tuned_dev = evaluate_gains(DEV_EPISODES, selected_gains)
    tuned_holdout_records, tuned_holdout = evaluate_gains(HOLDOUT_EPISODES, selected_gains)

    improvement = float(baseline_holdout["rmse"]) - float(tuned_holdout["rmse"])
    decision = bool(tuned_holdout["stable"]) and improvement > 0.0

    tuning_rows: list[dict[str, object]] = []
    ordered = sorted(development_candidates, key=lambda candidate: (candidate["aggregate"]["rmse"], candidate["gains"]))
    selected_tuple = selected["gains"]
    for rank, candidate in enumerate(ordered, start=1):
        kp, ki, kd = candidate["gains"]
        aggregate = candidate["aggregate"]
        tuning_rows.append(
            {
                "rank": rank,
                "kp": format_float(float(kp)),
                "ki": format_float(float(ki)),
                "kd": format_float(float(kd)),
                "mean_dev_rmse": format_float(float(aggregate["rmse"])),
                "mean_dev_overshoot": format_float(float(aggregate["overshoot"])),
                "mean_dev_settling_time_s": format_float(float(aggregate["settling_time"])),
                "mean_dev_energy": format_float(float(aggregate["energy"])),
                "stable_episodes": int(aggregate["stable_episodes"]),
                "selected": bool(candidate["gains"] == selected_tuple),
            }
        )
    write_csv(
        RESULTS / "tuning_grid.csv",
        tuning_rows,
        (
            "rank",
            "kp",
            "ki",
            "kd",
            "mean_dev_rmse",
            "mean_dev_overshoot",
            "mean_dev_settling_time_s",
            "mean_dev_energy",
            "stable_episodes",
            "selected",
        ),
    )

    result_rows: list[dict[str, object]] = []
    all_final_records = (
        ("baseline", BASELINE_GAINS, "development", baseline_dev_records),
        ("searched", selected_gains, "development", tuned_dev_records),
        ("baseline", BASELINE_GAINS, "holdout", baseline_holdout_records),
        ("searched", selected_gains, "holdout", tuned_holdout_records),
    )
    for controller, gains, split, records in all_final_records:
        kp, ki, kd = gains
        for record in records:
            episode = record["episode"]
            metrics = record["metrics"]
            result_rows.append(
                {
                    "controller": controller,
                    "split": split,
                    "episode": episode.name,
                    "target_rad": format_float(episode.target),
                    "kp": format_float(kp),
                    "ki": format_float(ki),
                    "kd": format_float(kd),
                    "rmse_rad": format_float(float(metrics["rmse"])),
                    "overshoot_rad": format_float(float(metrics["overshoot"])),
                    "settling_time_s": format_float(float(metrics["settling_time"])),
                    "energy_torque2_s": format_float(float(metrics["energy"])),
                    "stable": bool(not metrics["unstable"]),
                }
            )
    write_csv(
        RESULTS / "results.csv",
        result_rows,
        (
            "controller",
            "split",
            "episode",
            "target_rad",
            "kp",
            "ki",
            "kd",
            "rmse_rad",
            "overshoot_rad",
            "settling_time_s",
            "energy_torque2_s",
            "stable",
        ),
    )

    summary = {
        "question": "Does a small automatic PID gain search improve hold-out tracking on a simulated one-joint arm?",
        "primary_metric": "mean_holdout_rmse_rad",
        "baseline_gains": {"kp": BASELINE_GAINS[0], "ki": BASELINE_GAINS[1], "kd": BASELINE_GAINS[2]},
        "selected_gains": {"kp": selected_gains[0], "ki": selected_gains[1], "kd": selected_gains[2]},
        "development": {"baseline": baseline_dev, "searched": tuned_dev},
        "holdout": {"baseline": baseline_holdout, "searched": tuned_holdout},
        "holdout_rmse_improvement_rad": improvement,
        "decision": "PASS" if decision else "FAIL",
        "rows": len(result_rows),
        "tuning_rows": len(tuning_rows),
        "claim_boundary": "Finite comparison on the frozen simulated plant and episodes only; no hardware or optimality claim.",
    }
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    representative_baseline = simulate(HOLDOUT_EPISODES[0], BASELINE_GAINS)
    representative_tuned = simulate(HOLDOUT_EPISODES[0], selected_gains)
    trajectory_svg(RESULTS / "trajectory.svg", HOLDOUT_EPISODES[0], representative_baseline, representative_tuned)
    comparison_svg(RESULTS / "rmse_comparison.svg", float(baseline_holdout["rmse"]), float(tuned_holdout["rmse"]))

    receipt = {
        "status": "COMPLETE",
        "command": "python3 experiment.py",
        "python": platform.python_version(),
        "protocol_sha256": protocol_hash(),
        "parameters": {
            "dt_s": DT,
            "horizon_steps": HORIZON_STEPS,
            "inertia": INERTIA,
            "damping": DAMPING,
            "torque_limit": TORQUE_LIMIT,
            "development_episode_count": len(DEV_EPISODES),
            "holdout_episode_count": len(HOLDOUT_EPISODES),
            "grid_size": len(development_candidates),
        },
        "outputs": [
            "results.csv",
            "tuning_grid.csv",
            "summary.json",
            "trajectory.svg",
            "rmse_comparison.svg",
            "run_receipt.json",
        ],
    }
    with (RESULTS / "run_receipt.json").open("w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=2, sort_keys=True)
        handle.write("\n")

    # Checked artifacts: the run should fail loudly if an output silently
    # disappears or if a future edit changes the expected experiment size.
    assert len(result_rows) == 10, len(result_rows)
    assert len(tuning_rows) == 27, len(tuning_rows)
    for filename in receipt["outputs"]:
        output_path = RESULTS / filename
        assert output_path.exists() and output_path.stat().st_size > 0, filename
    for svg_name in ("trajectory.svg", "rmse_comparison.svg"):
        svg_text = (RESULTS / svg_name).read_text(encoding="utf-8")
        assert svg_text.startswith("<svg ") and svg_text.rstrip().endswith("</svg>"), svg_name
    assert abs(float(summary["holdout_rmse_improvement_rad"]) - improvement) < 1e-12

    print(json.dumps({
        "status": receipt["status"],
        "decision": summary["decision"],
        "selected_gains": summary["selected_gains"],
        "baseline_holdout_rmse": baseline_holdout["rmse"],
        "searched_holdout_rmse": tuned_holdout["rmse"],
        "improvement_rad": improvement,
        "results": str(RESULTS),
    }, sort_keys=True))
    return summary


if __name__ == "__main__":
    run()
