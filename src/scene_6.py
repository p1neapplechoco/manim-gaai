from collections import namedtuple

import numpy as np

from utils.manim_compat import *
from utils.theme import *

ScalingFactor = namedtuple(
    "ScalingFactor",
    ["symbol", "label", "alpha", "constant_tex", "color"],
)

SCALING_FACTORS = (
    ScalingFactor("N", "model size", 0.076, r"8.8 \times 10^{13}", ACCENT),
    ScalingFactor("D", "data", 0.095, r"5.4 \times 10^{13}", GOLD),
    ScalingFactor("C", "compute", 0.050, r"3.1 \times 10^8", GREEN),
)


def loss_curve_points():
    return [
        (0.00, 0.94),
        (0.16, 0.78),
        (0.34, 0.60),
        (0.54, 0.43),
        (0.75, 0.29),
        (1.00, 0.18),
    ]


def make_attention_web(n_nodes=6, radius=0.75):
    nodes = VGroup()
    edges = VGroup()

    for i in range(n_nodes):
        angle = i * TAU / n_nodes - PI / 2
        dot = Dot(
            radius=0.055,
            color=WHITE,
            fill_opacity=0.75,
        )
        dot.move_to([radius * np.cos(angle), radius * np.sin(angle), 0])
        nodes.add(dot)

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            edge = Line(
                nodes[i].get_center(),
                nodes[j].get_center(),
                color=WHITE,
                stroke_width=0.8,
                stroke_opacity=0.24,
            )
            edges.add(edge)

    return VGroup(edges, nodes)


def make_transformer_block():
    box = RoundedRectangle(
        width=1.7,
        height=1.25,
        corner_radius=0.12,
        color=WHITE,
        stroke_width=1.6,
        fill_color=BG,
        fill_opacity=1,
    )

    rows = VGroup()
    for row_i in range(3):
        left = box.get_left() + RIGHT * 0.28 + UP * (0.32 - row_i * 0.32)
        right = box.get_right() + LEFT * 0.28 + UP * (0.32 - row_i * 0.32)
        rows.add(Line(left, right, color=DIM, stroke_width=1.0))

    heads = VGroup()
    for x in [-0.44, 0, 0.44]:
        head = Circle(
            radius=0.08,
            color=WHITE,
            stroke_width=1.2,
            fill_color=WHITE,
            fill_opacity=0.12,
        )
        head.move_to(box.get_center() + RIGHT * x + UP * 0.48)
        heads.add(head)

    return VGroup(box, rows, heads)


def make_model_size_icon():
    base = make_transformer_block().scale(0.72)

    blocks = VGroup()
    for i, scale in enumerate([0.45, 0.62, 0.82]):
        block = base.copy().scale(scale)
        block.move_to(LEFT * 0.55 + RIGHT * i * 0.55 + DOWN * 0.03)
        block.set_stroke(WHITE, width=1.2)
        blocks.add(block)

    arc = CurvedArrow(
        blocks[0].get_top() + UP * 0.05,
        blocks[-1].get_top() + UP * 0.05,
        angle=-0.45,
        color=WHITE,
        stroke_width=1.3,
        tip_length=0.12,
    )
    return VGroup(blocks, arc)


def make_data_icon():
    rows = VGroup()
    for i, width in enumerate([1.35, 1.05, 1.25, 0.85, 1.15]):
        line = RoundedRectangle(
            width=width,
            height=0.12,
            corner_radius=0.03,
            color=WHITE,
            stroke_width=1.0,
            fill_color=WHITE,
            fill_opacity=0.16,
        )
        line.move_to(UP * (0.42 - i * 0.2))
        rows.add(line)

    page = RoundedRectangle(
        width=1.75,
        height=1.3,
        corner_radius=0.08,
        color=WHITE,
        stroke_width=1.5,
        fill_color=BG,
        fill_opacity=1,
    )
    page.move_to(rows.get_center())

    token_dots = VGroup()
    for row in rows:
        token_dots.add(Dot(row.get_left() + RIGHT * 0.08, radius=0.025, color=WHITE))

    return VGroup(page, rows, token_dots)


def make_compute_icon():
    chip = RoundedRectangle(
        width=1.35,
        height=1.1,
        corner_radius=0.08,
        color=WHITE,
        stroke_width=1.6,
        fill_color=BG,
        fill_opacity=1,
    )

    core = Square(side_length=0.46, color=WHITE, stroke_width=1.2)
    core.move_to(chip)

    pins = VGroup()
    for x in [-0.45, -0.15, 0.15, 0.45]:
        pins.add(Line(UP * 0.55 + RIGHT * x, UP * 0.78 + RIGHT * x))
        pins.add(Line(DOWN * 0.55 + RIGHT * x, DOWN * 0.78 + RIGHT * x))
    for y in [-0.32, 0, 0.32]:
        pins.add(Line(LEFT * 0.68 + UP * y, LEFT * 0.9 + UP * y))
        pins.add(Line(RIGHT * 0.68 + UP * y, RIGHT * 0.9 + UP * y))
    pins.set_color(WHITE)
    pins.set_stroke(width=1.0, opacity=0.75)

    traces = VGroup(
        Line(core.get_top(), chip.get_top() + DOWN * 0.16, color=DIM, stroke_width=1.0),
        Line(
            core.get_bottom(),
            chip.get_bottom() + UP * 0.16,
            color=DIM,
            stroke_width=1.0,
        ),
        Line(
            core.get_left(), chip.get_left() + RIGHT * 0.18, color=DIM, stroke_width=1.0
        ),
        Line(
            core.get_right(),
            chip.get_right() + LEFT * 0.18,
            color=DIM,
            stroke_width=1.0,
        ),
    )

    return VGroup(chip, pins, traces, core)


