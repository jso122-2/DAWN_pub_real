"""
Pulse Module - Core pulse and SCUP tracking functionality
"""

from pulse.pulse_layer import (
    PulseLayer,
    PulseState,
    get_pulse_layer,
    run_tick,
    get_state,
    add_heat,
    update_scup
)

# Export key components
__all__ = [
    'PulseLayer',
    'PulseState',
    'get_pulse_layer',
    'run_tick',
    'get_state',
    'add_heat',
    'update_scup'
]
