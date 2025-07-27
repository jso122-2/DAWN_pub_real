"""
Test script to verify imports
"""

import sys
from pathlib import Path

# Add the root directory to sys.path
root_dir = str(Path(__file__).parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

print("Python path:", sys.path)

try:
    from core.consciousness_core import ConsciousnessCore
    print("Successfully imported ConsciousnessCore")
except ImportError as e:
    print(f"Failed to import ConsciousnessCore: {e}")
    print("Current directory:", Path.cwd())
    print("Root directory:", root_dir)
    print("Core directory exists:", (Path(root_dir) / "core").exists())
    print("consciousness_core.py exists:", (Path(root_dir) / "core" / "consciousness_core.py").exists()) 