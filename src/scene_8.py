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


def make_svg_icon(filename, color=WHITE, height=1.2):
    """Load a B&W SVG and style it."""
    svg = SVGMobject(str(BASE_DIR / "assets" / "svgs" / filename))
    svg.set_color(color)
    svg.set_stroke(color, width=1.2)
    svg.scale_to_fit_height(height)
    return svg


def make_neural_network_small(center, width=2.0, height=1.5, color=ACCENT):
    """A simple small neural-net illustration: nodes + edges."""
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

    # Edges
    for li in range(len(layers) - 1):
        for p1 in node_positions[li]:
            for p2 in node_positions[li + 1]:
                edge = Line(
                    p1,
                    p2,
                    color=color,
                    stroke_width=0.4,
                    stroke_opacity=0.25,
                )
                net.add(edge)

    # Nodes
    for li, col in enumerate(node_positions):
        for pos in col:
            dot = Dot(
                pos,
                radius=0.04,
                color=color,
                fill_opacity=0.7,
            )
            net.add(dot)

    return net


def make_conveyor_belt(start, end, n_segments=12, color=DIM2):
    """A simple conveyor belt illustration (two lines + rollers)."""
    belt = VGroup()
    direction = end - start
    length = np.linalg.norm(direction)
    unit = direction / length
    perp = np.array([-unit[1], unit[0], 0])
    belt_h = 0.12

    top_line = Line(
        start + perp * belt_h, end + perp * belt_h, color=color, stroke_width=1.5
    )
    bot_line = Line(
        start - perp * belt_h, end - perp * belt_h, color=color, stroke_width=1.5
    )
    belt.add(top_line, bot_line)

    # Rollers
    for i in range(n_segments + 1):
        t = i / n_segments
        pt = start + direction * t
        roller = Line(
            pt + perp * belt_h,
            pt - perp * belt_h,
            color=color,
            stroke_width=0.6,
            stroke_opacity=0.5,
        )
        belt.add(roller)

    return belt


