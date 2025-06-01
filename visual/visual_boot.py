# visual/visual_boot.py

"""
🎬 DAWN Visual Snapshot Launcher
Run this after DAWN has processed several hundred ticks.

Triggers a curated subset of the visual suite to capture:
- Pulse Field
- Drift / Entropy
- Rebloom Lineage
- Mood / Belief Maps
- Sigil Emissions
- Mycelium Growth

All outputs go to: juliet_flowers/cluster_report/ or visuals/
"""

# --- Import visual modules ---
from pulse_field_animator import animate_pulse_field
from pulse_zone_timeline import visualize_zone_timeline
from drift_entropy_animator import animate_drift_entropy
from rebloom_lineage_animator import animate_rebloom_lineage
from nutrient_field_animator import animate_root_density_over_time
from mood_pressure_timeseries import animate_mood_pressure
from sigil_emission_timeline import animate_sigil_timeline
from entropy_overlay_gradient import render_entropy_gradient
from sealing_dashboard import render_sealing_snapshot

# --- Run Sequence ---
def run_visual_sweep():
    print("🧠 Starting DAWN Visual Snapshot Sequence...\n")
    
    try:
        animate_pulse_field()
    except Exception as e:
        print(f"[pulse_field_animator] ❌ {e}")

    try:
        visualize_zone_timeline()
    except Exception as e:
        print(f"[pulse_zone_timeline] ❌ {e}")

    try:
        animate_drift_entropy()
    except Exception as e:
        print(f"[drift_entropy_animator] ❌ {e}")

    try:
        animate_rebloom_lineage()
    except Exception as e:
        print(f"[rebloom_lineage_animator] ❌ {e}")

    try:
        animate_root_density_over_time()
    except Exception as e:
        print(f"[nutrient_field_animator] ❌ {e}")

    try:
        animate_mood_pressure()
    except Exception as e:
        print(f"[mood_pressure_timeseries] ❌ {e}")

    try:
        animate_sigil_timeline()
    except Exception as e:
        print(f"[sigil_emission_timeline] ❌ {e}")

    try:
        render_entropy_gradient()
    except Exception as e:
        print(f"[entropy_overlay_gradient] ❌ {e}")

    try:
        render_sealing_snapshot()
    except Exception as e:
        print(f"[sealing_dashboard] ❌ {e}")

    print("\n✅ DAWN Visual Sweep Complete.\nAll visuals saved to 'visuals/' or 'cluster_report/'.")


if __name__ == "__main__":
    run_visual_sweep()
