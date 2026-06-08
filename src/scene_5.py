import sys
import numpy as np
from pathlib import Path

from utils.artifacts import *

CMD = Path(sys.argv[0]).name.lower()
if "manimgl" in CMD:
    from manimlib import *
else:
    from manim import *

from utils.tex_text import Text

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
PURPLE = "#B39DDB"


class AttentionMechanism(Scene):
    def construct(self):
        # ================================================================
        #  PART 1 — TRANSITION: Attention-based architectures
        # ================================================================

        # Small complete graph echoing scene_4 ending
        n_nodes = 6
        graph_r = 0.9
        intro_nodes = VGroup()
        intro_edges = VGroup()

        for i in range(n_nodes):
            angle = i * TAU / n_nodes - PI / 2
            pos = (
                np.array(
                    [
                        graph_r * np.cos(angle),
                        graph_r * np.sin(angle),
                        0,
                    ]
                )
                + UP * 1.0
            )
            node = Dot(radius=0.05, color=ACCENT, fill_opacity=0.5)
            node.move_to(pos)
            intro_nodes.add(node)

        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = Line(
                    intro_nodes[i].get_center(),
                    intro_nodes[j].get_center(),
                    color=GOLD,
                    stroke_width=0.6,
                    stroke_opacity=0.25,
                )
                intro_edges.add(edge)

        trans_label = Text(
            "attention-based architectures",
            font_size=22,
            color=ACCENT,
        )
        trans_label.move_to(DOWN * 0.8)

        era_label = Text("the present day", font_size=16, color=DIM)
        era_label.next_to(trans_label, DOWN, buff=0.3)

        self.play(
            FadeIn(intro_nodes),
            FadeIn(intro_edges),
            run_time=0.7,
        )
        self.play(
            Write(trans_label),
            FadeIn(era_label, shift=UP * 0.1),
            run_time=0.8,
        )
        # [13:16] This brings us to the present day — attention-based architectures
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 2 — THE ATTENTION IDEA: example sentence
        # ================================================================

        # Use one Tex object per line.
        # Important words are separate arguments so we can highlight them cleanly.
        row1 = Tex(
            r"The~",
            r"animal",
            r"~didn't cross the~",
            r"street",
            font_size=30,
            color=WHITE,
        )

        row2 = Tex(
            r"because~",
            r"it",
            r"~was too tired.",
            font_size=30,
            color=WHITE,
        )

        sentence = VGroup(row1, row2).arrange(
            DOWN,
            buff=0.38,
            aligned_edge=LEFT,
        )
        sentence.move_to(UP * 0.55)

        # Important references
        animal_word = row1[1]
        street_word = row1[3]
        it_word = row2[1]

        self.play(
            LaggedStart(
                FadeIn(row1[0], shift=UP * 0.08),
                FadeIn(row1[1], shift=UP * 0.08),
                FadeIn(row1[2], shift=UP * 0.08),
                FadeIn(row1[3], shift=UP * 0.08),
                FadeIn(row2[0], shift=UP * 0.08),
                FadeIn(row2[1], shift=UP * 0.08),
                FadeIn(row2[2], shift=UP * 0.08),
                lag_ratio=0.08,
            ),
            run_time=1.0,
        )

        # [13:25] The core idea is the attention mechanism
        self.wait(4.0)

        # ================================================================
        #  Highlight "it"
        # ================================================================

        it_highlight = SurroundingRectangle(
            it_word,
            color=GOLD,
            buff=0.08,
            corner_radius=0.06,
            stroke_width=2.5,
            fill_color=GOLD,
            fill_opacity=0.1,
        )

        self.play(Create(it_highlight), run_time=0.4)

        # [13:38] To understand "it," the model needs to know what it refers to
        self.wait(3.0)

        # ================================================================
        #  PART 3 — AMBIGUITY: what does "it" refer to?
        # ================================================================

        animal_hl = SurroundingRectangle(
            animal_word,
            color=GREEN,
            buff=0.08,
            corner_radius=0.06,
            stroke_width=2,
            fill_color=GREEN,
            fill_opacity=0.08,
        )

        street_hl = SurroundingRectangle(
            street_word,
            color=RED,
            buff=0.08,
            corner_radius=0.06,
            stroke_width=2,
            fill_color=RED,
            fill_opacity=0.08,
        )

        self.play(
            Create(animal_hl),
            Create(street_hl),
            run_time=0.5,
        )

        # ================================================================
        #  Arrows: point to the BOTTOM of the candidate boxes
        # ================================================================

        start = it_highlight.get_top() + UP * 0.05

        q_arrow_animal = CurvedArrow(
            start,
            animal_hl.get_bottom() + DOWN * 0.05,
            angle=-0.75,
            color=GREEN,
            stroke_width=2,
            tip_length=0.12,
        )

        q_arrow_street = CurvedArrow(
            start,
            street_hl.get_bottom() + DOWN * 0.05,
            angle=0.35,
            color=RED,
            stroke_width=2,
            tip_length=0.12,
        )

        q_label = Tex(
            r"\text{``it'' = ?}",
            font_size=28,
            color=GOLD,
        )
        q_label.next_to(sentence, DOWN, buff=0.8)

        animal_opt = Tex(
            r"\text{animal?}",
            font_size=23,
            color=GREEN,
        )
        street_opt = Tex(
            r"\text{street?}",
            font_size=23,
            color=RED,
        )

        animal_opt.next_to(q_label, LEFT, buff=0.9)
        street_opt.next_to(q_label, RIGHT, buff=0.9)

        self.play(
            Create(q_arrow_animal),
            Create(q_arrow_street),
            FadeIn(q_label),
            FadeIn(animal_opt),
            FadeIn(street_opt),
            run_time=0.7,
        )

        # [13:45] Is it "animal" or is it "street"?
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 4 — RNN/LSTM: step-by-step, connection weakens
        # ================================================================

        rnn_title = Text("RNN / LSTM", font_size=20, color=DIM)
        rnn_title.to_edge(UP, buff=0.4)
        self.play(Write(rnn_title), run_time=0.4)

        # Compact chain of cells
        chain_words = [
            "The",
            "animal",
            "didn't",
            "cross",
            "the",
            "street",
            "because",
            "it",
        ]
        n_chain = len(chain_words)
        c_w = 0.65
        c_gap = 0.9
        c_start = -(n_chain - 1) * c_gap / 2

        chain_cells = VGroup()
        chain_arrows = VGroup()
        chain_labels = VGroup()

        for i in range(n_chain):
            cx = c_start + i * c_gap
            cell = RoundedRectangle(
                width=c_w,
                height=0.4,
                corner_radius=0.06,
                color=ACCENT if i != 1 else GREEN,
                stroke_width=1.5,
                fill_color="#0A1A2A",
                fill_opacity=1,
            )
            cell.move_to(RIGHT * cx + UP * 0.5)
            chain_cells.add(cell)

            lb = Text(chain_words[i], font_size=10, color=WHITE)
            lb.next_to(cell, DOWN, buff=0.1)
            chain_labels.add(lb)

            if i < n_chain - 1:
                arr = Arrow(
                    cell.get_right(),
                    cell.get_right() + RIGHT * 0.25,
                    buff=0.04,
                    color=GOLD,
                    stroke_width=1.2,
                    max_tip_length_to_length_ratio=0.3,
                )
                chain_arrows.add(arr)

        # Color "animal" cell green, "it" cell gold
        chain_cells[1].set_stroke(GREEN, width=2)
        chain_cells[7].set_stroke(GOLD, width=2)

        self.play(
            FadeIn(chain_cells),
            FadeIn(chain_labels),
            LaggedStart(*[GrowArrow(a) for a in chain_arrows], lag_ratio=0.03),
            run_time=0.7,
        )
        # [13:54] In older models, information travels step by step
        self.wait(3.0)

        # Show signal fading from "animal" to "it"
        # Draw dotted path highlighting the 6 hops
        hop_path = VGroup()
        for i in range(1, 7):
            seg = Line(
                chain_cells[i].get_right() + RIGHT * 0.03,
                chain_cells[i + 1].get_left() + LEFT * 0.03,
                color=GREEN,
                stroke_width=2.5,
                stroke_opacity=max(1.0 - i * 0.15, 0.1),
            )
            hop_path.add(seg)

        self.play(
            LaggedStart(*[Create(s) for s in hop_path], lag_ratio=0.08),
            run_time=0.8,
        )

        fade_label = Text("signal weakens over 6 steps", font_size=14, color=RED)
        fade_label.next_to(chain_cells, DOWN, buff=0.6)

        self.play(FadeIn(fade_label, shift=UP * 0.08), run_time=0.4)
        # [14:03] If the relevant word appeared much earlier, connection becomes weak
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 5 — TRANSFORMERS HANDLE THIS DIFFERENTLY
        # ================================================================

        tf_title = Tex(
            r"\text{Transformer}",
            font_size=30,
            color=ACCENT,
        )
        tf_title.to_edge(UP, buff=0.55)

        self.play(Write(tf_title), run_time=0.4)

        # ------------------------------------------------
        # Sentence tokens as dots in a line
        # ------------------------------------------------

        attn_words = [
            "The",
            "animal",
            "didn't",
            "cross",
            "the",
            "street",
            "because",
            "it",
        ]

        n_attn = len(attn_words)
        attn_gap = 0.95
        attn_start = -(n_attn - 1) * attn_gap / 2

        attn_dots = VGroup()
        attn_labels = VGroup()

        for i, word in enumerate(attn_words):
            cx = attn_start + i * attn_gap

            dot = Dot(
                radius=0.085,
                color=ACCENT,
                fill_opacity=0.75,
            )
            dot.move_to(RIGHT * cx + DOWN * 0.35)
            attn_dots.add(dot)

            label = Tex(
                rf"\text{{{word}}}",
                font_size=17,
                color=WHITE,
            )
            label.next_to(dot, DOWN, buff=0.14)
            attn_labels.add(label)

        # Special token colors
        attn_dots[1].set_color(GREEN)  # animal
        attn_dots[7].set_color(GOLD)  # it

        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in attn_dots],
                lag_ratio=0.04,
            ),
            LaggedStart(
                *[FadeIn(l) for l in attn_labels],
                lag_ratio=0.04,
            ),
            run_time=0.7,
        )

        # [14:14] Transformers handle this differently — with attention
        self.wait(3.0)

        # ------------------------------------------------
        # Curved attention arrow: "it" looks back to "animal"
        # ------------------------------------------------

        main_start = attn_dots[7].get_top() + UP * 0.05
        main_end = attn_dots[1].get_top() + UP * 0.05

        attn_arrow_main = CurvedArrow(
            main_start,
            main_end,
            angle=PI / 2,  # positive here makes it curve upward
            color=GOLD,
            stroke_width=3.2,
            tip_length=0.16,
        )

        self.play(
            Create(attn_arrow_main),
            run_time=0.7,
        )

        self.play(
            Flash(
                attn_dots[1].get_center(),
                color=GREEN,
                flash_radius=0.3,
                num_lines=6,
            ),
            run_time=0.4,
        )

        # ------------------------------------------------
        # Dimmer attention connections to other tokens
        # ------------------------------------------------

        attn_lines_dim = VGroup()

        for i in range(n_attn):
            if i == 7 or i == 1:
                continue

            dim_start = attn_dots[7].get_top() + UP * 0.03
            dim_end = attn_dots[i].get_top() + UP * 0.03

            dim_arrow = CurvedArrow(
                dim_start,
                dim_end,
                angle=PI / 3,
                color=ACCENT,
                stroke_width=0.9,
                stroke_opacity=0.18,
                tip_length=0.08,
            )

            attn_lines_dim.add(dim_arrow)

        self.play(
            LaggedStart(
                *[Create(l) for l in attn_lines_dim],
                lag_ratio=0.03,
            ),
            run_time=0.5,
        )

        # [14:23] "it" can directly look back and assign more weight to "animal"
        self.wait(3.0)

        # ------------------------------------------------
        # Attention weight label
        # ------------------------------------------------

        weight_main = Tex(
            r"0.72",
            font_size=20,
            color=GOLD,
        )

        weight_main.move_to(attn_arrow_main.point_from_proportion(0.5) + UP * 0.15)

        self.play(
            FadeIn(weight_main, scale=1.1),
            run_time=0.3,
        )

        # ------------------------------------------------
        # Direct connection label
        # ------------------------------------------------

        direct_label = Tex(
            r"\text{direct connection - no chain needed}",
            font_size=24,
            color=GOLD,
        )

        direct_label.next_to(attn_labels, DOWN, buff=0.55)

        self.play(
            FadeIn(direct_label, shift=UP * 0.1),
            run_time=0.5,
        )

        # [14:31] Instead of relying on compressed memory, Transformer builds direct connections
        self.wait(10.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 6 — WHY ATTENTION IS POWERFUL
        # ================================================================

        # Full attention visualization: every token attends to every other
        n_full = 6
        full_gap = 1.2
        full_start = -(n_full - 1) * full_gap / 2
        full_tokens = [r"$t_1$", r"$t_2$", r"$t_3$", r"$t_4$", r"$t_5$", r"$t_6$"]

        full_dots = VGroup()
        full_labels = VGroup()

        for i in range(n_full):
            cx = full_start + i * full_gap
            dot = Dot(radius=0.1, color=ACCENT, fill_opacity=0.7)
            dot.move_to(RIGHT * cx + UP * 1.5)
            full_dots.add(dot)

            lb = Tex(full_tokens[i], color=WHITE, font_size=20)
            lb.next_to(dot, DOWN, buff=0.12)
            full_labels.add(lb)

        # All pairwise connections
        full_edges = VGroup()
        for i in range(n_full):
            for j in range(i + 1, n_full):
                e = Line(
                    full_dots[i].get_center(),
                    full_dots[j].get_center(),
                    color=GOLD,
                    stroke_width=1.0,
                    stroke_opacity=0.3,
                )
                full_edges.add(e)

        self.play(
            FadeIn(full_dots),
            FadeIn(full_labels),
            LaggedStart(*[Create(e) for e in full_edges], lag_ratio=0.01),
            run_time=0.8,
        )

        power_label = Text(
            "each token sees every other token",
            font_size=18,
            color=GOLD,
        )
        power_label.move_to(DOWN * 0.5)

        mainstream = Text(
            "this is why most modern models use attention",
            font_size=16,
            color=DIM,
        )
        mainstream.next_to(power_label, DOWN, buff=0.4)

        self.play(FadeIn(power_label, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(mainstream, shift=UP * 0.08), run_time=0.5)
        # [14:41] This is why most mainstream models use attention
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 7 — BUT ATTENTION IS NOT MAGIC
        # ================================================================

        but_text = Text("But attention is not magic.", font_size=28, color=WHITE)
        but_text.move_to(ORIGIN)

        self.play(Write(but_text), run_time=0.9)
        # [14:47] But attention is not magic
        self.wait(2.0)

        self.play(
            but_text.animate.scale(0.6).to_edge(UP, buff=0.4).set_color(DIM),
            run_time=0.6,
        )

        # ================================================================
        #  PART 8 — ATTENTION DILUTION: candy metaphor
        # ================================================================

        # Bag of candies
        bag = RoundedRectangle(
            width=1.4,
            height=1.8,
            corner_radius=0.25,
            color=GOLD,
            stroke_width=2,
            fill_color="#1A1500",
            fill_opacity=1,
        )
        bag.move_to(LEFT * 3.0 + DOWN * 0.3)

        bag_label = Text("attention", font_size=14, color=GOLD)
        bag_label.next_to(bag, DOWN, buff=0.2)

        # Candies inside bag
        candies = VGroup()
        candy_positions = [
            UP * 0.3 + LEFT * 0.15,
            UP * 0.3 + RIGHT * 0.2,
            UP * 0.0 + LEFT * 0.1,
            UP * 0.0 + RIGHT * 0.25,
            DOWN * 0.3,
            DOWN * 0.3 + RIGHT * 0.15,
        ]
        for pos in candy_positions:
            candy = Dot(radius=0.08, color=GOLD, fill_opacity=0.7)
            candy.move_to(bag.get_center() + pos)
            candies.add(candy)

        self.play(FadeIn(bag), FadeIn(candies), FadeIn(bag_label), run_time=0.5)
        self.wait(1.0)

        # Few people (short context) — each gets plenty
        few_people = VGroup()
        for i in range(3):
            person = Circle(
                radius=0.2,
                color=WHITE,
                stroke_width=1.5,
                fill_color="#111111",
                fill_opacity=1,
            )
            person.move_to(RIGHT * 0.5 + UP * (0.8 - i * 0.8))
            few_people.add(person)

        few_label = Text("3 tokens", font_size=14, color=WHITE)
        few_label.next_to(few_people, DOWN, buff=0.25)

        # Arrows from bag to people (thick = lots of candy)
        few_arrows = VGroup()
        for p in few_people:
            arr = Arrow(
                bag.get_right(),
                p.get_left(),
                buff=0.1,
                color=GOLD,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.2,
            )
            few_arrows.add(arr)

        self.play(
            FadeIn(few_people),
            FadeIn(few_label),
            LaggedStart(*[GrowArrow(a) for a in few_arrows], lag_ratio=0.1),
            run_time=0.6,
        )

        enough = Text("plenty for everyone", font_size=14, color=GREEN)
        enough.next_to(few_people, RIGHT, buff=0.5)
        self.play(FadeIn(enough), run_time=0.3)
        # [14:56] Attention dilution — too many people for the candies
        self.wait(2.0)

        # Transition to many people
        self.play(
            FadeOut(few_people),
            FadeOut(few_label),
            FadeOut(few_arrows),
            FadeOut(enough),
            run_time=0.4,
        )

        # Many people (long context) — diluted
        many_people = VGroup()
        for i in range(10):
            person = Circle(
                radius=0.13,
                color=WHITE,
                stroke_width=1,
                fill_color="#111111",
                fill_opacity=1,
            )
            row = i // 2
            col = i % 2
            person.move_to(RIGHT * (0.8 + col * 0.5) + UP * (1.5 - row * 0.55))
            many_people.add(person)

        many_label = Text("many tokens", font_size=14, color=WHITE)
        many_label.next_to(many_people, DOWN, buff=0.2)

        # Thin arrows = diluted attention
        many_arrows = VGroup()
        for p in many_people:
            arr = Arrow(
                bag.get_right(),
                p.get_left(),
                buff=0.06,
                color=GOLD,
                stroke_width=0.6,
                stroke_opacity=0.4,
                max_tip_length_to_length_ratio=0.3,
            )
            many_arrows.add(arr)

        self.play(
            FadeIn(many_people),
            FadeIn(many_label),
            LaggedStart(*[GrowArrow(a) for a in many_arrows], lag_ratio=0.02),
            run_time=0.7,
        )

        diluted = Text("attention diluted", font_size=14, color=RED)
        diluted.next_to(many_people, RIGHT, buff=0.4)
        self.play(FadeIn(diluted, scale=1.1), run_time=0.3)
        self.wait(1.0)

        # Highlight the one important person buried in the crowd
        important = many_people[1]
        imp_glow = (
            important.copy().set_stroke(GREEN, width=3).set_fill(GREEN, opacity=0.2)
        )
        imp_label = Text("important!", font_size=11, color=GREEN)
        imp_label.next_to(important, RIGHT, buff=0.15)

        self.play(FadeIn(imp_glow), FadeIn(imp_label), run_time=0.4)
        # [15:12] Important information becomes harder to find
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 9 — SHORT vs LONG CONTEXT ATTENTION HEATMAP
        # ================================================================

        # Short context — sharp attention
        short_heading = Text("short context", font_size=18, color=GREEN)
        short_heading.move_to(UP * 3.0 + LEFT * 3.2)

        short_n = 4
        short_grid = VGroup()
        for r in range(short_n):
            for c in range(short_n):
                # Diagonal and near-diagonal get high attention
                dist = abs(r - c)
                opacity = max(0.8 - dist * 0.25, 0.05)
                # Make one off-diagonal bright (the "important" connection)
                if r == 3 and c == 0:
                    opacity = 0.7
                cell = Square(
                    side_length=0.4,
                    color=GOLD,
                    stroke_width=0.5,
                    fill_color=GOLD,
                    fill_opacity=opacity,
                )
                cell.move_to(
                    LEFT * 3.2
                    + RIGHT * c * 0.42
                    + DOWN * r * 0.42
                    + UP * 1.3
                    + LEFT * 0.6
                )
                short_grid.add(cell)

        short_label = Text("focused attention", font_size=14, color=GREEN)
        short_label.next_to(short_grid, DOWN, buff=0.3)

        # Long context — diluted attention
        long_heading = Text("long context", font_size=18, color=RED)
        long_heading.move_to(UP * 3.0 + RIGHT * 2.8)

        long_n = 8
        long_grid = VGroup()
        for r in range(long_n):
            for c in range(long_n):
                dist = abs(r - c)
                opacity = max(0.3 - dist * 0.03, 0.02)
                # Diagonal still gets some
                if r == c:
                    opacity = 0.35
                cell = Square(
                    side_length=0.25,
                    color=GOLD,
                    stroke_width=0.3,
                    fill_color=GOLD,
                    fill_opacity=opacity,
                )
                cell.move_to(
                    RIGHT * 2.8
                    + RIGHT * c * 0.27
                    + DOWN * r * 0.27
                    + UP * 1.8
                    + LEFT * 0.9
                )
                long_grid.add(cell)

        long_label = Text("diluted attention", font_size=14, color=RED)
        long_label.next_to(long_grid, DOWN, buff=0.3)

        # Divider
        div = Line(UP * 2.5, DOWN * 1.8, color=DIM2, stroke_width=0.8)

        self.play(Write(short_heading), Write(long_heading), Create(div), run_time=0.5)

        self.play(
            LaggedStart(*[FadeIn(c) for c in short_grid], lag_ratio=0.01),
            FadeIn(short_label),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(c) for c in long_grid], lag_ratio=0.005),
            FadeIn(long_label),
            run_time=0.6,
        )
        # [15:15] Short context: focused attention. Long context: diluted attention
        self.wait(8.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 10 — MODEL PERFORMANCE TABLE
        # ================================================================

        tbl_title = Text(
            "retrieval accuracy across context lengths",
            font_size=20,
            color=WHITE,
        )
        tbl_title.to_edge(UP, buff=0.35)
        self.play(Write(tbl_title), run_time=0.6)

        # Table data
        models = [
            ("GPT-4o", "75.9%", "76.7%", "+0.8%", GREEN),
            ("Claude 3.5 Sonnet", "74.8%", "70.6%", "-4.2%", RED),
            ("GPT-4o mini", "66.2%", "64.3%", "-1.9%", RED),
            ("Gemini 1.5 Pro", "59.5%", "62.2%", "+2.7%", GREEN),
            ("Llama 3.1 405B", "59.4%", "42.6%", "-16.8%", RED),
            ("Llama 3.1 70B", "46.9%", "35.3%", "-11.6%", RED),
        ]

        # Column headers
        headers = ["Model", "32K tokens", "125K tokens", "Drop-off"]
        header_x = [-3.2, -0.7, 1.2, 3.2]
        header_mobs = VGroup()

        for i, (h, x) in enumerate(zip(headers, header_x)):
            hm = Text(h, font_size=14, color=ACCENT, weight=BOLD)
            hm.move_to(RIGHT * x + UP * 2.0)
            header_mobs.add(hm)

        # Header line
        h_line = Line(
            LEFT * 4.5 + UP * 1.75,
            RIGHT * 4.5 + UP * 1.75,
            color=DIM,
            stroke_width=1,
        )

        self.play(
            FadeIn(header_mobs),
            Create(h_line),
            run_time=0.4,
        )

        # Table rows
        row_mobs = VGroup()
        for ri, (name, s32, s125, drop, drop_color) in enumerate(models):
            y = 1.3 - ri * 0.5

            nm = Text(name, font_size=13, color=WHITE)
            nm.move_to(RIGHT * header_x[0] + UP * y)

            v32 = Text(s32, font_size=13, color=DIM)
            v32.move_to(RIGHT * header_x[1] + UP * y)

            v125 = Text(s125, font_size=13, color=DIM)
            v125.move_to(RIGHT * header_x[2] + UP * y)

            vd = Text(drop, font_size=13, color=drop_color, weight=BOLD)
            vd.move_to(RIGHT * header_x[3] + UP * y)

            row = VGroup(nm, v32, v125, vd)
            row_mobs.add(row)

        # Animate rows one by one
        for row in row_mobs:
            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.35)

        # [15:28] Model performance across context lengths
        self.wait(2.0)

        # Highlight the worst drop-offs
        worst_box = SurroundingRectangle(
            VGroup(row_mobs[4][3], row_mobs[5][3]),
            color=RED,
            buff=0.1,
            corner_radius=0.06,
            stroke_width=1.5,
            fill_color=RED,
            fill_opacity=0.05,
        )
        self.play(Create(worst_box), run_time=0.4)

        drop_note = Text(
            "larger context ≠ better performance",
            font_size=16,
            color=RED,
        )
        drop_note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(drop_note, shift=UP * 0.1), run_time=0.5)
        # [15:50] Larger context ≠ better performance
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ================================================================
        #  PART 11 — TWO CHALLENGES: n² cost + retrieval quality
        # ================================================================

        challenges_title = Text("two challenges remain", font_size=24, color=WHITE)
        challenges_title.to_edge(UP, buff=0.5)
        self.play(Write(challenges_title), run_time=0.6)

        # Divider
        ch_div = Line(UP * 1.8, DOWN * 1.5, color=DIM2, stroke_width=0.8)
        self.play(Create(ch_div), run_time=0.3)

        # ── LEFT: Computational cost n² ──
        cost_label = Text("computational cost", font_size=18, color=RED)
        cost_label.move_to(LEFT * 3.2 + UP * 1.8)

        # Visualize O(n²): grid that grows
        # Small grid (short context)
        small_n = 3
        small_cost_grid = VGroup()
        for r in range(small_n):
            for c in range(small_n):
                cell = Square(
                    side_length=0.3,
                    color=ACCENT,
                    stroke_width=0.8,
                    fill_color=ACCENT,
                    fill_opacity=0.3,
                )
                cell.move_to(LEFT * 4.0 + RIGHT * c * 0.32 + DOWN * r * 0.32 + UP * 0.5)
                small_cost_grid.add(cell)

        small_n_label = MathTex(r"n=3", font_size=18, color=ACCENT)
        small_n_label.next_to(small_cost_grid, DOWN, buff=0.2)
        small_ops = MathTex(r"9 \text{ ops}", font_size=14, color=DIM)
        small_ops.next_to(small_n_label, DOWN, buff=0.1)

        # Large grid (long context)
        large_n = 6
        large_cost_grid = VGroup()
        for r in range(large_n):
            for c in range(large_n):
                cell = Square(
                    side_length=0.2,
                    color=RED,
                    stroke_width=0.5,
                    fill_color=RED,
                    fill_opacity=0.2,
                )
                cell.move_to(LEFT * 2.0 + RIGHT * c * 0.22 + DOWN * r * 0.22 + UP * 0.7)
                large_cost_grid.add(cell)

        large_n_label = MathTex(r"n=6", font_size=18, color=RED)
        large_n_label.next_to(large_cost_grid, DOWN, buff=0.2)
        large_ops = MathTex(r"36 \text{ ops}", font_size=14, color=RED)
        large_ops.next_to(large_n_label, DOWN, buff=0.1)

        # Formula
        n2_formula = MathTex(r"\mathcal{O}(n^2)", font_size=30, color=RED)
        n2_formula.move_to(LEFT * 3.0 + DOWN * 1.5)

        self.play(Write(cost_label), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(c) for c in small_cost_grid], lag_ratio=0.02),
            FadeIn(small_n_label),
            FadeIn(small_ops),
            run_time=0.5,
        )
        self.play(
            LaggedStart(*[FadeIn(c) for c in large_cost_grid], lag_ratio=0.01),
            FadeIn(large_n_label),
            FadeIn(large_ops),
            run_time=0.5,
        )
        self.play(Write(n2_formula), run_time=0.5)
        self.wait(1.0)

        # ── RIGHT: Retrieval quality ──
        ret_label = Text("retrieval quality", font_size=18, color=GOLD)
        ret_label.move_to(RIGHT * 3.2 + UP * 1.8)

        # Needle in haystack visual
        hay_tokens = VGroup()
        for i in range(35):
            row = i // 7
            col = i % 7
            dot = Dot(
                radius=0.06,
                color=DIM2,
                fill_opacity=0.3,
            )
            dot.move_to(RIGHT * 2.0 + RIGHT * col * 0.35 + DOWN * row * 0.3 + UP * 0.8)
            hay_tokens.add(dot)

        # One needle (the important token)
        needle_idx = 17  # middle-ish
        hay_tokens[needle_idx].set_color(GOLD)
        hay_tokens[needle_idx].set_fill(GOLD, opacity=0.9)

        needle_label = Text("needle", font_size=11, color=GOLD)
        needle_label.next_to(hay_tokens[needle_idx], RIGHT, buff=0.15)

        hay_label = Text("haystack of tokens", font_size=14, color=DIM)
        hay_label.next_to(hay_tokens, DOWN, buff=0.3)

        q_text = Text("can the model find it?", font_size=14, color=GOLD)
        q_text.next_to(hay_label, DOWN, buff=0.2)

        self.play(Write(ret_label), run_time=0.4)
        self.play(
            FadeIn(hay_tokens),
            FadeIn(hay_label),
            run_time=0.5,
        )
        self.play(
            FadeIn(needle_label),
            Flash(
                hay_tokens[needle_idx].get_center(),
                color=GOLD,
                flash_radius=0.2,
                num_lines=6,
            ),
            run_time=0.4,
        )
        self.play(FadeIn(q_text, shift=UP * 0.08), run_time=0.4)
        self.wait(3.0)

        # Final summary box
        summary = Text(
            "stronger context, but not unlimited",
            font_size=18,
            color=WHITE,
        )
        summary.to_edge(DOWN, buff=0.4)

        sum_box = SurroundingRectangle(
            summary,
            color=SEPIA,
            buff=0.2,
            corner_radius=0.12,
            fill_color=SEPIA_DARK,
            fill_opacity=1,
            stroke_width=1.5,
        )

        self.play(Create(sum_box), run_time=0.4)
        self.play(Write(summary), run_time=0.7)
        self.play(
            Flash(
                sum_box, color=SEPIA, flash_radius=0.4, line_length=0.12, num_lines=8
            ),
            run_time=0.5,
        )
        # Stronger context but not unlimited — two challenges: n² cost + retrieval quality
        self.wait(3.0)

        # Final fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
