import sys
from pathlib import Path

CMD = Path(sys.argv[0]).name.lower()
if "manimgl" in CMD:
    from manimlib import *
else:
    from manim import *

BASE_DIR = Path("/home/pineapple/Desktop/projects/manim-gaai/")

WHITE = "#F5F5F5"
ACCENT = "#4FC3F7"
GOLD = "#FFD54F"
SEPIA = "#C8A96E"
SEPIA_DARK = "#0D0900"
DIM = "#8A7676"
DIM2 = "#615B5B"


class ContextLength(Scene):
    # ── helpers ────────────────────────────────────────────────────────────────
    def _sepia_label(self, text, font_size=22):
        return Text(text, font_size=font_size, color=SEPIA)

    def _dim_label(self, text, font_size=20):
        return Text(text, font_size=font_size, color=DIM)

    def _white_label(self, text, font_size=26):
        return Text(text, font_size=font_size, color=WHITE)

    def _strike(self, mob):
        """Draw a red strikethrough over a mobject."""
        return Line(
            mob.get_left() + LEFT * 0.05,
            mob.get_right() + RIGHT * 0.05,
            color="#FF5252",
            stroke_width=2.5,
        )

    def construct(self):
        # the begining
        digits = ["1", "9", "1", "3"]
        digit_mobs = VGroup(
            *[
                Text(
                    d,
                    font_size=110,
                    weight=BOLD,
                )
                for d in digits
            ]
        )

        digit_mobs.arrange(RIGHT, buff=0.22).move_to(ORIGIN)

        for dm in digit_mobs:
            dm.shift(UP * 7)

        final_positions = (
            VGroup(
                *[
                    Text(
                        d,
                        font_size=110,
                        weight=BOLD,
                    )
                    for d in digits
                ]
            )
            .arrange(RIGHT, buff=0.22)
            .move_to(ORIGIN)
        )

        self.play(
            LaggedStart(
                *[
                    dm.animate.move_to(fp.get_center())
                    for dm, fp in zip(digit_mobs, final_positions)
                ],
                lag_ratio=0.2,
            ),
            run_time=1.4,
        )

        self.play(digit_mobs.animate.scale(1.1), run_time=0.08)
        self.play(digit_mobs.animate.scale(1 / 1.1), run_time=0.14)

        self.play(
            digit_mobs.animate.scale(1 / 3).to_corner(UL, buff=0.3),
            run_time=0.8,
        )

        self._year_group = VGroup(digit_mobs)

        # Portrait circle + name slide in from left
        portrait = Circle(
            radius=0.85,
            color=SEPIA,
            fill_color="#1A1200",
            fill_opacity=1,
            stroke_width=2,
        )
        initials = Text("AM", font_size=26, color=SEPIA)
        initials.move_to(portrait.get_center())
        portrait_grp = VGroup(portrait, initials)
        portrait_grp.move_to(LEFT * 4 + ORIGIN)  # start off-screen left
        portrait_grp.shift(LEFT * 2)

        name = Text("Andrey Markov", font_size=28, color=WHITE, weight=BOLD)
        role = Text("Russian Mathematician", font_size=19, color=DIM)
        year2 = Text("1856 – 1922", font_size=17, color=DIM)

        name.next_to(portrait_grp, RIGHT, buff=0.5)
        role.next_to(name, DOWN, aligned_edge=LEFT, buff=0.14)
        year2.next_to(role, DOWN, aligned_edge=LEFT, buff=0.1)

        bio_grp = VGroup(portrait_grp, name, role, year2)
        bio_grp.move_to(UP * 1.2)

        # slide in from left
        bio_grp.shift(LEFT * 8)
        self.play(
            bio_grp.animate.shift(RIGHT * 8),
            run_time=0.9,
            rate_func=smooth,
        )

        # ---- open book icon (two rectangles, spine line) ----
        page_l = Rectangle(
            width=1.3,
            height=1.7,
            color=SEPIA,
            fill_color="#1A1200",
            fill_opacity=1,
            stroke_width=1.8,
        )
        page_r = Rectangle(
            width=1.3,
            height=1.7,
            color=SEPIA,
            fill_color="#1A1200",
            fill_opacity=1,
            stroke_width=1.8,
        )
        page_l.next_to(ORIGIN, LEFT, buff=0.02)
        page_r.next_to(ORIGIN, RIGHT, buff=0.02)
        spine = Line(UP * 0.85, DOWN * 0.85, color=SEPIA, stroke_width=2)

        # text lines on pages
        lines_l = VGroup(
            *[
                Line(
                    page_l.get_left() + RIGHT * 0.15 + UP * (0.5 - i * 0.28),
                    page_l.get_right() + LEFT * 0.15 + UP * (0.5 - i * 0.28),
                    color=DIM,
                    stroke_width=1,
                )
                for i in range(4)
            ]
        )
        lines_r = VGroup(
            *[
                Line(
                    page_r.get_left() + RIGHT * 0.15 + UP * (0.5 - i * 0.28),
                    page_r.get_right() + LEFT * 0.15 + UP * (0.5 - i * 0.28),
                    color=DIM,
                    stroke_width=1,
                )
                for i in range(4)
            ]
        )

        book = VGroup(page_l, page_r, spine, lines_l, lines_r)
        book.move_to(DOWN * 1.3)

        action = Text("studying text...", font_size=22, color=SEPIA)
        action.next_to(book, DOWN, buff=0.3)

        self.play(FadeIn(book, scale=0.7), run_time=0.7)
        self.play(Write(action), run_time=0.8)
        self.wait(1.0)

        self._bio_grp = bio_grp
        self._book_grp = VGroup(book, action)

        # The wrong question (crossed out) vs the right attitude
        wrong_q = Text('"What does this poem mean?"', font_size=24, color=DIM)
        wrong_q.move_to(DOWN * 1.0)

        not_label = Text("He was NOT asking:", font_size=22, color=WHITE)
        not_label.next_to(wrong_q, UP, buff=0.35)

        self.play(
            FadeOut(self._book_grp),
            run_time=0.5,
        )

        self.play(Write(not_label), run_time=0.7)
        self.play(FadeIn(wrong_q, shift=UP * 0.1), run_time=0.6)
        self.wait(0.4)

        strike = self._strike(wrong_q)
        self.play(Create(strike), run_time=0.45)
        self.wait(0.3)

        self.play(
            VGroup(not_label, wrong_q, strike).animate.set_opacity(0).shift(UP * 0.5),
            run_time=0.6,
        )

        self._wrong_grp = VGroup(not_label, wrong_q, strike)
        self.play(
            FadeOut(self._bio_grp),
            FadeOut(self._wrong_grp),
            run_time=0.6,
        )

        instead = Text("Instead, he was asking:", font_size=24, color=WHITE)
        instead.move_to(UP * 1.8)
        self.play(Write(instead), run_time=0.7)

        # The core question — build it in two colour-coded parts
        part1 = Text(
            '"If I know the previous symbol,',
            font_size=26,
            color=WHITE,
        )
        part2 = Text(
            'can I predict what comes next?"',
            font_size=26,
            color=SEPIA,
        )

        q_grp = VGroup(part1, part2)
        q_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        q_grp.move_to(ORIGIN + DOWN * 0.1)

        box = SurroundingRectangle(
            q_grp,
            color=SEPIA,
            buff=0.35,
            corner_radius=0.2,
            fill_color=SEPIA_DARK,
            fill_opacity=1,
            stroke_width=2,
        )

        self.play(Create(box), run_time=0.6)
        self.play(Write(part1), run_time=1.0)
        self.play(
            Write(part2),
            run_time=1.0,
        )

        tracker = ValueTracker(0)
        self.play(tracker.animate.set_value(1.0), run_time=0.8)

        self.wait(0.5)

        corners = [box.get_corner(c) for c in [UL, UR, DL, DR]]
        self.play(
            AnimationGroup(
                *[
                    Flash(
                        c, color=SEPIA, flash_radius=0.38, line_length=0.2, num_lines=7
                    )
                    for c in corners
                ],
                lag_ratio=0.0,
            ),
            run_time=0.7,
        )

        self.wait(0.5)
        self.play(
            VGroup(box, part1, part2, instead, self._year_group).animate.set_opacity(
                0.0
            ),
            run_time=1.0,
        )

        # ── CLEAN SLATE ──────────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6,
        )

        # ================================================================
        #  PART 1 — THE SIMPLE GAME : "The capital of France is ___"
        # ================================================================

        # ── sentence with blank ──────────────────────────────────────────
        prompt_words = ["The", "capital", "of", "France", "is"]
        prompt_mobs = VGroup(
            *[Text(w, font_size=36, color=WHITE) for w in prompt_words]
        )
        prompt_mobs.arrange(RIGHT, buff=0.25)

        blank_box = RoundedRectangle(
            width=1.8,
            height=0.65,
            corner_radius=0.12,
            color=ACCENT,
            stroke_width=2.5,
            fill_color="#0A2A3A",
            fill_opacity=1,
        )
        question_marks = Text("???", font_size=30, color=ACCENT)

        blank_box.next_to(prompt_mobs, RIGHT, buff=0.3)
        question_marks.move_to(blank_box.get_center())
        blank_grp = VGroup(blank_box, question_marks)

        sentence_grp = VGroup(prompt_mobs, blank_grp).move_to(UP * 1.0)

        self.play(
            LaggedStart(
                *[FadeIn(w, shift=UP * 0.15) for w in prompt_mobs],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.play(
            FadeIn(blank_box, scale=0.85),
            Write(question_marks),
            run_time=0.7,
        )
        self.wait(0.6)

        # ── reveal "Paris" ───────────────────────────────────────────────
        answer = Text("Paris", font_size=36, color=GOLD, weight=BOLD)
        answer.move_to(blank_box.get_center())

        self.play(
            FadeOut(question_marks),
            run_time=0.25,
        )
        self.play(
            blank_box.animate.set_stroke(color=GOLD),
            FadeIn(answer, scale=1.3),
            run_time=0.6,
        )
        self.play(
            Flash(answer, color=GOLD, flash_radius=0.6, num_lines=10, line_length=0.2),
            run_time=0.5,
        )
        self.wait(0.8)

        # ── "But what if we don't know?" — library illustration ──────────
        self.play(
            sentence_grp.animate.shift(UP * 1.5).scale(0.6).set_opacity(0.35),
            answer.animate.shift(UP * 1.5).scale(0.6).set_opacity(0.35),
            run_time=0.7,
        )

        # Build a tiny bookshelf icon — stacked book rectangles
        books = VGroup()
        book_colors = ["#8A7676", "#615B5B", "#C8A96E", "#8A7676", "#615B5B"]
        for i, bc in enumerate(book_colors):
            b = Rectangle(
                width=0.28 + (i % 3) * 0.04,
                height=1.3 + (i % 2) * 0.2,
                color=bc,
                fill_color=bc,
                fill_opacity=0.5,
                stroke_width=1.2,
            )
            books.add(b)
        books.arrange(RIGHT, buff=0.06, aligned_edge=DOWN)

        shelf_line = Line(
            books.get_corner(DL) + LEFT * 0.15,
            books.get_corner(DR) + RIGHT * 0.15,
            color=SEPIA,
            stroke_width=2,
        )
        bookshelf = VGroup(books, shelf_line).scale(0.9).move_to(DOWN * 0.6)

        reading_label = Text("learning from patterns…", font_size=20, color=DIM)
        reading_label.next_to(bookshelf, DOWN, buff=0.35)

        self.play(
            FadeIn(bookshelf, scale=0.7),
            run_time=0.8,
        )
        self.play(Write(reading_label), run_time=0.7)
        self.wait(1.0)

        # ── transition — sweep everything out ────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6,
        )

        # ================================================================
        #  PART 2 — THE FORMULA  P(w | h)
        # ================================================================

        lm_label = Text("Language Model", font_size=28, color=ACCENT)
        lm_label.to_edge(UP, buff=0.6)
        self.play(Write(lm_label), run_time=0.7)

        formula = MathTex(r"P(", r"w", r"\mid", r"h", r")", font_size=56)
        formula[0].set_color(WHITE)
        formula[1].set_color(GOLD)  # w — next word
        formula[2].set_color(WHITE)
        formula[3].set_color(ACCENT)  # h — history/context
        formula[4].set_color(WHITE)
        formula.move_to(ORIGIN)

        self.play(Write(formula), run_time=1.2)
        self.wait(0.4)

        # annotations
        w_ann = Text("next word", font_size=18, color=GOLD)
        h_ann = Text("context", font_size=18, color=ACCENT)
        w_ann.next_to(formula[1], DOWN, buff=0.35)
        h_ann.next_to(formula[3], DOWN, buff=0.35)

        w_arrow = Arrow(
            w_ann.get_top(),
            formula[1].get_bottom(),
            buff=0.06,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.25,
        )
        h_arrow = Arrow(
            h_ann.get_top(),
            formula[3].get_bottom(),
            buff=0.06,
            color=ACCENT,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.25,
        )

        self.play(
            FadeIn(w_ann, shift=DOWN * 0.1),
            GrowArrow(w_arrow),
            run_time=0.6,
        )
        self.play(
            FadeIn(h_ann, shift=DOWN * 0.1),
            GrowArrow(h_arrow),
            run_time=0.6,
        )
        self.wait(0.8)

        # ── concrete example: P(w | "The capital of France is") ──────────
        example = MathTex(
            r"P(",
            r"w",
            r"\mid",
            r"\text{``The capital of France is''}",
            r")",
            font_size=36,
        )
        example[1].set_color(GOLD)
        example[3].set_color(ACCENT)
        example.next_to(formula, DOWN, buff=1.4)

        self.play(
            FadeOut(w_ann),
            FadeOut(h_ann),
            FadeOut(w_arrow),
            FadeOut(h_arrow),
            run_time=0.35,
        )
        self.play(Write(example), run_time=1.2)
        self.wait(0.8)

        # ================================================================
        #  PART 3 — PROBABILITY DISTRIBUTION BAR CHART
        # ================================================================

        self.play(
            FadeOut(lm_label),
            FadeOut(formula),
            FadeOut(example),
            run_time=0.5,
        )

        # words and their "probabilities"
        candidates = ["Paris", "Lyon", "the", "banana", "42"]
        probs = [0.82, 0.07, 0.05, 0.01, 0.005]
        bar_colors = [GOLD, DIM, DIM, DIM2, DIM2]

        max_bar_h = 3.5
        bar_w = 0.65
        bars = VGroup()
        word_labels = VGroup()
        prob_labels = VGroup()

        for i, (word, p, c) in enumerate(zip(candidates, probs, bar_colors)):
            h = max(max_bar_h * p, 0.08)
            bar = Rectangle(
                width=bar_w,
                height=h,
                color=c,
                fill_color=c,
                fill_opacity=0.65,
                stroke_width=1.5,
            )
            bars.add(bar)

            wl = Text(word, font_size=18, color=WHITE)
            word_labels.add(wl)

            pl = Text(f"{p:.0%}" if p >= 0.01 else "<1%", font_size=14, color=c)
            prob_labels.add(pl)

        bars.arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
        bars.move_to(DOWN * 0.3)

        # baseline
        baseline = Line(
            bars.get_corner(DL) + LEFT * 0.3,
            bars.get_corner(DR) + RIGHT * 0.3,
            color=WHITE,
            stroke_width=1.5,
        )
        baseline.next_to(bars, DOWN, buff=0.0)

        for wl, bar in zip(word_labels, bars):
            wl.next_to(bar, DOWN, buff=0.22)
        for pl, bar in zip(prob_labels, bars):
            pl.next_to(bar, UP, buff=0.1)

        chart_title = MathTex(
            r"P(w \mid \text{``The capital of France is''})",
            font_size=30,
            color=WHITE,
        )
        chart_title.to_edge(UP, buff=0.5)

        self.play(Write(chart_title), run_time=0.7)
        self.play(Create(baseline), run_time=0.3)

        # grow bars one by one
        for bar, wl, pl in zip(bars, word_labels, prob_labels):
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)
            self.play(
                bar.animate.restore(),
                FadeIn(wl, shift=UP * 0.1),
                FadeIn(pl, shift=DOWN * 0.1),
                run_time=0.4,
            )

        self.wait(0.4)

        # highlight Paris bar
        paris_bar = bars[0]
        glow = paris_bar.copy().set_fill(GOLD, opacity=0.3).set_stroke(GOLD, width=3)
        self.play(
            FadeIn(glow),
            paris_bar.animate.set_fill(opacity=0.9),
            run_time=0.5,
        )
        self.play(
            Flash(paris_bar, color=GOLD, flash_radius=0.5, num_lines=8),
            run_time=0.5,
        )
        self.wait(0.8)

        # ── "not geography, just statistics" ─────────────────────────────
        stat_note = Text(
            "Not knowledge — just statistics.",
            font_size=22,
            color=DIM,
        )
        stat_note.next_to(baseline, DOWN, buff=0.8)
        self.play(FadeIn(stat_note, shift=UP * 0.1), run_time=0.7)
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6,
        )

        # ================================================================
        #  PART 4 — CONTEXT MATTERS  (more context → better prediction)
        # ================================================================

        # ── Short context: "of France is" ────────────────────────────────
        short_ctx = Text('"of France is …"', font_size=30, color=DIM)
        short_ctx.move_to(UP * 2.2)
        short_label = Text("short context", font_size=16, color=DIM2)
        short_label.next_to(short_ctx, UP, buff=0.2)

        # many possible continuations — fan of arrows
        short_options = ["capital?", "cuisine?", "flag?", "history?"]
        opt_mobs = VGroup()
        for i, opt in enumerate(short_options):
            t = Text(opt, font_size=20, color=DIM)
            t.move_to(RIGHT * (-2.5 + i * 1.7) + DOWN * 0.0)
            opt_mobs.add(t)

        fan_arrows = VGroup()
        for om in opt_mobs:
            a = Arrow(
                short_ctx.get_bottom(),
                om.get_top(),
                buff=0.15,
                color=DIM2,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.2,
            )
            fan_arrows.add(a)

        ambig_label = Text("ambiguous!", font_size=20, color="#FF5252")
        ambig_label.next_to(opt_mobs, DOWN, buff=0.45)

        self.play(Write(short_label), FadeIn(short_ctx, shift=DOWN * 0.1), run_time=0.7)
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in fan_arrows],
                lag_ratio=0.12,
            ),
            LaggedStart(
                *[FadeIn(o, shift=DOWN * 0.1) for o in opt_mobs],
                lag_ratio=0.12,
            ),
            run_time=0.9,
        )
        self.play(FadeIn(ambig_label, scale=1.2), run_time=0.5)
        self.wait(1.0)

        # ── transition to long context ───────────────────────────────────
        self.play(
            *[
                FadeOut(m)
                for m in [short_label, short_ctx, *fan_arrows, *opt_mobs, ambig_label]
            ],
            run_time=0.5,
        )

        long_ctx = Text('"The capital of France is …"', font_size=30, color=ACCENT)
        long_ctx.move_to(UP * 2.2)
        long_label = Text("full context", font_size=16, color=ACCENT)
        long_label.next_to(long_ctx, UP, buff=0.2)

        single_arrow = Arrow(
            long_ctx.get_bottom(),
            ORIGIN + UP * 0.3,
            buff=0.15,
            color=GOLD,
            stroke_width=2.5,
        )
        paris_answer = Text("Paris", font_size=36, color=GOLD, weight=BOLD)
        paris_answer.move_to(DOWN * 0.3)

        clear_label = Text("clear!", font_size=20, color=GOLD)
        clear_label.next_to(paris_answer, DOWN, buff=0.4)

        self.play(Write(long_label), FadeIn(long_ctx, shift=DOWN * 0.1), run_time=0.7)
        self.play(GrowArrow(single_arrow), run_time=0.5)
        self.play(
            FadeIn(paris_answer, scale=1.3),
            run_time=0.5,
        )
        self.play(
            FadeIn(clear_label, scale=1.1),
            Flash(paris_answer, color=GOLD, flash_radius=0.5, num_lines=8),
            run_time=0.5,
        )
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6,
        )

        # ================================================================
        #  PART 5 — THE TRADEOFF : context vs cost
        # ================================================================

        # ── the two equations side by side ───────────────────────────────
        eq_better = MathTex(
            r"\text{Better context}",
            r"\;\rightarrow\;",
            r"\text{better prediction}",
            font_size=30,
        )
        eq_better[0].set_color(ACCENT)
        eq_better[2].set_color(GOLD)

        eq_cost = MathTex(
            r"\text{Longer context}",
            r"\;\rightarrow\;",
            r"\text{higher cost}",
            font_size=30,
        )
        eq_cost[0].set_color(ACCENT)
        eq_cost[2].set_color("#FF5252")

        eqs = VGroup(eq_better, eq_cost).arrange(DOWN, buff=0.6).move_to(UP * 1.5)

        self.play(Write(eq_better), run_time=0.9)
        self.wait(0.4)
        self.play(Write(eq_cost), run_time=0.9)
        self.wait(0.8)

        # ── visual: growing context bar vs growing cost bar ──────────────
        self.play(eqs.animate.to_edge(UP, buff=0.4).scale(0.85), run_time=0.5)

        # context bar (blue, grows right)
        ctx_bar_bg = Rectangle(
            width=5,
            height=0.45,
            color=WHITE,
            fill_opacity=0.05,
            stroke_width=1,
        ).move_to(LEFT * 0.5 + DOWN * 0.5)

        ctx_bar = Rectangle(
            width=0.1,
            height=0.45,
            color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.6,
            stroke_width=0,
        )
        ctx_bar.align_to(ctx_bar_bg, LEFT)
        ctx_bar.move_to(ctx_bar_bg.get_center())
        ctx_bar.align_to(ctx_bar_bg, LEFT)

        ctx_label = Text("context length", font_size=16, color=ACCENT)
        ctx_label.next_to(ctx_bar_bg, LEFT, buff=0.25)

        # cost bar (red, grows right)
        cost_bar_bg = Rectangle(
            width=5,
            height=0.45,
            color=WHITE,
            fill_opacity=0.05,
            stroke_width=1,
        ).move_to(LEFT * 0.5 + DOWN * 1.5)

        cost_bar = Rectangle(
            width=0.1,
            height=0.45,
            color="#FF5252",
            fill_color="#FF5252",
            fill_opacity=0.6,
            stroke_width=0,
        )
        cost_bar.align_to(cost_bar_bg, LEFT)
        cost_bar.move_to(cost_bar_bg.get_center())
        cost_bar.align_to(cost_bar_bg, LEFT)

        cost_label = Text("compute cost", font_size=16, color="#FF5252")
        cost_label.next_to(cost_bar_bg, LEFT, buff=0.25)

        self.play(
            FadeIn(ctx_bar_bg),
            FadeIn(cost_bar_bg),
            FadeIn(ctx_label),
            FadeIn(cost_label),
            run_time=0.5,
        )

        # animate both bars growing
        self.play(
            ctx_bar.animate.stretch_to_fit_width(4.8).align_to(ctx_bar_bg, LEFT),
            cost_bar.animate.stretch_to_fit_width(4.8).align_to(cost_bar_bg, LEFT),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(0.6)

        # ── the key question ─────────────────────────────────────────────
        question = Text(
            "How much context should the model look at?",
            font_size=24,
            color=WHITE,
        )
        question.move_to(DOWN * 2.8)

        q_box = SurroundingRectangle(
            question,
            color=SEPIA,
            buff=0.25,
            corner_radius=0.15,
            fill_color=SEPIA_DARK,
            fill_opacity=1,
            stroke_width=1.8,
        )

        self.play(Create(q_box), run_time=0.5)
        self.play(Write(question), run_time=1.0)

        self.play(
            Flash(q_box, color=SEPIA, flash_radius=0.4, line_length=0.15, num_lines=8),
            run_time=0.6,
        )

        self.wait(1.5)

        # ── final fade ───────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
