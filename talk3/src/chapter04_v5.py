from v5_common import *


class Chapter04V5(V5BaseScene):
    chapter = 4
    beats = [
        {"title": "A valid transition still needs a controller.", "kind": "handoff", "left": "valid transition", "right": "controller?", "equation": "s_t\\rightarrow s_{t+1}"},
        {"title": "RL trains a policy to realize the transition under feedback.", "kind": "loop", "nodes": ["state", "action", "reward", "update"], "center": "RL policy"},
        {"title": "Contact dimensions describe what is maintained, detached, or constrained.", "kind": "pipeline", "steps": ["maintain", "detach", "constraint", "dimension state"], "accent": ACCENT_BLUE, "result_color": ACCENT_AMBER},
        {"title": "Direction geometry turns dimensions into control choices.", "kind": "sphere", "equation": "\\mathcal{D}_{adm}", "note": "admissible directions"},
        {"title": "Dimension transitions provide reusable control laws.", "kind": "equation", "equation": "D_i\\rightarrow D_j\\Rightarrow u_k", "left": "dimension change", "right": "control law"},
        {"title": "Place and insert are examples of the same transition-to-policy decoding.", "kind": "chips", "heading": "transition-to-policy examples", "chips": ["Place", "Insert", "axis", "goal", "contact", "feedback"], "accent": ACCENT_PURPLE},
        {"title": "Drawer, door, and wipe agents differ in dynamics but share feedback execution.", "kind": "loop", "nodes": ["vision", "force", "state", "action"], "center": "skill agent"},
        {"title": "The next chapter asks how grasping generalizes across object shape.", "kind": "handoff", "left": "policy surface", "right": "grasp agent interface", "equation": "g(o)\\rightarrow a"},
    ]

