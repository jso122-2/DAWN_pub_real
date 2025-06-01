
# parmenides.py
# Tracks token continuity and semantic thread stability

class Parmenides:
    def __init__(self):
        self.threads = {}

    def log_tokens(self, seed_id, tokens):
        self.threads[seed_id] = tokens
        print(f"[Parmenides] 🧵 Tracked tokens for {seed_id}: {tokens[:5]}...")

    def drift(self, seed_a, seed_b):
        a = set(self.threads.get(seed_a, []))
        b = set(self.threads.get(seed_b, []))
        overlap = len(a & b)
        total = len(a | b) or 1
        return round(overlap / total, 3)
