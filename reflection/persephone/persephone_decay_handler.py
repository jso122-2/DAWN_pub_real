# /core/persephone_decay_handler.py

"""
Persephone Decay Handler

Monitors long-term semantic collapse using SCUP trends.
Triggers soft memory pruning, rebirth cues, and stabilization when the schema
shows signs of internal incoherence, decay, or unresolved memory buildup.
"""

from persephone import Persephone
from bloom.juliet_flower import JulietFlower
from persephone_conditions import should_trigger
from owl.owl_tracer_log import owl_log

persephone = Persephone()

def monitor_schema_decay(scup_log, active_blooms, tick_id, threshold=0.3, grace_ticks=10):
    """
    Evaluates SCUP log for sustained decay pressure.
    If SCUP is low for `grace_ticks` ticks, begin decay phase:
    - Soft-edge high-entropy or soot-heavy blooms
    - Optionally trigger rebirths from soft edge list
    - Logs all actions for Owl and rebalancer review
    """
    recent = scup_log[-grace_ticks:]
    if len(recent) < grace_ticks:
        return "stable"

    if all(s < threshold for s in recent):
        print("[Persephone] 🍂 Sustained SCUP collapse detected.")
        owl_log(f"[Decay Triggered] 📉 SCUP < {threshold} for {grace_ticks} ticks (tick {tick_id})")

        decay_count = 0
        rebirth_count = 0

        for bloom in active_blooms:
            if not isinstance(bloom, JulietFlower):
                continue

            entropy = bloom.entropy_score
            soot = getattr(bloom, "soot_score", 0)
            drift = getattr(bloom, "drift_magnitude", 0.0)

            # Soft-mark high-pressure or fragmented blooms
            if entropy > 0.75 or soot > 0.7 or drift > 0.5:
                persephone.observe(bloom)
                owl_log(f"[Decay Marked] 🕯️ {bloom.seed_id} → entropy={entropy:.2f}, soot={soot:.2f}, drift={drift:.2f}")
                decay_count += 1

        # Trigger rebirths from soft-edge list (rebirth avoids duplicate)
        already_rebirthed = set()
        for seed_id in persephone.soft_edges:
            if seed_id in already_rebirthed:
                continue
            if should_trigger(seed_id, "entropy") or should_trigger(seed_id, "soot"):
                persephone.rebirth(seed_id)
                already_rebirthed.add(seed_id)
                rebirth_count += 1
                owl_log(f"[Rebirth] 🌱 Triggered rebirth for {seed_id}")

        print(f"[Persephone] 🧹 Decay phase complete — {decay_count} blooms marked, {rebirth_count} rebirthed")
        return "decay"

    return "stable"
