from manim import *
import textwrap
import numpy as np


BG_PRIMARY = "#000000"
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

FONT_TITLE = 40
FONT_SUBTITLE = 30
FONT_BODY = 24
FONT_CAPTION = 18

EDGE_MARGIN = 0.5
GAP_MEDIUM = 0.5
GAP_SMALL = 0.25

T_REVEAL_STD = 0.8
T_REVEAL_FAST = 0.4
T_TRANS_STD = 0.5
T_PAUSE_LONG = 2.5
T_PAUSE_STD = 1.5
T_PAUSE_SHORT = 0.8

TITLE_FONT = "Avenir Next"
ANIMATION_TIME_SCALE = 3.75


class V5BaseScene(MovingCameraScene):
    chapter = 0
    beats = []

    def setup(self):
        self.camera.background_color = BG_PRIMARY
        self.title = None
        self.stage = VGroup()
        self.progress = self.chapter_progress(self.chapter, 9)
        self.add(self.progress)

    def construct(self):
        for beat in self.beats:
            self.render_beat(beat)
        self.wait(T_PAUSE_LONG)

    def play(self, *animations, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] *= ANIMATION_TIME_SCALE
        return super().play(*animations, **kwargs)

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

    def content_text(self, text, font_size=FONT_BODY, color=TEXT_SECONDARY, max_width=None, weight=NORMAL):
        def build(line, size):
            body = self.tex_escape(line)
            if weight == BOLD:
                body = r"\textbf{" + body + "}"
            return Tex(body, font_size=size, color=color)

        mob = build(text, font_size)
        if not max_width or mob.width <= max_width:
            return mob

        fitted = max(FONT_CAPTION, font_size * max_width / mob.width)
        mob = build(text, fitted)
        if mob.width <= max_width:
            return mob

        words = text.split()
        if not words:
            return mob
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
        return group

    def label(self, text, color=TEXT_SECONDARY, size=FONT_BODY, max_width=2.8, weight=NORMAL):
        return self.content_text(text, size, color, max_width=max_width, weight=weight)

    def caption(self, text, color=TEXT_MUTED, max_width=3.2):
        return self.content_text(text, FONT_CAPTION, color, max_width=max_width)

    def make_title(self, text):
        lines = textwrap.wrap(text, width=42, break_long_words=False)
        title = VGroup(
            *[
                Text(line, font=TITLE_FONT, font_size=FONT_TITLE, color=TEXT_PRIMARY, weight=BOLD)
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

    def set_stage(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage, shift=DOWN * 0.08), run_time=T_TRANS_STD, rate_func=rush_into)
        self.stage = new_stage

    def chapter_progress(self, current, total):
        dots = []
        for idx in range(1, total + 1):
            active = idx == current
            dots.append(
                Circle(
                    radius=0.045 if not active else 0.07,
                    stroke_width=1.2,
                    stroke_color=TEXT_PRIMARY if active else TEXT_MUTED,
                    fill_color=TEXT_PRIMARY if active else TEXT_MUTED,
                    fill_opacity=1,
                )
            )
        rail = VGroup(*dots).arrange(RIGHT, buff=0.18)
        label = self.caption(f"{current:02d}/{total:02d}", TEXT_MUTED, max_width=0.8).next_to(
            rail, RIGHT, buff=GAP_SMALL
        )
        return VGroup(rail, label).to_edge(DOWN, buff=0.28).to_edge(RIGHT, buff=0.55)

    def box(self, label, width=2.3, height=1.0, accent=ACCENT_BLUE, fill=BG_SECONDARY, size=FONT_CAPTION):
        rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.13,
            stroke_color=accent,
            stroke_width=1.5,
            fill_color=fill,
            fill_opacity=0.92,
        )
        text = self.label(label, TEXT_PRIMARY, size, max_width=width - 0.25, weight=BOLD).move_to(rect)
        return VGroup(rect, text)

    def chip(self, label, accent=ACCENT_PURPLE, width=1.34):
        rect = RoundedRectangle(
            width=width,
            height=0.52,
            corner_radius=0.12,
            stroke_color=accent,
            stroke_width=1.3,
            fill_color=BG_TERTIARY,
            fill_opacity=1,
        )
        text = self.label(label, TEXT_PRIMARY, FONT_CAPTION, max_width=width - 0.2).move_to(rect)
        return VGroup(rect, text)

    def arrow_between(self, left, right, color=ACCENT_BLUE, buff=0.18):
        return Arrow(left.get_right(), right.get_left(), buff=buff, color=color, stroke_width=2.3, tip_length=0.17)

    def render_beat(self, beat):
        self.set_title(beat["title"])
        stage = self.visual(beat)
        self.set_stage(stage)
        self.play(FadeIn(stage, shift=UP * 0.18), run_time=T_REVEAL_STD)
        if "emphasis" in beat:
            target = stage[beat["emphasis"]]
            self.play(Indicate(target, color=beat.get("emphasis_color", ACCENT_AMBER)), run_time=T_REVEAL_FAST)
        self.wait(beat.get("pause", T_PAUSE_STD))

    def visual(self, beat):
        kind = beat["kind"]
        if kind == "handoff":
            return self.v_handoff(**beat)
        if kind == "blocks":
            return self.v_blocks(**beat)
        if kind == "sphere":
            return self.v_sphere(**beat)
        if kind == "matrix":
            return self.v_matrix(**beat)
        if kind == "graph":
            return self.v_graph(**beat)
        if kind == "chips":
            return self.v_chips(**beat)
        if kind == "pipeline":
            return self.v_pipeline(**beat)
        if kind == "gates":
            return self.v_gates(**beat)
        if kind == "loop":
            return self.v_loop(**beat)
        if kind == "compare":
            return self.v_compare(**beat)
        if kind == "domains":
            return self.v_domains(**beat)
        if kind == "equation":
            return self.v_equation(**beat)
        if kind == "spectrum":
            return self.v_spectrum(**beat)
        return self.v_chips(**beat)

    def v_handoff(self, left="handoff", right="next object", equation=None, accent=ACCENT_AMBER, **_):
        lbox = self.box(left, 3.2, 1.25, accent).move_to(LEFT * 3.05)
        rbox = self.box(right, 3.2, 1.25, ACCENT_PURPLE).move_to(RIGHT * 3.05)
        arrow = self.arrow_between(lbox, rbox, ACCENT_PURPLE)
        group = VGroup(lbox, arrow, rbox)
        if equation:
            eq = MathTex(equation, font_size=FONT_SUBTITLE, color=TEXT_PRIMARY).next_to(group, DOWN, buff=0.55)
            group.add(eq)
        return group.move_to(DOWN * 0.15)

    def v_blocks(self, label_a="A", label_b="B", relation="contact", accent=ACCENT_BLUE, **_):
        base = Line(LEFT * 2.7, RIGHT * 2.7, color=BORDER_COLOR, stroke_width=1.4)
        a = Square(0.74, stroke_color=accent, fill_color=BG_TERTIARY, fill_opacity=1, stroke_width=1.8)
        b = a.copy()
        ta = self.label(label_a, TEXT_PRIMARY, FONT_BODY, max_width=0.5).move_to(a)
        tb = self.label(label_b, TEXT_PRIMARY, FONT_BODY, max_width=0.5).move_to(b)
        ga = VGroup(a, ta)
        gb = VGroup(b, tb).next_to(ga, UP, buff=0.05)
        stack = VGroup(base, ga, gb).arrange(DOWN, buff=-0.08).move_to(LEFT * 2.6 + DOWN * 0.2)
        dirs = VGroup(
            Arrow(ORIGIN, RIGHT * 1.3, color=ACCENT_AMBER, stroke_width=2.2, tip_length=0.15),
            Arrow(ORIGIN, UP * 0.85, color=ACCENT_AMBER, stroke_width=2.2, tip_length=0.15),
            DashedLine(ORIGIN, DOWN * 0.85, color=TEXT_MUTED, stroke_width=1.5),
        ).arrange(RIGHT, buff=0.35)
        dir_label = self.caption("movable vs constrained directions", TEXT_SECONDARY, max_width=3.0).next_to(
            dirs, DOWN, buff=0.22
        )
        relation_label = self.label(relation, ACCENT_AMBER, FONT_BODY, max_width=2.2, weight=BOLD).next_to(
            stack, UP, buff=0.2
        )
        right = VGroup(dirs, dir_label).move_to(RIGHT * 2.45 + DOWN * 0.05)
        arrow = self.arrow_between(stack, right, ACCENT_AMBER, buff=0.3)
        return VGroup(relation_label, stack, arrow, right)

    def v_sphere(self, equation="constraints", note="feasible region", **_):
        circle = Circle(radius=1.45, stroke_color=ACCENT_BLUE, stroke_width=2, fill_color=BG_SECONDARY, fill_opacity=0.25)
        axes = VGroup(
            Line(circle.get_left(), circle.get_right(), color=BORDER_COLOR, stroke_width=1.2),
            Line(circle.get_bottom(), circle.get_top(), color=BORDER_COLOR, stroke_width=1.2),
            Arc(radius=1.0, start_angle=0.2, angle=1.2, color=ACCENT_AMBER, stroke_width=5),
        )
        eq = MathTex(equation, font_size=FONT_SUBTITLE, color=TEXT_PRIMARY).next_to(circle, UP, buff=0.35)
        note_m = self.label(note, ACCENT_AMBER, FONT_BODY, max_width=3.0, weight=BOLD).next_to(circle, DOWN, buff=0.35)
        return VGroup(eq, circle, axes, note_m).move_to(DOWN * 0.25)

    def v_matrix(self, rows=7, cols=7, label="49 candidate transitions", **_):
        cells = VGroup()
        for _ in range(rows * cols):
            cells.add(Square(0.23, stroke_color=BORDER_COLOR, stroke_width=0.7, fill_color=BG_SECONDARY, fill_opacity=0.55))
        cells.arrange_in_grid(rows=rows, cols=cols, buff=0.04)
        brace = Brace(cells, DOWN, color=ACCENT_AMBER)
        count = self.label(label, ACCENT_AMBER, FONT_BODY, max_width=3.8, weight=BOLD).next_to(brace, DOWN, buff=0.18)
        side = MathTex(f"{rows}\\times {cols}", font_size=FONT_SUBTITLE, color=TEXT_PRIMARY).next_to(cells, UP, buff=0.28)
        return VGroup(side, cells, brace, count).move_to(DOWN * 0.25)

    def v_graph(self, labels=None, highlight=None, caption="filtered transition graph", **_):
        labels = labels or ["NC", "PC", "PR", "OP", "OR", "S", "D"]
        points = [LEFT * 2.7, LEFT * 1.45 + UP * 0.85, ORIGIN + UP * 1.1, RIGHT * 1.45 + UP * 0.85, RIGHT * 2.7, RIGHT * 1.25 + DOWN * 0.95, LEFT * 1.25 + DOWN * 0.95]
        nodes = VGroup()
        for label, point in zip(labels, points):
            node = Circle(radius=0.28, stroke_color=ACCENT_BLUE, fill_color=BG_SECONDARY, fill_opacity=1, stroke_width=1.6).move_to(point)
            nodes.add(VGroup(node, self.label(label, TEXT_PRIMARY, FONT_CAPTION, max_width=0.55).move_to(node)))
        edges = VGroup()
        edge_pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (2, 6), (6, 0), (5, 4)]
        for idx, (a, b) in enumerate(edge_pairs):
            color = ACCENT_AMBER if highlight and idx in highlight else ACCENT_BLUE
            edges.add(Arrow(nodes[a].get_center(), nodes[b].get_center(), buff=0.34, color=color, stroke_width=1.9, tip_length=0.12))
        cap = self.label(caption, ACCENT_AMBER, FONT_BODY, max_width=4.4, weight=BOLD).next_to(VGroup(nodes, edges), DOWN, buff=0.42)
        return VGroup(edges, nodes, cap).move_to(DOWN * 0.2)

    def v_chips(self, heading="library", chips=None, accent=ACCENT_PURPLE, **_):
        chips = chips or ["Pick", "Bring", "Place"]
        box = RoundedRectangle(width=6.0, height=2.35, corner_radius=0.16, stroke_color=accent, stroke_width=1.5, fill_color=BG_SECONDARY, fill_opacity=0.86)
        title = self.label(heading, accent, FONT_BODY, max_width=4.2, weight=BOLD).next_to(box, UP, buff=0.16)
        chip_group = VGroup(*[self.chip(chip, accent, width=max(1.25, min(1.85, 0.18 * len(chip) + 0.75))) for chip in chips])
        chip_group.arrange_in_grid(rows=2 if len(chips) > 4 else 1, buff=(0.25, 0.24)).move_to(box)
        return VGroup(box, title, chip_group).move_to(DOWN * 0.15)

    def v_pipeline(self, steps=None, accent=ACCENT_BLUE, result_color=ACCENT_GREEN, **_):
        steps = steps or ["input", "model", "agent", "robot"]
        boxes = VGroup()
        for i, step in enumerate(steps):
            color = result_color if i == len(steps) - 1 else accent
            boxes.add(self.box(step, width=1.85, height=0.86, accent=color, size=FONT_CAPTION))
        boxes.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.15)
        arrows = VGroup(*[self.arrow_between(boxes[i], boxes[i + 1], accent, buff=0.15) for i in range(len(boxes) - 1)])
        return VGroup(boxes, arrows)

    def v_gates(self, left="physical", right="semantic", outcome="valid transition", **_):
        source = self.box("candidate edge", 2.0, 0.9, ACCENT_BLUE).move_to(LEFT * 4.2)
        gate1 = self.box(left, 1.9, 1.15, ACCENT_AMBER).move_to(LEFT * 1.45)
        gate2 = self.box(right, 1.9, 1.15, ACCENT_PURPLE).move_to(RIGHT * 1.45)
        out = self.box(outcome, 2.25, 0.9, ACCENT_GREEN).move_to(RIGHT * 4.25)
        arrows = VGroup(
            self.arrow_between(source, gate1, ACCENT_AMBER),
            self.arrow_between(gate1, gate2, ACCENT_PURPLE),
            self.arrow_between(gate2, out, ACCENT_GREEN),
        )
        return VGroup(source, gate1, gate2, out, arrows).move_to(DOWN * 0.1)

    def v_loop(self, nodes=None, center="policy", accent=ACCENT_PURPLE, **_):
        nodes = nodes or ["state", "action", "feedback", "update"]
        center_box = self.box(center, 2.0, 1.0, accent).move_to(ORIGIN)
        positions = [UP * 1.55, RIGHT * 2.75, DOWN * 1.55, LEFT * 2.75]
        boxes = VGroup(*[self.box(n, 1.55, 0.72, ACCENT_BLUE, size=FONT_CAPTION).move_to(pos) for n, pos in zip(nodes, positions)])
        arrows = VGroup()
        for i in range(len(boxes)):
            arrows.add(Arrow(boxes[i].get_center(), boxes[(i + 1) % len(boxes)].get_center(), buff=0.58, color=accent, stroke_width=2.0, tip_length=0.14))
        return VGroup(arrows, boxes, center_box).move_to(DOWN * 0.1)

    def v_compare(self, left="trajectory", right="state relation", bad=False, **_):
        left_box = self.box(left, 3.2, 1.7, ACCENT_CORAL if bad else ACCENT_BLUE).move_to(LEFT * 2.6)
        right_box = self.box(right, 3.2, 1.7, ACCENT_GREEN).move_to(RIGHT * 2.6)
        left_curve = VMobject(color=ACCENT_CORAL if bad else ACCENT_BLUE, stroke_width=3)
        left_curve.set_points_smoothly([left_box.get_center() + LEFT * 0.9 + DOWN * 0.35, left_box.get_center() + UP * 0.6, left_box.get_center() + RIGHT * 0.85 + DOWN * 0.25])
        relation = MathTex("s_t\\rightarrow s_{t+1}", font_size=FONT_SUBTITLE, color=ACCENT_GREEN).move_to(right_box)
        arrow = self.arrow_between(left_box, right_box, ACCENT_AMBER, buff=0.28)
        return VGroup(left_box, left_curve, arrow, right_box, relation).move_to(DOWN * 0.1)

    def v_domains(self, panels=None, **_):
        panels = panels or ["contact", "mating", "topology", "key pose"]
        group = VGroup()
        for name in panels:
            panel = self.box(name, 2.35, 1.25, ACCENT_BLUE, size=FONT_CAPTION)
            icon = self.domain_icon(name).next_to(panel[0], DOWN, buff=-0.82)
            group.add(VGroup(panel, icon))
        group.arrange_in_grid(rows=2, cols=2, buff=(0.65, 0.5)).move_to(DOWN * 0.12)
        return group

    def domain_icon(self, name):
        if "mating" in name:
            return VGroup(Square(0.32, color=ACCENT_AMBER), Circle(0.18, color=ACCENT_AMBER)).arrange(RIGHT, buff=0.08)
        if "topology" in name:
            return ParametricFunction(lambda t: np.array([0.42 * np.sin(t), 0.24 * np.sin(2 * t), 0]), t_range=[0, TAU], color=ACCENT_AMBER, stroke_width=2)
        if "pose" in name or "dance" in name:
            return VGroup(Circle(0.08, color=ACCENT_AMBER), Line(UP * 0.02, DOWN * 0.45, color=ACCENT_AMBER), Line(LEFT * 0.28 + DOWN * 0.16, RIGHT * 0.28 + DOWN * 0.16, color=ACCENT_AMBER))
        return VGroup(Square(0.3, color=ACCENT_AMBER), Square(0.3, color=ACCENT_AMBER).shift(UP * 0.32))

    def v_equation(self, equation, left=None, right=None, accent=ACCENT_AMBER, **_):
        eq = MathTex(equation, font_size=FONT_TITLE, color=accent).move_to(ORIGIN + UP * 0.1)
        group = VGroup(eq)
        if left:
            lbox = self.box(left, 2.5, 0.9, ACCENT_BLUE).next_to(eq, LEFT, buff=0.9)
            group.add(lbox, self.arrow_between(lbox, eq, ACCENT_BLUE, buff=0.25))
        if right:
            rbox = self.box(right, 2.5, 0.9, ACCENT_GREEN).next_to(eq, RIGHT, buff=0.9)
            group.add(rbox, self.arrow_between(eq, rbox, ACCENT_GREEN, buff=0.25))
        return group.move_to(DOWN * 0.05)

    def v_spectrum(self, labels=None, **_):
        labels = labels or ["gesture", "navigation", "manipulation", "locomotion"]
        line = Line(LEFT * 4.2, RIGHT * 4.2, color=BORDER_COLOR, stroke_width=2)
        ticks = VGroup()
        for i, label in enumerate(labels):
            x = -4.2 + i * (8.4 / (len(labels) - 1))
            tick = Line(UP * 0.12, DOWN * 0.12, color=ACCENT_BLUE, stroke_width=2).move_to(RIGHT * x)
            text = self.caption(label, TEXT_SECONDARY, max_width=1.5).next_to(tick, DOWN, buff=0.18)
            ticks.add(VGroup(tick, text))
        local = self.label("more local feedback", ACCENT_AMBER, FONT_BODY, max_width=3.0, weight=BOLD).next_to(line, UP, buff=0.35)
        arrow = Arrow(line.get_left(), line.get_right(), buff=0, color=ACCENT_AMBER, stroke_width=2.2, tip_length=0.16)
        return VGroup(line, arrow, ticks, local).move_to(DOWN * 0.05)
