import numpy as np

from utils.manim_compat import *
from utils.theme import *


def make_svg_icon(filename, color=WHITE, height=1.2):
    """Load a B&W SVG and style it."""
    svg = SVGMobject(str(svg_path(filename)))
    svg.set_color(color)
    svg.set_stroke(color, width=1.2)
    svg.scale_to_fit_height(height)
    return svg


def make_pill(
    text_str, color=ACCENT, font_size=16, fill_opacity=0.15, tex_escape=True
):
    """A rounded pill-shaped label."""
    label = Text(text_str, font_size=font_size, color=WHITE, tex_escape=tex_escape)
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
    """A glowing hexagon shape."""
    hex_shape = RegularPolygon(
        n=6,
        color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    hex_shape.scale(side_length)
    return hex_shape


def make_card(title, color, width=2.8, height=2.6):
    """A benchmark card with a title at top."""
    card = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        color=color,
        stroke_width=1.8,
        fill_color=color,
        fill_opacity=0.04,
    )
    title_label = Text(title, font_size=16, color=color, weight=BOLD)
    title_label.move_to(card.get_top() + DOWN * 0.3)
    return VGroup(card, title_label)


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
    """A single stair step block for spectrum charts."""
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


def make_neural_network_small(center, width=2.0, height=1.5, color=ACCENT):
    """A simple small neural-net illustration: nodes plus edges."""
    net = VGroup()
    layers = [3, 5, 4, 2]
    x_step = width / (len(layers) - 1)
    x_start = center[0] - width / 2
    y_center = center[1]

    node_positions = []
    for li, count in enumerate(layers):
        x = x_start + li * x_step
        y_start = y_center + (count - 1) * height / (2 * max(layers))
        col_positions = []
        for ni in range(count):
            y = y_start - ni * height / max(layers)
            col_positions.append(np.array([x, y, 0]))
        node_positions.append(col_positions)

    for li in range(len(layers) - 1):
        for p1 in node_positions[li]:
            for p2 in node_positions[li + 1]:
                net.add(
                    Line(
                        p1,
                        p2,
                        color=color,
                        stroke_width=2.0,
                        stroke_opacity=0.25,
                    )
                )

    for col in node_positions:
        for pos in col:
            net.add(Dot(pos, radius=0.04, color=color, fill_opacity=0.7))

    return net


def make_conveyor_belt(start, end, n_segments=12, color=DIM2):
    """A simple conveyor belt illustration."""
    belt = VGroup()
    direction = end - start
    length = np.linalg.norm(direction)
    unit = direction / length
    perp = np.array([-unit[1], unit[0], 0])
    belt_h = 0.12

    belt.add(
        Line(start + perp * belt_h, end + perp * belt_h, color=color, stroke_width=1.5),
        Line(start - perp * belt_h, end - perp * belt_h, color=color, stroke_width=1.5),
    )

    for i in range(n_segments + 1):
        t = i / n_segments
        pt = start + direction * t
        belt.add(
            Line(
                pt + perp * belt_h,
                pt - perp * belt_h,
                color=color,
                stroke_width=0.6,
                stroke_opacity=0.5,
            )
        )

    return belt
