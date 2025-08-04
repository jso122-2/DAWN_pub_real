#!/usr/bin/env python3
"""
DAWN Repository Structure Display

This script shows the cleaned up repository structure after organization.
"""

import os
from pathlib import Path

def show_structure(root_dir: str = ".", max_depth: int = 3):
    """Display the repository structure"""
    root_path = Path(root_dir)
    
    print("🌅 DAWN Repository Structure")
    print("=" * 50)
    print(f"📁 Root: {root_path.absolute()}")
    print()
    
    def print_tree(path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return
            
        # Get all items in directory
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            return
            
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            next_prefix = "    " if is_last else "│   "
            
            # Skip certain directories/files
            if item.name in ['.git', '__pycache__', '.vscode', '.cursor']:
                continue
                
            # Display item
            if item.is_dir():
                print(f"{prefix}{current_prefix}📁 {item.name}/")
                if depth < max_depth:
                    print_tree(item, prefix + next_prefix, depth + 1)
            else:
                # Show file with size
                try:
                    size = item.stat().st_size
                    size_str = f"({size:,} bytes)" if size > 0 else "(empty)"
                    print(f"{prefix}{current_prefix}📄 {item.name} {size_str}")
                except:
                    print(f"{prefix}{current_prefix}📄 {item.name}")
    
    print_tree(root_path)
    
    # Show summary statistics
    print("\n📊 Repository Statistics:")
    
    python_files = list(root_path.rglob("*.py"))
    directories = [d for d in root_path.iterdir() if d.is_dir() and d.name not in ['.git', '__pycache__', '.vscode', '.cursor']]
    
    print(f"   📁 Directories: {len(directories)}")
    print(f"   📄 Python files: {len(python_files)}")
    
    # Show main entry points
    print("\n🚀 Main Entry Points:")
    main_files = ['main.py', 'launcher_scripts/launch_dawn_unified.py']
    for main_file in main_files:
        if (root_path / main_file).exists():
            print(f"   ✅ {main_file}")
        else:
            print(f"   ❌ {main_file} (missing)")
    
    # Show key directories
    print("\n📂 Key Directories:")
    key_dirs = [
        'core', 'conversation', 'visual', 'tests', 'demos', 
        'launcher_scripts', 'config', 'runtime', 'logs', 'docs'
    ]
    for key_dir in key_dirs:
        if (root_path / key_dir).exists():
            print(f"   ✅ {key_dir}/")
        else:
            print(f"   ❌ {key_dir}/ (missing)")

def main():
    """Main function"""
    show_structure()
    
    print("\n🎉 Repository cleanup verification complete!")
    print("\n💡 To test the system:")
    print("   python main.py --help")

if __name__ == "__main__":
    main() 