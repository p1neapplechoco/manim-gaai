#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIM_BIN="${MANIM_BIN:-manim}"
QUALITY_FLAG="-qk"
DRY_RUN=0

usage() {
    printf 'Usage: %s [--dry-run]\n' "$(basename "$0")"
    printf '\n'
    printf 'Renders every Scene class in src/scene_*.py with Manim 4K quality (-qk).\n'
    printf 'Set MANIM_BIN=/path/to/manim to use a custom Manim executable.\n'
}

while (($#)); do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf 'Unknown option: %s\n\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
    shift
done

cd "$ROOT_DIR"

if (( ! DRY_RUN )) && ! command -v "$MANIM_BIN" >/dev/null 2>&1; then
    printf 'Could not find Manim executable: %s\n' "$MANIM_BIN" >&2
    printf 'Install Manim or set MANIM_BIN=/path/to/manim.\n' >&2
    exit 127
fi

discover_scenes() {
    python - <<'PY'
import ast
import re
from pathlib import Path


def natural_key(path):
    return [
        int(part) if part.isdigit() else part
        for part in re.split(r"(\d+)", str(path))
    ]


def base_name(base):
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return base.attr
    if isinstance(base, ast.Subscript):
        return base_name(base.value)
    return ""


for path in sorted(Path("src").glob("scene_*.py"), key=natural_key):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if any(base_name(base).endswith("Scene") for base in node.bases):
            print(f"{path} {node.name}")
PY
}

mapfile -t SCENES < <(discover_scenes)

if ((${#SCENES[@]} == 0)); then
    printf 'No Scene classes found in src/scene_*.py\n' >&2
    exit 1
fi

for entry in "${SCENES[@]}"; do
    read -r scene_file scene_class <<<"$entry"
    command=("$MANIM_BIN" "$QUALITY_FLAG" "$scene_file" "$scene_class")
    printf '%q ' "${command[@]}"
    printf '\n'

    if (( ! DRY_RUN )); then
        "${command[@]}"
    fi
done
