import os
import shutil
from datetime import datetime

EXPORTS_DIR = "exports"
ASSETS = {
    "nutrient_growth.gif": "visuals/nutrient_growth.gif",
    "rebloom_trails.gif": "visuals/rebloom_trail_animation.gif",
    "field_entropy_drift.png": "visuals/field_entropy_drift.png"
}

def export_visual_artifacts():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_path = os.path.join(EXPORTS_DIR, f"run_{timestamp}")
    os.makedirs(export_path, exist_ok=True)

    print(f"[Exporter] 🗂 Saving artifacts to: {export_path}")

    for label, source in ASSETS.items():
        if os.path.exists(source):
            target = os.path.join(export_path, label)
            shutil.copy(source, target)
            print(f"[Exporter] ✅ {label} → exported")
        else:
            print(f"[Exporter] ⚠️ Missing: {label} (not generated yet)")

    generate_manifest(export_path)

def generate_manifest(folder):
    manifest_path = os.path.join(folder, "export_manifest.txt")
    with open(manifest_path, "w") as f:
        f.write(f"Export Timestamp: {datetime.now().isoformat()}\n")
        f.write("Files:\n")
        for file in os.listdir(folder):
            f.write(f"  - {file}\n")
    print(f"[Exporter] 📝 Manifest created → {manifest_path}")

if __name__ == "__main__":
    export_visual_artifacts()
