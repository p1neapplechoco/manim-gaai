from v5_common import *


class Chapter09V5(V5BaseScene):
    chapter = 9
    beats = [
        {"title": "Imitation replays execution; LfO preserves task equivalence.", "kind": "compare", "left": "path replay", "right": "state equivalence", "bad": True},
        {"title": "Symbolic teleoperation separates encoding from decoding.", "kind": "pipeline", "steps": ["observation", "GPT/VLM encoder", "M=(what,where)", "skill decoder"], "accent": ACCENT_BLUE, "result_color": ACCENT_AMBER},
        {"title": "High-level intent and local reaction belong on different sides.", "kind": "spectrum", "labels": ["gesture", "navigation", "manipulation", "locomotion"]},
        {"title": "Vision can encode intent because force is handled during execution.", "kind": "gates", "left": "vision intent", "right": "local force", "outcome": "execution"},
        {"title": "Piaget's analogy frames skills as internalized action schemas.", "kind": "pipeline", "steps": ["observe", "schema", "practice", "adapt"], "accent": ACCENT_BLUE, "result_color": ACCENT_GREEN},
        {"title": "Transfer succeeds only when representation, grounding, and skill coverage align.", "kind": "equation", "equation": "Transfer\\Leftrightarrow R\\wedge G\\wedge K", "left": "conditions", "right": "transfer"},
        {"title": "The full architecture is observation, task model, skill agents, and robot feedback.", "kind": "pipeline", "steps": ["observation", "task model", "skill agents", "feedback", "robot"], "accent": ACCENT_BLUE, "result_color": ACCENT_GREEN},
        {"title": "Generalist behavior factorizes invariants from adaptation.", "kind": "equation", "equation": "invariants\\;\\oplus\\;adaptation", "left": "task state", "right": "robot control"},
    ]

