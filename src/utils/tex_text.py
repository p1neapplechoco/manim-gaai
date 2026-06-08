import sys
from pathlib import Path

_LATEX_ESCAPES = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}

_UNICODE_TO_TEX = {
    "\n": r"\\",
    "–": "--",
    "—": "--",
    "…": r"\ldots{}",
    "‘": "`",
    "’": "'",
    "“": "``",
    "”": "''",
    "→": r"$\rightarrow$",
    "←": r"$\leftarrow$",
    "⇒": r"$\Rightarrow$",
    "⇔": r"$\Leftrightarrow$",
    "×": r"$\times$",
    "÷": r"$\div$",
    "±": r"$\pm$",
    "≤": r"$\leq$",
    "≥": r"$\geq$",
    "≠": r"$\neq$",
    "≈": r"$\approx$",
    "∞": r"$\infty$",
    "π": r"$\pi$",
    "α": r"$\alpha$",
    "β": r"$\beta$",
    "γ": r"$\gamma$",
    "✓": r"$\checkmark$",
    "✗": r"$\times$",
    "🖼": r"\fbox{\phantom{M}}",
}

_PASSTHROUGH_KWARGS = {
    "color",
    "font_size",
    "height",
    "width",
    "fill_opacity",
    "stroke_width",
    "stroke_opacity",
    "tex_template",
    "tex_environment",
    "arg_separator",
    "substrings_to_isolate",
    "tex_to_color_map",
    "organize_left_to_right",
}


def escape_tex_text(text):
    """Escape plain text so Manim's Tex can render it as regular prose."""
    pieces = []
    for char in str(text):
        if char in _UNICODE_TO_TEX:
            pieces.append(_UNICODE_TO_TEX[char])
        else:
            pieces.append(_LATEX_ESCAPES.get(char, char))
    return "".join(pieces)


def _wants_style(value, name):
    return value is not None and name in str(value).lower()


def _style_tex(text, weight=None, slant=None):
    if _wants_style(slant, "italic") or _wants_style(slant, "oblique"):
        text = r"\textit{" + text + "}"
    if _wants_style(weight, "bold"):
        text = r"\textbf{" + text + "}"
    return text


def _load_tex_class():
    for module_name in ("manim", "manimlib"):
        module = sys.modules.get(module_name)
        tex_class = getattr(module, "Tex", None) if module is not None else None
        if tex_class is not None:
            return tex_class

    cmd = Path(sys.argv[0]).name.lower()
    if "manimgl" in cmd:
        from manimlib import Tex
    else:
        from manim import Tex
    return Tex


def Text(*strings, **kwargs):
    """Compatibility wrapper that renders normal Text calls through Tex."""
    weight = kwargs.pop("weight", None)
    slant = kwargs.pop("slant", None)
    tex_escape = kwargs.pop("tex_escape", True)
    raw_tex = kwargs.pop("raw_tex", False)
    if raw_tex:
        tex_escape = False
    kwargs.pop("font", None)
    kwargs.pop("line_spacing", None)
    tex_kwargs = {
        key: value for key, value in kwargs.items() if key in _PASSTHROUGH_KWARGS
    }
    tex_strings = tuple(
        _style_tex(
            escape_tex_text(text) if tex_escape else str(text),
            weight=weight,
            slant=slant,
        )
        for text in strings
    )

    return _load_tex_class()(*tex_strings, **tex_kwargs)
