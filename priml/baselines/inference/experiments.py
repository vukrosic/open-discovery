"""
FP4 Speculative Decoding Experiment Configurations (exp004).

Following priml pattern: one change per fork, frozen baselines.
Generates 480 configurations varying drafter type, tree depth,
acceptance threshold, calibration data, FP4 quantization, and format.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# =============================================================================
# Config Classes
# =============================================================================

@dataclass
class SpeculativeDecodingConfig:
    """Configuration for a speculative decoding experiment.

    Attributes:
        drafter_type: Type of speculative drafter (eagle, medusa, tiny_llama)
        tree_depth: Depth of the token tree (1-5)
        acceptance_threshold: Quality/speedup tradeoff threshold (0.5-1.0)
        calibration_data: Calibration dataset (c4, wikitext, sharegpt, ultrachat)
        quantize_drafter: Whether to FP4-quantize the drafter model
        drafter_fp4_format: FP4 format if quantizing (e2m1, nvfp4_block16)
    """

    drafter_type: str = "eagle"
    tree_depth: int = 1
    acceptance_threshold: float = 0.5
    calibration_data: str = "c4"
    quantize_drafter: bool = False
    drafter_fp4_format: str = "e2m1"

    def __post_init__(self) -> None:
        """Validate configuration parameters after initialization."""
        # Use module-level constants from experiments.py
        # (DRAFTER_TYPES, CALIBRATION_DATASETS, VALID_FP4_FORMATS are defined at module level)

        if self.drafter_type not in DRAFTER_TYPES:
            msg = f"drafter_type must be one of {DRAFTER_TYPES}, got {self.drafter_type}"
            raise ValueError(msg)

        if not 1 <= self.tree_depth <= 5:
            msg = f"tree_depth must be between 1 and 5, got {self.tree_depth}"
            raise ValueError(msg)

        if not 0.5 <= self.acceptance_threshold <= 1.0:
            msg = (
                f"acceptance_threshold must be between 0.5 and 1.0, "
                f"got {self.acceptance_threshold}"
            )
            raise ValueError(msg)

        if self.calibration_data not in CALIBRATION_DATASETS:
            msg = (
                f"calibration_data must be one of {CALIBRATION_DATASETS}, "
                f"got {self.calibration_data}"
            )
            raise ValueError(msg)

        if self.quantize_drafter and self.drafter_fp4_format not in VALID_FP4_FORMATS:
            msg = (
                f"drafter_fp4_format must be one of {VALID_FP4_FORMATS} "
                f"when quantize_drafter=True, got {self.drafter_fp4_format}"
            )
            raise ValueError(msg)

    def speedup_estimate(self) -> float:
        """Estimate speedup factor based on configuration.

        Returns:
            Estimated speedup multiplier. Deeper trees and lower thresholds
            give higher speedup but potentially lower quality.
        """

        base = 1.0 + 0.15 * self.tree_depth
        threshold_factor = 1.0 / self.acceptance_threshold
        quant_factor = 1.3 if self.quantize_drafter else 1.0
        drafter_factor = {"eagle": 1.0, "medusa": 1.2, "tiny_llama": 1.1}[self.drafter_type]
        return base * threshold_factor * quant_factor * drafter_factor

    def quality_estimate(self) -> float:
        """Estimate quality (inverse PPL loss) based on configuration.

        Returns:
            Estimated quality metric. Higher is better (closer to autoregressive).
        """
        threshold_penalty = (1.1 - self.acceptance_threshold) ** 2
        quant_penalty = 0.1 if self.quantize_drafter else 0.0
        drafter_penalty = {"eagle": 0.0, "medusa": 0.05, "tiny_llama": 0.1}[self.drafter_type]
        return 1.0 - threshold_penalty - quant_penalty - drafter_penalty


# =============================================================================
# Search Space Generation (constants moved here from experiments.py)
# =============================================================================

# Moved from priml/baselines/inference/experiments.py
DRAFTER_TYPES = ["eagle", "medusa", "tiny_llama"]
"""Valid drafter types for speculative decoding configurations."""

CALIBRATION_DATASETS = ["c4", "wikitext", "sharegpt", "ultrachat"]
"""Valid calibration datasets for experiment configuration."""

VALID_FP4_FORMATS = ["e2m1", "nvfp4_block16"]
"""Valid FP4 quantization formats."""


def _generate_configs() -> list[SpeculativeDecodingConfig]:
    """Generate the full configuration set for exp004.

    The search space combines:
        - 3 drafter types: eagle, medusa, tiny_llama
        - 5 tree depths: 1, 2, 3, 4, 5
        - 4 acceptance threshold values: 0.5, 0.75, 0.9, 1.0
        - 4 calibration datasets: c4, wikitext, sharegpt, ultrachat
        - 2 quantize_drafter settings: True, False

    The drafter_fp4_format is derived from quantize_drafter:
        - When quantize_drafter=False: format is e2m1
        - When quantize_drafter=True: format is nvfp4_block16

    Effective config count: 3 × 5 × 4 × 4 × 2 = 480 configurations.

    Returns:
        List of SpeculativeDecodingConfig objects.
    """
    configs: list[SpeculativeDecodingConfig] = []

    # Acceptance thresholds: 0.5, 0.75, 0.9, 1.0
    # (spanning lenient to strict, covering the key tradeoff points)
    acceptance_thresholds = [0.5, 0.75, 0.9, 1.0]

    for drafter_type in DRAFTER_TYPES:
        for tree_depth in range(1, 6):
            for acceptance_threshold in acceptance_thresholds:
                for calib_data in CALIBRATION_DATASETS:
                    for quantize in [True, False]:
                        # fp4_format is derived from quantize_drafter:
                        # - quantize_drafter=False → e2m1
                        # - quantize_drafter=True → nvfp4_block16
                        fp4_format = "e2m1" if not quantize else "nvfp4_block16"
                        config = SpeculativeDecodingConfig(
                            drafter_type=drafter_type,
                            tree_depth=tree_depth,
                            acceptance_threshold=acceptance_threshold,
                            calibration_data=calib_data,
                            quantize_drafter=quantize,
                            drafter_fp4_format=fp4_format,
                        )
                        configs.append(config)

    return configs


# =============================================================================
# Experiment Configuration Generators
# =============================================================================

def exp004() -> dict[str, Any]:
    """Generate exp004 experiment configuration (480 configs for FP4 speculative decoding).

    This is the main experiment configuration for the FP4 speculative decoding
    search space. It generates 480 configurations varying:
        - drafter_type: eagle, medusa, tiny_llama
        - tree_depth: 1-5
        - acceptance_threshold: 0.5-1.0
        - calibration_data: c4, wikitext, sharegpt, ultrachat
        - quantize_drafter: True/False
        - drafter_fp4_format: e2m1, nvfp4_block16

    Returns:
        Dictionary with experiment metadata and config list.
    """
    configs = _generate_configs()
    return {
        "experiment": "exp004",
        "description": "FP4 fused Triton kernel + Speculative Decoding search space",
        "num_configs": len(configs),
        "configs": configs,
        "search_space_params": {
            "drafter_types": DRAFTER_TYPES,
            "tree_depths": list(range(1, 6)),
            "acceptance_thresholds": [t / 10.0 for t in range(5, 11)],
            "calibration_datasets": CALIBRATION_DATASETS,
            "quantize_drafter_options": [True, False],
            "fp4_formats": VALID_FP4_FORMATS,
        },
    }


def exp004_smoke() -> dict[str, Any]:
    """Smoke test configuration for exp004 (quick CI verification).

    Returns a minimal configuration set (6 configs) for fast CI validation.
    Used in continuous integration to verify the experiment pipeline works
    without running the full 480-config search.

    Returns:
        Dictionary with minimal experiment configuration.
    """
    configs = [
        SpeculativeDecodingConfig(
            drafter_type="eagle",
            tree_depth=1,
            acceptance_threshold=0.75,
            calibration_data="c4",
            quantize_drafter=False,
            drafter_fp4_format="e2m1",
        ),
        SpeculativeDecodingConfig(
            drafter_type="eagle",
            tree_depth=3,
            acceptance_threshold=0.8,
            calibration_data="wikitext",
            quantize_drafter=True,
            drafter_fp4_format="nvfp4_block16",
        ),
        SpeculativeDecodingConfig(
            drafter_type="medusa",
            tree_depth=2,
            acceptance_threshold=0.7,
            calibration_data="sharegpt",
            quantize_drafter=False,
            drafter_fp4_format="e2m1",
        ),
        SpeculativeDecodingConfig(
            drafter_type="tiny_llama",
            tree_depth=4,
            acceptance_threshold=0.5,
            calibration_data="ultrachat",
            quantize_drafter=True,
            drafter_fp4_format="nvfp4_block16",
        ),
        SpeculativeDecodingConfig(
            drafter_type="eagle",
            tree_depth=5,
            acceptance_threshold=1.0,
            calibration_data="c4",
            quantize_drafter=False,
            drafter_fp4_format="e2m1",
        ),
        SpeculativeDecodingConfig(
            drafter_type="medusa",
            tree_depth=1,
            acceptance_threshold=0.5,
            calibration_data="wikitext",
            quantize_drafter=True,
            drafter_fp4_format="nvfp4_block16",
        ),
    ]
    return {
        "experiment": "exp004_smoke",
        "description": "FP4 speculative decoding smoke test (6 configs)",
        "num_configs": len(configs),
        "configs": configs,
    }


# =============================================================================
# Experiment Registry
# =============================================================================

ALL_EXPERIMENTS: dict[str, Any] = {
    "exp004": exp004,
    "exp004_smoke": exp004_smoke,
}

DEFAULT_EXPERIMENT = "exp004_smoke"