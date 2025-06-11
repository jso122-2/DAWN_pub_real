import os
from pathlib import Path

def create_tree(directory, prefix="", is_last=True, max_depth=3, current_depth=0):
    """Generate a tree structure of directories and files."""
    if current_depth >= max_depth:
        return ""
    
    tree_str = ""
    path = Path(directory)
    
    # Skip these directories
    skip_dirs = {'__pycache__', '.git', 'venv', 'node_modules'}
    
    # Get all items, filter and sort
    items = [item for item in path.iterdir() if item.name not in skip_dirs]
    items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        
        # Create the tree branch
        if current_depth > 0:
            tree_str += prefix
            tree_str += "└── " if is_last_item else "├── "
        
        # Add the item name
        if item.is_dir():
            tree_str += f"📁 {item.name}/\n"
            # Recurse into subdirectories
            extension = "    " if is_last_item else "│   "
            new_prefix = prefix + extension if current_depth > 0 else ""
            tree_str += create_tree(item, new_prefix, is_last_item, max_depth, current_depth + 1)
        else:
            ext = item.suffix.lower()
            icon = "🐍" if ext == ".py" else "📄" if ext in [".json", ".yaml", ".yml"] else "📝"
            tree_str += f"{icon} {item.name}\n"
    
    return tree_str

# Run
header = "🌲 DAWN Tick Engine Directory Structure 🌲\n" + "=" * 50 + "\n"
tree = create_tree(".", max_depth=3)

# Summary
dirs = [d for d in Path(".").iterdir() if d.is_dir() and not d.name.startswith('.')]
files = [f for f in Path(".").iterdir() if f.is_file() and not f.name.startswith('.')]
summary = (
    "\n📊 Summary:\n"
    f"Total directories: {len(dirs)}\n"
    f"Total root files: {len(files)}\n"
    f"\nCore modules: {[d.name for d in dirs if d.name in ['core', 'processors', 'network', 'reflection', 'schema', 'semantic']]}\n"
)

# Combine and save to file
output_path = Path("directory_tree.txt")
output_path.write_text(header + tree + summary, encoding="utf-8")

# Also print to terminal
print(header)
print(tree)
print(summary)
print(f"\n📁 Output saved to: {output_path.resolve()}")
