import random
import os
from datetime import datetime
from core.event_bus import event_bus, TickEvent, Event

# === HIVE MEMORY ===
TRACER_REGISTRY = {}

# === Events ===
class TracerMoved(Event):
    def __init__(self, tracer_id: str, new_node: str, reason: str):
        self.tracer_id = tracer_id
        self.new_node = new_node
        self.reason = reason

# === Tracer Class ===
class Tracer:
    def __init__(self, tracer_id: str, start_node: str = "ROOT", tracer_type: str = "bee"):
        self.tracer_id = tracer_id
        self.current_node = start_node
        self.tracer_type = tracer_type
        self.urgency = 0.5
        self.tick_interval = 1.0
        self.path_memory = [(start_node, datetime.now())]
        self.state = "idle"

    async def on_tick(self, event: TickEvent):
        mood = self._get_mood_for_tick()
        self.urgency = self._mood_to_urgency(mood)
        self._adjust_tick_interval()

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
        bias_map = {
            "whale": ["C3", "D4", "D3"],
            "bee": ["A1", "B2", "C3", "D4"],
            "spider": ["A1", "A2", "B1"],
            "crow": ["C3", "B2", "A2"]
        }
        options = bias_map.get(self.tracer_type, ["A1", "B2", "C3", "D4"])
        return random.choice(options)

    def _mood_to_urgency(self, mood):
        return {
            "anxious": 1.0,
            "excited": 0.8,
            "curious": 0.6,
            "reflective": 0.4,
            "calm": 0.2
        }.get(mood.lower(), 0.5)

    def _get_mood_for_tick(self) -> str:
        return random.choice(["anxious", "calm", "excited", "reflective", "curious"])

    def _adjust_tick_interval(self):
        if self.urgency >= 1.0:
            self.tick_interval = 0.25
        elif self.urgency >= 0.6:
            self.tick_interval = 0.5
        else:
            self.tick_interval = 1.0

    def receive_heat(self, heat):
        if heat > 2.5:
            self.state = "searching"
        elif heat < 0.3:
            self.state = "gliding"

    def apply_soot(self, soot_level):
        self.state = "pruning" if soot_level > 0.4 else "tracking"

    def route_hint(self, preferred_zone: str):
        self.current_node = preferred_zone
        print(f"[Tracer] {self.tracer_id} routed to {preferred_zone} via hint.")

    def dump_trail_to_csv(self, path="logs/tracers/"):
        os.makedirs(path, exist_ok=True)
        with open(f"{path}{self.tracer_id}_trail.csv", "w") as f:
            f.write("timestamp,node\n")
            for node, ts in self.path_memory:
                f.write(f"{ts.isoformat()},{node}\n")

    def report(self):
        return {
            "id": self.tracer_id,
            "node": self.current_node,
            "urgency": self.urgency,
            "tick_interval": self.tick_interval,
            "state": self.state,
            "type": self.tracer_type,
            "last_path": self.path_memory[-5:]
        }

# === Spawn + Register ===
def spawn_tracer(tracer_id, start="ROOT", tracer_type="bee") -> Tracer:
    t = Tracer(tracer_id, start, tracer_type)
    TRACER_REGISTRY[tracer_id] = t
    event_bus.subscribe(TickEvent, t.on_tick)
    return t
