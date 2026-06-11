from pathlib import Path

from manim import *

_ASSETS = Path(__file__).resolve().parents[1] / "assets"


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


class Scene2(ScaledTimingMixin, MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK

        def glass_panel(width, height, color, label, label_color=WHITE, font_size=17):
            rect = RoundedRectangle(
                corner_radius=0.16,
                width=width,
                height=height,
                stroke_color=color,
                stroke_width=2.2,
                fill_color=color,
                fill_opacity=0.22,
            )
            shine = rect.copy().set_stroke(WHITE, width=0.7, opacity=0.22).scale(1.025)
            text = Text(label, font=TEXT_FONT, font_size=font_size, color=label_color, line_spacing=1.05)
            text.move_to(rect)
            return VGroup(rect, shine, text)

        def explain(text, color=GREY_B, font_size=12):
            return Text(
                text,
                font=TEXT_FONT,
                font_size=font_size,
                color=color,
                line_spacing=1.08,
            )

        def flow_dot(path, color=YELLOW, radius=0.055):
            dot = Dot(path.get_start(), radius=radius, color=color)
            return Succession(
                FadeIn(dot, scale=0.5, run_time=0.15),
                MoveAlongPath(dot, path, rate_func=smooth, run_time=0.85),
                FadeOut(dot, scale=0.4, run_time=0.15),
            )

        title = Text(
            "Basic Architecture of Generalist Multimodal Models",
            font=TEXT_FONT,
            font_size=30,
            color=WHITE,
            weight=BOLD,
        ).to_edge(UP, buff=0.28)
        underline = Line(LEFT, RIGHT).set_width(6.4).next_to(title, DOWN, buff=0.14)
        underline.set_color_by_gradient(BLUE_B, YELLOW, GREEN_B)

        self.play(LaggedStart(Write(title), Create(underline), lag_ratio=0.28), run_time=1.6)

        image_label = Text("Image", font=TEXT_FONT, font_size=19, color=YELLOW, weight=BOLD).move_to(LEFT * 5.2 + DOWN * 0.25)
        car_img = ImageMobject(str(_ASSETS / "Scene2" / "YellowCar.png")).set_width(2.2).next_to(image_label, RIGHT, buff=0.34)
        image_group = Group(image_label, car_img).move_to(LEFT * 4.05 + DOWN * 1.15)

        visual_encoder = glass_panel(2.55, 0.7, BLUE_C, "Visual Encoder", font_size=17).move_to(LEFT * 0.95 + DOWN * 1.5)
        visual_note = explain("extracts image features", BLUE_B, 13).next_to(visual_encoder, DOWN, buff=0.16)
        vector_group = VGroup(
            Text("visual embedding", font=TEXT_FONT, font_size=15, color=GREY_B),
            Text("[0.12, ..., 1.08]", font=MONO_FONT, font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.08).next_to(visual_encoder, RIGHT, buff=0.55)

        connector = glass_panel(3.0, 0.76, ORANGE, "Cross-modal Connector", label_color=BLACK, font_size=16)
        connector.move_to(vector_group.get_center() + UP * 1.12)
        connector_note = explain("maps into language space", ORANGE, 13).next_to(connector, RIGHT, buff=0.24)
        language_vector = VGroup(
            Text("language-ready embedding", font=TEXT_FONT, font_size=15, color=GREY_B),
            Text("[<img>, ..., <car>]", font=MONO_FONT, font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.08).next_to(connector, UP, buff=0.34)
        decoder = glass_panel(3.0, 0.76, GREEN_C, "Language Decoder", label_color=BLACK, font_size=17)
        decoder.next_to(language_vector, UP, buff=0.34)

        instruction_title = Text("Instruction", font=TEXT_FONT, font_size=17, color=YELLOW, weight=BOLD)
        instruction_text = Text("What is unusual about this image?", font=TEXT_FONT, font_size=16, color=WHITE)
        instruction = VGroup(instruction_title, instruction_text).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        instruction.move_to(LEFT * 4.15 + UP * 0.42)

        output_title = Text("Output", font=TEXT_FONT, font_size=17, color=GREEN_B, weight=BOLD)
        output_text = Text("The unusual aspect of this image is ...", font=TEXT_FONT, font_size=16, color=WHITE)
        output = VGroup(output_title, output_text).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        output.next_to(decoder, UP, buff=0.32).align_to(decoder, LEFT)

        arrow_img = Arrow(car_img.get_right(), visual_encoder.get_left(), buff=0.12, color=YELLOW, stroke_width=4)
        arrow_vec = Arrow(visual_encoder.get_right(), vector_group.get_left(), buff=0.12, color=YELLOW, stroke_width=4)
        arrow_connector = Arrow(vector_group.get_top(), connector.get_bottom(), buff=0.09, color=ORANGE, stroke_width=4)
        arrow_lang_vec = Arrow(connector.get_top(), language_vector.get_bottom(), buff=0.09, color=ORANGE, stroke_width=4)
        arrow_decoder = Arrow(language_vector.get_top(), decoder.get_bottom(), buff=0.09, color=GREEN_B, stroke_width=4)
        arrow_instruction = Arrow(instruction.get_right(), decoder.get_left(), buff=0.18, color=WHITE, stroke_width=3.4)
        arrow_output = Arrow(decoder.get_top(), output.get_bottom(), buff=0.08, color=GREEN_B, stroke_width=3.4)

        intro_group = Group(
            title,
            underline,
            image_group,
            visual_encoder,
            visual_note,
            vector_group,
            connector,
            connector_note,
            language_vector,
            decoder,
            instruction,
            output,
            arrow_img,
            arrow_vec,
            arrow_connector,
            arrow_lang_vec,
            arrow_decoder,
            arrow_instruction,
            arrow_output,
        )

        self.play(
            LaggedStart(
                FadeIn(image_label, shift=RIGHT * 0.15),
                FadeIn(car_img, shift=RIGHT * 0.15),
                GrowArrow(arrow_img),
                DrawBorderThenFill(visual_encoder),
                FadeIn(visual_note, shift=DOWN * 0.08),
                GrowArrow(arrow_vec),
                FadeIn(vector_group, shift=RIGHT * 0.18),
                GrowArrow(arrow_connector),
                DrawBorderThenFill(connector),
                FadeIn(connector_note, shift=RIGHT * 0.12),
                GrowArrow(arrow_lang_vec),
                FadeIn(language_vector, shift=UP * 0.14),
                GrowArrow(arrow_decoder),
                DrawBorderThenFill(decoder),
                lag_ratio=0.18,
            ),
            run_time=4.3,
        )
        self.play(
            LaggedStart(
                flow_dot(arrow_img, YELLOW),
                flow_dot(arrow_vec, YELLOW),
                flow_dot(arrow_connector, ORANGE),
                flow_dot(arrow_lang_vec, ORANGE),
                flow_dot(arrow_decoder, GREEN_B),
                lag_ratio=0.2,
            ),
            Circumscribe(connector, color=ORANGE, fade_out=True),
            run_time=2.4,
        )
        self.play(FadeIn(instruction, shift=RIGHT * 0.18), GrowArrow(arrow_instruction), run_time=1.2)
        self.play(FadeIn(output, shift=UP * 0.12), GrowArrow(arrow_output), run_time=1.1)
        self.wait(1.0)

        lang_dec = glass_panel(3.15, 1.45, GREEN_C, "Language Decoder", font_size=20).move_to(ORIGIN)
        training_title = Text("Training the LLM", font=TEXT_FONT, font_size=27, color=WHITE, weight=BOLD).to_edge(UP, buff=0.48)
        old_arch = Group(intro_group)
        self.play(
            FadeOut(old_arch, shift=DOWN * 0.35, scale=0.95),
            FadeIn(training_title, shift=DOWN * 0.12),
            DrawBorderThenFill(lang_dec),
            self.camera.frame.animate.set(width=12.5).move_to(ORIGIN),
            run_time=1.8,
        )
        self.play(lang_dec.animate.scale(1.08).move_to(UP * 1.78), run_time=1.0, rate_func=smooth)

        timeline = NumberLine(x_range=[0, 10, 1], length=9.2, include_numbers=False, color=GREY_B).next_to(lang_dec, DOWN, buff=1.65)
        stage1 = Text("1. Self-supervised\npretraining", font=TEXT_FONT, font_size=20, color=BLUE_B).next_to(timeline.n2p(2.5), UP, buff=0.45)
        stage2 = Text("2. Instruction\nTuning", font=TEXT_FONT, font_size=20, color=YELLOW).next_to(timeline.n2p(7.5), UP, buff=0.45)
        dot1 = Dot(timeline.n2p(2.5), color=BLUE_B, radius=0.13)
        dot2 = Dot(timeline.n2p(7.5), color=YELLOW, radius=0.13)
        brace = BraceBetweenPoints(timeline.n2p(5.15), timeline.n2p(9.85), DOWN, color=YELLOW)
        teacher_hint = Text("requires instruction data", font=TEXT_FONT, font_size=17, color=YELLOW).next_to(brace, DOWN, buff=0.15)
        self.play(Create(timeline), run_time=1.1)
        self.play(
            LaggedStart(
                GrowFromCenter(dot1),
                FadeIn(stage1, shift=UP * 0.2),
                GrowFromCenter(dot2),
                FadeIn(stage2, shift=UP * 0.2),
                GrowFromCenter(brace),
                FadeIn(teacher_hint, shift=DOWN * 0.1),
                lag_ratio=0.18,
            ),
            run_time=2.2,
        )
        data_question = Text(
            "How do we create instruction-tuning data?",
            font=TEXT_FONT,
            font_size=25,
            color=YELLOW,
            weight=BOLD,
        ).next_to(brace, DOWN, buff=0.62)
        question_box = SurroundingRectangle(data_question, color=YELLOW, buff=0.16, corner_radius=0.1).set_stroke(width=2)
        self.play(FadeOut(teacher_hint, shift=DOWN * 0.1), FadeIn(data_question, shift=DOWN * 0.14), Create(question_box), run_time=1.2)
        self.wait(0.8)

        timeline_group = VGroup(lang_dec, timeline, stage1, stage2, dot1, dot2, brace, data_question, question_box, training_title)

        data_title = Text(
            "Instruction-tuning data can come from:",
            font=TEXT_FONT,
            font_size=28,
            color=WHITE,
            weight=BOLD,
        ).to_edge(UP, buff=0.55)

        human_card = RoundedRectangle(
            corner_radius=0.12,
            width=5.1,
            height=2.1,
            fill_color="#101820",
            fill_opacity=0.92,
            stroke_color=BLUE_B,
            stroke_width=2,
        )
        human_title = Text("Humans", font=TEXT_FONT, font_size=23, color=BLUE_B, weight=BOLD)
        human_body = VGroup(
            Text("High-quality examples", font=TEXT_FONT, font_size=17, color=WHITE),
            Text("Written by people", font=TEXT_FONT, font_size=17, color=WHITE),
            Text("High cost", font=TEXT_FONT, font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        human_content = VGroup(human_title, human_body).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(human_card)
        human_group = VGroup(human_card, human_content).move_to(LEFT * 3.0 + DOWN * 0.2)

        machine_card = RoundedRectangle(
            corner_radius=0.12,
            width=5.1,
            height=2.1,
            fill_color="#17160a",
            fill_opacity=0.92,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        machine_title = Text("Machines", font=TEXT_FONT, font_size=23, color=YELLOW, weight=BOLD)
        machine_body = VGroup(
            Text("Strong LLM teacher", font=TEXT_FONT, font_size=17, color=WHITE),
            Text("Example: GPT", font=TEXT_FONT, font_size=17, color=WHITE),
            Text("Affordable at scale", font=TEXT_FONT, font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        machine_content = VGroup(machine_title, machine_body).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(machine_card)
        machine_group = VGroup(machine_card, machine_content).move_to(RIGHT * 3.0 + DOWN * 0.2)

        self.play(
            FadeOut(timeline_group, shift=UP * 0.25),
            FadeIn(data_title, shift=DOWN * 0.12),
            self.camera.frame.animate.set(width=13.2).move_to(DOWN * 0.15),
            run_time=1.4,
        )
        self.play(
            LaggedStart(
                FadeIn(human_group, shift=RIGHT * 0.2),
                FadeIn(machine_group, shift=LEFT * 0.2),
                lag_ratio=0.25,
            ),
            run_time=1.6,
        )
        self.play(
            Circumscribe(machine_group, color=YELLOW, fade_out=True),
            run_time=1.2,
        )
        self.wait(3)

        teacher_img = ImageMobject(str(_ASSETS / "Scene2" / "Teacher.png")).set_width(2.05).move_to(LEFT * 4.45 + DOWN * 1.05)
        teacher_frame = SurroundingRectangle(teacher_img, color=GREEN_B, buff=0.05).set_stroke(width=2)
        example_instruction = RoundedRectangle(
            corner_radius=0.08,
            width=2.75,
            height=0.72,
            fill_color="#dcefd5",
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 1.0 + DOWN * 1.05)
        example_instruction_text = Text(
            "What are the two people\ndoing?",
            font=TEXT_FONT,
            font_size=16,
            color=BLACK,
            line_spacing=1.05,
        ).move_to(example_instruction)
        example_output = RoundedRectangle(
            corner_radius=0.08,
            width=3.75,
            height=0.72,
            fill_color="#fff0c9",
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 3.15 + DOWN * 1.05)
        example_output_text = Text(
            "They are talking in front\nof a whiteboard ...",
            font=TEXT_FONT,
            font_size=16,
            color=BLACK,
            line_spacing=1.05,
        ).move_to(example_output)
        example_arrow1 = Arrow(teacher_img.get_right(), example_instruction.get_left(), buff=0.18, color=GREY_B, stroke_width=3)
        example_arrow2 = Arrow(example_instruction.get_right(), example_output.get_left(), buff=0.18, color=GREY_B, stroke_width=3)
        triplet_label = Text("Image  +  Instruction  +  Output", font=TEXT_FONT, font_size=22, color=GREEN_B, weight=BOLD)
        triplet_label.next_to(example_instruction, UP, buff=0.38).align_to(example_instruction, LEFT)
        triplet_group = Group(
            teacher_img,
            teacher_frame,
            example_instruction,
            example_instruction_text,
            example_output,
            example_output_text,
            triplet_label,
        )
        triplet_full_group = Group(triplet_group, example_arrow1, example_arrow2)

        multimodal_question = Text(
            "Can an LLM generate\nImage-Instruction-Output data\nfor Large Multimodal Models?",
            font=TEXT_FONT,
            font_size=24,
            color=GREEN_B,
            weight=BOLD,
            line_spacing=1.1,
        ).move_to(UP * 1.35)
        multimodal_box = SurroundingRectangle(multimodal_question, color=GREEN_B, buff=0.22, corner_radius=0.12).set_stroke(width=2)
        comparison_group = VGroup(data_title, human_group, machine_group)
        self.play(
            FadeOut(comparison_group, shift=UP * 0.25),
            FadeIn(multimodal_question, shift=DOWN * 0.14),
            Create(multimodal_box),
            run_time=1.3,
        )
        self.play(
            FadeIn(triplet_group, shift=DOWN * 0.14),
            GrowArrow(example_arrow1),
            GrowArrow(example_arrow2),
            run_time=1.5,
        )
        self.wait(1.0)
        self.play(
            FadeOut(Group(triplet_full_group, multimodal_question, multimodal_box), shift=UP * 0.25),
            self.camera.frame.animate.set(width=14).move_to(ORIGIN + DOWN * 0.32),
            run_time=1.2,
        )

        problem_title = Text(
            "Problem: GPT only accepts text",
            font=TEXT_FONT,
            font_size=28,
            color=WHITE,
            weight=BOLD,
        ).to_edge(UP, buff=0.55)

        uav_img = ImageMobject(str(_ASSETS / "Scene2" / "UAV.png")).set_width(2.8).move_to(LEFT * 4.9 + UP * 0.05)
        uav_frame = SurroundingRectangle(uav_img, color=GREEN_B, buff=0.08).set_stroke(width=2, opacity=0.8)
        gpt_logo = Text("GPT", font=TEXT_FONT, font_size=32, color=WHITE, weight=BOLD).move_to(RIGHT * 4.95 + UP * 0.95)
        gpt_text = Text("(text only)", font=TEXT_FONT, font_size=20, color=GREY_B).next_to(gpt_logo, DOWN, buff=0.16)
        gpt_group = VGroup(gpt_logo, gpt_text)
        blocked_arrow = Arrow(uav_img.get_right(), gpt_group.get_left(), buff=0.3, color=RED_B, stroke_width=5)
        arrow_mid = blocked_arrow.get_center()
        q_mark = Text("?", font=TEXT_FONT, font_size=72, color=RED, weight=BOLD).move_to(arrow_mid + DOWN * 0.92)
        problem_note = explain("We want to send an image,\nbut GPT only accepts text", RED_B, 13).next_to(q_mark, DOWN, buff=0.05)
        self.play(
            FadeIn(problem_title, shift=DOWN * 0.12),
            FadeIn(uav_img, shift=RIGHT * 0.25),
            Create(uav_frame),
            FadeIn(gpt_group, shift=LEFT * 0.25),
            FadeIn(problem_note, shift=DOWN * 0.12),
            run_time=1.2,
        )
        self.play(GrowArrow(blocked_arrow), FadeIn(q_mark, scale=1.2), run_time=1.0)
        self.play(Flash(q_mark, color=RED, flash_radius=0.72, line_length=0.3), Indicate(gpt_text, color=RED), run_time=1.2)
        self.wait(0.7)

        context_title = Text(
            "Generating Data from Context Information",
            font=TEXT_FONT,
            font_size=28,
            color=WHITE,
            weight=BOLD,
        ).to_edge(UP, buff=0.72)
        context_row_y = 0.12
        uav_detect_img = ImageMobject(str(_ASSETS / "Scene2" / "UAV_detect.png")).set_width(4.25).move_to(LEFT * 4.45 + UP * context_row_y)
        detect_frame = SurroundingRectangle(uav_detect_img, color=YELLOW, buff=0.08).set_stroke(width=2, opacity=0.9)
        solution_note = explain("Represent the image as context:\ncaption + layout", YELLOW, 14).next_to(uav_detect_img, DOWN, buff=0.16)
        self.play(
            FadeOut(uav_img),
            FadeIn(uav_detect_img),
            ReplacementTransform(uav_frame, detect_frame),
            FadeOut(blocked_arrow),
            FadeOut(q_mark),
            FadeOut(problem_note, shift=UP * 0.12),
            FadeOut(problem_title, shift=UP * 0.12),
            FadeOut(gpt_group, shift=RIGHT * 0.12),
            FadeIn(context_title, shift=DOWN * 0.12),
            FadeIn(solution_note, shift=DOWN * 0.12),
            run_time=1.6,
        )
        self.wait(0.3)

        code_bg = RoundedRectangle(
            corner_radius=0.12,
            width=3.75,
            height=2.38,
            fill_color="#05070d",
            fill_opacity=0.92,
            stroke_color=GREY_B,
            stroke_width=1.4,
        ).move_to(LEFT * 0.22 + UP * context_row_y)
        context_caption = Text(
            "caption:\nA group of people standing outside\nof a black vehicle...",
            font=MONO_FONT,
            font_size=14,
            color=GREEN_B,
            line_spacing=1.15,
        )
        context_layout = Text(
            "layout:\nperson [0.68, 0.24, 0.77, 0.69]\nvehicle [0.10, 0.20, 0.80, 0.90] ...",
            font=MONO_FONT,
            font_size=14,
            color=BLUE_B,
            line_spacing=1.15,
        )
        code_group = VGroup(context_caption, context_layout).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if code_group.width > code_bg.width - 0.36:
            code_group.set_width(code_bg.width - 0.36)
        code_group.move_to(code_bg)
        extract_arrow = Arrow(uav_detect_img.get_right(), code_bg.get_left(), buff=0.08, color=YELLOW, stroke_width=4)
        self.play(GrowArrow(extract_arrow), DrawBorderThenFill(code_bg), run_time=1.1)
        self.play(
            LaggedStart(AddTextLetterByLetter(context_caption), AddTextLetterByLetter(context_layout), lag_ratio=0.45),
            run_time=3.2,
        )
        self.wait(0.8)

        right_col_x = 4.55
        seed_title = Text("Manual Seed Examples", font=TEXT_FONT, font_size=18, color=YELLOW, weight=BOLD)
        seed_flow = VGroup(
            Text("Context", font=TEXT_FONT, font_size=13.5, color=LIGHT_GREY),
            MathTex(r"\rightarrow", font_size=15, color=YELLOW),
            Text("Instruction", font=TEXT_FONT, font_size=13.5, color=LIGHT_GREY),
            MathTex(r"\rightarrow", font_size=15, color=YELLOW),
            Text("Output", font=TEXT_FONT, font_size=13.5, color=LIGHT_GREY),
        ).arrange(RIGHT, buff=0.08)
        seed_body = VGroup(
            Text("Manually prepare a few examples", font=TEXT_FONT, font_size=13.5, color=LIGHT_GREY),
            seed_flow,
            Text("GPT learns the answer format", font=TEXT_FONT, font_size=13.5, color=LIGHT_GREY),
        ).arrange(DOWN, buff=0.08)

        seed_labels = VGroup()
        seed_data = [
            ("Context", "caption\nlayout", BLUE_B),
            ("Instruction", "question\nrequest", YELLOW),
            ("Output", "target\nanswer", GREEN_B),
        ]
        for label, desc, color in seed_data:
            seed_card = RoundedRectangle(
                corner_radius=0.08,
                width=1.18,
                height=0.86,
                fill_color="#111827",
                fill_opacity=0.95,
                stroke_color=color,
                stroke_width=1.4,
            )
            seed_label = Text(label, font=TEXT_FONT, font_size=12.5, color=color)
            seed_desc = Text(desc, font=TEXT_FONT, font_size=11.5, color=WHITE, line_spacing=0.9)
            seed_text = VGroup(seed_label, seed_desc).arrange(DOWN, buff=0.07).move_to(seed_card)
            if seed_text.width > seed_card.width - 0.12:
                seed_text.set_width(seed_card.width - 0.12)
            seed_labels.add(VGroup(seed_card, seed_text))
        seed_labels.arrange(RIGHT, buff=0.14)

        seed_content = VGroup(seed_title, seed_body, seed_labels).arrange(DOWN, buff=0.22)
        seed_panel = RoundedRectangle(
            corner_radius=0.12,
            width=4.25,
            height=2.58,
            fill_color="#05070d",
            fill_opacity=0.92,
            stroke_color=YELLOW,
            stroke_width=1.5,
        ).move_to(RIGHT * right_col_x + UP * context_row_y)
        if seed_content.width > seed_panel.width - 0.34:
            seed_content.set_width(seed_panel.width - 0.34)
        if seed_content.height > seed_panel.height - 0.24:
            seed_content.set_height(seed_panel.height - 0.24)
        seed_content.move_to(seed_panel)
        seed_group = VGroup(seed_panel, seed_content)
        self.play(FadeIn(seed_group, shift=LEFT * 0.16), run_time=1.2)
        self.wait(0.8)

        left_context = Group(uav_detect_img, detect_frame, extract_arrow, code_bg, code_group, solution_note)
        gpt_teacher_text = Text(
            "GPT generates data:\nimage + instruction + output",
            font=TEXT_FONT,
            font_size=15,
            color=WHITE,
            line_spacing=1.05,
        )
        gpt_teacher_box = RoundedRectangle(
            corner_radius=0.1,
            width=3.25,
            height=0.82,
            fill_color="#05070d",
            fill_opacity=0.92,
            stroke_color=GREEN_B,
            stroke_width=1.5,
        ).move_to(RIGHT * right_col_x + UP * 1.18)
        gpt_teacher_text.move_to(gpt_teacher_box)
        gpt_teacher_group = VGroup(gpt_teacher_box, gpt_teacher_text)
        self.play(
            left_context.animate.shift(LEFT * 0.35),
            FadeOut(seed_group, shift=UP * 0.12),
            FadeOut(context_title, shift=UP * 0.12),
            FadeIn(gpt_teacher_group, shift=DOWN * 0.08),
            run_time=1.5,
        )

        teacher_arrow = Arrow(code_bg.get_right(), gpt_teacher_box.get_left(), buff=0.14, color=YELLOW, stroke_width=4)
        self.play(GrowArrow(teacher_arrow), flow_dot(teacher_arrow, YELLOW), run_time=1.4)

        scroll_titles = [
            ("Conversation", "58K examples", BLUE_B),
            ("Detailed description", "23K examples", GREEN_B),
            ("Complex reasoning", "77K examples", ORANGE),
        ]
        cards = VGroup()
        for vi, en, color in scroll_titles:
            card = RoundedRectangle(
                corner_radius=0.1,
                width=3.65,
                height=0.78,
                fill_color="#f7f7f2",
                fill_opacity=1,
                stroke_color=color,
                stroke_width=2,
            )
            vi_text = Text(vi, font=TEXT_FONT, font_size=17, color=BLACK)
            en_text = Text(en, font=TEXT_FONT, font_size=15, color=GREY_E)
            label = VGroup(vi_text, en_text).arrange(DOWN, buff=0.035).move_to(card)
            cards.add(VGroup(card, label))
        cards.arrange(DOWN, buff=0.22).move_to(RIGHT * right_col_x + DOWN * 0.48)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        FadeIn(card, shift=RIGHT * 0.45),
                        Flash(card[0], color=card[0].get_stroke_color(), flash_radius=0.65, line_length=0.18),
                    )
                    for card in cards
                ],
                lag_ratio=0.35,
            ),
            run_time=2.4,
        )

        final_text = Text("LLaVA-Instruct-158K", font=TEXT_FONT, font_size=24, color=GREEN_B, weight=BOLD).next_to(cards, DOWN, buff=0.34)
        final_text.move_to([right_col_x, final_text.get_center()[1], 0])
        final_box = SurroundingRectangle(final_text, color=GREEN_B, buff=0.18, corner_radius=0.12).set_stroke(width=2)
        star = Star(n=5, outer_radius=0.22, inner_radius=0.1, color=YELLOW, fill_opacity=1).next_to(final_text, LEFT, buff=0.25)
        self.play(Write(final_text), Create(final_box), GrowFromCenter(star), run_time=1.4)
        self.play(
            Circumscribe(VGroup(final_box, final_text), color=GREEN_B, fade_out=True),
            self.camera.frame.animate.set(width=14.2).move_to(Group(left_context, gpt_teacher_group, cards, final_text).get_center() + UP * 0.18),
            run_time=1.6,
        )
        self.wait(3.5)
