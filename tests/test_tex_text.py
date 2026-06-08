import importlib.util
import sys
import types
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_tex_text_escapes_plain_text_for_latex():
    spec = importlib.util.spec_from_file_location(
        "tex_text_module", SRC / "utils" / "tex_text.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.escape_tex_text('5% of A&B_cost #1') == (
        r"5\% of A\&B\_cost \#1"
    )
    assert module.escape_tex_text("line 1\nline 2") == r"line 1\\line 2"
    assert module.escape_tex_text("✓ → × — …") == (
        r"$\checkmark$ $\rightarrow$ $\times$ -- \ldots{}"
    )


def test_text_wrapper_uses_loaded_tex_class(monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "tex_text_module", SRC / "utils" / "tex_text.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class FakeTex:
        def __init__(self, *strings, **kwargs):
            self.strings = strings
            self.kwargs = kwargs

    fake_manim = types.SimpleNamespace(Tex=FakeTex)
    monkeypatch.setitem(sys.modules, "manim", fake_manim)

    text = module.Text("87%", font_size=72, color="gold", weight="bold")

    assert isinstance(text, FakeTex)
    assert text.strings == (r"\textbf{87\%}",)
    assert text.kwargs == {"font_size": 72, "color": "gold"}


def test_text_wrapper_can_pass_raw_tex(monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "tex_text_module", SRC / "utils" / "tex_text.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class FakeTex:
        def __init__(self, *strings, **kwargs):
            self.strings = strings
            self.kwargs = kwargs

    fake_manim = types.SimpleNamespace(Tex=FakeTex)
    monkeypatch.setitem(sys.modules, "manim", fake_manim)

    text = module.Text(
        r"$\blacktriangleright$ frame 42",
        font_size=18,
        color="orange",
        tex_escape=False,
    )

    assert text.strings == (r"$\blacktriangleright$ frame 42",)
    assert text.kwargs == {"font_size": 18, "color": "orange"}


@pytest.mark.parametrize("scene_path", sorted(SRC.glob("scene_*.py")))
def test_scenes_shadow_manim_text_with_tex_text(scene_path):
    source = scene_path.read_text()

    assert "from utils.tex_text import Text" in source
    assert source.index("from utils.tex_text import Text") > source.index("import *")
