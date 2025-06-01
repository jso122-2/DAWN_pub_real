import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bloom.spawn_bloom import spawn_bloom
from owl.owl_rebloom_log import owl_log_rebloom
from visual.rebloom_lineage_animator import animate_rebloom_lineage
from core.system_state import system_state


class AutonomousFieldTrigger:
    def __init__(self):
        self.tick_count = 0

    async def on_tick(self, tick_data=None):
        self.tick_count += 1
        if self.tick_count % 10 == 0:  # every 10 ticks, trigger rebloom
            bloom_data = {
                "seed_id": f"autowhale-{self.tick_count}",
                "lineage_depth": (self.tick_count // 10) % 5,
                "bloom_factor": 1.0 + ((self.tick_count % 30) / 10),
                "entropy_score": 0.25 + ((self.tick_count % 7) * 0.05),
                "mood": "reflective" if self.tick_count % 20 == 0 else "anxious"
            }

            print(f"[FieldTrigger] 🌱 Triggering autonomous bloom at tick {self.tick_count}")
            spawn_bloom(bloom_data, pulse=pulse)  # ✅ pulse passed here
            owl_log_rebloom(bloom_data)
            animate_rebloom_lineage()
