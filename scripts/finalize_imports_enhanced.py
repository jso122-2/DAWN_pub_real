
import os
import re

BUCKET_MAP = {
    "tick_engine": "core",
    "event_bus": "core",
    "pulse_heat": "core",
    "pulse_thresholds": "core",
    "tick_listener": "core",
    "tick_emitter": "core",
    "tick_loop": "core",
    "system_state": "core",
    "bloom_event": "bloom",
    "bloom_engine": "bloom",
    "bloom_writer": "bloom",
    "bloom_memory": "bloom",
    "juliet_flower": "bloom",
    "juliet_cluster": "bloom",
    "juliet_utils": "bloom",
    "juliet_inspector": "bloom",
    "memory_utils": "bloom",
    "tracer_core": "router",
    "tracer_listener": "router",
    "router": "router",
    "mycelium_layer": "mycelium",
    "nutrient_logger": "mycelium",
    "owl_auditor": "owl",
    "trust_model": "owl",
    "fractal_generator": "fractal",
    "generate_julia_set": "fractal",
    "fractal_boost": "fractal"
}

def rewrite_imports(root_dir="Tick_engine"):
    changes = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content
                for mod, bucket in BUCKET_MAP.items():
                    pattern1 = rf"(\bfrom\s+){mod}(\s+import\b)"
                    content = re.sub(pattern1, rf"\1{bucket}.{mod}\2", content)

                    pattern2 = rf"(\bimport\s+){mod}\b"
                    content = re.sub(pattern2, rf"\1{bucket}.{mod}", content)

                if content != original_content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    changes.append(path)

    return changes

if __name__ == "__main__":
    updated = rewrite_imports()
    print(f"✅ Updated {len(updated)} files.")
    for path in updated:
        print(f" - {path}")
