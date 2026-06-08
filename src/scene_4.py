import sys
import numpy as np
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
GREEN = "#66BB6A"


class RNNDeepDive(Scene):
    def construct(self):
        # ================================================================
        #  PART 1 — N-GRAM RECAP: count patterns, but it doesn't scale
        # ================================================================

        # Mini lookup table
        table = Rectangle(
            width=4.5,
            height=3.0,
            color=DIM,
            stroke_width=2,
            fill_color="#0A0A0A",
            fill_opacity=1,
        )
        table.move_to(RIGHT * 1.5)

        # Grid lines inside table
        glines = VGroup()
        for i in range(1, 7):
            glines.add(
                Line(
                    table.get_left() + RIGHT * 0.08 + UP * (i * 0.42 - 1.3),
                    table.get_right() + LEFT * 0.08 + UP * (i * 0.42 - 1.3),
                    color=DIM2,
                    stroke_width=0.4,
                )
            )
        for i in range(1, 10):
            glines.add(
                Line(
                    table.get_bottom() + UP * 0.08 + RIGHT * (i * 0.45 - 2.1),
                    table.get_top() + DOWN * 0.08 + RIGHT * (i * 0.45 - 2.1),
                    color=DIM2,
                    stroke_width=0.4,
                )
            )

        tbl_label = Text("lookup table", font_size=16, color=DIM)
        tbl_label.next_to(table, DOWN, buff=0.2)

        # Input tokens on the left
        tokens_in = ["The", "capital", "of", "France", "is"]
        tok_mobs = VGroup(
            *[Text(t, font_size=22, color=WHITE) for t in tokens_in]
        )
        tok_mobs.arrange(DOWN, buff=0.25)
        tok_mobs.move_to(LEFT * 3.5)

        arrow_to_table = Arrow(
            LEFT * 1.8,
            table.get_left(),
            buff=0.1,
            color=DIM,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )

        # Prediction output
        pred_arrow = Arrow(
            table.get_right(),
            RIGHT * 5.5,
            buff=0.1,
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        pred_q = Text("?", font_size=30, color=GOLD)
        pred_q.next_to(pred_arrow, RIGHT, buff=0.15)

        self.play(
            LaggedStart(
                *[FadeIn(t, shift=RIGHT * 0.15) for t in tok_mobs],
                lag_ratio=0.08,
            ),
            run_time=0.7,
        )
        self.play(
            FadeIn(table),
            LaggedStart(*[Create(l) for l in glines], lag_ratio=0.02),
            FadeIn(tbl_label),
            run_time=0.7,
        )
        self.play(GrowArrow(arrow_to_table), run_time=0.4)
        self.play(GrowArrow(pred_arrow), FadeIn(pred_q), run_time=0.4)
        # [8:39] N-gram models give a simple way to use context: count patterns
        self.wait(4.0)

        # Red ✗ — "does not scale"
        x1 = Line(
            table.get_corner(UL) + DR * 0.25,
            table.get_corner(DR) + UL * 0.25,
            color=RED,
            stroke_width=4,
        )
        x2 = Line(
            table.get_corner(UR) + DL * 0.25,
            table.get_corner(DL) + UR * 0.25,
            color=RED,
            stroke_width=4,
        )

        no_scale = Text("does not scale", font_size=20, color=RED)
        no_scale.next_to(table, UP, buff=0.3)

        self.play(Create(x1), Create(x2), run_time=0.5)
        self.play(
            FadeIn(no_scale, scale=1.2),
            Flash(table.get_center(), color=RED, flash_radius=0.8, num_lines=10),
            run_time=0.5,
        )
        # [8:51] But this approach does not scale
        self.wait(6.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 2 — THE NEW QUESTION: compress context into memory
        # ================================================================

        q_text = Text(
            "Can we compress context into a smaller memory?",
            font_size=26,
            color=WHITE,
        )
        q_text.move_to(UP * 3.0)
        self.play(Write(q_text), run_time=0.9)
        # [8:55] Can the model compress everything into a smaller internal memory?
        self.wait(3.0)

        # The processing box (the "model")
        model_box = RoundedRectangle(
            width=2.2,
            height=1.6,
            corner_radius=0.2,
            color=ACCENT,
            stroke_width=2,
            fill_color="#0A1A2A",
            fill_opacity=1,
        )
        model_box.move_to(ORIGIN)

        # Hidden state dot — starts small
        state = Dot(radius=0.1, color=ACCENT, fill_opacity=0.2)
        state.move_to(model_box.get_center())

        h_label = MathTex(r"h", font_size=24, color=GOLD)
        h_label.next_to(model_box, DOWN, buff=0.15)

        self.play(FadeIn(model_box, scale=0.9), run_time=0.5)
        self.play(FadeIn(state, scale=0.5), FadeIn(h_label), run_time=0.3)

        input_words = ["The", "capital", "of", "France", "is"]
        state_radii = [0.13, 0.18, 0.24, 0.31, 0.38]
        state_opacs = [0.25, 0.35, 0.50, 0.65, 0.85]
        state_cols = [ACCENT, ACCENT, ACCENT, GOLD, GOLD]

        for i, word in enumerate(input_words):
            w = Text(word, font_size=22, color=WHITE)
            w.move_to(LEFT * 4.5)

            self.play(FadeIn(w, shift=RIGHT * 0.3), run_time=0.2)

            new_state = Dot(
                radius=state_radii[i],
                color=state_cols[i],
                fill_opacity=state_opacs[i],
            )
            new_state.move_to(model_box.get_center())

            self.play(
                w.animate.move_to(model_box.get_center()).scale(0.15).set_opacity(0),
                Transform(state, new_state),
                run_time=0.45,
            )
            self.remove(w)

        # [9:09] The key idea behind RNNs
        self.wait(2.0)

        # Output prediction
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

        self.play(GrowArrow(out_arrow), run_time=0.4)
        self.play(
            FadeIn(prediction, scale=1.2),
            Flash(prediction, color=GOLD, flash_radius=0.5, num_lines=8),
            run_time=0.5,
        )
        # [9:15] Hidden state — a learned vector updated with each token
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 3 — TOKENIZATION ASIDE
        # ================================================================

        tok_title = Text("tokenization", font_size=24, color=ACCENT)
        tok_title.move_to(UP * 2.5)

        # Word splitting visual
        full_word = Text("unhappiness", font_size=32, color=WHITE)
        full_word.move_to(UP * 1.0)

        self.play(Write(tok_title), run_time=0.5)
        self.play(FadeIn(full_word, shift=UP * 0.1), run_time=0.5)
        # [9:27] Tokenization — representing words as tokens
        self.wait(5.0)

        # Split into subword pieces
        pieces = ["un", "happi", "ness"]
        piece_mobs = VGroup(
            *[Text(p, font_size=28, color=GOLD) for p in pieces]
        )
        piece_mobs.arrange(RIGHT, buff=0.5)
        piece_mobs.move_to(DOWN * 0.3)

        # Boxes around each piece
        piece_boxes = VGroup()
        for pm in piece_mobs:
            box = SurroundingRectangle(
                pm,
                color=GOLD,
                buff=0.12,
                corner_radius=0.08,
                stroke_width=1.5,
                fill_color="#1A1500",
                fill_opacity=0.5,
            )
            piece_boxes.add(box)

        # Arrow from word to pieces
        split_arrow = Arrow(
            full_word.get_bottom(),
            piece_mobs.get_top(),
            buff=0.15,
            color=DIM,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.2,
        )

        self.play(GrowArrow(split_arrow), run_time=0.3)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(FadeIn(pm, scale=0.8), Create(bx))
                    for pm, bx in zip(piece_mobs, piece_boxes)
                ],
                lag_ratio=0.15,
            ),
            run_time=0.7,
        )
        # [9:44] Tokenization helps represent language using smaller building blocks
        self.wait(8.0)

        # "but that's another story"
        aside = Text("...but that's another story.", font_size=18, color=DIM)
        aside.move_to(DOWN * 1.8)

        # "From now on: words → tokens"
        switch_label = Text("words  →  tokens", font_size=22, color=ACCENT)
        switch_label.move_to(DOWN * 2.5)

        self.play(FadeIn(aside, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(switch_label, shift=UP * 0.1), run_time=0.5)
        # [9:57] But that is a story for another time
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 4 — RNN = NEURAL NETWORK + TIME (unrolled diagram)
        # ================================================================

        n_cells = 5
        cell_w = 1.0
        cell_h = 0.8
        cell_gap = 1.6
        start_x = -(n_cells - 1) * cell_gap / 2

        cells = VGroup()
        h_arrows = VGroup()
        x_arrows = VGroup()
        y_arrows = VGroup()
        x_labels = VGroup()
        y_labels = VGroup()
        h_labels = VGroup()

        token_names = ["The", "capital", "of", "France", "is"]

        for i in range(n_cells):
            cx = start_x + i * cell_gap

            # Cell box
            cell = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.1,
                color=ACCENT,
                stroke_width=2,
                fill_color="#0A1A2A",
                fill_opacity=1,
            )
            cell.move_to(RIGHT * cx)
            cells.add(cell)

            # h_t label inside cell
            hl = MathTex(f"h_{i}", font_size=18, color=GOLD)
            hl.move_to(cell.get_center())
            h_labels.add(hl)

            # Input arrow from below
            x_arr = Arrow(
                cell.get_bottom() + DOWN * 0.8,
                cell.get_bottom(),
                buff=0.05,
                color=WHITE,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.25,
            )
            x_arrows.add(x_arr)

            # Input label
            xl = Text(token_names[i], font_size=14, color=WHITE)
            xl.next_to(x_arr, DOWN, buff=0.08)
            x_labels.add(xl)

            # Output arrow upward
            y_arr = Arrow(
                cell.get_top(),
                cell.get_top() + UP * 0.8,
                buff=0.05,
                color=ACCENT,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.25,
            )
            y_arrows.add(y_arr)

            # Output label
            yl = MathTex(f"y_{i}", font_size=16, color=ACCENT)
            yl.next_to(y_arr, UP, buff=0.05)
            y_labels.add(yl)

            # Hidden state arrow to next cell
            if i < n_cells - 1:
                nx = start_x + (i + 1) * cell_gap
                h_arr = Arrow(
                    RIGHT * cx + RIGHT * cell_w / 2,
                    RIGHT * nx + LEFT * cell_w / 2,
                    buff=0.08,
                    color=GOLD,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.2,
                )
                h_arrows.add(h_arr)

        # Title
        rnn_title = Text("RNN — unrolled through time", font_size=22, color=DIM)
        rnn_title.to_edge(UP, buff=0.4)

        self.play(Write(rnn_title), run_time=0.5)

        # Build the diagram cell by cell
        for i in range(n_cells):
            anims = [
                FadeIn(cells[i], scale=0.8),
                FadeIn(h_labels[i]),
                GrowArrow(x_arrows[i]),
                FadeIn(x_labels[i]),
                GrowArrow(y_arrows[i]),
                FadeIn(y_labels[i]),
            ]
            if i > 0:
                anims.append(GrowArrow(h_arrows[i - 1]))

            self.play(*anims, run_time=0.45)

        # [10:03] RNNs as standard neural networks with the dimension of time
        self.wait(3.0)

        # Animate a pulse traveling through the hidden state chain
        pulse = Dot(radius=0.08, color=GOLD, fill_opacity=0.9)
        pulse.move_to(cells[0].get_center())
        self.play(FadeIn(pulse, scale=0.5), run_time=0.2)

        for i in range(n_cells - 1):
            self.play(
                pulse.animate.move_to(cells[i + 1].get_center()),
                run_time=0.35,
                rate_func=smooth,
            )

        self.play(
            Flash(cells[-1].get_center(), color=GOLD, flash_radius=0.4, num_lines=8),
            FadeOut(pulse),
            run_time=0.5,
        )
        # [10:10] As each token is read, the model updates its memory
        self.wait(10.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 5 — COMPRESSED MEMORY LIKE A HUMAN
        # ================================================================

        # Left: human head metaphor
        head = Circle(
            radius=0.7,
            color=WHITE,
            stroke_width=2,
            fill_color="#111111",
            fill_opacity=1,
        )
        head.move_to(LEFT * 3.0 + UP * 0.3)

        # Thought bubble (three circles)
        b1 = Circle(radius=0.08, color=DIM, stroke_width=1, fill_opacity=0)
        b1.next_to(head, UR, buff=0.1)
        b2 = Circle(radius=0.12, color=DIM, stroke_width=1, fill_opacity=0)
        b2.next_to(b1, UR, buff=0.08)
        thought = RoundedRectangle(
            width=2.0,
            height=0.8,
            corner_radius=0.15,
            color=DIM,
            stroke_width=1.5,
            fill_color="#151515",
            fill_opacity=1,
        )
        thought.next_to(b2, UR, buff=0.08)
        thought_text = Text("context so far...", font_size=12, color=DIM)
        thought_text.move_to(thought.get_center())

        human_label = Text("human", font_size=16, color=DIM)
        human_label.next_to(head, DOWN, buff=0.3)

        # Right: RNN cell with hidden state vector
        rnn_cell = RoundedRectangle(
            width=1.4,
            height=1.1,
            corner_radius=0.12,
            color=ACCENT,
            stroke_width=2,
            fill_color="#0A1A2A",
            fill_opacity=1,
        )
        rnn_cell.move_to(RIGHT * 3.0 + UP * 0.3)

        # Hidden state as a vertical bar of values
        h_vec = VGroup()
        vec_vals = [0.3, 0.7, 0.5, 0.9, 0.2, 0.6]
        for j, v in enumerate(vec_vals):
            cell_rect = Rectangle(
                width=0.3,
                height=0.15,
                color=GOLD,
                stroke_width=0.8,
                fill_color=GOLD,
                fill_opacity=v * 0.8,
            )
            h_vec.add(cell_rect)
        h_vec.arrange(DOWN, buff=0.02)
        h_vec.move_to(rnn_cell.get_center())

        rnn_label = Text("RNN", font_size=16, color=ACCENT)
        rnn_label.next_to(rnn_cell, DOWN, buff=0.3)

        # Divider
        divider = Line(UP * 2.0, DOWN * 1.5, color=DIM2, stroke_width=0.8)

        # Title
        mem_title = Text(
            "compressed memory", font_size=22, color=WHITE
        )
        mem_title.to_edge(UP, buff=0.5)

        self.play(Write(mem_title), run_time=0.5)
        self.play(Create(divider), run_time=0.3)

        # Human side
        self.play(
            FadeIn(head),
            FadeIn(human_label),
            run_time=0.5,
        )
        self.play(
            FadeIn(b1),
            FadeIn(b2),
            FadeIn(thought),
            Write(thought_text),
            run_time=0.6,
        )

        # RNN side
        self.play(
            FadeIn(rnn_cell),
            FadeIn(rnn_label),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(c, shift=DOWN * 0.05) for c in h_vec],
                lag_ratio=0.06,
            ),
            run_time=0.5,
        )
        # [10:20] This makes RNNs feel a little more human
        self.wait(18.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 6 — FORGETTING: signal fades through the chain
        # ================================================================

        fade_title = Text("the forgetting problem", font_size=22, color=RED)
        fade_title.to_edge(UP, buff=0.4)
        self.play(Write(fade_title), run_time=0.5)

        # Rebuild unrolled RNN chain (compact)
        n_fade = 7
        f_cell_w = 0.7
        f_cell_gap = 1.1
        f_start_x = -(n_fade - 1) * f_cell_gap / 2

        f_cells = VGroup()
        f_h_arrows = VGroup()
        f_labels = VGroup()

        fade_tokens = ["t₁", "t₂", "t₃", "t₄", "t₅", "t₆", "t₇"]

        for i in range(n_fade):
            cx = f_start_x + i * f_cell_gap
            cell = RoundedRectangle(
                width=f_cell_w,
                height=0.55,
                corner_radius=0.08,
                color=ACCENT,
                stroke_width=1.5,
                fill_color="#0A1A2A",
                fill_opacity=1,
            )
            cell.move_to(RIGHT * cx)
            f_cells.add(cell)

            lb = Text(fade_tokens[i], font_size=13, color=WHITE)
            lb.next_to(cell, DOWN, buff=0.12)
            f_labels.add(lb)

            if i < n_fade - 1:
                nx = f_start_x + (i + 1) * f_cell_gap
                arr = Arrow(
                    RIGHT * cx + RIGHT * f_cell_w / 2,
                    RIGHT * nx + LEFT * f_cell_w / 2,
                    buff=0.06,
                    color=GOLD,
                    stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.2,
                )
                f_h_arrows.add(arr)

        chain_grp = VGroup(f_cells, f_h_arrows, f_labels)
        chain_grp.move_to(ORIGIN)

        self.play(
            FadeIn(f_cells),
            FadeIn(f_labels),
            LaggedStart(*[GrowArrow(a) for a in f_h_arrows], lag_ratio=0.05),
            run_time=0.8,
        )
        # [10:44] But there is a catch — these models can forget
        self.wait(3.0)

        # Highlight first token in GOLD, then watch it fade through cells
        glow = f_cells[0].copy().set_stroke(GOLD, width=3).set_fill(GOLD, opacity=0.3)
        self.play(FadeIn(glow), run_time=0.3)

        # Create fading trail — each subsequent cell gets dimmer
        fade_glows = []
        for i in range(1, n_fade):
            opacity = max(0.3 - i * 0.04, 0.02)
            fg = f_cells[i].copy().set_stroke(GOLD, width=max(3 - i * 0.4, 0.5)).set_fill(
                GOLD, opacity=opacity
            )
            fade_glows.append(fg)

        for i, fg in enumerate(fade_glows):
            self.play(FadeIn(fg), run_time=0.25)

        # [10:56] Earlier information has to survive through many updates
        self.wait(5.0)

        # "information fades" label
        info_fade = Text("early information fades away", font_size=18, color=RED)
        info_fade.next_to(chain_grp, DOWN, buff=0.7)

        # Gradient arrow showing decay
        decay_arrow = Arrow(
            f_cells[0].get_bottom() + DOWN * 0.35,
            f_cells[-1].get_bottom() + DOWN * 0.35,
            buff=0,
            color=RED,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.1,
        )

        self.play(
            FadeIn(info_fade, scale=1.1),
            GrowArrow(decay_arrow),
            run_time=0.6,
        )
        # [11:05] Important details from the beginning slowly fade away
        self.wait(15.0)

        self.play(*[FadeOut(m) for m in self.mobjects + [glow] + fade_glows], run_time=0.6)

        # ================================================================
        #  PART 7 — HIDDEN STATE SIZE: fixed capacity
        # ================================================================

        size_title = Text("hidden state = fixed-size memory", font_size=22, color=WHITE)
        size_title.to_edge(UP, buff=0.4)
        self.play(Write(size_title), run_time=0.5)

        # Small hidden state
        small_label = Text("small hidden state", font_size=16, color=DIM)
        small_bar = VGroup()
        for j in range(4):
            r = Rectangle(
                width=0.6, height=0.25,
                color=GOLD, stroke_width=1,
                fill_color=GOLD, fill_opacity=0.4,
            )
            small_bar.add(r)
        small_bar.arrange(DOWN, buff=0.02)
        small_bar.move_to(LEFT * 3.0)
        small_label.next_to(small_bar, DOWN, buff=0.3)

        # Large hidden state
        large_label = Text("large hidden state", font_size=16, color=ACCENT)
        large_bar = VGroup()
        for j in range(10):
            r = Rectangle(
                width=0.6, height=0.25,
                color=ACCENT, stroke_width=1,
                fill_color=ACCENT, fill_opacity=0.4,
            )
            large_bar.add(r)
        large_bar.arrange(DOWN, buff=0.02)
        large_bar.move_to(RIGHT * 3.0)
        large_label.next_to(large_bar, DOWN, buff=0.3)

        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in small_bar], lag_ratio=0.05),
            FadeIn(small_label),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in large_bar], lag_ratio=0.03),
            FadeIn(large_label),
            run_time=0.6,
        )
        # [11:12] By changing the size of the hidden state
        self.wait(5.0)

        # "But still fixed" brace
        brace_s = Brace(small_bar, LEFT, color=DIM)
        brace_l = Brace(large_bar, RIGHT, color=ACCENT)

        fixed_s = Text("fixed", font_size=14, color=RED)
        fixed_s.next_to(brace_s, LEFT, buff=0.1)
        fixed_l = Text("still fixed", font_size=14, color=RED)
        fixed_l.next_to(brace_l, RIGHT, buff=0.1)

        self.play(
            GrowFromCenter(brace_s), FadeIn(fixed_s),
            GrowFromCenter(brace_l), FadeIn(fixed_l),
            run_time=0.6,
        )
        # [11:25] A larger hidden state gives more space
        self.wait(5.0)

        # Key point
        key_point = Text(
            "No matter how long the sequence, same capacity.",
            font_size=18,
            color=DIM,
        )
        key_point.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(key_point, shift=UP * 0.1), run_time=0.6)
        # [11:29] But this memory is still fixed in size
        self.wait(10.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 8 — SHORT vs LONG SEQUENCES
        # ================================================================

        # --- Short sequence (works well) ---
        short_title = Text("short sequence", font_size=18, color=GREEN)
        short_title.move_to(UP * 3.0 + LEFT * 3.0)

        n_short = 3
        s_cells = VGroup()
        s_arrows = VGroup()
        s_cx_start = -4.5

        for i in range(n_short):
            cx = s_cx_start + i * 1.1
            cell = RoundedRectangle(
                width=0.65, height=0.45, corner_radius=0.07,
                color=GREEN, stroke_width=1.5,
                fill_color="#0A2A0A", fill_opacity=1,
            )
            cell.move_to(RIGHT * cx + UP * 1.5)
            s_cells.add(cell)
            if i < n_short - 1:
                arr = Arrow(
                    cell.get_right(), cell.get_right() + RIGHT * 0.45,
                    buff=0.06, color=GOLD, stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.25,
                )
                s_arrows.add(arr)

        # Prediction: check mark
        s_pred = Arrow(
            s_cells[-1].get_right(), s_cells[-1].get_right() + RIGHT * 0.8,
            buff=0.06, color=GREEN, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        check = Text("✓", font_size=24, color=GREEN)
        check.next_to(s_pred, RIGHT, buff=0.1)

        self.play(Write(short_title), run_time=0.3)
        self.play(
            FadeIn(s_cells),
            LaggedStart(*[GrowArrow(a) for a in s_arrows], lag_ratio=0.1),
            run_time=0.5,
        )
        self.play(GrowArrow(s_pred), FadeIn(check, scale=1.2), run_time=0.4)
        # [11:42] For short sequences, this works fairly well
        self.wait(4.0)

        # --- Long sequence (struggles) ---
        long_title = Text("long sequence", font_size=18, color=RED)
        long_title.move_to(UP * 3.0 + RIGHT * 3.0)

        n_long = 8
        l_cells = VGroup()
        l_arrows = VGroup()
        l_cx_start = 0.5

        for i in range(n_long):
            cx = l_cx_start + i * 0.75
            # Cells get progressively dimmer
            opacity = max(0.8 - i * 0.08, 0.2)
            cell = RoundedRectangle(
                width=0.45, height=0.35, corner_radius=0.06,
                color=ACCENT, stroke_width=1.0,
                fill_color="#0A1A2A", fill_opacity=opacity,
            )
            cell.move_to(RIGHT * cx + UP * 1.5)
            l_cells.add(cell)
            if i < n_long - 1:
                arr = Arrow(
                    cell.get_right(), cell.get_right() + RIGHT * 0.3,
                    buff=0.04, color=GOLD, stroke_width=1,
                    max_tip_length_to_length_ratio=0.3,
                )
                l_arrows.add(arr)

        # Prediction: question mark
        l_pred = Arrow(
            l_cells[-1].get_right(), l_cells[-1].get_right() + RIGHT * 0.6,
            buff=0.06, color=RED, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        q_mark = Text("?", font_size=24, color=RED)
        q_mark.next_to(l_pred, RIGHT, buff=0.1)

        self.play(Write(long_title), run_time=0.3)
        self.play(
            FadeIn(l_cells),
            LaggedStart(*[GrowArrow(a) for a in l_arrows], lag_ratio=0.03),
            run_time=0.5,
        )
        self.play(GrowArrow(l_pred), FadeIn(q_mark, scale=1.2), run_time=0.4)
        self.wait(4.0)

        # Labels below
        short_ok = Text("hidden state retains info", font_size=14, color=GREEN)
        short_ok.next_to(s_cells, DOWN, buff=0.5)
        long_bad = Text("early tokens fade away", font_size=14, color=RED)
        long_bad.next_to(l_cells, DOWN, buff=0.5)

        self.play(FadeIn(short_ok), FadeIn(long_bad), run_time=0.5)
        # [11:53] But as the sequence grows longer, the model struggles
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 9 — LSTM: better gates, same chain
        # ================================================================

        lstm_title = Text("LSTM — gated memory", font_size=22, color=ACCENT)
        lstm_title.to_edge(UP, buff=0.4)
        self.play(Write(lstm_title), run_time=0.5)

        # Single LSTM cell (detailed view)
        lstm_box = RoundedRectangle(
            width=3.0, height=2.2, corner_radius=0.15,
            color=ACCENT, stroke_width=2,
            fill_color="#0A1A2A", fill_opacity=1,
        )
        lstm_box.move_to(UP * 0.2)

        # Three gates inside
        gate_colors = [RED, GREEN, ACCENT]
        gate_names = ["forget", "input", "output"]
        gates = VGroup()
        gate_labels = VGroup()

        for i, (gc, gn) in enumerate(zip(gate_colors, gate_names)):
            gate = RoundedRectangle(
                width=0.65, height=0.45, corner_radius=0.06,
                color=gc, stroke_width=2,
                fill_color=gc, fill_opacity=0.15,
            )
            gate.move_to(lstm_box.get_center() + LEFT * 0.85 + RIGHT * i * 0.85 + UP * 0.15)
            gates.add(gate)

            gl = Text(gn, font_size=10, color=gc)
            gl.next_to(gate, DOWN, buff=0.06)
            gate_labels.add(gl)

        # Cell state line through the top
        c_line = Arrow(
            lstm_box.get_left() + UP * 0.7,
            lstm_box.get_right() + UP * 0.7,
            buff=0.1,
            color=GOLD,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.1,
        )
        c_label = MathTex(r"c_t", font_size=18, color=GOLD)
        c_label.next_to(c_line, UP, buff=0.05)

        self.play(FadeIn(lstm_box), run_time=0.4)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(FadeIn(g, scale=0.8), FadeIn(gl))
                    for g, gl in zip(gates, gate_labels)
                ],
                lag_ratio=0.2,
            ),
            run_time=0.7,
        )
        self.play(GrowArrow(c_line), FadeIn(c_label), run_time=0.4)
        # [12:08] LSTMs use gates to decide what to remember/forget
        self.wait(5.0)

        # Animate gates "opening and closing"
        for gate in gates:
            self.play(
                gate.animate.set_fill(opacity=0.5),
                run_time=0.2,
            )
            self.play(
                gate.animate.set_fill(opacity=0.15),
                run_time=0.2,
            )

        self.wait(3.0)

        # Shrink and show chain — still sequential
        detail_grp = VGroup(lstm_box, gates, gate_labels, c_line, c_label)
        self.play(
            detail_grp.animate.scale(0.5).move_to(UP * 2.5 + LEFT * 3.0),
            run_time=0.6,
        )

        # Chain of LSTM cells
        n_lstm = 6
        lstm_cells_chain = VGroup()
        lstm_chain_arrows = VGroup()
        chain_start_x = -3.0

        for i in range(n_lstm):
            cx = chain_start_x + i * 1.3
            cell = RoundedRectangle(
                width=0.8, height=0.55, corner_radius=0.08,
                color=ACCENT, stroke_width=1.5,
                fill_color="#0A1A2A", fill_opacity=1,
            )
            cell.move_to(RIGHT * cx + DOWN * 0.5)

            # Mini gate indicators inside
            for gi, gc in enumerate([RED, GREEN, ACCENT]):
                mini = Dot(radius=0.04, color=gc, fill_opacity=0.6)
                mini.move_to(cell.get_center() + LEFT * 0.15 + RIGHT * gi * 0.15)
                cell.add(mini)

            lstm_cells_chain.add(cell)

            if i < n_lstm - 1:
                nx = chain_start_x + (i + 1) * 1.3
                arr = Arrow(
                    RIGHT * cx + RIGHT * 0.4,
                    RIGHT * nx + LEFT * 0.4,
                    buff=0.06, color=GOLD, stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.2,
                )
                lstm_chain_arrows.add(arr)

        chain_label = Text("still sequential", font_size=18, color=RED)
        chain_label.next_to(lstm_cells_chain, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(c, scale=0.8) for c in lstm_cells_chain],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in lstm_chain_arrows],
                lag_ratio=0.06,
            ),
            run_time=0.5,
        )
        self.play(FadeIn(chain_label, scale=1.1), run_time=0.4)
        # [12:30] The fundamental limitation remains: context flows step by step
        self.wait(5.0)

        # Long brace under chain
        chain_brace = Brace(
            VGroup(lstm_cells_chain, lstm_chain_arrows), DOWN, color=DIM
        )
        chain_brace.next_to(chain_label, DOWN, buff=0.2)
        brace_label = Text("better memory, but still step-by-step", font_size=14, color=DIM)
        brace_label.next_to(chain_brace, DOWN, buff=0.1)

        self.play(
            GrowFromCenter(chain_brace),
            FadeIn(brace_label),
            run_time=0.5,
        )
        # [12:39] Information from first token must travel through the chain
        self.wait(10.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 10 — INFORMATION TRAVELS STEP BY STEP
        # ================================================================

        step_title = Text("information must travel through every step", font_size=20, color=WHITE)
        step_title.to_edge(UP, buff=0.4)
        self.play(Write(step_title), run_time=0.6)

        # Chain of cells
        n_steps = 8
        step_cells = VGroup()
        step_arrows = VGroup()
        step_start = -(n_steps - 1) * 0.95 / 2

        for i in range(n_steps):
            cx = step_start + i * 0.95
            cell = RoundedRectangle(
                width=0.55, height=0.4, corner_radius=0.06,
                color=DIM, stroke_width=1.5,
                fill_color="#111111", fill_opacity=1,
            )
            cell.move_to(RIGHT * cx)
            step_cells.add(cell)

            if i < n_steps - 1:
                nx = step_start + (i + 1) * 0.95
                arr = Arrow(
                    RIGHT * cx + RIGHT * 0.275,
                    RIGHT * nx + LEFT * 0.275,
                    buff=0.04, color=DIM2, stroke_width=1.2,
                    max_tip_length_to_length_ratio=0.25,
                )
                step_arrows.add(arr)

        self.play(
            FadeIn(step_cells), FadeIn(step_arrows),
            run_time=0.6,
        )

        # Highlight first cell (source) and last cell (destination)
        source_glow = step_cells[0].copy().set_stroke(GOLD, width=3).set_fill(GOLD, opacity=0.3)
        dest_glow = step_cells[-1].copy().set_stroke(ACCENT, width=3).set_fill(ACCENT, opacity=0.2)

        src_label = MathTex(r"t_1", font_size=18, color=GOLD)
        src_label.next_to(step_cells[0], DOWN, buff=0.2)
        dst_label = MathTex(r"t_8", font_size=18, color=ACCENT)
        dst_label.next_to(step_cells[-1], DOWN, buff=0.2)

        self.play(
            FadeIn(source_glow), FadeIn(dest_glow),
            FadeIn(src_label), FadeIn(dst_label),
            run_time=0.4,
        )

        # Animate signal hopping through each cell with decay
        signal = Dot(radius=0.07, color=GOLD, fill_opacity=1.0)
        signal.move_to(step_cells[0].get_center())
        self.play(FadeIn(signal), run_time=0.2)

        hop_labels = VGroup()
        for i in range(n_steps - 1):
            # Fade the signal as it travels
            new_opacity = max(1.0 - (i + 1) * 0.12, 0.15)
            self.play(
                signal.animate.move_to(step_cells[i + 1].get_center()).set_opacity(new_opacity),
                run_time=0.3,
            )

        # Show number of hops
        hops_label = Text(f"{n_steps - 1} hops", font_size=20, color=RED)
        hops_label.next_to(step_cells, DOWN, buff=0.8)

        fragile = Text("long and fragile path", font_size=16, color=RED)
        fragile.next_to(hops_label, DOWN, buff=0.2)

        self.play(
            FadeIn(hops_label, scale=1.1),
            FadeIn(fragile),
            FadeOut(signal),
            run_time=0.5,
        )
        # [12:50] Even with better memory, still forced to carry context
        self.wait(5.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 11 — THE KEY QUESTIONS + complete graph
        # ================================================================

        # Dramatic black pause
        self.wait(0.3)

        # First question
        q1 = Text(
            "What if memory didn't have to travel step by step?",
            font_size=24,
            color=WHITE,
        )
        q1.move_to(UP * 1.0)

        self.play(Write(q1), run_time=1.2)
        # [12:57] What if the model didn't have to carry memory step by step?
        self.wait(0.5)

        # Second question
        q2 = Text(
            "What if every token could look at every other token?",
            font_size=24,
            color=GOLD,
        )
        q2.move_to(DOWN * 0.3)

        self.play(Write(q2), run_time=1.2)
        # [13:05] What if every token could look directly at every other token?
        self.wait(0.3)

        # Move questions up
        self.play(
            q1.animate.move_to(UP * 3.0).scale(0.7).set_opacity(0.5),
            q2.animate.move_to(UP * 2.3).scale(0.7).set_opacity(0.5),
            run_time=0.7,
        )

        # Complete graph — all tokens connected to all
        n_nodes = 8
        node_radius = 2.0
        nodes = VGroup()
        node_labels = VGroup()
        token_names_graph = ["t₁", "t₂", "t₃", "t₄", "t₅", "t₆", "t₇", "t₈"]

        for i in range(n_nodes):
            angle = i * TAU / n_nodes - PI / 2
            pos = np.array([
                node_radius * np.cos(angle),
                node_radius * np.sin(angle),
                0,
            ])
            pos += DOWN * 0.5  # shift the whole graph down

            node = Dot(radius=0.12, color=ACCENT, fill_opacity=0.8)
            node.move_to(pos)
            nodes.add(node)

            label = Text(token_names_graph[i], font_size=12, color=WHITE)
            # Place label slightly outside the circle
            label_pos = pos + (pos - DOWN * 0.5) / node_radius * 0.3
            label.move_to(label_pos)
            node_labels.add(label)

        # Draw all edges
        edges = VGroup()
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = Line(
                    nodes[i].get_center(),
                    nodes[j].get_center(),
                    color=GOLD,
                    stroke_width=0.8,
                    stroke_opacity=0.3,
                )
                edges.add(edge)

        # Animate nodes appearing
        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.5) for n in nodes],
                lag_ratio=0.06,
            ),
            LaggedStart(
                *[FadeIn(l) for l in node_labels],
                lag_ratio=0.06,
            ),
            run_time=0.8,
        )

        # Animate edges appearing with glow
        self.play(
            LaggedStart(
                *[Create(e) for e in edges],
                lag_ratio=0.01,
            ),
            run_time=1.2,
        )

        # Make edges glow brighter
        self.play(
            *[e.animate.set_stroke(opacity=0.7) for e in edges],
            run_time=0.6,
        )

        # Flash on each node
        self.play(
            *[
                Flash(
                    n.get_center(),
                    color=GOLD,
                    flash_radius=0.25,
                    num_lines=6,
                    line_length=0.1,
                )
                for n in nodes
            ],
            run_time=0.6,
        )

        direct_label = Text("direct access", font_size=18, color=GOLD)
        direct_label.next_to(VGroup(nodes, edges), DOWN, buff=0.4)
        self.play(FadeIn(direct_label, shift=UP * 0.1), run_time=0.4)

        self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 12 — TRANSFORMERS TITLE CARD
        # ================================================================

        self.wait(0.3)

        # Bring back the complete graph, smaller, as a backdrop
        small_nodes = VGroup()
        small_edges = VGroup()

        for i in range(n_nodes):
            angle = i * TAU / n_nodes - PI / 2
            pos = np.array([
                1.2 * np.cos(angle),
                1.2 * np.sin(angle),
                0,
            ]) + UP * 0.8

            node = Dot(radius=0.06, color=ACCENT, fill_opacity=0.4)
            node.move_to(pos)
            small_nodes.add(node)

        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = Line(
                    small_nodes[i].get_center(),
                    small_nodes[j].get_center(),
                    color=GOLD,
                    stroke_width=0.5,
                    stroke_opacity=0.2,
                )
                small_edges.add(edge)

        self.play(
            FadeIn(small_nodes),
            FadeIn(small_edges),
            run_time=0.8,
        )

        # Title
        title = Text("Transformers", font_size=36, color=ACCENT, weight=BOLD)
        title.move_to(DOWN * 1.2)

        title_box = SurroundingRectangle(
            title,
            color=SEPIA,
            buff=0.3,
            corner_radius=0.18,
            fill_color=SEPIA_DARK,
            fill_opacity=1,
            stroke_width=2,
        )

        self.play(Create(title_box), run_time=0.5)
        self.play(Write(title), run_time=1.0)

        # Flash
        self.play(
            Flash(
                title_box,
                color=SEPIA,
                flash_radius=0.5,
                line_length=0.2,
                num_lines=10,
            ),
            run_time=0.6,
        )

        # Make the graph lines glow brighter momentarily
        self.play(
            *[e.animate.set_stroke(opacity=0.6) for e in small_edges],
            *[n.animate.set_fill(opacity=0.8) for n in small_nodes],
            run_time=0.5,
        )

        # [13:11] That idea brings us to Transformers
        self.wait(1.0)

        # Final fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
