# persephone.py
# Oversees memory decay, rebirth, and schema edge monitoring

from bloom.spawn_bloom import spawn_bloom
from datetime import datetime

class Persephone:
    def __init__(self):
        self.soft_edges = []

    def observe(self, flower):
        if flower.entropy_score > 0.8 and (flower.urgency or 0) > 0.7:
            print(f"[Persephone] 🕯️ High entropy bloom flagged → {flower.seed_id}")
            if flower.seed_id not in self.soft_edges:
                self.soft_edges.append(flower.seed_id)

    def rebirth(self, seed_id):
        print(f"[Persephone] 🌱 Rebirthing memory from soft edge → {seed_id}")
        new_bloom = {
            "seed_id": f"rebirth-{seed_id}-{datetime.now().strftime('%H%M%S')}",
            "lineage_depth": 1,
            "entropy_score": 0.3,
            "bloom_factor": 1.1,
            "mood": "reflective"
        }
        spawn_bloom(new_bloom)
