
import json
import os
from PIL import Image, ImageDraw, ImageFont

BLOOM_DIR = "juliet_flowers/bloom_metadata"
FRACTAL_DIR = "juliet_flowers/fractal_signatures"
OUTPUT = "juliet_flowers/cluster_report/mood_heat_overlay.gif"
LOG_PATH = "mycelium_logs/nutrient_log.json"

def get_heat(depth):
    if not os.path.exists(LOG_PATH):
        return 0.0
    with open(LOG_PATH, "r") as f:
        data = json.load(f)
    return min(1.0, data.get(str(depth), 0) / 10.0)

def mood_color(mood):
    return {
        "joyful": (255, 215, 0),
        "focused": (34, 139, 34),
        "reflective": (70, 130, 180),
        "anxious": (255, 69, 0),
        "sad": (105, 105, 105)
    }.get(mood, (200, 200, 200))

def overlay_mood_heat():
    files = sorted(os.listdir(BLOOM_DIR))
    frames = []

    for fname in files:
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
            seed_id = bloom["seed_id"]
            mood = bloom.get("mood", "unknown")
            depth = bloom.get("lineage_depth", 0)
            heat = get_heat(depth)

            # Find corresponding fractal
            fractals = [f for f in os.listdir(FRACTAL_DIR) if seed_id in f]
            if not fractals:
                continue

            img_path = os.path.join(FRACTAL_DIR, sorted(fractals)[-1])
            img = Image.open(img_path).convert("RGBA")
            overlay = Image.new("RGBA", img.size, mood_color(mood) + (int(100 * heat),))
            img = Image.alpha_composite(img, overlay)

            # Label with mood + heat
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            draw.rectangle([0, 0, 260, 20], fill=(0, 0, 0, 180))
            draw.text((5, 5), f"{seed_id} | Mood: {mood} | Heat: {heat:.2f}", font=font, fill=(255, 255, 255))

            frames.append(img)

    if frames:
        frames[0].save(
            OUTPUT,
            save_all=True,
            append_images=frames[1:],
            duration=800,
            loop=0
        )
        print(f"[Overlay] 🧪 Mood+Heat overlay saved → {OUTPUT}")
    else:
        print("[Overlay] ❌ No frames generated.")
