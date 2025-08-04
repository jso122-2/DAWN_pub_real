"""
KAN-Cairrn Adapters Module

Adapter components for integrating KAN-Cairrn with external systems.
"""

from ...claude_kan import ClaudeKANAdapter
from ...weave_kan import WeaveKANAdapter
from ...memory_kan import MemoryKANAdapter

__all__ = [
    'ClaudeKANAdapter',
    'WeaveKANAdapter', 
    'MemoryKANAdapter'
] 