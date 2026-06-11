import numpy as np

from utils.manim_compat import *
from utils.mobjects import (
    make_hexagon,
    make_pill,
    make_svg_icon,
)
from utils.theme import *


class WhatsNext(Scene):
    def construct(self):
        self.camera.background_color = BG

        self._part_1_opening()
        self._part_2_multimodality()
        self._part_3_better_benchmarks()
        self._part_4_learning()
        self._part_5_closing()

    # ==================================================================
    #  PART 1 — Opening: "What's Next?"
    # ==================================================================

    def _part_1_opening(self):
        title = Text("what's next?", font_size=42, color=WHITE, weight=BOLD)
        title.move_to(ORIGIN)

        underline = Line(
            title.get_left() + DOWN * 0.35,
            title.get_right() + DOWN * 0.35,
            color=ACCENT,
            stroke_width=2.5,
        )

        subtitle = Text(
            "how can we improve from here",
            font_size=16,
            color=DIM,
        )
        subtitle.next_to(underline, DOWN, buff=0.4)

        self.play(
            FadeIn(title, scale=1.15),
            run_time=0.7,
        )
        self.play(
            Create(underline),
            FadeIn(subtitle, shift=UP * 0.05),
            run_time=0.5,
        )
        # "So what's next? How can we improve from all of the stuffs we mentioned."
        self.wait(4.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

    # ==================================================================
    #  PART 2 — Multimodality
    #  Agent surrounded by modality icons that light up
    # ==================================================================

    def _part_2_multimodality(self):
        section_label = Text("1. multimodality", font_size=22, color=ACCENT)
        section_label.move_to(UP * 3.3)
        self.play(FadeIn(section_label, shift=DOWN * 0.1), run_time=0.4)

        # Central agent hexagon
        agent_hex = make_hexagon(side_length=0.9, color=ACCENT, fill_opacity=0.08)
        agent_hex.move_to(ORIGIN)
        agent_label = Text("agent", font_size=16, color=ACCENT)
        agent_label.move_to(agent_hex.get_center())

        self.play(
            FadeIn(agent_hex, scale=0.7),
            FadeIn(agent_label, scale=0.8),
            run_time=0.5,
        )
        # "Agents should not only process text."
        self.wait(2.5)

        # Modality icons arranged in a circle around the agent
        modalities = [
            ("eye.svg", "images", GOLD, 90),
            ("video.svg", "video", ORANGE, 150),
            ("speaker.svg", "audio", PURPLE, 210),
            ("monitor.svg", "screens", TEAL, 270),
            ("document.svg", "docs", DIM, 330),
            ("hand-pointer.svg", "interact", GREEN, 30),
        ]

        radius = 2.4
        mod_groups = VGroup()
        mod_positions = []

        for icon_file, label_text, color, angle_deg in modalities:
            angle = angle_deg * PI / 180
            pos = ORIGIN + radius * np.array([np.cos(angle), np.sin(angle), 0])
            mod_positions.append(pos)

            icon = make_svg_icon(icon_file, color=color, height=0.55)
            icon.move_to(pos)

            label = Text(label_text, font_size=11, color=color)
            label.next_to(icon, DOWN, buff=0.15)

            bg_circle = Circle(
                radius=0.5,
                color=color,
                stroke_width=1.5,
                stroke_opacity=0.3,
                fill_color=color,
                fill_opacity=0.03,
            )
            bg_circle.move_to(pos)

            mod_groups.add(VGroup(bg_circle, icon, label))

        # Connecting lines from agent to each modality
        conn_lines = VGroup()
        for pos, (_, _, color, _) in zip(mod_positions, modalities):
            line = Line(
                ORIGIN,
                pos,
                color=color,
                stroke_width=1.0,
                stroke_opacity=0.3,
            )
            conn_lines.add(line)

        # Animate modalities appearing one by one
        # "They need to understand images, videos, audio, screens, documents, and real interfaces."
        self.play(
            LaggedStart(
                *[Create(l) for l in conn_lines],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[FadeIn(mg, scale=0.6) for mg in mod_groups],
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        # "Because real tasks are not purely textual."
        self.wait(4.0)

        # Signal pulse from each modality to center
        # "Humans see, listen, click, move, and react to changes."
        for i, (mg, pos) in enumerate(zip(mod_groups, mod_positions)):
            signal = Dot(radius=0.08, color=modalities[i][2], fill_opacity=0.9)
            signal.move_to(pos)
            self.play(FadeIn(signal, scale=0.5), run_time=0.08)
            self.play(
                signal.animate.move_to(ORIGIN),
                run_time=0.25,
                rate_func=smooth,
            )
            self.remove(signal)

        # Agent pulses after receiving all signals
        pulse = agent_hex.copy().set_stroke(ACCENT, width=4, opacity=0.7)
        self.play(FadeIn(pulse), run_time=0.12)
        self.play(pulse.animate.scale(1.3).set_opacity(0), run_time=0.4)
        self.remove(pulse)

        # "Future agents need to do the same."
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

    # ==================================================================
    #  PART 3 — Better Benchmarks and Environments
    #  A "clean" benchmark crumbles into a messy real world
    # ==================================================================

    def _part_3_better_benchmarks(self):
        section_label = Text("2. better benchmarks", font_size=22, color=GOLD)
        section_label.move_to(UP * 3.3)
        self.play(FadeIn(section_label, shift=DOWN * 0.1), run_time=0.4)

        # LEFT SIDE: "Current benchmarks" — neat, orderly
        neat_title = Text("current", font_size=14, color=DIM)
        neat_title.move_to(LEFT * 3.2 + UP * 2.0)

        neat_boxes = VGroup()
        for i in range(4):
            box = RoundedRectangle(
                width=2.4,
                height=0.5,
                corner_radius=0.08,
                color=DIM2,
                stroke_width=1.2,
                fill_color=DIM2,
                fill_opacity=0.06,
            )
            neat_boxes.add(box)
        neat_boxes.arrange(DOWN, buff=0.15)
        neat_boxes.move_to(LEFT * 3.2 + DOWN * 0.3)

        neat_checks = VGroup()
        for box in neat_boxes:
            check = Text("✓", font_size=16, color=GREEN)
            check.move_to(box.get_right() + LEFT * 0.3)
            neat_checks.add(check)

        # RIGHT SIDE: "Real world" — messy, broken
        messy_title = Text("real world", font_size=14, color=RED)
        messy_title.move_to(RIGHT * 3.2 + UP * 2.0)

        messy_elements = VGroup()
        # Broken/tilted boxes
        problems = [
            ("websites change", -5),
            ("tools fail", 8),
            ("unclear instructions", -3),
            ("agents must recover", 6),
        ]

        for i, (label_text, tilt) in enumerate(problems):
            box = RoundedRectangle(
                width=2.6,
                height=0.5,
                corner_radius=0.08,
                color=RED,
                stroke_width=1.2,
                fill_color=RED,
                fill_opacity=0.05,
            )
            label = Text(label_text, font_size=11, color=RED)
            label.move_to(box.get_center())
            group = VGroup(box, label)
            group.rotate(tilt * DEGREES)
            messy_elements.add(group)

        messy_elements.arrange(DOWN, buff=0.2)
        messy_elements.move_to(RIGHT * 3.2 + DOWN * 0.3)

        # Divider
        divider = DashedLine(
            UP * 2.5,
            DOWN * 2.5,
            color=DIM2,
            stroke_width=1,
            dash_length=0.1,
        )

        vs_arrow = Arrow(
            LEFT * 0.8,
            RIGHT * 0.8,
            buff=0,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12,
        )
        vs_arrow.move_to(DOWN * 0.3)

        gap_label = Text("gap", font_size=14, color=GOLD, weight=BOLD)
        gap_label.next_to(vs_arrow, UP, buff=0.15)

        # Animate
        self.play(Create(divider), run_time=0.3)

        # "Current agent benchmarks are still too simple."
        self.play(
            FadeIn(neat_title),
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.08) for b in neat_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[FadeIn(c, scale=1.3) for c in neat_checks],
                lag_ratio=0.06,
            ),
            run_time=0.4,
        )
        self.wait(3.0)

        # "Real-world tasks are messy..."
        self.play(
            FadeIn(messy_title),
            LaggedStart(
                *[FadeIn(me, scale=0.8) for me in messy_elements],
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )
        self.wait(2.0)

        # Show the gap
        self.play(
            GrowArrow(vs_arrow),
            FadeIn(gap_label, scale=0.8),
            run_time=0.5,
        )
        # "websites change, tools fail, instructions are unclear, agents must recover"
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

    # ==================================================================
    #  PART 4 — Learning and Generalization
    #  An agent evolving across different environments
    # ==================================================================

    def _part_4_learning(self):
        section_label = Text("3. learning & generalization", font_size=22, color=GREEN)
        section_label.move_to(UP * 3.3)
        self.play(FadeIn(section_label, shift=DOWN * 0.1), run_time=0.4)

        # Show the problem: agent relying on a fixed prompt
        prompt_box = RoundedRectangle(
            width=3.0,
            height=1.4,
            corner_radius=0.12,
            color=DIM2,
            stroke_width=1.5,
            fill_color=DIM2,
            fill_opacity=0.06,
        )
        prompt_box.move_to(LEFT * 3.0 + UP * 0.5)

        prompt_label = Text("fixed prompts", font_size=13, color=DIM)
        prompt_label.move_to(prompt_box.get_top() + DOWN * 0.25)

        # Few-shot example lines
        example_lines = VGroup()
        for i in range(3):
            line = RoundedRectangle(
                width=2.2,
                height=0.18,
                corner_radius=0.04,
                color=DIM,
                stroke_width=0,
                fill_color=DIM,
                fill_opacity=0.3 + i * 0.1,
            )
            example_lines.add(line)
        example_lines.arrange(DOWN, buff=0.1)
        example_lines.move_to(prompt_box.get_center() + DOWN * 0.15)

        # "Chained" badge
        chain = make_pill("rigid", color=RED, font_size=12, fill_opacity=0.15)
        chain.next_to(prompt_box, RIGHT, buff=0.4)

        # "Many agents today still rely too much on prompts and few-shot examples."
        self.play(
            FadeIn(prompt_box, scale=0.9),
            FadeIn(prompt_label),
            LaggedStart(
                *[FadeIn(l, shift=RIGHT * 0.05) for l in example_lines],
                lag_ratio=0.1,
            ),
            run_time=0.6,
        )
        self.play(FadeIn(chain, scale=1.3), run_time=0.3)
        self.wait(4.0)

        # Transition: break free → adaptive agent
        # Arrow to the right side
        evolve_arrow = Arrow(
            LEFT * 0.8,
            RIGHT * 0.8,
            buff=0,
            color=GREEN,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )
        evolve_arrow.move_to(ORIGIN + UP * 0.5)

        self.play(GrowArrow(evolve_arrow), run_time=0.4)

        # RIGHT: adaptive agent with multiple environments
        agent_icon = make_svg_icon("robot.svg", color=GREEN, height=0.7)
        agent_icon.move_to(RIGHT * 3.0 + UP * 0.5)

        # Environment circles around the adaptive agent
        env_configs = [
            ("browser.svg", TEAL, 60),
            ("gear.svg", GOLD, 140),
            ("document.svg", ACCENT, 220),
            ("database.svg", PURPLE, 300),
        ]

        env_radius = 1.3
        env_icons = VGroup()
        for fname, color, angle_deg in env_configs:
            angle = angle_deg * PI / 180
            pos = agent_icon.get_center() + env_radius * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            icon = make_svg_icon(fname, color=color, height=0.35)
            icon.move_to(pos)
            env_icons.add(icon)

        # Adaptive ring
        adapt_ring = Circle(
            radius=env_radius + 0.2,
            color=GREEN,
            stroke_width=1.5,
            stroke_opacity=0.3,
        )
        adapt_ring.move_to(agent_icon.get_center())

        # "A stronger agent should adapt to new environments"
        self.play(
            FadeIn(agent_icon, scale=0.7),
            Create(adapt_ring),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(ei, scale=0.5) for ei in env_icons],
                lag_ratio=0.1,
            ),
            run_time=0.6,
        )

        # Agent "reaches out" to each environment
        for ei in env_icons:
            conn = Line(
                agent_icon.get_center(),
                ei.get_center(),
                color=GREEN,
                stroke_width=1.2,
                stroke_opacity=0.4,
            )
            self.play(Create(conn), run_time=0.15)

        # Pulse to show adaptation
        agent_pulse = agent_icon.copy().set_stroke(GREEN, width=3, opacity=0.6)
        self.play(FadeIn(agent_pulse), run_time=0.1)
        self.play(agent_pulse.animate.scale(1.4).set_opacity(0), run_time=0.4)
        self.remove(agent_pulse)

        adapt_label = Text("adapts to new environments", font_size=13, color=GREEN)
        adapt_label.move_to(RIGHT * 3.0 + DOWN * 1.8)
        self.play(FadeIn(adapt_label, shift=UP * 0.05), run_time=0.3)

        self.wait(4.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

    # ==================================================================
    #  PART 5 — Closing: Combining Everything
    #  "language + perception + action + learning" → agent
    #  "A chatbot answers. An agent acts."
    # ==================================================================

    def _part_5_closing(self):
        # Four pillars converging into one
        pillars = [
            ("language", ACCENT, "chat-bubble.svg"),
            ("perception", GOLD, "eye.svg"),
            ("action", GREEN, "hand-pointer.svg"),
            ("learning", PURPLE, "brain.svg"),
        ]

        pillar_groups = VGroup()
        pillar_positions = [
            LEFT * 4.0 + UP * 1.0,
            LEFT * 1.5 + UP * 1.0,
            RIGHT * 1.5 + UP * 1.0,
            RIGHT * 4.0 + UP * 1.0,
        ]

        for (label_text, color, icon_file), pos in zip(pillars, pillar_positions):
            icon = make_svg_icon(icon_file, color=color, height=0.6)
            icon.move_to(pos)
            label = Text(label_text, font_size=13, color=color)
            label.next_to(icon, DOWN, buff=0.2)
            pillar_groups.add(VGroup(icon, label))

        # "The future of agents is not just bigger language models."
        future_text = Text(
            "the future is not just bigger models",
            font_size=18,
            color=DIM,
        )
        future_text.move_to(UP * 2.8)
        self.play(FadeIn(future_text, shift=DOWN * 0.05), run_time=0.5)
        self.wait(3.0)

        # "It is about combining language, perception, action, and learning."
        self.play(
            LaggedStart(
                *[FadeIn(pg, shift=DOWN * 0.15) for pg in pillar_groups],
                lag_ratio=0.15,
            ),
            run_time=1.0,
        )
        self.wait(3.0)

        # Convergence point
        center_target = ORIGIN + DOWN * 1.0
        converge_hex = make_hexagon(side_length=0.8, color=WHITE, fill_opacity=0.1)
        converge_hex.move_to(center_target)

        # Arrows from each pillar to center
        conv_arrows = VGroup()
        for pos in pillar_positions:
            direction = center_target - pos
            direction_norm = direction / np.linalg.norm(direction)
            arr = Arrow(
                pos + direction_norm * 0.7,
                center_target - direction_norm * 0.9,
                buff=0,
                color=DIM,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.12,
            )
            conv_arrows.add(arr)

        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in conv_arrows],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.play(FadeIn(converge_hex, scale=0.5), run_time=0.4)

        # Agent emerges
        agent_label = Text("agent", font_size=18, color=WHITE, weight=BOLD)
        agent_label.move_to(converge_hex.get_center())
        self.play(FadeIn(agent_label, scale=1.2), run_time=0.4)

        # Glow pulse
        glow = converge_hex.copy().set_stroke(WHITE, width=4, opacity=0.6)
        self.play(FadeIn(glow), run_time=0.12)
        self.play(glow.animate.scale(1.4).set_opacity(0), run_time=0.5)
        self.remove(glow)

        self.wait(3.0)

        # Fade everything out for the final comparison
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ── Final comparison: "A chatbot answers. An agent acts." ──
        # Left: chatbot (static, just a bubble)
        chatbot_bubble = RoundedRectangle(
            width=3.0,
            height=2.0,
            corner_radius=0.2,
            color=DIM2,
            stroke_width=1.5,
            fill_color=DIM2,
            fill_opacity=0.06,
        )
        chatbot_bubble.move_to(LEFT * 3.0)

        chatbot_icon = make_svg_icon("chat-bubble.svg", color=DIM, height=0.7)
        chatbot_icon.move_to(chatbot_bubble.get_center() + UP * 0.2)

        chatbot_label = Text("chatbot", font_size=16, color=DIM)
        chatbot_label.move_to(chatbot_bubble.get_center() + DOWN * 0.55)

        chatbot_verb = Text("answers", font_size=20, color=DIM, weight=BOLD)
        chatbot_verb.next_to(chatbot_bubble, DOWN, buff=0.4)

        # Right: agent (active, dynamic)
        agent_box = RoundedRectangle(
            width=3.0,
            height=2.0,
            corner_radius=0.2,
            color=ACCENT,
            stroke_width=2.5,
            fill_color=ACCENT,
            fill_opacity=0.06,
        )
        agent_box.move_to(RIGHT * 3.0)

        agent_icon = make_svg_icon("robot.svg", color=ACCENT, height=0.7)
        agent_icon.move_to(agent_box.get_center() + UP * 0.2)

        agent_final_label = Text("agent", font_size=16, color=ACCENT)
        agent_final_label.move_to(agent_box.get_center() + DOWN * 0.55)

        agent_verb = Text("acts", font_size=20, color=ACCENT, weight=BOLD)
        agent_verb.next_to(agent_box, DOWN, buff=0.4)

        # Animate comparison
        self.play(
            FadeIn(chatbot_bubble, scale=0.9),
            FadeIn(chatbot_icon, scale=0.8),
            FadeIn(chatbot_label),
            run_time=0.5,
        )
        self.play(FadeIn(chatbot_verb, shift=UP * 0.1), run_time=0.4)
        self.wait(2.0)

        self.play(
            FadeIn(agent_box, scale=0.9),
            FadeIn(agent_icon, scale=0.8),
            FadeIn(agent_final_label),
            run_time=0.5,
        )
        self.play(FadeIn(agent_verb, shift=UP * 0.1), run_time=0.4)

        # Agent side pulses with energy
        agent_glow = agent_box.copy().set_stroke(ACCENT, width=4, opacity=0.6)
        self.play(FadeIn(agent_glow), run_time=0.15)
        self.play(agent_glow.animate.scale(1.08).set_opacity(0), run_time=0.5)
        self.remove(agent_glow)

        # Small action dots emanating from agent
        for _ in range(3):
            dot = Dot(
                agent_box.get_center(),
                radius=0.06,
                color=ACCENT,
                fill_opacity=0.7,
            )
            target = agent_box.get_center() + np.array(
                [np.random.uniform(-1.5, 1.5), np.random.uniform(-1.0, 1.0), 0]
            )
            self.play(FadeIn(dot, scale=0.5), run_time=0.05)
            self.play(
                dot.animate.move_to(target).set_opacity(0),
                run_time=0.3,
                rate_func=smooth,
            )
            self.remove(dot)

        # "A chatbot answers. An agent acts."
        self.wait(4.0)

        # Final fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(1.0)
