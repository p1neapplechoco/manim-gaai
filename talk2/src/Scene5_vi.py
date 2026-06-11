from pathlib import Path

from manim import *


_ASSETS = Path(__file__).resolve().parents[1] / "assets"
SCENE5_DIR = _ASSETS / "Scene5"
if not SCENE5_DIR.exists():
    SCENE5_DIR = _ASSETS / "Sccene5"

ARCHITECTURE_IMAGE = SCENE5_DIR / "ViP-LLaVA_Architecture.png"
LEFT_EXAMPLE_IMAGE = SCENE5_DIR / "Left.png"
RIGHT_EXAMPLE_IMAGE = SCENE5_DIR / "Right.png"
PROMPT_IMAGES = {
    "Mask contour\noutline prompt": SCENE5_DIR / "Mask contour.png",
    "Ellipse\nregion prompt": SCENE5_DIR / "Ellipse.png",
    "Bounding box\nbox prompt": SCENE5_DIR / "Bounding Box.png",
    "Triangle\nshape prompt": SCENE5_DIR / "Triangle.png",
    "Scribble\nfreehand prompt": SCENE5_DIR / "Scribble.png",
    "Point\npoint prompt": SCENE5_DIR / "Point.png",
    "Arrow\ndirectional prompt": SCENE5_DIR / "Arrow.png",
    "Mask\nfilled prompt": SCENE5_DIR / "Mask.png",
}

TEXT_FONT = "Times New Roman"


TIME_SCALE = 3.2


class ScaledTimingMixin:
    time_scale = TIME_SCALE

    def play(self, *animations, **kwargs):
        if "run_time" in kwargs:
            if kwargs["run_time"] is not None:
                kwargs["run_time"] *= self.time_scale
        else:
            run_times = [
                getattr(animation, "run_time", None)
                for animation in animations
                if getattr(animation, "run_time", None) is not None
            ]
            kwargs["run_time"] = (max(run_times) if run_times else 1.0) * self.time_scale
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, stop_condition=None, frozen_frame=None):
        if duration is not None:
            duration *= self.time_scale
        return super().wait(duration=duration, stop_condition=stop_condition, frozen_frame=frozen_frame)


