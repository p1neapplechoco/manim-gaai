from manim import *
import textwrap


# --- Design system -----------------------------------------------------------

BG_PRIMARY = "#000000"  # User-approved V5 override.
BG_SECONDARY = "#1e293b"
BG_TERTIARY = "#334155"

TEXT_PRIMARY = "#f8fafc"
TEXT_SECONDARY = "#94a3b8"
TEXT_MUTED = "#475569"

ACCENT_BLUE = "#38bdf8"
ACCENT_PURPLE = "#a78bfa"
ACCENT_AMBER = "#fbbf24"
ACCENT_GREEN = "#34d399"
ACCENT_CORAL = "#fb7185"

BORDER_COLOR = "#334155"

FONT_HERO = 52
FONT_TITLE = 40
FONT_SUBTITLE = 30
FONT_BODY = 24
FONT_CAPTION = 18
FONT_TINY = 14

EDGE_MARGIN = 0.5
GAP_LARGE = 0.8
GAP_MEDIUM = 0.5
GAP_SMALL = 0.25
BOX_PADDING = 0.35

T_REVEAL_SLOW = 1.2
T_REVEAL_STD = 0.8
T_REVEAL_FAST = 0.4
T_TRANS_STD = 0.5
T_TRANS_FAST = 0.3
T_PAUSE_LONG = 2.5
T_PAUSE_STD = 1.5
T_PAUSE_SHORT = 0.8

TITLE_FONT = "Avenir Next"
ANIMATION_TIME_SCALE = 2.35