def make_factor_icon(symbol):
    if symbol == "N":
        return make_model_size_icon()
    if symbol == "D":
        return make_data_icon()
    return make_compute_icon()


def make_factor_panels():
    panels = VGroup()

    for factor in SCALING_FACTORS:
        icon = make_factor_icon(factor.symbol)
        symbol = MathTex(factor.symbol, font_size=34, color=factor.color)
        label = Text(factor.label, font_size=15, color=DIM)
        panel = VGroup(icon, symbol, label).arrange(DOWN, buff=0.24)
        panels.add(panel)

    panels.arrange(RIGHT, buff=1.1)
    return panels


def make_equation_block():
    rows = VGroup()

    for factor in SCALING_FACTORS:
        equation = MathTex(
            rf"L({factor.symbol})",
            r"=",
            rf"\left(\frac{{{factor.symbol}_c}}{{{factor.symbol}}}\right)"
            rf"^{{\alpha_{factor.symbol}}}",
            font_size=28,
        )
        equation[0].set_color(factor.color)
        equation[2].set_color(WHITE)

        values = MathTex(
            rf"\alpha_{factor.symbol}\approx {factor.alpha:.3f},\quad "
            rf"{factor.symbol}_c\approx {factor.constant_tex}",
            font_size=14,
            color=DIM,
        )
        row = VGroup(equation, values).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        rows.add(row)

    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)

    brace = Brace(rows, LEFT, color=DIM)
    tag = Text("power law", font_size=16, color=DIM)
    tag.next_to(brace, LEFT, buff=0.16)
    return VGroup(brace, rows, tag)


def make_loss_graph():
    origin = LEFT * 3.7 + DOWN * 1.8
    width = 7.4
    height = 3.0

    x_axis = Arrow(
        origin,
        origin + RIGHT * width,
        buff=0,
        color=DIM,
        stroke_width=1.3,
        max_tip_length_to_length_ratio=0.025,
    )
    y_axis = Arrow(
        origin,
        origin + UP * height,
        buff=0,
        color=DIM,
        stroke_width=1.3,
        max_tip_length_to_length_ratio=0.06,
    )
    scale_label = Text("scale", font_size=15, color=DIM)
    scale_label.next_to(x_axis, RIGHT, buff=0.18)
    loss_label = Text("loss", font_size=15, color=DIM)
    loss_label.next_to(y_axis, UP, buff=0.12)

    def to_scene(point):
        x, y = point
        return origin + RIGHT * (x * (width - 0.35)) + UP * (y * (height - 0.35))

    curve = VMobject(color=GOLD, stroke_width=4)
    curve.set_points_smoothly([to_scene(point) for point in loss_curve_points()])

    dots = VGroup(
        *[
            Dot(to_scene(point), radius=0.045, color=WHITE, fill_opacity=0.9)
            for point in loss_curve_points()
        ]
    )

    guides = VGroup()
    for point in loss_curve_points()[1:-1]:
        scene_point = to_scene(point)
        guides.add(
            DashedLine(
                scene_point,
                np.array([scene_point[0], origin[1], 0]),
                color=DIM2,
                stroke_width=0.6,
                dash_length=0.07,
            )
        )

    lower_loss = VGroup(
        Text("lower", font_size=18, color=GOLD),
        Text("loss", font_size=18, color=GOLD),
    ).arrange(RIGHT, buff=0.14)
    lower_loss.next_to(dots[-1], UP, buff=0.18)

    graph = VGroup(
        x_axis, y_axis, scale_label, loss_label, guides, curve, dots, lower_loss
    )
    return graph


