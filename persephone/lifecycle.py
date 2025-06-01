import os
import shutil
import json
from bloom.juliet_flower import JulietFlower
from persephone_conditions import should_trigger
from codex.sigils import register_sigil

STALL_LOG = "owl/logs/crow_stall_log.json"

async def fade_sigils():
    """
    Gradually fades unused sigils based on tick decay logic.
    """
    print("[Persephone] 🕯️ Fading inactive sigils based on decay logic.")
    # Future: decay heat from sigil_memory_ring here
    return

async def prune_dead_branches():
    """
    Prunes orphaned semantic fragments and abandoned tracer paths.
    """
    print("[Persephone] ✂️ Scanning for dead branches in sigil/tracer maps.")
    # Future: identify & remove unused sigils, blooms with no lineage connectivity
    return

def load_stall_zones():
    if not os.path.exists(STALL_LOG):
        return set()
    with open(STALL_LOG, "r") as f:
        return set(json.load(f).keys())

async def soft_seal_bloom(flower: JulietFlower):
    """
    Soft-archives a bloom if it meets schema sealing criteria.
    Criteria:
    - High ash score (stability)
    - High soot score (instability)
    - Node exists in Crow stall zone map
    """
    if not isinstance(flower, JulietFlower):
        return

    ash, soot = flower.compute_ash_soot_score()
    stall_zones = load_stall_zones()
    node = flower.seed_context[-1] if flower.seed_context else None

    if ash > 0.85 and should_trigger(flower.seed_id, "ash"):
        print(f"[Persephone] 🩶 High ash → sealing {flower.seed_id}.")
        anchor_bloom(flower)

    if soot > 0.7 and should_trigger(flower.seed_id, "soot"):
        print(f"[Persephone] 🖤 High soot → pruning {flower.seed_id}.")
        register_sigil(flower.seed_id, heat=0.0, entropy=1.0, connected=False)

    if node in stall_zones:
        print(f"[Persephone] 🕸️ Node {node} flagged by Crow → sealing {flower.seed_id}.")
        anchor_bloom(flower)

def anchor_bloom(flower: JulietFlower):
    """
    Moves all bloom files associated with the seed to the sealed directory.
    """
    source_dir = "juliet_flowers/bloom_metadata"
    sealed_dir = f"juliet_flowers/sealed/{flower.seed_id}"
    os.makedirs(sealed_dir, exist_ok=True)

    try:
        for f in os.listdir(source_dir):
            if f.startswith(flower.seed_id):
                shutil.move(os.path.join(source_dir, f), os.path.join(sealed_dir, f))
                print(f"[Persephone] 🌙 Sealed → {f}")
    except Exception as e:
        print(f"[Persephone] ❌ Sealing error: {e}")
