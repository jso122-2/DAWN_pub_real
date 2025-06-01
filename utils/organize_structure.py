import os
import shutil
from datetime import datetime

def organize_juliet_memory():
    base = "juliet_flowers/"
    for bloom in os.listdir(base):
        path = os.path.join(base, bloom)
        if os.path.isdir(path):
            # Load mood tag
            try:
                with open(os.path.join(path, "metadata.json"), "r") as f:
                    mood = json.load(f).get("mood_tag", "unknown")
                new_path = os.path.join(base, bloom, mood)
                os.makedirs(new_path, exist_ok=True)
                for file in os.listdir(path):
                    if file != mood:
                        shutil.move(os.path.join(path, file), new_path)
            except:
                continue

def organize_mycelium_logs():
    src = "mycelium_logs/"
    for f in os.listdir(src):
        if f.endswith(".json") or f.endswith(".csv"):
            day = f.split("T")[0]
            dst = os.path.join(src, day)
            os.makedirs(dst, exist_ok=True)
            shutil.move(os.path.join(src, f), os.path.join(dst, f))

def create_export_dir():
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("visual_exports", today)
    os.makedirs(path, exist_ok=True)
    print(f"[FS] ✅ Export path ready: {path}")

if __name__ == "__main__":
    organize_juliet_memory()
    organize_mycelium_logs()
    create_export_dir()
