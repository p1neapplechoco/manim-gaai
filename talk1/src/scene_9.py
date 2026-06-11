import numpy as np

from utils.manim_compat import *
from utils.mobjects import make_hexagon, make_pill, make_svg_icon, make_token_box
from utils.theme import *


MODEL_DATA = [
    # (year, name, params_billions, is_slm)
    (2018.0, "ELMo", 0.093, False),
    (2018.5, "GPT-1", 0.117, False),
    (2019.0, "GPT-2", 1.5, False),
    (2020.0, "GPT-3", 175, False),
    (2021.0, "Gopher", 280, False),
    (2022.0, "PaLM", 540, False),
    (2023.0, "GPT-4", 1800, False),
    # SLMs
    (2022.5, "DistilBERT", 0.066, True),
    (2023.5, "Phi-2", 2.7, True),
    (2024.0, "Gemma", 2.0, True),
]


class ThreeRolesToAgentLoop(Scene):
    def construct(self):
        self.camera.background_color = BG

        self._scene_1_three_roles()
        self._scene_2_scale_of_models()
        self._scene_3_chatbot_vs_agent()
        self._scene_4_agent_loop()
        self._scene_5_closing()

    # ==================================================================
    #  SCENE 1 — The Three Roles
    # ==================================================================

    def _scene_1_three_roles(self):
        # ── Three icons: document (Work), calendar (Personal), star (Creative)
        doc_icon = make_svg_icon("document.svg", color=ACCENT, height=1.1)
        cal_icon = make_svg_icon("calendar.svg", color=GOLD, height=1.1)
        star_icon = make_svg_icon("star.svg", color=PURPLE, height=1.1)

        icons = VGroup(doc_icon, cal_icon, star_icon)
        icons.arrange(RIGHT, buff=2.8)
        icons.move_to(UP * 0.5)

        labels = VGroup(
            Text("WORK", font_size=18, color=ACCENT),
            Text("PERSONAL", font_size=18, color=GOLD),
            Text("CREATIVE", font_size=18, color=PURPLE),
        )
        for label, icon in zip(labels, icons):
            label.next_to(icon, DOWN, buff=0.5)

        # Subtle environment rings around each icon
        rings = VGroup()
        ring_colors = [ACCENT, GOLD, PURPLE]
        for icon, rc in zip(icons, ring_colors):
            ring = Circle(
                radius=0.8,
                color=rc,
                stroke_width=5.0,
                stroke_opacity=0.3,
                fill_opacity=0,
            )
            ring.move_to(icon.get_center())
            rings.add(ring)

        # ── Small descriptive sub-icons beneath each label ──
        # Work: email, document, gear
        work_sub_icons = VGroup(
            make_svg_icon("email.svg", color=ACCENT, height=0.35),
            make_svg_icon("document.svg", color=ACCENT, height=0.35),
            make_svg_icon("gear.svg", color=ACCENT, height=0.35),
        )
        work_sub_icons.arrange(RIGHT, buff=0.2)
        work_sub_icons.next_to(labels[0], DOWN, buff=0.25)
        work_sub_icons.set_opacity(0.5)

        # Personal: calendar, person
        personal_sub_icons = VGroup(
            make_svg_icon("calendar.svg", color=GOLD, height=0.35),
            make_svg_icon("person.svg", color=GOLD, height=0.35),
        )
        personal_sub_icons.arrange(RIGHT, buff=0.2)
        personal_sub_icons.next_to(labels[1], DOWN, buff=0.25)
        personal_sub_icons.set_opacity(0.5)

        # Creative: star, brain
        creative_sub_icons = VGroup(
            make_svg_icon("star.svg", color=PURPLE, height=0.35),
            make_svg_icon("brain.svg", color=PURPLE, height=0.35),
        )
        creative_sub_icons.arrange(RIGHT, buff=0.2)
        creative_sub_icons.next_to(labels[2], DOWN, buff=0.25)
        creative_sub_icons.set_opacity(0.5)

        all_sub_icons = VGroup(work_sub_icons, personal_sub_icons, creative_sub_icons)

        # ── Animate: pulse in one at a time ──
        for icon, label in zip(icons, labels):
            self.play(
                FadeIn(icon, scale=0.7),
                run_time=0.5,
            )
            self.play(
                FadeIn(label, shift=UP * 0.08),
                run_time=0.35,
            )
            # [20:18] Three broad categories of agents
            self.wait(3.0)

        # [20:25] Work, personal, and creative agents
        self.wait(3.0)

        # Show environment rings
        self.play(
            LaggedStart(*[Create(ring) for ring in rings], lag_ratio=0.15),
            run_time=0.7,
        )

        # Show sub-icons
        self.play(
            LaggedStart(
                *[FadeIn(si, shift=UP * 0.05) for si in all_sub_icons],
                lag_ratio=0.12,
            ),
            run_time=0.6,
        )
        # [20:37] Each agent adapts its role based on task and environment
        self.wait(5.0)

        # Icons drift slightly apart with rings growing
        self.play(
            icons[0].animate.shift(LEFT * 0.3),
            icons[2].animate.shift(RIGHT * 0.3),
            labels[0].animate.shift(LEFT * 0.3),
            labels[2].animate.shift(RIGHT * 0.3),
            rings[0].animate.shift(LEFT * 0.3).scale(1.1),
            rings[2].animate.shift(RIGHT * 0.3).scale(1.1),
            work_sub_icons.animate.shift(LEFT * 0.3),
            creative_sub_icons.animate.shift(RIGHT * 0.3),
            run_time=0.8,
            rate_func=smooth,
        )
        # [20:51] The role is not fixed — determined by the environment
        self.wait(8.0)

        # Fade out
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  SCENE 2 — The Scale of Models
    # ==================================================================

    def _scene_2_scale_of_models(self):
        # ── Timeline arrow ──
        timeline_y = DOWN * 0.5
        tl_start = LEFT * 6.0 + timeline_y
        tl_end = RIGHT * 6.0 + timeline_y

        timeline = Arrow(
            tl_start,
            tl_end,
            buff=0,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.02,
        )

        # Year markers
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
        year_marks = VGroup()
        for year in years:
            t = (year - 2017.5) / 7.0
            x = tl_start[0] + t * (tl_end[0] - tl_start[0])
            tick = Line(
                np.array([x, timeline_y[1] - 0.1, 0]),
                np.array([x, timeline_y[1] + 0.1, 0]),
                color=DIM2,
                stroke_width=1.0,
            )
            label = Text(str(year), font_size=11, color=DIM2)
            label.next_to(tick, DOWN, buff=0.12)
            year_marks.add(VGroup(tick, label))

        self.play(GrowArrow(timeline), run_time=0.6)
        self.play(
            LaggedStart(
                *[FadeIn(ym, shift=UP * 0.05) for ym in year_marks],
                lag_ratio=0.06,
            ),
            run_time=0.5,
        )
        # [21:12] LLM parameter growth over years
        self.wait(3.0)

        # ── Plot model dots ──
        # Size proportional to log of parameter count
        def year_to_x(year):
            t = (year - 2017.5) / 7.0
            return tl_start[0] + t * (tl_end[0] - tl_start[0])

        def params_to_radius(params_b):
            # log scale: 0.093B → small, 1800B → large
            return 0.06 + 0.22 * np.log10(max(params_b, 0.01) + 1) / np.log10(1801)

        # Separate LLMs and SLMs
        llm_data = [(y, n, p) for y, n, p, s in MODEL_DATA if not s]
        slm_data = [(y, n, p) for y, n, p, s in MODEL_DATA if s]

        # Show first dot (ELMo) with emphasis
        first = llm_data[0]
        x0 = year_to_x(first[0])
        r0 = params_to_radius(first[2])
        dot0 = Dot(
            np.array([x0, timeline_y[1] + 0.8, 0]),
            radius=r0,
            color=ACCENT,
            fill_opacity=0.7,
        )
        glow0 = dot0.copy().set_stroke(ACCENT, width=2, opacity=0.5).set_fill(opacity=0)
        label0 = Text(f"{first[1]}", font_size=12, color=ACCENT)
        label0.next_to(dot0, UP, buff=0.12)
        param_label0 = Text("93M params", font_size=10, color=DIM)
        param_label0.next_to(label0, UP, buff=0.08)

        self.play(
            FadeIn(dot0, scale=0.5),
            FadeIn(glow0, scale=0.5),
            run_time=0.5,
        )
        self.play(
            FadeIn(label0, shift=UP * 0.05),
            FadeIn(param_label0, shift=UP * 0.05),
            run_time=0.4,
        )
        self.play(FadeOut(glow0), run_time=0.3)
        # [21:22] ELMo started it in 2018
        self.wait(5.0)

        # Show remaining LLM dots growing larger
        llm_dots = VGroup(dot0)
        llm_labels = VGroup(VGroup(label0, param_label0))
        prev_label_group = VGroup(label0, param_label0)

        for y, name, params in llm_data[1:]:
            x = year_to_x(y)
            r = params_to_radius(params)
            dot = Dot(
                np.array([x, timeline_y[1] + 0.8 + r * 1.5, 0]),
                radius=r,
                color=ACCENT,
                fill_opacity=0.65,
            )
            label = Text(name, font_size=11, color=ACCENT)
            label.next_to(dot, UP, buff=0.1)

            self.play(
                FadeOut(prev_label_group),
                run_time=0.15,
            )
            self.play(
                FadeIn(dot, scale=0.4),
                FadeIn(label, shift=UP * 0.05),
                run_time=0.35,
            )
            llm_dots.add(dot)
            prev_label_group = label
            llm_labels.add(label)

        # [21:34] GPT-4 reached 1.8 trillion parameters
        self.wait(5.0)
        self.play(FadeOut(prev_label_group), run_time=0.2)

        # ── SLMs appear below the timeline ──
        slm_dots = VGroup()
        slm_labels = VGroup()

        for y, name, params in slm_data:
            x = year_to_x(y)
            r = params_to_radius(params) * 0.7
            dot = Dot(
                np.array([x, timeline_y[1] - 0.8, 0]),
                radius=r,
                color=DIM,
                fill_opacity=0.4,
            )
            label = Text(name, font_size=9, color=DIM)
            label.next_to(dot, DOWN, buff=0.08)
            slm_dots.add(dot)
            slm_labels.add(label)

        slm_title = Text("SLMs", font_size=14, color=DIM)
        slm_title.move_to(LEFT * 5.5 + timeline_y + DOWN * 0.8)

        self.play(
            FadeIn(slm_title, shift=RIGHT * 0.1),
            LaggedStart(
                *[
                    AnimationGroup(
                        FadeIn(dot, scale=0.5),
                        FadeIn(label, shift=UP * 0.03),
                    )
                    for dot, label in zip(slm_dots, slm_labels)
                ],
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )
        # [21:42] Smaller, specialized models also matter — SLMs
        self.wait(10.0)

        # Fade everything out
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  SCENE 3 — Chatbot vs. Agent
    # ==================================================================

    def _scene_3_chatbot_vs_agent(self):
        # ── LEFT SIDE: simple chatbot interaction ──
        divider = DashedLine(
            UP * 3.5,
            DOWN * 3.5,
            color=DIM2,
            stroke_width=1,
            dash_length=0.1,
        )

        # Person icon
        person_icon = make_svg_icon("person.svg", color=DIM, height=0.9)
        person_icon.move_to(LEFT * 4.8 + UP * 0.5)

        # Chat box
        chatbot_box = RoundedRectangle(
            width=1.6,
            height=1.2,
            corner_radius=0.12,
            color=ACCENT,
            stroke_width=1.8,
            fill_color=ACCENT,
            fill_opacity=0.06,
        )
        chatbot_box.move_to(LEFT * 2.2 + UP * 0.5)
        chat_icon = make_svg_icon("chat-bubble.svg", color=ACCENT, height=0.6)
        chat_icon.move_to(chatbot_box.get_center())

        # Arrows: person → box → person (simple back-and-forth)
        send_arrow = Arrow(
            person_icon.get_right(),
            chatbot_box.get_left(),
            buff=0.15,
            color=DIM2,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.12,
        )
        reply_arrow = Arrow(
            chatbot_box.get_right(),
            person_icon.get_right() + RIGHT * 0.8 + DOWN * 0.8,
            buff=0.15,
            color=DIM2,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.12,
        )
        # Instead, let's do a cleaner layout
        reply_arrow = Arrow(
            chatbot_box.get_left() + DOWN * 0.2,
            person_icon.get_right() + DOWN * 0.2,
            buff=0.15,
            color=ACCENT,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.12,
        )

        # "done" marker — interaction ends
        done_mark = Text("✓ done", font_size=13, color=DIM2)
        done_mark.next_to(chatbot_box, DOWN, buff=0.5)

        chatbot_title = Text("chatbot", font_size=20, color=ACCENT)
        chatbot_title.move_to(LEFT * 3.5 + UP * 2.5)

        # Animate left side
        self.play(Create(divider), run_time=0.4)
        self.play(
            Write(chatbot_title),
            FadeIn(person_icon, shift=RIGHT * 0.1),
            FadeIn(chatbot_box, scale=0.9),
            FadeIn(chat_icon, scale=0.8),
            run_time=0.6,
        )
        self.play(GrowArrow(send_arrow), run_time=0.35)
        self.wait(1.0)

        # Pulse the chatbox (processing)
        pulse = chatbot_box.copy().set_stroke(ACCENT, width=3.5, opacity=0.5)
        self.play(FadeIn(pulse), run_time=0.12)
        self.play(FadeOut(pulse), run_time=0.18)

        self.play(GrowArrow(reply_arrow), run_time=0.35)
        self.play(FadeIn(done_mark, shift=UP * 0.05), run_time=0.3)
        # [22:03] A chatbot just generates text and stops
        self.wait(3.0)

        # Dim the left side
        left_side = VGroup(
            person_icon,
            chatbot_box,
            chat_icon,
            send_arrow,
            reply_arrow,
            done_mark,
            chatbot_title,
        )
        self.play(left_side.animate.set_opacity(0.35), run_time=0.4)

        # ── RIGHT SIDE: agent diagram (preview, simpler version) ──
        agent_title = Text("agent", font_size=20, color=GREEN)
        agent_title.move_to(RIGHT * 3.5 + UP * 2.5)

        # Person gives task
        person_r = make_svg_icon("person.svg", color=DIM, height=0.7)
        person_r.move_to(RIGHT * 1.5 + UP * 1.0)

        # Agent core (robot)
        agent_core = RoundedRectangle(
            width=1.6,
            height=1.2,
            corner_radius=0.12,
            color=GREEN,
            stroke_width=1.8,
            fill_color=GREEN,
            fill_opacity=0.06,
        )
        agent_core.move_to(RIGHT * 3.5 + UP * 0.3)
        robot_icon = make_svg_icon("robot.svg", color=GREEN, height=0.6)
        robot_icon.move_to(agent_core.get_center())

        # Environment icons beneath
        env_icons = VGroup()
        env_data = [
            ("document.svg", ACCENT),
            ("calendar.svg", GOLD),
            ("browser.svg", TEAL),
        ]
        for fname, clr in env_data:
            ei = make_svg_icon(fname, color=clr, height=0.4)
            env_icons.add(ei)
        env_icons.arrange(RIGHT, buff=0.35)
        env_icons.next_to(agent_core, DOWN, buff=0.5)

        # Arrow: person → agent
        task_arrow = Arrow(
            person_r.get_right(),
            agent_core.get_left(),
            buff=0.15,
            color=DIM2,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.12,
        )

        # Looping arrow (agent ↔ environment)
        loop_arrow_down = Arrow(
            agent_core.get_bottom(),
            env_icons.get_top(),
            buff=0.1,
            color=GREEN,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )
        loop_arrow_up = Arrow(
            env_icons.get_top() + RIGHT * 0.5,
            agent_core.get_bottom() + RIGHT * 0.5,
            buff=0.1,
            color=GOLD,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )

        # Animate right side
        self.play(
            Write(agent_title),
            run_time=0.4,
        )
        self.play(
            FadeIn(person_r, shift=RIGHT * 0.1),
            FadeIn(agent_core, scale=0.9),
            FadeIn(robot_icon, scale=0.8),
            run_time=0.5,
        )
        self.play(GrowArrow(task_arrow), run_time=0.3)
        self.play(
            LaggedStart(
                *[FadeIn(ei, scale=0.6) for ei in env_icons],
                lag_ratio=0.1,
            ),
            run_time=0.5,
        )
        self.play(
            GrowArrow(loop_arrow_down),
            GrowArrow(loop_arrow_up),
            run_time=0.5,
        )

        # Highlight the looping nature with a pulse
        glow_rect = SurroundingRectangle(
            VGroup(agent_core, env_icons),
            color=GREEN,
            buff=0.25,
            corner_radius=0.15,
            stroke_width=2,
            fill_color=GREEN,
            fill_opacity=0.03,
        )
        self.play(Create(glow_rect), run_time=0.4)
        pulse_rect = glow_rect.copy().set_stroke(GREEN, width=3)
        self.play(
            pulse_rect.animate.scale(1.06).set_opacity(0),
            run_time=0.6,
        )
        self.remove(pulse_rect)
        # [22:27] An agent interacts with the real world — it loops
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    # ==================================================================
    #  SCENE 4 — The Agent Loop (detailed)
    # ==================================================================

    def _scene_4_agent_loop(self):
        # ── Central hexagon: LLM core ──
        llm_hex = make_hexagon(side_length=0.9, color=ACCENT, fill_opacity=0.1)
        llm_hex.move_to(ORIGIN)
        llm_label = Text("LLM", font_size=16, color=ACCENT)
        llm_label.move_to(llm_hex.get_center())

        self.play(
            FadeIn(llm_hex, scale=0.7),
            FadeIn(llm_label, scale=0.8),
            run_time=0.6,
        )

        # ── Environment icons orbiting ──
        orbit_radius = 2.4
        env_configs = [
            ("document.svg", ACCENT, PI / 2),  # top
            ("calendar.svg", GOLD, PI / 6),  # upper right
            ("browser.svg", TEAL, -PI / 6),  # lower right
            ("database.svg", PURPLE, -PI / 2),  # bottom
            ("email.svg", ORANGE, -5 * PI / 6),  # lower left
            ("gear.svg", DIM, 5 * PI / 6),  # upper left
        ]

        env_icons = VGroup()
        for fname, clr, angle in env_configs:
            icon = make_svg_icon(fname, color=clr, height=0.55)
            pos = ORIGIN + orbit_radius * np.array([np.cos(angle), np.sin(angle), 0])
            icon.move_to(pos)
            env_icons.add(icon)

        # Faint orbit ring
        orbit_ring = Circle(
            radius=orbit_radius,
            color=DIM2,
            stroke_width=0.6,
            stroke_opacity=0.25,
        )
        orbit_ring.move_to(ORIGIN)

        self.play(
            FadeIn(orbit_ring),
            LaggedStart(
                *[FadeIn(ei, scale=0.5) for ei in env_icons],
                lag_ratio=0.08,
            ),
            run_time=0.8,
        )
        # [22:50] Act, observe, reason loop
        self.wait(5.0)

        # ── Show a single act-observe cycle ──
        # Arrow from LLM → calendar (act)
        target_icon = env_icons[1]  # calendar

        act_arrow = Arrow(
            llm_hex.get_center()
            + 0.5
            * (target_icon.get_center() - llm_hex.get_center()).astype(float)
            / np.linalg.norm(target_icon.get_center() - llm_hex.get_center()),
            target_icon.get_center()
            - 0.3
            * (target_icon.get_center() - llm_hex.get_center()).astype(float)
            / np.linalg.norm(target_icon.get_center() - llm_hex.get_center()),
            buff=0,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(GrowArrow(act_arrow), run_time=0.4)

        # Result pulse bounces back
        result_dot = Dot(
            target_icon.get_center(),
            radius=0.08,
            color=GOLD,
            fill_opacity=0.8,
        )
        self.play(FadeIn(result_dot, scale=0.5), run_time=0.15)
        self.play(
            result_dot.animate.move_to(llm_hex.get_center()),
            run_time=0.4,
            rate_func=smooth,
        )
        self.play(FadeOut(result_dot), FadeOut(act_arrow), run_time=0.2)
        # [23:00] Act → observe → reason → act again
        self.wait(5.0)

        # ── Build the continuous loop ──
        # Four phase labels around the loop
        phase_data = [
            ("act", GREEN, PI / 2 + 0.3),
            ("observe", GOLD, 0),
            ("reason", ACCENT, -PI / 2 - 0.3),
            ("act", GREEN, PI),
        ]

        # Create a smooth cycling path: LLM → env → LLM → env …
        # We show arrows cycling around in a loop
        loop_arrows = VGroup()
        n_arrows = 8
        for i in range(n_arrows):
            angle_start = i * TAU / n_arrows
            angle_end = (i + 1) * TAU / n_arrows
            mid_r = 1.6 if i % 2 == 0 else 1.2

            start_pt = ORIGIN + mid_r * np.array(
                [np.cos(angle_start), np.sin(angle_start), 0]
            )
            end_pt = ORIGIN + mid_r * np.array(
                [np.cos(angle_end), np.sin(angle_end), 0]
            )

            arc = ArcBetweenPoints(
                start_pt,
                end_pt,
                angle=PI / 6,
                color=GREEN,
                stroke_width=1.5,
                stroke_opacity=0.4,
            )
            loop_arrows.add(arc)

        # Instead, let's use a single smooth circular arrow for the loop
        loop_circle = Circle(
            radius=1.5,
            color=GREEN,
            stroke_width=2.0,
            stroke_opacity=0.5,
        )
        loop_circle.move_to(ORIGIN)

        # Directional arrow tips at quarters
        tip_angles = [PI / 4, 3 * PI / 4, -3 * PI / 4, -PI / 4]
        tip_arrows = VGroup()
        for ta in tip_angles:
            pt = ORIGIN + 1.5 * np.array([np.cos(ta), np.sin(ta), 0])
            tangent = np.array([-np.sin(ta), np.cos(ta), 0])
            tip = Arrow(
                pt - 0.15 * tangent,
                pt + 0.15 * tangent,
                buff=0,
                color=GREEN,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.6,
            )
            tip_arrows.add(tip)

        self.play(
            Create(loop_circle),
            LaggedStart(
                *[GrowArrow(ta) for ta in tip_arrows],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )

        # Phase labels
        phase_labels = VGroup()
        phase_positions = [
            (UP * 1.7, "act", GREEN),
            (RIGHT * 2.0, "observe", GOLD),
            (DOWN * 1.7, "reason", ACCENT),
            (LEFT * 2.0, "act again", GREEN),
        ]
        for pos, txt, clr in phase_positions:
            pl = Text(txt, font_size=14, color=clr)
            pl.move_to(pos)
            phase_labels.add(pl)

        self.play(
            LaggedStart(
                *[FadeIn(pl, scale=0.8) for pl in phase_labels],
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )
        # [23:15] The loop continues until task is complete
        self.wait(8.0)

        # Glow the loop each revolution
        glow_ring = loop_circle.copy().set_stroke(GREEN, width=4, opacity=0.6)
        self.play(FadeIn(glow_ring), run_time=0.2)
        self.play(
            glow_ring.animate.scale(1.05).set_opacity(0),
            run_time=0.6,
        )
        self.remove(glow_ring)

        # Fade out phase labels, keep the loop diagram clean
        self.play(
            LaggedStart(
                *[FadeOut(pl) for pl in phase_labels],
                lag_ratio=0.05,
            ),
            run_time=0.4,
        )
        # [23:28] Agent loop with phase labels
        self.wait(6.0)

        # Store everything for Scene 5 transition
        self._loop_diagram = VGroup(
            llm_hex,
            llm_label,
            orbit_ring,
            env_icons,
            loop_circle,
            tip_arrows,
        )
        self._loop_center = ORIGIN.copy()

        self.play(
            *[mob.animate.shift(DOWN * 0.5) for mob in self.mobjects],
            run_time=0.8,
            rate_func=smooth,
        )

    # ==================================================================
    #  SCENE 5 — Closing
    # ==================================================================

    def _scene_5_closing(self):
        loop_diagram = self._loop_diagram

        # ── The three role icons reappear faintly in the background ──
        doc_icon = make_svg_icon("document.svg", color=ACCENT, height=0.7)
        cal_icon = make_svg_icon("calendar.svg", color=GOLD, height=0.7)
        star_icon = make_svg_icon("star.svg", color=PURPLE, height=0.7)

        role_icons = VGroup(doc_icon, cal_icon, star_icon)
        role_positions = [LEFT * 4.5 + UP * 2.0, UP * 3.5, RIGHT * 4.5 + UP * 2.0]
        for icon, pos in zip(role_icons, role_positions):
            icon.move_to(pos)
            icon.set_opacity(0.75)

        role_labels = VGroup(
            Text("WORK", font_size=11, color=ACCENT),
            Text("PERSONAL", font_size=11, color=GOLD),
            Text("CREATIVE", font_size=11, color=PURPLE),
        )
        for label, icon in zip(role_labels, role_icons):
            label.next_to(icon, DOWN, buff=0.15)
            label.set_opacity(0.75)

        # Faint connection lines from each role icon to the loop
        conn_lines = VGroup()
        for icon in role_icons:
            line = DashedLine(
                icon.get_center(),
                self._loop_center,
                color=DIM2,
                stroke_width=8.0,
                stroke_opacity=0.5,
                dash_length=0.08,
            )
            conn_lines.add(line)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(FadeIn(icon), FadeIn(label))
                    for icon, label in zip(role_icons, role_labels)
                ],
                lag_ratio=0.12,
            ),
            LaggedStart(
                *[Create(line) for line in conn_lines],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )
        # [23:35] Three roles reconnect to the central loop
        self.wait(5.0)

        # ── The loop slows and settles ──
        # Gentle pulse
        glow = loop_diagram[4].copy().set_stroke(GREEN, width=3, opacity=0.4)
        self.play(FadeIn(glow), run_time=0.2)
        self.play(
            glow.animate.scale(1.03).set_opacity(0),
            run_time=0.8,
            rate_func=smooth,
        )
        self.remove(glow)

        # ── Fade everything to black ──
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.3)

        # ── "AGENT" title fades in at center ──
        agent_text = Text(
            "AGENT",
            font_size=52,
            color=WHITE,
            weight=BOLD,
        )
        agent_text.move_to(ORIGIN)

        # Subtle underline
        underline = Line(
            agent_text.get_left() + DOWN * 0.35,
            agent_text.get_right() + DOWN * 0.35,
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.6,
        )

        self.play(
            FadeIn(agent_text, scale=1.1),
            run_time=0.8,
            rate_func=smooth,
        )
        self.play(Create(underline), run_time=0.4)
        # [23:42] AGENT title — final emphasis
        self.wait(4.0)

        # Final fade out
        self.play(
            FadeOut(agent_text),
            FadeOut(underline),
            run_time=1.0,
        )
        self.wait(0.3)
