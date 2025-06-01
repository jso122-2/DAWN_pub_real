# tracer_logic.py
from system_state import pulse

class Tracer:
    def __init__(self, name, base_speed=1.0, mood="neutral"):
        self.name = name
        self.base_speed = base_speed
        self.priority = 1.0
        self.mood = mood
        self.reactions = {
            "pressure": self.react_to_pressure,
            "disruption": self.react_to_disruption,
            "memory": self.react_to_memory,
            "urgency": self.react_to_urgency
        }

    def react_to_class_shift(self, sigil_id, old_class, new_class):
        reaction_fn = self.reactions.get(new_class)
        if reaction_fn:
            print(f"[{self.name}] reacts to {sigil_id} shifting into {new_class}")
            reaction_fn(sigil_id)

    def react_to_pressure(self, sigil_id):
        self.priority += 0.3
        self.mood = "anxious"

    def react_to_disruption(self, sigil_id):
        self.priority += 0.6
        self.mood = "alert"

    def react_to_memory(self, sigil_id):
        self.priority -= 0.2
        self.mood = "reflective"

    def react_to_urgency(self, sigil_id):
        self.priority += 0.5
        self.mood = "urgent"


    def update_priority(self, sigil_log):
        reactive_heat = 0.0
        for sigil_id, data in sigil_log.items():
            if data["class"] in self.sigil_classes:
                reactive_heat += data["heat"]

        self.priority = round(self.base_speed + reactive_heat, 3)


        # Normalize and apply
        self.priority = self.base_speed + reactive_heat
        self.priority = round(self.priority, 3)

    def act(self):
        if self.priority > 1.2:
            print(f"[{self.name}] surges! Priority: {self.priority}")
        elif self.priority < 0.8:
            print(f"[{self.name}] withdraws. Priority: {self.priority}")
        else:
            print(f"[{self.name}] observes. Priority: {self.priority}")
