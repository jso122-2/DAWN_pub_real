# /core/emotional_override.py
"""
Trigger schema-level overrides based on pulse zone.
- Calm: No override.
- Active: Allow mild drift expansion.
- Surge: Force bloom reroute, suppress high-entropy trails.
"""

def apply_emotional_override(pulse_zone, active_bloom):
    if pulse_zone == "🔴 surge":
        active_bloom.override_flags["reroute"] = True
        active_bloom.override_flags["suppress_entropy"] = True
        return "⚠️ Surge override applied"
    elif pulse_zone == "🟡 active":
        active_bloom.override_flags["drift_softening"] = True
        return "🌗 Drift softened"
    return "🟢 No override"
