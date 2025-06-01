from core.system_state import pulse
from owl.visual_inspector import run_visual
import shutil

def owl_visual_reflex(tick):
    avg = pulse.get_average()
    zone = pulse.classify()
    entropy_zone = "low" if avg < 0.3 else "medium" if avg < 0.7 else "high"

    # Reflex logic
    if zone == "🔴 surge":
        run_visual("tracer_trail_animator")
        run_visual("entropy_cluster_plot")

    if tick % 50 == 0:
        run_visual("mood_pressure_timeseries")

    if tick % 100 == 0:
        run_visual("signature_grid_animator")

    if entropy_zone == "high":
        run_visual("entropy_arc_animator")

def archive_owl_visuals(tick):
    src = "juliet_flowers/cluster_report"
    dst = f"owl/archives/tick_{tick}"
    os.makedirs(dst, exist_ok=True)

    for file in os.listdir(src):
        if file.endswith(".png") or file.endswith(".gif"):
            shutil.copy(os.path.join(src, file), os.path.join(dst, file))

    print(f"[Owl] 🗂️ Archived visuals to {dst}")

