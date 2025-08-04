"""
DAWN core package - Core modules for DAWN consciousness system
"""

# Simplified imports to avoid relative import issues
# Previous subsystems (if they still exist)
_has_subsystems = False

# Core consciousness modules - simplified to avoid relative import issues
ConsciousnessCore = None
DAWNConsciousness = None

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
