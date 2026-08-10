from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "scripts" / "lock_baseline.py"
RUN = ROOT / "scripts" / "run_benchmark.py"
SUMMARY = ROOT / "scripts" / "summarize_results.py"


class ProgramEvolutionTests(unittest.TestCase):
    def test_baseline_lock_records_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline.py"
            evaluator = root / "evaluate.py"
            output = root / "lock"
            baseline.write_text("VALUE = 7\n", encoding="utf-8")
            evaluator.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                "print(json.dumps({'valid': 'VALUE = 7' in Path(sys.argv[1]).read_text()}))\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(LOCK),
                    "--baseline",
                    str(baseline),
                    "--evaluator",
                    str(evaluator),
                    "--goal",
                    "preserve value",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            lock = json.loads((output / "lock.json").read_text())
            self.assertEqual(lock["status"], "locked")
            self.assertTrue(lock["evaluator"]["metrics"]["valid"])
            self.assertFalse(any(output.rglob("*.pyc")))

    def test_baseline_lock_rejects_mutating_evaluator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline.py"
            evaluator = root / "evaluate.py"
            output = root / "lock"
            baseline.write_text("VALUE = 7\n", encoding="utf-8")
            evaluator.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                "Path(sys.argv[1]).write_text('VALUE = 8\\n')\n"
                "print(json.dumps({'valid': True}))\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(LOCK),
                    "--baseline",
                    str(baseline),
                    "--evaluator",
                    str(evaluator),
                    "--goal",
                    "preserve value",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 1)
            lock = json.loads((output / "lock.json").read_text())
            self.assertEqual(lock["status"], "setup_failed")
            self.assertEqual(lock["error"], "evaluator modified the locked baseline")

    def test_included_benchmarks_accept_their_baselines(self):
        for name in [
            "networkx-bounded-cycles",
            "pillow-histogram",
            "power-economic-dispatch",
        ]:
            benchmark = ROOT / "benchmarks" / name
            completed = subprocess.run(
                [sys.executable, str(benchmark / "evaluate.py"), str(benchmark / "baseline.py")],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertTrue(result["valid"], name)
            self.assertFalse(result["improved"], name)

    def test_frontier_benchmark_rejects_missing_cycles(self):
        benchmark = ROOT / "benchmarks" / "networkx-bounded-cycles"
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.py"
            candidate.write_text(
                "def bounded_cycle_search(graph, path, length_bound):\n"
                "    if False:\n"
                "        yield None\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(benchmark / "evaluate.py"), str(candidate)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertFalse(result["valid"])
            self.assertFalse(result["improved"])

    def test_benchmark_runner_appends_comparable_record(self):
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "runs.jsonl"
            benchmark = ROOT / "benchmarks" / "power-economic-dispatch"
            environment = os.environ.copy()
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUN),
                    "--benchmark",
                    str(benchmark),
                    "--candidate",
                    str(benchmark / "baseline.py"),
                    "--model",
                    "test-model",
                    "--results",
                    str(results),
                ],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            record = json.loads(results.read_text())
            self.assertEqual(record["model"], "test-model")
            self.assertEqual(record["track"], "unspecified")
            self.assertTrue(record["evaluation"]["valid"])
            self.assertFalse(any(benchmark.rglob("*.pyc")))
            summary = subprocess.run(
                [sys.executable, str(SUMMARY), str(results)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(summary.returncode, 0, summary.stderr)
            benchmark_summary = next(iter(json.loads(summary.stdout).values()))
            self.assertEqual(benchmark_summary["track"], "unspecified")
            model_summary = benchmark_summary["models"]["test-model"]
            self.assertEqual(model_summary["runs"], 1)
            self.assertEqual(model_summary["valid_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
