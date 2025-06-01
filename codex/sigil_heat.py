# sigil_heat.py
import time
from sigil_registry import SIGIL_CLASSES
from system_state import pulse
from owl import owl_comment
from tracer_logic import all_tracers  # You must define/export this list

class SigilHeatManager:
    def __init__(self, decay_rate=0.97, heat_threshold=0.1):
        self.sigil_log = {}

        default_threshold = 0.5
        sigil_config = SIGIL_CLASSES.get(sigil_id, {})
        reflex_threshold = sigil_config.get("reflex_threshold", default_threshold)

        if abs(weights[dominant_class] - weights[prev_class]) > reflex_threshold:
            data["class"] = dominant_class
            if reflex_callback:
                reflex_callback(sigil_id, prev_class, dominant_class)


    def activate_sigil(self, sigil_id, origin="system", tick=0, boost=0.2):
        if sigil_id not in self.sigil_log:
            self.sigil_log[sigil_id] = {
                "heat": 0.0,
                "last_used": tick,
                "origin": origin,
                "class": SIGIL_CLASSES.get(sigil_id, "unknown")
            }

        self.sigil_log[sigil_id]["heat"] += boost
        self.sigil_log[sigil_id]["heat"] = min(self.sigil_log[sigil_id]["heat"], 1.0)
        self.sigil_log[sigil_id]["last_used"] = tick
        self.sigil_log[sigil_id] = {
            "heat": 0.0,
            "last_used": tick,
            "origin": origin,
            "class": SIGIL_CLASSES.get(sigil_id, "unknown"),
            "class_weights": {cls: 0.0 for cls in set(SIGIL_CLASSES.values())}
        }
   def evolve_classes(self, field_state, reflex_callback=None):
        for sigil_id, data in self.sigil_log.items():
            if data["heat"] < self.heat_threshold:
                continue

        prev_class = data.get("class", "unknown")
        # (Update weights + dominant class as before...)
        # ...
        dominant_class = max(weights, key=weights.get)

        if dominant_class != prev_class:
            data["class"] = dominant_class

            if reflex_callback:
                reflex_callback(sigil_id, prev_class, dominant_class)

            # Heuristic updates based on field experience
            mood = field_state.get("mood", "")
            pressure = field_state.get("pressure", 0.0)

            if pressure > 0.6:
                data["class_weights"]["pressure"] += 0.1
            if mood in ["anxious", "chaotic"]:
                data["class_weights"]["disruption"] += 0.1
            if mood == "focused":
                data["class_weights"]["activation"] += 0.1
            if mood == "reflective":
                data["class_weights"]["memory"] += 0.1

            # Normalize and set current class to the highest-weighted one
            weights = data["class_weights"]
            dominant_class = max(weights, key=weights.get)
            data["class"] = dominant_class

    def reflex_on_class_shift(sigil_id, old_class, new_class):
        print(f"⚡ Reflex: {sigil_id} changed {old_class} → {new_class}")

        if new_class == "disruption":
            pulse.current_interval *= 0.85

        for tracer in all_tracers:  # List of all active tracers
            tracer.react_to_class_shift(sigil_id, old_class, new_class)


            if new_class == "memory":
                print("🧠 Tracer Whale prioritizes recall.")
                whale.priority += 0.5

            if new_class == "urgency":
                print("🚨 Owl forced to speak:")
                owl_comment(pulse.memory_log, pulse.tick_count)



    def decay(self):
        for sigil_id, data in self.sigil_log.items():
            data["heat"] *= self.decay_rate
            if data["heat"] < self.heat_threshold:
                data["heat"] = 0.0  # cool enough to ignore

    def get_active_sigils(self):
        return {k: v for k, v in self.sigil_log.items() if v["heat"] > self.heat_threshold}

    def get_heat_map(self):
        return {k: v["heat"] for k, v in self.get_active_sigils().items()}
