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
BG = "#000000"
ACCENT = "#4FC3F7"
GOLD = "#FFD54F"
GREEN = "#66BB6A"
DIM = "#8A8A8A"
DIM2 = "#4A4A4A"
RED = "#FF5252"
PURPLE = "#B39DDB"
ORANGE = "#FFB74D"

PATCH_COLORS = [
    "#5C6BC0",
    "#42A5F5",
    "#26A69A",
    "#66BB6A",
    "#FFCA28",
    "#FF7043",
    "#AB47BC",
    "#EC407A",
    "#8D6E63",
    "#78909C",
    "#7E57C2",
    "#29B6F6",
    "#9CCC65",
    "#FFA726",
    "#EF5350",
    "#26C6DA",
]

# ── helpers ─────────────────────────────────────────────────────────


def make_robot(scale_factor=1.0):
    """Build the robot from the project SVG asset."""
    robot = SVGMobject(
        str(BASE_DIR / "assets" / "svgs" / "robot.svg"),
        fill_color=WHITE,
        stroke_color=WHITE,
        stroke_width=1.2,
        fill_opacity=0.9,
    )
    robot.set_height(2.4 * scale_factor)
    return robot


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


def make_patch_token(color, size=0.28):
    """A single visual-token square."""
    return RoundedRectangle(
        width=size,
        height=size,
        corner_radius=0.04,
        color=color,
        stroke_width=1.0,
        fill_color=color,
        fill_opacity=0.7,
    )


def make_pill(text_str, color=ACCENT, font_size=16):
    """A rounded pill-shaped label."""
    label = Text(text_str, font_size=font_size, color=WHITE)
    pill = RoundedRectangle(
        width=label.width + 0.4,
        height=label.height + 0.22,
        corner_radius=0.15,
        color=color,
        stroke_width=1.4,
        fill_color=color,
        fill_opacity=0.15,
    )
    pill.move_to(label.get_center())
    return VGroup(pill, label)


