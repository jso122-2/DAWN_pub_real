"""
KAN-Cairrn Interfaces Module

Interface components for exposing KAN-Cairrn functionality through various APIs.
"""

from .spline_api import SplineAPIServer
from .visual_kan import KANVisualizationSocket
from .cursor_stream import CursorStreamHandler

__all__ = [
    'SplineAPIServer',
    'KANVisualizationSocket',
    'CursorStreamHandler'
] 