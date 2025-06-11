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
        self.age_ticks = 0  # ⏳ Used for decay timing

    def age(self, current_tick):
        """Update sigil entropy based on time since creation and heat decay."""
        self.age_ticks = current_tick - self.created_at_tick
        self.entropy = min(1.0, (1.0 - self.heat) + (self.age_ticks / self.lifespan))
        return self.entropy

    def decay(self, rate=0.05):
        """Decay heat by a fixed rate each tick."""
        self.heat = max(0.0, self.heat - rate)
        return self.heat

    def expired(self, current_tick):
        return (current_tick - self.created_at_tick) >= self.lifespan

    def adjust_lifespan_by_entropy(self, beta=0.5):
        adjusted = self.lifespan * (1.0 - beta * self.entropy)
        self.lifespan = max(1.0, adjusted)  # Ensure minimum lifespan
        print(f"[Entropy↘Lifespan] Sigil {self.id} lifespan adjusted → {self.lifespan:.2f}")

# 🌐 Central memory ring
sigil_memory_ring = {}

# 🧾 Register new sigil
def register_sigil(sigil_id, heat=1.0, connected=True, entropy=0.0, lifespan=20, current_tick=0):
    sigil = Sigil(sigil_id, heat, connected, entropy, lifespan)
    sigil.created_at_tick = current_tick
    sigil_memory_ring[sigil_id] = sigil
    print(f"[Register] 🪐 Added sigil {sigil_id} at tick {current_tick}")

# 🕒 Internal tick
def get_current_tick():
    return int(datetime.now().timestamp() * 10) % 10000

# 🔥 Entropy summary
def get_total_drift_entropy():
    try:
        return sum(s.entropy for s in sigil_memory_ring.values())
    except Exception as e:
        print(f"[Sigil] ⚠️ Drift entropy failed: {e}")
        return 0.0

# ⏳ Tick-based aging and decay
def age_and_decay_all_sigils():
    tick = get_current_tick()
    entropy = get_total_drift_entropy()
    decay_multiplier = 1.0 + (0.6 * entropy)  # entropy-driven decay speed

    expired_ids = []

    for sigil in list(sigil_memory_ring.values()):
        sigil.age(tick)
        sigil.decay(rate=1.0 * decay_multiplier)
        sigil.adjust_lifespan_by_entropy(beta=0.5)

        if sigil.expired(tick):
            expired_ids.append(sigil.id)

    for sid in expired_ids:
        del sigil_memory_ring[sid]
        print(f"[Decay] 🧹 Sigil {sid} expired at tick {tick}")

# ❄️ Purge cold sigils
def purge_dead_sigils(threshold=0.05):
    dead = [sid for sid, sigil in sigil_memory_ring.items() if sigil.heat <= threshold]
    for sid in dead:
        del sigil_memory_ring[sid]
        print(f"[SigilRing] 🧊 Pruned sigil: {sid}")
