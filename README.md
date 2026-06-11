# manim-gaai

Animated video series on **Generalist Agent AI**, built with [Manim](https://www.manim.community/).

This project produces a set of explanatory animations covering the key ideas presented in the
[CVPR 2024 Tutorial on Generalist Agent AI](https://multimodalagentai.github.io/).
Each scene file corresponds to a self-contained segment of the talk, rendered as a
publication-ready video at up to 4K resolution.

## Content

The animations follow the structure of the tutorial, beginning with an opening that
motivates the shift from language models to generalist agents and progressing through
the core concepts of multimodal perception, environment interaction, and autonomous
decision-making.

| Scene file | Topic |
|---|---|
| `scene_1.py` | Opening -- from language models to Generalist Agent AI |
| `scene_2.py` -- `scene_12.py` | Subsequent segments of the tutorial |
| `scene_talk1_title.py` | Talk 1 title card |

## Project Structure

```
manim-gaai/
  assets/
    images/          Static image assets
    svgs/            SVG icons and illustrations (robot, brain, browser, etc.)
  project/           Kdenlive project files for final video editing
  scripts/
    render_all_4k.sh Batch-render all scenes in 4K
  src/
    scene_*.py       Manim scene definitions
    utils/
      manim_compat.py  Compatibility layer for Manim / ManimGL
      tex_text.py      LaTeX-based Text rendering wrapper
      theme.py         Shared color palette and asset path helpers
      artifacts.py     Reusable visual components
      mobjects.py      Custom Mobject definitions
```

## Prerequisites

- Python 3.10 or later
- [Manim Community Edition](https://docs.manim.community/en/stable/installation.html)
- A working LaTeX distribution (required by the `Tex`-based text renderer)
- FFmpeg (bundled with most Manim installations)

A Conda environment named `gaa-manim` is used in this project. Activate it before
running any commands:

```bash
conda activate gaa-manim
```

## Rendering

### Single scene

Render a specific scene at the desired quality level:

```bash
# Low quality preview (480p, 15 fps)
manim -ql src/scene_1.py IntroductionGAA

# High quality (1080p, 60 fps)
manim -qh src/scene_1.py IntroductionGAA

# 4K production quality (2160p, 60 fps)
manim -qk src/scene_1.py IntroductionGAA
```

### All scenes

Use the provided batch script to render every scene at 4K:

```bash
bash scripts/render_all_4k.sh
```

Pass `--dry-run` to preview the commands without executing them. Set `MANIM_BIN` to
override the default Manim executable path:

```bash
MANIM_BIN=/path/to/manim bash scripts/render_all_4k.sh
```

Rendered videos are written to `src/media/videos/`.

## Post-Production

Final assembly and editing is done in [Kdenlive](https://kdenlive.org/). Project files
for each segment are located in the `project/` directory.

## Attribution

The content of these animations is based on the
[CVPR 2024 Tutorial on Generalist Agent AI](https://multimodalagentai.github.io/).
This project is an independent educational visualization and is not affiliated with
the tutorial organizers.

## License

This project is released under the [MIT License](LICENSE).
