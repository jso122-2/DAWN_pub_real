# /Tick_engine/launch_visual_suite.py

import os

# Visual Reflex Components
from mycelium.heat_overlay import render_heat_overlay
from mycelium.mood_drift import render_mood_drift_map
from mycelium.animate_trails import animate_nutrient_trails
from mycelium.mycelium_nutrient_map import generate_nutrient_map as render_nutrient_map


from owl.owl_entropy_plot import render_entropy_chart
from field_entropy_map import render_entropy_field
from codex.sigil_memory_ring import get_active_sigil_entropy_list

# Optional fallback stubs if some modules aren't ready
def safe_call(name, func):
    try:
        print(f"[VisualSuite] 🟢 Launching: {name}")
        func()
    except Exception as e:
        print(f"[VisualSuite] ⚠️ Failed to launch {name}: {e}")

def launch_all_reflexes():
    """
    Launch all visual reflex tools used during DAWN's live execution.
    Includes heatmaps, entropy charts, drift fields, sigil trails, and overlays.
    """

    print("[VisualSuite] 🎬 Launching full visual reflex suite...")

    # Nutrient + Field Visuals
    safe_call("Nutrient Field Overlay", render_nutrient_map)
    safe_call("Mycelium Trail Animation", animate_nutrient_trails)
    safe_call("Nutrient Field Overlay", generate_nutrient_map)

    # Heat + Drift Mapping
    safe_call("Heat Overlay", render_heat_overlay)
    safe_call("Mood Drift Map", render_mood_drift_map)  # ✅

    # Entropy Visuals
    safe_call("Entropy Chart", render_entropy_chart)
    safe_call("Field Entropy Map", render_entropy_field)

    # Sigil Summary
    try:
        entropy_list = get_active_sigil_entropy_list()
        avg_entropy = sum(entropy_list) / len(entropy_list) if entropy_list else 0.0
        print(f"[VisualSuite] 🔮 Avg Sigil Entropy: {avg_entropy:.3f}")
    except Exception as e:
        print(f"[VisualSuite] ⚠️ Sigil entropy fetch failed: {e}")

    print("[VisualSuite] ✅ All available visualizations dispatched.")

