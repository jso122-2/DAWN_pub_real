"""
DAWN Unified SCUP System
========================
Semantic Coherence Under Pressure - The heart of schema stability
Consolidates: scup.py, scup_engine.py, scup_loop.py, scup_recovery.py
Generated: 2025-06-04 21:29
"""

from .scup_math import (
    SCUPInputs, SCUPOutputs, compute_basic_scup, compute_enhanced_scup,
    compute_recovery_scup, compute_legacy_scup, classify_zone
)
from .scup_tracker import SCUPTracker, compute_scup, calculate_SCUP, log_scup

# Re-export everything for backward compatibility
__all__ = [
    'SCUPInputs',
    'SCUPOutputs',
    'compute_basic_scup',
    'compute_enhanced_scup',
    'compute_recovery_scup',
    'compute_legacy_scup',
    'classify_zone',
    'SCUPTracker',
    'compute_scup',
    'calculate_SCUP',
    'log_scup'
]
