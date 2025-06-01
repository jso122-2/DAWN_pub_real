
import os
from PIL import Image

def optimize_fractal_images(root_dir="juliet_flowers", quality=85):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".png"):
                path = os.path.join(subdir, file)
                try:
                    img = Image.open(path).convert("RGB")
                    img.save(path, optimize=True, quality=quality)
                    print(f"🗜️ Compressed: {path}")
                except Exception as e:
                    print(f"⚠️ Failed to process {path}: {e}")

if __name__ == "__main__":
    optimize_fractal_images()
