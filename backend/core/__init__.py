"""
Core modules for the DAWN system.
"""

from ...pattern_detector import create_pattern_detector
from ...state_machine import create_state_machine
from ...fractal_emotions import create_fractal_emotions
from ...memory_manager import create_memory_manager
from ...mood_gradient import create_mood_gradient_plotter

__all__ = [
    'create_pattern_detector',
    'create_state_machine',
    'create_fractal_emotions',
    'create_memory_manager',
    'create_mood_gradient_plotter'
] 