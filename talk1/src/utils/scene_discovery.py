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


def discover_scene_classes(root="."):
    """Discover Scene subclasses in all talk*/src/scene_*.py files."""
    root = Path(root)
    scenes = []

    # Talk 1: talk1/src/scene_*.py
    for path in sorted(root.glob("talk1/src/scene_*.py"), key=natural_key):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if any(base_name(base).endswith("Scene") for base in node.bases):
                scenes.append((path.relative_to(root).as_posix(), node.name))

    # Talk 2: talk2/src/Scene*_vi.py
    for path in sorted(root.glob("talk2/src/Scene*_vi.py"), key=natural_key):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if any(base_name(base).endswith("Scene") for base in node.bases):
                scenes.append((path.relative_to(root).as_posix(), node.name))

    # Talk 3: talk3/src/chapter*_v5.py
    for path in sorted(root.glob("talk3/src/chapter*_v5.py"), key=natural_key):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if any(base_name(base).endswith("Scene") for base in node.bases):
                scenes.append((path.relative_to(root).as_posix(), node.name))

    return scenes


def main():
    for scene_file, scene_class in discover_scene_classes(Path.cwd()):
        print(f"{scene_file} {scene_class}")


if __name__ == "__main__":
    main()
