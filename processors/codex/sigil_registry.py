# sigil_registry.py

SIGIL_CLASSES = {
    "/|-|": {"class": "pressure", "reflex_threshold": 0.5},
    "🜂": {"class": "urgency", "reflex_threshold": 0.3},
    "⟁": {"class": "disruption", "reflex_threshold": 0.2},
    "⌘": {"class": "stabilization", "reflex_threshold": 0.4},
    "☍": {"class": "contradiction", "reflex_threshold": 0.4},
    "🝕": {"class": "memory", "reflex_threshold": 0.3},
    "↻": {"class": "loop", "reflex_threshold": 0.2},
    "⚡": {"class": "activation", "reflex_threshold": 0.5}
}
