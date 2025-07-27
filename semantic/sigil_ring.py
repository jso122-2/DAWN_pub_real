from datetime import datetime

class Sigil:
    def __init__(self, sigil_id, heat=1.0, connected=True, entropy=0.0, lifespan=20):
        self.id = sigil_id
        self.heat = heat
        self.connected = connected
        self.entropy = entropy
        self.created_at = datetime.now()
        self.lifespan = lifespan  # in ticks
        self.last_updated = self.created_at
        self.created_at_tick = 0

    def age(self, current_tick):
        """Update sigil entropy based on time since creation and heat decay."""
        age_ticks = current_tick - self.created_at_tick
        self.entropy = min(1.0, (1.0 - self.heat) + (age_ticks / self.lifespan))
        return self.entropy

    def decay(self, rate=0.05):
        """Decay heat by a fixed rate each tick."""
        self.heat = max(0.0, self.heat - rate)
        return self.heat

sigil_memory_ring = {}

def register_sigil(sigil_id, heat=1.0, connected=True, entropy=0.0, lifespan=20, current_tick=0):
    sigil = Sigil(sigil_id, heat, connected, entropy, lifespan)
    sigil.created_at_tick = current_tick
    sigil_memory_ring[sigil_id] = sigil

def get_current_tick():
    from datetime import datetime
    return int(datetime.now().timestamp() * 10) % 1000

def get_total_drift_entropy():
    try:
        return sum(s.entropy for s in sigil_memory_ring.values())
    except Exception as e:
        print(f"[Sigil] ⚠️ Drift entropy failed: {e}")
        return 0.0
        
def adjust_lifespan_by_entropy(self, entropy, beta=0.5):
    adjusted = self.base_lifespan * (1.0 - beta * entropy)
    self.lifespan = max(1.0, adjusted)  # ensure minimum viable lifespan
    print(f"[Entropy↘Lifespan] Sigil {self.id} lifespan adjusted → {self.lifespan:.2f}")


def decay_all_sigils(entropy=0.0):
    base_decay_rate = 1.0
    decay_multiplier = 1.0 + (0.6 * entropy)  # 🔥 entropy controls decay speed

    for sigil in list(sigil_memory_ring.values()):
        sigil.age += base_decay_rate * decay_multiplier
        if sigil.age >= sigil.lifespan:
            del sigil_memory_ring[sigil.id]
            print(f"[Decay] 🧹 Sigil {sigil.id} expired at age {sigil.age:.2f}")

def age_all_sigils():
    tick = get_current_tick()
    for sigil in sigil_memory_ring.values():
        sigil.age(tick)

def purge_dead_sigils(threshold=0.05):
    dead = [sid for sid, sigil in sigil_memory_ring.items() if sigil.heat <= threshold]
    for sid in dead:
        del sigil_memory_ring[sid]
        print(f"[SigilRing] 🧊 Pruned sigil: {sid}")
