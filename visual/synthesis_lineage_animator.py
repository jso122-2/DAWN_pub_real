
import os
import json
from PIL import Image, ImageDraw, ImageFont

BLOOM_DIR = "juliet_flowers/bloom_metadata"
FRACTAL_DIR = "juliet_flowers/fractal_signatures"
OUTPUT_PATH = "juliet_flowers/cluster_report/synthesis_lineage.gif"
FPS = 1

def load_synthesis_blooms():
    entries = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json") and "synthesis-" in fname:
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

def annotate(image, mood, seed_id):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = f"{seed_id} | Mood: {mood}"
    draw.rectangle([0, 0, 260, 20], fill=(0, 0, 0))
    draw.text((5, 5), text, fill=(255, 255, 255), font=font)
    return image

def animate_synthesis_lineage():
    synthesis_data = load_synthesis_blooms()
    frames = []

    for entry in synthesis_data:
        fractal_path = get_fractal_path(entry["seed_id"])
        if fractal_path and os.path.exists(fractal_path):
            img = Image.open(fractal_path).convert("RGB")
            mood = entry.get("mood", "unknown")
            img = annotate(img, mood, entry["seed_id"])
            frames.append(img)

    if not frames:
        print("[Lineage] ❌ No synthesis bloom frames found.")
        return

    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),
        loop=0
    )
    print(f"[Lineage] 🎞️ Synthesis lineage saved → {OUTPUT_PATH}")

if __name__ == "__main__":
    animate_synthesis_lineage()
