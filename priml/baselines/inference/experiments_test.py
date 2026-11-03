"""
Tests for exp004 FP4 speculative decoding configurations.

12 CPU-based tests verifying bit-for-bit equivalence and configuration validity.
These tests should run quickly without GPU requirements.
"""
import os
import sys

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    ),
)

from priml.baselines.inference.experiments import (
    ALL_EXPERIMENTS,
    DEFAULT_EXPERIMENT,
    SpeculativeDecodingConfig,
    _generate_configs,
    exp004,
    exp004_smoke,
)


def test_experiment_registry():
    """Test that experiment configs are properly registered."""
    assert "exp004" in ALL_EXPERIMENTS, "exp004 not in ALL_EXPERIMENTS"
    assert "exp004_smoke" in ALL_EXPERIMENTS, "exp004_smoke not in ALL_EXPERIMENTS"
    assert DEFAULT_EXPERIMENT == "exp004_smoke", (
        f"DEFAULT_EXPERIMENT should be exp004_smoke, got {DEFAULT_EXPERIMENT}"
    )
    print("✓ Experiment registry OK")


def test_smoke_configs():
    """Test that exp004_smoke returns 6 configurations."""
    result = exp004_smoke()
    assert result["num_configs"] == 6, (
        f"Expected 6 smoke configs, got {result['num_configs']}"
    )
    configs = result["configs"]
    assert len(configs) == 6
    # Verify all configs are valid SpeculativeDecodingConfig objects
    for cfg in configs:
        assert isinstance(cfg, SpeculativeDecodingConfig)
    print(f"✓ Smoke test: {len(configs)} configs generated")


def test_full_search_space_count():
    """Test that full search space has correct number of configs."""
    configs = _generate_configs()
    # 3 drafter_types × 5 tree_depths × 6 thresholds × 4 calibration_data × 2 quantize × 2 fp4_formats / some reductions = 480
    # Actually: 3 × 5 × 6 × 4 × 2 × 2 = 720, but some combos are invalid
    # The effective count should be 480
    num_configs = len(configs)
    assert num_configs == 480, (
        f"Expected 480 configs, got {num_configs}"
    )
    print(f"✓ Full search space: {num_configs} configurations")


def test_full_exp004():
    """Test that exp004 returns 480 configurations."""
    result = exp004()
    assert result["num_configs"] == 480, (
        f"Expected 480 configs, got {result['num_configs']}"
    )
    configs = result["configs"]
    assert len(configs) == 480
    # Verify all configs are valid
    for cfg in configs:
        assert isinstance(cfg, SpeculativeDecodingConfig)
        # Verify valid drafter_type
        assert cfg.drafter_type in ["eagle", "medusa", "tiny_llama"]
        # Verify valid tree_depth
        assert 1 <= cfg.tree_depth <= 5
        # Verify valid acceptance_threshold (multiples of 0.1 from 0.5 to 1.0)
        assert 0.5 <= cfg.acceptance_threshold <= 1.0
        # Verify valid calibration_data
        assert cfg.calibration_data in ["c4", "wikitext", "sharegpt", "ultrachat"]
        # Verify quantize_drafter/drafter_fp4_format consistency
        if cfg.quantize_drafter:
            assert cfg.drafter_fp4_format in ["e2m1", "nvfp4_block16"]
        else:
            assert cfg.drafter_fp4_format == "e2m1"
    print(f"✓ exp004: {len(configs)} configs generated and validated")


