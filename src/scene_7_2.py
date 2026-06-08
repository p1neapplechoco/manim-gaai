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


# ── helpers ─────────────────────────────────────────────────────────


def make_patch_grid(image_mob, rows=3, cols=3):
    """Create a grid overlay on an image, returning (grid_lines, patch_rects)."""
    w = image_mob.width
    h = image_mob.height
    corner = image_mob.get_corner(UL)

    grid_lines = VGroup()
    # Horizontal lines
    for r in range(1, rows):
        y = corner[1] - r * h / rows
        grid_lines.add(
            Line(
                [corner[0], y, 0],
                [corner[0] + w, y, 0],
                color=ACCENT,
                stroke_width=1.5,
                stroke_opacity=0.8,
            )
        )
    # Vertical lines
    for c in range(1, cols):
        x = corner[0] + c * w / cols
        grid_lines.add(
            Line(
                [x, corner[1], 0],
                [x, corner[1] - h, 0],
                color=ACCENT,
                stroke_width=1.5,
                stroke_opacity=0.8,
            )
        )

    patch_rects = VGroup()
    for r in range(rows):
        for c in range(cols):
            rect = Rectangle(
                width=w / cols,
                height=h / rows,
                color=ACCENT,
                stroke_width=1.2,
                stroke_opacity=0.6,
                fill_color=ACCENT,
                fill_opacity=0.05,
            )
            rect.move_to(
                corner + RIGHT * (c + 0.5) * w / cols + DOWN * (r + 0.5) * h / rows
            )
            patch_rects.add(rect)

    return grid_lines, patch_rects


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


def make_thought_bubble(text_str, color=DIM, font_size=13):
    """A small thought text with a subtle background."""
    t = Text(text_str, font_size=font_size, color=color)
    return t


def make_environment_box():
    """Create a simple game-like environment visual."""
    # Ground
    ground = Rectangle(
        width=3.6,
        height=0.3,
        color="#4A6A3A",
        stroke_width=1,
        fill_color="#3A5A2A",
        fill_opacity=1,
    )
    ground.move_to(DOWN * 0.9)

    # Sky
    sky = Rectangle(
        width=3.6,
        height=2.1,
        color="#1A2A4A",
        stroke_width=1,
        fill_color="#0A1A3A",
        fill_opacity=1,
    )
    sky.next_to(ground, UP, buff=0)

    # Simple agent (stick figure)
    agent_body = Line(ORIGIN, DOWN * 0.4, color=WHITE, stroke_width=2)
    agent_head = Circle(radius=0.1, color=WHITE, stroke_width=1.5, fill_opacity=0)
    agent_head.next_to(agent_body, UP, buff=0.02)
    agent_left_arm = Line(ORIGIN, DL * 0.2 + LEFT * 0.05, color=WHITE, stroke_width=1.5)
    agent_right_arm = Line(
        ORIGIN, DR * 0.2 + RIGHT * 0.05, color=WHITE, stroke_width=1.5
    )
    agent_left_arm.move_to(agent_body.get_top() + DOWN * 0.12, aligned_edge=UP + RIGHT)
    agent_right_arm.move_to(agent_body.get_top() + DOWN * 0.12, aligned_edge=UP + LEFT)
    agent_legs_l = Line(
        agent_body.get_bottom(),
        agent_body.get_bottom() + DL * 0.2,
        color=WHITE,
        stroke_width=1.5,
    )
    agent_legs_r = Line(
        agent_body.get_bottom(),
        agent_body.get_bottom() + DR * 0.2,
        color=WHITE,
        stroke_width=1.5,
    )
    agent = VGroup(
        agent_head,
        agent_body,
        agent_left_arm,
        agent_right_arm,
        agent_legs_l,
        agent_legs_r,
    )
    agent.move_to(LEFT * 0.8 + UP * 0.05)

    # Simple obstacles
    obs1 = Rectangle(
        width=0.4,
        height=0.5,
        color="#8A5A3A",
        stroke_width=1,
        fill_color="#6A4A2A",
        fill_opacity=1,
    )
    obs1.next_to(ground, UP, buff=0).shift(RIGHT * 0.8)
    obs2 = Rectangle(
        width=0.3,
        height=0.8,
        color="#8A5A3A",
        stroke_width=1,
        fill_color="#6A4A2A",
        fill_opacity=1,
    )
    obs2.next_to(ground, UP, buff=0).shift(RIGHT * 1.5)

    # Goal star
    goal = Star(
        n=5,
        outer_radius=0.15,
        inner_radius=0.06,
        color=GOLD,
        fill_opacity=0.8,
        stroke_width=1,
    )
    goal.move_to(RIGHT * 1.2 + UP * 0.6)

    env = VGroup(sky, ground, agent, obs1, obs2, goal)

    border = RoundedRectangle(
        width=3.7,
        height=2.5,
        corner_radius=0.1,
        color=DIM2,
        stroke_width=1.5,
    )
    border.move_to(env.get_center())

    return VGroup(env, border)


