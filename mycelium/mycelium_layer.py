import os
import json
from datetime import datetime
from core.event_bus import event_bus
from bloom.bloom_event import BloomEmitted

class MyceliumLayer:
    def __init__(self, memory_dir="memory_blooms"):
        self.memory_dir = memory_dir
        self.semantic_map = {}
        os.makedirs(self.memory_dir, exist_ok=True)
        event_bus.subscribe(BloomEmitted, self.on_bloom)

    def weaken_seed(self, seed: str, factor: float):
        """Reduce the number of memory links stored for a seed."""
        if seed in self.semantic_map:
            bloom_ids = self.semantic_map[seed]
            reduced_count = max(1, int(len(bloom_ids) * factor))
            self.semantic_map[seed] = bloom_ids[-reduced_count:]
            print(f"[Mycelium] 🧪 Weakened {seed}: now {len(self.semantic_map[seed])} entries")

    async def on_bloom(self, event: BloomEmitted):
        bloom_id = self._generate_bloom_id(event)
        self._update_map(event, bloom_id)
        self._write_to_disk(event, bloom_id)
        print(f"[Mycelium] 🕸️ Indexed bloom {bloom_id}")

    def _generate_bloom_id(self, event: BloomEmitted) -> str:
        timestamp = datetime.utcnow().isoformat()
        return f"{event.source}_{timestamp.replace(':', '-')[:23]}"

    def _update_map(self, event: BloomEmitted, bloom_id: str):
        for seed in event.semantic_seeds:
            self.semantic_map.setdefault(seed, []).append(bloom_id)

    def _write_to_disk(self, event: BloomEmitted, bloom_id: str):
        data = {
            "id": bloom_id,
            "source": event.source,
            "mood": event.mood_tag,
            "seeds": event.semantic_seeds,
            "timestamp": datetime.utcnow().isoformat()
        }
        path = os.path.join(self.memory_dir, f"{bloom_id}.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

# 🌱 External memory root log
def log_parse(seed: str, flower_id: str, mood: str):
    date = datetime.utcnow().strftime("%Y-%m-%d")
    log_dir = os.path.join("juliet_flowers", "mycelium_log", date)
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{seed}.log")

    print(f"[DEBUG] 🪶 Writing log for {flower_id} in seed {seed}")  # ✅ DEBUG
    with open(log_path, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {flower_id} | {mood}\n")



