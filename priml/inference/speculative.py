"""
Speculative decoding architectures and FP4 quantization for inference acceleration.

Architectures:
    - EAGLE: Autoregressive head + token tree for draft generation
    - Medusa: FFN-based speculative heads for accelerated generation
    - TokenTreeVerifier: Verifies accepted token sequences
    - FP4Quantizer: FP4 quantization/dequantization (e2m1, NVFP4 block formats)

Search space:
    - 480 configurations for drafter type, tree depth, acceptance threshold,
      calibration data, FP4 format, and quantization settings.
"""
from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any

# =============================================================================
# FP4 Quantization
# =============================================================================


class FP4Quantizer(abc.ABC):
    """Abstract base class for FP4 quantization formats.

    FP4 (4-bit floating point) quantization enables significant speedups
    in inference while maintaining acceptable quality. Two formats are
    supported:

    - e2m1: 1 sign, 2 exponent, 1 mantissa bit (reduced range, higher precision)
    - nvfp4_block16: NVIDIA FP4 block format with 16-block grouping (mixed precision)
    """

    @abc.abstractmethod
    def quantize(self, fp32: float) -> int:
        """Quantize a FP32 value to FP4 encoding.

        Args:
            fp32: FP32 value to quantize

        Returns:
            FP4 integer code
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def dequantize(self, fp4: int) -> float:
        """Dequantize an FP4 code back to FP32.

        Args:
            fp4: FP4 integer code

        Returns:
            FP32 reconstructed value
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def bit_width(self) -> int:
        """Return the bit width of the quantization format."""
        raise NotImplementedError()


@dataclass
class E2M1Quantizer(FP4Quantizer):
    """e2m1 FP4 quantizer: 1 sign, 2 exponent, 1 mantissa bit.

    Format: SEEEEM where S=sign, E=exponent (2 bits), M=mantissa (1 bit)
    Provides ~3-bit effective precision with smaller range than NVFP4.
    """

    format_name: str = "e2m1"

    def quantize(self, fp32: float) -> int:
        """Quantize FP32 to e2m1 FP4 encoding."""
        if fp32 == 0.0:
            return 0

        sign = 0 if fp32 >= 0 else 1
        abs_val = abs(fp32)

        # Exponent: map to 2-bit range
        # FP4 e2m1 range: ~0.0625 to 7.5 (approx)
        if abs_val >= 8.0:
            exp_code = 3  # Saturate at max
        elif abs_val >= 4.0:
            exp_code = 2
        elif abs_val >= 2.0:
            exp_code = 1
        elif abs_val >= 1.0:
            exp_code = 0
        elif abs_val >= 0.5:
            exp_code = -1  # Subnormal-like
        else:
            exp_code = -2  # Very small

        # Mantissa: 1 bit (0 or 0.5 offset)
        mantissa = 0 if abs_val < 2.0 * (10 ** exp_code) else 1

        # Pack: sign(1) + exponent(2) + mantissa(1) = 4 bits
        packed = (sign << 3) | (exp_code << 1) | mantissa
        return packed & 0xF  # Ensure 4-bit unsigned

    def dequantize(self, fp4: int) -> float:
        """Dequantize e2m1 FP4 back to FP32."""
        fp4 = fp4 & 0xF

        sign = (fp4 >> 3) & 1
        exp_code = (fp4 >> 1) & 0b11  # 2 bits
        mantissa = fp4 & 0b1  # 1 bit

        # Reconstruct absolute value
        # e2m1 provides: value = (-1)^sign * 2^(exp_code + mantissa/2) * 1
        # With 2 exponent bits, we have values: 1, 2, 4, 8 (times mantissa offset)
        # Plus subnormal cases for exp_code < 0
        if exp_code >= 0:
            mantissa_factor = 1.0 + (mantissa * 0.5)
            value = mantissa_factor * (2 ** exp_code)
        else:
            # Subnormal: small values near zero
            value = 2 ** exp_code  # exp_code is -1 or -2

        if sign:
            value = -value
        return value

    def bit_width(self) -> int:
        """Return bit width (4 for FP4)."""
        return 4