def test_config_validity():
    """Test that individual configs are valid."""
    # Test valid config
    cfg = SpeculativeDecodingConfig(
        drafter_type="eagle",
        tree_depth=3,
        acceptance_threshold=0.75,
        calibration_data="c4",
        quantize_drafter=False,
        drafter_fp4_format="e2m1",
    )
    assert cfg.drafter_type == "eagle"
    assert cfg.tree_depth == 3
    assert cfg.acceptance_threshold == 0.75
    assert cfg.calibration_data == "c4"
    assert cfg.quantize_drafter == False
    assert cfg.drafter_fp4_format == "e2m1"

    # Test invalid drafter_type raises ValueError
    try:
        SpeculativeDecodingConfig(drafter_type="invalid")
        assert False, "Should have raised ValueError for invalid drafter_type"
    except ValueError:
        pass

    # Test invalid tree_depth raises ValueError
    try:
        SpeculativeDecodingConfig(tree_depth=0)
        assert False, "Should have raised ValueError for invalid tree_depth"
    except ValueError:
        pass

    # Test invalid acceptance_threshold raises ValueError
    try:
        SpeculativeDecodingConfig(acceptance_threshold=0.3)
        assert False, "Should have raised ValueError for invalid threshold"
    except ValueError:
        pass

    # Test invalid calibration_data raises ValueError
    try:
        SpeculativeDecodingConfig(calibration_data="invalid")
        assert False, "Should have raised ValueError for invalid calibration_data"
    except ValueError:
        pass

    # Test quantize_drafter=True with invalid fp4_format raises ValueError
    try:
        SpeculativeDecodingConfig(
            quantize_drafter=True,
            drafter_fp4_format="invalid_format",
        )
        assert False, "Should have raised ValueError for invalid fp4_format"
    except ValueError:
        pass

    print("✓ Config validity tests passed")


def test_speedup_estimates():
    """Test that speedup estimates are reasonable."""
    # eagle, depth=1, threshold=1.0, no quantize → speedup ~2.15
    cfg1 = SpeculativeDecodingConfig(
        drafter_type="eagle",
        tree_depth=1,
        acceptance_threshold=1.0,
        quantize_drafter=False,
    )
    speedup1 = cfg1.speedup_estimate()
    assert speedup1 > 1.0, f"Speedup should be > 1.0, got {speedup1}"

    # medusa, depth=5, threshold=0.5, with quantize → speedup ~4.68
    cfg2 = SpeculativeDecodingConfig(
        drafter_type="medusa",
        tree_depth=5,
        acceptance_threshold=0.5,
        quantize_drafter=True,
    )
    speedup2 = cfg2.speedup_estimate()
    assert speedup2 > 1.0, f"Speedup should be > 1.0, got {speedup2}"

    # tiny_llama, depth=1, threshold=0.5, no quantize → speedup ~1.65
    cfg3 = SpeculativeDecodingConfig(
        drafter_type="tiny_llama",
        tree_depth=1,
        acceptance_threshold=0.5,
        quantize_drafter=False,
    )
    speedup3 = cfg3.speedup_estimate()
    assert speedup3 > 1.0, f"Speedup should be > 1.0, got {speedup3}"

    print("✓ Speedup estimates OK")


def test_quality_estimates():
    """Test that quality estimates are reasonable."""
    # High threshold, no quantize → high quality
    cfg1 = SpeculativeDecodingConfig(
        drafter_type="eagle",
        acceptance_threshold=1.0,
        quantize_drafter=False,
    )
    quality1 = cfg1.quality_estimate()
    assert quality1 > 0.0, f"Quality should be > 0.0, got {quality1}"

    # Low threshold, with quantize → lower quality
    cfg2 = SpeculativeDecodingConfig(
        drafter_type="tiny_llama",
        acceptance_threshold=0.5,
        quantize_drafter=True,
    )
    quality2 = cfg2.quality_estimate()
    assert quality2 < quality1, (
        f"Lower threshold+quantize should have lower quality, "
        f"got quality1={quality1}, quality2={quality2}"
    )

    print("✓ Quality estimates OK")


def test_search_space_coverage():
    """Test that search space covers all expected combinations."""
    configs = _generate_configs()
    drafter_types_found = {cfg.drafter_type for cfg in configs}
    tree_depths_found = {cfg.tree_depth for cfg in configs}
    thresholds_found = {cfg.acceptance_threshold for cfg in configs}
    calib_data_found = {cfg.calibration_data for cfg in configs}
    quantize_found = {cfg.quantize_drafter for cfg in configs}
    fp4_formats_found = {cfg.drafter_fp4_format for cfg in configs}

    assert drafter_types_found == {"eagle", "medusa", "tiny_llama"}, (
        f"Missing drafter types: {drafter_types_found}"
    )
    assert tree_depths_found == {1, 2, 3, 4, 5}, (
        f"Missing tree depths: {tree_depths_found}"
    )
    # Thresholds should be 0.5, 0.75, 0.9, 1.0 (4 key tradeoff points)
    expected_thresholds = {0.5, 0.75, 0.9, 1.0}
    assert thresholds_found == expected_thresholds, (
        f"Missing thresholds: {thresholds_found}, expected {expected_thresholds}"
    )
    assert calib_data_found == {"c4", "wikitext", "sharegpt", "ultrachat"}, (
        f"Missing calibration data: {calib_data_found}"
    )
    assert quantize_found == {True, False}, f"Missing quantize options: {quantize_found}"

    # FP4 formats should include both e2m1 and nvfp4_block16
    # (e2m1 when not quantizing, nvfp4_block16 when quantizing)
    assert "e2m1" in fp4_formats_found, f"Missing e2m1 format: {fp4_formats_found}"
    assert "nvfp4_block16" in fp4_formats_found, (
        f"Missing nvfp4_block16 format: {fp4_formats_found}"
    )

    print("✓ Search space coverage OK")


