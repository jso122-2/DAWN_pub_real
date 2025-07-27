#!/usr/bin/env python3
"""
Comprehensive fix for all visualizer syntax issues
"""
import os
import glob
import re

def fix_syntax_issues():
    visualizer_dirs = ["backend/visual", "visual"]
    visualizer_files = []
    for dir_path in visualizer_dirs:
        if os.path.exists(dir_path):
            visualizer_files.extend(glob.glob(f"{dir_path}/*.py"))
    
    print(f"Found {len(visualizer_files)} visualizer files")
    patched_files = []
    
    for file_path in visualizer_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Remove orphaned except statements (except without try)
            # Look for except statements that don't have a preceding try at same indentation
            lines = content.split('\n')
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Check if this is an except statement
                except_match = re.match(r'^(\s*)(except\b.*)$', line)
                if except_match:
                    indent = except_match.group(1)
                    # Look backwards for a try statement at same indentation
                    found_try = False
                    for j in range(i-1, max(-1, i-10), -1):  # Look back up to 10 lines
                        if j < 0:
                            break
                        prev_line = lines[j].strip()
                        if prev_line == '' or prev_line.startswith('#'):
                            continue
                        if re.match(rf'^{re.escape(indent)}try\s*:', lines[j]):
                            found_try = True
                            break
                        if re.match(rf'^{re.escape(indent)}\w', lines[j]):  # Different indentation level
                            break
                    
                    if not found_try:
                        # This is an orphaned except, remove it
                        print(f"  Removing orphaned except in {file_path}: {line.strip()}")
                        i += 1
                        continue
                
                new_lines.append(line)
                i += 1
            
            content = '\n'.join(new_lines)
            
            # Fix 2: Remove empty try blocks (try: immediately followed by except)
            lines = content.split('\n')
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Check if this is a try: line
                try_match = re.match(r'^(\s*)try:\s*$', line)
                if try_match and i + 1 < len(lines):
                    next_line = lines[i+1]
                    # If next line is except/finally at same indent, skip the try: line
                    if re.match(rf'^{try_match.group(1)}(except|finally)\b', next_line):
                        print(f"  Removing empty try block in {file_path}")
                        i += 1
                        continue
                
                new_lines.append(line)
                i += 1
            
            content = '\n'.join(new_lines)
            
            # Fix 3: Remove duplicate function definitions
            # This is a simple approach - remove consecutive identical function definitions
            lines = content.split('\n')
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Check if this is a function definition
                func_match = re.match(r'^(\s*)def\s+(\w+)\s*\(', line)
                if func_match:
                    func_name = func_match.group(2)
                    # Look ahead to see if there's another function with same name
                    for j in range(i+1, min(len(lines), i+50)):
                        next_func_match = re.match(r'^(\s*)def\s+(\w+)\s*\(', lines[j])
                        if next_func_match and next_func_match.group(2) == func_name:
                            print(f"  Removing duplicate function {func_name} in {file_path}")
                            # Skip until we find the end of the first function
                            while i < len(lines) and (lines[i].strip() == '' or 
                                   not re.match(r'^(\s*)def\s+', lines[i]) or
                                   lines[i].startswith(' ' * (len(func_match.group(1)) + 1))):
                                i += 1
                            break
                
                if i < len(lines):
                    new_lines.append(lines[i])
                i += 1
            
            content = '\n'.join(new_lines)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                patched_files.append(file_path)
                print(f"Fixed: {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nFixed {len(patched_files)} files:")
    for file_path in patched_files:
        print(f"  - {file_path}")

if __name__ == "__main__":
    fix_syntax_issues() 