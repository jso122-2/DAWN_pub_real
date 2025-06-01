import os
from PIL import Image
from datetime import datetime
from pathlib import Path

# CONFIG
SIGNATURE_DIR = "juliet_flowers/fractal_signatures"
OUTPUT_PATH = "juliet_flowers/cluster_report/signature_field.gif"
GRID_SIZE = (3, 2)  # cols, rows
DURATION = 300  # milliseconds per frame

def load_images_sorted_by_time(folder):
    images = list(Path(folder).glob("*.png"))
    return sorted(images, key=lambda p: p.stat().st_mtime)

def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def build_grid(frames, grid_size):
    cols, rows = grid_size
    cell_w, cell_h = frames[0].size
    grid_img = Image.new("RGB", (cell_w * cols, cell_h * rows), color=(0, 0, 0))

    for idx, img in enumerate(frames):
        if idx >= cols * rows:
            break
        x = (idx % cols) * cell_w
        y = (idx // cols) * cell_h
        grid_img.paste(img, (x, y))
    return grid_img

def animate_signature_grid():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    images = load_images_sorted_by_time(SIGNATURE_DIR)

    grid_frames = []
    for frame_set in chunked(images, GRID_SIZE[0] * GRID_SIZE[1]):
        loaded = [Image.open(str(p)) for p in frame_set]
        grid = build_grid(loaded, GRID_SIZE)
        grid_frames.append(grid)

    if grid_frames:
        grid_frames[0].save(OUTPUT_PATH, save_all=True, append_images=grid_frames[1:],
                            duration=DURATION, loop=0)
        print(f"✅ Animated signature grid saved to: {OUTPUT_PATH}")
    else:
        print("❌ No signature images found.")

if __name__ == "__main__":
    animate_signature_grid()
