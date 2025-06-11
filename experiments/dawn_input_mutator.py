
import os
import re

# Define your bucket mapping
BUCKET_MAP = {
    "tick_engine": "core",
    "event_bus": "core",
    "pulse_heat": "core",
    "pulse_thresholds": "core",
    "main_loop": "core",
    "bloom_engine": "bloom",
    "bloom_event": "bloom",
    "bloom_writer": "bloom",
    "juliet_flower": "bloom",
    "juliet_cluster": "bloom",
    "juliet_utils": "bloom",
    "juliet_inspector": "bloom",
    "router": "router",
    "tracer_core": "router",
    "tracer_listener": "router",
    "owl_auditor": "owl",
    "owl_entropy_audit": "owl",
    "trust_model": "owl",
    "mycelium_layer": "mycelium",
    "mycelium_nutrient_map": "mycelium",
    "mycelium_animation": "mycelium",
    "fractal_generator": "fractal",
    "generate_julia_set": "fractal",
    "fractal_field_map": "fractal",
    "bloom_visualizer": "fractal",
    "field_report": "fractal"
}

def mutate_imports(root_dir):
    changes = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(subdir, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    updated_lines = []
                    modified = False

                    for line in lines:
                        for mod, bucket in BUCKET_MAP.items():
                            if re.match(rf"\s*from {mod} import", line):
                                line = line.replace(f"from {mod} import", f"from {bucket}.{mod} import")
                                modified = True
                            elif re.match(rf"\s*import {mod}\b", line):
                                line = line.replace(f"import {mod}", f"import {bucket}.{mod}")
                                modified = True
                        updated_lines.append(line)

                    if modified:
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.writelines(updated_lines)
                        changes.append(full_path)

                except Exception as e:
                    print(f"⚠️ Error in {full_path}: {e}")

    return changes

if __name__ == "__main__":
    root = input("Enter root directory of DAWN project (e.g. Tick_engine): ").strip()
    if os.path.exists(root):
        affected = mutate_imports(root)
        if affected:
            print(f"✅ Updated {len(affected)} files.")
            for file in affected:
                print(f" - {file}")
        else:
            print("No changes made.")
    else:
        print("❌ Invalid directory.")
