# /cortex/semantic_autopsy.py

import os
import json
import shutil
from datetime import datetime
from PIL import Image, ImageDraw

SUPPRESSION_LOG = "logs/suppression_log.csv"
ARCHIVE_ROOT = "archive/suppressed_blooms/"
os.makedirs(os.path.dirname(SUPPRESSION_LOG), exist_ok=True)
os.makedirs(ARCHIVE_ROOT, exist_ok=True)

# 📊 Log suppressed bloom metadata
def log_suppression_event(bloom, reasons):
    with open(SUPPRESSION_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()},"
                f"{bloom.get('seed_id')},"
                f"{'|'.join(reasons)},"
                f"{bloom.get('entropy_score')},"
                f"{bloom.get('trust_score')},"
                f"{bloom.get('lineage_depth')},"
                f"{bloom.get('mood')}\n")


# 🗃️ Move suppressed bloom files to indexed archive folders
def archive_suppressed_bloom(metadata_path, image_path, seed_id, reasons):
    for reason in reasons:
        dir_path = os.path.join(ARCHIVE_ROOT, reason)
        os.makedirs(dir_path, exist_ok=True)
        if os.path.exists(metadata_path):
            shutil.copy(metadata_path, os.path.join(dir_path, f"{seed_id}.json"))
        if os.path.exists(image_path):
            shutil.copy(image_path, os.path.join(dir_path, f"{seed_id}.png"))


# 🔥 Burnt bloom variant for suppressed visuals
def generate_burnt_bloom_visual(image_path):
    if not os.path.exists(image_path):
        return None

    img = Image.open(image_path).convert("RGB")
    overlay = Image.new("RGB", img.size, (40, 0, 0))  # dark red burn
    burnt = Image.blend(img, overlay, alpha=0.75)

    # Optional: draw sigil X across center
    draw = ImageDraw.Draw(burnt)
    w, h = burnt.size
    draw.line((0, 0, w, h), fill=(255, 0, 0), width=3)
    draw.line((0, h, w, 0), fill=(255, 0, 0), width=3)

    burnt_path = image_path.replace(".png", "_burnt.png")
    burnt.save(burnt_path)
    return burnt_path


# 📈 Optional summary (stubbed for expansion)
def suppression_summary_report():
    print("[Autopsy] 📊 Suppression summary report not yet implemented.")
    # Later: aggregate suppression counts, reasons, mood correlations, entropy histograms