class Scene5(ScaledTimingMixin, Scene):
    def construct(self):
        self.camera.background_color = BLACK

        self.visual = "#58C4DD"
        self.language = "#83C167"
        self.connector = "#FFFF00"
        self.orange = "#FF8C2A"
        self.warning = "#FF6666"
        self.dim = "#2C2C2C"

        self.scene_opening_question()
        self.scene_prior_work_limits()
        self.scene_alpha_blending()
        self.scene_architecture_pipeline()
        self.scene_architecture_steps()
        self.scene_ln_mlp_explanation()
        self.scene_prompt_types()
        self.scene_region_question()
        self.scene_final_insight()
        self.scene_left_right_example()

    def make_title(self, text, color=WHITE):
        title = Text(text, font=TEXT_FONT, font_size=30, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        underline = Line(LEFT, RIGHT).set_width(min(8.4, title.width * 0.92))
        underline.next_to(title, DOWN, buff=0.1)
        underline.set_color_by_gradient(self.visual, self.connector, self.language)
        return VGroup(title, underline)

    def text(self, content, color=WHITE, size=20, width=None, weight=NORMAL, line_spacing=1.0):
        mob = Text(content, font=TEXT_FONT, font_size=size, color=color, weight=weight, line_spacing=line_spacing)
        if width and mob.width > width:
            mob.set_width(width)
        return mob

    def card(self, width, height, color, content=None, fill_opacity=0.12, radius=0.12, stroke_width=1.6):
        rect = RoundedRectangle(
            corner_radius=radius,
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=stroke_width,
            fill_color=color,
            fill_opacity=fill_opacity,
        )
        glow = rect.copy().set_stroke(WHITE, width=0.5, opacity=0.11).scale(1.01)
        group = VGroup(rect, glow)
        if content is not None:
            content.move_to(rect)
            group.add(content)
        return group

    def image_card(self, path, width=4.4, height=2.8, color=None, fill="#0A1118"):
        color = color or self.visual
        frame = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=2,
            fill_color=fill,
            fill_opacity=0.9,
        )
        if Path(path).exists():
            image = ImageMobject(str(path))
            image.set_width(width - 0.16)
            if image.height > height - 0.16:
                image.set_height(height - 0.16)
            image.move_to(frame)
            return Group(frame, image)
        missing = self.text("Missing image\n" + Path(path).name, self.warning, 16, width - 0.3)
        missing.move_to(frame)
        return VGroup(frame, missing)

    def cleanup(self, *mobjects):
        self.play(FadeOut(Group(*mobjects), shift=UP * 0.12), run_time=0.6)

    def mini_image_scene(self, with_prompt=False):
        inner_frame = Rectangle(width=2.68, height=1.08, stroke_color=self.visual, fill_color="#303B45", fill_opacity=0.75)
        circle = Circle(radius=0.2, color=self.language, fill_opacity=0.9).shift(LEFT * 0.86 + UP * 0.06)
        square = Square(side_length=0.36, color=self.orange, fill_opacity=0.9).shift(RIGHT * 0.18 + DOWN * 0.06)
        triangle = Triangle(color=self.warning, fill_opacity=0.85).scale(0.2).shift(RIGHT * 0.94 + UP * 0.07)
        content = VGroup(inner_frame, circle, square, triangle)
        base = self.card(
            3.1,
            2.0,
            self.visual,
            content,
            fill_opacity=0.08,
        )
        if with_prompt:
            circle_center = circle.get_center()
            square_center = square.get_center()
            arrow = Arrow(
                circle_center + UP * 0.7,
                circle_center,
                buff=0,
                color=self.connector,
                stroke_width=7,
                max_tip_length_to_length_ratio=0.28,
            )
            scribble = VMobject(color=self.connector, stroke_width=5)
            scribble.set_points_smoothly([
                square_center + LEFT * 0.32 + DOWN * 0.43,
                square_center + LEFT * 0.12 + DOWN * 0.28,
                square_center + RIGHT * 0.1 + DOWN * 0.43,
                square_center + RIGHT * 0.34 + DOWN * 0.27,
            ])
            base.add(arrow, scribble)
        return base

    def scene_opening_question(self):
        title = self.make_title('Can LLaVA Understand "Visual Prompts"?', self.connector)
        image = self.mini_image_scene(with_prompt=False).move_to(LEFT * 3.45 + UP * 0.05)
        prompted = self.mini_image_scene(with_prompt=True).move_to(RIGHT * 3.45 + UP * 0.05)

        q1 = self.card(
            4.0,
            0.52,
            self.visual,
            self.text("What is happening in this image?", WHITE, 17, 3.55, weight=BOLD),
            fill_opacity=0.14,
        ).next_to(image, DOWN, buff=0.25)
        q2 = self.card(
            4.45,
            0.72,
            self.connector,
            self.text("What is the person pointed to by the arrow doing?", BLACK, 16, 4.05, weight=BOLD, line_spacing=0.86),
            fill_opacity=0.9,
        ).next_to(prompted, DOWN, buff=0.25)
        bridge = Arrow(image.get_right() + RIGHT * 0.15, prompted.get_left() + LEFT * 0.15, color=self.connector, stroke_width=5, buff=0.04)
        note = self.card(
            8.6,
            0.55,
            self.language,
            self.text("From image-level understanding to region-level instruction following.", WHITE, 19, 8.1, weight=BOLD),
            fill_opacity=0.12,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), FadeIn(q1, shift=UP * 0.08), run_time=1.0)
        self.play(GrowArrow(bridge), FadeIn(prompted, scale=0.96), FadeIn(q2, shift=UP * 0.08), run_time=1.1)
        self.play(FadeIn(note, shift=UP * 0.08), Circumscribe(q2, color=self.connector), run_time=1.1)
        self.wait(0.35)
        self.cleanup(title, image, prompted, q1, q2, bridge, note)

    def scene_prior_work_limits(self):
        title = self.make_title("Earlier Region Understanding Felt Unnatural")
        natural = self.card(
            4.8,
            3.3,
            self.language,
            VGroup(
                self.text("Natural human prompt", self.language, 22, 4.2, weight=BOLD),
                self.mini_image_scene(with_prompt=True).scale(0.85),
                self.text("Point here", WHITE, 22, 3.2, weight=BOLD),
            ).arrange(DOWN, buff=0.2),
            fill_opacity=0.08,
        ).move_to(LEFT * 3.0 + UP * 0.1)
        machine = self.card(
            4.9,
            3.3,
            self.warning,
            VGroup(
                self.text("Prior / concurrent work", self.warning, 21, 4.3, weight=BOLD),
                MathTex(r"[x_1,y_1,x_2,y_2]", font_size=32, color=WHITE),
                self.text("text (A) within <bbox>\nregion token\nlearned position embedding", WHITE, 18, 4.0, line_spacing=0.9),
            ).arrange(DOWN, buff=0.22),
            fill_opacity=0.08,
        ).move_to(RIGHT * 3.0 + UP * 0.1)
        conclusion = self.text("Problem: users had to speak in the machine's format.", self.connector, 20, 8.6, weight=BOLD).next_to(title, DOWN, buff=0.25)

        self.play(Write(title), FadeIn(conclusion, shift=DOWN * 0.08), run_time=1.0)
        self.play(FadeIn(natural, shift=RIGHT * 0.12), run_time=0.9)
        self.play(FadeIn(machine, shift=LEFT * 0.12), run_time=0.9)
        self.play(Circumscribe(machine[2][1], color=self.warning), run_time=1.2)
        self.wait(0.35)
        self.cleanup(title, conclusion, natural, machine)

    def scene_alpha_blending(self):
        title = self.make_title("ViP-LLaVA: Draw Directly on the Image", self.connector)
        original = self.mini_image_scene(with_prompt=False).move_to(LEFT * 4.25 + UP * 0.55)
        prompt_layer = self.card(
            2.35,
            1.55,
            self.connector,
            Circle(radius=0.43, color=self.connector, stroke_width=7),
            fill_opacity=0.06,
        ).move_to(UP * 0.55)
        blended = self.mini_image_scene(with_prompt=True).move_to(RIGHT * 4.25 + UP * 0.55)
        labels = VGroup(
            self.text("Original image", self.visual, 18, 2.7, weight=BOLD).next_to(original, DOWN, buff=0.16),
            self.text("Visual prompt", self.connector, 18, 2.7, weight=BOLD).next_to(prompt_layer, DOWN, buff=0.16),
            self.text("Marked image", self.language, 18, 2.7, weight=BOLD).next_to(blended, DOWN, buff=0.16),
        )
        plus = self.text("+", WHITE, 42, 0.5, weight=BOLD).move_to((original.get_right() + prompt_layer.get_left()) / 2)
        equals = self.text("=", WHITE, 42, 0.5, weight=BOLD).move_to((prompt_layer.get_right() + blended.get_left()) / 2)
        formula = MathTex(r"\tilde{X}_v=\alpha P_v+(1-\alpha)X_v", font_size=42)
        formula.set_color_by_tex(r"\tilde{X}_v", self.language)
        formula.set_color_by_tex(r"P_v", self.connector)
        formula.set_color_by_tex(r"X_v", self.visual)
        formula.to_edge(DOWN, buff=0.72)
        chips = VGroup(
            self.small_chip("Alpha Blending", self.connector, BLACK),
            self.small_chip("freehand on image", self.visual),
            self.small_chip("no coordinates", self.language),
        ).arrange(RIGHT, buff=0.18).next_to(title, DOWN, buff=0.25)

        self.play(Write(title), LaggedStart(*[FadeIn(chip, shift=DOWN * 0.06) for chip in chips], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(original), FadeIn(labels[0]), run_time=0.8)
        self.play(FadeIn(plus), FadeIn(prompt_layer, scale=0.95), FadeIn(labels[1]), run_time=0.8)
        self.play(FadeIn(equals), ReplacementTransform(original.copy(), blended), FadeIn(labels[2]), run_time=1.1)
        self.play(Write(formula), Circumscribe(blended, color=self.language), run_time=1.2)
        self.wait(0.45)
        self.cleanup(title, original, prompt_layer, blended, labels, plus, equals, formula, chips)

    def small_chip(self, label, color, text_color=WHITE):
        return self.card(
            2.25,
            0.42,
            color,
            self.text(label, text_color, 14, 2.0, weight=BOLD),
            fill_opacity=0.88 if text_color == BLACK else 0.13,
            radius=0.08,
        )

    def make_column_vector(self, entries=None, color=None, font_size=24):
        color = color or self.visual
        entries = entries or [r"z_1", r"z_2", r"z_3", r"\vdots", r"z_n"]
        vector = MathTex(
            r"\begin{bmatrix}" + r"\\".join(entries) + r"\end{bmatrix}",
            font_size=font_size,
            color=color,
        )
        frame = RoundedRectangle(
            corner_radius=0.08,
            width=vector.width + 0.36,
            height=vector.height + 0.28,
            stroke_color=color,
            stroke_width=1.8,
            fill_color=color,
            fill_opacity=0.08,
        )
        vector.move_to(frame)
        return VGroup(frame, vector)

    def scene_architecture_pipeline(self):
        title = self.make_title("ViP-LLaVA Architecture Pipeline")
        arch = self.image_card(ARCHITECTURE_IMAGE, width=9.4, height=4.05, color=self.orange).move_to(UP * 0.38)
        prompt = self.card(
            8.2,
            0.52,
            self.connector,
            self.text("Text question: What is the scribble-marked person trying to do?", BLACK, 17, 7.75, weight=BOLD),
            fill_opacity=0.9,
        ).next_to(arch, DOWN, buff=0.18)
        caption = self.card(
            8.7,
            0.5,
            self.language,
            self.text("The visual prompt is blended into the image before the encoder, so the model sees both content and focus region.", WHITE, 15, 8.2, weight=BOLD),
            fill_opacity=0.13,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(arch, scale=0.97), run_time=1.0)
        self.play(FadeIn(prompt, shift=UP * 0.08), FadeIn(caption, shift=UP * 0.08), run_time=0.9)
        self.play(Circumscribe(arch, color=self.orange), run_time=0.9)
        self.wait(0.35)
        self.cleanup(title, arch, caption, prompt)

    def scene_architecture_steps(self):
        title = self.make_title("ViP-LLaVA: From Marked Image to Answer")
        prompted_image = self.mini_image_scene(with_prompt=True).scale(0.66).move_to(LEFT * 5.45 + UP * 0.72)
        image_label = VGroup(
            self.text("Marked image", self.connector, 15, 2.15, weight=BOLD),
            MathTex(r"\tilde{X}_v", font_size=26, color=self.connector),
        ).arrange(DOWN, buff=0.04).next_to(prompted_image, DOWN, buff=0.15)

        encoder = self.card(
            1.58,
            1.02,
            self.visual,
            VGroup(
                self.text("CLIP", self.visual, 17, 1.2, weight=BOLD),
                self.text("Image\nEncoder", WHITE, 15, 1.35, weight=BOLD, line_spacing=0.82),
            ).arrange(DOWN, buff=0.05),
            fill_opacity=0.12,
        ).move_to(LEFT * 3.35 + UP * 0.72)
        encoder_note = self.text("encodes image", self.visual, 15, 1.95).next_to(encoder, DOWN, buff=0.2)

        feature_vector = self.make_column_vector(
            [r"z_1", r"z_2", r"z_3", r"z_4", r"\vdots", r"z_n"],
            self.visual,
            font_size=21,
        ).move_to(LEFT * 1.72 + UP * 0.72)
        feature_label = VGroup(
            self.text("Feature vector", self.visual, 15, 2.05, weight=BOLD),
            MathTex(r"Z_v", font_size=25, color=self.visual),
        ).arrange(DOWN, buff=0.04).next_to(feature_vector, DOWN, buff=0.15)

        connector = self.card(
            1.62,
            1.02,
            self.orange,
            VGroup(
                self.text("Fusion", self.orange, 16, 1.25, weight=BOLD),
                self.text("LN\nMLP", WHITE, 14, 1.2, weight=BOLD, line_spacing=0.8),
            ).arrange(DOWN, buff=0.06),
            fill_opacity=0.12,
        ).move_to(RIGHT * 0.18 + UP * 0.72)
        connector_note = self.text("projector", self.orange, 15, 1.8).next_to(connector, DOWN, buff=0.2)

        visual_tokens = VGroup(*[
            self.card(0.48, 0.56, self.language, self.text(f"h{i}", WHITE, 14, 0.4, weight=BOLD), fill_opacity=0.14, radius=0.06)
            for i in range(1, 6)
        ]).arrange(RIGHT, buff=0.08).move_to(RIGHT * 2.62 + UP * 0.72)
        tokens_label = VGroup(
            self.text("Visual tokens", self.language, 15, 1.95, weight=BOLD),
            MathTex(r"H_v", font_size=25, color=self.language),
        ).arrange(DOWN, buff=0.04).next_to(visual_tokens, DOWN, buff=0.16)

        llm = self.card(
            1.55,
            1.08,
            self.language,
            self.text("LLM\nreasoning", WHITE, 16, 1.35, weight=BOLD, line_spacing=0.84),
            fill_opacity=0.14,
        ).move_to(RIGHT * 5.35 + UP * 0.72)
        answer = self.card(
            2.35,
            0.62,
            self.language,
            self.text("Answer", WHITE, 17, 2.15, weight=BOLD),
            fill_opacity=0.14,
        ).next_to(llm, DOWN, buff=0.48)

        text_prompt = self.card(
            3.35,
            0.58,
            self.connector,
            self.text("Text question:\nwhat is the marked region?", BLACK, 14, 3.0, weight=BOLD, line_spacing=0.85),
            fill_opacity=0.9,
        ).move_to(RIGHT * 5.35 + UP * 2.05)

        arrow_1 = Arrow(prompted_image.get_right(), encoder.get_left(), buff=0.12, color=self.visual, stroke_width=4)
        arrow_2 = Arrow(encoder.get_right(), feature_vector.get_left(), buff=0.12, color=self.visual, stroke_width=4)
        arrow_3 = Arrow(feature_vector.get_right(), connector.get_left(), buff=0.12, color=self.orange, stroke_width=4)
        arrow_3b = Arrow(connector.get_right(), visual_tokens.get_left(), buff=0.12, color=self.orange, stroke_width=4)
        arrow_4 = Arrow(visual_tokens.get_right(), llm.get_left(), buff=0.12, color=self.language, stroke_width=4)
        text_arrow = Arrow(text_prompt.get_bottom(), llm.get_top(), buff=0.12, color=self.connector, stroke_width=4)
        answer_arrow = Arrow(llm.get_bottom(), answer.get_top(), buff=0.1, color=self.language, stroke_width=4)

        formula = MathTex(r"\tilde{X}_v \rightarrow Z_v \rightarrow H_v \rightarrow X_a", font_size=34)
        formula.set_color_by_tex(r"\tilde{X}_v", self.connector)
        formula.set_color_by_tex(r"Z_v", self.visual)
        formula.set_color_by_tex(r"H_v", self.language)
        formula.set_color_by_tex(r"X_a", self.language)
        formula.to_edge(DOWN, buff=0.34)

        self.play(Write(title), run_time=0.85)
        self.play(FadeIn(prompted_image, scale=0.96), FadeIn(image_label, shift=UP * 0.08), run_time=1.0)
        self.play(GrowArrow(arrow_1), DrawBorderThenFill(encoder), FadeIn(encoder_note, shift=UP * 0.08), run_time=1.05)
        self.play(GrowArrow(arrow_2), TransformFromCopy(prompted_image, feature_vector), FadeIn(feature_label, shift=UP * 0.08), run_time=1.35)
        self.play(GrowArrow(arrow_3), DrawBorderThenFill(connector), FadeIn(connector_note, shift=UP * 0.08), run_time=1.05)
        self.play(GrowArrow(arrow_3b), TransformFromCopy(feature_vector, visual_tokens), FadeIn(tokens_label, shift=UP * 0.08), run_time=1.2)
        self.play(FadeIn(text_prompt, shift=UP * 0.08), GrowArrow(text_arrow), run_time=0.8)
        self.play(GrowArrow(arrow_4), DrawBorderThenFill(llm), run_time=1.0)
        self.play(GrowArrow(answer_arrow), FadeIn(answer, shift=UP * 0.08), Write(formula), run_time=1.2)
        self.play(Circumscribe(feature_vector, color=self.visual), Circumscribe(visual_tokens, color=self.language), run_time=1.0)
        self.wait(0.45)
        self.cleanup(
            title,
            prompted_image,
            image_label,
            encoder,
            encoder_note,
            feature_vector,
            feature_label,
            connector,
            connector_note,
            visual_tokens,
            tokens_label,
            llm,
            answer,
            text_prompt,
            arrow_1,
            arrow_2,
            arrow_3,
            arrow_3b,
            arrow_4,
            text_arrow,
            answer_arrow,
            formula,
        )

    def scene_ln_mlp_explanation(self):
        title = self.make_title("What Do LN and MLP Do in the Projector?")
        z_vec = self.make_column_vector(
            [r"z_1", r"z_2", r"z_3", r"\vdots", r"z_n"],
            self.visual,
            font_size=24,
        ).move_to(LEFT * 4.75 + UP * 0.45)
        z_label = VGroup(
            self.text("Features from CLIP", self.visual, 15, 2.4, weight=BOLD),
            MathTex(r"Z_v", font_size=28, color=self.visual),
        ).arrange(DOWN, buff=0.05).next_to(z_vec, DOWN, buff=0.16)

        ln = self.card(
            2.25,
            1.28,
            self.orange,
            VGroup(
                self.text("LN", self.orange, 28, 1.6, weight=BOLD),
                self.text("LayerNorm\nnormalizes scale", WHITE, 16, 2.0, weight=BOLD, line_spacing=0.88),
            ).arrange(DOWN, buff=0.08),
            fill_opacity=0.12,
        ).move_to(LEFT * 1.75 + UP * 0.45)
        ln_note = self.card(
            2.65,
            0.56,
            self.orange,
            self.text("keeps features stable\nbefore projection", WHITE, 15, 2.5, line_spacing=0.82),
            fill_opacity=0.12,
            radius=0.08,
        ).next_to(ln, DOWN, buff=0.22)

        mlp = self.card(
            2.25,
            1.28,
            self.connector,
            VGroup(
                self.text("MLP", BLACK, 28, 1.6, weight=BOLD),
                self.text("learned\nprojector", BLACK, 15, 1.85, weight=BOLD, line_spacing=0.88),
            ).arrange(DOWN, buff=0.08),
            fill_opacity=0.9,
        ).move_to(RIGHT * 1.25 + UP * 0.45)
        mlp_note = self.card(
            2.75,
            0.56,
            self.connector,
            self.text("maps visual vectors\ninto LLM embeddings", BLACK, 15, 2.6, line_spacing=0.82),
            fill_opacity=0.9,
            radius=0.08,
        ).next_to(mlp, DOWN, buff=0.22)

        h_tokens = VGroup(*[
            self.card(0.54, 0.64, self.language, self.text(f"h{i}", WHITE, 14, 0.44, weight=BOLD), fill_opacity=0.14, radius=0.06)
            for i in range(1, 6)
        ]).arrange(RIGHT, buff=0.07).move_to(RIGHT * 4.55 + UP * 0.45)
        h_label = VGroup(
            self.text("Tokens for the LLM", self.language, 15, 2.3, weight=BOLD),
            MathTex(r"H_v", font_size=28, color=self.language),
        ).arrange(DOWN, buff=0.05).next_to(h_tokens, DOWN, buff=0.18)

        arrows = VGroup(
            Arrow(z_vec.get_right(), ln.get_left(), buff=0.16, color=self.orange, stroke_width=4),
            Arrow(ln.get_right(), mlp.get_left(), buff=0.16, color=self.connector, stroke_width=4),
            Arrow(mlp.get_right(), h_tokens.get_left(), buff=0.16, color=self.language, stroke_width=4),
        )
        formula = MathTex(r"H_v=\mathrm{MLP}(\mathrm{LN}(Z_v))", font_size=38)
        formula.set_color_by_tex(r"H_v", self.language)
        formula.set_color_by_tex(r"Z_v", self.visual)
        formula.to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.85)
        self.play(FadeIn(z_vec, shift=UP * 0.08), FadeIn(z_label, shift=UP * 0.08), run_time=0.9)
        self.play(GrowArrow(arrows[0]), DrawBorderThenFill(ln), FadeIn(ln_note, shift=UP * 0.08), run_time=1.0)
        self.play(GrowArrow(arrows[1]), DrawBorderThenFill(mlp), FadeIn(mlp_note, shift=UP * 0.08), run_time=1.0)
        self.play(GrowArrow(arrows[2]), TransformFromCopy(z_vec, h_tokens), FadeIn(h_label, shift=UP * 0.08), run_time=1.2)
        self.play(Write(formula), Circumscribe(mlp, color=self.connector), run_time=1.1)
        self.wait(0.45)
        self.cleanup(title, z_vec, z_label, ln, ln_note, mlp, mlp_note, h_tokens, h_label, arrows, formula)

    def prompt_tile(self, label, path):
        image = self.image_card(path, width=2.55, height=1.55, color=self.visual)
        label_box = self.card(3.05, 0.62, self.orange, self.text(label, WHITE, 15, 2.85, weight=BOLD, line_spacing=0.84), fill_opacity=0.13, radius=0.08)
        return Group(image, label_box).arrange(DOWN, buff=0.08)

    def scene_prompt_types(self):
        title = self.make_title("8 Visual Prompt Types Supported by ViP-LLaVA", self.connector)
        tiles = Group(*[self.prompt_tile(label, path) for label, path in PROMPT_IMAGES.items()])
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.28)).scale(0.96).move_to(DOWN * 0.05)
        note = self.card(
            9.2,
            0.52,
            self.language,
            self.text("Prompts can vary by shape, color, transparency, stroke width, and direction.", WHITE, 16, 8.75, weight=BOLD),
            fill_opacity=0.13,
        ).to_edge(DOWN, buff=0.3)

        self.play(Write(title), run_time=0.8)
        for row in [tiles[:4], tiles[4:]]:
            self.play(LaggedStart(*[FadeIn(tile, scale=0.96) for tile in row], lag_ratio=0.1), run_time=1.25)
        self.play(FadeIn(note, shift=UP * 0.08), Circumscribe(tiles[6], color=self.connector), run_time=1.0)
        self.wait(0.45)
        self.cleanup(title, tiles, note)

    def scene_region_question(self):
        title = self.make_title("Same Image, Different Prompt -> Different Answer")
        image = self.mini_image_scene(with_prompt=False).scale(1.15).move_to(LEFT * 3.65 + UP * 0.15)
        circle_center = image[2][1].get_center()
        triangle_center = image[2][3].get_center()
        arrow_a = Arrow(circle_center + UP * 0.9, circle_center, color=self.connector, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.25)
        arrow_b = Arrow(triangle_center + UP * 0.86, triangle_center, color=self.connector, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.25)
        question = self.card(
            4.7,
            0.72,
            self.connector,
            self.text("What is the marked object\ndoing?", BLACK, 19, 4.3, weight=BOLD, line_spacing=0.9),
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.35 + UP * 1.35)
        answer_a = self.card(
            4.7,
            0.72,
            self.language,
            self.text("Answer A: focuses on the left region.", WHITE, 18, 4.25, weight=BOLD),
            fill_opacity=0.14,
        ).next_to(question, DOWN, buff=0.28)
        answer_b = self.card(
            4.7,
            0.72,
            self.visual,
            self.text("Answer B: changes with the indicated region.", WHITE, 17, 4.25, weight=BOLD),
            fill_opacity=0.14,
        ).move_to(answer_a)
        insight = self.card(
            8.6,
            0.55,
            self.orange,
            self.text("A visual prompt is not decoration. It makes the question spatially specific.", WHITE, 17, 8.1, weight=BOLD),
            fill_opacity=0.13,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), FadeIn(question, shift=LEFT * 0.08), run_time=1.0)
        self.play(GrowArrow(arrow_a), FadeIn(answer_a, shift=UP * 0.08), run_time=0.9)
        self.play(ReplacementTransform(arrow_a, arrow_b), ReplacementTransform(answer_a, answer_b), run_time=1.0)
        self.play(FadeIn(insight, shift=UP * 0.08), Circumscribe(question, color=self.connector), run_time=1.0)
        self.wait(0.4)
        self.cleanup(title, image, arrow_b, question, answer_b, insight)

    def scene_final_insight(self):
        title = self.make_title("Visual Prompt = Spatial Instruction", self.connector)
        text_prompt = self.card(
            4.35,
            1.25,
            self.visual,
            VGroup(
                self.text("Text instruction", self.visual, 21, 3.8, weight=BOLD),
                self.text("Describe the object\ninside the red box.", WHITE, 18, 3.6, line_spacing=0.88),
            ).arrange(DOWN, buff=0.14),
            fill_opacity=0.1,
        ).move_to(LEFT * 3.2 + UP * 0.6)
        visual_prompt = self.card(
            4.35,
            1.25,
            self.connector,
            VGroup(
                self.text("Visual instruction", BLACK, 21, 3.8, weight=BOLD),
                self.text("Point, circle, or draw\ndirectly on the image.", BLACK, 17, 3.6, line_spacing=0.88),
            ).arrange(DOWN, buff=0.14),
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.2 + UP * 0.6)
        llm = self.card(
            2.4,
            1.1,
            self.language,
            self.text("LLM\nreasoning", WHITE, 18, 2.0, weight=BOLD, line_spacing=0.86),
            fill_opacity=0.14,
        ).move_to(DOWN * 1.05)
        arrows = VGroup(
            Arrow(text_prompt.get_bottom(), llm.get_left() + UP * 0.12, color=self.visual, stroke_width=4, buff=0.1),
            Arrow(visual_prompt.get_bottom(), llm.get_right() + UP * 0.12, color=self.connector, stroke_width=4, buff=0.1),
        )
        final = self.card(
            8.6,
            0.62,
            self.language,
            self.text("More natural than coordinates. More specific than whole-image captions.", WHITE, 21, 8.0, weight=BOLD),
            fill_opacity=0.16,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(text_prompt, shift=RIGHT * 0.1), FadeIn(visual_prompt, shift=LEFT * 0.1), run_time=1.0)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(llm, scale=0.96), run_time=1.0)
        self.play(FadeIn(final, shift=UP * 0.08), Circumscribe(title, color=self.connector), run_time=1.1)
        self.wait(0.6)
        self.cleanup(title, text_prompt, visual_prompt, llm, arrows, final)

    def scene_left_right_example(self):
        title = self.make_title("Example: Change the Arrow, Change the Answer")
        question = self.card(
            7.9,
            0.54,
            self.connector,
            self.text("Describe the instance pointed to by the red arrow.", BLACK, 20, 7.35, weight=BOLD),
            fill_opacity=0.9,
        ).next_to(title, DOWN, buff=0.22)

        left_image = self.image_card(LEFT_EXAMPLE_IMAGE, width=5.15, height=3.55, color=self.visual)
        right_image = self.image_card(RIGHT_EXAMPLE_IMAGE, width=5.15, height=3.55, color=self.orange)
        examples = Group(left_image, right_image).arrange(RIGHT, buff=0.36).move_to(UP * 0.08)

        left_label = self.card(
            4.95,
            0.52,
            self.visual,
            self.text("Left prompt: the person in blue.", WHITE, 16, 4.55, weight=BOLD),
            fill_opacity=0.14,
            radius=0.08,
        ).next_to(left_image, DOWN, buff=0.16)
        right_label = self.card(
            4.95,
            0.52,
            self.orange,
            self.text("Right prompt: the person in white.", WHITE, 16, 4.55, weight=BOLD),
            fill_opacity=0.14,
            radius=0.08,
        ).next_to(right_image, DOWN, buff=0.16)

        insight = self.card(
            9.4,
            0.58,
            self.language,
            self.text("With the same question, the visual prompt decides which region the model describes.", WHITE, 18, 8.9, weight=BOLD),
            fill_opacity=0.16,
        ).to_edge(DOWN, buff=0.36)

        self.play(Write(title), FadeIn(question, shift=DOWN * 0.08), run_time=0.95)
        self.play(FadeIn(left_image, scale=0.96), FadeIn(left_label, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(right_image, scale=0.96), FadeIn(right_label, shift=UP * 0.08), run_time=1.0)
        self.play(Circumscribe(left_image, color=self.visual), run_time=0.75)
        self.play(Circumscribe(right_image, color=self.orange), run_time=0.75)
        self.play(FadeIn(insight, shift=UP * 0.08), run_time=0.85)
        self.wait(0.6)