class Chapter01V5(MovingCameraScene):
    def setup(self):
        self.camera.background_color = BG_PRIMARY
        self.title = None
        self.stage = VGroup()
        self.progress = self.chapter_progress(1, 9)
        self.add(self.progress)

    def construct(self):
        self.beat_01_generalist_motivation()
        self.beat_02_indirect_mimicking()
        self.beat_03_encoder_task_model()
        self.beat_04_what_field()
        self.beat_05_where_field()
        self.beat_06_skill_library()
        self.beat_07_cross_robot_task_model()
        self.beat_08_handoff_to_skills()
        self.wait(T_PAUSE_LONG)

    def play(self, *animations, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] *= ANIMATION_TIME_SCALE
        return super().play(*animations, **kwargs)

    # --- Text helpers --------------------------------------------------------

    def tex_escape(self, content):
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        return "".join(replacements.get(char, char) for char in content)

    def content_text(
        self,
        text,
        font_size=FONT_BODY,
        color=TEXT_SECONDARY,
        max_width=None,
        min_font_size=FONT_CAPTION,
        weight=NORMAL,
    ):
        def build(line, size):
            body = self.tex_escape(line)
            if weight == BOLD:
                body = r"\textbf{" + body + "}"
            return Tex(body, font_size=size, color=color)

        mob = build(text, font_size)
        if not max_width or mob.width <= max_width:
            return mob

        fitted = max(min_font_size, font_size * max_width / mob.width)
        mob = build(text, fitted)
        if mob.width <= max_width:
            return mob

        words = text.split()
        lines = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if build(candidate, font_size).width <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        group = VGroup(*[build(line, font_size) for line in lines]).arrange(DOWN, buff=0.08)
        if group.width > max_width:
            group.scale_to_fit_width(max_width)
            if group.height > 1.4:
                group.scale_to_fit_height(1.4)
        return group

    def make_title(self, text):
        lines = textwrap.wrap(text, width=42, break_long_words=False)
        title = VGroup(
            *[
                Text(
                    line,
                    font=TITLE_FONT,
                    font_size=FONT_TITLE,
                    color=TEXT_PRIMARY,
                    weight=BOLD,
                )
                for line in lines
            ]
        ).arrange(DOWN, buff=0.05)
        if title.width > 11.6:
            title.scale_to_fit_width(11.6)
        return title.to_edge(UP, buff=EDGE_MARGIN)

    def set_title(self, text):
        new_title = self.make_title(text)
        if self.title is None:
            self.play(Write(new_title), run_time=T_REVEAL_STD, rate_func=smooth)
        else:
            self.play(FadeOut(self.title, shift=UP * 0.08), run_time=T_TRANS_STD, rate_func=rush_into)
            self.play(Write(new_title), run_time=T_REVEAL_STD, rate_func=smooth)
        self.title = new_title

    def label(self, text, color=TEXT_SECONDARY, size=FONT_BODY, max_width=2.8, weight=NORMAL):
        return self.content_text(text, size, color, max_width=max_width, weight=weight)

    def caption(self, text, color=TEXT_MUTED, max_width=3.2):
        return self.content_text(text, FONT_CAPTION, color, max_width=max_width)

    # --- Layout helpers ------------------------------------------------------

    def chapter_progress(self, current, total):
        items = []
        for idx in range(1, total + 1):
            active = idx == current
            dot = Circle(
                radius=0.045 if not active else 0.07,
                stroke_width=1.2,
                stroke_color=TEXT_PRIMARY if active else TEXT_MUTED,
                fill_color=TEXT_PRIMARY if active else TEXT_MUTED,
                fill_opacity=1,
            )
            items.append(dot)
        rail = VGroup(*items).arrange(RIGHT, buff=0.18)
        label = self.caption(f"{current:02d}/{total:02d}", TEXT_MUTED, max_width=0.8).next_to(
            rail, RIGHT, buff=GAP_SMALL
        )
        return VGroup(rail, label).to_edge(DOWN, buff=0.28).to_edge(RIGHT, buff=0.55)

    def set_stage(self, new_stage, keep=()):
        old = VGroup(*[mob for mob in self.stage if mob not in keep])
        if len(old):
            self.play(FadeOut(old, shift=DOWN * 0.08), run_time=T_TRANS_STD, rate_func=rush_into)
        self.stage = VGroup(*keep, *new_stage)

    def arrow_between(self, left, right, color=ACCENT_BLUE, buff=0.18):
        return Arrow(
            left.get_right(),
            right.get_left(),
            buff=buff,
            color=color,
            stroke_width=2.4,
            tip_length=0.18,
        )

    def panel(self, width, height, label=None, accent=ACCENT_BLUE):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=accent,
            stroke_width=1.4,
            fill_color=BG_SECONDARY,
            fill_opacity=0.88,
        )
        if label is None:
            return VGroup(box)
        text = self.label(label, TEXT_PRIMARY, FONT_CAPTION, max_width=width - 0.25).next_to(
            box, UP, buff=0.08
        )
        return VGroup(box, text)

    def task_card(self, title="Task model", accent=ACCENT_AMBER, show_fields=True):
        card = RoundedRectangle(
            width=3.55,
            height=2.1 if show_fields else 1.28,
            corner_radius=0.16,
            stroke_color=accent,
            stroke_width=1.8,
            fill_color=BG_SECONDARY,
            fill_opacity=1,
        )
        heading = self.label(title, TEXT_PRIMARY, FONT_BODY, max_width=2.9, weight=BOLD).move_to(
            card.get_top() + DOWN * 0.34
        )
        group = VGroup(card, heading)
        if show_fields:
            what = self.field_row("what", "primitive action", ACCENT_BLUE)
            where = self.field_row("where", "grounded parameter", ACCENT_AMBER)
            fields = VGroup(what, where).arrange(DOWN, buff=0.22).move_to(card.get_center() + DOWN * 0.28)
            group.add(fields)
        else:
            formula = MathTex("M=(\\mathrm{what},\\mathrm{where})", font_size=FONT_BODY, color=TEXT_PRIMARY)
            formula.next_to(heading, DOWN, buff=0.18)
            group.add(formula)
        return group

    def field_row(self, key, value, accent):
        key_box = RoundedRectangle(
            width=0.9,
            height=0.42,
            corner_radius=0.08,
            stroke_color=accent,
            stroke_width=1.3,
            fill_color=BG_TERTIARY,
            fill_opacity=1,
        )
        key_text = self.label(key, TEXT_PRIMARY, FONT_CAPTION, max_width=0.75).move_to(key_box)
        value_text = self.label(value, TEXT_SECONDARY, FONT_CAPTION, max_width=1.8).next_to(
            key_box, RIGHT, buff=0.18
        )
        return VGroup(key_box, key_text, value_text)

    def robot(self, accent=ACCENT_GREEN, scale=1.0, mirrored=False):
        base = RoundedRectangle(
            width=0.95,
            height=0.34,
            corner_radius=0.08,
            stroke_color=accent,
            stroke_width=1.6,
            fill_color=BG_TERTIARY,
            fill_opacity=1,
        )
        shoulder = Dot(base.get_top() + UP * 0.22, radius=0.09, color=accent)
        elbow_offset = (LEFT if mirrored else RIGHT) * 0.55 + UP * 0.66
        hand_offset = (LEFT if mirrored else RIGHT) * 0.96 + UP * 0.28
        upper = Line(shoulder.get_center(), shoulder.get_center() + elbow_offset, color=accent, stroke_width=2.4)
        lower = Line(upper.get_end(), shoulder.get_center() + hand_offset, color=accent, stroke_width=2.4)
        hand = Circle(radius=0.07, color=accent, fill_color=accent, fill_opacity=1).move_to(lower.get_end())
        return VGroup(base, shoulder, upper, lower, hand).scale(scale)

    def simple_world(self, variant=0, accent=ACCENT_BLUE):
        table = RoundedRectangle(
            width=2.55,
            height=1.3,
            corner_radius=0.12,
            stroke_color=BORDER_COLOR,
            stroke_width=1.2,
            fill_color=BG_SECONDARY,
            fill_opacity=0.72,
        )
        obj = Square(
            side_length=0.36,
            stroke_color=accent,
            stroke_width=1.4,
            fill_color=BG_TERTIARY,
            fill_opacity=1,
        )
        target = Circle(
            radius=0.2,
            stroke_color=ACCENT_GREEN,
            stroke_width=1.4,
            fill_opacity=0,
        )
        if variant == 0:
            obj.move_to(table.get_center() + LEFT * 0.56 + UP * 0.2)
            target.move_to(table.get_center() + RIGHT * 0.55 + DOWN * 0.18)
        else:
            obj.move_to(table.get_center() + RIGHT * 0.42 + UP * 0.08)
            target.move_to(table.get_center() + LEFT * 0.58 + DOWN * 0.2)
        return VGroup(table, target, obj)

    def encoder_box(self):
        box = RoundedRectangle(
            width=2.1,
            height=1.12,
            corner_radius=0.15,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.7,
            fill_color=BG_SECONDARY,
            fill_opacity=1,
        )
        label = self.label("GPT / VLM encoder", TEXT_PRIMARY, FONT_CAPTION, max_width=1.75).move_to(box)
        return VGroup(box, label)

    # --- Beats ---------------------------------------------------------------

    def beat_01_generalist_motivation(self):
        self.set_title("A generalist robot needs task intent that survives new settings.")

        goal = self.task_card("same task intent", ACCENT_AMBER, show_fields=False).scale(0.82)
        goal.move_to(UP * 0.55)

        world_a = self.simple_world(0, ACCENT_BLUE)
        robot_a = self.robot(ACCENT_GREEN, 0.72).next_to(world_a, DOWN, buff=0.22)
        setup_a = VGroup(world_a, robot_a)

        world_b = self.simple_world(1, ACCENT_BLUE)
        robot_b = self.robot(ACCENT_GREEN, 0.72, mirrored=True).next_to(world_b, DOWN, buff=0.22)
        setup_b = VGroup(world_b, robot_b)

        setups = VGroup(setup_a, setup_b).arrange(RIGHT, buff=1.8).move_to(DOWN * 0.75)
        left_arrow = Arrow(goal.get_bottom(), setup_a.get_top(), buff=0.15, color=ACCENT_BLUE, stroke_width=2.2)
        right_arrow = Arrow(goal.get_bottom(), setup_b.get_top(), buff=0.15, color=ACCENT_BLUE, stroke_width=2.2)
        caption = self.caption("same intent, different geometry and bodies", TEXT_SECONDARY, max_width=4.6)
        caption.next_to(setups, DOWN, buff=0.2)

        stage = VGroup(goal, setups, left_arrow, right_arrow, caption)
        self.set_stage(stage)
        self.play(DrawBorderThenFill(goal), run_time=T_REVEAL_STD)
        self.play(
            LaggedStart(
                FadeIn(setup_a, shift=UP * 0.18),
                FadeIn(setup_b, shift=UP * 0.18),
                lag_ratio=0.18,
            ),
            run_time=T_REVEAL_STD,
        )
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow), run_time=T_REVEAL_FAST)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=T_REVEAL_FAST)
        self.wait(T_PAUSE_STD)

    def beat_02_indirect_mimicking(self):
        self.set_title("LfO copies the purpose of a demonstration, not its trajectory.")

        world = self.simple_world(0, ACCENT_BLUE).scale(1.15)
        world.move_to(LEFT * 2.65 + DOWN * 0.25)
        path = VMobject(color=ACCENT_BLUE, stroke_width=3)
        points = [
            world.get_center() + LEFT * 0.85 + DOWN * 0.1,
            world.get_center() + LEFT * 0.25 + UP * 0.55,
            world.get_center() + RIGHT * 0.65 + UP * 0.12,
        ]
        path.set_points_smoothly(points)
        human = self.label("demonstration path", ACCENT_BLUE, FONT_CAPTION, max_width=2.0)
        human.next_to(world, DOWN, buff=0.2)

        card = self.task_card("purpose", ACCENT_AMBER, show_fields=False).scale(0.9)
        card.move_to(RIGHT * 2.65 + DOWN * 0.15)
        not_motor = self.caption("not human joint motion", TEXT_SECONDARY, max_width=2.3).next_to(
            card, DOWN, buff=0.2
        )
        arrow = Arrow(world.get_right(), card.get_left(), buff=0.34, color=ACCENT_AMBER, stroke_width=2.4)
        bridge = self.label("abstract", ACCENT_AMBER, FONT_CAPTION, max_width=1.2).next_to(arrow, UP, buff=0.08)

        stage = VGroup(world, path, human, card, not_motor, arrow, bridge)
        self.set_stage(stage)
        self.play(FadeIn(world, shift=UP * 0.16), FadeIn(human), run_time=T_REVEAL_STD)
        self.play(Create(path), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_SHORT)
        self.play(GrowArrow(arrow), FadeIn(bridge, shift=UP * 0.08), run_time=T_REVEAL_FAST)
        self.play(TransformFromCopy(path, card), FadeIn(not_motor, shift=UP * 0.08), run_time=T_REVEAL_STD)
        self.play(Indicate(card, color=ACCENT_AMBER), run_time=T_REVEAL_FAST)
        self.wait(T_PAUSE_STD)

    def beat_03_encoder_task_model(self):
        self.set_title("The encoder turns observation into a compact task model.")

        language = self.panel(2.25, 0.92, "language", ACCENT_BLUE)
        lang_text = self.label("\"open the drawer\"", TEXT_PRIMARY, FONT_CAPTION, max_width=1.85)
        lang_text.move_to(language[0])
        language.add(lang_text)

        frames = VGroup(
            *[
                RoundedRectangle(
                    width=0.7,
                    height=0.52,
                    corner_radius=0.05,
                    stroke_color=ACCENT_BLUE,
                    stroke_width=1.2,
                    fill_color=BG_TERTIARY,
                    fill_opacity=1,
                )
                for _ in range(3)
            ]
        ).arrange(RIGHT, buff=0.12)
        frames_label = self.caption("vision frames", TEXT_SECONDARY, max_width=1.4).next_to(
            frames, UP, buff=0.1
        )
        vision = VGroup(frames, frames_label)

        inputs = VGroup(language, vision).arrange(DOWN, buff=0.72).move_to(LEFT * 4.1 + DOWN * 0.1)
        encoder = self.encoder_box().move_to(ORIGIN + DOWN * 0.1)
        model = self.task_card("task model", ACCENT_AMBER, show_fields=True).scale(0.9)
        model.move_to(RIGHT * 3.75 + DOWN * 0.1)
        arrow_1 = self.arrow_between(inputs, encoder, ACCENT_BLUE)
        arrow_2 = self.arrow_between(encoder, model, ACCENT_AMBER)

        stage = VGroup(inputs, encoder, model, arrow_1, arrow_2)
        self.set_stage(stage)
        self.play(LaggedStart(FadeIn(language), FadeIn(vision), lag_ratio=0.16), run_time=T_REVEAL_STD)
        self.play(GrowArrow(arrow_1), DrawBorderThenFill(encoder), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_SHORT)
        self.play(GrowArrow(arrow_2), DrawBorderThenFill(model), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_STD)

    def beat_04_what_field(self):
        self.set_title("What-to-do names the primitive action.")

        instruction = RoundedRectangle(
            width=4.25,
            height=0.78,
            corner_radius=0.12,
            stroke_color=BORDER_COLOR,
            stroke_width=1.2,
            fill_color=BG_SECONDARY,
            fill_opacity=1,
        )
        words = VGroup(
            self.label("open", ACCENT_AMBER, FONT_BODY, max_width=0.8, weight=BOLD),
            self.label("the drawer", TEXT_SECONDARY, FONT_BODY, max_width=1.8),
        ).arrange(RIGHT, buff=0.18)
        words.move_to(instruction)
        phrase = VGroup(instruction, words).move_to(LEFT * 2.8 + DOWN * 0.1)

        what_box = RoundedRectangle(
            width=2.6,
            height=1.18,
            corner_radius=0.14,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.7,
            fill_color=BG_SECONDARY,
            fill_opacity=1,
        )
        what_key = self.label("what-to-do", ACCENT_AMBER, FONT_BODY, max_width=2.1, weight=BOLD)
        what_value = self.label("Open", TEXT_PRIMARY, FONT_BODY, max_width=1.2)
        VGroup(what_key, what_value).arrange(DOWN, buff=0.12).move_to(what_box)
        what = VGroup(what_box, what_key, what_value).move_to(RIGHT * 2.6 + DOWN * 0.1)
        arrow = self.arrow_between(phrase, what, ACCENT_AMBER, buff=0.24)
        caption = self.caption("a symbolic operation, not a trajectory", TEXT_SECONDARY, max_width=4.0)
        caption.next_to(VGroup(phrase, what), DOWN, buff=0.42)

        stage = VGroup(phrase, what, arrow, caption)
        self.set_stage(stage)
        self.play(FadeIn(phrase, shift=UP * 0.12), run_time=T_REVEAL_STD)
        self.play(Indicate(words[0], color=ACCENT_AMBER), run_time=T_REVEAL_FAST)
        self.play(GrowArrow(arrow), TransformFromCopy(words[0], what_value), DrawBorderThenFill(what_box), FadeIn(what_key), run_time=T_REVEAL_STD)
        self.play(FadeIn(caption, shift=UP * 0.08), run_time=T_REVEAL_FAST)
        self.wait(T_PAUSE_STD)

    def beat_05_where_field(self):
        self.set_title("Where-to-do grounds the action in objects and affordances.")

        scene = RoundedRectangle(
            width=4.4,
            height=2.55,
            corner_radius=0.14,
            stroke_color=BORDER_COLOR,
            stroke_width=1.2,
            fill_color=BG_SECONDARY,
            fill_opacity=0.78,
        )
        drawer = RoundedRectangle(
            width=2.15,
            height=0.74,
            corner_radius=0.08,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.5,
            fill_color=BG_TERTIARY,
            fill_opacity=1,
        )
        handle = Line(LEFT * 0.36, RIGHT * 0.36, color=ACCENT_AMBER, stroke_width=3)
        handle.move_to(drawer.get_center() + DOWN * 0.02)
        axis = Arrow(
            drawer.get_right() + RIGHT * 0.1,
            drawer.get_right() + RIGHT * 0.88,
            buff=0.0,
            color=ACCENT_AMBER,
            stroke_width=2.3,
            tip_length=0.16,
        )
        drawer_group = VGroup(drawer, handle, axis).move_to(scene)
        scene_group = VGroup(scene, drawer_group).move_to(LEFT * 2.75 + DOWN * 0.1)

        where = RoundedRectangle(
            width=3.0,
            height=1.3,
            corner_radius=0.14,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.7,
            fill_color=BG_SECONDARY,
            fill_opacity=1,
        )
        key = self.label("where-to-do", ACCENT_AMBER, FONT_BODY, max_width=2.3, weight=BOLD)
        value = self.label("handle + pull axis", TEXT_PRIMARY, FONT_CAPTION, max_width=2.2)
        VGroup(key, value).arrange(DOWN, buff=0.16).move_to(where)
        where_group = VGroup(where, key, value).move_to(RIGHT * 2.75 + DOWN * 0.1)
        arrow = self.arrow_between(scene_group, where_group, ACCENT_AMBER, buff=0.28)

        stage = VGroup(scene_group, where_group, arrow)
        self.set_stage(stage)
        self.play(FadeIn(scene_group, shift=UP * 0.14), run_time=T_REVEAL_STD)
        self.play(Indicate(handle, color=ACCENT_AMBER), GrowArrow(axis), run_time=T_REVEAL_FAST)
        self.play(GrowArrow(arrow), DrawBorderThenFill(where), FadeIn(key), TransformFromCopy(handle, value), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_STD)

    def beat_06_skill_library(self):
        self.set_title("The skill library supplies how-to-do for each robot.")

        model = self.task_card("task model", ACCENT_AMBER, show_fields=True).scale(0.84)
        model.move_to(LEFT * 4.1 + DOWN * 0.1)

        chips = VGroup(
            *[self.skill_chip(name) for name in ["Pick", "Bring", "Place", "Drawer", "Door", "Wipe"]]
        ).arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.25))
        library_box = RoundedRectangle(
            width=4.95,
            height=2.55,
            corner_radius=0.16,
            stroke_color=ACCENT_PURPLE,
            stroke_width=1.6,
            fill_color=BG_SECONDARY,
            fill_opacity=0.88,
        )
        library_label = self.label("skill-agent library", ACCENT_PURPLE, FONT_BODY, max_width=3.0, weight=BOLD)
        library_label.next_to(library_box, UP, buff=0.12)
        chips.move_to(library_box.get_center())
        library = VGroup(library_box, library_label, chips).move_to(RIGHT * 1.65 + DOWN * 0.05)

        arrow = self.arrow_between(model, library, ACCENT_PURPLE, buff=0.22)
        how = self.label("how-to-do", ACCENT_PURPLE, FONT_BODY, max_width=1.8, weight=BOLD).next_to(
            arrow, UP, buff=0.1
        )
        stage = VGroup(model, library, arrow, how)
        self.set_stage(stage)
        self.play(DrawBorderThenFill(model), run_time=T_REVEAL_STD)
        self.play(GrowArrow(arrow), FadeIn(how, shift=UP * 0.08), run_time=T_REVEAL_FAST)
        self.play(DrawBorderThenFill(library_box), FadeIn(library_label), run_time=T_REVEAL_STD)
        self.play(LaggedStart(*[FadeIn(chip, shift=UP * 0.12) for chip in chips], lag_ratio=0.08), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_STD)

    def skill_chip(self, name):
        box = RoundedRectangle(
            width=1.34,
            height=0.54,
            corner_radius=0.12,
            stroke_color=ACCENT_PURPLE,
            stroke_width=1.3,
            fill_color=BG_TERTIARY,
            fill_opacity=1,
        )
        label = self.label(name, TEXT_PRIMARY, FONT_CAPTION, max_width=1.0).move_to(box)
        return VGroup(box, label)

    def beat_07_cross_robot_task_model(self):
        self.set_title("A task model can cross robot bodies because it is not a motor program.")

        model = self.task_card("shared task model", ACCENT_AMBER, show_fields=False).scale(0.86)
        model.move_to(UP * 1.05)

        robot_a = self.robot(ACCENT_GREEN, 0.9).move_to(LEFT * 2.75 + DOWN * 0.85)
        robot_b = self.robot(ACCENT_GREEN, 0.9, mirrored=True).move_to(RIGHT * 2.75 + DOWN * 0.85)
        label_a = self.caption("robot A motion", TEXT_SECONDARY, max_width=1.7).next_to(robot_a, DOWN, buff=0.18)
        label_b = self.caption("robot B motion", TEXT_SECONDARY, max_width=1.7).next_to(robot_b, DOWN, buff=0.18)

        trace_a = ArcBetweenPoints(robot_a.get_top() + LEFT * 0.2, robot_a.get_top() + RIGHT * 1.0, angle=-PI / 3)
        trace_a.set_color(ACCENT_GREEN).set_stroke(width=2.2)
        trace_b = ArcBetweenPoints(robot_b.get_top() + RIGHT * 0.2, robot_b.get_top() + LEFT * 1.0, angle=PI / 3)
        trace_b.set_color(ACCENT_GREEN).set_stroke(width=2.2)
        arrow_a = Arrow(model.get_bottom(), robot_a.get_top(), buff=0.18, color=ACCENT_GREEN, stroke_width=2.2, tip_length=0.16)
        arrow_b = Arrow(model.get_bottom(), robot_b.get_top(), buff=0.18, color=ACCENT_GREEN, stroke_width=2.2, tip_length=0.16)
        caption = self.caption("same request, different feasible trajectories", TEXT_SECONDARY, max_width=4.5)
        caption.next_to(VGroup(robot_a, robot_b), DOWN, buff=0.55)

        stage = VGroup(model, robot_a, robot_b, label_a, label_b, trace_a, trace_b, arrow_a, arrow_b, caption)
        self.set_stage(stage)
        self.play(DrawBorderThenFill(model), run_time=T_REVEAL_STD)
        self.play(GrowArrow(arrow_a), GrowArrow(arrow_b), run_time=T_REVEAL_FAST)
        self.play(
            LaggedStart(
                FadeIn(robot_a, shift=UP * 0.12),
                FadeIn(robot_b, shift=UP * 0.12),
                FadeIn(label_a),
                FadeIn(label_b),
                lag_ratio=0.12,
            ),
            run_time=T_REVEAL_STD,
        )
        self.play(Create(trace_a), Create(trace_b), FadeIn(caption, shift=UP * 0.08), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_STD)

    def beat_08_handoff_to_skills(self):
        self.set_title("The next question is how to define the skill vocabulary.")

        card = self.task_card("handoff", ACCENT_AMBER, show_fields=False).scale(0.95)
        card.move_to(LEFT * 3.35 + DOWN * 0.15)

        slot = RoundedRectangle(
            width=3.25,
            height=1.45,
            corner_radius=0.16,
            stroke_color=ACCENT_PURPLE,
            stroke_width=1.8,
            fill_color=BG_SECONDARY,
            fill_opacity=0.86,
        )
        slot_label = self.label("primitive skill vocabulary", TEXT_PRIMARY, FONT_BODY, max_width=2.75, weight=BOLD)
        slot_hint = self.caption("Chapter 02: state-transition graph", TEXT_SECONDARY, max_width=2.7)
        VGroup(slot_label, slot_hint).arrange(DOWN, buff=0.16).move_to(slot)
        slot_group = VGroup(slot, slot_label, slot_hint).move_to(RIGHT * 2.45 + DOWN * 0.15)

        graph_nodes = VGroup(
            Circle(radius=0.12, color=ACCENT_PURPLE, fill_color=ACCENT_PURPLE, fill_opacity=1),
            Circle(radius=0.12, color=ACCENT_PURPLE, fill_color=ACCENT_PURPLE, fill_opacity=1),
            Circle(radius=0.12, color=ACCENT_PURPLE, fill_color=ACCENT_PURPLE, fill_opacity=1),
        )
        graph_nodes.arrange(RIGHT, buff=0.52).next_to(slot_group, DOWN, buff=0.38)
        graph_edges = VGroup(
            Arrow(graph_nodes[0].get_right(), graph_nodes[1].get_left(), buff=0.07, color=ACCENT_PURPLE, stroke_width=1.8, tip_length=0.12),
            Arrow(graph_nodes[1].get_right(), graph_nodes[2].get_left(), buff=0.07, color=ACCENT_PURPLE, stroke_width=1.8, tip_length=0.12),
        )
        graph = VGroup(graph_nodes, graph_edges)
        arrow = self.arrow_between(card, slot_group, ACCENT_PURPLE, buff=0.26)
        final = MathTex(
            "M=(\\mathrm{what},\\mathrm{where})\\;\\rightarrow\\;?",
            font_size=FONT_SUBTITLE,
            color=TEXT_PRIMARY,
        )
        final.next_to(VGroup(card, slot_group), DOWN, buff=1.15)

        stage = VGroup(card, slot_group, graph, arrow, final)
        self.set_stage(stage)
        self.play(DrawBorderThenFill(card), run_time=T_REVEAL_STD)
        self.play(GrowArrow(arrow), DrawBorderThenFill(slot), FadeIn(slot_label), run_time=T_REVEAL_STD)
        self.play(FadeIn(slot_hint, shift=UP * 0.08), LaggedStart(*[FadeIn(n) for n in graph_nodes], lag_ratio=0.12), run_time=T_REVEAL_FAST)
        self.play(LaggedStart(*[GrowArrow(edge) for edge in graph_edges], lag_ratio=0.12), Write(final), run_time=T_REVEAL_STD)
        self.wait(T_PAUSE_STD)
