import importlib
import os

VISUAL_ROOT = "visual"

def get_visual_modules():
    files = os.listdir(VISUAL_ROOT)
    return {
        f.replace(".py", ""): f"{VISUAL_ROOT}.{f.replace('.py', '')}"
        for f in files if f.endswith(".py") and not f.startswith("__")
    }

def run_visual(name: str):
    try:
        modules = get_visual_modules()
        if name not in modules:
            print(f"[Owl] ❌ Visual '{name}' not found.")
            return
        mod = importlib.import_module(modules[name])
        for fn in ["main", "render", "animate"]:
            if hasattr(mod, fn):
                getattr(mod, fn)()
                print(f"[Owl] ✅ Executed {fn}() in {name}")
                return
        print(f"[Owl] ⚠️ No valid entrypoint in {name}")
    except Exception as e:
        print(f"[Owl] ❌ Failed to run {name}: {e}")
