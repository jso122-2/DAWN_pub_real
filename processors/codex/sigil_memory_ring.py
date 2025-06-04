# /codex/sigil_memory_ring.py

from datetime import datetime
from core.schema_anomaly_logger import log_anomaly

# --- Sigil Object Definition ---

class Sigil:
    def __init__(self, name, entropy=0.0, house=None, temperature=18.0):
        self.name = name                    # e.g. "/heat"
        self.entropy = entropy              # 0.0 → 1.0 volatility
        self.house = house or "default"     # task group or origin
        self.temperature = temperature      # activation energy or mood-link
        self.age = 0                        # tick-based aging
        self.created_at = datetime.now()
        self.active = True

    def decay(self, rate=0.01):
        self.entropy = max(0.0, self.entropy - rate)
        self.age += 1

    def is_expired(self, threshold=50):
        return self.age > threshold or self.entropy < 0.01

    def summary(self):
        return {
            "name": self.name,
            "entropy": self.entropy,
            "house": self.house,
            "temp": self.temperature,
            "age": self.age,
            "active": self.active
        }

# --- Memory Ring Structure ---

# Stores sigils in memory ring grouped by house
sigil_memory_ring = {}

log_anomaly(
    label="PhantomStructure",
    message="DAWN requested 'sigil_memory_ring' from codex before it was defined. Memory ring initialized."
)

# --- Ring Management Utilities ---

def register_sigil(name, entropy=0.1, house=None, temperature=18.0):
    """
    Registers or updates a sigil in the memory ring.
    """
    if name not in sigil_memory_ring:
        sigil_memory_ring[name] = Sigil(name, entropy, house, temperature)
        log_anomaly("SigilRegistered", f"Sigil '{name}' registered to house '{house or 'default'}'")
    else:
        sigil_memory_ring[name].entropy += entropy  # amplify signal
        sigil_memory_ring[name].age = 0  # reset age on reactivation

def decay_all_sigils():
    """
    Applies decay to all sigils.
    """
    for sigil in sigil_memory_ring.values():
        sigil.decay()

def age_all_sigils():
    """
    Increments age of all sigils. Can be used with decay.
    """
    for sigil in sigil_memory_ring.values():
        sigil.age += 1

def purge_expired_sigils():
    """
    Removes sigils that are too old or too quiet.
    """
    expired = [k for k, s in sigil_memory_ring.items() if s.is_expired()]
    for k in expired:
        log_anomaly("SigilExpired", f"Sigil '{k}' removed from memory ring.")
        del sigil_memory_ring[k]

def get_active_sigil_entropy_list():
    """
    Returns entropy values for all active sigils for SCUP/SHI.
    """
    return [s.entropy for s in sigil_memory_ring.values() if s.active]

def dump_sigil_snapshot():
    """
    Returns full state of ring for diagnostic output or Owl commentary.
    """
    return {k: v.summary() for k, v in sigil_memory_ring.items()}

def get_sigil_energy_index():
    """
    Returns a normalized 0.0–1.0 value representing the current symbolic activity load.
    Used for dynamic visual tinting of fractal blooms.
    """
    if not sigil_memory_ring:
        return 0.0

    total_entropy = sum(s.entropy for s in sigil_memory_ring.values() if s.entropy is not None)
    count = len([s for s in sigil_memory_ring.values() if s.entropy is not None])

    if count == 0:
        return 0.0

    avg_entropy = total_entropy / count
    return min(max(avg_entropy, 0.0), 1.0)
