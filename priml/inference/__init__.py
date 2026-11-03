"""
Inference module for speculative decoding and FP4 quantization.

Exports:
    - EAGLE, Medusa speculative decoding architectures
    - TokenTreeVerifier for token tree acceptance
    - FP4Quantizer for FP4 quantization (e2m1, NVFP4)
    - Experiment configuration generators (exp004, exp004_smoke)
    - Testing
"""
from __future__ import annotations

# Core exports from speculative.py
from .speculative import (
    EAGLE,
    FP4Quantizer,
    Medusa,
    TokenTreeVerifier,
    speculative_decoding_search_space,
)

# Experiment configs from baselines.inference.experiments
# Import directly to avoid circular dependencies with priml.inference package
try:
    from priml.baselines.inference.experiments import (
        ALL_EXPERIMENTS,
        DEFAULT_EXPERIMENT,
        exp004,
        exp004_smoke,
    )
except ImportError:
    # Fallback for when baselines not available
    exp004 = None  # type: ignore
    exp004_smoke = None  # type: ignore
    ALL_EXPERIMENTS = {}  # type: ignore
    DEFAULT_EXPERIMENT = "exp004_smoke"  # type: ignore

# Testing
from .experiments_test import test_verification_equivalence_fp32

__all__ = [
    "ALL_EXPERIMENTS",
    "DEFAULT_EXPERIMENT",
    "EAGLE",
    "FP4Quantizer",
    "Medusa",
    "TokenTreeVerifier",
    "exp004",
    "exp004_smoke",
    "speculative_decoding_search_space",
    "test_verification_equivalence_fp32",
]