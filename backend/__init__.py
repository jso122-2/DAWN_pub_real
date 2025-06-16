"""
DAWN Tick Engine Backend Package
==============================

This package contains the backend implementation of the DAWN Tick Engine,
including WebSocket servers, visualizers, and core consciousness components.
"""

__version__ = "1.0.0"
__author__ = "DAWN Research Team"

# Import commonly used components
from backend.core.unified_tick_engine import tick_engine
from backend.websocket_manager import manager as ws_manager
from backend.visual.visual_manager import VisualManager

__all__ = [
    'tick_engine',
    'ws_manager',
    'VisualManager',
]

import os
import sys
from pathlib import Path

# Add the root directory to Python path
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 