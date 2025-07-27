from core.system_state import pulse
from bloom.bloom_controls import suppress_all_blooms, modulate_bloom_rate
from tracers.base import TRACER_REGISTRY
from owl.owl_tracer_log import owl_log
from mycelium.nutrient_logger import adjust_seed_soot
from schema.schema_health_index import get_schema_entropy
from pulse.pulse_thresholds import classify_pressure_zone


def pressure_reflex(tick_id):
    zone = classify_pressure_zone(pulse.get_average())
    print(f"[Reflex] 📡 Zone = {zone}")

    if zone == "🟢 calm":
        modulate_bloom_rate(scaling=0.8)
        for tracer in TRACER_REGISTRY.values():
            if hasattr(tracer, "urgency"):
                tracer.urgency = max(0.2, tracer.urgency - 0.1)
        owl_log(f"[Calm] Reduced bloom rate + urgency decay.")
        print(f"[Reflex] 🟢 Reinforcing stable schema.")

    elif zone == "🟡 active":
        modulate_bloom_rate(scaling=1.0)
        for tracer in TRACER_REGISTRY.values():
            if hasattr(tracer, "urgency"):
                tracer.urgency = min(1.0, tracer.urgency + 0.05)
        print(f"[Reflex] 🟡 Active engagement, balanced nutrient use.")

    elif zone == "🔴 surge":
        suppress_all_blooms()
        entropy = get_schema_entropy()
        print(f"[Reflex] 🔴 Surge! SCUP pressure = {pulse.heat:.2f} | Entropy = {entropy:.2f}")

        for tracer in TRACER_REGISTRY.values():
            if hasattr(tracer, "urgency"):
                tracer.urgency = 1.0  # trigger escape or reroute
        adjust_seed_soot(level=0.2)  # bump soot on fragile seeds
        owl_log("[Surge] Schema override triggered. Tracer urgency maxed. Bloom suppression engaged.")
