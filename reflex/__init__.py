"""
DAWN Reflex System Package

This package contains the reflex components for the DAWN consciousness system:
- ReflexExecutor: Command execution and system control
- SymbolicNotation: Emoji/codex translation system  
- OwlPanel: Commentary and observation interface
- FractalColorizer: Mood-color mapping and visualization
"""

from ...reflex_executor import ReflexExecutor
from ...symbolic_notation import SymbolicNotation, NotationMode
from ...owl_panel import OwlPanel, OwlCommentType, OwlEntry
from ...fractal_colorizer import FractalColorizer, ColorSpace

__version__ = "1.0.0"
__author__ = "DAWN Consciousness System"

__all__ = [
    'ReflexExecutor',
    'SymbolicNotation', 
    'NotationMode',
    'OwlPanel',
    'OwlCommentType',
    'OwlEntry', 
    'FractalColorizer',
    'ColorSpace'
] 