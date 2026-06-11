#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIM_BIN="${MANIM_BIN:-manim}"
QUALITY_FLAG="-qk"
DRY_RUN=0
TALK_FILTER=""

usage() {
    printf 'Usage: %s [--dry-run] [--talk 1|2|3]\n' "$(basename "$0")"
    printf '\n'
    printf 'Renders every Scene class across all talks with Manim 4K quality (-qk).\n'
    printf 'Set MANIM_BIN=/path/to/manim to use a custom Manim executable.\n'
    printf '\n'
    printf 'Options:\n'
    printf '  --talk N      Render only talk N (1, 2, or 3)\n'
    printf '  --dry-run     Print commands without executing\n'
}

while (($#)); do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            ;;
        --talk)
            shift
            TALK_FILTER="$1"
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

render_scene() {
    local scene_file="$1"
    local scene_class="$2"
    local command=("$MANIM_BIN" "$QUALITY_FLAG" "$scene_file" "$scene_class")

    printf '%q' "${command[0]}"
    for arg in "${command[@]:1}"; do
        printf ' %q' "$arg"
    done
    printf '\n'

    if (( ! DRY_RUN )); then
        "${command[@]}"
    fi
}

# ── Talk 1 ───────────────────────────────────────────────────────────
if [[ -z "$TALK_FILTER" || "$TALK_FILTER" == "1" ]]; then
    for f in "$ROOT_DIR"/talk1/src/scene_*.py; do
        [[ -f "$f" ]] || continue
        while IFS= read -r class_name; do
            render_scene "$f" "$class_name"
        done < <(python3 -c "
import ast, sys
tree = ast.parse(open('$f').read())
for node in tree.body:
    if isinstance(node, ast.ClassDef):
        for base in node.bases:
            name = getattr(base, 'id', getattr(base, 'attr', ''))
            if name.endswith('Scene'):
                print(node.name)
                break
")
    done
fi

# ── Talk 2 ───────────────────────────────────────────────────────────
if [[ -z "$TALK_FILTER" || "$TALK_FILTER" == "2" ]]; then
    for f in "$ROOT_DIR"/talk2/src/Scene*_vi.py; do
        [[ -f "$f" ]] || continue
        while IFS= read -r class_name; do
            render_scene "$f" "$class_name"
        done < <(python3 -c "
import ast, sys
tree = ast.parse(open('$f').read())
for node in tree.body:
    if isinstance(node, ast.ClassDef):
        for base in node.bases:
            name = getattr(base, 'id', getattr(base, 'attr', ''))
            if name.endswith('Scene'):
                print(node.name)
                break
")
    done
fi

# ── Talk 3 ───────────────────────────────────────────────────────────
if [[ -z "$TALK_FILTER" || "$TALK_FILTER" == "3" ]]; then
    for f in "$ROOT_DIR"/talk3/src/chapter*_v5.py; do
        [[ -f "$f" ]] || continue
        while IFS= read -r class_name; do
            render_scene "$f" "$class_name"
        done < <(python3 -c "
import ast, sys
tree = ast.parse(open('$f').read())
for node in tree.body:
    if isinstance(node, ast.ClassDef):
        for base in node.bases:
            name = getattr(base, 'id', getattr(base, 'attr', ''))
            if name.endswith('Scene'):
                print(node.name)
                break
")
    done
fi
