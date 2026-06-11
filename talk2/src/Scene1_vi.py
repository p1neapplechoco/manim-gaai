from manim import *
from pathlib import Path


IMAGE_DIR = Path(__file__).resolve().parents[1] / "assets"
TEXT_FONT = "Times New Roman"


def image_path(filename):
    return str(IMAGE_DIR / filename)


TIME_SCALE = 1.5


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


class Scene1(ScaledTimingMixin, Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1: Intro
        title = Text('Generalist Multimodal Models', font=TEXT_FONT, font_size=40, line_spacing=1.2)
        intro_group = VGroup(title)
        
        self.play(LaggedStart(*[Write(m) for m in intro_group], lag_ratio=0.5), run_time=2)
        self.wait(2)
        self.play(FadeOut(intro_group, shift=UP*0.3), run_time=1.5)

        # 2: Computer Vision deep learning era and six tasks
        cv_title = Text('The Deep Learning Era in Computer Vision\n(2012 - Present)', font=TEXT_FONT, font_size=36).to_edge(UP)
        self.play(Write(cv_title), run_time=1.5)
        
        task_names = [
            'Classification', 'Object Detection', 'Pose Recognition',
            'Segmentation', '3D Prediction', 'Surface normal Prediction'
        ]
        task_images = [
            image_path('Classification.png'),
            image_path('Object detection.png'),
            image_path('Pose recognition.png'),
            image_path('Segmentation.png'),
            image_path('3D prediction.png'),
            image_path('Surface normal prediction.png'),
        ]

        task_vgroups = Group()
        for name, img_path in zip(task_names, task_images):
            task_text = Text(name, font=TEXT_FONT, font_size=18)
            task_img = ImageMobject(img_path).scale(0.7)
            task_img.next_to(task_text, UP, buff=0.2)
            task_vgroups.add(Group(task_img, task_text))

        task_vgroups.arrange_in_grid(rows=2, cols=3, buff=0.7).next_to(cv_title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(task, shift=UP*0.2) for task in task_vgroups], lag_ratio=0.1), run_time=2.5)
        self.wait(2)
        self.play(FadeOut(Group(cv_title, task_vgroups), shift=DOWN*0.3), run_time=1.5)

        # 3: Computer Vision research growth
        trend_text = Text("The research boom in Computer Vision", 
                         font=TEXT_FONT, font_size=32, weight=BOLD, color=YELLOW).to_edge(UP)
        self.play(Write(trend_text), run_time=1)

        axes = NumberPlane(
            x_range=[2006, 2024, 2], 
            y_range=[0, 10000, 2000], 
            x_length=9, 
            y_length=5,
            axis_config={"include_numbers": True, "font_size": 20},
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            }
        ).shift(DOWN*0.5)

        self.play(Create(axes), run_time=1.5)

        years = list(range(2006, 2024))
        blue_data = [1131, 1250, 1593, 1464, 1724, 1677, 1933, 1798, 1807, 2123, 2145, 2680, 3309, 5165, 6424, 7093, 8161, 9155]
        red_data = [318, 353, 508, 383, 462, 440, 466, 472, 540, 602, 643, 783, 979, 1294, 1467, 1661, 2063, 2359]

        blue_graph = axes.plot_line_graph(
            x_values=years, y_values=blue_data, line_color=BLUE,
            add_vertex_dots=True, vertex_dot_radius=0.04
        )
        red_graph = axes.plot_line_graph(
            x_values=years, y_values=red_data, line_color=RED,
            add_vertex_dots=True, vertex_dot_radius=0.04
        )

        blue_label = Text('9155 Submitted', font=TEXT_FONT, color=BLUE, font_size=16).next_to(axes.c2p(years[-1], blue_data[-1]), UP)
        red_label = Text('2359 Accepted', font=TEXT_FONT, color=RED, font_size=16).next_to(axes.c2p(years[-1], red_data[-1]), RIGHT)

        self.play(
            Create(blue_graph, run_time=3),
            Create(red_graph, run_time=3),
            LaggedStart(Write(blue_label), Write(red_label), lag_ratio=0.5)
        )

        # 4: Limitations
        self.play(FadeOut(VGroup(trend_text, axes, blue_graph, red_graph, blue_label, red_label)), run_time=1)

        limitation_title = Text('Limitations of Traditional Computer Vision', font=TEXT_FONT, color=RED, font_size=36, weight=BOLD).to_edge(UP)
        self.play(Write(limitation_title), run_time=1)

        prevail_text = Text('Specialist models', font=TEXT_FONT, color=YELLOW, font_size=32).next_to(limitation_title, DOWN, buff=0.5)
        limit_text = Text('Each model solves only one narrow task', font=TEXT_FONT, color=WHITE, font_size=28).next_to(prevail_text, DOWN, buff=0.3)
        
        self.play(LaggedStart(FadeIn(prevail_text), Write(limit_text), lag_ratio=0.5), run_time=2)

        def limitation_row(task, result):
            bullet = MathTex(r"\bullet", color=LIGHT_GREY, font_size=28)
            task_text = Text(task, font=TEXT_FONT, font_size=24, color=LIGHT_GREY)
            arrow = MathTex(r"\rightarrow", color=YELLOW, font_size=26)
            result_text = Text(result, font=TEXT_FONT, font_size=24, color=LIGHT_GREY)
            return VGroup(bullet, task_text, arrow, result_text).arrange(RIGHT, buff=0.16)

        limitation_rows = VGroup(
            limitation_row("Image classification", "one dedicated model"),
            limitation_row("Object detection", "one dedicated model"),
            limitation_row("Semantic segmentation", "one dedicated model"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)

        takeaway = VGroup(
            MathTex(r"\Longrightarrow", color=RED_C, font_size=30),
            Text("Expensive, resource-heavy, and hard to scale!", font=TEXT_FONT, font_size=28, color=RED_C, weight=BOLD),
        ).arrange(RIGHT, buff=0.18)

        bullet_points = VGroup(limitation_rows, takeaway).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        bullet_points.next_to(limit_text, DOWN, buff=0.72).to_edge(LEFT, buff=1.65)
        
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT*0.2) for p in bullet_points], lag_ratio=0.3), run_time=3)
        self.wait(1.5)

        transition_text = Text('That is why Foundation Models began to rise...', 
                              font=TEXT_FONT, font_size=30, color=GREEN, weight=BOLD).next_to(bullet_points, DOWN, buff=0.8)
        self.play(FadeIn(transition_text, shift=UP*0.2), run_time=1)
        self.wait(1.5)

        # 5: Foundation Models (The modern era)
        self.play(FadeOut(VGroup(limitation_title, prevail_text, limit_text, bullet_points, transition_text)), run_time=1)

        gen_title = Text('The Rise of Foundation Models\n(2020s)', font=TEXT_FONT, font_size=36, color=WHITE).to_edge(UP, buff=0.2)
        gen_subtitle = Text('One model, many tasks',
                           font=TEXT_FONT, font_size=28, color=GREEN).next_to(gen_title, DOWN, buff=0.2)
        
        self.play(LaggedStart(Write(gen_title), Write(gen_subtitle), lag_ratio=0.5), run_time=2)

        foundation_img = ImageMobject(image_path("Foundation Model.png")).scale(0.51)
        foundation_img.shift(LEFT * 3.5 + DOWN * 0.4)
        self.play(FadeIn(foundation_img, shift=RIGHT*0.3), run_time=1)

        examples = VGroup(
            Text('Language Models\n(GPT-4, Llama 3)', font=TEXT_FONT, font_size=24, color=BLUE),
            Text('Vision Models\n(SAM, DINOv2)', font=TEXT_FONT, font_size=24, color=YELLOW),
            Text('Multimodal Models\n(Gemini, CLIP)', font=TEXT_FONT, font_size=24, color=RED_C)
        ).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(RIGHT * 3.5 + DOWN * 0.4)
        
        arrows = VGroup(*[
            Arrow(foundation_img.get_right(), ex.get_left(), buff=0.2, color=WHITE)
            for ex in examples
        ])

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(ex, shift=RIGHT*0.2) for ex in examples], lag_ratio=0.2), run_time=1.5)
        self.wait(3)

        # 6: Large Generalist Multimodal Models (LMMs)
        self.play(FadeOut(Group(gen_title, gen_subtitle, foundation_img, examples, arrows)), run_time=1)

        lmm_title = Text('Large Generalist Multimodal Models (LMMs)', font=TEXT_FONT, font_size=36, color=BLUE).to_edge(UP, buff=0.5)
        lmm_desc = Text(
            'Models that combine language and vision,\n'
            'understand visual data, and communicate\n'
            'naturally in human language.',
            font=TEXT_FONT, font_size=28, line_spacing=1.5, t2c={'language': YELLOW, 'vision': YELLOW, 'visual data': GREEN, 'communicate': GREEN}
        ).next_to(lmm_title, DOWN, buff=0.7)

        self.play(Write(lmm_title), run_time=1.5)
        self.play(FadeIn(lmm_desc, shift=UP*0.2), run_time=2)
        self.wait(2)

        challenge_text = Text(
            'Core challenge:', font=TEXT_FONT, font_size=30, color=RED, weight=BOLD
        ).next_to(lmm_desc, DOWN, buff=1.0)
        challenge_desc = Text(
            'How can we train these models effectively\n'
            'with only a minimal amount of supervised data?',
            font=TEXT_FONT, font_size=26, line_spacing=1.2
        ).next_to(challenge_text, DOWN, buff=0.3)

        self.play(LaggedStart(FadeIn(challenge_text, shift=RIGHT*0.2), Write(challenge_desc), lag_ratio=0.5), run_time=2.5)
        self.wait(2)
        
        self.play(FadeOut(VGroup(lmm_desc, challenge_text, challenge_desc)), run_time=1)

        solution_title = Text('Breakthrough strategy', font=TEXT_FONT, font_size=32, color=GREEN, weight=BOLD).next_to(lmm_title, DOWN, buff=1.0)
        solution_desc1 = Text('Fine-tune pretrained foundation models', font=TEXT_FONT, font_size=26).next_to(solution_title, DOWN, buff=0.4)
        solution_plus = Text('+', font=TEXT_FONT, font_size=30, color=YELLOW, weight=BOLD).next_to(solution_desc1, DOWN, buff=0.3)
        solution_desc2 = Text('Design semi-automatic data collection methods', font=TEXT_FONT, font_size=26).next_to(solution_plus, DOWN, buff=0.3)

        self.play(FadeIn(solution_title, shift=UP*0.2), run_time=1)
        self.play(Write(solution_desc1), run_time=1.5)
        self.play(FadeIn(solution_plus), run_time=0.5)
        self.play(Write(solution_desc2), run_time=1.5)
        self.wait(3)
