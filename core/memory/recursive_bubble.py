# /core/recursive_bubble.py

"""
Recursive Bubble: the core reflective loop of DAWN.
Processes the now-state (sentence), executes sigils, and reacts to SCUP state.
"""

class RecursiveBubble:
    def __init__(self, schema_state):
        self.now_state = None
        self.active_sigils = []
        self.tick_id = 0
        self.pause_until = -1
        self.schema_state = schema_state  # shared state object
        self.recent_history = []

    def update(self, sentence, scup_score):
        """
        Main reflection loop. Updates now-state, checks SCUP, pauses if needed.
        """
        self.tick_id += 1

        if self.tick_id < self.pause_until:
            print(f"[Bubble] 💤 Paused (SCUP recovery). Resumes at tick {self.pause_until}")
            return

        self.now_state = sentence
        self.recent_history.append(sentence)
        if len(self.recent_history) > 10:
            self.recent_history.pop(0)

        print(f"[Bubble] 🧠 Reflecting on: {sentence}")

        # SCUP breakdown
        if scup_score < 0.3:
            self.pause_until = self.tick_id + 10
            print(f"[Bubble] ⚠️ SCUP collapse ({scup_score:.2f}) — cooling for 10 ticks")
            return

        self.execute_sigils()

    def execute_sigils(self):
        """
        Executes all current sigils in the active loop.
        Sigils are wiped every 10 ticks externally unless persistent.
        """
        for sigil in self.active_sigils:
            if sigil.priority == "persistent":
                print(f"[Bubble] ⚠️ Persistent sigil: {sigil.label}")
            sigil.invoke()

    def inject_sigils(self, sigils):
        """
        External hook to inject sigils for this tick.
        """
        self.active_sigils = sigils
