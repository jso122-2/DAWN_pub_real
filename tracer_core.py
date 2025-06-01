import random
import os
from datetime import datetime
from event_bus import event_bus, TickEvent, Event

TRACER_REGISTRY = {}

class TracerMoved(Event):
    def __init__(self, tracer_id: str, new_node: str, reason: str):
        self.tracer_id = tracer_id
        self.new_node = new_node
        self.reason = reason

class Tracer:
    def __init__(self, tracer_id: str, start_node: str = "ROOT", tracer_type="bee"):
        self.tracer_id = tracer_id
        self.current_node = start_node
        self.tracer_type = tracer_type
        self.urgency = 0.5
        self.path_memory = [(start_node, datetime.now())]
        self.state = "idle"

    async def on_tick(self, event: TickEvent):
        mood = self._get_mood_for_tick()
        self.urgency = self._mood_to_urgency(mood)
        if random.random() < self.urgency:
            self.current_node = self._choose_next()
            self.path_memory.append((self.current_node, datetime.now()))
            await event_bus.publish(TracerMoved(
                tracer_id=self.tracer_id,
                new_node=self.current_node,
                reason=f"mood:{mood}"
            ))
            print(f"[Tracer] {self.tracer_id} moved to {self.current_node} | mood={mood} | urgency={self.urgency:.2f}")
        else:
            print(f"[Tracer] {self.tracer_id} held | mood={mood} | urgency={self.urgency:.2f}")

    def _choose_next(self) -> str:
        zone_map = {
            "whale": ["C3", "D4", "D3"],
            "bee": ["A1", "B2", "C3", "D4"],
            "crow": ["C3", "B2", "A2"],
            "spider": ["A1", "A2", "B1"],
            "ant": ["B1", "B2", "C1", "C2"],
            "beetle": ["D1", "D2", "C2"]
        }
        return random.choice(zone_map.get(self.tracer_type, ["B2"]))

    def _mood_to_urgency(self, mood):
        return {
            "anxious": 1.0, "excited": 0.8,
            "curious": 0.6, "reflective": 0.4,
            "calm": 0.2
        }.get(mood.lower(), 0.5)

    def _get_mood_for_tick(self) -> str:
        return random.choice(["anxious", "calm", "excited", "reflective", "curious"])

    def emit_rgb_pigment(self):
        pigment_map = {
            "bee": (255, 223, 0),
            "whale": (0, 191, 255),
            "crow": (70, 70, 70),
            "spider": (138, 43, 226),
            "ant": (139, 69, 19),
            "beetle": (255, 105, 180),
            "owl": (192, 192, 192)
        }
        return pigment_map.get(self.tracer_type, (128, 128, 128))

    def dump_trail_to_csv(self, path="logs/tracers/"):
        os.makedirs(path, exist_ok=True)
        with open(f"{path}{self.tracer_id}_trail.csv", "w") as f:
            f.write("timestamp,node\n")
            for node, ts in self.path_memory:
                f.write(f"{ts.isoformat()},{node}\n")

def spawn_tracer(tracer_id: str, start_node: str = "ROOT", tracer_type="bee") -> Tracer:
    tracer = Tracer(tracer_id, start_node, tracer_type)
    TRACER_REGISTRY[tracer_id] = tracer
    event_bus.subscribe(TickEvent, tracer.on_tick)
    return tracer
