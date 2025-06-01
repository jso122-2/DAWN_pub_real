import random
from owl.owl_tracer_log import owl_log
from bloom.spawn_bloom import load_all_blooms  # assumes you have this
from time import sleep

# Memory of previous batches
VISUAL_HISTORY = []

def select_next_visual_batch(all_blooms, batch_size=5):
    """
    Selects the next batch based on entropy + novelty score.
    """
    unvisited = [b for b in all_blooms if b.seed_id not in VISUAL_HISTORY]
    scored = []

    for bloom in unvisited:
        entropy = getattr(bloom, "entropy_score", 0.5)
        factor = getattr(bloom, "bloom_factor", 1.0)
        drift = getattr(bloom, "drift_magnitude", 0.3)
        mood = getattr(bloom, "mood", "neutral")

        # Score = entropy + 0.5 * drift + 0.2 * bloom_factor
        score = entropy + (0.5 * drift) + (0.2 * factor)
        scored.append((bloom, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    next_batch = [b[0] for b in scored[:batch_size]]
    return next_batch

def owl_log_commentary(bloom):
    """
    Logs a dynamic line about what Owl sees in a bloom.
    """
    options = [
        f"[Owl] 🪶 Observing {bloom.seed_id} — entropy={bloom.entropy_score:.2f}, mood={bloom.mood}",
        f"[Owl] 👁️ Drift detected: {bloom.seed_id} → bloom_factor={bloom.bloom_factor:.2f}",
        f"[Owl] 🌾 Tracing bloom {bloom.seed_id} lineage={bloom.lineage_depth}, entropy={bloom.entropy_score:.2f}",
        f"[Owl] 🌀 Bloom {bloom.seed_id} reflects recursive tension.",
        f"[Owl] 🧠 Forecasting synthesis potential in {bloom.seed_id}"
    ]
    owl_log(random.choice(options))

def run_owl_visual_oscillator(batch_size=5, delay=1.5):
    """
    Main loop: Owl cycles through 5-bloom batches, comments visually.
    """
    from bloom.spawn_bloom import load_all_blooms
    all_blooms = load_all_blooms()

    while True:
        batch = select_next_visual_batch(all_blooms, batch_size=batch_size)

        if not batch:
            owl_log("[Owl] 🌙 All blooms reviewed. Cycle complete.")
            break

        for bloom in batch:
            VISUAL_HISTORY.append(bloom.seed_id)
            owl_log_commentary(bloom)
            sleep(delay)

        owl_log("[Owl] 🔄 Moving to next batch...\n")
        sleep(1.5)