class FromChatbotsToAgents(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ==============================================================
        #  PART 1 — "It's tempting to think of these as Q&A machines"
        #  Show: input → box → output (simple, mechanical)
        # ==============================================================

        # Simple "machine" box in the center
        machine_box = RoundedRectangle(
            width=2.4,
            height=1.6,
            corner_radius=0.15,
            color=ACCENT,
            stroke_width=2,
            fill_color=ACCENT,
            fill_opacity=0.06,
        )
        machine_box.move_to(ORIGIN)

        # Robot icon inside the machine
        robot_icon = make_svg_icon("robot.svg", color=WHITE, height=1.0)
        robot_icon.move_to(machine_box.get_center())

        # "input" label (left) and "output" label (right)
        input_label = Text("input", font_size=16, color=DIM)
        input_label.move_to(LEFT * 4.0)
        output_label = Text("output", font_size=16, color=DIM)
        output_label.move_to(RIGHT * 4.0)

        # Arrows
        in_arrow = Arrow(
            input_label.get_right(),
            machine_box.get_left(),
            buff=0.2,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )
        out_arrow = Arrow(
            machine_box.get_right(),
            output_label.get_left(),
            buff=0.2,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # Show examples cycling: sentence→sentence, image→description
        example_inputs = [
            Text('"Hello, how are you?"', font_size=14, color=ACCENT),
            # We'll represent an image as a small rectangle with grid
            VGroup(
                RoundedRectangle(
                    width=0.9,
                    height=0.7,
                    corner_radius=0.06,
                    color=TEAL,
                    stroke_width=1.2,
                    fill_color=TEAL,
                    fill_opacity=0.12,
                ),
                Text("🖼", font_size=24),
            ),
        ]
        example_outputs = [
            Text('"I\'m doing well!"', font_size=14, color=GOLD),
            Text('"A dog playing in the park"', font_size=12, color=GOLD),
        ]

        for ex in example_inputs:
            ex.move_to(LEFT * 4.0 + DOWN * 0.7)
        for ex in example_outputs:
            ex.move_to(RIGHT * 4.0 + DOWN * 0.7)

        # Animate
        self.play(
            FadeIn(machine_box, scale=0.9),
            FadeIn(robot_icon, scale=0.85),
            run_time=0.7,
        )
        self.play(
            FadeIn(input_label),
            FadeIn(output_label),
            GrowArrow(in_arrow),
            GrowArrow(out_arrow),
            run_time=0.6,
        )
        # [19:05] So far, we've been thinking of models as Q&A machines
        self.wait(1.0)

        # Show first example: text → text
        self.play(FadeIn(example_inputs[0], shift=UP * 0.1), run_time=0.4)
        self.wait(0.2)

        # Pulse to show processing
        pulse = machine_box.copy().set_stroke(ACCENT, width=4, opacity=0.6)
        self.play(FadeIn(pulse), run_time=0.15)
        self.play(FadeOut(pulse), run_time=0.2)

        self.play(FadeIn(example_outputs[0], shift=UP * 0.1), run_time=0.4)
        # [19:10] You give it input, it gives output
        self.wait(1.5)

        # Swap to second example: image → text
        self.play(
            FadeOut(example_inputs[0]),
            FadeOut(example_outputs[0]),
            run_time=0.3,
        )
        self.play(FadeIn(example_inputs[1], shift=UP * 0.1), run_time=0.4)

        pulse2 = machine_box.copy().set_stroke(ACCENT, width=4, opacity=0.6)
        self.play(FadeIn(pulse2), run_time=0.15)
        self.play(FadeOut(pulse2), run_time=0.2)

        self.play(FadeIn(example_outputs[1], shift=UP * 0.1), run_time=0.4)
        # [19:15] Different modalities, same pattern
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 2 — "Internal representation → next thing"
        #  Show: diverse inputs converging through a neural net into
        #  a common representation, then "next token" emerging
        # ==============================================================

        # Multiple input types flowing into a neural network
        # Left side: different modality icons
        sentence_icon = make_svg_icon("chat_bubble.svg", color=ACCENT, height=0.8)
        sentence_icon.move_to(LEFT * 5.0 + UP * 1.5)

        image_rect = VGroup(
            RoundedRectangle(
                width=0.8,
                height=0.6,
                corner_radius=0.06,
                color=TEAL,
                stroke_width=1.5,
                fill_color=TEAL,
                fill_opacity=0.12,
            ),
        )
        # Grid overlay for image
        for r in range(2):
            for c in range(3):
                sq = Square(
                    side_length=0.15,
                    color=TEAL,
                    stroke_width=0.5,
                    fill_opacity=0.1,
                )
                sq.move_to(
                    image_rect[0].get_center()
                    + RIGHT * (c - 1) * 0.2
                    + UP * (0.5 - r) * 0.2
                )
                image_rect.add(sq)
        image_rect.move_to(LEFT * 5.0)

        # Sound wave
        wave = VMobject(color=PURPLE, stroke_width=2)
        wave_pts = []
        for i in range(40):
            x = -0.8 + i * 0.04
            y = 0.15 * np.sin(i * 0.8) * np.exp(-0.03 * abs(i - 20))
            wave_pts.append(np.array([x, y, 0]))
        wave.set_points_smoothly(wave_pts)
        wave.move_to(LEFT * 5.0 + DOWN * 1.5)

        input_icons = VGroup(sentence_icon, image_rect, wave)

        # Central neural net
        nn = make_neural_network_small(
            center=np.array([0, 0, 0]),
            width=3.0,
            height=2.5,
            color=ACCENT,
        )

        # Internal representation box
        repr_box = RoundedRectangle(
            width=1.4,
            height=0.6,
            corner_radius=0.1,
            color=PURPLE,
            stroke_width=1.8,
            fill_color=PURPLE,
            fill_opacity=0.08,
        )
        repr_box.move_to(RIGHT * 3.5)
        repr_dots = VGroup()
        for i in range(5):
            d = Dot(
                radius=0.04,
                color=PURPLE,
                fill_opacity=0.4 + 0.12 * i,
            )
            d.move_to(repr_box.get_left() + RIGHT * (0.2 + i * 0.22))
            repr_dots.add(d)

        # "→ next" arrow and token
        next_arrow = Arrow(
            repr_box.get_right(),
            repr_box.get_right() + RIGHT * 1.0,
            buff=0.1,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        next_token = make_token_box("next", color=GOLD, font_size=14)
        next_token.next_to(next_arrow, RIGHT, buff=0.12)

        # Arrows from input icons to NN
        input_arrows = VGroup()
        for icon in input_icons:
            arr = Arrow(
                icon.get_right(),
                nn.get_left() + LEFT * 0.1,
                buff=0.15,
                color=DIM2,
                stroke_width=1.0,
                max_tip_length_to_length_ratio=0.12,
            )
            input_arrows.add(arr)

        nn_to_repr = Arrow(
            nn.get_right() + RIGHT * 0.1,
            repr_box.get_left(),
            buff=0.1,
            color=ACCENT,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # Animate
        self.play(
            LaggedStart(
                *[FadeIn(icon, shift=RIGHT * 0.15) for icon in input_icons],
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in input_arrows], lag_ratio=0.1),
            run_time=0.5,
        )
        self.play(FadeIn(nn, scale=0.9), run_time=0.6)
        self.wait(0.3)

        # Pulse through the network
        nn_glow = nn.copy()
        nn_glow.set_color(ACCENT)
        nn_glow.set_stroke(ACCENT, width=2, opacity=0.5)
        self.play(FadeIn(nn_glow), run_time=0.2)
        self.play(FadeOut(nn_glow), run_time=0.3)

        self.play(GrowArrow(nn_to_repr), run_time=0.4)
        self.play(
            FadeIn(repr_box, scale=0.9),
            LaggedStart(*[FadeIn(d, scale=0.5) for d in repr_dots], lag_ratio=0.06),
            run_time=0.5,
        )
        self.wait(0.3)
        self.play(
            GrowArrow(next_arrow),
            FadeIn(next_token, shift=RIGHT * 0.1),
            run_time=0.5,
        )
        # [19:20] Model learns to predict "next token"
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 3 — "For a language model: next token.
        #             For multimodal: next word about image, next frame..."
        #  Show a carousel of "next X" predictions
        # ==============================================================

        # Central robot
        robot_center = make_svg_icon("robot.svg", color=WHITE, height=2.0)
        robot_center.move_to(LEFT * 1.5)

        self.play(FadeIn(robot_center, scale=0.9), run_time=0.5)

        # Show different "next" outputs cycling on the right side
        output_configs = [
            ("next token", ACCENT, '"The"'),
            ("next word about image", TEAL, '"fluffy"'),
            ("next sound description", PURPLE, '"bark"'),
            ("next video frame", ORANGE, "▶ frame 42"),
        ]

        output_label_pos = RIGHT * 2.5 + UP * 1.0
        output_value_pos = RIGHT * 2.5 + DOWN * 0.3

        prev_label = None
        prev_value = None
        prev_arrow = None

        for i, (label_text, color, value_text) in enumerate(output_configs):
            label = Text(label_text, font_size=15, color=color)
            label.move_to(output_label_pos)

            value = make_pill(value_text, color=color, font_size=18)
            value.move_to(output_value_pos)

            arrow = Arrow(
                robot_center.get_right(),
                value.get_left(),
                buff=0.2,
                color=color,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.12,
            )

            if prev_label is None:
                self.play(
                    Write(label),
                    GrowArrow(arrow),
                    FadeIn(value, scale=0.9),
                    run_time=0.6,
                )
            else:
                self.play(
                    FadeOut(prev_label),
                    FadeOut(prev_value),
                    FadeOut(prev_arrow),
                    run_time=0.25,
                )
                self.play(
                    Write(label),
                    GrowArrow(arrow),
                    FadeIn(value, scale=0.9),
                    run_time=0.5,
                )

            self.wait(0.5)
            prev_label = label
            prev_value = value
            prev_arrow = arrow

        self.wait(0.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 4 — THE PIVOT: "But now imagine the next output
        #  is not a word. Imagine the next output is an ACTION."
        #  Big visual shift — from text tokens to action tokens
        # ==============================================================

        # Show "word" token morphing into "action" token
        word_token = make_pill('"word"', color=ACCENT, font_size=24)
        word_token.move_to(ORIGIN)

        self.play(FadeIn(word_token, scale=0.8), run_time=0.5)
        # [19:32] But what if the model predicted actions instead of words?
        self.wait(1.5)

        # Question mark appears
        question = Text("?", font_size=60, color=DIM)
        question.move_to(ORIGIN)

        self.play(
            word_token.animate.set_opacity(0.3),
            FadeIn(question, scale=1.5),
            run_time=0.5,
        )
        self.wait(0.3)
        self.play(FadeOut(question), FadeOut(word_token), run_time=0.3)

        # Lightning bolt transition
        lightning = make_svg_icon("lightning.svg", color=GOLD, height=2.0)
        lightning.move_to(ORIGIN)
        self.play(
            FadeIn(lightning, scale=0.5),
            Flash(ORIGIN, color=GOLD, flash_radius=1.5, num_lines=12),
            run_time=0.4,
        )
        self.wait(0.2)
        self.play(FadeOut(lightning), run_time=0.3)

        # "action" token emerges with emphasis
        action_token = make_pill("action", color=GREEN, font_size=28, fill_opacity=0.2)
        action_token.move_to(ORIGIN)

        # Action icons orbit around it
        gear_icon = make_svg_icon("gear.svg", color=GREEN, height=0.6)
        hand_icon = make_svg_icon("hand_pointer.svg", color=GREEN, height=0.6)
        eye_icon = make_svg_icon("eye.svg", color=GREEN, height=0.5)

        action_satellites = VGroup(gear_icon, hand_icon, eye_icon)
        angles = [PI / 3, PI, 5 * PI / 3]
        radius = 1.5
        for sat, angle in zip(action_satellites, angles):
            sat.move_to(ORIGIN + radius * np.array([np.cos(angle), np.sin(angle), 0]))

        self.play(
            FadeIn(action_token, scale=1.4),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(sat, scale=0.5) for sat in action_satellites],
                lag_ratio=0.12,
            ),
            run_time=0.6,
        )

        # Subtle orbit animation
        orbit_anims = []
        for sat, start_angle in zip(action_satellites, angles):
            target_angle = start_angle + PI / 6
            target_pos = ORIGIN + radius * np.array(
                [np.cos(target_angle), np.sin(target_angle), 0]
            )
            orbit_anims.append(sat.animate.move_to(target_pos))

        self.play(*orbit_anims, run_time=0.8, rate_func=smooth)
        # [19:38] The pivot from "word" to "action"
        self.wait(1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 5 — CHATBOT vs AGENT: the central question
        #  "What should I SAY next?" vs "What should I DO next?"
        # ==============================================================

        # Split screen: left = chatbot, right = agent
        divider = DashedLine(
            UP * 3.5,
            DOWN * 3.5,
            color=DIM2,
            stroke_width=1,
            dash_length=0.1,
        )

        # ─── LEFT SIDE: CHATBOT ───
        chatbot_title = Text("chatbot", font_size=22, color=ACCENT)
        chatbot_title.move_to(LEFT * 3.5 + UP * 2.8)

        chat_bubble = make_svg_icon("chat_bubble.svg", color=ACCENT, height=1.8)
        chat_bubble.move_to(LEFT * 3.5 + UP * 0.5)

        # Speech bubbles below — back-and-forth conversation
        user_msg = VGroup()
        user_bubble = RoundedRectangle(
            width=2.0,
            height=0.5,
            corner_radius=0.12,
            color=DIM2,
            stroke_width=1.2,
            fill_color=DIM2,
            fill_opacity=0.1,
        )
        user_text = Text("Hello!", font_size=12, color=DIM)
        user_text.move_to(user_bubble)
        user_msg.add(user_bubble, user_text)
        user_msg.move_to(LEFT * 3.5 + DOWN * 1.0)

        bot_msg = VGroup()
        bot_bubble = RoundedRectangle(
            width=2.4,
            height=0.5,
            corner_radius=0.12,
            color=ACCENT,
            stroke_width=1.2,
            fill_color=ACCENT,
            fill_opacity=0.08,
        )
        bot_text = Text("Hi! How can I help?", font_size=12, color=ACCENT)
        bot_text.move_to(bot_bubble)
        bot_msg.add(bot_bubble, bot_text)
        bot_msg.move_to(LEFT * 3.5 + DOWN * 1.8)

        # The key question
        chatbot_question = Text(
            '"What should I\nsay next?"',
            font_size=16,
            color=ACCENT,
        )
        chatbot_question.move_to(LEFT * 3.5 + DOWN * 2.8)

        # ─── RIGHT SIDE: AGENT ───
        agent_title = Text("agent", font_size=22, color=GREEN)
        agent_title.move_to(RIGHT * 3.5 + UP * 2.8)

        # Robot with gear — represents an agent
        robot_agent = make_svg_icon("robot.svg", color=WHITE, height=1.4)
        robot_agent.move_to(RIGHT * 3.5 + UP * 0.8)

        gear_small = make_svg_icon("gear.svg", color=GREEN, height=0.5)
        gear_small.move_to(robot_agent.get_corner(UR) + RIGHT * 0.1 + UP * 0.1)

        # Action icons below the robot
        action_icons = VGroup()
        action_items = [
            ("📧", "send email"),
            ("🔍", "search web"),
            ("📝", "write code"),
        ]
        for i, (emoji, desc) in enumerate(action_items):
            icon_group = VGroup()
            bg = RoundedRectangle(
                width=1.8,
                height=0.4,
                corner_radius=0.08,
                color=GREEN,
                stroke_width=1,
                fill_color=GREEN,
                fill_opacity=0.06,
            )
            txt = Text(desc, font_size=11, color=GREEN)
            txt.move_to(bg)
            icon_group.add(bg, txt)
            action_icons.add(icon_group)

        action_icons.arrange(DOWN, buff=0.12)
        action_icons.move_to(RIGHT * 3.5 + DOWN * 1.3)

        # The key question
        agent_question = Text(
            '"What should I\ndo next?"',
            font_size=16,
            color=GREEN,
        )
        agent_question.move_to(RIGHT * 3.5 + DOWN * 2.8)

        # Animate: build left side first, then right
        self.play(Create(divider), run_time=0.4)

        # Left side
        self.play(
            Write(chatbot_title),
            FadeIn(chat_bubble, shift=DOWN * 0.15),
            run_time=0.6,
        )
        self.play(
            FadeIn(user_msg, shift=RIGHT * 0.1),
            run_time=0.3,
        )
        self.play(
            FadeIn(bot_msg, shift=LEFT * 0.1),
            run_time=0.3,
        )
        self.play(Write(chatbot_question), run_time=0.5)
        self.wait(0.3)

        # Right side
        self.play(
            Write(agent_title),
            FadeIn(robot_agent, shift=DOWN * 0.15),
            FadeIn(gear_small, scale=0.5),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=LEFT * 0.1) for item in action_icons],
                lag_ratio=0.1,
            ),
            run_time=0.5,
        )
        self.play(Write(agent_question), run_time=0.5)
        # [19:42] Chatbot asks "what should I say?" — Agent asks "what should I do?"
        self.wait(2.0)

        # Emphasize the agent side — it glows
        agent_highlight = SurroundingRectangle(
            VGroup(agent_title, robot_agent, gear_small, action_icons, agent_question),
            color=GREEN,
            buff=0.3,
            corner_radius=0.15,
            stroke_width=2,
            fill_color=GREEN,
            fill_opacity=0.03,
        )
        self.play(Create(agent_highlight), run_time=0.5)

        # Pulse
        pulse_rect = agent_highlight.copy().set_stroke(GREEN, width=3)
        self.play(
            pulse_rect.animate.scale(1.05).set_opacity(0),
            run_time=0.6,
        )
        self.remove(pulse_rect)
        self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 6 — THE BRIDGE ANIMATION
        #  Visually morph chatbot → agent → LAM
        #  Show "say" tokens becoming "do" tokens on a conveyor belt
        # ==============================================================

        # Conveyor belt metaphor
        belt_start = LEFT * 5.5 + DOWN * 0.5
        belt_end = RIGHT * 5.5 + DOWN * 0.5
        belt = make_conveyor_belt(belt_start, belt_end, n_segments=20)

        self.play(FadeIn(belt), run_time=0.5)

        # "Say" tokens on the left → transform into "Do" tokens on the right
        say_tokens = VGroup()
        say_words = ["reply", "answer", "explain", "describe"]
        say_positions = [LEFT * 4.0, LEFT * 2.5, LEFT * 1.0, RIGHT * 0.5]
        for word, pos in zip(say_words, say_positions):
            tok = make_token_box(word, color=ACCENT, font_size=12)
            tok.move_to(pos + DOWN * 0.5)
            say_tokens.add(tok)

        self.play(
            LaggedStart(
                *[FadeIn(tok, shift=RIGHT * 0.15) for tok in say_tokens],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.wait(0.4)

        # Transform zone — lightning in the middle
        transform_zone = VGroup()
        tz_rect = RoundedRectangle(
            width=1.0,
            height=1.5,
            corner_radius=0.12,
            color=GOLD,
            stroke_width=2,
            fill_color=GOLD,
            fill_opacity=0.05,
        )
        tz_rect.move_to(RIGHT * 2.5 + DOWN * 0.5)
        tz_lightning = make_svg_icon("lightning.svg", color=GOLD, height=0.7)
        tz_lightning.move_to(tz_rect.get_center())
        transform_zone.add(tz_rect, tz_lightning)

        self.play(FadeIn(transform_zone, scale=0.8), run_time=0.4)

        # Animate tokens sliding right and transforming
        do_words = ["click", "search", "execute", "deploy"]
        do_tokens = VGroup()
        do_positions = [RIGHT * 3.8, RIGHT * 4.5, RIGHT * 5.2, RIGHT * 5.9]

        for i, (say_tok, do_word, do_pos) in enumerate(
            zip(say_tokens, do_words, do_positions)
        ):
            do_tok = make_token_box(do_word, color=GREEN, font_size=12)
            do_tok.move_to(do_pos + DOWN * 0.5)
            do_tokens.add(do_tok)

        # Slide all say tokens toward the transform zone and swap
        self.play(
            *[tok.animate.move_to(tz_rect.get_center()) for tok in say_tokens],
            run_time=0.6,
        )
        self.play(
            Flash(tz_rect.get_center(), color=GOLD, flash_radius=0.8, num_lines=8),
            FadeOut(say_tokens),
            run_time=0.3,
        )
        self.play(
            LaggedStart(
                *[FadeIn(tok, shift=RIGHT * 0.2) for tok in do_tokens],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        # [19:49] The bridge: "say" tokens transform into "do" tokens
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 7 — LARGE ACTION MODELS (LAMs)
        #  The final concept: show the evolution
        #  LLM → Agent → LAM, with the LAM being the culmination
        # ==============================================================

        # Three stages arranged horizontally
        # Stage 1: LLM (chatbot)
        llm_box = RoundedRectangle(
            width=2.0,
            height=1.3,
            corner_radius=0.12,
            color=ACCENT,
            stroke_width=1.8,
            fill_color=ACCENT,
            fill_opacity=0.06,
        )
        llm_box.move_to(LEFT * 4.0)
        llm_label = Text("LLM", font_size=18, color=ACCENT)
        llm_label.move_to(llm_box.get_center() + UP * 0.2)
        llm_desc = Text("says", font_size=13, color=DIM)
        llm_desc.move_to(llm_box.get_center() + DOWN * 0.25)
        chat_icon_small = make_svg_icon("chat_bubble.svg", color=ACCENT, height=0.5)
        chat_icon_small.next_to(llm_box, UP, buff=0.15)

        # Stage 2: Agent
        agent_box = RoundedRectangle(
            width=2.0,
            height=1.3,
            corner_radius=0.12,
            color=PURPLE,
            stroke_width=1.8,
            fill_color=PURPLE,
            fill_opacity=0.06,
        )
        agent_box.move_to(ORIGIN)
        agent_label = Text("Agent", font_size=18, color=PURPLE)
        agent_label.move_to(agent_box.get_center() + UP * 0.2)
        agent_desc = Text("plans", font_size=13, color=DIM)
        agent_desc.move_to(agent_box.get_center() + DOWN * 0.25)
        robot_small = make_svg_icon("robot.svg", color=PURPLE, height=0.5)
        robot_small.next_to(agent_box, UP, buff=0.15)

        # Stage 3: LAM
        lam_box = RoundedRectangle(
            width=2.4,
            height=1.5,
            corner_radius=0.12,
            color=GREEN,
            stroke_width=2.5,
            fill_color=GREEN,
            fill_opacity=0.08,
        )
        lam_box.move_to(RIGHT * 4.0)
        lam_label = Text("LAM", font_size=22, color=GREEN, weight=BOLD)
        lam_label.move_to(lam_box.get_center() + UP * 0.2)
        lam_desc = Text("acts", font_size=14, color=GREEN)
        lam_desc.move_to(lam_box.get_center() + DOWN * 0.3)
        gear_icon2 = make_svg_icon("gear.svg", color=GREEN, height=0.6)
        gear_icon2.next_to(lam_box, UP, buff=0.15)

        # Arrows between stages
        arr_1 = Arrow(
            llm_box.get_right(),
            agent_box.get_left(),
            buff=0.15,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )
        arr_2 = Arrow(
            agent_box.get_right(),
            lam_box.get_left(),
            buff=0.15,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # Animate evolution: stage by stage
        self.play(
            FadeIn(llm_box, scale=0.9),
            FadeIn(llm_label),
            FadeIn(llm_desc),
            FadeIn(chat_icon_small, shift=DOWN * 0.1),
            run_time=0.6,
        )
        self.wait(0.3)

        self.play(GrowArrow(arr_1), run_time=0.4)
        self.play(
            FadeIn(agent_box, scale=0.9),
            FadeIn(agent_label),
            FadeIn(agent_desc),
            FadeIn(robot_small, shift=DOWN * 0.1),
            run_time=0.6,
        )
        self.wait(0.3)

        self.play(GrowArrow(arr_2), run_time=0.4)
        self.play(
            FadeIn(lam_box, scale=0.9),
            FadeIn(lam_label),
            FadeIn(lam_desc),
            FadeIn(gear_icon2, shift=DOWN * 0.1),
            run_time=0.6,
        )
        self.wait(0.3)

        # LAM emphasis — glow + pulse
        lam_glow = SurroundingRectangle(
            VGroup(lam_box, gear_icon2),
            color=GREEN,
            buff=0.15,
            corner_radius=0.18,
            stroke_width=2.5,
            fill_color=GREEN,
            fill_opacity=0.04,
        )
        self.play(Create(lam_glow), run_time=0.4)

        # Flash
        self.play(
            Flash(lam_box.get_center(), color=GREEN, flash_radius=1.0, num_lines=10),
            run_time=0.5,
        )
        # [19:55] LLM → Agent → LAM evolution
        self.wait(1.0)

        # ==============================================================
        #  PART 7b — LAM IN ACTION: show it doing things
        #  Actions radiating out from the LAM box
        # ==============================================================

        # Dim everything except LAM
        non_lam = VGroup(
            llm_box,
            llm_label,
            llm_desc,
            chat_icon_small,
            agent_box,
            agent_label,
            agent_desc,
            robot_small,
            arr_1,
            arr_2,
        )
        self.play(
            non_lam.animate.set_opacity(0.15),
            lam_box.animate.move_to(LEFT * 1.5).scale(1.3),
            lam_label.animate.move_to(LEFT * 1.5 + UP * 0.3),
            lam_desc.animate.move_to(LEFT * 1.5 + DOWN * 0.4),
            gear_icon2.animate.move_to(LEFT * 1.5 + UP * 1.5),
            FadeOut(lam_glow),
            run_time=0.8,
        )

        # Action outputs radiating from the LAM
        actions = [
            ("browse web", TEAL),
            ("write code", ACCENT),
            ("send message", GOLD),
            ("run command", ORANGE),
            ("book flight", PURPLE),
            ("analyze data", PINK),
        ]

        action_groups = VGroup()
        action_angles = [PI / 4, PI / 8, -PI / 8, -PI / 4, -3 * PI / 8, 3 * PI / 8]
        action_radius = 2.8

        for (act_text, act_color), angle in zip(actions, action_angles):
            pos = LEFT * 1.5 + action_radius * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            # Shift everything to the right so actions spread nicely
            pos = pos + RIGHT * 2.0

            act_pill = make_pill(act_text, color=act_color, font_size=12)
            act_pill.move_to(pos)

            act_line = Line(
                LEFT * 1.5,
                pos,
                color=act_color,
                stroke_width=0.8,
                stroke_opacity=0.4,
            )

            action_groups.add(VGroup(act_line, act_pill))

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(grp[0]),
                        FadeIn(grp[1], scale=0.7),
                    )
                    for grp in action_groups
                ],
                lag_ratio=0.1,
            ),
            run_time=1.2,
        )

        # Subtle pulsing glow on each action
        for grp in action_groups:
            pill = grp[1]
            glow = pill[0].copy().set_stroke(width=3, opacity=0.6)
            self.play(
                FadeIn(glow, run_time=0.1),
                FadeOut(glow, run_time=0.15),
            )

        self.wait(1.0)

        # ==============================================================
        #  PART 8 — FINAL: The small change that matters
        #  "say" → "do" — minimal, powerful
        # ==============================================================

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # Big question transformation
        say_text = Text('"What should I say next?"', font_size=28, color=ACCENT)
        say_text.move_to(ORIGIN)

        self.play(Write(say_text), run_time=0.8)
        self.wait(0.6)

        # Highlight "say" and morph to "do"
        # We'll animate the whole text fading out and new text appearing
        do_text = Text('"What should I do next?"', font_size=28, color=GREEN)
        do_text.move_to(ORIGIN)

        # Create a highlight around "say" then "do"
        # Find approximate position of "say" in the text
        self.play(
            ReplacementTransform(say_text, do_text),
            run_time=1.0,
            rate_func=smooth,
        )

        # Emphasize
        self.play(
            Flash(do_text.get_center(), color=GREEN, flash_radius=1.5, num_lines=12),
            run_time=0.5,
        )
        self.wait(0.5)

        # Subtle underline
        underline = Line(
            do_text.get_left() + DOWN * 0.3,
            do_text.get_right() + DOWN * 0.3,
            color=GREEN,
            stroke_width=2,
        )
        self.play(Create(underline), run_time=0.4)
        # [20:06] "What should I say next?" → "What should I do next?"
        self.wait(2.0)

        # Final fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
