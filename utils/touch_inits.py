import os

ROOT = "."  # ← updated
subdirs = ["core", "bloom", "fractal", "owl", "mycelium", "scripts", "router"]

def touch_init(folder):
    path = os.path.join(ROOT, folder, "__init__.py")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("# init")
        print(f"✅ Created {path}")
    else:
        print(f"✔️ Already exists: {path}")

# Root __init__.py
root_init = os.path.join(ROOT, "__init__.py")
if not os.path.exists(root_init):
    with open(root_init, "w", encoding="utf-8") as f:
        f.write("# root init")
    print(f"✅ Created {root_init}")
else:
    print(f"✔️ Already exists: {root_init}")

# Subdirs
for sd in subdirs:
    touch_init(sd)
