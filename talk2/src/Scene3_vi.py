from manim import *


TEXT_FONT = "Times New Roman"
MONO_FONT = "Times New Roman"

TIME_SCALE = 2.5


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


class Scene3(ScaledTimingMixin, MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK

        self.visual_color = "#58C4DD"
        self.language_color = "#83C167"
        self.connector_color = "#FFFF00"
        self.frozen_color = "#888888"
        self.warning_color = "#FF6666"
        self.panel_fill = "#071018"

        self.opening_question()
        self.overview_pipeline()
        self.vision_encoder_flow()
        self.projector_bridge()
        self.instruction_embedding()
        self.llm_generation()
        self.training_stage_1()
        self.training_stage_2()
        self.training_table()

    def make_title(self, text, color=WHITE):
        title = Text(text, font=TEXT_FONT, font_size=31, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.32)
        underline = Line(LEFT, RIGHT).set_width(min(7.7, title.width * 0.95))
        underline.next_to(title, DOWN, buff=0.12)
        underline.set_color_by_gradient(self.visual_color, self.connector_color, self.language_color)
        return VGroup(title, underline)

    def glass_panel(self, width, height, color, label, label_color=WHITE, font_size=17):
        rect = RoundedRectangle(
            corner_radius=0.14,
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=2,
            fill_color=color,
            fill_opacity=0.18,
        )
        glow = rect.copy().set_stroke(WHITE, width=0.75, opacity=0.2).scale(1.02)
        if isinstance(label, Mobject):
            content = label
        else:
            content = Text(label, font=TEXT_FONT, font_size=font_size, color=label_color, line_spacing=1.05)
        content.move_to(rect)
        return VGroup(rect, glow, content)

    def small_label(self, text, color=GREY_B, font_size=13):
        return Text(text, font=TEXT_FONT, font_size=font_size, color=color, line_spacing=1.05)

    def label_with_math(self, text, latex, color=WHITE, text_size=13, math_size=26):
        label = Text(text, font=TEXT_FONT, font_size=text_size, color=color, line_spacing=1.05)
        formula = MathTex(latex, font_size=math_size, color=color)
        return VGroup(label, formula).arrange(DOWN, buff=0.06)

    def math_only_label(self, latex, color=WHITE, font_size=28):
        return MathTex(latex, font_size=font_size, color=color)

    def token(self, text, color, width=None, font_size=13):
        font_size = max(font_size, 14)
        if width is None:
            width = max(0.68, 0.22 * len(text) + 0.36)
        rect = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=0.48,
            stroke_color=color,
            stroke_width=1.4,
            fill_color=color,
            fill_opacity=0.18,
        )
        label = Text(text, font=MONO_FONT, font_size=font_size, color=WHITE)
        if label.width > rect.width * 0.84:
            label.set_width(rect.width * 0.84)
        label.move_to(rect)
        return VGroup(rect, label)

    def math_token(self, latex, color, width=None, font_size=22):
        if width is None:
            width = max(0.62, 0.22 * len(latex) + 0.22)
        rect = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=0.42,
            stroke_color=color,
            stroke_width=1.4,
            fill_color=color,
            fill_opacity=0.18,
        )
        label = MathTex(latex, font_size=font_size, color=WHITE)
        if label.width > rect.width * 0.82:
            label.set_width(rect.width * 0.82)
        label.move_to(rect)
        return VGroup(rect, label)

    def token_stream(self, labels, color, font_size=13, buff=0.08):
        stream = VGroup(*[self.token(label, color, font_size=font_size) for label in labels])
        stream.arrange(RIGHT, buff=buff)
        return stream

    def math_token_stream(self, labels, color, font_size=22, buff=0.08):
        stream = VGroup(*[self.math_token(label, color, font_size=font_size) for label in labels])
        stream.arrange(RIGHT, buff=buff)
        return stream

    def make_patch_grid(self, size=2.0, rows=4, cols=4):
        patches = VGroup()
        cell_w = size / cols
        cell_h = size / rows
        for r in range(rows):
            for c in range(cols):
                shade = interpolate_color(BLUE_E, ManimColor(self.visual_color), (r + c) / (rows + cols - 2))
                sq = Square(side_length=min(cell_w, cell_h) * 0.92)
                sq.set_fill(shade, opacity=0.55)
                sq.set_stroke(WHITE, width=0.8, opacity=0.35)
                patches.add(sq)
        patches.arrange_in_grid(rows=rows, cols=cols, buff=0.02)
        return patches

    def make_vector_bars(self, count=8, color=None):
        color = color or self.visual_color
        bars = VGroup()
        heights = [0.62, 0.98, 0.72, 1.2, 0.86, 0.52, 1.08, 0.78]
        for i in range(count):
            bar = RoundedRectangle(
                corner_radius=0.04,
                width=0.13,
                height=heights[i % len(heights)],
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.85,
            )
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        return bars

    def make_column_vector(self, entries=None, color=None, font_size=28):
        color = color or self.visual_color
        entries = entries or [r"+1.0", r"-8.9", r"+1.5", r"-7.1", r"\vdots", r"+3.9"]
        vector = MathTex(
            r"\begin{bmatrix}" + r"\\".join(entries) + r"\end{bmatrix}",
            font_size=font_size,
            color=color,
        )
        frame = RoundedRectangle(
            corner_radius=0.08,
            width=vector.width + 0.42,
            height=vector.height + 0.34,
            stroke_color=color,
            stroke_width=1.8,
            fill_color=color,
            fill_opacity=0.08,
        )
        vector.move_to(frame)
        return VGroup(frame, vector)

    def flow_dot(self, path, color=YELLOW, radius=0.055, run_time=0.95):
        dot = Dot(path.get_start(), radius=radius, color=color)
        return Succession(
            FadeIn(dot, scale=0.4, run_time=0.12),
            MoveAlongPath(dot, path, rate_func=smooth, run_time=run_time),
            FadeOut(dot, scale=0.4, run_time=0.12),
        )

    def lock_label(self, text="frozen"):
        tag = RoundedRectangle(
            corner_radius=0.06,
            width=1.2,
            height=0.34,
            fill_color="#2a2a2a",
            fill_opacity=0.95,
            stroke_color=self.frozen_color,
            stroke_width=1.2,
        )
        label = Text(text, font=TEXT_FONT, font_size=15, color=GREY_B)
        label.move_to(tag)
        return VGroup(tag, label)

    def train_label(self, text="trained"):
        tag = RoundedRectangle(
            corner_radius=0.06,
            width=1.2,
            height=0.34,
            fill_color="#2a2300",
            fill_opacity=0.95,
            stroke_color=self.connector_color,
            stroke_width=1.2,
        )
        label = Text(text, font=TEXT_FONT, font_size=15, color=self.connector_color)
        label.move_to(tag)
        return VGroup(tag, label)

    def formula_tex(self, latex, color=WHITE, font_size=34, max_width=11.5):
        formula = MathTex(latex, font_size=font_size, color=color)
        if formula.width > max_width:
            formula.set_width(max_width)
        return formula

    def make_pipeline(self, y=0.12, scale=1.0):
        labels = [
            (self.label_with_math("Image", r"X_v", self.visual_color, 13, 25), self.visual_color, 1.35),
            ("CLIP\nViT-L/14", self.visual_color, 1.55),
            (self.math_only_label(r"Z_v", self.visual_color, 28), self.visual_color, 1.0),
            (self.math_only_label(r"W/\mathrm{MLP}", BLACK, 24), self.connector_color, 1.32),
            (self.math_only_label(r"H_v", self.visual_color, 28), self.visual_color, 1.0),
            (self.label_with_math("LLM", r"f_{\phi}", self.language_color, 13, 24), self.language_color, 1.32),
            (self.label_with_math("Answer", r"X_a", self.language_color, 13, 25), self.language_color, 1.35),
        ]
        nodes = VGroup()
        for label, color, width in labels:
            nodes.add(self.glass_panel(width, 0.78, color, label, font_size=14))
        nodes.arrange(RIGHT, buff=0.32).move_to(UP * y).scale(scale)

        arrows = VGroup()
        for left, right in zip(nodes[:-1], nodes[1:]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.08, color=GREY_B, stroke_width=3))

        instruction_label = VGroup(
            Text("Instruction", font=TEXT_FONT, font_size=15, color=self.language_color),
            MathTex(r"X_q", font_size=24, color=self.language_color),
        ).arrange(RIGHT, buff=0.12)
        instruction = self.glass_panel(2.05, 0.55, self.language_color, instruction_label, font_size=13)
        instruction.next_to(nodes[5], DOWN, buff=0.78)
        instruction_arrow = Arrow(instruction.get_top(), nodes[5].get_bottom(), buff=0.12, color=self.language_color, stroke_width=3)

        return VGroup(nodes, arrows, instruction, instruction_arrow)

    def transition_out(self, *mobjects, shift=UP * 0.18):
        self.play(FadeOut(VGroup(*mobjects), shift=shift), run_time=0.9)

    def opening_question(self):
        title = self.make_title("LLaVA: How Can an LLM See an Image?", self.connector_color)
        image_box = RoundedRectangle(
            corner_radius=0.12,
            width=2.45,
            height=1.55,
            stroke_color=self.visual_color,
            stroke_width=2,
            fill_color="#102c3a",
            fill_opacity=0.7,
        ).move_to(LEFT * 4.55 + DOWN * 0.1)
        image_grid = self.make_patch_grid(size=1.18, rows=3, cols=3).move_to(image_box)
        image_label = Text("Image", font=TEXT_FONT, font_size=21, color=self.visual_color, weight=BOLD)
        image_label.next_to(image_box, UP, buff=0.18)
        image_group = VGroup(image_box, image_grid, image_label)

        llm = self.glass_panel(2.35, 1.24, self.language_color, "LLM\nreads tokens only", font_size=18)
        llm.move_to(RIGHT * 4.55 + DOWN * 0.1)

        text_tokens = self.token_stream(["What", "is", "odd", "?"], self.language_color, font_size=14)
        text_tokens.move_to(UP * 1.28)
        text_arrow = Arrow(text_tokens.get_right(), llm.get_left() + UP * 0.42, buff=0.15, color=self.language_color, stroke_width=3)
        blocked_y = -0.62
        blocked_arrow = Arrow(
            [image_box.get_right()[0] + 0.18, blocked_y, 0],
            [llm.get_left()[0] - 0.18, blocked_y, 0],
            buff=0,
            color=self.warning_color,
            stroke_width=4,
        )
        barrier = VGroup(
            Line(UP * 0.32, DOWN * 0.32, color=self.warning_color, stroke_width=8),
            Line(UP * 0.32, DOWN * 0.32, color=self.warning_color, stroke_width=8).rotate(PI / 2),
        ).move_to(blocked_arrow.get_center())
        question = VGroup(
            Text("Image", font=TEXT_FONT, font_size=32, color=WHITE, weight=BOLD),
            MathTex(r"\rightarrow", font_size=34, color=self.connector_color),
            Text("?", font=TEXT_FONT, font_size=34, color=self.connector_color, weight=BOLD),
            MathTex(r"\rightarrow", font_size=34, color=self.connector_color),
            Text("Language", font=TEXT_FONT, font_size=32, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.18)
        question.next_to(text_tokens, DOWN, buff=0.75)

        self.play(LaggedStart(Write(title), FadeIn(image_group, shift=RIGHT * 0.2), DrawBorderThenFill(llm), lag_ratio=0.22), run_time=2.0)
        self.play(FadeIn(text_tokens, shift=DOWN * 0.18), GrowArrow(text_arrow), run_time=1.1)
        self.play(GrowArrow(blocked_arrow), FadeIn(barrier, scale=1.25), run_time=1.0)
        self.play(Write(question), Flash(barrier, color=self.warning_color, flash_radius=0.55), run_time=1.4)
        self.wait(0.7)
        self.transition_out(title, image_group, llm, text_tokens, text_arrow, blocked_arrow, barrier, question)

    def overview_pipeline(self):
        title = self.make_title("LLaVA at a Glance")
        pipeline = self.make_pipeline(y=-0.1, scale=0.96)
        nodes, arrows, instruction, instruction_arrow = pipeline
        note_parts = ["Image", "CLIP", "projector", "visual tokens", "LLM", "answer"]
        note = VGroup()
        for idx, part in enumerate(note_parts):
            note.add(Text(part, font=TEXT_FONT, font_size=18, color=GREY_B))
            if idx < len(note_parts) - 1:
                note.add(MathTex(r"\rightarrow", font_size=22, color=self.connector_color))
        note.arrange(RIGHT, buff=0.12).next_to(pipeline, DOWN, buff=0.65)

        self.play(Write(title), run_time=0.9)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(node) for node in nodes],
                *[GrowArrow(arrow) for arrow in arrows],
                lag_ratio=0.12,
            ),
            AnimationGroup(
                DrawBorderThenFill(instruction),
                GrowArrow(instruction_arrow),
                lag_ratio=0.15,
            ),
            run_time=3.2,
        )
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.9)
        self.play(
            LaggedStart(*[self.flow_dot(arrow, color=self.connector_color, run_time=0.55) for arrow in arrows], lag_ratio=0.15),
            Circumscribe(nodes[3], color=self.connector_color, fade_out=True),
            run_time=2.0,
        )
        self.wait(0.6)
        self.transition_out(title, pipeline, note)

    def vision_encoder_flow(self):
        title = self.make_title("Vision Encoder: Turning Images into Features")
        patches = self.make_patch_grid(size=2.15, rows=4, cols=4).move_to(LEFT * 4.3 + DOWN * 0.15)
        patch_label = self.label_with_math("Image and ViT patches", r"X_v", self.visual_color, 15, 25).next_to(patches, DOWN, buff=0.25)
        encoder_label = VGroup(
            Text("CLIP-ViT-L/14", font=TEXT_FONT, font_size=17, color=self.visual_color, weight=BOLD),
            MathTex(r"g_{\theta}", font_size=28, color=self.visual_color),
        ).arrange(DOWN, buff=0.05)
        encoder = self.glass_panel(2.35, 1.05, self.visual_color, encoder_label, font_size=18)
        encoder.move_to(LEFT * 0.65 + DOWN * 0.08)
        frozen = self.lock_label().next_to(encoder, UP, buff=0.18)
        bars = self.make_column_vector(
            [r"z1", r"z2", r"z3", r"z4", r"z5", r"\vdots", r"z7"],
            self.visual_color,
            font_size=25,
        ).move_to(RIGHT * 3.75 + DOWN * 0.08)
        bars_label = self.label_with_math("Visual feature vectors", r"Z_v", self.visual_color, 15, 27).next_to(bars, DOWN, buff=0.2)
        arrow_1 = Arrow(patches.get_right(), encoder.get_left(), buff=0.16, color=self.visual_color, stroke_width=4)
        arrow_2 = Arrow(encoder.get_right(), bars.get_left(), buff=0.16, color=self.visual_color, stroke_width=4)
        formula = self.formula_tex(r"Z_v = g_{\theta}(X_v)", self.connector_color, 36).to_edge(DOWN, buff=0.55)

        self.play(Write(title), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in patches], lag_ratio=0.035), FadeIn(patch_label), run_time=1.4)
        self.play(GrowArrow(arrow_1), DrawBorderThenFill(encoder), FadeIn(frozen, shift=DOWN * 0.08), run_time=1.2)
        self.play(GrowArrow(arrow_2), TransformFromCopy(patches, bars), FadeIn(bars_label, shift=UP * 0.1), run_time=1.5)
        self.play(Write(formula), Circumscribe(bars, color=self.visual_color, fade_out=True), run_time=1.3)
        self.wait(0.7)
        self.transition_out(title, patches, patch_label, encoder, frozen, bars, bars_label, arrow_1, arrow_2, formula)

    def projector_bridge(self):
        title = self.make_title("Projector: Bridging Two Spaces")
        visual_plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3.25,
            y_length=2.35,
            background_line_style={"stroke_color": self.visual_color, "stroke_width": 1, "stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0.25},
        ).move_to(LEFT * 4.15 + DOWN * 0.25)
        lang_plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3.25,
            y_length=2.35,
            background_line_style={"stroke_color": self.language_color, "stroke_width": 1, "stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0.25},
        ).move_to(RIGHT * 4.15 + DOWN * 0.25)
        visual_label = self.label_with_math("visual space", r"Z_v", self.visual_color, 14, 25).next_to(visual_plane, DOWN, buff=0.16)
        lang_label = self.label_with_math("language embedding space", r"H_v", self.language_color, 12, 25).next_to(lang_plane, DOWN, buff=0.16)

        visual_dots = VGroup(
            Dot(visual_plane.c2p(-1.2, 0.75), color=self.visual_color),
            Dot(visual_plane.c2p(-0.7, -0.42), color=self.visual_color),
            Dot(visual_plane.c2p(0.2, 0.28), color=self.visual_color),
            Dot(visual_plane.c2p(0.9, -0.82), color=self.visual_color),
            Dot(visual_plane.c2p(1.28, 0.65), color=self.visual_color),
        )
        target_dots = VGroup(
            Dot(lang_plane.c2p(-1.05, -0.38), color=self.language_color),
            Dot(lang_plane.c2p(-0.34, 0.65), color=self.language_color),
            Dot(lang_plane.c2p(0.32, -0.72), color=self.language_color),
            Dot(lang_plane.c2p(0.84, 0.32), color=self.language_color),
            Dot(lang_plane.c2p(1.22, -0.1), color=self.language_color),
        )
        projector = self.glass_panel(1.45, 1.0, self.connector_color, "W", label_color=BLACK, font_size=30).move_to(DOWN * 0.25)
        arrow_in = Arrow(visual_plane.get_right(), projector.get_left(), buff=0.18, color=self.connector_color, stroke_width=4)
        arrow_out = Arrow(projector.get_right(), lang_plane.get_left(), buff=0.18, color=self.connector_color, stroke_width=4)
        formula = self.formula_tex(r"H_v = W\,Z_v", self.connector_color, 36).to_edge(DOWN, buff=0.65)
        formula_mlp = self.formula_tex(r"\text{LLaVA-1.5:}\quad H_v = \mathrm{MLP}(Z_v)", self.language_color, 28).next_to(formula, UP, buff=0.2)

        self.play(Write(title), run_time=0.9)
        self.play(Create(visual_plane), FadeIn(visual_label), LaggedStart(*[GrowFromCenter(dot) for dot in visual_dots], lag_ratio=0.12), run_time=1.6)
        self.play(GrowArrow(arrow_in), DrawBorderThenFill(projector), GrowArrow(arrow_out), Create(lang_plane), FadeIn(lang_label), run_time=1.4)
        self.play(
            LaggedStart(*[TransformFromCopy(src, dst) for src, dst in zip(visual_dots, target_dots)], lag_ratio=0.15),
            Write(formula),
            run_time=1.9,
        )
        mlp_box = self.glass_panel(1.7, 1.0, self.connector_color, "MLP", label_color=BLACK, font_size=24).move_to(projector)
        self.play(ReplacementTransform(projector, mlp_box), FadeIn(formula_mlp, shift=UP * 0.12), run_time=1.2)
        self.play(Circumscribe(mlp_box, color=self.connector_color, fade_out=True), run_time=1.0)
        self.wait(0.7)
        self.transition_out(title, visual_plane, lang_plane, visual_label, lang_label, visual_dots, target_dots, mlp_box, arrow_in, arrow_out, formula, formula_mlp)

    def instruction_embedding(self):
        title = self.make_title("Instructions Become Embeddings Too")
        question = Text("What is unusual about this image?", font=TEXT_FONT, font_size=28, color=WHITE)
        question.move_to(UP * 1.72)
        token_labels = ["What", "is", "unusual", "in", "this", "image", "?"]
        tokens = self.token_stream(token_labels, self.language_color, font_size=14, buff=0.07)
        tokens.next_to(question, DOWN, buff=0.42)
        vectors = self.make_column_vector(
            [r"h_1", r"h_2", r"h_3", r"\vdots", r"h_m"],
            self.language_color,
            font_size=27,
        )
        vectors.scale(0.74).next_to(tokens, DOWN, buff=0.38)
        formula = self.formula_tex(r"H_q = \mathrm{Emb}(X_q)", self.language_color, 31).next_to(vectors, DOWN, buff=0.18)

        visual_tokens = self.token_stream(["<img1>", "<img2>", "<img3>", "..."], self.visual_color, font_size=14, buff=0.07)
        question_tokens = self.token_stream(["What", "is", "odd", "?"], self.language_color, font_size=14, buff=0.07)
        plus = Text("+", font=TEXT_FONT, font_size=26, color=self.connector_color)
        prompt_stream = VGroup(visual_tokens, plus, question_tokens).arrange(RIGHT, buff=0.14)
        prompt_stream.scale(0.72).move_to(DOWN * 3.12)
        bracket_label = self.formula_tex(r"[\,H_v\,;\,H_q\,]", self.connector_color, 24).next_to(prompt_stream, UP, buff=0.08)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(question, shift=DOWN * 0.15), run_time=0.8)
        self.play(LaggedStart(*[TransformFromCopy(question, token) for token in tokens], lag_ratio=0.08), run_time=1.4)
        self.play(TransformFromCopy(tokens, vectors), Write(formula), run_time=1.5)
        self.play(FadeIn(prompt_stream, shift=UP * 0.16), FadeIn(bracket_label, shift=UP * 0.08), run_time=1.1)
        self.play(Circumscribe(prompt_stream, color=self.connector_color, fade_out=True), run_time=1.1)
        self.wait(0.6)
        self.transition_out(title, question, tokens, vectors, formula, prompt_stream, bracket_label)

    def llm_generation(self):
        title = self.make_title("Token-by-Token Generation")
        prompt = self.token_stream(["<image>", "What", "is unusual?"], self.connector_color, font_size=14, buff=0.06)
        llm_label = VGroup(
            Text("LLM", font=TEXT_FONT, font_size=22, color=self.language_color, weight=BOLD),
            MathTex(r"f_{\phi}", font_size=30, color=self.language_color),
        ).arrange(DOWN, buff=0.05)
        llm = self.glass_panel(2.15, 1.15, self.language_color, llm_label, font_size=22).move_to(ORIGIN + UP * 0.2)
        output_tokens = self.token_stream(["The", "unusual", "thing", "is", "..."], self.language_color, font_size=14, buff=0.07)
        max_stream_width = 4.65
        if prompt.width > max_stream_width:
            prompt.set_width(max_stream_width)
        if output_tokens.width > max_stream_width:
            output_tokens.set_width(max_stream_width)

        prompt.next_to(llm, LEFT, buff=0.42).align_to(llm, UP).shift(UP * 0.08)
        output_tokens.next_to(llm, RIGHT, buff=0.42).align_to(llm, UP).shift(UP * 0.08)

        safe_left = -6.55
        safe_right = 6.55
        if prompt.get_left()[0] < safe_left:
            prompt.shift(RIGHT * (safe_left - prompt.get_left()[0]))
        if output_tokens.get_right()[0] > safe_right:
            output_tokens.shift(LEFT * (output_tokens.get_right()[0] - safe_right))
        arrow_in = Arrow(prompt.get_right(), llm.get_left(), buff=0.12, color=self.connector_color, stroke_width=4, max_tip_length_to_length_ratio=0.18)
        arrow_out = Arrow(llm.get_right(), output_tokens.get_left(), buff=0.12, color=self.language_color, stroke_width=4, max_tip_length_to_length_ratio=0.18)
        short_formula = self.formula_tex(r"X_a = f_{\phi}(H_v, H_q)", self.language_color, 34).move_to(DOWN * 1.38)
        prob_formula = self.formula_tex(
            r"p(X_a \mid X_v, X_q) = \prod_t p_{\phi}(x_t \mid H_v, H_q, x_{<t})",
            WHITE,
            26,
        )
        prob_formula.next_to(short_formula, DOWN, buff=0.28)

        bars = VGroup()
        for height in [0.62, 0.36, 0.92, 0.48]:
            bars.add(Rectangle(width=0.34, height=height, fill_color=self.language_color, fill_opacity=0.75, stroke_width=0))
        bars.arrange(RIGHT, aligned_edge=DOWN, buff=0.14)
        dist_label = Text("next-token probabilities", font=TEXT_FONT, font_size=15, color=GREY_B)
        distribution = VGroup(dist_label, bars).arrange(DOWN, buff=0.12).next_to(output_tokens, DOWN, buff=0.34)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(prompt, shift=RIGHT * 0.2), GrowArrow(arrow_in), DrawBorderThenFill(llm), run_time=1.2)
        self.play(GrowArrow(arrow_out), LaggedStart(*[FadeIn(tok, shift=RIGHT * 0.22) for tok in output_tokens], lag_ratio=0.22), run_time=1.6)
        self.play(Write(short_formula), run_time=0.9)
        self.play(FadeIn(prob_formula, shift=UP * 0.1), FadeIn(dist_label, shift=UP * 0.05), LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.12), run_time=1.6)
        self.play(Indicate(output_tokens[1], color=self.connector_color), Circumscribe(llm, color=self.language_color, fade_out=True), run_time=1.2)
        self.wait(0.6)
        self.transition_out(title, prompt, llm, output_tokens, arrow_in, arrow_out, short_formula, prob_formula, distribution)

    def training_stage_1(self):
        title = self.make_title("Stage 1: Pretraining to Align Features")
        pipeline = self.make_pipeline(y=1.08, scale=0.83)
        nodes = pipeline[0]
        arrows = pipeline[1]
        instruction = pipeline[2]
        instruction_arrow = pipeline[3]
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(VGroup(nodes, arrows, instruction, instruction_arrow), shift=DOWN * 0.15), run_time=1.0)

        frozen_vision = self.lock_label().next_to(nodes[1], UP, buff=0.12)
        train_projector = self.train_label().next_to(nodes[3], UP, buff=0.12)
        frozen_llm = self.lock_label().next_to(nodes[5], UP, buff=0.12)

        data_cards = VGroup()
        for i in range(3):
            image_card = RoundedRectangle(
                corner_radius=0.08,
                width=1.15,
                height=0.62,
                fill_color=self.visual_color,
                fill_opacity=0.2,
                stroke_color=self.visual_color,
                stroke_width=1.3,
            )
            caption_card = RoundedRectangle(
                corner_radius=0.08,
                width=1.75,
                height=0.62,
                fill_color=self.language_color,
                fill_opacity=0.18,
                stroke_color=self.language_color,
                stroke_width=1.3,
            )
            img_text = Text("image", font=TEXT_FONT, font_size=14, color=WHITE).move_to(image_card)
            cap_text = Text("caption", font=TEXT_FONT, font_size=14, color=WHITE).move_to(caption_card)
            pair = VGroup(VGroup(image_card, img_text), VGroup(caption_card, cap_text)).arrange(RIGHT, buff=0.12)
            data_cards.add(pair)
        data_cards.arrange(DOWN, buff=0.16).move_to(LEFT * 4.6 + DOWN * 1.22)
        dataset_label = Text("CC3M subset ~595K", font=TEXT_FONT, font_size=19, color=self.visual_color, weight=BOLD)
        dataset_label.next_to(data_cards, UP, buff=0.22)
        loss = self.formula_tex(
            r"\mathcal{L}_{\mathrm{align}} = -\sum_t \log p_{\phi}(y_t \mid H_v, y_{<t})",
            WHITE,
            27,
        )
        loss.move_to(DOWN * 3.05)
        key = Text("Only projector W is updated", font=TEXT_FONT, font_size=23, color=self.connector_color, weight=BOLD)
        key.next_to(loss, UP, buff=0.22)

        self.play(FadeIn(frozen_vision), FadeIn(train_projector), FadeIn(frozen_llm), run_time=0.9)
        self.play(FadeIn(dataset_label, shift=DOWN * 0.1), LaggedStart(*[FadeIn(card, shift=RIGHT * 0.15) for card in data_cards], lag_ratio=0.14), run_time=1.5)
        self.play(Write(key), FadeIn(loss, shift=UP * 0.1), Circumscribe(nodes[3], color=self.connector_color, fade_out=True), run_time=1.5)
        self.wait(0.7)
        self.transition_out(title, pipeline, frozen_vision, train_projector, frozen_llm, data_cards, dataset_label, loss, key)

    def training_stage_2(self):
        title = self.make_title("Stage 2: Visual Instruction Tuning")
        pipeline = self.make_pipeline(y=1.12, scale=0.83)
        nodes = pipeline[0]
        arrows = pipeline[1]
        instruction = pipeline[2]
        instruction_arrow = pipeline[3]
        instruction.next_to(nodes[5], DOWN, buff=0.5)
        instruction_arrow.become(Arrow(instruction.get_top(), nodes[5].get_bottom(), buff=0.1, color=self.language_color, stroke_width=3))
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(VGroup(nodes, arrows, instruction, instruction_arrow), shift=DOWN * 0.15), run_time=1.0)

        frozen_vision = self.lock_label().next_to(nodes[1], UP, buff=0.12)
        train_projector = self.train_label().next_to(nodes[3], UP, buff=0.12)
        train_llm = self.train_label().next_to(nodes[5], UP, buff=0.12)

        triplet = VGroup()
        specs = [
            ("Image", self.visual_color, 1.25),
            ("Instruction", self.connector_color, 1.85),
            ("Answer", self.language_color, 1.5),
        ]
        for label, color, width in specs:
            card = RoundedRectangle(
                corner_radius=0.1,
                width=width,
                height=0.76,
                fill_color=color,
                fill_opacity=0.18,
                stroke_color=color,
                stroke_width=1.7,
            )
            text = Text(label, font=TEXT_FONT, font_size=15, color=WHITE, weight=BOLD).move_to(card)
            triplet.add(VGroup(card, text))
        triplet.arrange(RIGHT, buff=0.18).move_to(LEFT * 4 + DOWN * 1.18)
        triplet_label = Text("LLaVA-Instruct-158K", font=TEXT_FONT, font_size=22, color=self.language_color, weight=BOLD)
        triplet_label.next_to(triplet, UP, buff=0.25)

        tasks = VGroup(
            self.task_card("Conversation", "dialogue", self.visual_color),
            self.task_card("Description", "captioning", self.language_color),
            self.task_card("Reasoning", "complex QA", ORANGE),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 4.85 + DOWN * 1.57)

        loss = self.formula_tex(
            r"\mathcal{L}_{\mathrm{inst}} = -\sum_t \log p_{\phi}(x_t^a \mid H_v, H_q, x_{<t}^a)",
            WHITE,
            25,
        )
        loss.move_to(DOWN * 3.42)
        key = Text("Stage 1: learn alignment  |  Stage 2: learn visual instruction following", font=TEXT_FONT, font_size=18, color=self.connector_color)
        key.move_to(DOWN * 2.86)

        self.play(FadeIn(frozen_vision), FadeIn(train_projector), FadeIn(train_llm), run_time=0.9)
        self.play(FadeIn(triplet_label, shift=DOWN * 0.1), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in triplet], lag_ratio=0.15), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(task, shift=LEFT * 0.18) for task in tasks], lag_ratio=0.2), run_time=1.3)
        self.play(Write(key), FadeIn(loss, shift=UP * 0.1), Circumscribe(nodes[5], color=self.language_color, fade_out=True), run_time=1.6)
        self.wait(0.7)
        self.transition_out(title, pipeline, frozen_vision, train_projector, train_llm, triplet, triplet_label, tasks, loss, key)

    def task_card(self, title, subtitle, color):
        card = RoundedRectangle(
            corner_radius=0.1,
            width=2.4,
            height=0.76,
            fill_color=color,
            fill_opacity=0.16,
            stroke_color=color,
            stroke_width=1.5,
        )
        top = Text(title, font=TEXT_FONT, font_size=16, color=color, weight=BOLD)
        bottom = Text(subtitle, font=TEXT_FONT, font_size=14, color=GREY_B)
        text = VGroup(top, bottom).arrange(DOWN, buff=0.04).move_to(card)
        return VGroup(card, text)

    def training_table(self):
        title = self.make_title("What Gets Trained at Each Stage?")
        headers = ["Stage", "Vision Encoder", "Projector", "LLM"]
        rows = [
            ["1", "frozen", "trained", "frozen"],
            ["2", "frozen", "trained", "trained"],
        ]

        table = VGroup()
        cell_w = [1.2, 2.35, 2.05, 1.75]
        cell_h = 0.72
        for r in range(3):
            row_group = VGroup()
            values = headers if r == 0 else rows[r - 1]
            for c, value in enumerate(values):
                color = GREY_B
                if value == "trained":
                    color = self.connector_color
                elif value == "frozen":
                    color = self.frozen_color
                elif c == 0:
                    color = WHITE
                cell = RoundedRectangle(
                    corner_radius=0.05,
                    width=cell_w[c],
                    height=cell_h,
                    stroke_color=color,
                    stroke_width=1.5,
                    fill_color=color,
                    fill_opacity=0.08 if r > 0 else 0.16,
                )
                text_color = color if r > 0 or c == 0 else WHITE
                text = Text(value, font=TEXT_FONT, font_size=15, color=text_color, weight=BOLD if r == 0 or c == 0 else NORMAL)
                text.move_to(cell)
                row_group.add(VGroup(cell, text))
            row_group.arrange(RIGHT, buff=0.06)
            table.add(row_group)
        table.arrange(DOWN, buff=0.08).move_to(DOWN * 0.05)

        note = Text("The power comes from reusing CLIP and an existing LLM,\nthen learning the bridge and instruction-following behavior.", font=TEXT_FONT, font_size=20, color=GREY_B, line_spacing=1.08)
        note.next_to(table, DOWN, buff=0.45)

        self.play(Write(title), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.12) for row in table], lag_ratio=0.18), run_time=1.4)
        self.play(FadeIn(note, shift=UP * 0.1), Indicate(table[2][3], color=self.connector_color), run_time=1.4)
        self.wait(0.7)
        self.transition_out(title, table, note)
