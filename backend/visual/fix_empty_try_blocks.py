#!/usr/bin/env python3
"""
Remove all empty try blocks from visualizer scripts (i.e., 'try:' immediately followed by 'except' or 'finally').
"""
import os
import glob
import re

def remove_empty_try_blocks():
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
        changed = False
        while i < len(lines):
            line = lines[i]
            # Look for a try: line
            m = re.match(r'^(\s*)try:\s*$', line)
            if m and i + 1 < len(lines):
                next_line = lines[i+1]
                # If next line is except/finally at same indent, skip the try: line
                if re.match(rf'^{m.group(1)}(except|finally)\b', next_line):
                    # skip this try: line
                    changed = True
                    i += 1
                    continue
            new_lines.append(line)
            i += 1
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Patched: {file_path}")
            patched_files.append(file_path)
    print(f"\nPatched {len(patched_files)} files.")

if __name__ == "__main__":
    remove_empty_try_blocks() 