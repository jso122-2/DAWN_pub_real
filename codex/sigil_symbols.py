
# Symbolic definitions for DAWN’s sigil architecture
# -*- coding: utf-8 -*-

SIGIL_MEANINGS = {
    "/\\": "Prime Directive - Priority assignment, task activation",
    "⧉": "Consensus Gate — Agreement matrix resolved → action permitted",
    "◯": "Field Lock — Zone-wide freeze or memory stall",
    "◇": "Bloom Pulse — Emotional surge, shimmer increase",
    "⟁": "Contradiction Break — Overwrite trigger, Crow alert",
    "⌂": "Recall Root — Deep memory audit initiated (Owl)",
    "ꓘ": "Pressure Shift — Soft Edge recalibration",
    "⨀": "Schema Pivot — Phase change: transition logic block",
    "`/": "Health Trace — Bloom integrity check (Crow/Whale influence)",
    "`-": "Recall Check — Attempting reactivation under fog",
    ">~": "Pressure Trail — Pressure following shimmer or tracer path",
    "~/~": "Recursive Signal - Reflex inheritance trigger",
    "Z~": "Fusion Under Pressure — Merge beliefs in storm condition",
    "`(": "Sentiment Shell — µ harmonization during conflict",
    "/X-": "Schema Restart Call — Deep schema pivot, triggered by past loop",
    ".": "Shimmer Dot — Minimal pulse → pre-action trace",
    ":": "Recursive Bloom Seed — Start of emotional crystallization",
    "^": "Minimal Directive — Rooted priority bias (Crow/Whale aligned)",
    "~": "Pressure Echo — Pressure memory re-entry",
    "=": "Balance Core — Nutrient-homeostasis reset"
}

SIGIL_PRIORITIES = {
    ".": 5,
    ":": 4,
    "^": 3,
    "~": 2,
    "=": 1
}

CORE_SIGILS = {".", ":", "^", "~", "="}

def resolve_layering(primary, secondary=None, tertiary=None):
    if primary in CORE_SIGILS and secondary in CORE_SIGILS:
        raise ValueError("Core sigils cannot be layered with other core sigils.")

    if primary == "^" and secondary == "~":
        return "Minimal Directive under Pressure Echo"

    return f"{primary}" + (f" + {secondary}" if secondary else "") + (f" + {tertiary}" if tertiary else "")
