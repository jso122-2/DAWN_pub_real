"""
DAWN Bloom System - Fractal Memory Architecture
Manages cognitive blooms, lineage tracking, and semantic evolution
"""

# Core bloom manager exports
from ...bloom_manager import (
    Bloom,
    BloomManager, 
    RebloomEvent,
    create_bloom_manager,
    integrate_with_codex
)

# Existing bloom system exports (maintain compatibility)
try:
    from ...bloom_engine import BloomEngine
    from ...bloom_spawner import BloomSpawner
    from ...unified_bloom_engine import UnifiedBloomEngine
    from ...bloom_memory_system import BloomMemorySystem
    from ...juliet_flower import JulietFlower
except ImportError:
    # Handle missing modules gracefully
    pass

# Version and metadata
__version__ = "2.0.0"
__author__ = "DAWN Cognitive Architecture"

# Main exports for easy import
__all__ = [
    'Bloom',
    'BloomManager',
    'RebloomEvent', 
    'create_bloom_manager',
    'integrate_with_codex',
    'BloomEngine',
    'BloomSpawner',
    'UnifiedBloomEngine',
    'BloomMemorySystem',
    'JulietFlower'
]
