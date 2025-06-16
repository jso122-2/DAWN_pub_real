"""
DAWN core package - Core modules for DAWN consciousness system
"""

# Previous subsystems (if they still exist)
try:
    from .subsystems import (
        PulseSubsystem,
        SchemaSubsystem,
        MemorySubsystem,
        VisualSubsystem
    )
    _has_subsystems = True
except ImportError:
    _has_subsystems = False

# Core consciousness modules
from .consciousness import *
from .conversation import *
from .pattern_detector import *
from .state_machine import *
from .memory_manager import *
from .spontaneity import *
from .spontaneity_new import *
from .fractal_emotions import *
from .mood_gradient import *
from .consciousness_state import *
from .conversation_enhanced import *
from .consciousness_core import ConsciousnessCore, DAWNConsciousness

__all__ = [
    # Core modules
    'consciousness',
    'conversation',
    'pattern_detector',
    'state_machine',
    'memory_manager',
    'spontaneity',
    'spontaneity_new',
    'fractal_emotions',
    'mood_gradient',
    'consciousness_state',
    'conversation_enhanced',
    'ConsciousnessCore',
    'DAWNConsciousness',
]

# Add subsystems if available
if _has_subsystems:
    __all__.extend([
        'PulseSubsystem',
        'SchemaSubsystem',
        'MemorySubsystem',
        'VisualSubsystem',
    ])
