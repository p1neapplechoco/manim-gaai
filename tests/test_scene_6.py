import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "scene_6.py"
pytest.importorskip("manim")


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_6_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.config.media_dir = "/tmp/manim-gaai-test-media"
    return module


def test_scaling_factors_match_narration_values():
    module = load_scene_module()

    factors = {factor.symbol: factor for factor in module.SCALING_FACTORS}

    assert list(factors) == ["N", "D", "C"]
    assert factors["N"].label == "model size"
    assert factors["D"].label == "data"
    assert factors["C"].label == "compute"
    assert factors["N"].alpha == pytest.approx(0.076)
    assert factors["D"].alpha == pytest.approx(0.095)
    assert factors["C"].alpha == pytest.approx(0.050)
    assert factors["N"].constant_tex == r"8.8 \times 10^{13}"
    assert factors["D"].constant_tex == r"5.4 \times 10^{13}"
    assert factors["C"].constant_tex == r"3.1 \times 10^8"


def test_factor_panels_are_compact_visual_groups():
    module = load_scene_module()

    panels = module.make_factor_panels()

    assert len(panels) == 3
    assert panels.width < 10
    assert panels.height < 4
    assert all(len(panel) >= 3 for panel in panels)


def test_loss_curve_points_descend_as_scale_increases():
    module = load_scene_module()

    points = module.loss_curve_points()

    assert len(points) >= 5
    assert all(points[i][0] < points[i + 1][0] for i in range(len(points) - 1))
    assert all(points[i][1] > points[i + 1][1] for i in range(len(points) - 1))