class ScalingLaws(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Echo the attention scene, then shrink it into one component.
        web = make_attention_web().move_to(UP * 0.8)
        transformer = make_transformer_block().move_to(ORIGIN)
        transformer_label = Text("Transformer", font_size=18, color=DIM)
        transformer_label.next_to(transformer, DOWN, buff=0.18)
        transformer_group = VGroup(transformer, transformer_label)

        self.play(
            FadeIn(web[1]),
            LaggedStart(*[Create(e) for e in web[0]], lag_ratio=0.01),
            run_time=1.0,
        )
        # [16:06] But what happens when we make these Transformers bigger?
        self.wait(2.0)
        self.play(ReplacementTransform(web, transformer_group), run_time=0.8)
        # [16:10] Transformers are the foundation — now scale them up
        self.wait(2.0)

        small = transformer.copy().scale(0.48).move_to(LEFT * 2.7 + DOWN * 0.15)
        medium = transformer.copy().scale(0.72).move_to(ORIGIN + DOWN * 0.05)
        large = transformer.copy().scale(1.05).move_to(RIGHT * 2.8)
        scale_stack = VGroup(small, medium, large)
        scale_stack.set_stroke(WHITE, width=1.2)

        self.play(
            transformer_group.animate.scale(0.55)
            .to_edge(UP, buff=0.45)
            .set_opacity(0.45),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                TransformFromCopy(transformer, small),
                TransformFromCopy(transformer, medium),
                TransformFromCopy(transformer, large),
                lag_ratio=0.18,
            ),
            run_time=1.2,
        )
        self.play(
            Flash(
                large.get_center(),
                color=WHITE,
                flash_radius=0.8,
                line_length=0.16,
                num_lines=10,
            ),
            run_time=0.45,
        )
        # [16:16] Researchers discovered: bigger models don't just get better slowly
        self.wait(3.0)

        self.play(
            FadeOut(scale_stack),
            FadeOut(transformer_group),
            run_time=0.6,
        )

        # The three independent factors are the main illustration.
        panels = make_factor_panels()
        panels.move_to(UP * 0.95)

        self.play(
            LaggedStart(
                *[FadeIn(panel[0], shift=UP * 0.1) for panel in panels],
                lag_ratio=0.16,
            ),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        FadeIn(panel[1], scale=0.85),
                        FadeIn(panel[2], shift=UP * 0.05),
                    )
                    for panel in panels
                ],
                lag_ratio=0.16,
            ),
            run_time=0.8,
        )

        factor_glows = VGroup()
        for panel, factor in zip(panels, SCALING_FACTORS):
            glow = SurroundingRectangle(
                panel[0],
                color=factor.color,
                buff=0.18,
                corner_radius=0.12,
                stroke_width=1.4,
                fill_color=factor.color,
                fill_opacity=0.04,
            )
            factor_glows.add(glow)

        self.play(
            LaggedStart(*[Create(glow) for glow in factor_glows], lag_ratio=0.12),
            run_time=0.8,
        )
        # [16:24] Three independent factors: model size, data, compute
        self.wait(5.0)

        # Compact mathematical statement, revealed after the pictures.
        equation_block = make_equation_block().scale(0.92)
        equation_block.move_to(DOWN * 1.05)

        self.play(
            VGroup(panels, factor_glows).animate.scale(0.78).to_edge(UP, buff=0.45),
            run_time=0.6,
        )
        for row in equation_block[1]:
            self.play(Write(row[0]), FadeIn(row[1], shift=UP * 0.04), run_time=0.65)
        self.play(
            GrowFromCenter(equation_block[0]), FadeIn(equation_block[2]), run_time=0.45
        )
        # [16:38] Each one follows a power-law relationship
        self.wait(4.0)

        # Turn the equations into the main intuition: more scale, lower loss.
        compact_factors = VGroup()
        for panel in panels:
            icon = panel[0].copy().scale(0.72)
            compact_factors.add(icon)
        compact_factors.arrange(RIGHT, buff=0.28)
        compact_factors.to_edge(UP, buff=0.35)

        graph = make_loss_graph()
        graph.move_to(DOWN * 0.25)

        self.play(
            FadeOut(equation_block),
            ReplacementTransform(
                VGroup(*[panel[0].copy() for panel in panels]), compact_factors
            ),
            FadeOut(VGroup(*[panel[1:] for panel in panels])),
            FadeOut(VGroup(panels, factor_glows)),
            run_time=0.7,
        )
        self.play(
            Create(graph[0]),
            Create(graph[1]),
            FadeIn(graph[2]),
            FadeIn(graph[3]),
            run_time=0.55,
        )
        self.play(
            LaggedStart(*[Create(g) for g in graph[4]], lag_ratio=0.04), run_time=0.5
        )
        self.play(Create(graph[5]), run_time=1.4)
        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.6) for dot in graph[6]], lag_ratio=0.07),
            run_time=0.6,
        )
        self.play(FadeIn(graph[7], shift=UP * 0.08), run_time=0.45)

        arrows = VGroup()
        for icon, proportion in zip(compact_factors, [0.56, 0.66, 0.76]):
            arrows.add(
                Line(
                    icon.get_bottom(),
                    graph[5].point_from_proportion(proportion),
                    color=DIM,
                    stroke_width=0.8,
                    stroke_opacity=0.5,
                )
            )

        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1), run_time=0.7
        )
        self.play(
            Flash(
                graph[5].point_from_proportion(0.76),
                color=GOLD,
                flash_radius=0.45,
                line_length=0.12,
                num_lines=8,
            ),
            run_time=0.5,
        )
        # [16:55] More scale, lower loss — a smooth, predictable curve
        self.wait(3.0)

        self.play(
            FadeOut(compact_factors),
            FadeOut(arrows),
            FadeOut(graph),
            run_time=0.9,
        )
