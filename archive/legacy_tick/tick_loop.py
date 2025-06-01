from tick_emitter import emit_tick
from bloom_writer import write_bloom
from system_state import pulse
from owl import owl_comment
from schema.scup_loop import (
    calculate_SCUP,
    get_scup_zone,
    reinforce_scup_weights,
    print_scup_summary,
    plot_scup_heatmap
)

def simulate_tick():
    tick = emit_tick()

    for i in range(5):
        pressure = 0.2 + i * 0.1
        activity = 0.5 + i * 0.05

        pulse.current_pressure = pressure
        pulse.activity_level = activity
        pulse.tick_count += 1

        pulse.memory_log.append({
            "tick": pulse.tick_count,
            "activity": pulse.activity_level,
            "pressure": pulse.current_pressure,
            "interval": pulse.current_interval
        })

        avg_pressure = pulse.average_pressure(window=5)
        if avg_pressure > 0.4:
            pulse.current_interval *= 0.95
            mood = "stressed"
        elif avg_pressure < 0.2:
            pulse.current_interval *= 1.02
            mood = "calm"
        else:
            mood = "neutral"

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

        # --- SCUP variables ---
        delta_vector = 0.2 + (i * 0.05)         # mock semantic drift
        pulse_pressure = pressure
        drift_variance = abs(activity - 0.6)    # mock mood instability

        scup = calculate_SCUP(delta_vector, pulse_pressure, drift_variance)

        if pulse.tick_count % 25 == 0:
            print_scup_summary()
            reinforce_scup_weights(scup, feedback="positive" if scup > 0.75 else "negative")

        if pulse.tick_count % 100 == 0:
            plot_scup_heatmap()

if __name__ == "__main__":
    simulate_tick()
