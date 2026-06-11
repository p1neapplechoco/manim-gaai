from utils.manim_compat import *
from utils.theme import *


# Steel-blue palette (inspired by the reference slide)
SLIDE_BG = "#1B5E8A"
SLIDE_TEXT = "#FFFFFF"
SLIDE_SUBTITLE = "#B0C4D8"


class Talk1TitleCard(Scene):
    """Blue title-card slide for Talk 1, matching the reference style."""

    def construct(self):
        # ── full-screen blue background ──────────────────────────────
        bg = Rectangle(
            width=config.frame_width + 0.5,
            height=config.frame_height + 0.5,
            fill_color=SLIDE_BG,
            fill_opacity=1,
            stroke_width=0,
        )
        bg.move_to(ORIGIN)

        # ── title (two lines, bold, left-aligned) ───────────────────
        title_line1 = Text(
            "From Language Models",
            font_size=52,
            color=SLIDE_TEXT,
            weight=BOLD,
        )
        title_line2 = Text(
            "to Generalist Agents:",
            font_size=52,
            color=SLIDE_TEXT,
            weight=BOLD,
        )

        title_group = VGroup(title_line1, title_line2)
        title_group.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # ── subtitle (smaller, lighter color) ────────────────────────
        subtitle = Text(
            "The Shift from Predicting Words",
            font_size=30,
            color=SLIDE_SUBTITLE,
        )
        subtitle2 = Text(
            "to Taking Actions",
            font_size=30,
            color=SLIDE_SUBTITLE,
        )
        subtitle_group = VGroup(subtitle, subtitle2)
        subtitle_group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        # ── source info ──────────────────────────────────────────────
        source_line1 = Text(
            "CVPR 2024 Tutorial",
            font_size=22,
            color=SLIDE_SUBTITLE,
        )
        source_line2 = Text(
            "Generalist Agent AI",
            font_size=22,
            color=SLIDE_SUBTITLE,
        )
        source_line3 = Text(
            "Talk 1",
            font_size=22,
            color=SLIDE_SUBTITLE,
        )

        source_group = VGroup(source_line1, source_line2, source_line3)
        source_group.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        # ── layout everything left-aligned ───────────────────────────
        content = VGroup(title_group, subtitle_group, source_group)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        content.move_to(ORIGIN)
        content.shift(LEFT * 1.2)           # push towards left like the reference
        content.shift(DOWN * 0.3)           # nudge down slightly

        # ── animations ───────────────────────────────────────────────
        self.add(bg)

        # Fade in the title line by line
        self.play(FadeIn(title_line1, shift=LEFT * 0.3), run_time=1.0)
        self.play(FadeIn(title_line2, shift=LEFT * 0.3), run_time=0.8)

        self.wait(0.5)

        # Fade in subtitle
        self.play(
            FadeIn(subtitle_group, shift=UP * 0.15),
            run_time=0.8,
        )

        self.wait(0.3)

        # Fade in source info
        self.play(
            FadeIn(source_group, shift=UP * 0.15),
            run_time=0.8,
        )

        # Hold the title card
        self.wait(3)
