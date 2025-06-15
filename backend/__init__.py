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