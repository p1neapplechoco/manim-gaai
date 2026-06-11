from pathlib import Path

from manim import *


_ASSETS = Path(__file__).resolve().parents[1] / "assets"
YELLOW_IMAGE = _ASSETS / "Scene4" / "Yellow.png"
MONA_IMAGE = _ASSETS / "Scene4" / "Monalisa.png"
BENCHMARK_IMAGE = _ASSETS / "Scene4" / "benmark.png"
COMBINATORIAL_IMAGE = _ASSETS / "Scene4" / "Combinatorial Task.png"
MULTILINGUAL_IMAGE = _ASSETS / "Scene4" / "Multilingual.jpg"
TEXT_FONT = "Times New Roman"


TIME_SCALE = 3.3


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


class Scene4(ScaledTimingMixin, Scene):
    def construct(self):
        self.camera.background_color = BLACK

        self.visual = "#58C4DD"
        self.language = "#83C167"
        self.connector = "#FFFF00"
        self.orange = "#FF8C2A"
        self.warning = "#FF6666"
        self.navy = "#1D3F6E"
        self.peach = "#F7D9C8"

        self.scene_one_question()
        self.scene_two_responses()
        self.scene_mona_lisa()
        self.scene_combinatorial_generalization()
        self.scene_multilingual_generalization()
        self.scene_transition_to_benchmark()
        self.scene_benchmark_table()
        self.scene_benchmark_image()

    def make_title(self, text, color=WHITE):
        title = Text(text, font=TEXT_FONT, font_size=31, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        underline = Line(LEFT, RIGHT).set_width(min(8.2, title.width * 0.92))
        underline.next_to(title, DOWN, buff=0.1)
        underline.set_color_by_gradient(self.visual, self.connector, self.language)
        return VGroup(title, underline)

    def text(self, content, color=WHITE, size=20, width=None, weight=NORMAL, line_spacing=1.02):
        def make_line(line):
            return Text(line, font=TEXT_FONT, font_size=size, color=color, weight=weight, line_spacing=line_spacing)

        mob = make_line(content)
        if width and mob.width > width and "\n" not in content and " " in content:
            lines = []
            current_words = []
            for word in content.split():
                trial = " ".join(current_words + [word])
                if current_words and make_line(trial).width > width:
                    lines.append(" ".join(current_words))
                    current_words = [word]
                else:
                    current_words.append(word)
            if current_words:
                lines.append(" ".join(current_words))
            mob = VGroup(*[make_line(line) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.06 * line_spacing)
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
        glow = rect.copy().set_stroke(WHITE, width=0.55, opacity=0.12).scale(1.01)
        group = VGroup(rect, glow)
        if content is not None:
            content.move_to(rect)
            group.add(content)
        return group

    def image_card(self, path, width=4.8, height=3.0, color=None):
        color = color or self.visual
        frame = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=2,
            fill_color="#0A1118",
            fill_opacity=0.85,
        )
        if Path(path).exists():
            image = ImageMobject(str(path))
            image.set_width(width - 0.16)
            if image.height > height - 0.16:
                image.set_height(height - 0.16)
            image.move_to(frame)
            return Group(frame, image)
        missing = self.text("Missing image\n" + Path(path).name, self.warning, 18, width - 0.35)
        missing.move_to(frame)
        return VGroup(frame, missing)

    def response_card(self, name, body, color, width, height, body_size=15):
        title = self.text(name, color, 18, width - 0.3, weight=BOLD)
        body_mob = self.text(body, WHITE, body_size, width - 0.45, line_spacing=0.95)
        content = VGroup(title, body_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        box = self.card(width, height, color, content, fill_opacity=0.1)
        content.align_to(box[0], LEFT).shift(RIGHT * 0.22)
        content.move_to([content.get_center()[0], box[0].get_center()[1], 0])
        return box

    def cleanup(self, *mobjects):
        self.play(FadeOut(Group(*mobjects), shift=UP * 0.15), run_time=0.65)

    def reasoning_card(self, title, subtitle, color):
        content = VGroup(
            self.text(title, color, 19, 3.15, weight=BOLD),
            self.text(subtitle, WHITE, 16, 3.15),
        ).arrange(DOWN, buff=0.04)
        return self.card(3.55, 0.82, color, content, fill_opacity=0.1, radius=0.08)

    def scene_one_question(self):
        title = self.make_title("What LLaVA Can Do", self.connector)
        image = self.image_card(YELLOW_IMAGE, width=6.0, height=3.55).move_to(UP * 0.45)
        question = self.card(
            6.2,
            0.58,
            self.connector,
            self.text("What is unusual about this image?", BLACK, 24, 5.8, weight=BOLD),
            fill_opacity=0.9,
        ).next_to(image, DOWN, buff=0.28)
        models = VGroup(*[
            self.card(2.05, 0.52, color, self.text(name, WHITE, 16, 1.8, weight=BOLD), fill_opacity=0.15, radius=0.08)
            for name, color in [
                ("LLaVA", self.language),
                ("GPT-4", self.visual),
                ("BLIP-2", GREY_B),
                ("OpenFlamingo", GREY_B),
            ]
        ]).arrange(RIGHT, buff=0.16).to_edge(DOWN, buff=0.42)
        highlight = Rectangle(width=1.55, height=1.2, stroke_color=self.warning, stroke_width=4)
        highlight.move_to(image.get_center() + UP * 0.35 + RIGHT * 0.35)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), run_time=1.0)
        self.play(FadeIn(question, shift=UP * 0.1), LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in models], lag_ratio=0.1), run_time=1.2)
        self.play(Create(highlight), Circumscribe(question, color=self.connector), run_time=1.1)
        self.wait(0.35)
        self.cleanup(title, image, question, models, highlight)

    def scene_two_responses(self):
        title = self.make_title("Same Question, Stronger Answer")
        question = self.text("What is unusual about this image?", self.connector, 24, 7.5, weight=BOLD).next_to(title, DOWN, buff=0.28)

        llava_response = (
            "1. Identifies the activity: ironing clothes.\n"
            "2. Grounds the location: on the back of a minivan / van.\n"
            "3. Compares it with normal context: unsafe and unusual.\n"
            "4. Explains why balance is hard in an unstable setting."
        )
        llava = self.response_card("LLaVA", llava_response, self.language, 6.2, 2.62, body_size=18).move_to(LEFT * 2.95 + UP * 0.38)
        gpt = self.response_card(
            "GPT-4 [32]",
            "Recognizes someone ironing on a car, but gives a shorter explanation.",
            self.visual,
            4.45,
            0.92,
            body_size=16,
        ).move_to(RIGHT * 3.42 + UP * 1.08)
        blip = self.response_card("BLIP-2", "Only captions: a person sitting on the back of a yellow taxi.", GREY_B, 4.45, 0.92, body_size=15).next_to(gpt, DOWN, buff=0.24)
        flamingo = self.response_card("OpenFlamingo", "Misreads the action as drying clothes on the hood of a car.", GREY_B, 4.45, 0.92, body_size=15).next_to(blip, DOWN, buff=0.24)

        comment = self.card(
            8.4,
            0.56,
            self.connector,
            self.text("Takeaway: LLaVA gives a fuller answer by recognizing the action, context, and risk.", BLACK, 17, 7.95, weight=BOLD),
            fill_opacity=0.9,
        ).to_edge(DOWN, buff=0.52)

        self.play(Write(title), FadeIn(question, shift=DOWN * 0.08), run_time=1.0)
        self.play(FadeIn(llava, shift=RIGHT * 0.12), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(card, shift=LEFT * 0.12) for card in [gpt, blip, flamingo]], lag_ratio=0.18), run_time=1.3)
        self.play(FadeIn(comment, shift=UP * 0.08), run_time=0.8)
        self.play(Circumscribe(llava, color=self.language), Circumscribe(comment, color=self.connector), run_time=1.15)
        self.wait(0.4)
        self.cleanup(title, question, llava, gpt, blip, flamingo, comment)

    def scene_mona_lisa(self):
        title = self.make_title("Understanding Parody: Mona Lisa")
        image = self.image_card(MONA_IMAGE, width=4.1, height=3.3).move_to(LEFT * 3.7 + UP * 0.1)
        question = self.card(
            4.85,
            0.54,
            self.connector,
            self.text("What may be the purpose of this painting?", BLACK, 17, 4.55, weight=BOLD),
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.2 + UP * 1.62)
        points = VGroup(
            self.reasoning_card("famous painting", "The Mona Lisa", self.visual),
            self.reasoning_card("same pose", "dog replaces the subject", self.orange),
            self.reasoning_card("humorous take", "creative parody", self.language),
            self.reasoning_card("commentary", "tribute / cultural meaning", self.connector),
        ).arrange(DOWN, buff=0.14).scale(0.88).move_to(RIGHT * 3.25 + DOWN * 0.35)

        quote = self.card(
            9.4,
            0.48,
            self.language,
            self.text("It does not just see objects; it recognizes references and artistic intent.", WHITE, 18, 8.9, weight=BOLD),
            fill_opacity=0.13,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), FadeIn(question, shift=DOWN * 0.08), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.13) for p in points], lag_ratio=0.13), run_time=1.35)
        self.play(FadeIn(quote, shift=UP * 0.1), Circumscribe(points[2], color=self.language), run_time=1.2)
        self.wait(0.4)
        self.cleanup(title, image, question, points, quote)

    def scene_combinatorial_generalization(self):
        title = self.make_title("Combinatorial Task Generalization")
        diagram = self.image_card(COMBINATORIAL_IMAGE, width=7.05, height=4.05, color=self.orange)
        diagram.move_to(LEFT * 2.75 + UP * 0.03)

        idea_content = VGroup(
            self.text("Combinatorial Task\nGeneralization", BLACK, 18, 3.65, weight=BOLD, line_spacing=0.88),
            self.text(
                "The model does not need\n"
                "every task combination.\n"
                "It recombines learned skills.",
                BLACK,
                16,
                3.65,
                line_spacing=0.9,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        idea = self.card(
            4.05,
            1.9,
            self.connector,
            idea_content,
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.85 + UP * 0.86)
        skills = VGroup(
            self.skill_chip("multilingual", self.visual),
            self.skill_chip("visual conversation", self.orange),
            self.skill_chip("OCR / groundedness", self.language),
            self.skill_chip("longer writing", self.connector, text_color=BLACK),
        ).arrange(DOWN, buff=0.12).next_to(idea, DOWN, buff=0.24)

        note = self.card(
            9.3,
            0.5,
            self.language,
            self.text("Takeaway: LLaVA composes learned skills for new tasks instead of memorizing training examples.", WHITE, 16, 8.85, weight=BOLD),
            fill_opacity=0.14,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(diagram, scale=0.96), run_time=1.0)
        self.play(FadeIn(idea, shift=LEFT * 0.12), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(skill, shift=UP * 0.08) for skill in skills], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(note, shift=UP * 0.08), Circumscribe(diagram, color=self.orange), run_time=1.1)
        self.wait(0.4)
        self.cleanup(title, diagram, idea, skills, note)

    def skill_chip(self, text, color, text_color=WHITE):
        return self.card(
            3.05,
            0.46,
            color,
            self.text(text, text_color, 15, 2.75, weight=BOLD),
            fill_opacity=0.18 if text_color == WHITE else 0.9,
            radius=0.08,
        )

    def scene_multilingual_generalization(self):
        title = self.make_title("Emergent Multilingual")
        example = self.image_card(MULTILINGUAL_IMAGE, width=5.85, height=4.05, color=self.visual)
        example.move_to(LEFT * 3.25 + UP * 0.03)

        prompt = self.card(
            4.55,
            0.78,
            self.connector,
            self.text("Image: French Quarter\nRequest: answer in Chinese", BLACK, 17, 4.1, weight=BOLD),
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.55 + UP * 1.35)
        explanation = self.card(
            4.55,
            1.78,
            self.language,
            self.text(
                "LLaVA sees a U.S. street scene,\n"
                "recognizes the cultural context,\n"
                "then writes a fluent description\n"
                "in another language.",
                WHITE,
                18,
                4.1,
                weight=BOLD,
                line_spacing=0.95,
            ),
            fill_opacity=0.13,
        ).next_to(prompt, DOWN, buff=0.28)
        conclusion = self.card(
            4.55,
            0.78,
            self.orange,
            self.text("This is generalization: vision + language + world knowledge.", WHITE, 16, 4.1, weight=BOLD),
            fill_opacity=0.16,
        ).next_to(explanation, DOWN, buff=0.28)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(example, scale=0.96), run_time=1.0)
        self.play(FadeIn(prompt, shift=LEFT * 0.1), FadeIn(explanation, shift=LEFT * 0.1), run_time=1.1)
        self.play(FadeIn(conclusion, shift=UP * 0.08), Circumscribe(example, color=self.visual), run_time=1.1)
        self.wait(0.4)
        self.cleanup(title, example, prompt, explanation, conclusion)

    def labeled_thumbnail(self, image_path, label, color, width, height):
        image = self.image_card(image_path, width=width, height=height, color=color)
        label_box = self.card(width + 0.18, 0.46, color, self.text(label, WHITE, 15, width - 0.05, weight=BOLD), fill_opacity=0.16, radius=0.08)
        return Group(image, label_box).arrange(DOWN, buff=0.12)

    def scene_transition_to_benchmark(self):
        title = self.make_title("From Examples to Benchmarks")
        yellow_group = self.labeled_thumbnail(YELLOW_IMAGE, "Extreme Ironing", self.visual, 2.9, 1.75)
        mona_group = self.labeled_thumbnail(MONA_IMAGE, "Parodied Mona Lisa", self.orange, 2.25, 1.6)
        examples = Group(yellow_group, mona_group).arrange(DOWN, buff=0.46).move_to(LEFT * 4.25 + DOWN * 0.05)

        axis = Line(LEFT * 2.2, RIGHT * 2.2, color=GREY_B, stroke_width=3).move_to(RIGHT * 2.35 + DOWN * 0.05)
        left_label = self.text("qualitative\nexamples", self.visual, 20, 2.0).next_to(axis, LEFT, buff=0.38)
        right_label = self.text("quantitative\nbenchmarks", self.language, 20, 2.1).next_to(axis, RIGHT, buff=0.38)
        dots = VGroup(Dot(axis.get_left(), color=self.visual), Dot(axis.get_right(), color=self.language))
        arrow = Arrow(axis.get_left(), axis.get_right(), buff=0.08, color=self.connector, stroke_width=4)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(examples, shift=RIGHT * 0.12), run_time=1.0)
        self.play(Create(axis), FadeIn(left_label), FadeIn(right_label), FadeIn(dots), GrowArrow(arrow), run_time=1.2)
        self.play(Circumscribe(right_label, color=self.connector), run_time=0.9)
        self.wait(0.3)
        self.cleanup(title, examples, axis, left_label, right_label, dots, arrow)

    def scene_benchmark_table(self):
        title = self.make_title("Benchmark Table: LLaVA-1.6-34B")
        headers = ["Model", "MMMU\n(val)", "MMMU\n(test)", "MathVista", "MMBench\n-EN", "MMBench\n-CN", "MM-Vet"]
        rows = [
            ["GPT-4V", "56.8", "55.7", "49.9", "75.8", "73.9", "67.6"],
            ["Gemini Ultra", "59.4", "-", "53", "-", "-", "-"],
            ["Gemini Pro", "47.9", "-", "45.2", "73.6", "74.3", "64.3"],
            ["LLaVA-1.5-13B", "36.4", "33.6", "27.6", "67.8", "63.3", "36.3"],
            ["LLaVA-1.6-34B", "51.1", "45.3", "46.5", "79.3", "79", "57.4"],
        ]
        table = self.make_benchmark_table(headers, rows).move_to(UP * 0.05)
        note = self.text("LLaVA-1.6-34B beats Gemini Pro on MMMU val, MathVista, and MMBench; MM-Vet remains lower.", self.connector, 18, 10.6)
        note.next_to(table, DOWN, buff=0.35)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(table[0], shift=DOWN * 0.08), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.08) for row in table[1:4]], lag_ratio=0.13), run_time=1.25)
        self.play(FadeIn(table[4], shift=UP * 0.08), run_time=0.55)
        self.play(FadeIn(table[5], shift=UP * 0.08), FadeIn(note, shift=UP * 0.08), run_time=0.9)
        self.play(Circumscribe(table[5], color=self.orange), run_time=1.0)
        for idx in [1, 3, 4, 5]:
            self.play(Circumscribe(table[5][idx], color=self.connector), run_time=0.35)
        self.wait(0.35)
        self.cleanup(title, table, note)

    def make_benchmark_table(self, headers, rows):
        widths = [2.05, 1.1, 1.1, 1.25, 1.25, 1.25, 1.1]
        cell_h = 0.54
        table = VGroup()
        all_rows = [headers] + rows
        for r, values in enumerate(all_rows):
            row_group = VGroup()
            for c, value in enumerate(values):
                is_header = r == 0
                is_llava16 = r == len(all_rows) - 1
                fill = self.navy if is_header else (self.peach if is_llava16 else "#ECECEC")
                stroke = WHITE if is_header else "#C8C8C8"
                text_color = WHITE if is_header else (self.orange if is_llava16 else BLACK)
                cell = Rectangle(width=widths[c], height=cell_h, stroke_color=stroke, stroke_width=0.8, fill_color=fill, fill_opacity=1.0)
                text = Text(str(value), font=TEXT_FONT, font_size=16 if c else 15, color=text_color, weight=BOLD if is_header or is_llava16 else NORMAL)
                if text.width > widths[c] - 0.12:
                    text.set_width(widths[c] - 0.12)
                text.move_to(cell)
                row_group.add(VGroup(cell, text))
            row_group.arrange(RIGHT, buff=0)
            table.add(row_group)
        table.arrange(DOWN, buff=0)
        return table

    def scene_benchmark_image(self):
        title = self.make_title("Radar Chart: LLaVA-1.5 Across Benchmarks")
        radar = self.image_card(BENCHMARK_IMAGE, width=8.7, height=5.45, color=self.warning).move_to(DOWN * 0.15)
        callout_text = VGroup(
            Text("Larger area", font=TEXT_FONT, font_size=18, color=BLACK, weight=BOLD),
            MathTex(r"\rightarrow", font_size=22, color=BLACK),
            Text("more balanced capability", font=TEXT_FONT, font_size=18, color=BLACK, weight=BOLD),
        ).arrange(RIGHT, buff=0.12)
        callout = self.card(
            5.25,
            0.48,
            self.connector,
            callout_text,
            fill_opacity=0.9,
        ).next_to(title, DOWN, buff=0.22)
        note = self.card(
            4.8,
            0.52,
            self.warning,
            self.text("Red curve: LLaVA-1.5", WHITE, 19, 4.4, weight=BOLD),
            fill_opacity=0.2,
        ).to_edge(DOWN, buff=0.34)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(radar, scale=0.96), run_time=1.0)
        self.play(FadeIn(callout, shift=DOWN * 0.08), FadeIn(note, shift=UP * 0.08), run_time=0.9)
        self.play(Circumscribe(radar, color=self.warning), run_time=1.0)
        self.wait(0.4)
