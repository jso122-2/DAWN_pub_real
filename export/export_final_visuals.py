import shutil
from datetime import datetime

EXPORTS = [
    "nutrient_growth.gif",
    "rebloom_trails.gif",
    "field_entropy_drift.png"
]

def export_visuals():
    today = datetime.now().strftime("%Y-%m-%d")
    dst = f"visual_exports/{today}/"
    os.makedirs(dst, exist_ok=True)

    for file in EXPORTS:
        shutil.copy(file, dst)
        print(f"[EXPORT] ✅ Moved {file} → {dst}")

if __name__ == "__main__":
    export_visuals()
