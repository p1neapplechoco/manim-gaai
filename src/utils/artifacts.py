import numpy as np

from utils.manim_compat import *

VIEWBOX_WIDTH = 870
VIEWBOX_HEIGHT = 470

DARK_WALL = "#2A2A2A"
DARK_FLOOR = "#1E1B17"
SHELF_BACK = "#1A1510"
SHELF_WOOD = "#9A7550"
FRAME_DARK = "#7A5C3A"
FRAME_MID = "#8A6A44"
FRAME_LIGHT = "#9A7A54"
BASE_DARK = "#6A4A28"
LAMP_METAL = "#8A7A60"
LAMP_BASE = "#7A6A50"
LAMP_SHADE = "#C8A030"
LAMP_SHADE_STROKE = "#A07820"
LAMP_GLOW = "#FCDE9C"
TEXT_DIM = "#888888"

SHELF_ORIGINS = (30, 308, 586)
SHELF_WIDTH = 245
SHELF_HEIGHT = 340
SHELF_TOP = 50
SHELF_BOARDS = (376, 309, 242, 175, 108)

BOOK_COLORS = [
    "#C8314A",
    "#3A6FB5",
    "#D4924A",
    "#5A8A3A",
    "#8A3A7A",
    "#C8A040",
    "#5A7A9A",
    "#C85A3A",
    "#5A4A8A",
    "#B84A30",
    "#3A8A60",
    "#D4A848",
    "#6A3A5A",
    "#4A7AAA",
    "#C87840",
    "#A03030",
    "#2A6A9A",
    "#7A9A2A",
    "#B06840",
    "#5A3A8A",
    "#3A8A7A",
    "#C8883A",
    "#4A6A9A",
    "#C83A50",
    "#6A9A3A",
    "#9A3A4A",
    "#4A5A9A",
    "#C8A830",
    "#5A8A5A",
    "#B85030",
]

BOOK_WIDTHS = (16, 13, 18, 14, 15, 17, 13, 16, 14, 18, 13, 16, 14)
LOWER_BOOK_HEIGHTS = (57, 52, 59, 54, 60, 55, 58, 53, 59, 56, 54, 60, 55)
TOP_BOOK_HEIGHTS = (44, 47, 44, 46, 44, 47, 44, 46, 44, 47, 44, 46, 44)
ROW_BOTTOMS = (375, 308, 241, 174, 107)


def scale_px(value):
    return value * config.frame_width / VIEWBOX_WIDTH


def svg_point(x, y, z=0):
    return np.array(
        [
            scale_px(x - VIEWBOX_WIDTH / 2),
            scale_px(VIEWBOX_HEIGHT / 2 - y),
            z,
        ]
    )


def svg_rect(
    x,
    y,
    width,
    height,
    fill_color,
    *,
    fill_opacity=1,
    stroke_color=None,
    stroke_width=0,
    stroke_opacity=1,
    corner_radius=0,
):
    if corner_radius > 0:
        rect = RoundedRectangle(
            width=scale_px(width),
            height=scale_px(height),
            corner_radius=scale_px(corner_radius),
        )
    else:
        rect = Rectangle(width=scale_px(width), height=scale_px(height))

    rect.set_fill(fill_color, opacity=fill_opacity)
    rect.set_stroke(
        stroke_color or fill_color,
        width=stroke_width,
        opacity=stroke_opacity if stroke_width else 0,
    )
    rect.move_to(svg_point(x + width / 2, y + height / 2))
    return rect


def svg_line(x1, y1, x2, y2, color, *, stroke_width=1, stroke_opacity=1):
    return Line(
        svg_point(x1, y1),
        svg_point(x2, y2),
        color=color,
        stroke_width=stroke_width,
        stroke_opacity=stroke_opacity,
    )


def svg_polygon(
    points, fill_color, *, fill_opacity=1, stroke_color=None, stroke_width=0
):
    polygon = Polygon(
        *[svg_point(x, y) for x, y in points],
        color=stroke_color or fill_color,
        stroke_width=stroke_width,
    )
    polygon.set_fill(fill_color, opacity=fill_opacity)
    polygon.set_stroke(stroke_color or fill_color, width=stroke_width)
    return polygon


def svg_circle(cx, cy, radius, fill_color, *, fill_opacity=1):
    circle = Circle(radius=scale_px(radius), stroke_width=0)
    circle.set_fill(fill_color, opacity=fill_opacity)
    circle.move_to(svg_point(cx, cy))
    return circle


def svg_ellipse(cx, cy, rx, ry, fill_color, *, fill_opacity=1):
    ellipse = Ellipse(width=scale_px(rx * 2), height=scale_px(ry * 2), stroke_width=0)
    ellipse.set_fill(fill_color, opacity=fill_opacity)
    ellipse.move_to(svg_point(cx, cy))
    return ellipse


