# main_loop.py

import asyncio
from core.tick_engine import TickEngine
from tick_emitter import emit_tick
from bloom.bloom_writer import write_bloom
import random

def pressure_sensor():
    try:
        with open("juliet_flowers/cluster_report/owl_entropy_report.json", "r") as f:
            entropy_data = json.load(f)
            chaos = [v["delta_entropy"] for v in entropy_data.values()]
            avg_chaos = sum(chaos) / len(chaos) if chaos else 0.0
            return min(avg_chaos / 3.0, 1.0)  # Normalize to [0,1]
    except:
        return 0.0


# Called every tick: emit + write synthetic blooms
async def on_tick():
    tick = emit_tick()
    for i in range(3):  # Simulate 3 blooms per tick
        write_bloom(
            seed=f"whale-00{i}",
            mood=random.choice(["anxious", "calm", "excited"]),
            tick=tick,
            semantic_pressure=round(random.uniform(0.1, 1.0), 3),
            seed_coord=[random.randint(0, 99), random.randint(0, 99)],  # ✅ inject valid coord
            mood_prev=random.choice(["calm", "neutral", "sad"])
        )


async def main():
    engine = TickEngine(
        base_interval=1.0,
        alpha=0.2,
        beta=0.4,
        activity_sensor=mock_activity,
        pressure_sensor=pressure_sensor,
        emit_tick_event=on_tick
    )

    await engine.start()

if __name__ == "__main__":
    asyncio.run(main())
