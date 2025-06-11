#!/usr/bin/env python3
"""
Migrate Legacy Scripts
Moves all dawn_*.py scripts from tools/scripts/ to experiments/
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_legacy_scripts():
    """Move legacy dawn scripts to experiments folder"""
    
    # Create experiments directory
    experiments_dir = Path("experiments")
    experiments_dir.mkdir(exist_ok=True)
    logger.info(f"Created {experiments_dir} directory")
    
    # Patterns to move
    patterns = [
        "tools/scripts/dawn_*.py",
        "main_*.py",
        "dawn_*.py",  # But not dawn.py (our new entry)
    ]
    
    moved_count = 0
    
    # Find and move scripts
    for pattern in patterns:
        for script_path in Path(".").glob(pattern):
            # Skip our new dawn.py
            if script_path.name == "dawn.py" and script_path.parent == Path("."):
                logger.info(f"Skipping new entry point: {script_path}")
                continue
                
            # Move to experiments
            dest_path = experiments_dir / script_path.name
            
            try:
                shutil.move(str(script_path), str(dest_path))
                logger.info(f"Moved {script_path} -> {dest_path}")
                moved_count += 1
            except Exception as e:
                logger.error(f"Failed to move {script_path}: {e}")
                
    # Also create a README in experiments
    readme_content = """# DAWN Experiments

This directory contains experimental scripts and legacy entry points that have been superseded by the main dawn.py entry point.

## Legacy Scripts

These scripts were used during DAWN's development but are no longer the primary entry points:

- `dawn_consciousness.py` - Early consciousness experiments
- `dawn_engine.py` - Original engine implementation
- `dawn_helix_interface.py` - Helix integration experiments
- `main_*.py` - Various main entry attempts

## Usage

These scripts are preserved for reference and experimentation. The main DAWN system should be run via:

```bash
python dawn.py
```

For experimental features, you can still run individual scripts:

```bash
python experiments/dawn_consciousness.py
```
"""
    
    readme_path = experiments_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    logger.info(f"Created {readme_path}")
    
    logger.info(f"Migration complete! Moved {moved_count} scripts to {experiments_dir}")
    
    # Create __init__.py files where needed
    init_files = [
        "core/__init__.py",
        "core/system/__init__.py",
        "experiments/__init__.py",
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        init_path.parent.mkdir(parents=True, exist_ok=True)
        if not init_path.exists():
            init_path.touch()
            logger.info(f"Created {init_path}")

if __name__ == "__main__":
    migrate_legacy_scripts()