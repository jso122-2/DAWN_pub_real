"""
DAWN Core Package
===============
Core system components including wiring monitor and diagnostics.
"""

import sys
from pathlib import Path

# Add the project root to sys.path if not already there
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Re-export the main core package
from core import * 