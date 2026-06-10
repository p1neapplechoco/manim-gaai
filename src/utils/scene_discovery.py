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
    root = Path(root)
    scenes = []
    for path in sorted((root / "src").glob("scene_*.py"), key=natural_key):
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
