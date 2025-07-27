#!/usr/bin/env python3
"""
Patch all visualizer scripts to add a generic except block after any try: that is missing an except or finally.
"""
import os
import glob
import re

def patch_try_blocks():
    visualizer_dirs = ["backend/visual", "visual"]
    visualizer_files = []
    for dir_path in visualizer_dirs:
        if os.path.exists(dir_path):
            visualizer_files.extend(glob.glob(f"{dir_path}/*.py"))
    print(f"Found {len(visualizer_files)} visualizer files")
    patched_files = []
    for file_path in visualizer_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            # Look for a try: line
            if re.match(r'\s*try:\s*$', line):
                # Look ahead to see if next non-empty, non-comment line is except/finally
                j = i + 1
                while j < len(lines) and (lines[j].strip() == '' or lines[j].strip().startswith('#')):
                    j += 1
                if j >= len(lines) or not re.match(r'\s*(except|finally)\b', lines[j]):
                    # Insert a generic except block at the same indentation as try
                    indent = re.match(r'(\s*)try:', line).group(1)
                    new_lines.append(f"{indent}except Exception as e:\n{indent}    print(f'Error: {{e}}', file=sys.stderr)\n")
                    patched_files.append(file_path)
            i += 1
        if new_lines != lines:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Patched: {file_path}")
    print(f"\nPatched {len(set(patched_files))} files.")

if __name__ == "__main__":
    patch_try_blocks() 