import importlib.util
import inspect
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "test.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("library_scene_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.config.media_dir = "/tmp/manim-gaai-test-media"
    return module


def test_svg_rect_uses_svg_dimensions_and_center():
    module = load_scene_module()

    rect = module.svg_rect(30, 50, 245, 340, "#123456")
    expected_center = module.svg_point(152.5, 220)

    assert rect.width == pytest.approx(module.scale_px(245))
    assert rect.height == pytest.approx(module.scale_px(340))
    assert rect.get_center()[0] == pytest.approx(expected_center[0])
    assert rect.get_center()[1] == pytest.approx(expected_center[1])


def test_scene_builders_expose_expected_major_parts():
    module = load_scene_module()

    shelves = module.make_shelves()
    lamp = module.make_reading_lamp()
    scene = module.build_library_scene()

    assert len(module.SHELF_ORIGINS) == 3
    assert len(shelves) == 3
    assert lamp.height > module.scale_px(200)
    assert len(scene) == 4


def test_scene_uses_outline_first_entrance_for_main_objects():
    module = load_scene_module()

    construct_source = inspect.getsource(module.LibraryScene.construct)

    assert hasattr(module, "outline_first")
    assert hasattr(module, "make_outline")
    assert "Create" in inspect.getsource(module.outline_first)
    assert "ReplacementTransform" in inspect.getsource(module.outline_first)
    assert "outline_first(shelves" in construct_source
    assert "outline_first(lamp" in construct_source
    assert "FadeIn(shelves" not in construct_source
    assert "FadeIn(lamp" not in construct_source


def test_make_outline_removes_fill_and_adds_visible_stroke():
    module = load_scene_module()

    outline = module.make_outline(module.make_book(42, 375, 16, 57, "#C8314A"))
    pieces = [
        piece
        for piece in outline.family_members_with_points()
        if isinstance(piece, module.VMobject)
    ]

    assert pieces
    assert all(piece.get_fill_opacity() == pytest.approx(0) for piece in pieces)
    assert all(piece.get_stroke_width() > 0 for piece in pieces)


def test_outline_first_handles_nested_vgroups():
    module = load_scene_module()

    animation = module.outline_first(module.make_shelves(), run_time=0.5)

    assert animation.run_time == pytest.approx(0.5)
