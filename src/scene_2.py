import sys
from pathlib import Path

CMD = Path(sys.argv[0]).name.lower()
if "manimgl" in CMD:
    from manimlib import *
else:
    from manim import *

BASE_DIR = Path("/home/pineapple/Desktop/projects/manim-GAA/Talk1")

BG = "#0D0D0D"
WHITE = "#F5F5F5"
ACCENT = "#4FC3F7"
GOLD = "#FFD54F"
SEPIA = "#C8A96E"  # aged/historical warmth
DIM = "#444444"


class BackInTime1913(Scene):

    def construct(self):
        self.camera.background_color = BG

        self._clock_rewind()
        self._year_land()
        self._markov_reveal()

    # ── Clock rewind ───────────────────────────────────────────────────────────
    def _clock_rewind(self):
        # ---- clock face ----
        face = Circle(
            radius=1.5, color=DIM, fill_color="#111111", fill_opacity=1, stroke_width=2
        )
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
            ticks.add(Line(inner, outer, color=DIM, stroke_width=1.5))

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
            color=SEPIA,
            stroke_width=4,
        )
        center_dot = Dot(face.get_center(), radius=0.07, color=WHITE)

        clock = VGroup(face, ticks, minute_hand, hour_hand, center_dot)

        self.play(FadeIn(clock, scale=0.7), run_time=0.8)

        # ---- "going back" label ----
        rewind_text = Text("going back...", font="Courier New", font_size=22, color=DIM)
        rewind_text.next_to(clock, DOWN, buff=0.4)
        self.play(FadeIn(rewind_text, shift=UP * 0.1), run_time=0.5)

        # ---- spin hands backward (counter-clockwise = negative angle) ----
        # minute hand spins fast, hour hand slower — classic rewind feel
        self.play(
            Rotating(
                minute_hand,
                angle=-4 * TAU,
                about_point=face.get_center(),
                run_time=2.5,
                rate_func=linear,
            ),
            Rotating(
                hour_hand,
                angle=-TAU,
                about_point=face.get_center(),
                run_time=2.5,
                rate_func=linear,
            ),
            run_time=2.5,
        )

        # ---- blur/flash wipe to transition ----
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
            FadeOut(rewind_text),
            run_time=0.6,
            rate_func=rush_into,
        )
        self.play(
            flash_rect.animate.set_fill(opacity=0),
            run_time=0.5,
            rate_func=smooth,
        )
        self.remove(flash_rect)

    # ── Year landing ───────────────────────────────────────────────────────────
    def _year_land(self):
        # Digits drop in one by one from above
        digits = ["1", "9", "1", "3"]
        digit_mobs = VGroup(
            *[
                Text(d, font="Courier New", font_size=120, color=SEPIA, weight=BOLD)
                for d in digits
            ]
        )
        digit_mobs.arrange(RIGHT, buff=0.18).move_to(ORIGIN)

        # start each digit high above, staggered
        starts = [dm.copy().shift(UP * 6) for dm in digit_mobs]
        for dm, st in zip(digit_mobs, starts):
            dm.move_to(st)

        self.play(
            LaggedStart(
                *[
                    dm.animate.move_to(final.get_center())
                    for dm, final in zip(
                        digit_mobs,
                        digit_mobs.copy().arrange(RIGHT, buff=0.18).move_to(ORIGIN),
                    )
                ],
                lag_ratio=0.18,
            ),
            run_time=1.4,
            rate_func=rush_from,
        )

        # thud effect — brief scale bounce
        self.play(
            digit_mobs.animate.scale(1.12),
            run_time=0.1,
        )
        self.play(
            digit_mobs.animate.scale(1 / 1.12),
            run_time=0.15,
        )

        # sepia underline sweeps in
        underline = Line(
            digit_mobs.get_left() + DOWN * 0.55,
            digit_mobs.get_right() + DOWN * 0.55,
            color=SEPIA,
            stroke_width=3,
        )
        self.play(Create(underline), run_time=0.6)
        self.wait(0.3)

        self._year_group = VGroup(digit_mobs, underline)  # keep for next beat

    # ── Markov reveal ──────────────────────────────────────────────────────────
    def _markov_reveal(self):
        # push year to top
        self.play(
            self._year_group.animate.scale(0.45).to_edge(UP, buff=0.3),
            run_time=0.7,
        )

        # ---- portrait placeholder (circle + initials) ----
        portrait = Circle(
            radius=0.9,
            color=SEPIA,
            fill_color="#1A1200",
            fill_opacity=1,
            stroke_width=2,
        )
        initials = Text("A.M.", font="Courier New", font_size=28, color=SEPIA)
        initials.move_to(portrait.get_center())
        portrait_grp = VGroup(portrait, initials)
        portrait_grp.move_to(LEFT * 3.2 + DOWN * 0.3)

        # ---- name + title ----
        name = Text(
            "Andrey Markov", font="Courier New", font_size=30, color=WHITE, weight=BOLD
        )
        title = Text(
            "Mathematician · St. Petersburg",
            font="Courier New",
            font_size=20,
            color=DIM,
        )
        name.next_to(portrait_grp, RIGHT, buff=0.5)
        title.next_to(name, DOWN, aligned_edge=LEFT, buff=0.18)

        # ---- key idea box ----
        idea_lines = Text(
            "Can we predict the next\ncharacter using statistics?",
            font="Courier New",
            font_size=22,
            color=SEPIA,
            line_spacing=1.4,
        )
        idea_box = SurroundingRectangle(
            idea_lines,
            color=SEPIA,
            buff=0.3,
            corner_radius=0.15,
            fill_color="#0D0900",
            fill_opacity=1,
            stroke_width=1.8,
        )
        idea_grp = VGroup(idea_box, idea_lines)
        idea_grp.next_to(portrait_grp, DOWN, buff=0.5).shift(RIGHT * 1.8)

        # ---- animate in ----
        self.play(
            FadeIn(portrait_grp, scale=0.8),
            run_time=0.8,
        )
        self.play(
            Write(name),
            run_time=0.7,
        )
        self.play(
            FadeIn(title, shift=RIGHT * 0.15),
            run_time=0.5,
        )
        self.wait(0.3)
        self.play(
            Create(idea_box),
            run_time=0.6,
        )
        self.play(
            Write(idea_lines),
            run_time=1.2,
        )

        # ---- connector dashed line portrait → idea box ----
        connector = DashedLine(
            portrait_grp.get_bottom(),
            idea_box.get_left() + LEFT * 0.05,
            color=SEPIA,
            dash_length=0.1,
            stroke_width=1.5,
        )
        self.play(Create(connector), run_time=0.5)
        self.wait(1.2)

        # ---- flash around the idea box to close ----
        corners = [idea_box.get_corner(c) for c in [UL, UR, DL, DR]]
        self.play(
            AnimationGroup(
                *[
                    Flash(
                        c, color=SEPIA, flash_radius=0.35, line_length=0.18, num_lines=6
                    )
                    for c in corners
                ],
                lag_ratio=0.0,
            ),
            run_time=0.7,
        )
        self.wait(0.6)
