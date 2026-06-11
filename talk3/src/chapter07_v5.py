from v5_common import *


class Chapter07V5(V5BaseScene):
    chapter = 7
    beats = [
        {"title": "System integration forces the question of task essence.", "kind": "handoff", "left": "errand system", "right": "essence?", "equation": "what\\;is\\;preserved?"},
        {"title": "LfO historically moved from copying motion to extracting purpose.", "kind": "pipeline", "steps": ["mimic motion", "observe task", "extract purpose", "LfO"], "accent": ACCENT_BLUE, "result_color": ACCENT_AMBER},
        {"title": "The essence cannot be the observed trajectory.", "kind": "compare", "left": "trajectory", "right": "intended relation", "bad": True},
        {"title": "Top-down LfO starts from the task outcome.", "kind": "pipeline", "steps": ["desired outcome", "state relation", "primitive action", "parameters"], "accent": ACCENT_AMBER, "result_color": ACCENT_GREEN},
        {"title": "Recognition identifies the objects and relations that define state.", "kind": "gates", "left": "object recognition", "right": "task recognition", "outcome": "state fields"},
        {"title": "The key abstraction is a state transition.", "kind": "equation", "equation": "T:s_t\\rightarrow s_{t+1}", "left": "before state", "right": "after state"},
        {"title": "The next chapter asks how state changes across domains.", "kind": "handoff", "left": "T:s_t\\rightarrow s_{t+1}", "right": "domain-state atlas", "equation": "T\\in\\mathcal{S}_{domain}"},
    ]

