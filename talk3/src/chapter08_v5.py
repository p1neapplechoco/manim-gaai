from v5_common import *


class Chapter08V5(V5BaseScene):
    chapter = 8
    beats = [
        {"title": "A state transition needs a domain-specific state space.", "kind": "handoff", "left": "T:s_t -> s_{t+1}", "right": "choose state space", "equation": "\\mathcal{S}_{domain}"},
        {"title": "Polyhedral manipulation uses face contact as state.", "kind": "blocks", "relation": "face-contact state"},
        {"title": "Machine assembly uses part mating as state.", "kind": "domains", "panels": ["peg", "hole", "aligned", "mated"]},
        {"title": "Knot tying uses topology as state.", "kind": "domains", "panels": ["loop", "crossing", "topology", "knot state"]},
        {"title": "Dance uses key pose and foot contact as state.", "kind": "domains", "panels": ["key pose", "left foot", "right foot", "sequence"]},
        {"title": "Different representations ignore different irrelevant variations.", "kind": "compare", "left": "appearance variation", "right": "state variables", "bad": True},
        {"title": "The shared principle is task-relevant state change.", "kind": "domains", "panels": ["contact", "mating", "topology", "key pose"]},
    ]

