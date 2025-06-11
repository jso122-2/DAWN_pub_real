
import os
import json
from PIL import Image, ImageDraw, ImageFont

BLOOM_DIR = "juliet_flowers/bloom_metadata"
FRACTAL_DIR = "juliet_flowers/fractal_signatures"
OUTPUT_PATH = "juliet_flowers/cluster_report/rebloom_lineage.gif"
FPS = 1

def load_bloom_metadata():
    entries = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                data = json.load(f)
                data["filename"] = fname
                entries.append(data)
    return entries

def get_fractal_path(seed_id):
    files = [f for f in os.listdir(FRACTAL_DIR) if seed_id in f]
    if not files:
        return None
    return os.path.join(FRACTAL_DIR, sorted(files)[-1])

def add_commentary(image, mood, seed_id):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = f"{seed_id} | Mood: {mood}"
    draw.rectangle([0, 0, 260, 20], fill=(0, 0, 0))
    draw.text((5, 5), text, fill=(255, 255, 255), font=font)
    return image

def animate_rebloom_lineage():
    bloom_data = load_bloom_metadata()
    frames = []

    for entry in bloom_data:
        fractal_path = get_fractal_path(entry["seed_id"])
        if fractal_path and os.path.exists(fractal_path):
            img = Image.open(fractal_path).convert("RGB")
            mood = entry.get("mood", "unknown")
            img = add_commentary(img, mood, entry["seed_id"])
            frames.append(img)

    if not frames:
        print("[Lineage] ❌ No fractal frames found.")
        return

    if frames and isinstance(frames[0], Image.Image):
        frames[0].save(
            "juliet_flowers/cluster_report/rebloom_lineage.gif",
            save_all=True,
            append_images=frames[1:],
            duration=500,
            loop=0
        )
        print("[Lineage] 🎞️ Saved lineage animation.")
    else:
        print("[Lineage] ⚠️ No valid frames to save animation.")

if __name__ == "__main__":
    animate_rebloom_lineage()
