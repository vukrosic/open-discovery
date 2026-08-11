"""Create a fresh post-freeze confirmation bundle and print its receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import secrets
from pathlib import Path

from fixtures import _sample


def build(seed: int) -> dict:
    cohorts = []
    specifications = ((-0.90, 20), (0.35, 30), (1.05, 40))
    for index, (shift, disease_count) in enumerate(specifications, start=1):
        rng = random.Random(seed + index)
        labels = [1] * disease_count + [0] * (60 - disease_count)
        rng.shuffle(labels)
        batch = f"CONFIRM_{index}"
        rows = [
            _sample(rng, f"{batch}_{row_index:03d}", batch, label, shift)
            for row_index, label in enumerate(labels)
        ]
        cohorts.append({"name": batch, "rows": rows})
    return {"schema_version": 1, "cohorts": cohorts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else secrets.randbits(63)
    encoded = (json.dumps(build(seed), sort_keys=True, separators=(",", ":")) + "\n").encode()
    args.output.write_bytes(encoded)
    print(json.dumps({"seed": seed, "sha256": hashlib.sha256(encoded).hexdigest()}))

