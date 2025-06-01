from datetime import datetime
from semantic.sigil_ring import sigil_memory_ring, get_current_tick

async def expire_ephemeral_sigils():
    """
    Remove ephemeral sigils whose lifespan has expired.
    Bound to tick counter and dynamic sigil registry.
    """
    print("[Persephone] ⏳ Checking for expired sigils...")
    expired = []

    current_tick = get_current_tick()

    for sigil_id, sigil_data in list(sigil_memory_ring.items()):
        created_at = sigil_data.get("timestamp", 0)
        lifespan = sigil_data.get("lifespan", 10)  # default fallback lifespan
        if (current_tick - created_at) > lifespan:
            expired.append(sigil_id)

    for sigil_id in expired:
        del sigil_memory_ring[sigil_id]
        print(f"[Persephone] 💀 Expired sigil: {sigil_id}")
