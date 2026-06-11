from v5_common import *


class Chapter03V5(V5BaseScene):
    chapter = 3
    beats = [
        {"title": "A physical transition can still be the wrong action.", "kind": "compare", "left": "physical edge", "right": "task-valid edge", "bad": True},
        {"title": "Tool-environment common sense is a task constraint.", "kind": "pipeline", "steps": ["tool role", "object role", "surface role", "meaning"], "accent": ACCENT_BLUE, "result_color": ACCENT_AMBER},
        {"title": "Physical constraints decide what can move.", "kind": "gates", "left": "contact", "right": "reachable", "outcome": "can move"},
        {"title": "Semantic constraints decide what should move.", "kind": "gates", "left": "physical", "right": "semantic", "outcome": "should move"},
        {"title": "Semantic manipulation agents encode these role constraints.", "kind": "chips", "heading": "semantic agents", "chips": ["pour", "stir", "use tool", "serve", "contain", "clean"], "accent": ACCENT_PURPLE},
        {"title": "The current library is a coverage map, not a complete world model.", "kind": "matrix", "rows": 4, "cols": 6, "label": "known cells + explicit gaps"},
        {"title": "The next problem is learning controllers for valid transitions.", "kind": "handoff", "left": "physical + semantic", "right": "trainable policy target", "equation": "\\pi_k(x,g,\\theta)"},
    ]

