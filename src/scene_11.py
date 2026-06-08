import sys
import numpy as np
from pathlib import Path

CMD = Path(sys.argv[0]).name.lower()
if "manimgl" in CMD:
    from manimlib import *
else:
    from manim import *

BASE_DIR = Path("/home/pineapple/Desktop/projects/manim-gaai/")

WHITE = "#F5F5F5"
BG = "#0D0D0D"
ACCENT = "#4FC3F7"
GOLD = "#FFD54F"
DIM = "#8A7676"
DIM2 = "#615B5B"
RED = "#FF5252"
GREEN = "#66BB6A"
PURPLE = "#B39DDB"
ORANGE = "#FFB74D"
TEAL = "#4DB6AC"
PINK = "#F48FB1"


# ── helpers ─────────────────────────────────────────────────────────


def make_svg_icon(filename, color=WHITE, height=1.2):
    """Load a B&W SVG and style it."""
    svg = SVGMobject(str(BASE_DIR / "assets" / "svgs" / filename))
    svg.set_color(color)
    svg.set_stroke(color, width=1.2)
    svg.scale_to_fit_height(height)
    return svg


def make_pill(text_str, color=ACCENT, font_size=16, fill_opacity=0.15):
    """A rounded pill-shaped label."""
    label = Text(text_str, font_size=font_size, color=WHITE)
    pill = RoundedRectangle(
        width=label.width + 0.4,
        height=label.height + 0.22,
        corner_radius=0.15,
        color=color,
        stroke_width=1.4,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    pill.move_to(label.get_center())
    return VGroup(pill, label)


def make_token_box(label_text, color=ACCENT, font_size=14, width=None):
    """A small rounded box with a label, representing a token."""
    label = Text(label_text, font_size=font_size, color=WHITE)
    box_w = width or (label.width + 0.3)
    box = RoundedRectangle(
        width=box_w,
        height=label.height + 0.2,
        corner_radius=0.06,
        color=color,
        stroke_width=1.5,
        fill_color=color,
        fill_opacity=0.15,
    )
    label.move_to(box)
    return VGroup(box, label)


def make_hexagon(side_length=0.8, color=ACCENT, fill_opacity=0.08):
    """A glowing hexagon shape (LLM core)."""
    hex_shape = RegularPolygon(
        n=6,
        color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    hex_shape.scale(side_length)
    return hex_shape


def make_code_lines(center, n_lines=6, max_width=1.6, color=DIM):
    """Simple horizontal lines representing lines of code."""
    lines = VGroup()
    widths = [max_width * w for w in [0.9, 0.6, 1.0, 0.45, 0.75, 0.85, 0.5, 0.95]]
    for i in range(n_lines):
        w = widths[i % len(widths)]
        line = RoundedRectangle(
            width=w,
            height=0.06,
            corner_radius=0.02,
            color=color,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.5,
        )
        lines.add(line)
    lines.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    lines.move_to(center)
    return lines


def make_stair_block(label_text, color, width=2.2, height=0.7):
    """A single stair step block for the spectrum chart."""
    block = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.2,
    )
    label = Text(label_text, font_size=13, color=WHITE, weight=BOLD)
    label.move_to(block.get_center())
    return VGroup(block, label)


class AgentArchitectures(Scene):
    def construct(self):
        self.camera.background_color = BG

        self._part_1_spectrum_intro()
        self._part_2_prompt_template()
        self._part_3_react()
        self._part_4_learnable_prompt()
        self._part_5_lam_trajectories()
        self._part_6_multi_agent()
        self._part_7_closing_spectrum()

    # ==================================================================
    #  PART 1 — The Spectrum: simple → complex
    # ==================================================================

    def _part_1_spectrum_intro(self):
        # ── Horizontal spectrum line ──
        line_start = LEFT * 5.0
        line_end = RIGHT * 5.0

        spectrum_line = Arrow(
            line_start, line_end,
            buff=0,
            color=DIM,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.02,
        )

        # Labels at the ends
        simple_label = Text("simple", font_size=16, color=DIM)
        simple_label.next_to(line_start, DOWN, buff=0.25)

        complex_label = Text("complex", font_size=16, color=ACCENT)
        complex_label.next_to(line_end, DOWN, buff=0.25)

        # Gradient dots along the line
        n_dots = 12
        dots = VGroup()
        for i in range(n_dots):
            t = i / (n_dots - 1)
            x = line_start[0] + t * (line_end[0] - line_start[0])
            opacity = 0.15 + 0.6 * t
            dot = Dot(
                np.array([x, 0, 0]),
                radius=0.06 + 0.04 * t,
                color=ACCENT,
                fill_opacity=opacity,
            )
            dots.add(dot)

        # Title
        title = Text(
            "agent architectures",
            font_size=24,
            color=WHITE,
        )
        title.move_to(UP * 2.0)

        subtitle = Text(
            "a spectrum of designs",
            font_size=14,
            color=DIM,
        )
        subtitle.next_to(title, DOWN, buff=0.25)

        self.play(
            FadeIn(title, scale=1.1),
            FadeIn(subtitle, shift=UP * 0.05),
            run_time=0.6,
        )
        # [25:28] The journey from language models to generalist agents
        self.wait(3.0)

        self.play(
            GrowArrow(spectrum_line),
            run_time=0.6,
        )
        self.play(
            FadeIn(simple_label, shift=UP * 0.05),
            FadeIn(complex_label, shift=UP * 0.05),
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in dots],
                lag_ratio=0.04,
            ),
            run_time=0.7,
        )
        # [25:35] From simple text prediction to complex multi-step tasks
        self.wait(3.0)

        # ── Four milestone markers along the spectrum ──
        milestones = [
            ("prompt\ntemplate", DIM, 0.1),
            ("learnable\nprompt", TEAL, 0.37),
            ("action\nmodel", GOLD, 0.63),
            ("multi-\nagent", ACCENT, 0.9),
        ]

        markers = VGroup()
        for label_text, color, t in milestones:
            x = line_start[0] + t * (line_end[0] - line_start[0])
            tick = Line(
                np.array([x, -0.15, 0]),
                np.array([x, 0.15, 0]),
                color=color,
                stroke_width=2,
            )
            mark_label = Text(label_text, font_size=11, color=color)
            mark_label.next_to(tick, UP, buff=0.15)
            marker = VGroup(tick, mark_label)
            markers.add(marker)

        self.play(
            LaggedStart(
                *[FadeIn(m, shift=DOWN * 0.1) for m in markers],
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        # [25:40] But this is not a solved problem — challenges remain
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 2 — Prompt-Template Agent (zero-shot)
    # ==================================================================

    def _part_2_prompt_template(self):
        # ── Central LLM hexagon ──
        llm_hex = make_hexagon(side_length=0.8, color=ACCENT, fill_opacity=0.1)
        llm_hex.move_to(ORIGIN)
        llm_label = Text("LLM", font_size=16, color=ACCENT)
        llm_label.move_to(llm_hex.get_center())

        # ── The "fixed prompt" document above ──
        prompt_doc = RoundedRectangle(
            width=3.6,
            height=2.0,
            corner_radius=0.12,
            color=DIM2,
            stroke_width=1.5,
            fill_color=DIM2,
            fill_opacity=0.06,
        )
        prompt_doc.move_to(UP * 2.2)

        prompt_title = Text("system prompt", font_size=12, color=DIM)
        prompt_title.move_to(prompt_doc.get_top() + DOWN * 0.25)

        # Simulated prompt text lines
        prompt_lines = VGroup()
        line_texts = [
            '"You are an expert..."',
            "role: assistant",
            "task: decide next action",
            "format: JSON",
        ]
        for i, lt in enumerate(line_texts):
            line = Text(lt, font_size=11, color=WHITE if i == 0 else DIM)
            prompt_lines.add(line)
        prompt_lines.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        prompt_lines.move_to(prompt_doc.get_center() + DOWN * 0.1)

        # ── Arrow: prompt → LLM ──
        prompt_arrow = Arrow(
            prompt_doc.get_bottom(),
            llm_hex.get_top(),
            buff=0.15,
            color=DIM2,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # ── Output action pill ──
        action_pill = make_pill("action", color=GREEN, font_size=16)
        action_pill.move_to(DOWN * 2.0)

        out_arrow = Arrow(
            llm_hex.get_bottom(),
            action_pill.get_top(),
            buff=0.15,
            color=GREEN,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # ── "fixed" badge ──
        fixed_badge = VGroup()
        badge_bg = RoundedRectangle(
            width=0.8,
            height=0.35,
            corner_radius=0.08,
            color=RED,
            stroke_width=1.2,
            fill_color=RED,
            fill_opacity=0.15,
        )
        badge_text = Text("fixed", font_size=11, color=RED)
        badge_text.move_to(badge_bg)
        fixed_badge.add(badge_bg, badge_text)
        fixed_badge.next_to(prompt_doc, RIGHT, buff=0.2)

        # ── Animate ──
        self.play(
            FadeIn(llm_hex, scale=0.7),
            FadeIn(llm_label, scale=0.8),
            run_time=0.5,
        )

        self.play(
            FadeIn(prompt_doc, scale=0.9),
            FadeIn(prompt_title, shift=DOWN * 0.05),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=RIGHT * 0.08) for l in prompt_lines],
                lag_ratio=0.1,
            ),
            run_time=0.6,
        )
        self.play(
            FadeIn(fixed_badge, scale=0.8),
            run_time=0.3,
        )

        self.play(GrowArrow(prompt_arrow), run_time=0.4)

        # Pulse LLM processing
        pulse = llm_hex.copy().set_stroke(ACCENT, width=4, opacity=0.6)
        self.play(FadeIn(pulse), run_time=0.12)
        self.play(FadeOut(pulse), run_time=0.18)

        self.play(
            GrowArrow(out_arrow),
            FadeIn(action_pill, scale=0.8),
            run_time=0.5,
        )
        # [25:58] Hallucinations: confident-sounding but wrong answers
        self.wait(5.0)

        # ── Show limitation: if agent fails, prompt doesn't change ──
        fail_x = Text("✗", font_size=28, color=RED, weight=BOLD)
        fail_x.next_to(action_pill, RIGHT, buff=0.3)
        self.play(FadeIn(fail_x, scale=1.3), run_time=0.3)
        self.wait(0.2)

        # Arrow back up to prompt doc — but it stays the same
        retry_arrow = CurvedArrow(
            fail_x.get_right() + RIGHT * 0.1,
            fixed_badge.get_bottom() + DOWN * 0.1,
            angle=-PI / 3,
            color=RED,
            stroke_width=1.2,
            tip_length=0.12,
        )
        no_change = Text("no change", font_size=11, color=RED)
        no_change.next_to(retry_arrow, RIGHT, buff=0.1)

        self.play(
            Create(retry_arrow),
            FadeIn(no_change, shift=LEFT * 0.05),
            run_time=0.5,
        )
        # [26:10] The model generates plausible but factually wrong content
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 3 — ReAct: Reason → Act → Observe loop
    # ==================================================================

    def _part_3_react(self):
        # ── Central LLM ──
        llm_hex = make_hexagon(side_length=0.7, color=ACCENT, fill_opacity=0.1)
        llm_hex.move_to(ORIGIN)
        llm_label = Text("LLM", font_size=14, color=ACCENT)
        llm_label.move_to(llm_hex.get_center())

        # ── Three phase nodes arranged around LLM ──
        phase_radius = 2.0
        phase_data = [
            ("reason", ACCENT, "brain.svg", PI / 2),
            ("act", GREEN, "gear.svg", PI / 2 - 2 * PI / 3),
            ("observe", GOLD, "eye.svg", PI / 2 + 2 * PI / 3),
        ]

        phase_groups = VGroup()
        phase_positions = []
        for label_text, color, icon_file, angle in phase_data:
            pos = ORIGIN + phase_radius * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            phase_positions.append(pos)

            icon = make_svg_icon(icon_file, color=color, height=0.55)
            icon.move_to(pos)

            label = Text(label_text, font_size=14, color=color)
            label.next_to(icon, DOWN, buff=0.15)

            # Subtle background circle
            bg_circle = Circle(
                radius=0.5,
                color=color,
                stroke_width=1,
                stroke_opacity=0.3,
                fill_color=color,
                fill_opacity=0.04,
            )
            bg_circle.move_to(pos)

            phase_groups.add(VGroup(bg_circle, icon, label))

        # ── Curved arrows between phases ──
        loop_arrows = VGroup()
        arrow_colors = [GREEN, GOLD, ACCENT]
        for i in range(3):
            start_pos = phase_positions[i]
            end_pos = phase_positions[(i + 1) % 3]

            # Offset to avoid overlapping the icons
            direction = end_pos - start_pos
            direction_norm = direction / np.linalg.norm(direction)
            start_pt = start_pos + direction_norm * 0.6
            end_pt = end_pos - direction_norm * 0.6

            arc = ArcBetweenPoints(
                start_pt, end_pt,
                angle=PI / 5,
                color=arrow_colors[i],
                stroke_width=2,
                stroke_opacity=0.6,
            )
            tip = Arrow(
                end_pt - direction_norm * 0.15,
                end_pt,
                buff=0,
                color=arrow_colors[i],
                stroke_width=2,
                max_tip_length_to_length_ratio=0.8,
            )
            loop_arrows.add(VGroup(arc, tip))

        # ── Animate ──
        self.play(
            FadeIn(llm_hex, scale=0.7),
            FadeIn(llm_label, scale=0.8),
            run_time=0.5,
        )

        for pg in phase_groups:
            self.play(FadeIn(pg, scale=0.7), run_time=0.4)
            # [26:30] Safety: preventing harmful or biased outputs
            self.wait(2.0)

        self.play(
            LaggedStart(
                *[AnimationGroup(Create(la[0]), GrowArrow(la[1])) for la in loop_arrows],
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )
        # [26:45] Guardrails, alignment, red-teaming
        self.wait(5.0)

        # ── Animate a signal traveling the loop ──
        signal = Dot(radius=0.1, color=GOLD, fill_opacity=0.9)
        glow = signal.copy().scale(2).set_fill(GOLD, opacity=0.2)
        signal_group = VGroup(glow, signal)

        signal_group.move_to(phase_positions[0])
        self.play(FadeIn(signal_group, scale=0.5), run_time=0.2)

        for i in range(3):
            next_pos = phase_positions[(i + 1) % 3]
            self.play(
                signal_group.animate.move_to(next_pos),
                run_time=0.4,
                rate_func=smooth,
            )
            # Flash at each node
            self.play(
                Flash(
                    next_pos,
                    color=phase_data[(i + 1) % 3][1],
                    flash_radius=0.3,
                    num_lines=6,
                    line_length=0.08,
                ),
                run_time=0.2,
            )

        self.play(FadeOut(signal_group), run_time=0.2)

        # ── "structured but still fixed" label ──
        note = Text("structured loop — but prompt is still fixed", font_size=13, color=DIM)
        note.move_to(DOWN * 3.2)
        self.play(FadeIn(note, shift=UP * 0.05), run_time=0.4)
        # [26:55] Three critical safety concerns
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 4 — Learnable-Prompt Agents (Retroformer)
    # ==================================================================

    def _part_4_learnable_prompt(self):
        # ── Attempt 1 panel (left): agent tries and fails ──
        attempt_1 = RoundedRectangle(
            width=3.2, height=3.5, corner_radius=0.12,
            color=RED, stroke_width=1.5,
            fill_color=RED, fill_opacity=0.03,
        )
        attempt_1.move_to(LEFT * 3.5)

        a1_title = Text("attempt 1", font_size=14, color=RED)
        a1_title.move_to(attempt_1.get_top() + DOWN * 0.3)

        # Mini agent loop inside
        a1_robot = make_svg_icon("robot.svg", color=DIM, height=0.6)
        a1_robot.move_to(attempt_1.get_center() + UP * 0.3)

        a1_gear = make_svg_icon("gear.svg", color=DIM, height=0.35)
        a1_gear.move_to(attempt_1.get_center() + DOWN * 0.3 + LEFT * 0.4)

        a1_eye = make_svg_icon("eye.svg", color=DIM, height=0.3)
        a1_eye.move_to(attempt_1.get_center() + DOWN * 0.3 + RIGHT * 0.4)

        # Big X for failure
        fail_mark = Text("✗", font_size=36, color=RED, weight=BOLD)
        fail_mark.move_to(attempt_1.get_center() + DOWN * 1.0)

        # ── Reflection arrow (center): retrospective model ──
        retro_box = RoundedRectangle(
            width=2.4, height=1.4, corner_radius=0.12,
            color=PURPLE, stroke_width=2,
            fill_color=PURPLE, fill_opacity=0.06,
        )
        retro_box.move_to(ORIGIN + UP * 0.3)

        retro_brain = make_svg_icon("brain.svg", color=PURPLE, height=0.5)
        retro_brain.move_to(retro_box.get_center() + UP * 0.15)

        retro_label = Text("reflect", font_size=13, color=PURPLE)
        retro_label.move_to(retro_box.get_center() + DOWN * 0.35)

        # Arrow from attempt 1 to reflection
        reflect_arrow = Arrow(
            attempt_1.get_right(),
            retro_box.get_left(),
            buff=0.15,
            color=PURPLE,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # ── Memory / lessons learned ──
        memory_pills = VGroup()
        lessons = ["avoid loop", "check output", "use tool B"]
        for i, lesson in enumerate(lessons):
            pill = make_pill(lesson, color=PURPLE, font_size=10, fill_opacity=0.1)
            memory_pills.add(pill)
        memory_pills.arrange(DOWN, buff=0.15)
        memory_pills.move_to(ORIGIN + DOWN * 1.8)

        memory_label = Text("lessons", font_size=11, color=PURPLE)
        memory_label.next_to(memory_pills, LEFT, buff=0.3)

        lesson_arrows = VGroup()
        for pill in memory_pills:
            la = Arrow(
                retro_box.get_bottom(),
                pill.get_top(),
                buff=0.08,
                color=PURPLE,
                stroke_width=0.8,
                stroke_opacity=0.4,
                max_tip_length_to_length_ratio=0.15,
            )
            lesson_arrows.add(la)

        # ── Attempt 2 panel (right): improved ──
        attempt_2 = RoundedRectangle(
            width=3.2, height=3.5, corner_radius=0.12,
            color=GREEN, stroke_width=1.5,
            fill_color=GREEN, fill_opacity=0.03,
        )
        attempt_2.move_to(RIGHT * 3.5)

        a2_title = Text("attempt 2", font_size=14, color=GREEN)
        a2_title.move_to(attempt_2.get_top() + DOWN * 0.3)

        a2_robot = make_svg_icon("robot.svg", color=GREEN, height=0.6)
        a2_robot.move_to(attempt_2.get_center() + UP * 0.3)

        a2_gear = make_svg_icon("gear.svg", color=GREEN, height=0.35)
        a2_gear.move_to(attempt_2.get_center() + DOWN * 0.3 + LEFT * 0.4)

        a2_eye = make_svg_icon("eye.svg", color=GREEN, height=0.3)
        a2_eye.move_to(attempt_2.get_center() + DOWN * 0.3 + RIGHT * 0.4)

        success_mark = Text("✓", font_size=36, color=GREEN, weight=BOLD)
        success_mark.move_to(attempt_2.get_center() + DOWN * 1.0)

        # Arrow from reflection to attempt 2
        improve_arrow = Arrow(
            retro_box.get_right(),
            attempt_2.get_left(),
            buff=0.15,
            color=GREEN,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # Dashed arrow from memory to attempt 2 prompt
        memory_to_a2 = DashedLine(
            memory_pills.get_right(),
            attempt_2.get_bottom() + LEFT * 0.5,
            color=PURPLE,
            stroke_width=1,
            dash_length=0.06,
        )

        # ── Animate ──
        self.play(
            FadeIn(attempt_1, scale=0.9),
            FadeIn(a1_title),
            run_time=0.5,
        )
        self.play(
            FadeIn(a1_robot, scale=0.8),
            FadeIn(a1_gear, scale=0.7),
            FadeIn(a1_eye, scale=0.7),
            run_time=0.4,
        )
        self.play(
            FadeIn(fail_mark, scale=1.5),
            Flash(fail_mark.get_center(), color=RED, flash_radius=0.4, num_lines=8),
            run_time=0.4,
        )
        # [27:11] Planning and reasoning: can the agent break down complex tasks?
        self.wait(5.0)

        # Reflection
        self.play(GrowArrow(reflect_arrow), run_time=0.4)
        self.play(
            FadeIn(retro_box, scale=0.9),
            FadeIn(retro_brain, scale=0.8),
            FadeIn(retro_label),
            run_time=0.5,
        )

        # Brain pulses
        brain_pulse = retro_brain.copy().set_stroke(PURPLE, width=3, opacity=0.5)
        self.play(FadeIn(brain_pulse), run_time=0.12)
        self.play(FadeOut(brain_pulse), run_time=0.2)

        # Lessons emerge
        self.play(
            FadeIn(memory_label),
            LaggedStart(
                *[
                    AnimationGroup(Create(la), FadeIn(pill, scale=0.7))
                    for la, pill in zip(lesson_arrows, memory_pills)
                ],
                lag_ratio=0.15,
            ),
            run_time=0.7,
        )
        # [27:20] Not just predicting the next word, but deciding what to do
        self.wait(5.0)

        # Improved attempt
        self.play(GrowArrow(improve_arrow), run_time=0.4)
        self.play(Create(memory_to_a2), run_time=0.3)
        self.play(
            FadeIn(attempt_2, scale=0.9),
            FadeIn(a2_title),
            run_time=0.5,
        )
        self.play(
            FadeIn(a2_robot, scale=0.8),
            FadeIn(a2_gear, scale=0.7),
            FadeIn(a2_eye, scale=0.7),
            run_time=0.4,
        )
        self.play(
            FadeIn(success_mark, scale=1.5),
            Flash(success_mark.get_center(), color=GREEN, flash_radius=0.4, num_lines=8),
            run_time=0.4,
        )
        # [27:30] When things go wrong, can the agent self-correct?
        self.wait(10.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 5 — Large Action Models + Trajectory Data illustration
    # ==================================================================

    def _part_5_lam_trajectories(self):
        # ── 5a: LLM predicts tokens vs LAM predicts actions ──
        # LEFT: token prediction
        llm_box = RoundedRectangle(
            width=2.0, height=1.2, corner_radius=0.12,
            color=ACCENT, stroke_width=1.8,
            fill_color=ACCENT, fill_opacity=0.06,
        )
        llm_box.move_to(LEFT * 3.5 + UP * 1.5)
        llm_lbl = Text("LLM", font_size=16, color=ACCENT)
        llm_lbl.move_to(llm_box.get_center() + UP * 0.15)
        llm_desc = Text("predicts tokens", font_size=11, color=DIM)
        llm_desc.move_to(llm_box.get_center() + DOWN * 0.25)

        # Token output
        tokens = VGroup()
        token_words = ["The", "cat", "sat"]
        for tw in token_words:
            tokens.add(make_token_box(tw, color=ACCENT, font_size=11))
        tokens.arrange(RIGHT, buff=0.1)
        tokens.next_to(llm_box, DOWN, buff=0.35)

        tok_arrow = Arrow(
            llm_box.get_bottom(), tokens.get_top(),
            buff=0.08, color=ACCENT, stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )

        # RIGHT: action prediction
        lam_box = RoundedRectangle(
            width=2.0, height=1.2, corner_radius=0.12,
            color=GREEN, stroke_width=2.5,
            fill_color=GREEN, fill_opacity=0.08,
        )
        lam_box.move_to(RIGHT * 3.5 + UP * 1.5)
        lam_lbl = Text("LAM", font_size=16, color=GREEN, weight=BOLD)
        lam_lbl.move_to(lam_box.get_center() + UP * 0.15)
        lam_desc = Text("predicts actions", font_size=11, color=GREEN)
        lam_desc.move_to(lam_box.get_center() + DOWN * 0.25)

        # Action output
        actions = VGroup()
        action_words = ["search", "click", "submit"]
        for aw in action_words:
            actions.add(make_token_box(aw, color=GREEN, font_size=11))
        actions.arrange(RIGHT, buff=0.1)
        actions.next_to(lam_box, DOWN, buff=0.35)

        act_arrow = Arrow(
            lam_box.get_bottom(), actions.get_top(),
            buff=0.08, color=GREEN, stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )

        # Divider
        divider = DashedLine(
            UP * 3.0, DOWN * 0.5,
            color=DIM2, stroke_width=1, dash_length=0.1,
        )

        # Vs label
        vs_label = Text("vs", font_size=18, color=DIM)
        vs_label.move_to(UP * 1.5)

        # Animate comparison
        self.play(Create(divider), FadeIn(vs_label), run_time=0.4)

        self.play(
            FadeIn(llm_box, scale=0.9),
            FadeIn(llm_lbl), FadeIn(llm_desc),
            run_time=0.5,
        )
        self.play(
            GrowArrow(tok_arrow),
            LaggedStart(*[FadeIn(t, shift=DOWN * 0.05) for t in tokens], lag_ratio=0.1),
            run_time=0.5,
        )
        # [27:50] Generalization: can the agent handle novel tasks?
        self.wait(5.0)

        self.play(
            FadeIn(lam_box, scale=0.9),
            FadeIn(lam_lbl), FadeIn(lam_desc),
            run_time=0.5,
        )
        self.play(
            GrowArrow(act_arrow),
            LaggedStart(*[FadeIn(a, shift=DOWN * 0.05) for a in actions], lag_ratio=0.1),
            run_time=0.5,
        )

        # Emphasize LAM
        lam_glow = SurroundingRectangle(
            VGroup(lam_box, actions),
            color=GREEN, buff=0.15, corner_radius=0.15,
            stroke_width=2, fill_color=GREEN, fill_opacity=0.03,
        )
        self.play(Create(lam_glow), run_time=0.4)
        pulse_rect = lam_glow.copy().set_stroke(GREEN, width=3)
        self.play(pulse_rect.animate.scale(1.05).set_opacity(0), run_time=0.5)
        self.remove(pulse_rect)
        # [28:00] Real-time adaptation to new environments
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ── 5b: Trajectory Data Illustration (recreating image 2) ──
        # Two card panels side by side showing trajectory data structure

        # LEFT CARD: HotPotQA-style trajectory
        card_left = RoundedRectangle(
            width=4.8, height=5.0, corner_radius=0.12,
            color=ACCENT, stroke_width=1.5,
            fill_color=ACCENT, fill_opacity=0.03,
        )
        card_left.move_to(LEFT * 3.0)

        cl_title = Text("HotPotQA", font_size=16, color=ACCENT)
        cl_title.move_to(card_left.get_top() + DOWN * 0.35)

        # Trajectory fields — color-coded key:value pairs
        traj_left_data = [
            ("question:", GOLD, "Which magazine was..."),
            ("thought:", ACCENT, "I need to Search..."),
            ("action:", GREEN, "Search[Arthur's Mag]"),
            ("observation:", ORANGE, "Published in 1844"),
            ("thought:", ACCENT, "Now I know..."),
            ("action:", GREEN, "Finish[Arthur's Mag]"),
        ]

        traj_left_lines = VGroup()
        for key, color, value in traj_left_data:
            key_mob = Text(key, font_size=10, color=color, weight=BOLD)
            val_mob = Text(value, font_size=10, color=DIM)
            row = VGroup(key_mob, val_mob)
            row.arrange(RIGHT, buff=0.12)
            traj_left_lines.add(row)

        traj_left_lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        traj_left_lines.move_to(card_left.get_center() + DOWN * 0.2)

        # Stacked card shadow effect (representing multiple trajectories)
        shadow_l1 = card_left.copy().set_stroke(DIM2, width=0.8).set_fill(opacity=0.01)
        shadow_l1.shift(RIGHT * 0.08 + DOWN * 0.08)
        shadow_l2 = card_left.copy().set_stroke(DIM2, width=0.5).set_fill(opacity=0.005)
        shadow_l2.shift(RIGHT * 0.16 + DOWN * 0.16)

        # RIGHT CARD: WebShop-style trajectory
        card_right = RoundedRectangle(
            width=4.8, height=5.0, corner_radius=0.12,
            color=TEAL, stroke_width=1.5,
            fill_color=TEAL, fill_opacity=0.03,
        )
        card_right.move_to(RIGHT * 3.0)

        cr_title = Text("WebShop", font_size=16, color=TEAL)
        cr_title.move_to(card_right.get_top() + DOWN * 0.35)

        traj_right_data = [
            ("user:", GOLD, "Find a cotton shirt..."),
            ("thought:", ACCENT, "I need to search..."),
            ("action:", GREEN, "search[cotton shirt]"),
            ("observation:", ORANGE, "3 results found"),
            ("thought:", ACCENT, "Item 2 matches..."),
            ("action:", GREEN, "click[Buy Now]"),
        ]

        traj_right_lines = VGroup()
        for key, color, value in traj_right_data:
            key_mob = Text(key, font_size=10, color=color, weight=BOLD)
            val_mob = Text(value, font_size=10, color=DIM)
            row = VGroup(key_mob, val_mob)
            row.arrange(RIGHT, buff=0.12)
            traj_right_lines.add(row)

        traj_right_lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        traj_right_lines.move_to(card_right.get_center() + DOWN * 0.2)

        # Stacked shadows for right card
        shadow_r1 = card_right.copy().set_stroke(DIM2, width=0.8).set_fill(opacity=0.01)
        shadow_r1.shift(RIGHT * 0.08 + DOWN * 0.08)
        shadow_r2 = card_right.copy().set_stroke(DIM2, width=0.5).set_fill(opacity=0.005)
        shadow_r2.shift(RIGHT * 0.16 + DOWN * 0.16)

        # Top title
        traj_title = Text("agent trajectory data", font_size=20, color=WHITE)
        traj_title.move_to(UP * 3.3)

        # ── Animate trajectory illustration ──
        self.play(FadeIn(traj_title, scale=1.1), run_time=0.5)

        # Left card with shadow stack
        self.play(
            FadeIn(shadow_l2), FadeIn(shadow_l1),
            FadeIn(card_left, scale=0.95),
            FadeIn(cl_title),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=RIGHT * 0.08) for row in traj_left_lines],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )

        # Right card with shadow stack
        self.play(
            FadeIn(shadow_r2), FadeIn(shadow_r1),
            FadeIn(card_right, scale=0.95),
            FadeIn(cr_title),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=RIGHT * 0.08) for row in traj_right_lines],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        # [28:30] The future: autonomous systems that work alongside humans
        self.wait(5.0)

        # ── Highlight the action fields specifically ──
        # Flash the "action:" rows in both cards
        action_rows_left = [traj_left_lines[2], traj_left_lines[5]]
        action_rows_right = [traj_right_lines[2], traj_right_lines[5]]

        for row in action_rows_left + action_rows_right:
            hl = SurroundingRectangle(
                row, color=GREEN, buff=0.06,
                corner_radius=0.04, stroke_width=1.5,
                fill_color=GREEN, fill_opacity=0.06,
            )
            self.play(Create(hl), run_time=0.15)

        # Bottom note
        train_note = Text(
            "LAM is trained on these trajectories",
            font_size=14, color=GREEN,
        )
        train_note.move_to(DOWN * 3.3)
        self.play(FadeIn(train_note, shift=UP * 0.05), run_time=0.4)
        # [28:40] But this requires trust, safety, and reliability
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 6 — Multi-Agent Orchestration
    # ==================================================================

    def _part_6_multi_agent(self):
        # ── Central controller ──
        controller = RoundedRectangle(
            width=2.0, height=1.0, corner_radius=0.12,
            color=GOLD, stroke_width=2,
            fill_color=GOLD, fill_opacity=0.08,
        )
        controller.move_to(ORIGIN)
        ctrl_icon = make_svg_icon("brain.svg", color=GOLD, height=0.45)
        ctrl_icon.move_to(controller.get_center() + LEFT * 0.4)
        ctrl_label = Text("controller", font_size=13, color=GOLD)
        ctrl_label.move_to(controller.get_center() + RIGHT * 0.35)

        # ── Specialized agent nodes around the controller ──
        agent_configs = [
            ("planner", ACCENT, "brain.svg", UP * 2.2),
            ("searcher", TEAL, "browser.svg", RIGHT * 3.5 + UP * 0.8),
            ("coder", GREEN, "gear.svg", RIGHT * 3.5 + DOWN * 0.8),
            ("reviewer", PURPLE, "eye.svg", DOWN * 2.2),
        ]

        agent_nodes = VGroup()
        node_positions = []
        for name, color, icon_file, pos in agent_configs:
            node_box = RoundedRectangle(
                width=1.8, height=0.9, corner_radius=0.1,
                color=color, stroke_width=1.5,
                fill_color=color, fill_opacity=0.06,
            )
            node_box.move_to(pos)

            icon = make_svg_icon(icon_file, color=color, height=0.35)
            icon.move_to(node_box.get_center() + LEFT * 0.35)

            label = Text(name, font_size=12, color=color)
            label.move_to(node_box.get_center() + RIGHT * 0.3)

            node = VGroup(node_box, icon, label)
            agent_nodes.add(node)
            node_positions.append(pos)

        # ── Arrows from controller to each agent ──
        ctrl_arrows = VGroup()
        for pos in node_positions:
            direction = pos - ORIGIN
            direction_norm = direction / np.linalg.norm(direction)
            start_pt = ORIGIN + direction_norm * 0.7
            end_pt = pos - direction_norm * 0.65

            arr = Arrow(
                start_pt, end_pt,
                buff=0,
                color=GOLD,
                stroke_width=1.2,
                stroke_opacity=0.5,
                max_tip_length_to_length_ratio=0.1,
            )
            ctrl_arrows.add(arr)

        # ── Animate ──
        self.play(
            FadeIn(controller, scale=0.9),
            FadeIn(ctrl_icon, scale=0.8),
            FadeIn(ctrl_label),
            run_time=0.5,
        )
        # [28:55] Key research directions that will shape the future
        self.wait(3.0)

        # Agents appear one by one with arrows
        for node, arrow in zip(agent_nodes, ctrl_arrows):
            self.play(
                GrowArrow(arrow),
                FadeIn(node, scale=0.8),
                run_time=0.45,
            )
            self.wait(1.0)

        self.wait(3.0)

        # ── Show a task flowing through the pipeline ──
        # Task dot travels: controller → planner → controller → searcher → ...
        task_dot = Dot(radius=0.1, color=GOLD, fill_opacity=0.9)
        task_glow = task_dot.copy().scale(2).set_fill(GOLD, opacity=0.2)
        task_group = VGroup(task_glow, task_dot)

        task_path = [
            ORIGIN,
            node_positions[0],  # planner
            ORIGIN,
            node_positions[1],  # searcher
            ORIGIN,
            node_positions[2],  # coder
            ORIGIN,
            node_positions[3],  # reviewer
            ORIGIN,
        ]

        task_group.move_to(ORIGIN)
        self.play(FadeIn(task_group, scale=0.5), run_time=0.2)

        for pos in task_path[1:]:
            self.play(
                task_group.animate.move_to(pos),
                run_time=0.3,
                rate_func=smooth,
            )
            if not np.allclose(pos, ORIGIN, atol=0.1):
                self.play(
                    Flash(pos, color=GOLD, flash_radius=0.25,
                          num_lines=5, line_length=0.06),
                    run_time=0.15,
                )

        self.play(FadeOut(task_group), run_time=0.2)

        # ── Highlight the orchestration complexity ──
        orch_glow = SurroundingRectangle(
            VGroup(controller, *agent_nodes),
            color=GOLD, buff=0.4, corner_radius=0.2,
            stroke_width=1.5, fill_color=GOLD, fill_opacity=0.02,
        )
        self.play(Create(orch_glow), run_time=0.4)

        # Warning note
        warn_items = VGroup()
        warnings = [
            ("powerful", GREEN),
            ("but complex", RED),
        ]
        for txt, clr in warnings:
            pill = make_pill(txt, color=clr, font_size=12, fill_opacity=0.12)
            warn_items.add(pill)
        warn_items.arrange(RIGHT, buff=0.3)
        warn_items.move_to(DOWN * 3.3)

        self.play(
            LaggedStart(
                *[FadeIn(w, scale=0.8) for w in warn_items],
                lag_ratio=0.2,
            ),
            run_time=0.5,
        )
        # [29:10] Personalization: agents that learn your preferences
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 7 — Closing: The Full Spectrum (staircase chart)
    #  Recreating Image 1 as a Manim illustration
    # ==================================================================

    def _part_7_closing_spectrum(self):
        # ── Axes ──
        x_axis = Arrow(
            LEFT * 5.5 + DOWN * 2.5,
            RIGHT * 5.5 + DOWN * 2.5,
            buff=0,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.015,
        )
        y_axis = Arrow(
            LEFT * 5.0 + DOWN * 2.5,
            LEFT * 5.0 + UP * 3.0,
            buff=0,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.02,
        )

        x_label = Text("agent capability", font_size=14, color=DIM)
        x_label.next_to(x_axis, DOWN, buff=0.2)

        y_label = Text("architecture\ncomplexity", font_size=12, color=DIM)
        y_label.next_to(y_axis, LEFT, buff=0.15)

        self.play(
            GrowArrow(x_axis), GrowArrow(y_axis),
            FadeIn(x_label), FadeIn(y_label),
            run_time=0.6,
        )

        # ── Staircase blocks ──
        stair_data = [
            ("Prompt-template\nAgents", DIM, LEFT * 3.0 + DOWN * 1.5, 2.4, 0.9),
            ("Learnable-prompt\nAgents", TEAL, LEFT * 0.6 + DOWN * 0.3, 2.6, 0.9),
            ("Large Action\nModels (LAMs)", GOLD, RIGHT * 2.0 + UP * 0.9, 2.6, 0.9),
            ("Multi-agent\nOrchestration", ACCENT, RIGHT * 4.2 + UP * 2.1, 2.4, 0.9),
        ]

        stair_blocks = VGroup()
        for label_text, color, pos, w, h in stair_data:
            block = RoundedRectangle(
                width=w, height=h, corner_radius=0.1,
                color=color, stroke_width=2,
                fill_color=color, fill_opacity=0.2,
            )
            block.move_to(pos)
            label = Text(label_text, font_size=12, color=WHITE, weight=BOLD)
            label.move_to(block.get_center())
            stair_blocks.add(VGroup(block, label))

        # Animate stairs climbing up
        for i, stair in enumerate(stair_blocks):
            self.play(
                FadeIn(stair, shift=UP * 0.15 + RIGHT * 0.1),
                run_time=0.5,
            )
            # Brief flash
            self.play(
                Flash(
                    stair[0].get_center(),
                    color=stair_data[i][1],
                    flash_radius=0.4,
                    num_lines=6,
                    line_length=0.08,
                ),
                run_time=0.2,
            )
            self.wait(1.0)

        # [29:22] This is not the end, but the beginning
        self.wait(3.0)

        # ── Connecting lines between stairs (ascending path) ──
        step_lines = VGroup()
        for i in range(len(stair_blocks) - 1):
            line = DashedLine(
                stair_blocks[i][0].get_right(),
                stair_blocks[i + 1][0].get_left(),
                color=DIM2,
                stroke_width=1,
                dash_length=0.06,
            )
            step_lines.add(line)

        self.play(
            LaggedStart(
                *[Create(sl) for sl in step_lines],
                lag_ratio=0.15,
            ),
            run_time=0.6,
        )
        # [29:30] The journey continues
        self.wait(3.0)

        # ── Glow sweep across all stairs ──
        for stair in stair_blocks:
            glow = stair[0].copy().set_stroke(width=3.5, opacity=0.6)
            self.play(FadeIn(glow), run_time=0.1)
            self.play(FadeOut(glow), run_time=0.12)

        # [29:35] Thank you for watching
        self.wait(3.0)

        # ── Final fade out ──
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        # [29:40] Final pause before fade
        self.wait(2.0)