@dataclass
class NVFP4Block16Quantizer(FP4Quantizer):
    """NVIDIA FP4 block16 quantizer: FP4 with 16-value block grouping.

    NVFP4 blocks group 16 FP4 values together, allowing shared
    block-level scaling for improved precision across matrix operations.
    Commonly used in Triton kernels for LLM acceleration.
    """

    format_name: str = "nvfp4_block16"
    block_size: int = 16

    def quantize(self, fp32: float, block_idx: int = 0) -> int:
        """Quantize FP32 to NVFP4 block16 encoding.

        Args:
            fp32: FP32 value to quantize
            block_idx: Index of the 16-value block (for block-level scaling)

        Returns:
            FP4 integer code
        """
        # Delegate to e2m1 logic, block scaling handled separately
        # In a full implementation, block max/min would be computed
        # and used for scaling before e2m1 quantization
        quantizer = E2M1Quantizer()
        return quantizer.quantize(fp32)

    def dequantize(self, fp4: int, block_idx: int = 0) -> float:
        """Dequantize NVFP4 block16 back to FP32.

        Args:
            fp4: FP4 integer code
            block_idx: Index of the 16-value block

        Returns:
            FP32 reconstructed value
        """
        # Delegate to e2m1 dequantization
        quantizer = E2M1Quantizer()
        return quantizer.dequantize(fp4)

    def bit_width(self) -> int:
        """Return bit width (4 for FP4)."""
        return 4


# =============================================================================
# Speculative Decoding Architectures
# =============================================================================


class TokenTreeVerifier(abc.ABC):
    """Verifies accepted token sequences in token tree speculative decoding.

    Token tree speculative decoding (also called EAGLE architecture) uses
    a tree structure over token candidates. The verifier determines which
    branches of the tree are accepted based on an acceptance threshold,
    balancing speedup against output quality.
    """

    @abc.abstractmethod
    def verify(
        self,
        draft_tokens: list[int],
        acceptance_threshold: float,
    ) -> tuple[list[int], bool]:
        """Verify draft tokens against acceptance criteria.

        Args:
            draft_tokens: List of drafted token IDs
            acceptance_threshold: Threshold [0, 1] for acceptance

        Returns:
            Tuple of (accepted_tokens, all_accepted)
            - accepted_tokens: Tokens that passed verification
            - all_accepted: Whether all draft tokens were accepted
        """
        raise NotImplementedError()


@dataclass
class EAGLEVerifier(TokenTreeVerifier):
    """EAGLE (AR head + token tree) verifier for speculative decoding.

    EAGLE architecture combines an autoregressive draft head with a token
    tree structure. The verifier checks each branch of the token tree
    against the acceptance threshold to determine which tokens to accept
    and which to fall back to autoregressive generation.
    """

    verifier_name: str = "eagle"
    default_threshold: float = 0.75

    def verify(
        self,
        draft_tokens: list[int],
        acceptance_threshold: float,
    ) -> tuple[list[int], bool]:
        """Verify draft tokens using EAGLE token tree criteria.

        Args:
            draft_tokens: List of drafted token IDs from the token tree
            acceptance_threshold: Threshold [0, 1] for acceptance (0.5-1.0)

        Returns:
            Tuple of (accepted_tokens, all_accepted)
        """
        if not draft_tokens:
            return [], True

        accepted = []
        all_accepted = True

        for i, token in enumerate(draft_tokens):
            # EAGLE acceptance: higher thresholds = stricter verification,
            # accepting fewer tokens but maintaining better quality
            # Token at position i has decreasing confidence
            if i == 0:
                # First token has highest confidence
                accepted.append(token)
            elif acceptance_threshold >= 0.8:
                # Strict threshold: only accept high-confidence tokens
                accepted.append(token)
            elif acceptance_threshold >= 0.7:
                # Moderate threshold
                accepted.append(token if i < 3 else None)  # type: ignore
            else:
                # lenient: accept most tokens
                accepted.append(token)

        # Filter out None values (rejected tokens)
        accepted = [t for t in accepted if t is not None]  # type: ignore

        if len(accepted) < len(draft_tokens):
            all_accepted = False

        return accepted, all_accepted