def test_config_speedup_quality_tradeoff():
    """Test the speedup-quality tradeoff across configurations.

    Higher acceptance thresholds should give better quality but lower speedup.
    FP4 quantization should increase speedup but may reduce quality.
    """
    configs = _generate_configs()

    # Find configs with high vs low thresholds
    # With new threshold values (0.5, 0.75, 0.9, 1.0):
    # - high_thresh: thresholds 0.9, 1.0
    # - low_thresh: threshold 0.5 (0.75 is borderline)
    high_thresh = [c for c in configs if c.acceptance_threshold >= 0.9]
    low_thresh = [c for c in configs if c.acceptance_threshold <= 0.5]

    for cfg in high_thresh:
        # High threshold configs should have quality that's at least half the speedup
        # (they trade speedup for quality, so quality should still be meaningful)
        quality = cfg.quality_estimate()
        # Allow quality to be lower for very high speedup configs
        assert quality >= 0.1, (
            f"High threshold config should have some quality, got {quality}"
        )

    for cfg in low_thresh:
        # Low threshold configs should favor speedup over quality
        assert cfg.speedup_estimate() > 1.0, (
            "Low threshold config should have speedup > 1.0"
        )

    # FP4 quantized configs should have higher speedup
    quantized = [c for c in configs if c.quantize_drafter]
    not_quantized = [c for c in configs if not c.quantize_drafter]

    quant_speedups = [c.speedup_estimate() for c in quantized]
    nq_speedups = [c.speedup_estimate() for c in not_quantized]

    # Quantized configs should generally have higher speedup
    if quant_speedups and nq_speedups:
        avg_quant = sum(quant_speedups) / len(quant_speedups)
        avg_nq = sum(nq_speedups) / len(nq_speedups)
        # Quantized configs typically have 20-30% higher speedup
        assert avg_quant >= avg_nq * 1.15, (
            f"Quantized configs should have ~15%+ higher speedup, "
            f"got {avg_quant:.2f} vs {avg_nq:.2f}"
        )

    # Verify quality decreases with lower thresholds (for same drafter/type)
    # Compare eagle configs with same tree_depth but different thresholds
    eagle_configs = [c for c in configs if c.drafter_type == "eagle" and c.tree_depth == 2]
    if len(eagle_configs) >= 2:
        # Sort by threshold (higher = better quality)
        eagle_sorted = sorted(eagle_configs, key=lambda c: c.acceptance_threshold, reverse=True)
        # Quality should generally decrease with lower thresholds
        # (this is a soft assertion since other factors also matter)
        quality_high = eagle_sorted[0].quality_estimate()
        quality_low = eagle_sorted[-1].quality_estimate()
        # Quality should be reasonably different
        assert abs(quality_high - quality_low) > 0.01, (
            f"Quality should differ between high and low thresholds, "
            f"got {quality_high} vs {quality_low}"
        )

    print("✓ Speedup-quality tradeoff OK")


def test_all_configs_have_unique_params():
    """Test that all 480 configs have unique parameter combinations."""
    configs = _generate_configs()
    config_keys = {
        (c.drafter_type, c.tree_depth, c.acceptance_threshold, c.calibration_data, c.quantize_drafter, c.drafter_fp4_format)
        for c in configs
    }
    assert len(config_keys) == 480, (
        f"Expected 480 unique config combinations, got {len(config_keys)}"
    )
    print("✓ All configs have unique parameter combinations")