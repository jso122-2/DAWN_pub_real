
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
                    lines = f.readlines()

                modified = False
                new_lines = []

                for line in lines:
                    original_line = line
                    for mod, bucket in BUCKET_MAP.items():
                        if re.match(rf"\s*from {mod} import", line):
                            line = line.replace(f"from {mod} import", f"from {bucket}.{mod} import")
                            modified = True
                        elif re.match(rf"\s*import {mod}\b", line):
                            line = line.replace(f"import {mod}", f"import {bucket}.{mod}")
                            modified = True
                    new_lines.append(line)

                if modified:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    changes.append(path)

    return changes

if __name__ == "__main__":
    changed = rewrite_imports()
    print(f"✅ Updated {len(changed)} files.")
    for c in changed:
        print(f" - {c}")
