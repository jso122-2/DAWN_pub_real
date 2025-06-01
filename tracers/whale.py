import random
from datetime import datetime
from core.event_bus import event_bus, TickEvent, Event
from math import sqrt

class WhalePulse(Event):
    def __init__(self, tracer_id, pigment, belief, zone):
        self.tracer_id = tracer_id
        self.pigment = pigment
        self.belief = belief
        self.zone = zone

# 🎨 Platonic Pigment Map
PIGMENTS = {
    "Justice": ((255, 0, 0), "Moral decisions, retribution"),
    "Harmony": ((0, 255, 0), "Peace, rhythm, reconciliation"),
    "Inquiry": ((0, 0, 255), "Knowledge, skepticism"),
    "Truth": ((255, 255, 0), "Revelation, epistemic shock"),
    "Irony": ((110, 0, 255), "Humor, satire, self-awareness"),
    "Care": ((0, 255, 110), "Empathy, nurture, protection")
}

def nearest_belief(rgb):
    return min(PIGMENTS.items(), key=lambda item: euclidean(item[1][0], rgb))[0]

def euclidean(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

class Whale:
    def __init__(self, tracer_id, start="D4", belief=None):
        self.tracer_id = tracer_id
        self.current_node = start
        self.belief = belief or random.choice(list(PIGMENTS.keys()))
        self.pigment, self.content = PIGMENTS[self.belief]
        self.path_memory = [(start, datetime.now())]

    async def on_tick(self, event: TickEvent):
        if random.random() < 0.7:
            self.current_node = random.choice(["C3", "D4", "D3"])
            self.path_memory.append((self.current_node, datetime.now()))

            await event_bus.publish(WhalePulse(
                tracer_id=self.tracer_id,
                pigment=self.pigment,
                belief=self.belief,
                zone=self.current_node
            ))

            print(f"[Whale] 🐋 {self.tracer_id} echoed {self.belief} ({self.pigment}) in {self.current_node}")
        else:
            print(f"[Whale] 🐋 {self.tracer_id} held in {self.current_node}")

    def get_pigment(self):
        return self.pigment

    def get_belief(self):
        return self.belief

    def match_belief(self, rgb):
        return nearest_belief(rgb)

    def report(self):
        return {
            "id": self.tracer_id,
            "belief": self.belief,
            "pigment": self.pigment,
            "current": self.current_node,
            "last_path": self.path_memory[-3:]
        }
