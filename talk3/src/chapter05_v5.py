from v5_common import *


class Chapter05V5(V5BaseScene):
    chapter = 5
    beats = [
        {"title": "Grasping is a skill family, not one hand pose.", "kind": "compare", "left": "fixed hand pose", "right": "grasp agent family", "bad": True},
        {"title": "Taxonomy names grasp styles, but task purpose selects useful ones.", "kind": "pipeline", "steps": ["taxonomy", "task purpose", "closure goal", "agent"], "accent": ACCENT_BLUE, "result_color": ACCENT_AMBER},
        {"title": "Closure turns grasp purpose into a testable condition.", "kind": "equation", "equation": "\\mathrm{closure}\\Rightarrow stable", "left": "disturbance", "right": "held object"},
        {"title": "Three prepared grasp agents cover distinct closure strategies.", "kind": "chips", "heading": "prepared grasp agents", "chips": ["power", "precision", "contact-web"], "accent": ACCENT_PURPLE},
        {"title": "Contact-web agents make grasp structure explicit.", "kind": "graph", "labels": ["F1", "F2", "F3", "O", "C1", "C2", "C3"], "caption": "finger-object contact web", "highlight": [0, 1, 2]},
        {"title": "Superquadrics provide a compact shape representation.", "kind": "domains", "panels": ["box-like", "cylinder-like", "rounded", "shape params"]},
        {"title": "CNN and RL training connect perceived shape to grasp action.", "kind": "pipeline", "steps": ["image", "CNN", "shape params", "RL policy", "grasp"], "accent": ACCENT_BLUE, "result_color": ACCENT_GREEN},
        {"title": "One grasp agent can handle many object shapes.", "kind": "chips", "heading": "same agent, varied objects", "chips": ["cup", "box", "bottle", "tool", "bowl", "handle"], "accent": ACCENT_GREEN},
        {"title": "Force strategy becomes part of the agent interface.", "kind": "handoff", "left": "grasp agent", "right": "errand system", "equation": "\\{passive, active\\}"},
    ]

