# manim-gaai

Animated video series on **Generalist Agent AI**, built with [Manim](https://www.manim.community/).

This project produces a set of explanatory animations covering the key ideas presented in the
[CVPR 2024 Tutorial on Generalist Agent AI](https://multimodalagentai.github.io/).
The repository is organized as a monorepo with three independent talks, each with its own
scenes, assets, and planning materials.

## Talks

| Talk | Title | Speaker | Scenes |
|------|-------|---------|--------|
| 1 | From Language Models to Generalist Agents | -- | `talk1/src/scene_*.py` |
| 2 | Multimodal Foundation Models and Visual Grounding | Yong Jae Lee | `talk2/src/Scene*_vi.py` |
| 3 | Agent Robotics: Learning-from-Observation | Katsushi Ikeuchi | `talk3/src/chapter*_v5.py` |

## Project Structure

```
manim-gaai/
  talk1/
    src/
      scene_1.py ... scene_12.py       Scene definitions
      scene_talk1_title.py              Title card
      utils/                            Shared utilities (theme, compat, text)
    assets/
      images/                           Static image assets
      svgs/                             SVG icons and illustrations
    project/                            Kdenlive project files

  talk2/
    src/
      Scene1_vi.py ... Scene6_vi.py     Scene definitions
    assets/                             Image assets (per-scene subdirectories)
    script/                             Narrative scripts (markdown)
    inputs/                             PDF slide deck

  talk3/
    src/
      v5_common.py                      Shared base scene and design system
      chapter01_v5.py ... chapter09_v5.py
    planning/                           Storyboards, narrations, deck maps
    inputs/                             PDF slide deck

  scripts/
    render_all_4k.sh                    Batch-render all scenes in 4K
```

## Prerequisites

- Python 3.10 or later
- [Manim Community Edition](https://docs.manim.community/en/stable/installation.html)
- A working LaTeX distribution (required by Talk 1's Tex-based text renderer)
- FFmpeg (bundled with most Manim installations)

A Conda environment named `gaa-manim` is used in this project:

```bash
conda activate gaa-manim
```

## Rendering

### Single scene

```bash
# Talk 1 -- low quality preview
manim -ql talk1/src/scene_1.py IntroductionGAA

# Talk 2 -- high quality
manim -qh talk2/src/Scene1_vi.py Scene1

# Talk 3 -- 4K production
manim -qk talk3/src/chapter02_v5.py Chapter02V5
```

### All scenes

Use the batch script to render every scene at 4K:

```bash
bash scripts/render_all_4k.sh
```

Render a single talk:

```bash
bash scripts/render_all_4k.sh --talk 1
bash scripts/render_all_4k.sh --talk 2
bash scripts/render_all_4k.sh --talk 3
```

Pass `--dry-run` to preview commands without executing. Set `MANIM_BIN` to
override the default Manim executable:

```bash
MANIM_BIN=/path/to/manim bash scripts/render_all_4k.sh --talk 2
```

Rendered videos are written to `talk*/src/media/videos/`.

## Post-Production

Final assembly and editing for Talk 1 is done in [Kdenlive](https://kdenlive.org/).
Project files are located in `talk1/project/`.

## Attribution

The content of these animations is based on the
[CVPR 2024 Tutorial on Generalist Agent AI](https://multimodalagentai.github.io/).
This project is an independent educational visualization and is not affiliated with
the tutorial organizers.

## License

This project is released under the [MIT License](LICENSE).
