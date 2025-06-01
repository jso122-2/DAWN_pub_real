import json
from owl_visual_core import get_visual_output_folder, plot_drift_consistency, plot_stale_rates


from owl_visual_core import (
    get_visual_output_folder,
    plot_drift_consistency,
    plot_stale_rates,
    plot_loop_moods  # ← ensure this is also defined
)

def render_all_owl_visuals(log_path="C:/Users/Admin/OneDrive/Desktop/DAWN/Tick_engine/owl/owl_log.json"):
    with open(log_path, "r", encoding="utf-8") as f:
        owl_data = json.load(f)
    out_dir = get_visual_output_folder()
    plot_drift_consistency(owl_data, out_dir)
    plot_stale_rates(owl_data, out_dir)
    print(f"✅ Owl visuals saved to: {out_dir}")




if __name__ == "__main__":
    render_all_owl_visuals()
