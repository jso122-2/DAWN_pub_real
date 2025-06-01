# /owl/owl_drift_sentinel.py

from owl.owl_vector import get_last_vector_drift, classify_alignment
from schema.schema_state import get_current_alignment
from codex.sigil_router import trigger_sigil

DRIFT_THRESHOLD = 0.6
ALIGNMENT_SUPPRESSION_THRESHOLD = 0.4
ALIGNMENT_COLLAPSE_STREAK = 3

alignment_streak = []


def owl_drift_check(tick_id=None):
    delta = get_last_vector_drift()
    alignment = get_current_alignment()
    level = classify_alignment(delta)

    print(f"[OwlSentinel] 🧠 Drift ∆={delta:.3f} | Alignment={alignment:.3f} → {level}")

    # 🔴 Alert if drift too high
    if delta > DRIFT_THRESHOLD:
        print(f"[OwlSentinel] ⚠️ High drift warning @tick={tick_id}")

    # ❌ Suppression override if misaligned
    if alignment < ALIGNMENT_SUPPRESSION_THRESHOLD:
        print(f"[OwlSentinel] ❌ Alignment too low – suppression override triggered.")
        return "override_suppression"

    # 🆘 Sigil call if collapse sustained
    alignment_streak.append(alignment < 0.3)
    if len(alignment_streak) > ALIGNMENT_COLLAPSE_STREAK:
        alignment_streak.pop(0)

    if all(alignment_streak):
        print("[OwlSentinel] 🔁 Alignment collapse sustained – triggering sigil reboot")
        trigger_sigil("/sigil_reboot")
        alignment_streak.clear()

    return None
