TRACER_REGISTRY = {}

class Tracer:
    def __init__(self, name, role, watch, act):
        self.name = name
        self.role = role
        self.watch = watch
        self.act = act
        TRACER_REGISTRY[name] = self

    def respond(self, sigil):
        if sigil in self.watch:
            print(f"[{self.name}] ➤ Responding to sigil '{sigil}': {self.role}")
            self.act()
