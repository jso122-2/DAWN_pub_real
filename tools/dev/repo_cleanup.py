#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# 1. Define project root
ROOT_DIR = Path(__file__).resolve().parent

# 2. Define directories
DEST = {
    "legacy_tick": ROOT_DIR / "archive" / "legacy_tick",
    "utilities": ROOT_DIR / "archive" / "utilities",
    "tests": ROOT_DIR / "tests",
    "data_config": ROOT_DIR / "data" / "config",
    "data_bloom": ROOT_DIR / "data" / "bloom",
    "data_visuals": ROOT_DIR / "data" / "visuals",
    "data_text": ROOT_DIR / "data" / "text",
}

# 3. Create missing folders
for d in DEST.values():
    d.mkdir(parents=True, exist_ok=True)

# 4. Rule definitions
legacy_tick_files = {
    "minimal_tick.py", "tick_loop.py", "tick_engine.py",
    "tick_engine_integration.py", "tick_engine_config.json", "tick_state.json"
}
test_prefixes = ("test", "fix_and_test_visuals")
utility_exts = (".bak",)
utility_names = ("copy", "check_imports", "explicit_cleanup", "finalize_imports_enhanced", "scan_flat_imports")
visual_exts = (".png",)
text_exts = (".txt",)
bloom_keywords = ("bloom", "registry")
config_keywords = ("config.json",)

# 5. File move logic
def move(src: Path, target: Path):
    target_path = target / src.name
    if not target_path.exists():
        shutil.move(str(src), str(target_path))
        print(f"Moved: {src} → {target_path}")

# 6. File crawler + sorter
for file in ROOT_DIR.rglob("*"):
    if not file.is_file():
        continue
    name = file.name

    if name in legacy_tick_files:
        move(file, DEST["legacy_tick"])
    elif name.endswith(utility_exts) or name.startswith(utility_names):
        move(file, DEST["utilities"])
    elif name.startswith(test_prefixes):
        move(file, DEST["tests"])
    elif name.endswith(".json") and any(k in name for k in bloom_keywords):
        move(file, DEST["data_bloom"])
    elif name.endswith(".json") and any(k in name for k in config_keywords):
        move(file, DEST["data_config"])
    elif name.endswith(visual_exts):
        move(file, DEST["data_visuals"])
    elif name.endswith(text_exts):
        move(file, DEST["data_text"])

# 7. Auto-add __init__.py in all folders
for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    path = Path(dirpath)
    if "__init__.py" not in filenames:
        init_path = path / "__init__.py"
        try:
            init_path.touch()
            print(f"Created: {init_path}")
        except Exception:
            continue
