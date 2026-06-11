import numpy as np

from utils.manim_compat import *
from utils.mobjects import (
    make_card,
    make_code_lines,
    make_hexagon,
    make_pill,
    make_svg_icon,
    make_token_box,
)
from utils.theme import *


class AgentEvaluation(Scene):
    def construct(self):
        self.camera.background_color = BG

        self._part_1_evaluating_the_loop()
        self._part_2_no_single_metric()
        self._part_3_benchmark_showcase()
        self._part_4_closing()

    # ==================================================================
    #  PART 1 — Evaluating the Loop
    #  The agent loop reappears, a magnifying glass sweeps over it,
    #  and a checklist of evaluation criteria appears
    # ==================================================================

    def _part_1_evaluating_the_loop(self):
        # ── Central hexagon: LLM core (reuse from scene_9) ──
        llm_hex = make_hexagon(side_length=0.7, color=ACCENT, fill_opacity=0.1)
        llm_hex.move_to(LEFT * 2.5)
        llm_label = Text("LLM", font_size=14, color=ACCENT)
        llm_label.move_to(llm_hex.get_center())

        # Orbit ring
        orbit_ring = Circle(
            radius=1.6,
            color=DIM2,
            stroke_width=0.6,
            stroke_opacity=0.25,
        )
        orbit_ring.move_to(llm_hex.get_center())

        # Loop arrow (act-observe-reason cycle)
        loop_circle = Circle(
            radius=1.0,
            color=GREEN,
            stroke_width=2.0,
            stroke_opacity=0.5,
        )
        loop_circle.move_to(llm_hex.get_center())

        # Directional arrow tips at quarters
        tip_angles = [PI / 4, 3 * PI / 4, -3 * PI / 4, -PI / 4]
        tip_arrows = VGroup()
        for ta in tip_angles:
            pt = llm_hex.get_center() + 1.0 * np.array([np.cos(ta), np.sin(ta), 0])
            tangent = np.array([-np.sin(ta), np.cos(ta), 0])
            tip = Arrow(
                pt - 0.12 * tangent,
                pt + 0.12 * tangent,
                buff=0,
                color=GREEN,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.6,
            )
            tip_arrows.add(tip)

        # Environment icons around orbit
        env_configs = [
            ("document.svg", ACCENT, PI / 2),
            ("gear.svg", GOLD, -PI / 6),
            ("browser.svg", TEAL, -PI / 2 - PI / 3),
        ]

        env_icons = VGroup()
        for fname, clr, angle in env_configs:
            icon = make_svg_icon(fname, color=clr, height=0.45)
            pos = llm_hex.get_center() + 1.6 * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            icon.move_to(pos)
            env_icons.add(icon)

        # Animate the loop diagram
        self.play(
            FadeIn(llm_hex, scale=0.7),
            FadeIn(llm_label, scale=0.8),
            run_time=0.5,
        )
        self.play(
            FadeIn(orbit_ring),
            LaggedStart(
                *[FadeIn(ei, scale=0.5) for ei in env_icons],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.play(
            Create(loop_circle),
            LaggedStart(
                *[GrowArrow(ta) for ta in tip_arrows],
                lag_ratio=0.1,
            ),
            run_time=0.7,
        )
        # [23:53] How do we evaluate agents? Traditional metrics don't capture the full picture
        self.wait(2.0)

        # ── Magnifying glass (eye icon) sweeps over the loop ──
        eye = make_svg_icon("eye.svg", color=GOLD, height=0.8)
        eye.move_to(llm_hex.get_center() + UP * 2.5 + LEFT * 1.0)

        # Magnifying circle

        self.play(FadeIn(eye, scale=0.6), run_time=0.4)

        # Sweep down over the loop
        self.play(
            eye.animate.move_to(llm_hex.get_center()),
            run_time=0.8,
            rate_func=smooth,
        )

        # Move magnifying glass aside
        self.play(
            eye.animate.move_to(LEFT * 2.5 + DOWN * 2.5).scale(0.5).set_opacity(0.3),
            run_time=0.5,
        )

        # ── Checklist appears on the right ──
        checklist_items = [
            ("✓", "Understand task?", "brain.svg", GREEN),
            ("✓", "Right action?", "gear.svg", GREEN),
            ("✓", "Right tool?", "hand-pointer.svg", GREEN),
            ("✗", "Final answer only?", "chat-bubble.svg", RED),
        ]

        checklist = VGroup()
        for mark, desc, icon_file, mark_color in checklist_items:
            icon = make_svg_icon(icon_file, color=DIM, height=0.35)
            mark_text = Text(mark, font_size=20, color=mark_color, weight=BOLD)
            desc_text = Text(desc, font_size=14, color=WHITE)

            row = VGroup(mark_text, icon, desc_text)
            row.arrange(RIGHT, buff=0.2)
            checklist.add(row)

        checklist.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        checklist.move_to(RIGHT * 2.8)

        # Animate checklist rows one by one
        for i, row in enumerate(checklist):
            self.play(
                FadeIn(row, shift=LEFT * 0.15),
                run_time=0.4,
            )
            if i < 3:
                # Brief flash for checkmark
                self.play(
                    Flash(
                        row[0].get_center(),
                        color=GREEN,
                        flash_radius=0.2,
                        num_lines=6,
                        line_length=0.08,
                    ),
                    run_time=0.25,
                )
            else:
                # Red X gets a different emphasis
                self.play(
                    Flash(
                        row[0].get_center(),
                        color=RED,
                        flash_radius=0.2,
                        num_lines=6,
                        line_length=0.08,
                    ),
                    run_time=0.25,
                )
            # [24:03] Understand task? Right action? Right tool?
            self.wait(1.0)

        # [24:08] Checklist: multiple dimensions to evaluate
        self.wait(3.0)

        # Highlight the last row with a surrounding rect to show insufficiency
        insuff_rect = SurroundingRectangle(
            checklist[-1],
            color=RED,
            buff=0.12,
            corner_radius=0.08,
            stroke_width=1.5,
            fill_color=RED,
            fill_opacity=0.05,
        )
        self.play(Create(insuff_rect), run_time=0.4)

        not_enough = Text("not enough", font_size=12, color=RED)
        not_enough.next_to(insuff_rect, DOWN, buff=0.15)
        self.play(FadeIn(not_enough, shift=UP * 0.05), run_time=0.3)
        # [24:13] Not enough to just check the final answer
        self.wait(4.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 2 — No Single Metric
    #  A single score appears, then shatters into fragments
    # ==================================================================

    def _part_2_no_single_metric(self):
        # ── Big score number ──
        score = Text("87%", font_size=72, color=GOLD, weight=BOLD)
        score.move_to(ORIGIN)

        score_label = Text("accuracy", font_size=18, color=DIM)
        score_label.next_to(score, DOWN, buff=0.3)

        self.play(
            FadeIn(score, scale=1.3),
            FadeIn(score_label, shift=UP * 0.1),
            run_time=0.6,
        )
        # [24:18] A single score is not enough
        self.wait(2.0)

        # ── Red X overlay ──
        x1 = Line(
            score.get_corner(UL) + DR * 0.15,
            score.get_corner(DR) + UL * 0.15,
            color=RED,
            stroke_width=5,
        )
        x2 = Line(
            score.get_corner(UR) + DL * 0.15,
            score.get_corner(DL) + UR * 0.15,
            color=RED,
            stroke_width=5,
        )

        self.play(Create(x1), Create(x2), run_time=0.4)
        self.play(
            Flash(ORIGIN, color=RED, flash_radius=1.0, num_lines=12),
            run_time=0.4,
        )
        self.wait(1.0)

        # ── Shatter into multiple metric fragments ──
        metric_names = [
            ("task accuracy", ACCENT),
            ("tool precision", TEAL),
            ("reasoning steps", GOLD),
            ("action F1", GREEN),
            ("success rate", PURPLE),
            ("efficiency", ORANGE),
        ]

        fragments = VGroup()
        angles = [PI / 3, 2 * PI / 3, PI, 4 * PI / 3, 5 * PI / 3, 0]
        for (name, color), angle in zip(metric_names, angles):
            frag = make_pill(name, color=color, font_size=12, fill_opacity=0.12)
            target_pos = ORIGIN + 2.5 * np.array([np.cos(angle), np.sin(angle), 0])
            frag.move_to(ORIGIN)
            frag.target_pos = target_pos
            fragments.add(frag)

        # Animate the shatter
        self.play(
            FadeOut(score),
            FadeOut(score_label),
            FadeOut(x1),
            FadeOut(x2),
            *[frag.animate.move_to(frag.target_pos) for frag in fragments],
            run_time=0.7,
            rate_func=smooth,
        )

        # Brief pause showing all fragments
        # [24:23] Need multiple metrics: accuracy, precision, reasoning steps
        self.wait(2.0)

        # Connecting dashed lines from center to each fragment
        center_dot = Dot(ORIGIN, radius=0.06, color=DIM, fill_opacity=0.5)
        conn_lines = VGroup()
        for frag in fragments:
            line = DashedLine(
                ORIGIN,
                frag.get_center(),
                color=DIM2,
                stroke_width=0.8,
                stroke_opacity=0.3,
                dash_length=0.08,
            )
            conn_lines.add(line)

        self.play(
            FadeIn(center_dot),
            LaggedStart(*[Create(l) for l in conn_lines], lag_ratio=0.05),
            run_time=0.5,
        )
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  PART 3 — Benchmark Showcase
    #  Four cards, each with an illustrative mini-scene
    # ==================================================================

    def _part_3_benchmark_showcase(self):
        # Store all cards for the final 2×2 grid
        all_cards = []

        # ── 3a. HotPotQA — Multi-hop Reasoning ──
        card_hp = self._show_hotpotqa()
        all_cards.append(card_hp)

        # ── 3b. WebShop — E-commerce Agent ──
        card_ws = self._show_webshop()
        all_cards.append(card_ws)

        # ── 3c. ToolBench — Tool Use ──
        card_tb = self._show_toolbench()
        all_cards.append(card_tb)

        # ── 3d. SWE-bench — Software Engineering ──
        card_sw = self._show_swebench()
        all_cards.append(card_sw)

        # ── Arrange into 2×2 grid ──
        # All cards are currently off-screen or faded. Bring them all back.
        grid = VGroup(*all_cards)
        grid.arrange_in_grid(rows=2, cols=2, buff=0.35)
        grid.scale_to_fit_width(5)
        grid.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[FadeIn(card, scale=0.85) for card in all_cards],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        # [24:33] Benchmark environments: HotPotQA, WebShop, ToolBench, SWE-bench
        self.wait(3.0)

        # Store for part 4
        self._benchmark_grid = grid

    def _show_hotpotqa(self):
        """HotPotQA — Multi-hop Reasoning card."""
        card = make_card("HotPotQA", ACCENT)
        card.move_to(ORIGIN)

        # Illustration: two documents connected by a dashed path with brain
        doc_a = make_svg_icon("document.svg", color=ACCENT, height=0.6)
        doc_a.move_to(card.get_center() + LEFT * 0.9 + DOWN * 0.15)

        doc_b = make_svg_icon("document.svg", color=ACCENT, height=0.6)
        doc_b.move_to(card.get_center() + RIGHT * 0.9 + DOWN * 0.15)

        brain = make_svg_icon("brain.svg", color=GOLD, height=0.5)
        brain.move_to(card.get_center() + DOWN * 0.15)

        # Dashed connecting paths
        path_a = DashedLine(
            doc_a.get_right(),
            brain.get_left(),
            color=ACCENT,
            stroke_width=1.2,
            dash_length=0.06,
        )
        path_b = DashedLine(
            brain.get_right(),
            doc_b.get_left(),
            color=ACCENT,
            stroke_width=1.2,
            dash_length=0.06,
        )

        # Label
        desc = Text("multi-hop reasoning", font_size=16, color=DIM)
        desc.move_to(card.get_bottom() + DOWN * 0.35)

        # Info dots traveling the path
        dot_a = Dot(doc_a.get_right(), radius=0.05, color=GOLD, fill_opacity=0.8)
        dot_b = Dot(brain.get_right(), radius=0.05, color=GOLD, fill_opacity=0.8)

        illustration = VGroup(doc_a, doc_b, brain, path_a, path_b, desc)

        # Animate
        self.play(FadeIn(card, scale=0.9), run_time=0.5)
        self.play(
            FadeIn(doc_a, shift=RIGHT * 0.1),
            FadeIn(doc_b, shift=LEFT * 0.1),
            run_time=0.4,
        )
        self.play(
            Create(path_a),
            Create(path_b),
            FadeIn(brain, scale=0.7),
            run_time=0.5,
        )

        # Dots travel along paths
        self.play(FadeIn(dot_a, scale=0.5), run_time=0.1)
        self.play(
            dot_a.animate.move_to(brain.get_center()),
            run_time=0.35,
            rate_func=smooth,
        )
        self.play(FadeOut(dot_a), FadeIn(dot_b, scale=0.5), run_time=0.1)
        self.play(
            dot_b.animate.move_to(doc_b.get_center()),
            run_time=0.35,
            rate_func=smooth,
        )
        self.play(FadeOut(dot_b), run_time=0.1)

        self.play(FadeIn(desc, shift=UP * 0.05), run_time=0.3)
        # [24:43] HotPotQA: multi-hop reasoning
        self.wait(3.0)

        # Build the complete card VGroup for grid
        full_card = VGroup(card, illustration)
        self.play(FadeOut(*self.mobjects), run_time=0.5)

        return full_card.copy()

    def _show_webshop(self):
        """WebShop — E-commerce Agent card."""
        card = make_card("WebShop", GOLD)
        card.move_to(ORIGIN)

        # Browser icon at top
        browser = make_svg_icon("browser.svg", color=GOLD, height=0.45)
        browser.move_to(card.get_center() + UP * 0.3)

        # Product boxes in a row
        products = VGroup()
        for i in range(3):
            prod_box = RoundedRectangle(
                width=0.55,
                height=0.65,
                corner_radius=0.06,
                color=GOLD if i == 1 else DIM2,
                stroke_width=1.5 if i == 1 else 1.0,
                fill_color=GOLD if i == 1 else DIM2,
                fill_opacity=0.1 if i == 1 else 0.04,
            )
            # Star rating dots
            stars = VGroup()
            n_stars = [2, 4, 3][i]
            for s in range(n_stars):
                star = Dot(
                    radius=0.025, color=GOLD if i == 1 else DIM, fill_opacity=0.6
                )
                stars.add(star)
            stars.arrange(RIGHT, buff=0.04)
            stars.move_to(prod_box.get_bottom() + UP * 0.12)

            prod = VGroup(prod_box, stars)
            products.add(prod)

        products.arrange(RIGHT, buff=0.2)
        products.move_to(card.get_center() + DOWN * 0.35)

        # Hand pointer selecting middle product
        hand = make_svg_icon("hand-pointer.svg", color=GOLD, height=0.4)
        hand.move_to(products[1].get_bottom() + DOWN * 0.3)

        # Selection arrow
        sel_arrow = Arrow(
            hand.get_top(),
            products[1].get_bottom(),
            buff=0.05,
            color=GOLD,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.2,
        )

        desc = Text("e-commerce agent", font_size=16, color=DIM)
        desc.move_to(card.get_bottom() + DOWN * 0.35)

        illustration = VGroup(browser, products, hand, sel_arrow, desc)

        # Animate
        self.play(FadeIn(card, scale=0.9), run_time=0.5)
        self.play(FadeIn(browser, shift=DOWN * 0.1), run_time=0.3)
        self.play(
            LaggedStart(
                *[FadeIn(p, scale=0.8) for p in products],
                lag_ratio=0.1,
            ),
            run_time=0.5,
        )
        self.play(
            FadeIn(hand, shift=UP * 0.1),
            GrowArrow(sel_arrow),
            run_time=0.4,
        )

        # Highlight selected product
        sel_glow = products[1][0].copy().set_stroke(GOLD, width=3, opacity=0.6)
        self.play(FadeIn(sel_glow), run_time=0.15)
        self.play(FadeOut(sel_glow), run_time=0.2)

        self.play(FadeIn(desc, shift=UP * 0.05), run_time=0.3)
        # [24:50] WebShop: e-commerce browsing agent
        self.wait(3.0)

        full_card = VGroup(card, illustration)
        self.play(FadeOut(*self.mobjects), run_time=0.5)

        return full_card.copy()

    def _show_toolbench(self):
        """ToolBench — Tool Use card."""
        card = make_card("ToolBench", TEAL)
        card.move_to(ORIGIN)

        # Robot icon in center
        robot = make_svg_icon("robot.svg", color=WHITE, height=0.6)
        robot.move_to(card.get_center() + DOWN * 0.2)

        # Tool icons orbiting
        tool_configs = [
            ("gear.svg", TEAL, PI / 2),
            ("document.svg", DIM, PI / 2 + 2 * PI / 5),
            ("browser.svg", DIM, PI / 2 + 4 * PI / 5),
            ("email.svg", DIM, PI / 2 + 6 * PI / 5),
            ("database.svg", DIM, PI / 2 + 8 * PI / 5),
        ]

        tool_icons = VGroup()
        tool_radius = 0.85
        for fname, clr, angle in tool_configs:
            icon = make_svg_icon(fname, color=clr, height=0.3)
            pos = (
                robot.get_center()
                + UP * 0.05
                + tool_radius * np.array([np.cos(angle), np.sin(angle), 0])
            )
            icon.move_to(pos)
            tool_icons.add(icon)

        # Arrow from robot to the highlighted tool (gear — the correct one)
        correct_arrow = Arrow(
            robot.get_center() + 0.3 * np.array([np.cos(PI / 2), np.sin(PI / 2), 0]),
            tool_icons[0].get_center()
            - 0.15 * np.array([np.cos(PI / 2), np.sin(PI / 2), 0]),
            buff=0,
            color=TEAL,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )

        desc = Text("tool selection", font_size=16, color=DIM)
        desc.move_to(card.get_bottom() + DOWN * 0.35)

        illustration = VGroup(robot, tool_icons, correct_arrow, desc)

        # Animate
        self.play(FadeIn(card, scale=0.9), run_time=0.5)
        self.play(FadeIn(robot, scale=0.8), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(ti, scale=0.5) for ti in tool_icons],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )

        # Robot "thinks" — pulse
        robot_pulse = robot.copy().set_stroke(TEAL, width=3, opacity=0.5)
        self.play(FadeIn(robot_pulse), run_time=0.12)
        self.play(FadeOut(robot_pulse), run_time=0.2)

        # Arrow points to the correct tool
        self.play(GrowArrow(correct_arrow), run_time=0.4)

        # Correct tool glows
        self.play(
            Flash(
                tool_icons[0].get_center(),
                color=TEAL,
                flash_radius=0.25,
                num_lines=6,
                line_length=0.08,
            ),
            tool_icons[0].animate.set_color(TEAL),
            run_time=0.4,
        )

        self.play(FadeIn(desc, shift=UP * 0.05), run_time=0.3)
        # [24:57] ToolBench: tool selection and use
        self.wait(3.0)

        full_card = VGroup(card, illustration)
        self.play(FadeOut(*self.mobjects), run_time=0.5)

        return full_card.copy()

    def _show_swebench(self):
        """SWE-bench — Software Engineering card."""
        card = make_card("SWE-bench", GREEN)
        card.move_to(ORIGIN)

        # Code document
        doc_bg = RoundedRectangle(
            width=1.8,
            height=1.2,
            corner_radius=0.08,
            color=DIM2,
            stroke_width=1.2,
            fill_color=DIM2,
            fill_opacity=0.06,
        )
        doc_bg.move_to(card.get_center() + UP * 0.05)

        # Code lines
        code_lines = make_code_lines(
            doc_bg.get_center(), n_lines=5, max_width=1.4, color=DIM
        )

        # Bug dot (red) on third line
        bug_dot = Dot(
            code_lines[2].get_right() + RIGHT * 0.15,
            radius=0.07,
            color=RED,
            fill_opacity=0.9,
        )
        bug_label = Text("bug", font_size=9, color=RED)
        bug_label.next_to(bug_dot, RIGHT, buff=0.08)

        # Gear icon overlaying — representing the fixing process
        fix_gear = make_svg_icon("gear.svg", color=GREEN, height=0.35)
        fix_gear.move_to(doc_bg.get_corner(DR) + UL * 0.25)
        fix_gear.set_opacity(0)

        desc = Text("code repair", font_size=16, color=DIM)
        desc.move_to(card.get_bottom() + DOWN * 0.35)

        illustration = VGroup(doc_bg, code_lines, bug_dot, bug_label, fix_gear, desc)

        # Animate
        self.play(FadeIn(card, scale=0.9), run_time=0.5)
        self.play(
            FadeIn(doc_bg, scale=0.9),
            LaggedStart(
                *[FadeIn(l, shift=RIGHT * 0.1) for l in code_lines],
                lag_ratio=0.06,
            ),
            run_time=0.5,
        )

        # Bug appears
        self.play(
            FadeIn(bug_dot, scale=1.5),
            FadeIn(bug_label),
            Flash(
                bug_dot.get_center(),
                color=RED,
                flash_radius=0.2,
                num_lines=6,
                line_length=0.06,
            ),
            run_time=0.4,
        )
        self.wait(1.0)

        # Fix process — gear spins in, bug turns green
        self.play(
            fix_gear.animate.set_opacity(1),
            Rotate(fix_gear, angle=PI / 2),
            run_time=0.5,
        )

        # Bug fixed — dot turns green
        fixed_dot = Dot(
            bug_dot.get_center(),
            radius=0.07,
            color=GREEN,
            fill_opacity=0.9,
        )
        fixed_label = Text("fix", font_size=9, color=GREEN)
        fixed_label.next_to(fixed_dot, RIGHT, buff=0.08)

        self.play(
            ReplacementTransform(bug_dot, fixed_dot),
            ReplacementTransform(bug_label, fixed_label),
            Flash(
                fixed_dot.get_center(),
                color=GREEN,
                flash_radius=0.2,
                num_lines=6,
                line_length=0.06,
            ),
            run_time=0.4,
        )

        self.play(FadeIn(desc, shift=UP * 0.05), run_time=0.3)
        # [25:05] SWE-bench: code repair and debugging
        self.wait(3.0)

        full_card = VGroup(card, illustration)
        self.play(FadeOut(*self.mobjects), run_time=0.5)

        return full_card.copy()

    # ==================================================================
    #  PART 4 — Closing
    #  2×2 grid pulses in sequence, then fades out
    # ==================================================================

    def _part_4_closing(self):
        grid = self._benchmark_grid
        cards = grid.submobjects

        # ── Sequential pulse on each card ──
        pulse_colors = [ACCENT, GOLD, TEAL, GREEN]

        for card, color in zip(cards, pulse_colors):
            # Get the outer card rectangle (first submobject's first submobject)
            card_rect = card[0][
                0
            ]  # VGroup(card, illustration) -> card -> RoundedRectangle
            glow = SurroundingRectangle(
                card,
                color=color,
                buff=0.08,
                corner_radius=0.15,
                stroke_width=2.5,
                fill_color=color,
                fill_opacity=0.04,
            )
            pulse_rect = glow.copy().set_stroke(color, width=3)

            self.play(Create(glow), run_time=0.3)
            self.play(
                pulse_rect.animate.scale(1.05).set_opacity(0),
                run_time=0.4,
            )
            self.remove(pulse_rect)
            self.play(FadeOut(glow), run_time=0.2)

        # [25:15] Each benchmark tests different abilities
        self.wait(3.0)

        # ── Brace grouping all cards ──
        brace = Brace(grid, DOWN, color=DIM)
        brace_label = Text(
            "different benchmarks test different abilities",
            font_size=16,
            color=DIM,
        )
        brace_label.next_to(brace, DOWN, buff=0.15)

        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_label, shift=UP * 0.08),
            run_time=0.6,
        )
        # [25:22] Different benchmarks test different abilities
        self.wait(3.0)

        # ── Final fade out ──
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.3)
