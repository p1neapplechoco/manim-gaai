from v5_common import *


class Chapter02V5(V5BaseScene):
    chapter = 2
    beats = [
        {"title": "A primitive action must change a meaningful contact state.", "kind": "handoff", "left": "M = (what, where)", "right": "state change?", "equation": "s_t\\rightarrow s_{t+1}"},
        {"title": "Face contact represents what motion is constrained.", "kind": "blocks", "relation": "face contact"},
        {"title": "Kuhn-Tucker constraints separate possible states from impossible ones.", "kind": "sphere", "equation": "A x \\leq b", "note": "feasible contact directions"},
        {"title": "Seven contact classes create forty-nine candidate transitions.", "kind": "matrix", "rows": 7, "cols": 7, "label": "49 candidate transitions"},
        {"title": "Physics reduces the graph to twenty executable transitions.", "kind": "graph", "caption": "20 physically possible transitions", "highlight": [0, 2, 4]},
        {"title": "Observed tasks concentrate on a smaller frequent subset.", "kind": "chips", "heading": "6 frequent transitions", "chips": ["Bring", "Pick", "Place", "Drawer adjust", "Drawer open", "Drawer close"], "accent": ACCENT_AMBER},
        {"title": "Physical manipulation agents are named edges in the filtered graph.", "kind": "chips", "heading": "physical manipulation agents", "chips": ["Bring", "Pick", "Place", "Insert", "Door open", "Door close"], "accent": ACCENT_PURPLE},
        {"title": "The next layer asks whether a physical edge makes semantic sense.", "kind": "gates", "left": "physical", "right": "semantic?", "outcome": "Chapter 03 gate"},
    ]

