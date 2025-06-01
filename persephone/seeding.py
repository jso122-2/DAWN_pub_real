from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
import random
from bloom.spawn_bloom import spawn_bloom
from mood.current_state import get_global_mood

async def seed_whisper():
    """
    Whisper rebloom cues based on mood + pressure.
    Probabilistic rebloom when schema is calm and mood is stable.
    """
    print("[Persephone] 🌱 Evaluating rebloom whisper conditions...")

    mood = get_global_mood()
    pulse = PulseHeat()
    pressure_zone = pulse.classify()
    
    # Conditions for whisper
    if pressure_zone != "🟢 calm":
        return

    whisper_chance = {
        "joyful": 0.4,
        "neutral": 0.2,
        "tired": 0.1
    }.get(mood, 0.05)

    if random.random() < whisper_chance:
        bloom_data = {
            "seed_id": f"whisper-{datetime.now().strftime('%H%M%S')}",
            "lineage_depth": 0,
            "entropy_score": round(random.uniform(0.1, 0.5), 2),
            "bloom_factor": round(random.uniform(0.5, 1.2), 2),
            "mood": mood
        }
        print(f"[Persephone] 🌾 Whispering bloom: {bloom_data['seed_id']}")
        spawn_bloom(bloom_data)
