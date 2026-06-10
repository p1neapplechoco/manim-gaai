from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"
SVG_DIR = ASSETS_DIR / "svgs"
IMAGE_DIR = ASSETS_DIR / "images"

WHITE = "#F5F5F5"
BG = "#000000"
ACCENT = "#4FC3F7"
GOLD = "#FFD54F"
SEPIA = "#C8A96E"
SEPIA_DARK = "#0D0900"
DIM = "#8A7676"
DIM2 = "#615B5B"
RED = "#FF5252"
GREEN = "#66BB6A"
PURPLE = "#B39DDB"
ORANGE = "#FFB74D"
TEAL = "#4DB6AC"
PINK = "#F48FB1"


def svg_path(filename):
    return SVG_DIR / filename


def image_path(filename):
    return IMAGE_DIR / filename
