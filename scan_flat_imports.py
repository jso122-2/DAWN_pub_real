
import os
import re

# Known buckets
BUCKETS = ["core", "bloom", "fractal", "owl", "router", "scripts", "mycelium"]

def is_flat_import(line):
    # Ignore comments
    if line.strip().startswith("#"):
        return False
    # Flat import patterns
    return (
        re.match(r"^\s*from\s+[a-zA-Z_]+\s+import", line)
        or re.match(r"^\s*import\s+[a-zA-Z_]+", line)
    )

def scan_for_flat_imports(root_dir="Tick_engine"):
    results = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        if is_flat_import(line):
                            if not any(f"{b}." in line for b in BUCKETS):
                                results.append(f"{path}:{i}: {line.strip()}")

    return results

if __name__ == "__main__":
    issues = scan_for_flat_imports()
    if issues:
        print("⚠️ Flat (non-bucketed) imports found:")
        for issue in issues:
            print(" -", issue)
    else:
        print("✅ No flat imports found. All clean.")
