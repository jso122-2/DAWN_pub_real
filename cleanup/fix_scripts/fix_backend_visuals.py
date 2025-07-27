#!/usr/bin/env python3
"""
Comprehensive fix script for backend visual files
Removes orphaned error print statements and fixes indentation issues
"""

import os
import re
import glob

def fix_file(filepath):
    """Fix a single file by removing orphaned error prints and fixing indentation"""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove orphaned error print statements
    content = re.sub(r'^\s*print\(f\'Error: \{e\}\', file=sys\.stderr\)\s*$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines that might have been left
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Fix any remaining orphaned except blocks
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # If we find an orphaned except statement, remove it
        if re.match(r'^\s*except\s+Exception\s+as\s+e:\s*$', line):
            # Check if the previous line is not a try statement
            if i > 0 and not re.search(r'^\s*try\s*:\s*$', lines[i-1]):
                print(f"  Removing orphaned except at line {i+1}")
                i += 1
                continue
        
        # If we find an orphaned except statement without proper structure
        if re.match(r'^\s*except\s*:\s*$', line):
            # Check if the previous line is not a try statement
            if i > 0 and not re.search(r'^\s*try\s*:\s*$', lines[i-1]):
                print(f"  Removing orphaned except at line {i+1}")
                i += 1
                continue
        
        fixed_lines.append(line)
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Write the fixed content back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Fixed {filepath}")

def main():
    """Main function to fix all backend visual files"""
    backend_visual_dir = "backend/visual"
    
    if not os.path.exists(backend_visual_dir):
        print(f"Directory {backend_visual_dir} not found!")
        return
    
    # Find all Python files in backend/visual
    python_files = glob.glob(os.path.join(backend_visual_dir, "*.py"))
    
    print(f"Found {len(python_files)} Python files in {backend_visual_dir}")
    
    for filepath in python_files:
        try:
            fix_file(filepath)
        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
    
    print("\nFixing complete! Testing syntax...")
    
    # Test syntax of all files
    for filepath in python_files:
        try:
            import py_compile
            py_compile.compile(filepath, doraise=True)
            print(f"✓ {os.path.basename(filepath)} - Syntax OK")
        except Exception as e:
            print(f"✗ {os.path.basename(filepath)} - Syntax Error: {e}")

if __name__ == "__main__":
    main() 