import os
import shutil
from pathlib import Path

def refactor_substrate():
    """Refactor DAWN substrate layer"""
    
    # Create directories
    dirs = [
        "substrate",
        "substrate/genesis",
        "substrate/helix",
        "substrate/consciousness",
        "archive/abandoned/terminals_empty_20250604"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")
    
    # Move operations
    moves = [
        ("terminals", "archive/abandoned/terminals_empty_20250604/terminals"),
        ("helix/helix_bridge.py", "substrate/helix/bridge.py"),
        ("helix_import_architecture.py", "substrate/helix/import_architecture.py"),
        ("meta/dawn_meta_consciousness.py", "substrate/consciousness/meta_consciousness.py")
    ]
    
    # Move genome files
    genome_path = Path("genome")
    if genome_path.exists():
        for py_file in genome_path.glob("*.py"):
            dest = Path("substrate/genesis") / py_file.name
            shutil.move(str(py_file), str(dest))
            print(f"Moved: {py_file} -> {dest}")
    
    # Move other files
    for src, dst in moves:
        if Path(src).exists():
            shutil.move(src, dst)
            print(f"Moved: {src} -> {dst}")
    
    # Create __init__.py files
    init_files = [
        "substrate/__init__.py",
        "substrate/genesis/__init__.py",
        "substrate/helix/__init__.py",
        "substrate/consciousness/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"Created: {init_file}")