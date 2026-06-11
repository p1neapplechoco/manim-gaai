from pathlib import Path

from manim import *


_ASSETS = Path(__file__).resolve().parents[1] / "assets"
SCENE6_DIR = _ASSETS / "Scene6"
VEGETABLE_IMAGE = SCENE6_DIR / "Vegetable.png"
if not VEGETABLE_IMAGE.exists():
    VEGETABLE_IMAGE = SCENE6_DIR / "Matryosha.png"
MATRYOSHKA_IMAGE = SCENE6_DIR / "image1.png"
if not MATRYOSHKA_IMAGE.exists():
    MATRYOSHKA_IMAGE = SCENE6_DIR / "Matryosha.png"
ROBOT_IMAGE = SCENE6_DIR / "Robot.png"

TEXT_FONT = "Times New Roman"


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


class Scene6(ScaledTimingMixin, Scene):
    def construct(self):
        self.camera.background_color = BLACK

        self.visual = "#58C4DD"
        self.language = "#83C167"
        self.connector = "#FFFF00"
        self.orange = "#FF8C2A"
        self.warning = "#FF6666"
        self.navy = "#1D3F6E"
        self.panel = "#071018"

        self.scene_opening()
        self.scene_sota_tables()
        self.scene_visual_prompt_benchmark()
        self.scene_vegetable_example()
        self.scene_yollava()
        self.scene_matryoshka()
        self.scene_limitations()
        self.scene_future_directions()
        self.scene_multimodal_agents_detail()
        self.scene_robot_learning_pivot()
        self.scene_conclusion()

    def make_title(self, text, color=WHITE):
        title = Text(text, font=TEXT_FONT, font_size=30, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        underline = Line(LEFT, RIGHT).set_width(min(8.6, title.width * 0.92))
        underline.next_to(title, DOWN, buff=0.1)
        underline.set_color_by_gradient(self.visual, self.connector, self.language)
        return VGroup(title, underline)

    def make_arrow_title(self, left, right, color=WHITE):
        title = self.arrow_text([left, right], color=color, size=30, weight=BOLD, arrow_color=self.connector)
        title.to_edge(UP, buff=0.28)
        underline = Line(LEFT, RIGHT).set_width(min(8.6, title.width * 0.92))
        underline.next_to(title, DOWN, buff=0.1)
        underline.set_color_by_gradient(self.visual, self.connector, self.language)
        return VGroup(title, underline)

    def text(self, content, color=WHITE, size=20, width=None, weight=NORMAL, line_spacing=1.0):
        mob = Text(content, font=TEXT_FONT, font_size=size, color=color, weight=weight, line_spacing=line_spacing)
        if width and mob.width > width:
            mob.set_width(width)
        return mob

    def arrow_text(self, segments, color=WHITE, size=20, width=None, weight=NORMAL, arrow_color=None):
        parts = VGroup()
        for index, segment in enumerate(segments):
            parts.add(Text(segment, font=TEXT_FONT, font_size=size, color=color, weight=weight))
            if index < len(segments) - 1:
                parts.add(MathTex(r"\rightarrow", font_size=size + 4, color=arrow_color or color))
        parts.arrange(RIGHT, buff=0.09)
        if width and parts.width > width:
            parts.set_width(width)
        return parts

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

    def image_card(self, path, width=5.0, height=3.2, color=None, fill="#0A1118"):
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
        self.play(FadeOut(Group(*mobjects), shift=UP * 0.12), run_time=0.62)

    def chip(self, label, color, text_color=WHITE, width=2.15, height=0.5, size=15):
        return self.card(
            width,
            height,
            color,
            self.text(label, text_color, size, width - 0.25, weight=BOLD),
            fill_opacity=0.9 if text_color == BLACK else 0.14,
            radius=0.08,
        )

    def scene_opening(self):
        title = self.make_title("Quantitative Evaluation", self.connector)
        subtitle = self.text("Quantitative Evaluation of ViP-LLaVA", WHITE, 27, 7.5, weight=BOLD).next_to(title, DOWN, buff=0.28)
        capabilities = VGroup(*[
            self.chip(label, color, BLACK if color == self.connector else WHITE, width=2.25)
            for label, color in [
                ("recognition", self.visual),
                ("counting", self.orange),
                ("captioning", self.language),
                ("visual reasoning", self.visual),
                ("OCR", self.connector),
                ("math", self.language),
            ]
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.18, 0.22)).move_to(UP * 0.25)
        prompt_mark = VGroup(
            RoundedRectangle(width=2.7, height=1.6, corner_radius=0.12, stroke_color=self.visual, fill_color=self.visual, fill_opacity=0.1),
            Arrow(LEFT * 0.55 + UP * 0.45, LEFT * 0.15, color=self.connector, stroke_width=6),
            Circle(radius=0.28, color=self.connector, stroke_width=5).shift(LEFT * 0.15),
        ).move_to(LEFT * 3.7 + DOWN * 1.55)
        benchmark = self.card(
            3.0,
            1.25,
            self.language,
            VGroup(
                self.text("Benchmark", self.language, 22, 2.5, weight=BOLD),
                self.text("many questions\nmany capabilities", WHITE, 16, 2.5, line_spacing=0.86),
            ).arrange(DOWN, buff=0.08),
            fill_opacity=0.13,
        ).move_to(RIGHT * 3.55 + DOWN * 1.55)
        arrow = Arrow(prompt_mark.get_right(), benchmark.get_left(), color=self.connector, stroke_width=4, buff=0.18)
        hook = self.card(
            8.7,
            0.55,
            self.connector,
            self.text("Understanding visual prompts is not just a demo. It needs measurement.", BLACK, 19, 8.1, weight=BOLD),
            fill_opacity=0.9,
        ).to_edge(DOWN, buff=0.36)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN * 0.08), run_time=0.95)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in capabilities], lag_ratio=0.08), run_time=1.25)
        self.play(FadeIn(prompt_mark, scale=0.96), GrowArrow(arrow), FadeIn(benchmark, shift=LEFT * 0.1), run_time=1.15)
        self.play(FadeIn(hook, shift=UP * 0.08), Circumscribe(benchmark, color=self.language), run_time=1.0)
        self.wait(0.35)
        self.cleanup(title, subtitle, capabilities, prompt_mark, benchmark, arrow, hook)

    def table_card(self, title, headers, rows, color):
        card_width = 4.12
        card_height = 2.62
        title_mob = self.text(title, color, 15.5, 3.55, weight=BOLD, line_spacing=0.88)
        line = Line(LEFT, RIGHT, color=GREY_B).set_width(3.35)
        row_mobs = []
        all_rows = [headers] + rows
        for r, values in enumerate(all_rows):
            is_header = r == 0
            is_ours = r == len(all_rows) - 1
            cells = VGroup()
            for c, value in enumerate(values):
                cell_w = 1.75 if c == 0 else 0.9
                rect = Rectangle(
                    width=cell_w,
                    height=0.28,
                    stroke_width=0,
                    fill_color=self.connector if is_ours else self.panel,
                    fill_opacity=0.2 if is_ours else 0,
                )
                txt_color = BLACK if is_ours else (GREY_B if is_header else WHITE)
                if isinstance(value, list):
                    label = self.arrow_text(value, txt_color, 10.5 if c == 0 else 11.5, cell_w - 0.08, weight=BOLD if is_header or is_ours else NORMAL)
                else:
                    label = self.text(str(value), txt_color, 10.5 if c == 0 else 11.5, cell_w - 0.08, weight=BOLD if is_header or is_ours else NORMAL)
                label.move_to(rect)
                cells.add(VGroup(rect, label))
            cells.arrange(RIGHT, buff=0.02)
            row_mobs.append(cells)
        table = VGroup(*row_mobs).arrange(DOWN, buff=0.02)
        content = VGroup(title_mob, line, table).arrange(DOWN, buff=0.11)
        if content.height > card_height - 0.28:
            content.set_height(card_height - 0.28)
        if content.width > card_width - 0.32:
            content.set_width(card_width - 0.32)
        return self.card(card_width, card_height, color, content, fill_opacity=0.08, radius=0.08)

    def scene_sota_tables(self):
        title = self.make_title("SoTA Across Multiple Task Groups")
        tables = VGroup(
            self.table_card("Object recognition\nVisual7W", ["Method", "Acc"], [
                ["12in1", "83.35"], ["GPT4ROI-7B", "81.83"], ["Shikra-13B", "85.33"], ["Ours-13B", "87.91"],
            ], self.visual),
            self.table_card("Object counting\nPointQA", ["Method", "Acc"], [
                ["Point&ask", "60.20"], ["LLaVA-1.5", "57.93"], ["Shikra-13B", "70.30"], ["Ours-13B", "71.77"],
            ], self.orange),
            self.table_card("Visual Reasoning\nVCR", ["Model", ["Q", "AR"]], [
                ["ViLBERT", "54.0"], ["VLBERT-L", "58.9"], ["GPT4RoI", "78.6"], ["Ours-7B", "78.93"],
            ], self.language),
            self.table_card("Region Captioning\nRefCOCOg", ["Model", "CIDEr"], [
                ["GRIT", "71.6"], ["Kosmos-2", "62.3"], ["GLaMM", "105.0"], ["Ours-7B", "105.9"],
            ], self.connector),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.22, 0.24)).scale(0.88).move_to(UP * 0.18)
        summary = self.card(
            9.5,
            0.55,
            self.connector,
            self.text("SoTA on recognition, counting, captioning, and commonsense reasoning tasks", BLACK, 18, 9.0, weight=BOLD),
            fill_opacity=0.9,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, scale=0.96) for t in tables], lag_ratio=0.12), run_time=1.6)
        for table in tables:
            self.play(Circumscribe(table, color=table[0].get_stroke_color()), run_time=0.35)
        self.play(FadeIn(summary, shift=UP * 0.08), run_time=0.8)
        self.wait(0.35)
        self.cleanup(title, tables, summary)

    def scene_visual_prompt_benchmark(self):
        title = self.make_title("Visual Prompt Understanding Benchmark")
        center = self.card(
            3.0,
            1.35,
            self.connector,
            VGroup(
                self.text("303", BLACK, 42, 2.1, weight=BOLD),
                self.text("complex questions", BLACK, 17, 2.5, weight=BOLD),
            ).arrange(DOWN, buff=0.02),
            fill_opacity=0.9,
        ).move_to(ORIGIN)
        labels = [
            ("Perception\nvisual grounding", self.visual, LEFT * 4.2 + UP * 1.65),
            ("OCR\nreading text", self.connector, LEFT * 4.15 + DOWN * 1.55),
            ("World knowledge\ncommonsense", self.language, UP * 2.25),
            ("Math\ncalculation", self.orange, DOWN * 2.2),
            ("Relation reasoning\nobject relations", self.warning, RIGHT * 4.2 + UP * 1.55),
            ("Language generation\nanswer writing", self.language, RIGHT * 4.2 + DOWN * 1.55),
        ]
        nodes = VGroup(*[
            self.card(2.7, 0.74, color, self.text(label, BLACK if color == self.connector else WHITE, 15, 2.4, weight=BOLD, line_spacing=0.82), fill_opacity=0.9 if color == self.connector else 0.14, radius=0.08).move_to(pos)
            for label, color, pos in labels
        ])
        lines = VGroup(*[Line(node.get_center(), center.get_center(), color=GREY_B, stroke_width=1.6).set_opacity(0.45) for node in nodes])
        note = self.text("A single question may require looking at the right region, reading text, comparing, and answering.", self.connector, 17, 9.0, weight=BOLD).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(center, scale=0.9), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.08), Create(lines), run_time=1.4)
        self.play(FadeIn(note, shift=UP * 0.08), Circumscribe(center, color=self.connector), run_time=1.0)
        self.wait(0.35)
        self.cleanup(title, center, nodes, lines, note)

    def scene_vegetable_example(self):
        title = self.make_title("Benchmark Example: OCR + Math + Visual Prompt")
        image = self.image_card(VEGETABLE_IMAGE, width=6.0, height=4.0, color=self.visual).move_to(LEFT * 2.95 + UP * 0.05)
        question = self.card(
            4.55,
            0.72,
            self.connector,
            self.text("Which colored box contains\nthe lowest-price fruit?", BLACK, 18, 4.15, weight=BOLD, line_spacing=0.88),
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.55 + UP * 1.62)
        steps = VGroup(
            self.chip("1. Look at the right region", self.visual, width=3.65, size=14),
            self.chip("2. OCR the price table", self.connector, BLACK, width=3.65, size=14),
            self.chip("3. Compare prices", self.orange, width=3.65, size=15),
            self.chip("4. Identify: orange", self.language, width=3.65, size=15),
        ).arrange(DOWN, buff=0.16).next_to(question, DOWN, buff=0.3)
        answer = self.card(
            4.4,
            0.62,
            self.language,
            self.text("Answer: Orange", WHITE, 19, 4.0, weight=BOLD),
            fill_opacity=0.16,
        ).to_edge(DOWN, buff=0.38).align_to(steps, RIGHT)
        highlights = VGroup(
            Rectangle(width=1.55, height=1.05, color=RED, stroke_width=4).move_to(image.get_center() + LEFT * 0.9 + UP * 0.28),
            Rectangle(width=1.45, height=0.55, color=BLUE, stroke_width=4).move_to(image.get_center() + LEFT * 0.85 + DOWN * 0.52),
            Rectangle(width=1.85, height=0.85, color=GREEN, stroke_width=4).move_to(image.get_center() + RIGHT * 1.18 + DOWN * 0.03),
        )

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), FadeIn(question, shift=LEFT * 0.08), run_time=1.0)
        self.play(LaggedStart(*[Create(h) for h in highlights], lag_ratio=0.15), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in steps], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(answer, shift=UP * 0.08), Circumscribe(steps[-1], color=self.language), run_time=1.0)
        self.wait(0.4)
        self.cleanup(title, image, question, steps, answer, highlights)

    def scene_yollava(self):
        title = self.make_title("Yo'LLaVA: Your Personalized LMM")
        people = VGroup()
        names = ["Noah", "Lina", "Maya", "Max", "Anna"]
        colors = [self.visual, self.orange, self.connector, self.language, self.warning]
        for name, color in zip(names, colors):
            head = Circle(radius=0.28, stroke_color=color, fill_color=color, fill_opacity=0.25)
            body = RoundedRectangle(width=0.62, height=0.55, corner_radius=0.08, stroke_color=color, fill_color=color, fill_opacity=0.12).next_to(head, DOWN, buff=0.04)
            label = self.text(name, WHITE, 15, 0.95, weight=BOLD).next_to(body, DOWN, buff=0.05)
            people.add(VGroup(head, body, label))
        people.arrange(RIGHT, buff=0.42).move_to(LEFT * 2.8 + UP * 0.3)
        maya = people[2]
        highlight = SurroundingRectangle(maya, color=self.connector, buff=0.12, stroke_width=3)
        prompt = self.card(
            4.6,
            0.72,
            self.connector,
            self.text("Do you see <maya>\nin this image?", BLACK, 18, 4.15, weight=BOLD, line_spacing=0.88),
            fill_opacity=0.9,
        ).move_to(RIGHT * 3.15 + UP * 1.35)
        answer = self.card(
            4.6,
            1.18,
            self.language,
            self.text("Yes. Maya is smiling\nand making a peace sign\nat a party.", WHITE, 17, 4.1, weight=BOLD, line_spacing=0.88),
            fill_opacity=0.14,
        ).next_to(prompt, DOWN, buff=0.28)
        shift_text = VGroup(
            self.chip("person", GREY_B, width=1.45),
            Arrow(LEFT, RIGHT, color=self.connector, stroke_width=4).set_width(1.1),
            self.chip("<maya>", self.connector, BLACK, width=1.45),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.45)
        note = self.text("From generic person recognition to a personalized LMM.", self.visual, 18, 7.2, weight=BOLD).next_to(title, DOWN, buff=0.25)

        self.play(Write(title), FadeIn(note, shift=DOWN * 0.08), run_time=0.95)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.08) for p in people], lag_ratio=0.1), run_time=1.1)
        self.play(Create(highlight), FadeIn(prompt, shift=LEFT * 0.08), run_time=0.9)
        self.play(FadeIn(answer, shift=UP * 0.08), FadeIn(shift_text, shift=UP * 0.08), run_time=1.0)
        self.wait(0.35)
        self.cleanup(title, people, highlight, prompt, answer, shift_text, note)

    def scene_matryoshka(self):
        title = self.make_title("Matryoshka Multimodal Models")
        image = self.image_card(MATRYOSHKA_IMAGE, width=6.8, height=3.9, color=self.orange).move_to(LEFT * 2.55 + UP * 0.34)
        controller = self.card(
            3.5,
            0.82,
            self.visual,
            self.text("Granularity Controller", WHITE, 20, 3.1, weight=BOLD),
            fill_opacity=0.14,
        ).move_to(RIGHT * 3.5 + UP * 1.55)
        strips = VGroup()
        for i, count in enumerate([4, 7, 11]):
            row = VGroup(*[
                Rectangle(width=0.22, height=0.28, stroke_width=0, fill_color=interpolate_color(ManimColor(self.visual), ManimColor(self.warning), j / max(1, count - 1)), fill_opacity=0.9)
                for j in range(count)
            ]).arrange(RIGHT, buff=0.03)
            label = self.text(["coarse", "medium", "fine"][i], WHITE, 15, 1.2, weight=BOLD)
            strips.add(VGroup(label, row).arrange(RIGHT, buff=0.16))
        strips.arrange(DOWN, buff=0.18).next_to(controller, DOWN, buff=0.35)
        llm = self.card(3.2, 0.72, self.language, self.text("Large Language Model", WHITE, 17, 2.85, weight=BOLD), fill_opacity=0.14).next_to(strips, DOWN, buff=0.35)
        explain = VGroup(
            self.card(
                4.35,
                0.56,
                self.visual,
                self.arrow_text(["coarse: fewer tokens", "broad view, faster runtime"], WHITE, 14, 4.0, weight=BOLD),
                fill_opacity=0.14,
                radius=0.08,
            ),
            self.card(
                4.35,
                0.56,
                self.orange,
                self.arrow_text(["fine: more tokens", "preserves details for hard questions"], WHITE, 14, 4.0, weight=BOLD),
                fill_opacity=0.14,
                radius=0.08,
            ),
        ).arrange(DOWN, buff=0.12).next_to(llm, DOWN, buff=0.28)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), FadeIn(controller, shift=LEFT * 0.08), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in strips], lag_ratio=0.16), run_time=1.15)
        self.play(FadeIn(llm, shift=UP * 0.08), Circumscribe(controller, color=self.visual), run_time=0.9)
        self.play(FadeIn(explain, shift=UP * 0.08), run_time=1.05)
        self.play(Circumscribe(strips[-1], color=self.orange), run_time=0.85)
        self.wait(0.4)
        self.cleanup(title, image, controller, strips, llm, explain)

    def scene_limitations(self):
        title = self.make_title("Looking Forward: Not quite solved", self.warning)
        blocks = VGroup(
            self.limit_block("Hallucinations", "still unreliable", self.warning),
            self.limit_block("Video understanding", "temporal reasoning", self.visual),
            self.limit_block("Smaller models", "compact but capable", self.orange),
            self.limit_block("OCR emerges?", "why can it read?", self.connector, BLACK),
            self.limit_block(["LLM", "VLM"], "what changes?", self.visual),
            self.limit_block("Instruction tuning", "how knowledge shifts", self.language),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.28, 0.28)).move_to(UP * 0.12)
        note = self.text("SoTA does not mean the problem is solved.", self.connector, 21, 8.0, weight=BOLD).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(block, scale=0.96) for block in blocks], lag_ratio=0.08), run_time=1.35)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.8)
        self.wait(0.35)
        self.cleanup(title, blocks, note)

    def limit_block(self, title, subtitle, color, text_color=WHITE):
        title_mob = (
            self.arrow_text(title, text_color if text_color == BLACK else color, 16, 3.1, weight=BOLD)
            if isinstance(title, list)
            else Text(title, font=TEXT_FONT, font_size=16, color=text_color if text_color == BLACK else color, weight=BOLD)
        )
        return self.card(
            3.55,
            1.16,
            color,
            VGroup(
                title_mob,
                Text(subtitle, font=TEXT_FONT, font_size=15, color=text_color, weight=BOLD),
            ).arrange(DOWN, buff=0.08),
            fill_opacity=0.9 if text_color == BLACK else 0.12,
        )

    def scene_future_directions(self):
        title = self.make_title("Future Directions: Agents and Robot Learning")
        agents = self.card(
            5.75,
            3.15,
            self.language,
            VGroup(
                self.text("Multimodal AI Agents", self.language, 21, 5.05, weight=BOLD),
                self.flow_row(["observe", "reflect", "plan"], self.language, width=1.5, size=14, arrow_width=0.3),
                self.flow_row(["tool/API", "collaborate"], self.connector, BLACK, width=1.9, size=14, arrow_width=0.32),
            ).arrange(DOWN, buff=0.34),
            fill_opacity=0.1,
        ).move_to(LEFT * 3.08 + UP * 0.08)
        obstacle = Square(side_length=0.55, color=self.warning, fill_opacity=0.12)
        target = Circle(radius=0.23, color=self.language, fill_opacity=0.2)
        robot_visual = VGroup(obstacle, target).arrange(RIGHT, buff=-0.05)
        robot = self.card(
            5.75,
            3.15,
            self.visual,
            VGroup(
                self.text("Robot Learning / PIVOT", self.visual, 21, 5.05, weight=BOLD),
                robot_visual,
                self.text("Visual prompts guide actions\nin physical space", WHITE, 16, 5.0, weight=BOLD, line_spacing=0.88),
            ).arrange(DOWN, buff=0.23),
            fill_opacity=0.1,
        ).move_to(RIGHT * 3.08 + UP * 0.08)
        robot_path = VMobject(color=self.connector, stroke_width=6)
        robot_path.set_points_smoothly([LEFT * 1.1 + DOWN * 0.25, LEFT * 0.45 + UP * 0.35, RIGHT * 0.2 + UP * 0.05, RIGHT * 0.95 + UP * 0.52])
        robot_path.move_to(robot_visual.get_center() + UP * 0.18)
        insight = self.card(
            10.2,
            0.58,
            self.connector,
            self.text("Beyond image QA: models begin to plan and interact with the environment.", BLACK, 17, 9.7, weight=BOLD),
            fill_opacity=0.9,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(agents, shift=RIGHT * 0.08), FadeIn(robot, shift=LEFT * 0.08), run_time=1.1)
        self.play(Create(robot_path), Circumscribe(agents, color=self.language), run_time=1.0)
        self.play(FadeIn(insight, shift=UP * 0.08), run_time=0.8)
        self.wait(0.35)
        self.cleanup(title, agents, robot, robot_path, insight)

    def scene_multimodal_agents_detail(self):
        title = self.make_title("Multimodal AI Agents: From QA to Action", self.language)

        perception = self.card(
            3.2,
            2.35,
            self.visual,
            VGroup(
                self.text("Perception", self.visual, 21, 2.7, weight=BOLD),
                self.text("understands the environment", WHITE, 15, 2.85, weight=BOLD),
                VGroup(
                    self.chip("image", self.visual, width=1.35, size=14),
                    self.chip("audio", self.visual, width=1.35, size=14),
                    self.chip("TXT", self.visual, width=1.35, size=14),
                    self.chip("map", self.visual, width=1.35, size=14),
                ).arrange_in_grid(rows=2, cols=2, buff=(0.12, 0.12)),
            ).arrange(DOWN, buff=0.16),
            fill_opacity=0.1,
        ).move_to(LEFT * 4.25 + UP * 0.35)

        storage = self.card(
            1.65,
            0.68,
            self.connector,
            self.text("Storage\nmemory + knowledge", BLACK, 15, 1.65, weight=BOLD, line_spacing=0.86),
            fill_opacity=0.9,
            radius=0.08,
        )
        decision = self.card(
            1.65,
            0.68,
            self.orange,
            self.text("Decision\nplanning + reasoning", WHITE, 15, 1.65, weight=BOLD, line_spacing=0.86),
            fill_opacity=0.18,
            radius=0.08,
        )
        brain_inner = VGroup(storage, decision).arrange(DOWN, buff=0.14)
        brain = self.card(
            3.35,
            2.7,
            self.language,
            VGroup(
                self.text("Brain", self.language, 23, 2.8, weight=BOLD),
                self.text("summarize, remember,\nlearn, retrieve", WHITE, 14, 2.65, weight=BOLD, line_spacing=0.9),
                brain_inner,
            ).arrange(DOWN, buff=0.13),
            fill_opacity=0.12,
        ).move_to(UP * 0.35)

        action = self.card(
            3.2,
            2.35,
            self.orange,
            VGroup(
                self.text("Action", self.orange, 21, 2.7, weight=BOLD),
                self.text("turns reasoning into action", WHITE, 14, 2.7, weight=BOLD),
                VGroup(
                    self.chip("Text", self.orange, width=1.5, size=14),
                    self.chip("Tools/API", self.connector, BLACK, width=1.9, size=14),
                    self.chip("Embodiment", self.orange, width=2.2, size=14),
                ).arrange(DOWN, buff=0.1),
            ).arrange(DOWN, buff=0.15),
            fill_opacity=0.1,
        ).move_to(RIGHT * 4.25 + UP * 0.35)

        arrow_1 = Arrow(perception.get_right(), brain.get_left(), color=self.connector, stroke_width=4, buff=0.18)
        arrow_2 = Arrow(brain.get_right(), action.get_left(), color=self.connector, stroke_width=4, buff=0.18)
        feedback = CurvedArrow(action.get_bottom(), perception.get_bottom(), angle=-TAU / 5, color=self.language, stroke_width=3)
        feedback_label = self.text("Environment feedback", self.language, 15, 2.75, weight=BOLD).next_to(feedback, DOWN, buff=0.05)

        example = self.card(
            10.7,
            0.82,
            self.connector,
            self.arrow_text(
                ["Example: observe the sky + call a weather API", "infer rain", "robot brings an umbrella."],
                BLACK,
                17,
                10.1,
                weight=BOLD,
            ),
            fill_opacity=0.9,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(perception, shift=RIGHT * 0.08), run_time=0.8)
        self.play(GrowArrow(arrow_1), FadeIn(brain, scale=0.96), run_time=0.95)
        self.play(GrowArrow(arrow_2), FadeIn(action, shift=LEFT * 0.08), run_time=0.95)
        self.play(Create(feedback), FadeIn(feedback_label), run_time=0.9)
        self.play(FadeIn(example, shift=UP * 0.08), run_time=0.8)
        self.wait(0.45)
        self.cleanup(title, perception, brain, action, arrow_1, arrow_2, feedback, feedback_label, example)

    def scene_robot_learning_pivot(self):
        title = self.make_title("Robot Learning / PIVOT: Visual Prompts Become Actions", self.visual)

        image = self.image_card(ROBOT_IMAGE, width=5.65, height=3.55, color=self.visual).move_to(LEFT * 3.35 + UP * 0.15)
        loop_note = self.card(
            5.25,
            0.65,
            self.connector,
            self.text("Iterative visual prompting: draw, observe, revise, then act.", BLACK, 15, 4.9, weight=BOLD),
            fill_opacity=0.9,
        ).next_to(image, DOWN, buff=0.26)

        tasks = VGroup(
            self.robot_task_card("Pick and place", "pick up toy, put pepper\nshaker on pink plate", self.orange),
            self.robot_task_card("Avoid obstacles", "draw a safe trajectory\naround the obstacle", self.visual),
            self.robot_task_card("Sort recycling", "arrow points to the correct bin\nfor the Coca-Cola can", self.language),
        ).arrange(DOWN, buff=0.16).move_to(RIGHT * 3.25 + UP * 0.1)

        prompt_marks = VGroup(
            Circle(radius=0.18, color=self.connector, stroke_width=4).move_to(image.get_center() + LEFT * 0.72 + UP * 0.33),
            Arrow(image.get_center() + LEFT * 0.2 + UP * 0.95, image.get_center() + LEFT * 0.64 + UP * 0.45, color=self.connector, stroke_width=5, buff=0.05),
            VMobject(color=self.connector, stroke_width=5),
        )
        prompt_marks[-1].set_points_smoothly([
            image.get_center() + LEFT * 1.0 + DOWN * 0.85,
            image.get_center() + LEFT * 0.2 + DOWN * 0.35,
            image.get_center() + RIGHT * 0.55 + DOWN * 0.75,
        ])

        takeaway = self.card(
            10.5,
            0.64,
            self.language,
            self.text("PIVOT moves visual-prompt understanding from the screen into physical space.", WHITE, 17, 9.9, weight=BOLD),
            fill_opacity=0.14,
        ).to_edge(DOWN, buff=0.28)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(image, scale=0.96), run_time=0.9)
        self.play(LaggedStart(Create(prompt_marks[0]), GrowArrow(prompt_marks[1]), Create(prompt_marks[2]), lag_ratio=0.18), run_time=1.25)
        self.play(FadeIn(loop_note, shift=UP * 0.08), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(task, shift=LEFT * 0.08) for task in tasks], lag_ratio=0.16), run_time=1.25)
        self.play(FadeIn(takeaway, shift=UP * 0.08), Circumscribe(tasks[-1], color=self.connector), run_time=0.95)
        self.wait(0.45)
        self.cleanup(title, image, loop_note, tasks, prompt_marks, takeaway)

    def robot_task_card(self, title, subtitle, color):
        return self.card(
            4.45,
            1.02,
            color,
            VGroup(
                Text(title, font=TEXT_FONT, font_size=17, color=color, weight=BOLD),
                self.text(subtitle, WHITE, 15, 4.05, weight=BOLD, line_spacing=0.86),
            ).arrange(DOWN, buff=0.07),
            fill_opacity=0.11,
            radius=0.1,
        )

    def flow_row(self, labels, color, text_color=WHITE, width=1.45, size=14, arrow_width=0.42):
        parts = VGroup(*[self.chip(label, color, text_color, width=width, size=size) for label in labels])
        arrows = VGroup(*[
            Arrow(LEFT, RIGHT, color=color if text_color == WHITE else BLACK, stroke_width=3).set_width(arrow_width)
            for _ in range(len(parts) - 1)
        ])
        row = VGroup()
        for i, part in enumerate(parts):
            row.add(part)
            if i < len(arrows):
                row.add(arrows[i])
        row.arrange(RIGHT, buff=0.08)
        return row

    def scene_conclusion(self):
        title = self.make_arrow_title("Conclusion: Specialist", "Generalist")
        specialists = VGroup(*[
            self.chip(label, color, width=1.9, size=15)
            for label, color in [
                ("OCR", self.visual),
                ("detection", self.orange),
                ("captioning", self.language),
                ("VQA", self.connector),
                ("robot policy", self.warning),
            ]
        ]).arrange(DOWN, buff=0.14).move_to(LEFT * 4.0 + UP * 0.05)
        specialist_title = self.text("Specialist models", GREY_B, 18, 3.0, weight=BOLD).next_to(specialists, UP, buff=0.26)
        generalist = self.card(
            4.4,
            2.1,
            self.language,
            VGroup(
                self.text("Generalist\nmulti-modal model", self.language, 26, 3.8, weight=BOLD, line_spacing=0.9),
                self.text("image + visual prompt + text + tools", WHITE, 16, 3.9, weight=BOLD),
            ).arrange(DOWN, buff=0.18),
            fill_opacity=0.14,
        ).move_to(RIGHT * 2.7 + UP * 0.1)
        arrow = Arrow(specialists.get_right(), generalist.get_left(), color=self.connector, stroke_width=5, buff=0.18)
        tagline = self.card(
            9.1,
            0.62,
            self.connector,
            self.arrow_text(["Foundation models + semi-automatic data", "controllable visual understanding"], BLACK, 17, 8.6, weight=BOLD),
            fill_opacity=0.9,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(specialist_title), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in specialists], lag_ratio=0.08), run_time=1.1)
        self.play(GrowArrow(arrow), FadeIn(generalist, scale=0.96), run_time=1.1)
        self.play(
            specialists.animate.set_opacity(0.38),
            specialist_title.animate.set_opacity(0.55),
            FadeIn(tagline, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(Circumscribe(generalist, color=self.language), run_time=0.9)
        self.wait(0.55)