class MultimodalModels(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ==============================================================
        #  PART 1 — DOG IMAGE + HUMAN BRAIN PROCESSING
        # ==============================================================

        # Show the dog image
        dog_img = ImageMobject(str(BASE_DIR / "assets" / "images" / "dancing_dog.jpg"))
        dog_img.scale_to_fit_height(3.0)
        dog_img.move_to(LEFT * 2.5)

        # Rounded border for the image
        img_border = RoundedRectangle(
            width=dog_img.width + 0.1,
            height=dog_img.height + 0.1,
            corner_radius=0.12,
            color=DIM2,
            stroke_width=1.5,
        )
        img_border.move_to(dog_img)

        self.play(FadeIn(dog_img, scale=0.9), Create(img_border), run_time=0.8)
        # [18:00] Dog image + brain processing
        self.wait(1.0)

        # Brain SVG on the right
        brain = SVGMobject(str(BASE_DIR / "assets" / "svgs" / "brain.svg"))
        brain.set_color(WHITE)
        brain.set_stroke(WHITE, width=1.2)
        brain.scale_to_fit_height(1.8)
        brain.move_to(RIGHT * 2.5 + UP * 0.5)

        self.play(FadeIn(brain, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.3)

        # Arrow from dog image to brain: "sees"
        see_arrow = Arrow(
            dog_img.get_right() + RIGHT * 0.1,
            brain.get_left() + LEFT * 0.1,
            buff=0.15,
            color=DIM,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(GrowArrow(see_arrow), run_time=0.4)
        self.wait(0.3)

        # Brain "thinking" — associated concepts bubble out
        concepts = ["dog", "animal", "fur", "barking", "pet"]
        concept_colors = [GOLD, ACCENT, ORANGE, TEAL, GREEN]

        concept_mobs = VGroup()
        angles = [PI / 3, PI / 5, -PI / 6, -PI / 3, 0]
        radii = [1.4, 1.5, 1.3, 1.5, 1.6]

        for i, (word, color, angle, r) in enumerate(
            zip(concepts, concept_colors, angles, radii)
        ):
            t = Text(word, font_size=16, color=color)
            t.move_to(
                brain.get_center() + r * np.array([np.cos(angle), np.sin(angle), 0])
            )
            concept_mobs.add(t)

        # Thought connector lines
        thought_lines = VGroup()
        for cm in concept_mobs:
            line = DashedLine(
                brain.get_center(),
                cm.get_center(),
                color=DIM2,
                stroke_width=0.8,
                dash_length=0.08,
            )
            thought_lines.add(line)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(Create(line), FadeIn(cm, scale=0.7))
                    for line, cm in zip(thought_lines, concept_mobs)
                ],
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        # [18:06] Brain associates concepts: dog, animal, fur
        self.wait(2.0)

        # Clean transition
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 2 — IMAGE → PATCHES → VISUAL TOKENS → ROBOT → TEXT
        # ==============================================================

        # Show the dog image again, smaller, on the left
        dog_img2 = ImageMobject(str(BASE_DIR / "assets" / "images" / "dancing_dog.jpg"))
        dog_img2.scale_to_fit_height(2.4)
        dog_img2.move_to(LEFT * 4.2 + UP * 0.5)

        img_border2 = RoundedRectangle(
            width=dog_img2.width + 0.08,
            height=dog_img2.height + 0.08,
            corner_radius=0.08,
            color=DIM2,
            stroke_width=1.2,
        )
        img_border2.move_to(dog_img2)

        self.play(FadeIn(dog_img2, scale=0.95), Create(img_border2), run_time=0.5)
        self.wait(0.3)

        # Overlay grid — image breaks into patches
        grid_lines, patch_rects = make_patch_grid(dog_img2, rows=3, cols=3)

        self.play(
            LaggedStart(*[Create(line) for line in grid_lines], lag_ratio=0.06),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(pr, scale=0.9) for pr in patch_rects], lag_ratio=0.04),
            run_time=0.5,
        )
        self.wait(0.3)

        # Create patch token labels below
        patch_labels = VGroup()
        for i in range(9):
            token = make_token_box(f"P{i+1}", color=ACCENT, font_size=11, width=0.45)
            patch_labels.add(token)
        patch_labels.arrange(RIGHT, buff=0.08)
        patch_labels.scale(0.85)
        patch_labels.next_to(dog_img2, DOWN, buff=0.4)

        # Animate patches "collapsing" into token labels
        self.play(
            LaggedStart(
                *[
                    TransformFromCopy(pr, pl)
                    for pr, pl in zip(patch_rects, patch_labels)
                ],
                lag_ratio=0.04,
            ),
            run_time=0.8,
        )
        self.wait(0.3)

        # Robot on the right
        robot = SVGMobject(str(BASE_DIR / "assets" / "svgs" / "robot.svg"))
        robot.set_color(WHITE)
        robot.set_stroke(WHITE, width=1.0)
        robot.scale_to_fit_height(2.2)
        robot.move_to(RIGHT * 0.5 + UP * 0.5)

        self.play(FadeIn(robot, shift=UP * 0.15), run_time=0.5)
        self.wait(0.2)

        # Animate visual tokens flowing into robot
        flow_arrow = Arrow(
            patch_labels.get_right(),
            robot.get_left(),
            buff=0.15,
            color=ACCENT,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.12,
        )
        self.play(GrowArrow(flow_arrow), run_time=0.4)

        # Pulse dots flowing along the arrow
        for _ in range(3):
            pulse = Dot(radius=0.05, color=ACCENT, fill_opacity=0.8)
            pulse.move_to(flow_arrow.get_start())
            self.play(
                MoveAlongPath(pulse, flow_arrow),
                run_time=0.3,
                rate_func=linear,
            )
            self.remove(pulse)

        self.wait(0.2)

        # Text concepts emerge on the right side of the robot
        output_concepts = ["dog", "animal", "fur", "barking", "pet"]
        output_colors = [GOLD, ACCENT, ORANGE, TEAL, GREEN]

        concept_tokens = VGroup()
        for word, color in zip(output_concepts, output_colors):
            tok = make_token_box(word, color=color, font_size=13)
            concept_tokens.add(tok)
        concept_tokens.arrange(DOWN, buff=0.12)
        concept_tokens.move_to(RIGHT * 4.0 + UP * 0.5)

        out_arrow = Arrow(
            robot.get_right(),
            concept_tokens.get_left(),
            buff=0.15,
            color=GOLD,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(GrowArrow(out_arrow), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(ct, shift=RIGHT * 0.15) for ct in concept_tokens],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )
        # [18:15] Visual tokens flow through model to text concepts
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 3 — TEXT PROMPT + MODEL OUTPUT
        # ==============================================================

        # Robot at center
        robot2 = SVGMobject(str(BASE_DIR / "assets" / "svgs" / "robot.svg"))
        robot2.set_color(WHITE)
        robot2.set_stroke(WHITE, width=1.0)
        robot2.scale_to_fit_height(2.0)
        robot2.move_to(ORIGIN)

        self.play(FadeIn(robot2, scale=0.9), run_time=0.5)

        # Dog image thumbnail (small, top-left)
        dog_thumb = ImageMobject(
            str(BASE_DIR / "assets" / "images" / "dancing_dog.jpg")
        )
        dog_thumb.scale_to_fit_height(1.2)
        dog_thumb.move_to(LEFT * 4.0 + UP * 1.5)

        thumb_border = RoundedRectangle(
            width=dog_thumb.width + 0.06,
            height=dog_thumb.height + 0.06,
            corner_radius=0.06,
            color=DIM2,
            stroke_width=1,
        )
        thumb_border.move_to(dog_thumb)

        self.play(FadeIn(dog_thumb), Create(thumb_border), run_time=0.4)

        # Text prompt below the thumbnail
        prompt_text = Text('"What animal is this?"', font_size=18, color=ACCENT)
        prompt_text.next_to(dog_thumb, DOWN, buff=0.3)

        self.play(Write(prompt_text), run_time=0.6)
        self.wait(0.3)

        # Arrow from prompt to robot
        prompt_arrow = Arrow(
            prompt_text.get_right(),
            robot2.get_left(),
            buff=0.2,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.15,
        )
        # Also arrow from image to robot
        img_arrow = Arrow(
            dog_thumb.get_right(),
            robot2.get_left() + UP * 0.3,
            buff=0.2,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(GrowArrow(prompt_arrow), GrowArrow(img_arrow), run_time=0.5)
        self.wait(0.3)

        # Robot "processes" — glow
        robot_glow = robot2.copy().set_stroke(ACCENT, width=3, opacity=0.5)
        self.play(FadeIn(robot_glow), run_time=0.3)
        self.play(FadeOut(robot_glow), run_time=0.3)

        # Output: "Dog"
        output_text = Text('"Dog"', font_size=32, color=GOLD, weight=BOLD)
        output_text.move_to(RIGHT * 4.0)

        output_arrow = Arrow(
            robot2.get_right(),
            output_text.get_left(),
            buff=0.2,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(GrowArrow(output_arrow), run_time=0.4)
        self.play(
            FadeIn(output_text, scale=1.3),
            Flash(output_text.get_center(), color=GOLD, flash_radius=0.6, num_lines=8),
            run_time=0.6,
        )
        # [18:22] Model outputs "Dog" — combining vision and language
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 4 — KEY INSIGHT: different data, same representations
        # ==============================================================

        # Three modality icons with arrows converging to a single "representation"

        # Image modality
        img_icon = Rectangle(
            width=1.0,
            height=0.8,
            color=ACCENT,
            stroke_width=1.5,
            fill_color=ACCENT,
            fill_opacity=0.1,
        )
        img_icon_label = Text("image", font_size=14, color=ACCENT)
        img_grid = VGroup()
        for r in range(2):
            for c in range(3):
                sq = Square(
                    side_length=0.18, color=ACCENT, stroke_width=0.6, fill_opacity=0.15
                )
                sq.move_to(
                    img_icon.get_center()
                    + RIGHT * (c - 1) * 0.22
                    + UP * (0.5 - r) * 0.22
                )
                img_grid.add(sq)
        img_mod = VGroup(img_icon, img_grid, img_icon_label)
        img_icon_label.next_to(img_icon, DOWN, buff=0.12)

        # Text modality
        text_icon = Rectangle(
            width=1.0,
            height=0.8,
            color=GOLD,
            stroke_width=1.5,
            fill_color=GOLD,
            fill_opacity=0.1,
        )
        text_lines = VGroup()
        for i in range(3):
            w = [0.6, 0.45, 0.55][i]
            line = Line(LEFT * w / 2, RIGHT * w / 2, color=GOLD, stroke_width=1.2)
            line.move_to(text_icon.get_center() + UP * (0.2 - i * 0.2))
            text_lines.add(line)
        text_icon_label = Text("text", font_size=14, color=GOLD)
        text_icon_label.next_to(text_icon, DOWN, buff=0.12)
        text_mod = VGroup(text_icon, text_lines, text_icon_label)

        # Action modality
        action_icon = Rectangle(
            width=1.0,
            height=0.8,
            color=GREEN,
            stroke_width=1.5,
            fill_color=GREEN,
            fill_opacity=0.1,
        )
        # Small arrow inside representing action
        act_arr = Arrow(
            action_icon.get_center() + LEFT * 0.25,
            action_icon.get_center() + RIGHT * 0.25,
            buff=0,
            color=GREEN,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.3,
        )
        action_icon_label = Text("action", font_size=14, color=GREEN)
        action_icon_label.next_to(action_icon, DOWN, buff=0.12)
        action_mod = VGroup(action_icon, act_arr, action_icon_label)

        # Position them
        modalities = VGroup(img_mod, text_mod, action_mod)
        modalities.arrange(DOWN, buff=0.6)
        modalities.move_to(LEFT * 3.5)

        # Central representation
        repr_box = RoundedRectangle(
            width=2.0,
            height=1.0,
            corner_radius=0.15,
            color=PURPLE,
            stroke_width=2,
            fill_color=PURPLE,
            fill_opacity=0.08,
        )
        repr_box.move_to(ORIGIN)
        repr_label = Text("shared\nrepresentation", font_size=14, color=PURPLE)
        repr_label.move_to(repr_box)

        # Model box on the right
        model_box = RoundedRectangle(
            width=1.8,
            height=1.0,
            corner_radius=0.12,
            color=WHITE,
            stroke_width=1.5,
            fill_color=BG,
            fill_opacity=1,
        )
        model_box.move_to(RIGHT * 3.5)
        model_label = Text("same\nmodel", font_size=14, color=WHITE)
        model_label.move_to(model_box)

        # Arrows: modalities → representation → model
        mod_arrows = VGroup()
        for mod in modalities:
            arr = Arrow(
                mod.get_right(),
                repr_box.get_left(),
                buff=0.15,
                color=DIM,
                stroke_width=1.2,
                max_tip_length_to_length_ratio=0.15,
            )
            mod_arrows.add(arr)

        repr_to_model = Arrow(
            repr_box.get_right(),
            model_box.get_left(),
            buff=0.15,
            color=PURPLE,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # Animate
        self.play(
            LaggedStart(
                *[FadeIn(mod, shift=RIGHT * 0.15) for mod in modalities],
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in mod_arrows], lag_ratio=0.1),
            run_time=0.6,
        )
        self.play(
            FadeIn(repr_box, scale=0.9),
            FadeIn(repr_label),
            run_time=0.5,
        )
        self.play(GrowArrow(repr_to_model), run_time=0.4)
        self.play(
            FadeIn(model_box, scale=0.9),
            FadeIn(model_label),
            run_time=0.5,
        )

        # Glow on repr_box to emphasize
        repr_glow = SurroundingRectangle(
            repr_box,
            color=PURPLE,
            buff=0.1,
            corner_radius=0.18,
            stroke_width=2,
            fill_color=PURPLE,
            fill_opacity=0.06,
        )
        self.play(Create(repr_glow), run_time=0.4)
        # [18:30] Different data, same shared representation
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ==============================================================
        #  PART 5 — ACTION-BASED MODELS: environment → robot
        # ==============================================================

        # Show environment
        env_box = make_environment_box()
        env_box.scale(0.9)
        env_box.move_to(LEFT * 3.5)

        env_label = Text("environment", font_size=14, color=DIM)
        env_label.next_to(env_box, DOWN, buff=0.2)

        self.play(FadeIn(env_box, scale=0.95), FadeIn(env_label), run_time=0.6)
        self.wait(0.4)

        # Robot
        robot3 = SVGMobject(str(BASE_DIR / "assets" / "svgs" / "robot.svg"))
        robot3.set_color(WHITE)
        robot3.set_stroke(WHITE, width=1.0)
        robot3.scale_to_fit_height(2.0)
        robot3.move_to(RIGHT * 1.0)

        env_to_robot = Arrow(
            env_box.get_right(),
            robot3.get_left(),
            buff=0.2,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(FadeIn(robot3, shift=RIGHT * 0.15), run_time=0.5)
        self.play(GrowArrow(env_to_robot), run_time=0.4)
        self.wait(0.3)

        # ==============================================================
        #  PART 5b — ZOOM INSIDE ROBOT: decompose into modalities
        # ==============================================================

        # "Fake zoom" — scale up the robot and fade everything else
        other_mobs = VGroup(env_box, env_label, env_to_robot)

        self.play(
            other_mobs.animate.set_opacity(0.15),
            robot3.animate.scale(2.0).move_to(ORIGIN),
            run_time=0.8,
        )
        self.wait(0.2)

        # Inside the robot: show environment decomposing into modalities
        # Create small modality representations inside the "zoomed" robot

        # Visual modality
        vis_box = RoundedRectangle(
            width=1.2,
            height=0.6,
            corner_radius=0.08,
            color=ACCENT,
            stroke_width=1.5,
            fill_color=ACCENT,
            fill_opacity=0.1,
        )
        vis_label = Text("visual", font_size=13, color=ACCENT)
        vis_label.move_to(vis_box)
        vis_mod = VGroup(vis_box, vis_label)
        vis_mod.move_to(LEFT * 1.8 + UP * 0.8)

        # Spatial modality
        spatial_box = RoundedRectangle(
            width=1.2,
            height=0.6,
            corner_radius=0.08,
            color=TEAL,
            stroke_width=1.5,
            fill_color=TEAL,
            fill_opacity=0.1,
        )
        spatial_label = Text("spatial", font_size=13, color=TEAL)
        spatial_label.move_to(spatial_box)
        spatial_mod = VGroup(spatial_box, spatial_label)
        spatial_mod.move_to(ORIGIN + UP * 0.8)

        # State modality
        state_box = RoundedRectangle(
            width=1.2,
            height=0.6,
            corner_radius=0.08,
            color=GOLD,
            stroke_width=1.5,
            fill_color=GOLD,
            fill_opacity=0.1,
        )
        state_label = Text("state", font_size=13, color=GOLD)
        state_label.move_to(state_box)
        state_mod = VGroup(state_box, state_label)
        state_mod.move_to(RIGHT * 1.8 + UP * 0.8)

        # Internal process visualization
        inner_mods = VGroup(vis_mod, spatial_mod, state_mod)

        # Arrows converging to a processing node
        process_dot = Dot(radius=0.15, color=PURPLE, fill_opacity=0.6)
        process_dot.move_to(DOWN * 0.3)
        process_ring = Circle(
            radius=0.25,
            color=PURPLE,
            stroke_width=1.5,
            fill_opacity=0,
        )
        process_ring.move_to(process_dot)

        inner_arrows = VGroup()
        for mod in inner_mods:
            arr = Arrow(
                mod.get_bottom(),
                process_dot.get_top(),
                buff=0.1,
                color=DIM,
                stroke_width=1.2,
                max_tip_length_to_length_ratio=0.2,
            )
            inner_arrows.add(arr)

        # Fade in robot content to transparent to reveal inner workings
        self.play(
            robot3.animate.set_opacity(0.08),
            run_time=0.4,
        )

        self.play(
            LaggedStart(
                *[FadeIn(mod, scale=0.8) for mod in inner_mods],
                lag_ratio=0.12,
            ),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in inner_arrows], lag_ratio=0.1),
            FadeIn(process_dot, scale=0.5),
            Create(process_ring),
            run_time=0.6,
        )

        # Pulse the processing node
        pulse_ring = process_ring.copy().set_stroke(PURPLE, width=3)
        self.play(
            pulse_ring.animate.scale(1.8).set_opacity(0),
            run_time=0.6,
        )
        self.remove(pulse_ring)
        # [18:36] Inside: modalities decompose and merge
        self.wait(1.0)

        # ==============================================================
        #  PART 5c — ZOOM BACK OUT
        # ==============================================================

        # Fade out inner workings
        self.play(
            FadeOut(inner_mods),
            FadeOut(inner_arrows),
            FadeOut(process_dot),
            FadeOut(process_ring),
            robot3.animate.set_opacity(1).scale(0.5).move_to(RIGHT * 1.0),
            other_mobs.animate.set_opacity(1),
            run_time=0.8,
        )
        self.wait(0.3)

        # ==============================================================
        #  PART 5d — USER ASKS + ROBOT PRODUCES ACTION + LANGUAGE
        # ==============================================================

        # User question (speech bubble)
        user_q = Text('"What should I do now?"', font_size=16, color=WHITE)
        q_bubble = RoundedRectangle(
            width=user_q.width + 0.4,
            height=user_q.height + 0.3,
            corner_radius=0.1,
            color=DIM,
            stroke_width=1.2,
            fill_color="#151515",
            fill_opacity=1,
        )
        q_bubble.move_to(LEFT * 3.5 + UP * 2.2)
        user_q.move_to(q_bubble)

        q_tail = Triangle(fill_color="#151515", fill_opacity=1, stroke_width=0)
        q_tail.scale(0.12)
        q_tail.set_stroke(DIM, width=1.2)
        q_tail.next_to(q_bubble, DOWN, buff=-0.02)

        self.play(FadeIn(q_bubble), FadeIn(q_tail), Write(user_q), run_time=0.6)
        self.wait(0.4)

        # Arrow from question to robot
        q_to_robot = Arrow(
            q_bubble.get_right(),
            robot3.get_left() + UP * 0.3,
            buff=0.15,
            color=DIM,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(GrowArrow(q_to_robot), run_time=0.4)

        # Robot glow — processing
        robot_glow2 = robot3.copy().set_stroke(ACCENT, width=3, opacity=0.5)
        self.play(FadeIn(robot_glow2), run_time=0.25)
        self.play(FadeOut(robot_glow2), run_time=0.25)

        # Output: action + language
        # Action output
        action_output = VGroup()
        act_arrow_icon = Arrow(
            ORIGIN,
            RIGHT * 0.6,
            buff=0,
            color=GREEN,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.3,
        )
        act_label = Text("move right", font_size=14, color=GREEN)
        act_label.next_to(act_arrow_icon, DOWN, buff=0.1)
        action_output.add(act_arrow_icon, act_label)

        act_box = RoundedRectangle(
            width=1.6,
            height=0.9,
            corner_radius=0.1,
            color=GREEN,
            stroke_width=1.5,
            fill_color=GREEN,
            fill_opacity=0.06,
        )
        action_output.move_to(act_box)
        act_title = Text("action", font_size=12, color=GREEN)
        act_title.next_to(act_box, UP, buff=0.08)
        act_group = VGroup(act_box, action_output, act_title)
        act_group.move_to(RIGHT * 4.0 + UP * 1.0)

        # Language output
        lang_text = Text('"Jump over the obstacle"', font_size=13, color=GOLD)
        lang_box = RoundedRectangle(
            width=lang_text.width + 0.4,
            height=lang_text.height + 0.3,
            corner_radius=0.1,
            color=GOLD,
            stroke_width=1.5,
            fill_color=GOLD,
            fill_opacity=0.06,
        )
        lang_text.move_to(lang_box)
        lang_title = Text("language", font_size=12, color=GOLD)
        lang_title.next_to(lang_box, UP, buff=0.08)
        lang_group = VGroup(lang_box, lang_text, lang_title)
        lang_group.move_to(RIGHT * 4.0 + DOWN * 0.8)

        # Arrows from robot to outputs
        robot_to_act = Arrow(
            robot3.get_right(),
            act_group.get_left(),
            buff=0.15,
            color=GREEN,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )
        robot_to_lang = Arrow(
            robot3.get_right(),
            lang_group.get_left(),
            buff=0.15,
            color=GOLD,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(
            GrowArrow(robot_to_act),
            GrowArrow(robot_to_lang),
            run_time=0.5,
        )
        self.play(
            FadeIn(act_group, shift=RIGHT * 0.15),
            run_time=0.5,
        )
        self.play(
            FadeIn(lang_group, shift=RIGHT * 0.15),
            run_time=0.5,
        )

        # Final flash on both outputs
        self.play(
            Flash(act_group.get_center(), color=GREEN, flash_radius=0.5, num_lines=6),
            Flash(lang_group.get_center(), color=GOLD, flash_radius=0.5, num_lines=6),
            run_time=0.5,
        )
        # [18:40] Robot produces both actions and language
        self.wait(2.0)

        # Final fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