def make_grid_world():
    """Build a simple geometric grid-world environment."""
    env = VGroup()

    # Ground
    ground = Rectangle(
        width=4.0,
        height=2.5,
        color=DIM2,
        stroke_width=1.5,
        fill_color="#0A140A",
        fill_opacity=1,
    )
    env.add(ground)

    # Grid lines
    for i in range(1, 8):
        env.add(
            Line(
                ground.get_left() + RIGHT * i * 0.5 + UP * 1.25,
                ground.get_left() + RIGHT * i * 0.5 + DOWN * 1.25,
                color=DIM2,
                stroke_width=0.4,
                stroke_opacity=0.4,
            )
        )
    for j in range(1, 5):
        env.add(
            Line(
                ground.get_left() + UP * (1.25 - j * 0.5),
                ground.get_right() + UP * (1.25 - j * 0.5),
                color=DIM2,
                stroke_width=0.4,
                stroke_opacity=0.4,
            )
        )

    # Obstacles (rectangles)
    obs1 = RoundedRectangle(
        width=0.45,
        height=0.45,
        corner_radius=0.06,
        color=RED,
        stroke_width=1.5,
        fill_color=RED,
        fill_opacity=0.3,
    )
    obs1.move_to(ground.get_center() + LEFT * 0.5 + UP * 0.25)

    obs2 = RoundedRectangle(
        width=0.45,
        height=0.45,
        corner_radius=0.06,
        color=RED,
        stroke_width=1.5,
        fill_color=RED,
        fill_opacity=0.3,
    )
    obs2.move_to(ground.get_center() + RIGHT * 0.75 + DOWN * 0.5)

    # Agent dot
    agent = Dot(radius=0.12, color=ACCENT, fill_opacity=0.9)
    agent.move_to(ground.get_center() + LEFT * 1.5 + DOWN * 0.75)

    # Target star
    target = Star(
        n=5,
        outer_radius=0.15,
        inner_radius=0.07,
        color=GOLD,
        stroke_width=1.5,
        fill_color=GOLD,
        fill_opacity=0.6,
    )
    target.move_to(ground.get_center() + RIGHT * 1.5 + UP * 0.75)

    env.add(obs1, obs2, agent, target)

    return env


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
        # ================================================================
        #  PART 2 — VISION MULTIMODAL
        #  Dog image → patches → visual tokens → robot → text concepts
        # ================================================================

        # --- 1a. Show the dog image ---
        dog_img = ImageMobject(str(BASE_DIR / "assets" / "images" / "dancing_dog.jpg"))
        dog_img.set_height(3.2)
        dog_img.move_to(LEFT * 0.5 + UP * 0.3)

        # Rounded border
        img_border = RoundedRectangle(
            width=dog_img.width + 0.12,
            height=dog_img.height + 0.12,
            corner_radius=0.15,
            color=DIM,
            stroke_width=1.5,
        )
        img_border.move_to(dog_img.get_center())

        self.play(
            FadeIn(dog_img, scale=0.9),
            Create(img_border),
            run_time=0.8,
        )
        # [17:10] Can we go beyond text? What if models could see images?
        self.wait(2.0)

        # --- 1b. Overlay a grid to show patch decomposition ---
        n_rows, n_cols = 4, 4
        img_w = dog_img.width
        img_h = dog_img.height
        patch_w = img_w / n_cols
        patch_h = img_h / n_rows
        img_corner = dog_img.get_corner(UL)

        grid_lines = VGroup()
        for r in range(1, n_rows):
            y = img_corner[1] - r * patch_h
            grid_lines.add(
                Line(
                    np.array([img_corner[0], y, 0]),
                    np.array([img_corner[0] + img_w, y, 0]),
                    color=WHITE,
                    stroke_width=1.5,
                    stroke_opacity=0.7,
                )
            )
        for c in range(1, n_cols):
            x = img_corner[0] + c * patch_w
            grid_lines.add(
                Line(
                    np.array([x, img_corner[1], 0]),
                    np.array([x, img_corner[1] - img_h, 0]),
                    color=WHITE,
                    stroke_width=1.5,
                    stroke_opacity=0.7,
                )
            )

        self.play(
            LaggedStart(*[Create(l) for l in grid_lines], lag_ratio=0.04),
            run_time=0.7,
        )
        # [17:14] Image is broken into patches
        self.wait(1.0)

        # --- 1c. Create patch tokens from the grid cells ---
        patch_squares = VGroup()
        for r in range(n_rows):
            for c in range(n_cols):
                idx = r * n_cols + c
                sq = make_patch_token(PATCH_COLORS[idx % len(PATCH_COLORS)], size=0.28)
                # Position on top of the grid cell
                cx = img_corner[0] + (c + 0.5) * patch_w
                cy = img_corner[1] - (r + 0.5) * patch_h
                sq.move_to(np.array([cx, cy, 0]))
                patch_squares.add(sq)

        self.play(
            LaggedStart(
                *[FadeIn(sq, scale=0.5) for sq in patch_squares], lag_ratio=0.03
            ),
            run_time=0.6,
        )
        # [17:19] Each patch becomes a visual token
        self.wait(1.0)

        # Fade out the dog image, keep the patches
        self.play(
            FadeOut(dog_img),
            FadeOut(img_border),
            FadeOut(grid_lines),
            run_time=0.5,
        )

        # --- 1d. Arrange patches into a token row ---
        token_row = patch_squares.copy()
        token_row.arrange(RIGHT, buff=0.06)
        token_row.scale(0.75)
        token_row.move_to(LEFT * 3.0 + UP * 0.5)

        # Token labels underneath
        token_labels = VGroup()
        for i, sq in enumerate(token_row):
            if i < 4 or i == len(token_row) - 1:
                lbl_text = f"v{i+1}" if i < 4 else f"v{len(token_row)}"
                lbl = MathTex(lbl_text, font_size=12, color=DIM)
                lbl.next_to(sq, DOWN, buff=0.06)
                token_labels.add(lbl)
            elif i == 4:
                dots = MathTex(r"\cdots", font_size=14, color=DIM)
                dots.next_to(sq, DOWN, buff=0.06)
                token_labels.add(dots)

        self.play(
            ReplacementTransform(patch_squares, token_row),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[FadeIn(l) for l in token_labels], lag_ratio=0.05),
            run_time=0.4,
        )
        self.wait(1.0)

        # --- 1e. Robot appears center ---
        robot = make_robot(scale_factor=1.0)
        robot.move_to(RIGHT * 0.3)

        self.play(FadeIn(robot, scale=0.85), run_time=0.6)
        # [17:28] The model takes visual tokens
        self.wait(1.0)

        # --- 1f. Tokens flow into the robot ---
        # Animate tokens moving into the robot's center
        token_anims = []
        for sq in token_row:
            token_anims.append(
                sq.animate.move_to(robot.get_center()).scale(0.2).set_opacity(0)
            )

        self.play(
            LaggedStart(*token_anims, lag_ratio=0.04),
            FadeOut(token_labels),
            run_time=1.0,
        )
        self.remove(token_row)

        # Robot glows briefly to show processing
        robot_glow = robot.copy().set_stroke(ACCENT, width=4, opacity=0.6)
        self.play(FadeIn(robot_glow), run_time=0.2)
        self.play(FadeOut(robot_glow), run_time=0.3)

        # --- 1g. Text concepts emerge on the right ---
        concepts = ["dog", "animal", "fur", "barking", "pet"]
        concept_colors = [GOLD, ACCENT, GREEN, ORANGE, PURPLE]
        concept_pills = VGroup()

        for i, (text, color) in enumerate(zip(concepts, concept_colors)):
            pill = make_pill(f'"{text}"', color=color, font_size=15)
            concept_pills.add(pill)

        concept_pills.arrange(DOWN, buff=0.14)
        concept_pills.move_to(RIGHT * 3.8 + UP * 0.3)

        # Connect lines from robot to concept pills
        concept_lines = VGroup()
        for pill in concept_pills:
            line = Line(
                robot.get_right() + RIGHT * 0.1,
                pill.get_left() + LEFT * 0.05,
                color=DIM2,
                stroke_width=0.8,
                stroke_opacity=0.5,
            )
            concept_lines.add(line)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(line),
                        FadeIn(pill, shift=RIGHT * 0.15),
                    )
                    for line, pill in zip(concept_lines, concept_pills)
                ],
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        # [17:37] And maps them to text concepts like "dog", "animal", "fur"
        self.wait(2.0)

        # --- 1h. Prompt and response ---
        prompt = Text('"What animal is this?"', font_size=18, color=DIM)
        prompt.move_to(DOWN * 2.2 + LEFT * 2.0)

        prompt_arrow = Arrow(
            prompt.get_right(),
            robot.get_bottom() + DOWN * 0.1 + LEFT * 0.3,
            buff=0.15,
            color=DIM,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            FadeIn(prompt, shift=UP * 0.1),
            GrowArrow(prompt_arrow),
            run_time=0.6,
        )

        # Processing pulse
        pulse = Circle(radius=0.5, color=ACCENT, stroke_width=2, fill_opacity=0)
        pulse.move_to(robot.get_center())
        self.play(
            Create(pulse),
            pulse.animate.scale(1.8).set_stroke(opacity=0),
            run_time=0.5,
        )
        self.remove(pulse)

        # Output
        answer = Text('"Dog"', font_size=28, color=GOLD, weight=BOLD)
        answer.move_to(DOWN * 2.2 + RIGHT * 2.5)

        answer_arrow = Arrow(
            robot.get_bottom() + DOWN * 0.1 + RIGHT * 0.3,
            answer.get_left(),
            buff=0.15,
            color=GOLD,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            GrowArrow(answer_arrow),
            FadeIn(answer, scale=1.3),
            Flash(
                answer.get_center(),
                color=GOLD,
                flash_radius=0.5,
                line_length=0.12,
                num_lines=8,
            ),
            run_time=0.7,
        )
        # [17:43] It can answer questions about images
        self.wait(3.0)

        # --- Transition out Part 1 ---
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

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

        # ================================================================
        #  PART 2 — ACTION-BASED MULTIMODAL
        #  Environment → Robot → Decomposition → Actions + Language
        # ================================================================

        # --- 2a. Show the environment ---
        env = make_grid_world()
        env.scale(0.9)
        env.move_to(LEFT * 3.0 + DOWN * 0.3)

        env_label = Text("environment", font_size=14, color=DIM)
        env_label.next_to(env, DOWN, buff=0.2)

        self.play(
            FadeIn(env, scale=0.9),
            FadeIn(env_label),
            run_time=0.7,
        )
        # [17:52] The environment becomes another input modality
        self.wait(1.0)

        # --- 2b. Robot appears on the right ---
        robot2 = make_robot(scale_factor=1.0)
        robot2.move_to(RIGHT * 2.5 + DOWN * 0.3)

        self.play(FadeIn(robot2, scale=0.85), run_time=0.5)

        # Arrow from env to robot
        env_to_robot = Arrow(
            env.get_right() + RIGHT * 0.1,
            robot2.get_left() + LEFT * 0.1,
            buff=0.1,
            color=ACCENT,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(GrowArrow(env_to_robot), run_time=0.5)
        self.wait(0.3)

        # --- 2c. Environment flows into robot ---
        env_copy = env.copy()
        self.play(
            env_copy.animate.move_to(robot2.get_center()).scale(0.15).set_opacity(0),
            FadeOut(env),
            FadeOut(env_label),
            FadeOut(env_to_robot),
            run_time=0.8,
        )
        self.remove(env_copy)

        # --- 2d. Fake zoom into the robot ---
        # Scale robot to fill the screen
        zoom_center = robot2.get_center()

        self.play(
            robot2.animate.scale(4.5).move_to(ORIGIN + UP * 2.0),
            run_time=0.8,
            rate_func=smooth,
        )

        # --- 2e. Inside the robot: modality decomposition ---
        # Dark overlay to represent "inside"
        inside_bg = Rectangle(
            width=config.frame_width + 1,
            height=config.frame_height + 1,
            color=BG,
            stroke_width=0,
            fill_color=BG,
            fill_opacity=0.85,
        )
        inside_bg.move_to(ORIGIN)

        inside_label = Text("inside the model", font_size=16, color=DIM)
        inside_label.to_edge(UP, buff=0.4)

        self.play(FadeIn(inside_bg), FadeIn(inside_label), run_time=0.4)

        # --- Vision modality ---
        vision_title = Text("vision", font_size=16, color=ACCENT)
        vision_title.move_to(LEFT * 4.0 + UP * 1.8)

        vision_patches = VGroup()
        for r in range(3):
            for c in range(4):
                sq = make_patch_token(
                    PATCH_COLORS[(r * 4 + c) % len(PATCH_COLORS)], size=0.32
                )
                sq.move_to(LEFT * 4.5 + RIGHT * c * 0.38 + UP * (0.8 - r * 0.38))
                vision_patches.add(sq)

        # --- Audio modality ---
        audio_title = Text("audio", font_size=16, color=PURPLE)
        audio_title.move_to(UP * 1.8)

        # Simple waveform
        wave_points = []
        for i in range(60):
            x = -1.5 + i * 0.05
            y = 0.3 * np.sin(i * 0.5) * np.exp(-0.02 * abs(i - 30))
            wave_points.append(np.array([x, y + 0.5, 0]))

        waveform = VMobject(color=PURPLE, stroke_width=2.5)
        waveform.set_points_smoothly(wave_points)

        # Audio tokens below waveform
        audio_tokens = VGroup()
        for i in range(8):
            tok = RoundedRectangle(
                width=0.28,
                height=0.2,
                corner_radius=0.04,
                color=PURPLE,
                stroke_width=1,
                fill_color=PURPLE,
                fill_opacity=0.25,
            )
            tok.move_to(LEFT * 1.0 + RIGHT * i * 0.34 + DOWN * 0.2)
            audio_tokens.add(tok)

        # --- Text/state modality ---
        text_title = Text("state", font_size=16, color=GREEN)
        text_title.move_to(RIGHT * 4.0 + UP * 1.8)

        state_tokens = VGroup()
        state_labels_txt = ["pos", "vel", "dir", "hp", "inv"]
        for i, txt in enumerate(state_labels_txt):
            tok_bg = RoundedRectangle(
                width=0.55,
                height=0.3,
                corner_radius=0.05,
                color=GREEN,
                stroke_width=1,
                fill_color=GREEN,
                fill_opacity=0.15,
            )
            tok_label = Text(txt, font_size=10, color=GREEN)
            tok_label.move_to(tok_bg.get_center())
            tok = VGroup(tok_bg, tok_label)
            state_tokens.add(tok)

        state_tokens.arrange(DOWN, buff=0.1)
        state_tokens.move_to(RIGHT * 4.0 + UP * 0.5)

        # Animate the three modalities appearing
        self.play(
            Write(vision_title),
            LaggedStart(
                *[FadeIn(sq, scale=0.6) for sq in vision_patches], lag_ratio=0.02
            ),
            run_time=0.7,
        )
        self.play(
            Write(audio_title),
            Create(waveform),
            LaggedStart(
                *[FadeIn(t, shift=DOWN * 0.05) for t in audio_tokens], lag_ratio=0.04
            ),
            run_time=0.7,
        )
        self.play(
            Write(text_title),
            LaggedStart(*[FadeIn(t, scale=0.8) for t in state_tokens], lag_ratio=0.06),
            run_time=0.7,
        )

        # Convergence arrows pointing down to a central "model" token stream
        merge_point = DOWN * 1.8
        merge_label = Text("unified token stream", font_size=14, color=GOLD)
        merge_label.move_to(merge_point + DOWN * 0.5)

        # Unified stream visualization
        unified_tokens = VGroup()
        stream_colors = [
            ACCENT,
            ACCENT,
            PURPLE,
            PURPLE,
            GREEN,
            ACCENT,
            GREEN,
            PURPLE,
            ACCENT,
            GREEN,
        ]
        for i, clr in enumerate(stream_colors):
            tok = RoundedRectangle(
                width=0.3,
                height=0.22,
                corner_radius=0.04,
                color=clr,
                stroke_width=1,
                fill_color=clr,
                fill_opacity=0.4,
            )
            unified_tokens.add(tok)
        unified_tokens.arrange(RIGHT, buff=0.06)
        unified_tokens.move_to(merge_point)

        # Arrows from each modality to the merge point
        conv_arrows = VGroup()
        for source in [vision_patches, audio_tokens, state_tokens]:
            arr = Arrow(
                source.get_bottom(),
                merge_point + UP * 0.2,
                buff=0.15,
                color=DIM,
                stroke_width=1.2,
                max_tip_length_to_length_ratio=0.12,
            )
            conv_arrows.add(arr)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in conv_arrows], lag_ratio=0.1),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(t, scale=0.5) for t in unified_tokens], lag_ratio=0.03
            ),
            FadeIn(merge_label, shift=UP * 0.08),
            run_time=0.7,
        )
        # [17:54] All modalities merge into a unified token stream
        self.wait(2.0)

        # --- 2f. Zoom back out ---
        inside_elements = VGroup(
            inside_bg,
            inside_label,
            vision_title,
            vision_patches,
            audio_title,
            waveform,
            audio_tokens,
            text_title,
            state_tokens,
            conv_arrows,
            unified_tokens,
            merge_label,
        )

        self.play(FadeOut(inside_elements), run_time=0.5)
        self.play(
            robot2.animate.scale(1 / 4.5).move_to(ORIGIN),
            run_time=0.8,
            rate_func=smooth,
        )
        self.wait(1.0)

        # --- 2g. User prompt ---
        user_prompt = Text('"What should I do now?"', font_size=18, color=DIM)
        user_prompt.move_to(DOWN * 2.0)

        prompt_to_robot = Arrow(
            user_prompt.get_top(),
            robot2.get_bottom() + DOWN * 0.05,
            buff=0.12,
            color=DIM,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            FadeIn(user_prompt, shift=UP * 0.1),
            GrowArrow(prompt_to_robot),
            run_time=0.6,
        )

        # Processing pulse
        pulse2 = Circle(radius=0.4, color=GOLD, stroke_width=2, fill_opacity=0)
        pulse2.move_to(robot2.get_center())
        self.play(
            Create(pulse2),
            pulse2.animate.scale(2.0).set_stroke(opacity=0),
            run_time=0.5,
        )
        self.remove(pulse2)

        # --- 2h. Dual output: action + language ---
        # Action output (left side)
        action_label = Text("action", font_size=16, color=ACCENT)
        action_label.move_to(LEFT * 3.5 + UP * 1.8)

        # Movement arrow showing a path
        action_path = VGroup()
        path_start = LEFT * 4.0 + UP * 0.5
        path_points = [
            path_start,
            path_start + RIGHT * 0.8,
            path_start + RIGHT * 0.8 + UP * 0.6,
            path_start + RIGHT * 1.8 + UP * 0.6,
        ]

        for i in range(len(path_points) - 1):
            seg = Arrow(
                path_points[i],
                path_points[i + 1],
                buff=0,
                color=ACCENT,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.2,
            )
            action_path.add(seg)

        action_text = Text(
            '"move forward, then turn right"', font_size=13, color=ACCENT
        )
        action_text.move_to(LEFT * 3.2 + DOWN * 0.3)

        robot_to_action = Arrow(
            robot2.get_left() + LEFT * 0.05,
            LEFT * 2.5 + UP * 0.5,
            buff=0.15,
            color=DIM,
            stroke_width=1.0,
            max_tip_length_to_length_ratio=0.12,
        )

        # Language output (right side)
        lang_label = Text("language", font_size=16, color=GOLD)
        lang_label.move_to(RIGHT * 3.5 + UP * 1.8)

        # Speech bubble
        bubble_rect = RoundedRectangle(
            width=3.0,
            height=0.8,
            corner_radius=0.15,
            color=GOLD,
            stroke_width=1.5,
            fill_color=GOLD,
            fill_opacity=0.08,
        )
        bubble_text = Text(
            '"Obstacle ahead — go around it"',
            font_size=13,
            color=GOLD,
        )
        bubble_text.move_to(bubble_rect.get_center())
        bubble = VGroup(bubble_rect, bubble_text)
        bubble.move_to(RIGHT * 3.5 + UP * 0.5)

        robot_to_lang = Arrow(
            robot2.get_right() + RIGHT * 0.05,
            bubble.get_left() + LEFT * 0.05,
            buff=0.1,
            color=DIM,
            stroke_width=1.0,
            max_tip_length_to_length_ratio=0.12,
        )

        # Animate action output
        self.play(
            FadeIn(action_label, shift=DOWN * 0.1),
            GrowArrow(robot_to_action),
            run_time=0.5,
        )
        self.play(
            LaggedStart(*[GrowArrow(seg) for seg in action_path], lag_ratio=0.15),
            run_time=0.7,
        )
        self.play(FadeIn(action_text, shift=UP * 0.08), run_time=0.4)

        # Animate language output
        self.play(
            FadeIn(lang_label, shift=DOWN * 0.1),
            GrowArrow(robot_to_lang),
            run_time=0.5,
        )
        self.play(
            FadeIn(bubble, scale=0.9),
            run_time=0.5,
        )
        self.wait(2.0)

        # --- Final emphasis ---
        # Glow on both outputs
        action_glow = SurroundingRectangle(
            VGroup(action_path, action_text),
            color=ACCENT,
            buff=0.2,
            corner_radius=0.12,
            stroke_width=1.5,
            fill_color=ACCENT,
            fill_opacity=0.04,
        )
        lang_glow = SurroundingRectangle(
            bubble,
            color=GOLD,
            buff=0.15,
            corner_radius=0.12,
            stroke_width=1.5,
            fill_color=GOLD,
            fill_opacity=0.04,
        )

        self.play(
            Create(action_glow),
            Create(lang_glow),
            run_time=0.6,
        )
        self.play(
            Flash(
                action_path[-1].get_end(), color=ACCENT, flash_radius=0.3, num_lines=6
            ),
            Flash(bubble.get_center(), color=GOLD, flash_radius=0.4, num_lines=6),
            run_time=0.5,
        )
        # [18:00] The model produces both language and actions
        self.wait(3.0)

        # --- Final fade ---
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
