import sys
import numpy as np
from pathlib import Path

CMD = Path(sys.argv[0]).name.lower()

if "manimgl" in CMD:
    from manimlib import *
else:
    from manim import *

from pathlib import Path

BASE_DIR = Path("/home/pineapple/Desktop/projects/manim-gaai")


class IntroductionGAA(Scene):
    def text_bubble(
        self,
        text,
        color=WHITE,
        font_size=24,
        padding=0.35,
        corner_radius=0.3,
        stroke_width=2.5,
        fill_color="#0D0D0D",
        fill_opacity=1,
        text_color=WHITE,
        line_spacing=1.4,
    ):
        lines = text.split("\n")

        line_mobs = VGroup(
            *[Text(line, font_size=font_size, color=text_color) for line in lines]
        )

        line_height = line_mobs[0].get_height() if len(line_mobs) > 0 else 0.4
        for i, lm in enumerate(line_mobs):
            lm.move_to(ORIGIN + DOWN * i * line_height * line_spacing)

        line_mobs.move_to(ORIGIN)

        text_w = max(lm.get_width() for lm in line_mobs) if len(line_mobs) > 0 else 0.4
        text_h = line_mobs.get_height()
        box = RoundedRectangle(
            width=text_w + padding * 2,
            height=text_h + padding * 2,
            corner_radius=corner_radius,
            color=color,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
        )

        line_mobs.move_to(box.get_center())

        return VGroup(box, line_mobs)

    def AdaptiveFlash(self, mobject, **kwargs):
        w = mobject.get_width()
        h = mobject.get_height()
        radius = ((w / 2) ** 2 + (h / 2) ** 2) ** 0.5 + 0.3

        flash = Flash(
            mobject.get_center(),
            flash_radius=radius,
            **kwargs,
        )

        return flash

    def construct(self):
        # Crowd and robot interaction
        robot = SVGMobject(str(BASE_DIR / "assets/svgs/robot.svg"))
        robot.scale(1.25)
        robot.set_color(WHITE)
        robot.move_to(ORIGIN)

        crowd = SVGMobject(str(BASE_DIR / "assets/svgs/crowd.svg"))
        crowd.scale(0.8)
        crowd.set_color(WHITE)
        crowd.to_edge(LEFT)

        computer = SVGMobject(str(BASE_DIR / "assets/svgs/computer.svg"))
        computer.set_width(crowd.get_width())
        computer.set_color(WHITE)
        computer.to_edge(RIGHT)

        self.play(
            DrawBorderThenFill(robot),
            DrawBorderThenFill(crowd),
            DrawBorderThenFill(computer),
            run_time=4,
        )

        question_answer_pairs = [
            ("What is 1 + 1?", "2"),
            ("Explain gravity.", "Gravity is ..."),
            ("Design a system to ...", "Sure, let's start \nby ..."),
        ]

        for question, answer in question_answer_pairs:
            question_bubble = self.text_bubble(question, color=BLUE)
            answer_bubble = self.text_bubble(answer, color=GREEN)

            question_bubble.next_to(crowd, DOWN)
            answer_bubble.next_to(computer, DOWN)

            ask_arrow = Arrow(
                crowd.get_right(),
                robot.get_left(),
                buff=0.1,
                color=BLUE,
            )
            answer_arrow = Arrow(
                robot.get_right(),
                computer.get_left(),
                buff=0.1,
                color=GREEN,
            )

            self.play(
                FadeIn(question_bubble),
                GrowArrow(ask_arrow),
                run_time=2,
            )

            self.play(
                self.AdaptiveFlash(
                    robot,
                    line_length=0.5,
                    num_lines=20,
                ),
            )

            self.play(
                FadeIn(answer_bubble),
                GrowArrow(answer_arrow),
                run_time=2,
            )

            self.wait(1)
            self.play(
                FadeOut(question_bubble),
                FadeOut(answer_bubble),
                FadeOut(ask_arrow),
                FadeOut(answer_arrow),
                run_time=1,
            )

        # But recently, ...
        crowd_bubble = self.text_bubble("Goal", color=YELLOW)
        crowd_bubble.next_to(crowd, DOWN)
        self.play(
            FadeIn(crowd_bubble),
            run_time=2,
        )

        crowd_to_robot = Arrow(
            crowd.get_right(),
            robot.get_left(),
            buff=0.1,
            color=YELLOW,
        )
        self.play(
            GrowArrow(crowd_to_robot),
            run_time=1.0,
        )

        environment_bubble = self.text_bubble("Environment", color=ORANGE)
        environment_bubble.next_to(robot, DOWN, buff=1)
        self.play(
            FadeIn(environment_bubble),
            run_time=2,
        )

        ### trobt to environment should be labeled observe
        robot_to_environment = Arrow(
            robot.get_bottom() + LEFT * 0.2,
            environment_bubble.get_top() + LEFT * 0.2,
            buff=0.1,
            color=ORANGE,
        )
        label_observe = Text("Observe", font_size=20, color=ORANGE)
        label_observe.next_to(robot_to_environment, LEFT, buff=0.1)

        environment_to_robot = Arrow(
            environment_bubble.get_top() + RIGHT * 0.2,
            robot.get_bottom() + RIGHT * 0.2,
            buff=0.1,
            color=ORANGE,
        )
        label_observation = Text("Observation", font_size=20, color=ORANGE)
        label_observation.next_to(environment_to_robot, RIGHT, buff=0.1)

        self.play(
            FadeIn(label_observe),
            GrowArrow(robot_to_environment),
            run_time=1.0,
        )

        self.wait(1)

        self.play(
            FadeIn(label_observation),
            GrowArrow(environment_to_robot),
            run_time=1.0,
        )
        self.wait(2)

        language_bubble = self.text_bubble("Language", color=PURPLE)
        action_bubble = self.text_bubble("Action", color=RED)

        language_bubble.move_to(computer.get_center() + UP * 0.75)
        action_bubble.move_to(computer.get_center() + DOWN * 0.75)

        arrow_to_language = Arrow(
            robot.get_right(),
            language_bubble.get_left(),
            buff=0.1,
            color=PURPLE,
        )
        arrow_to_action = Arrow(
            robot.get_right(),
            action_bubble.get_left(),
            buff=0.1,
            color=RED,
        )

        self.play(
            self.AdaptiveFlash(
                robot,
                color=YELLOW,
                line_length=0.5,
                num_lines=20,
            )
        )

        self.play(
            FadeOut(computer),
            GrowArrow(arrow_to_language),
            GrowArrow(arrow_to_action),
            FadeIn(language_bubble),
            FadeIn(action_bubble),
            run_time=1.5,
        )
        self.wait(2)

        self.play(
            FadeOut(*self.mobjects),
            run_time=2,
        )

        # transition to the title

        letters = ["G", "A", "A"]
        words = ["Generalist", "Agent", "AI"]
        colors = [GOLD, PURE_CYAN, WHITE]

        letter_mobs = VGroup(
            *[
                Text(l, font_size=96, color=c, weight=BOLD)
                for l, c in zip(letters, colors)
            ]
        )
        letter_mobs.arrange(RIGHT, buff=1.2).move_to(UP * 0.6)

        word_mobs = VGroup(
            *[Text(w, font_size=26, color=c) for w, c in zip(words, colors)]
        )
        for wm, lm in zip(word_mobs, letter_mobs):
            wm.move_to(lm.get_center() + DOWN * 1.0)

        for lm, wm in zip(letter_mobs, word_mobs):
            self.play(Write(lm), run_time=0.55)
            self.play(FadeIn(wm, shift=DOWN * 0.2), run_time=0.4)

        # glow around each letter
        for lm in letter_mobs:
            flash = Circumscribe(lm)
            self.play(flash, run_time=1.0)

        self.wait(1.0)
        self._gaa_group = VGroup(letter_mobs, word_mobs)
        letter_mobs, word_mobs = self._gaa_group

        # Shrink & shift GAA upward
        self.play(
            self._gaa_group.animate.scale(0.55).to_edge(UP, buff=0.35),
            run_time=0.7,
        )

        generatlist_bubble = self.text_bubble(
            text="Understands and generates \nlanguage, images, code, \nand more",
            color=GOLD,
            font_size=19,
            line_spacing=1.3,
        )
        generatlist_bubble.move_to(LEFT * 3.2 + DOWN * 0.5)

        gen_line = DashedLine(
            generatlist_bubble.get_top(),
            letter_mobs[0].get_bottom() + DOWN * 0.05,
            color=GOLD,
            dash_length=0.1,
        )

        agent_bubble = self.text_bubble(
            text="Interacts with the environment \nto achieve goals",
            color=PURE_CYAN,
            font_size=19,
            line_spacing=1.3,
        )
        agent_bubble.move_to(RIGHT * 3.2 + DOWN * 0.5)
        agt_line = DashedLine(
            agent_bubble.get_top(),
            letter_mobs[1].get_bottom() + DOWN * 0.05,
            color=PURE_CYAN,
            dash_length=0.1,
        )

        self.play(Write(generatlist_bubble), Write(agent_bubble), run_time=1.5)
        self.play(Create(gen_line), Create(agt_line), run_time=1.5)
        self.wait(5.0)

        self.play(
            FadeOut(
                VGroup(
                    generatlist_bubble,
                    gen_line,
                    agent_bubble,
                    agt_line,
                    self._gaa_group,
                )
            ),
            run_time=0.8,
        )

        # "How did we get here?"
        hook_text = Text("How did we get here?", font_size=36, color=WHITE)
        question_mark = hook_text[-1]

        self.play(Write(hook_text), run_time=2.0)

        self.play(
            Wiggle(
                question_mark,
                scale_value=1.4,
                rotation_angle=0.06 * TAU,
                n_wiggles=5,
            ),
            run_time=1.5,
            rate_func=smooth,
        )

        self.play(
            FadeOut(hook_text),
            run_time=0.5,
        )

        # going back in time
        face = Circle(radius=1.5, fill_color="#111111", fill_opacity=1, stroke_width=2)
        face.move_to(ORIGIN)

        # tick marks
        ticks = VGroup()
        for i in range(12):
            angle = i * TAU / 12
            outer = face.get_center() + 1.5 * np.array(
                [np.sin(angle), np.cos(angle), 0]
            )
            inner = face.get_center() + 1.25 * np.array(
                [np.sin(angle), np.cos(angle), 0]
            )
            ticks.add(Line(inner, outer, stroke_width=1.5))

        # hands
        minute_hand = Line(
            face.get_center(),
            face.get_center() + UP * 1.1,
            color=WHITE,
            stroke_width=3,
        )
        hour_hand = Line(
            face.get_center(),
            face.get_center() + UP * 0.7,
            color="#C8A96E",
            stroke_width=4,
        )
        center_dot = Dot(face.get_center(), radius=0.07, color=WHITE)

        clock = VGroup(face, ticks, minute_hand, hour_hand, center_dot)

        self.play(FadeIn(clock, scale=0.7), run_time=0.8)
        self.wait(0.5)
        self.play(
            Rotating(
                minute_hand,
                angle=4 * TAU,
                about_point=face.get_center(),
                run_time=2.5,
                rate_func=linear,
            ),
            Rotating(
                hour_hand,
                angle=TAU,
                about_point=face.get_center(),
                run_time=2.5,
                rate_func=linear,
            ),
            run_time=2.5,
        )

        flash_rect = Rectangle(
            width=config.frame_width * 2,
            height=config.frame_height * 2,
            fill_color=WHITE,
            fill_opacity=0,
            stroke_width=0,
        )
        self.play(
            flash_rect.animate.set_fill(opacity=1),
            FadeOut(clock),
            run_time=0.6,
            rate_func=rush_into,
        )

        self.play(
            flash_rect.animate.set_fill(opacity=0),
            run_time=0.5,
            rate_func=smooth,
        )
        self.remove(flash_rect)
