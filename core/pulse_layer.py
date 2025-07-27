"""
Bridge module so core.* imports can access PulseLayer via `pulse_layer` instance.
"""
import logging
from pulse.pulse_layer import PulseLayer

log = logging.getLogger(__name__)

# Singleton instance expected by DAWN
pulse_layer = PulseLayer()

# Ensure it exposes a .tick(delta) method (delegate if missing)
if not hasattr(PulseLayer, "tick"):
    def _default_tick(self, delta: float = 0.0):
        log.debug("PulseLayer tick (noop) delta=%s", delta)
    setattr(PulseLayer, "tick", _default_tick) 