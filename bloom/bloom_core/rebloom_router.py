import os
from bloom.juliet_flower import JulietFlower
from reflection.owl.owl_tracer_log import owl_log

REFRACTOR_QUEUE = []

# Thresholds and classifiers
ENTROPY_THRESHOLD = 0.75
SEAL_ENTROPY_THRESHOLD = 0.85
DRIFT_THRESHOLD = 0.5
SHAPE_BLACKLIST = {"chaotic", "collapsed", "unstable"}

def activate_bloom(bloom: JulietFlower):
    """
    Activates a stable bloom by initializing its core processes.
    """
    try:
        bloom.initialize()
        bloom.activate()
        return True
    except Exception as e:
        owl_log(f"[RebloomRouter] ❌ Failed to activate bloom {bloom.seed_id}: {str(e)}", level="error")
        return False

def is_rebloom_unstable(bloom: JulietFlower):
    """
    Checks if a bloom is unstable based on:
    - Entropy
    - Drift magnitude
    - Shape class
    - Instability flags
    """
    entropy = bloom.entropy_score
    drift = getattr(bloom, "drift_magnitude", 0.0)
    shape = getattr(bloom, "shape_state", "undefined")
    flags = getattr(bloom, "instability_flags", 0)

    return (
        entropy > ENTROPY_THRESHOLD
        or drift > DRIFT_THRESHOLD
        or shape in SHAPE_BLACKLIST
        or flags >= 2
    )

def seal_bloom(bloom: JulietFlower, directory="juliet_flowers/sealed"):
    """
    Auto-seals unstable reblooms, removing them from circulation.
    """
    os.makedirs(directory, exist_ok=True)
    bloom_file = bloom.save(directory=directory)
    print(f"[Seal] 🌑 Bloom sealed: {bloom_file}")

def route_rebloom(bloom: JulietFlower):
    """
    Routes reblooms based on instability metrics:
    - Auto-seals if extremely unstable (entropy, shape, flags)
    - Sends to refactor queue for milder instability
    - Else activates normally
    """
    entropy = bloom.entropy_score
    shape = getattr(bloom, "shape_state", "undefined")

    if is_rebloom_unstable(bloom):
        if entropy > SEAL_ENTROPY_THRESHOLD or shape in SHAPE_BLACKLIST:
            seal_bloom(bloom)
            owl_log(f"[RebloomRouter] 🔒 Auto-sealed unstable rebloom: {bloom.seed_id} | shape={shape} | entropy={entropy:.2f}")
        else:
            REFRACTOR_QUEUE.append(bloom)
            owl_log(f"[RebloomRouter] 🔁 Routed {bloom.seed_id} to refactor queue (shape={shape}, entropy={entropy:.2f})")
    else:
        activate_bloom(bloom)
        owl_log(f"[RebloomRouter] ✅ {bloom.seed_id} activated (stable)")
