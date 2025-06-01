import random
from datetime import datetime
from tracers.base import Tracer, TRACER_REGISTRY
from core.event_bus import event_bus, TickEvent, Event
from mycelium.nutrient_logger import log_nutrient_flow
from core.system_state import pulse  # for shared mood_pressure

class BeeMoved(Event):
    def __init__(self, tracer_id, node, mood, pulse):
        self.tracer_id = tracer_id
        self.node = node
        self.mood = mood
        self.pulse = pulse

class Bee(Tracer):
    def __init__(self, tracer_id="bee-001", start="ROOT", mood="curious"):
        super().__init__(
            name=tracer_id,
            role="Mood-reactive nutrient carrier",
            watch=["/mood", "~pulse"],
            act=self.respond_to_sigil
        )
        self.current_node = start
        self.mood = mood
        self.path_memory = [(start, datetime.now())]
        self.urgency = 0.5
        TRACER_REGISTRY[tracer_id] = self
        event_bus.subscribe(TickEvent, self.on_tick)

    def _choose_mood(self):
        self.mood = random.choice(["curious", "reflective", "anxious", "joyful", "calm"])
        self.urgency = {
            "anxious": 1.0,
            "curious": 0.7,
            "reflective": 0.5,
            "calm": 0.3,
            "joyful": 0.8
        }[self.mood]
        pulse.mood_pressure[self.mood] = pulse.mood_pressure.get(self.mood, 0) + 1

    def _emit_pulse(self, pulse_value):
        log_nutrient_flow({
            "seed_id": self.name,
            "mood": self.mood,
            "entropy_score": 0.4,
            "bloom_factor": pulse_value,
            "lineage_depth": 2
        }, flow_strength=pulse_value)

    async def on_tick(self, event: TickEvent):
        self._choose_mood()
        if random.random() < self.urgency:
            self.current_node = random.choice(["A1", "B2", "C3", "D4"])
            self.path_memory.append((self.current_node, datetime.now()))
            pulse_value = round(self.urgency * 0.8, 2)
            self._emit_pulse(pulse_value)

            await event_bus.publish(BeeMoved(
                tracer_id=self.name,
                node=self.current_node,
                mood=self.mood,
                pulse=pulse_value
            ))
            print(f"[🐝 Bee] {self.name} moved to {self.current_node} | {self.mood} → pulse {pulse_value}")
        else:
            print(f"[🐝 Bee] {self.name} held | mood={self.mood} | urgency={self.urgency:.2f}")

    def respond_to_sigil(self):
        self._choose_mood()
        pulse_value = round(self.urgency * 0.9, 2)
        self._emit_pulse(pulse_value)
        print(f"[🐝 Bee] responded to sigil | mood={self.mood} | pulse={pulse_value}")

    def report(self):
        if pulse.mood_pressure:
            dominant = max(pulse.mood_pressure, key=pulse.mood_pressure.get)
        else:
            dominant = "N/A"

        report_data = (
            f"Bee Tracer Report:\n"
            f"  Mood: {self.mood}\n"
            f"  Mood Dominance: {dominant}\n"
            f"  Urgency: {self.urgency:.2f}\n"
            f"  Current Node: {self.current_node}\n"
            f"  Path Length: {len(self.path_memory)}"
        )
        print(report_data)
        return report_data
