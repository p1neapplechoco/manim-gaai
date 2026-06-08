import sys
from pathlib import Path

from utils.artifacts import *

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
RED = "#FF5252"


class NgramToRNN(Scene):
    def construct(self):
        # ================================================================
        #  PART 1 — COUNT THE PATTERNS
        #  Visual: sentence with a sliding "fixed window" highlight
        # ================================================================

        words = ["The", "capital", "of", "France", "is"]
        word_mobs = VGroup(*[Text(w, font_size=30, color=WHITE) for w in words])
        word_mobs.arrange(RIGHT, buff=0.25)
        word_mobs.move_to(UP * 1.0)

        # Blank prediction box
        blank = RoundedRectangle(
            width=1.5,
            height=0.55,
            corner_radius=0.1,
            color=GOLD,
            stroke_width=2,
            fill_color="#1A1500",
            fill_opacity=1,
        )
        q_mark = Text("?", font_size=28, color=GOLD)
        blank.next_to(word_mobs, RIGHT, buff=0.25)
        q_mark.move_to(blank)
        blank_grp = VGroup(blank, q_mark)

        self.play(
            LaggedStart(
                *[FadeIn(w, shift=UP * 0.15) for w in word_mobs],
                lag_ratio=0.1,
            ),
            run_time=1.0,
        )
        self.play(FadeIn(blank_grp, scale=0.9), run_time=0.4)
        # [5:18] The earliest LMs looked at a fixed number of previous words
        self.wait(3.0)

        # Sliding window — highlights n-1 previous words
        def make_window(si, ei):
            return SurroundingRectangle(
                VGroup(*word_mobs[si : ei + 1]),
                color=ACCENT,
                buff=0.1,
                corner_radius=0.08,
                fill_color=ACCENT,
                fill_opacity=0.1,
                stroke_width=2,
            )

        window = make_window(3, 4)
        bracket = Brace(VGroup(*word_mobs[3:5]), DOWN, color=ACCENT)
        br_label = Text("fixed window", font_size=16, color=ACCENT)
        br_label.next_to(bracket, DOWN, buff=0.1)

        self.play(
            Create(window),
            GrowFromCenter(bracket),
            FadeIn(br_label),
            run_time=0.7,
        )
        # [5:31] n represents the number of words, context is n-1 words
        self.wait(3.0)

        # Slide the window across the sentence
        for si in [2, 0]:
            ei = si + 1
            nw = make_window(si, ei)
            nb = Brace(VGroup(*word_mobs[si : ei + 1]), DOWN, color=ACCENT)
            nl = Text("fixed window", font_size=16, color=ACCENT)
            nl.next_to(nb, DOWN, buff=0.1)
            self.play(
                Transform(window, nw),
                Transform(bracket, nb),
                Transform(br_label, nl),
                run_time=0.6,
            )
            self.wait(1.5)

        # Small tally marks — visual for "counting"
        tally = VGroup()
        for i in range(4):
            tick = Line(UP * 0.18, DOWN * 0.18, color=SEPIA, stroke_width=2)
            tick.shift(DOWN * 2.0 + LEFT * 0.25 + RIGHT * i * 0.15)
            tally.add(tick)
        cross = Line(
            tally[0].get_bottom() + LEFT * 0.03,
            tally[3].get_top() + RIGHT * 0.03,
            color=SEPIA,
            stroke_width=2,
        )
        tally.add(cross)

        ct_label = Text("count", font_size=16, color=DIM)
        ct_label.next_to(tally, RIGHT, buff=0.25)

        self.play(
            LaggedStart(*[Create(t) for t in tally], lag_ratio=0.08),
            FadeIn(ct_label),
            run_time=0.6,
        )
        # [5:40] n usually ranges from 1 to 6
        self.wait(4.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(2.0)

        # ================================================================
        #  PART 2 — N-GRAM NAMING
        #  Visual: rows of (n value, name, box diagram)
        # ================================================================

        ngram_data = [
            (1, "unigram"),
            (2, "bigram"),
            (3, "trigram"),
        ]

        rows = VGroup()
        for n, name in ngram_data:
            n_lab = MathTex(f"n = {n}", font_size=26, color=ACCENT)
            nm_lab = Text(name, font_size=24, color=WHITE)
            boxes = VGroup(
                *[
                    RoundedRectangle(
                        width=0.35,
                        height=0.35,
                        corner_radius=0.05,
                        color=GOLD,
                        stroke_width=1.5,
                        fill_color=GOLD,
                        fill_opacity=0.15,
                    )
                    for _ in range(n)
                ]
            )
            boxes.arrange(RIGHT, buff=0.06)
            row = VGroup(n_lab, nm_lab, boxes).arrange(RIGHT, buff=0.6)
            rows.add(row)

        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        rows.move_to(UP * 0.8)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.5)
            # [5:48] unigram for n=1, bigram for n=2
            self.wait(2.0)

        # General n-gram row
        vdots = MathTex(r"\vdots", font_size=28, color=DIM)
        vdots.next_to(rows, DOWN, buff=0.3)
        vdots.align_to(rows, LEFT).shift(RIGHT * 0.5)

        gen_n = MathTex("n", font_size=26, color=ACCENT)
        gen_name = Text("n-gram", font_size=24, color=WHITE)
        gen_box1 = RoundedRectangle(
            width=0.35,
            height=0.35,
            corner_radius=0.05,
            color=GOLD,
            stroke_width=1.5,
            fill_color=GOLD,
            fill_opacity=0.15,
        )
        gen_box2 = gen_box1.copy()
        gen_dots = MathTex(r"\cdots", font_size=20, color=GOLD)
        gen_box3 = gen_box1.copy()
        gen_boxes = VGroup(gen_box1, gen_box2, gen_dots, gen_box3)
        gen_boxes.arrange(RIGHT, buff=0.06)
        gen_row = VGroup(gen_n, gen_name, gen_boxes).arrange(RIGHT, buff=0.6)
        gen_row.next_to(vdots, DOWN, buff=0.3)
        gen_row.align_to(rows, LEFT)

        self.play(FadeIn(vdots), run_time=0.3)
        self.play(FadeIn(gen_row, shift=RIGHT * 0.15), run_time=0.5)
        # [5:54] The main problem is that n-gram models do not scale well
        self.wait(4.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 3 — EXPONENTIAL GROWTH   V^n
        #  Visual: bars that grow exponentially, trigram crashes off-screen
        # ================================================================

        v_label = MathTex(r"V = 50{,}000", font_size=30, color=ACCENT)
        v_label.to_edge(UP, buff=0.5)
        self.play(Write(v_label), run_time=0.6)

        formula = MathTex(
            r"\underbrace{V \times V \times \cdots \times V}_{n}",
            r"= V^n",
            font_size=32,
        )
        formula[0].set_color(WHITE)
        formula[1].set_color(GOLD)
        formula.next_to(v_label, DOWN, buff=0.35)

        self.play(Write(formula), run_time=1.0)
        # [5:59] Every time we increase n, the model has to store more
        self.wait(6.0)

        self.play(
            VGroup(v_label, formula).animate.scale(0.8).to_edge(UP, buff=0.2),
            run_time=0.5,
        )

        # Baseline
        BASE_Y = -1.8
        base_line = Line(LEFT * 5, RIGHT * 5, color=WHITE, stroke_width=1)
        base_line.move_to(UP * BASE_Y)
        self.play(Create(base_line), run_time=0.3)

        # Bar specs: (name, V^k tex, height, color, number)
        bar_specs = [
            ("unigram", r"V", 0.7, ACCENT, "50K"),
            ("bigram", r"V^2", 2.0, GOLD, "2.5B"),
            ("trigram", r"V^3", 10.0, RED, "125T"),
        ]
        x_pos = [-2.8, 0, 2.8]
        bar_w = 1.0

        all_bar_mobs = VGroup()

        for i, (name, stex, h, col, num) in enumerate(bar_specs):
            bar = Rectangle(
                width=bar_w,
                height=h,
                color=col,
                fill_color=col,
                fill_opacity=0.5,
                stroke_width=1.5,
            )
            # Bottom of bar sits on baseline
            bar.move_to(RIGHT * x_pos[i] + UP * (BASE_Y + h / 2))

            nm = Text(name, font_size=17, color=col)
            nm.move_to(RIGHT * x_pos[i] + UP * (BASE_Y - 0.3))

            st = MathTex(stex, font_size=22, color=col)
            nt = Text(num, font_size=14, color=col)

            if i < 2:
                # Size label sits above the bar (visible)
                st.next_to(bar, UP, buff=0.1)
                nt.next_to(st, RIGHT, buff=0.12)
            else:
                # For trigram, label at a readable position
                st.move_to(RIGHT * x_pos[i] + UP * 2.2)
                nt.next_to(st, RIGHT, buff=0.12)

            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)

            if i < 2:
                self.play(
                    bar.animate.restore(),
                    FadeIn(nm),
                    run_time=0.6,
                )
                self.play(
                    FadeIn(st, shift=DOWN * 0.1),
                    FadeIn(nt, shift=DOWN * 0.1),
                    run_time=0.4,
                )
            else:
                # Trigram — dramatic
                self.play(FadeIn(nm), run_time=0.3)
                self.play(
                    bar.animate.restore(),
                    run_time=1.5,
                    rate_func=rush_into,
                )
                self.play(
                    FadeIn(st, scale=1.3),
                    FadeIn(nt, scale=1.3),
                    Flash(
                        RIGHT * x_pos[i] + UP * BASE_Y,
                        color=RED,
                        flash_radius=0.8,
                        num_lines=12,
                        line_length=0.2,
                    ),
                    run_time=0.6,
                )

            # [6:17] If vocabulary has V words, combinations = V^n
            self.wait(5.0)
            all_bar_mobs.add(bar, nm, st, nt)

        # [6:37] V x V x ... x V = V^n — proven using combinatorics
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 4 — TWO PROBLEMS : storage + sparsity
        #  Visual: split screen with illustrated icons
        # ================================================================

        divider = Line(UP * 2.5, DOWN * 2.0, color=DIM2, stroke_width=0.8)
        self.play(Create(divider), run_time=0.3)

        # ── Storage icon (left) ──────────────────────────────────────────
        drives = VGroup()
        for i in range(5):
            dr = RoundedRectangle(
                width=2.0,
                height=0.28,
                corner_radius=0.05,
                color=DIM if i < 3 else RED,
                stroke_width=1.5,
                fill_color="#151515" if i < 3 else "#2A0A0A",
                fill_opacity=1,
            )
            drives.add(dr)
        drives.arrange(UP, buff=0.06)

        # Capacity line between normal and overflow drives
        cap_line = DashedLine(
            LEFT * 1.3,
            RIGHT * 1.3,
            color=RED,
            stroke_width=1.5,
            dash_length=0.1,
        )
        cap_line.move_to(drives[2].get_top() + UP * 0.04)
        cap_txt = Text("capacity", font_size=11, color=RED)
        cap_txt.next_to(cap_line, RIGHT, buff=0.1)

        st_title = Text("storage", font_size=20, color=DIM)
        st_title.next_to(drives, DOWN, buff=0.4)

        storage_all = VGroup(drives, cap_line, cap_txt, st_title)
        storage_all.move_to(LEFT * 3.2 + UP * 0.2)

        self.play(
            LaggedStart(
                *[FadeIn(d, shift=UP * 0.08) for d in drives[:3]],
                lag_ratio=0.1,
            ),
            FadeIn(st_title),
            run_time=0.6,
        )
        self.play(Create(cap_line), FadeIn(cap_txt), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(d, shift=UP * 0.08) for d in drives[3:]],
                lag_ratio=0.1,
            ),
            run_time=0.5,
        )
        # [7:17] Two major problems: storage
        self.wait(4.0)

        # ── Sparsity icon (right) ────────────────────────────────────────
        g_n = 6
        cs = 0.28
        grid = VGroup()
        for r in range(g_n):
            for c in range(g_n):
                cell = Square(
                    side_length=cs,
                    color=DIM2,
                    stroke_width=0.5,
                    fill_color="#080808",
                    fill_opacity=1,
                )
                cell.shift(RIGHT * c * (cs + 0.02) + UP * r * (cs + 0.02))
                grid.add(cell)
        grid.center()

        # A few filled cells (data we actually observed)
        for idx in [0, 7, 14, 21, 28, 35]:
            if idx < len(grid):
                grid[idx].set_fill(ACCENT, opacity=0.25)

        q_marks = VGroup()
        for idx in [3, 10, 17, 29, 33]:
            if idx < len(grid):
                q = Text("?", font_size=9, color=DIM2)
                q.move_to(grid[idx])
                q_marks.add(q)

        sp_title = Text("sparsity", font_size=20, color=DIM)
        sp_title.next_to(grid, DOWN, buff=0.4)

        sparse_all = VGroup(grid, q_marks, sp_title)
        sparse_all.move_to(RIGHT * 3.2 + UP * 0.2)

        self.play(
            FadeIn(grid),
            FadeIn(q_marks),
            FadeIn(sp_title),
            run_time=0.7,
        )
        # [7:26] And data sparsity — never-seen phrases
        self.wait(10.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 5 — IT'S JUST COUNTING
        #  Visual: two phrases with count bars, "brute-force" label
        # ================================================================

        ph1 = Text('"…France is Paris"', font_size=22, color=WHITE)
        ct1 = Text("1,247×", font_size=20, color=GOLD)
        b1 = Rectangle(
            width=4.0,
            height=0.32,
            color=GOLD,
            fill_color=GOLD,
            fill_opacity=0.5,
            stroke_width=1,
        )

        ph2 = Text('"…France is London"', font_size=22, color=WHITE)
        ct2 = Text("12×", font_size=20, color=DIM)
        b2 = Rectangle(
            width=0.4,
            height=0.32,
            color=DIM,
            fill_color=DIM,
            fill_opacity=0.5,
            stroke_width=1,
        )

        ph1.move_to(UP * 1.6 + LEFT * 1.5)
        ct1.next_to(ph1, RIGHT, buff=0.4)
        b1.next_to(ph1, DOWN, buff=0.25)
        b1.align_to(ph1, LEFT)

        ph2.move_to(DOWN * 0.3 + LEFT * 1.5)
        ct2.next_to(ph2, RIGHT, buff=0.4)
        b2.next_to(ph2, DOWN, buff=0.25)
        b2.align_to(ph2, LEFT)

        # Phrase 1 + bar
        self.play(Write(ph1), run_time=0.6)
        b1.save_state()
        b1.stretch(0, 0, about_edge=LEFT)
        self.play(
            b1.animate.restore(),
            FadeIn(ct1),
            run_time=0.6,
        )

        # Phrase 2 + bar
        self.play(Write(ph2), run_time=0.6)
        b2.save_state()
        b2.stretch(0, 0, about_edge=LEFT)
        self.play(
            b2.animate.restore(),
            FadeIn(ct2),
            run_time=0.4,
        )
        # [7:52] Count how often patterns appear
        self.wait(3.0)

        # Arrow pointing to the bigger bar
        pick_arrow = Arrow(
            b1.get_right() + RIGHT * 0.3 + DOWN * 0.5,
            b1.get_right() + RIGHT * 0.1,
            buff=0.05,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.3,
        )
        pick_lab = Text("pick the bigger count", font_size=16, color=DIM)
        pick_lab.next_to(pick_arrow, DOWN, buff=0.12)

        self.play(GrowArrow(pick_arrow), FadeIn(pick_lab), run_time=0.5)
        self.wait(2.0)

        # "brute-force" bracket
        all_counts = VGroup(ph1, b1, ct1, ph2, b2, ct2)
        bf_brace = Brace(all_counts, RIGHT, color=RED)
        bf_lab = Text("brute-force", font_size=20, color=RED)
        bf_lab.next_to(bf_brace, RIGHT, buff=0.2)

        self.play(
            GrowFromCenter(bf_brace),
            Write(bf_lab),
            run_time=0.6,
        )
        # [7:59] Simple, intuitive, almost brute-force
        self.wait(4.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 6 — THE BRUTE-FORCE WALL
        #  Visual: giant lookup table with red ✗
        # ================================================================

        table = Rectangle(
            width=6,
            height=4,
            color=DIM,
            stroke_width=2,
            fill_color="#0A0A0A",
            fill_opacity=1,
        )
        table.move_to(ORIGIN)

        # Grid texture inside the table
        glines = VGroup()
        for i in range(1, 9):
            glines.add(
                Line(
                    table.get_left() + RIGHT * 0.1 + UP * (i * 0.42 - 1.9),
                    table.get_right() + LEFT * 0.1 + UP * (i * 0.42 - 1.9),
                    color=DIM2,
                    stroke_width=0.4,
                )
            )
        for i in range(1, 14):
            glines.add(
                Line(
                    table.get_bottom() + UP * 0.1 + RIGHT * (i * 0.42 - 2.9),
                    table.get_top() + DOWN * 0.1 + RIGHT * (i * 0.42 - 2.9),
                    color=DIM2,
                    stroke_width=0.4,
                )
            )

        tbl_label = MathTex(r"V^n \text{ entries}", font_size=30, color=DIM)
        tbl_label.move_to(table)

        # Small observer dot at the bottom
        observer = Dot(radius=0.06, color=WHITE)
        observer.next_to(table, DOWN, buff=0.25)

        self.play(
            FadeIn(table),
            LaggedStart(*[Create(l) for l in glines], lag_ratio=0.02),
            run_time=0.8,
        )
        self.play(Write(tbl_label), run_time=0.5)
        self.play(FadeIn(observer, scale=0.5), run_time=0.3)
        # [8:12] Instead of storing every combination in a giant table
        self.wait(3.0)

        # Red ✗
        x1 = Line(
            table.get_corner(UL) + DR * 0.3,
            table.get_corner(DR) + UL * 0.3,
            color=RED,
            stroke_width=5,
        )
        x2 = Line(
            table.get_corner(UR) + DL * 0.3,
            table.get_corner(DL) + UR * 0.3,
            color=RED,
            stroke_width=5,
        )

        self.play(Create(x1), Create(x2), run_time=0.5)
        self.play(
            Flash(ORIGIN, color=RED, flash_radius=1.2, num_lines=14),
            run_time=0.5,
        )
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 7 — THE NEW QUESTION
        #  Visual: words enter a box one-by-one, compressed state grows
        # ================================================================

        q_text = Text("What if we compress?", font_size=28, color=WHITE)
        q_text.move_to(UP * 3.0)
        self.play(Write(q_text), run_time=0.7)
        # [8:21] Can the model compress the context into a learned representation?
        self.wait(2.0)

        # The processing box (the "model")
        model_box = RoundedRectangle(
            width=2.0,
            height=1.5,
            corner_radius=0.2,
            color=ACCENT,
            stroke_width=2,
            fill_color="#0A1A2A",
            fill_opacity=1,
        )
        model_box.move_to(ORIGIN)

        # State dot — starts small and dim, grows with each absorbed word
        state = Dot(radius=0.12, color=ACCENT, fill_opacity=0.25)
        state.move_to(model_box.get_center())

        self.play(FadeIn(model_box, scale=0.9), run_time=0.5)
        self.play(FadeIn(state, scale=0.5), run_time=0.3)

        input_words = ["The", "capital", "of", "France", "is"]
        state_radii = [0.14, 0.19, 0.25, 0.32, 0.40]
        state_opacs = [0.30, 0.40, 0.50, 0.65, 0.85]
        state_cols = [ACCENT, ACCENT, ACCENT, GOLD, GOLD]

        for i, word in enumerate(input_words):
            w = Text(word, font_size=24, color=WHITE)
            w.move_to(LEFT * 4.5)

            self.play(FadeIn(w, shift=RIGHT * 0.3), run_time=0.25)

            # Create the target state after absorption
            new_state = Dot(
                radius=state_radii[i],
                color=state_cols[i],
                fill_opacity=state_opacs[i],
            )
            new_state.move_to(model_box.get_center())

            self.play(
                w.animate.move_to(model_box.get_center()).scale(0.15).set_opacity(0),
                Transform(state, new_state),
                run_time=0.5,
            )
            self.remove(w)

        self.wait(3.0)

        # Label the box
        comp_label = Text("compressed", font_size=14, color=ACCENT)
        comp_label.next_to(model_box, DOWN, buff=0.15)
        self.play(FadeIn(comp_label, shift=UP * 0.08), run_time=0.4)

        # Show output prediction
        out_arrow = Arrow(
            model_box.get_right(),
            RIGHT * 3.5,
            buff=0.1,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        prediction = Text("Paris", font_size=28, color=GOLD, weight=BOLD)
        prediction.next_to(out_arrow, RIGHT, buff=0.2)

        self.play(GrowArrow(out_arrow), run_time=0.5)
        self.play(
            FadeIn(prediction, scale=1.2),
            Flash(prediction, color=GOLD, flash_radius=0.5, num_lines=8),
            run_time=0.5,
        )
        # [8:30] Model reads words one by one, compresses into representation
        self.wait(4.0)

        # ── Transition to Part 8 (keep model_box + state) ────────────────
        self.play(
            FadeOut(q_text),
            FadeOut(out_arrow),
            FadeOut(prediction),
            FadeOut(comp_label),
            run_time=0.5,
        )

        # ================================================================
        #  PART 8 — THIS BRINGS US TO RNNs
        #  Visual: model box morphs into RNN cell with self-loop
        # ================================================================

        # Target RNN cell (smaller, cleaner)
        rnn_cell = RoundedRectangle(
            width=1.5,
            height=1.2,
            corner_radius=0.15,
            color=ACCENT,
            stroke_width=2,
            fill_color="#0A1A2A",
            fill_opacity=1,
        )
        rnn_cell.move_to(ORIGIN)

        h_label = MathTex(r"h_t", font_size=30, color=GOLD)
        h_label.move_to(rnn_cell.get_center())

        self.play(
            Transform(model_box, rnn_cell),
            FadeOut(state),
            FadeIn(h_label),
            run_time=0.8,
        )
        # [8:36] This brings us to RNNs
        self.wait(3.0)

        # Input arrow
        in_arrow = Arrow(
            LEFT * 3.5,
            model_box.get_left(),
            buff=0.1,
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        x_label = MathTex(r"x_t", font_size=22, color=WHITE)
        x_label.next_to(in_arrow, DOWN, buff=0.1)

        # Output arrow
        out_arrow2 = Arrow(
            model_box.get_right(),
            RIGHT * 3.5,
            buff=0.1,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        y_label = MathTex(r"y_t", font_size=22, color=GOLD)
        y_label.next_to(out_arrow2, DOWN, buff=0.1)

        self.play(
            GrowArrow(in_arrow),
            FadeIn(x_label),
            GrowArrow(out_arrow2),
            FadeIn(y_label),
            run_time=0.6,
        )

        # Self-loop (the defining feature of RNNs)
        loop = CurvedArrow(
            model_box.get_top() + LEFT * 0.25,
            model_box.get_top() + RIGHT * 0.25,
            angle=PI,
            color=GOLD,
            stroke_width=2.5,
            tip_length=0.15,
        )

        self.play(Create(loop), run_time=0.7)
        self.play(
            Flash(
                model_box.get_top() + UP * 0.5,
                color=GOLD,
                flash_radius=0.4,
                num_lines=8,
            ),
            run_time=0.5,
        )
        self.wait(3.0)

        # Title
        title = Text("Recurrent Neural Networks", font_size=30, color=ACCENT)
        title.next_to(model_box, DOWN, buff=1.2)

        title_box = SurroundingRectangle(
            title,
            color=SEPIA,
            buff=0.25,
            corner_radius=0.15,
            fill_color=SEPIA_DARK,
            fill_opacity=1,
            stroke_width=1.8,
        )

        self.play(Create(title_box), run_time=0.4)
        self.play(Write(title), run_time=0.9)
        self.play(
            Flash(
                title_box,
                color=SEPIA,
                flash_radius=0.4,
                line_length=0.15,
                num_lines=8,
            ),
            run_time=0.6,
        )

        self.wait(8.0)

        # Final fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
