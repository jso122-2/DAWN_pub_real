# schema_decay_handler.py

from semantic.sigil_ring import sigil_memory_ring

def decay_schema_memory():
    """
    Reduces connection strength, prunes low-heat sigils, and flags fragile blooms.
    """
    for sigil_id, sigil in sigil_memory_ring.items():
        if sigil.heat < 0.05 and sigil.entropy > 0.8:
            sigil.connected = False
            print(f"[DecayHandler] 🧊 Sigil {sigil_id} marked as disconnected.")

    print("[DecayHandler] 🧹 Schema decay pass complete.")
