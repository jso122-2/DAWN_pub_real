# Perform automatic rewrite of JulietFlower imports across all modules

import os

os.makedirs("diagnostics", exist_ok=True)
log_path = "diagnostics/julietflower_imports_patched.txt"


def rewrite_imports_for_julietflower(root_dir, import_line="from core.system_state import JulietFlower"):
    patched_files = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(".py"):
                continue
            full_path = os.path.join(subdir, file)

            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            uses_juliet = any("JulietFlower(" in line for line in lines)
            already_imported = any("JulietFlower" in line and "import" in line for line in lines)

            if uses_juliet and not already_imported:
                # Insert the import after any __future__ or built-in imports
                new_lines = []
                inserted = False
                for line in lines:
                    new_lines.append(line)
                    if not inserted and (line.startswith("import") or line.startswith("from")):
                        continue
                    if not inserted:
                        new_lines.append(import_line + "\n")
                        inserted = True
                with open(full_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                patched_files.append(full_path)

    return patched_files

# Execute the rewrite
patched = rewrite_imports_for_julietflower(".")

# Write a confirmation report
log_path = "diagnostics/julietflower_imports_patched.txt"
with open(log_path, "w") as f:
    for path in patched:
        f.write(f"✅ Patched: {path}\n")

log_path
