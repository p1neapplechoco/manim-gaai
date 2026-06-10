import sys
from pathlib import Path


CMD = Path(sys.argv[0]).name.lower()

if "manimgl" in CMD:
    from manimlib import *  # noqa: F403
else:
    from manim import *  # noqa: F403

from utils.tex_text import Text
