from core.event_bus import event_bus, TickEvent
from core.system_state import pulse
import random

print("✅ tick_listener imported and subscribing")


def compute_drift():
    return round(random.uniform(0.01, 0.2), 3)

def mood_to_heat(mood):
    mapping = {
        "anxious": 0.3,
        "excited": 0.2,
        "curious": 0.1,
        "reflective": 0.05,
        "calm": -0.2
    }
    return mapping.get(mood.lower(), 0.0)

def apply_mood_chemistry(mood="curious"):
    heat = mood_to_heat(mood)
    pulse.add_heat(heat)
    print(f"[MoodChem] {mood} → Δheat {heat:+.2f}")

async def on_tick(event):
    
    import random
    pulse.tick_count += 1
    pulse.current_pressure = random.uniform(0.1, 0.6)
    pulse.activity_level = random.uniform(0.3, 0.9)
    pulse.current_interval = random.uniform(0.5, 1.2)
    drift = random.uniform(0.01, 0.2)
    pulse.add_heat(drift)
    print(f"[PulseHeat] +{drift:.2f} from drift")
    pulse.memory_log.append({
        "tick": pulse.tick_count,
        "activity": pulse.activity_level,
        "pressure": pulse.current_pressure,
        "interval": pulse.current_interval
    })

    print(f"[MemoryLog] ✅ Appended tick {pulse.tick_count}")


    print(f"[PulseHeat] +{drift:.2f} from drift")
    apply_mood_chemistry("curious")

print("📡 Subscribing to TickEvent → on_tick")
event_bus.subscribe(TickEvent, on_tick)