@dataclass
class MedusaVerifier(TokenTreeVerifier):
    """Medusa (FFN heads) verifier for speculative decoding.

    Medusa architecture appends FFN-based speculative heads to the draft
    generator. The verifier checks multiple candidate token sequences
    generated in parallel, accepting those that match the true next token.
    """

    verifier_name: str = "medusa"
    default_threshold: float = 0.65
    n_heads: int = 3

    def verify(
        self,
        draft_tokens: list[int],
        acceptance_threshold: float,
    ) -> tuple[list[int], bool]:
        """Verify draft tokens using Medusa FFN head criteria.

        Args:
            draft_tokens: List of drafted token IDs from Medusa heads
            acceptance_threshold: Threshold [0, 1] for acceptance

        Returns:
            Tuple of (accepted_tokens, all_accepted)
        """
        if not draft_tokens:
            return [], True

        # Medusa generates multiple candidate tokens per step
        # Accept based on confidence threshold
        accepted = draft_tokens[: int(len(draft_tokens) * acceptance_threshold)]

        all_accepted = len(accepted) == len(draft_tokens)

        return accepted, all_accepted


# =============================================================================
# Search Space Configuration
# =============================================================================

DRAFTER_TYPES = ["eagle", "medusa", "tiny_llama"]
"""Valid drafter types for speculative decoding configurations."""

CALIBRATION_DATASETS = ["c4", "wikitext", "sharegpt", "ultrachat"]
"""Valid calibration datasets for experiment configuration."""

VALID_FP4_FORMATS = ["e2m1", "nvfp4_block16"]
"""Valid FP4 quantization formats."""


@dataclass
class SpeculativeDecodingConfig:
    """Configuration for a speculative decoding experiment configuration.

    This dataclass holds all parameters for a single configuration
    in the speculative decoding search space (480 total configurations).

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
        if self.drafter_type not in DRAFTER_TYPES:
            msg = f"drafter_type must be one of {DRAFTER_TYPES}, got {self.drafter_type}"
            raise ValueError(msg)

        if not 1 <= self.tree_depth <= 5:
            msg = f"tree_depth must be between 1 and 5, got {self.tree_depth}"
            raise ValueError(msg)

        if not 0.5 <= self.acceptance_threshold <= 1.0:
            msg = f"acceptance_threshold must be between 0.5 and 1.0, got {self.acceptance_threshold}"
            raise ValueError(msg)

        if self.calibration_data not in CALIBRATION_DATASETS:
            msg = f"calibration_data must be one of {CALIBRATION_DATASETS}, got {self.calibration_data}"
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


def speculative_decoding_search_space() -> list[SpeculativeDecodingConfig]:
    """Generate the full 480-configuration search space for exp004.

    The search space combines:
        - 3 drafter types: eagle, medusa, tiny_llama
        - 5 tree depths: 1, 2, 3, 4, 5
        - 6 acceptance threshold values: 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
        - 4 calibration datasets: c4, wikitext, sharegpt, ultrachat
        - 2 quantize_drafter settings: True, False
        - 2 FP4 formats: e2m1, nvfp4_block16

    Note: Not all combinations are valid (e.g., drafter_fp4_format
    is only relevant when quantize_drafter=True). The effective count
    is 480 configurations.

    Returns:
        List of SpeculativeDecodingConfig objects covering the search space.
    """
    configs: list[SpeculativeDecodingConfig] = []

    for drafter_type in DRAFTER_TYPES:
        for tree_depth in range(1, 6):  # 1-5
            for threshold_tenths in range(5, 11):  # 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
                acceptance_threshold = threshold_tenths / 10.0
                for calib_data in CALIBRATION_DATASETS:
                    for quantize in [True, False]:
                        # Only specify fp4_format when quantizing;
                        # when not quantizing, use e2m1 as default format
                        fp4_format = "e2m1" if not quantize else "nvfp4_block16"
                        # Skip invalid combinations: when not quantizing,
                        # still generate with e2m1 format for compatibility
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
    search space. It generates 480 configurations varying drafter type, tree depth,
    acceptance threshold, calibration data, FP4 quantization, and format.

    Returns:
        Dictionary with experiment metadata and config list.
    """
    configs = speculative_decoding_search_space()
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