def make_background():
    return VGroup(
        svg_rect(0, 390, VIEWBOX_WIDTH, 80, DARK_FLOOR),
        svg_line(0, 390, 860, 390, SHELF_WOOD, stroke_width=1.2, stroke_opacity=0.5),
    )


def make_book(x, bottom_y, width, height, color):
    return svg_rect(
        x,
        bottom_y - height,
        width,
        height,
        color,
        corner_radius=1,
    )


def make_book_row(unit_x, bottom_y, row_index, color_offset=0):
    row = VGroup()
    x_cursor = unit_x + 12
    heights = TOP_BOOK_HEIGHTS if row_index == 4 else LOWER_BOOK_HEIGHTS

    for book_index, width in enumerate(BOOK_WIDTHS):
        height = heights[(book_index + row_index * 2) % len(heights)]
        color = BOOK_COLORS[
            (color_offset + row_index * 7 + book_index) % len(BOOK_COLORS)
        ]
        row.add(make_book(x_cursor, bottom_y, width, height, color))
        x_cursor += width + 2

    return row


def make_shelf_unit(unit_x, color_offset=0):
    unit = VGroup()

    unit.add(svg_rect(unit_x, SHELF_TOP, SHELF_WIDTH, SHELF_HEIGHT, SHELF_BACK))
    unit.add(svg_rect(unit_x, SHELF_TOP, 10, SHELF_HEIGHT, FRAME_DARK))
    unit.add(
        svg_rect(unit_x + SHELF_WIDTH - 10, SHELF_TOP, 10, SHELF_HEIGHT, FRAME_DARK)
    )
    unit.add(svg_rect(unit_x, SHELF_TOP, SHELF_WIDTH, 9, FRAME_MID))
    unit.add(svg_rect(unit_x - 4, 43, SHELF_WIDTH + 8, 7, FRAME_LIGHT, corner_radius=1))
    unit.add(svg_rect(unit_x, 383, SHELF_WIDTH, 7, BASE_DARK))

    for board_y in SHELF_BOARDS:
        unit.add(svg_rect(unit_x, board_y, SHELF_WIDTH, 7, SHELF_WOOD))

    for row_index, bottom_y in enumerate(ROW_BOTTOMS):
        unit.add(make_book_row(unit_x, bottom_y, row_index, color_offset=color_offset))

    return unit


def make_shelves():
    shelves = VGroup()
    for unit_index, unit_x in enumerate(SHELF_ORIGINS):
        shelves.add(make_shelf_unit(unit_x, color_offset=unit_index * 10))
    return shelves


def make_reading_lamp():
    glow_cone = svg_polygon(
        [(308, 193), (362, 193), (390, 390), (280, 390)],
        LAMP_GLOW,
        fill_opacity=0.04,
    )
    floor_glow = svg_ellipse(335, 390, 38, 6, LAMP_GLOW, fill_opacity=0.10)
    pole = svg_rect(289, 168, 5, 222, LAMP_METAL, corner_radius=2)
    base = svg_rect(277, 384, 29, 6, LAMP_BASE, corner_radius=2)
    neck = svg_rect(281, 380, 21, 6, "#6A5A44", corner_radius=1)
    arm = svg_line(291, 170, 335, 157, LAMP_METAL, stroke_width=3.5)
    shade = svg_polygon(
        [(313, 157), (357, 157), (368, 193), (302, 193)],
        LAMP_SHADE,
        stroke_color=LAMP_SHADE_STROKE,
        stroke_width=0.8,
    )
    shade_highlight = svg_polygon(
        [(317, 160), (353, 160), (362, 188), (308, 188)],
        "#FCDE80",
        fill_opacity=0.35,
    )
    bulb = svg_circle(335, 158, 2.5, "#FFF8D0", fill_opacity=0.9)

    return VGroup(
        glow_cone,
        floor_glow,
        pole,
        base,
        neck,
        arm,
        shade,
        shade_highlight,
        bulb,
    )


def build_library_scene():
    return VGroup(
        make_background(),
        make_shelves(),
        make_reading_lamp(),
    )


def make_outline(mobject, *, stroke_width=1.0, stroke_opacity=0.95):
    outline = mobject.copy()
    for piece in outline.family_members_with_points():
        if not isinstance(piece, VMobject):
            continue

        color = piece.get_fill_color()
        if piece.get_fill_opacity() == 0:
            color = piece.get_stroke_color()

        piece.set_fill(opacity=0)
        piece.set_stroke(
            color=color,
            width=max(piece.get_stroke_width(), stroke_width),
            opacity=stroke_opacity,
        )
    return outline


def outline_first(mobject, *, run_time=1.5, lag_ratio=0.08):
    outline = make_outline(mobject)
    outline_submobjects = list(outline) or [outline]

    return Succession(
        LaggedStart(
            *[Create(submob) for submob in outline_submobjects],
            lag_ratio=lag_ratio,
            run_time=run_time * 0.58,
        ),
        ReplacementTransform(outline, mobject, run_time=run_time * 0.42),
    )
