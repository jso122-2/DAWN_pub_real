import os
import re

DAWN_ROOT = "./"  # Path to your repo
TARGET_MODULE = "pulse_heat"
HELIX_IMPORT_LINE = f"{TARGET_MODULE} = helix_import(\"{TARGET_MODULE}\")"
HELIX_HEADER = "from helix_import_architecture import helix_import\n"

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    has_helix = any("helix_import" in line for line in lines)
    rewritten = False
    new_lines = []

    for line in lines:
        if re.search(rf"(import|from).*{TARGET_MODULE}", line):
            # Skip the old import
            rewritten = True
            continue
        new_lines.append(line)

    if rewritten:
        # Insert helix import at the top
        if not has_helix:
            new_lines.insert(0, HELIX_HEADER)
        new_lines.insert(1, HELIX_IMPORT_LINE + "\n")

        backup_path = path + ".bak"
        os.rename(path, backup_path)

        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"[✔] Rewired: {path}")
        return True

    return False

# Walk repo and process
count = 0
for root, dirs, files in os.walk(DAWN_ROOT):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            if process_file(full_path):
                count += 1

print(f"✅ Rewired {count} files for helix_import('{TARGET_MODULE}')")
