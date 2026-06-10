import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from utils.tex_text import escape_tex_text


def test_escape_tex_text_preserves_angle_brackets_as_visible_symbols():
    assert escape_tex_text("<1%") == r"$<$1\%"
    assert escape_tex_text("a > b") == r"a $>$ b"
