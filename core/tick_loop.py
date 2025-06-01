from tick_emitter import emit_tick
from bloom_writer import write_bloom
from system_state import pulse  # Global PulseHeat instance
from owl import owl_comment

# Simulate 5 blooms per tick
def simulate_tick():
    tick = emit_tick()

    for i in range(5):
        # Simulated semantic pressure
        pressure = 0.2 + i * 0.1
        activity = 0.5 + i * 0.05

        # Update pulse state
        pulse.current_pressure = pressure
        pulse.activity_level = activity
        pulse.tick_count += 1

        # Memory log
        pulse.memory_log.append({
            "tick": pulse.tick_count,
            "activity": pulse.activity_level,
            "pressure": pulse.current_pressure,
            "interval": pulse.current_interval
        })

        # Calculate mood from average pressure (recalculated every bloom)
        avg_pressure = pulse.average_pressure(window=5)
        if avg_pressure > 0.4:
            pulse.current_interval *= 0.95  # Breath shortens
            mood = "stressed"
        elif avg_pressure < 0.2:
            pulse.current_interval *= 1.02  # Breath lengthens
            mood = "calm"
        else:
            mood = "neutral"

        # Simulated bloom
        write_bloom(
            seed=f"whale-00{i}",
            mood=mood,
            tick=tick,
            semantic_pressure=pressure,
            seed_coord=[i, tick % 100],
            mood_prev="calm" if i % 2 == 0 else "anxious"
        )
        if pulse.tick_count % 10 == 0:
            owl_comment(pulse.memory_log, pulse.tick_count)

        field_state = {
            "mood": mood,
            "pressure": pulse.current_pressure,
            "activity": pulse.activity_level
        }

        sigils.evolve_classes(field_state)

if __name__ == "__main__":
    simulate_tick()
