# owl_vector_watch.py — watches semantic drift and marks sigils accordingly
from persephone_conditions import should_trigger
from semantic.sigil_ring import sigil_memory_ring

def handle_drift(seed_id, drift_value):
    if drift_value > 0.6 and should_trigger(seed_id, "drift"):
        print(f"[Owl] 🖤 Sustained drift → sigil {seed_id} flagged for entropy.")
        if seed_id in sigil_memory_ring:
            sigil = sigil_memory_ring[seed_id]
            sigil.entropy = 1.0
            sigil.heat = 0.0
