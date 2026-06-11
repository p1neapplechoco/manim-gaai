from v5_common import *


class Chapter06V5(V5BaseScene):
    chapter = 6
    beats = [
        {"title": "The errand robot tests whether the modules work together.", "kind": "pipeline", "steps": ["grasp", "manipulate", "semantic check", "errand robot"], "accent": ACCENT_PURPLE, "result_color": ACCENT_GREEN},
        {"title": "An errand is a sequence of grounded task models.", "kind": "chips", "heading": "grounded task-model sequence", "chips": ["M1 pick", "M2 bring", "M3 place", "M4 open", "M5 close"], "accent": ACCENT_AMBER},
        {"title": "The humanoid body makes execution hardware-specific.", "kind": "compare", "left": "shared task model", "right": "local humanoid control"},
        {"title": "Recognition supplies objects, relations, and task cues.", "kind": "pipeline", "steps": ["vision", "objects", "relations", "task cues"], "accent": ACCENT_BLUE, "result_color": ACCENT_AMBER},
        {"title": "Skill agents turn each task model into local action.", "kind": "pipeline", "steps": ["task model", "skill agent", "feedback", "robot action"], "accent": ACCENT_AMBER, "result_color": ACCENT_GREEN},
        {"title": "System integration exposes the representation bottleneck.", "kind": "gates", "left": "recognition", "right": "task model", "outcome": "execution"},
        {"title": "The next chapter asks what task essence really means.", "kind": "handoff", "left": "errand system map", "right": "essence?", "equation": "?=T"},
    ]

