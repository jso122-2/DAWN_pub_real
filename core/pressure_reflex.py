# File Path: /src/core/schema/pressure_reflex.py

"""
Connects pulse zone states to schema-wide behaviors:
- 🟢 calm → suppression
- 🟡 active → bloom rate modulation
- 🔴 surge → emotional override
"""

from core.emotional_override import apply_emotional_override
from bloom.spawn_bloom import adjust_bloom_factor_by_nutrient
from schema.schema_flags import SchemaState  # Optional central flag handler
from bloom.bloom_controls import suppress_all_blooms, modulate_bloom_rate
from mycelium.nutrient_logger import adjust_seed_soot
from schema.schema_health_index import get_schema_entropy


def apply_pressure_reflex(pulse_zone, bloom, schema_state: SchemaState, schema=None):
    """
    Apply schema adjustments based on pulse zone.
    Hybrid version using both schema_state and schema-level behaviors.
    """

    # 1. Handling calm zone (🟢 calm)
    if pulse_zone == "🟢 calm":
        schema_state.suppression_active = True
        schema_state.override_trigger = None

        # Optional: call schema-level suppression
        if schema:
            schema.suppress(mode="entropy", threshold=0.7)
            schema.log("🛑 Calm zone → suppressing unstable blooms")

        print("[PressureReflex] 🧘 Suppression engaged (calm)")

    # 2. Handling active zone (🟡 active)
    elif pulse_zone == "🟡 active":
        schema_state.suppression_active = False
        schema_state.override_trigger = None

        # Modulate the bloom factor based on nutrient flow ("attention" nutrient for example)
        bloom["bloom_factor"] = adjust_bloom_factor_by_nutrient(bloom, nutrient="attention")

        # Optional: Modulate bloom rate at the schema level
        if schema:
            schema.modulate_bloom_rate(0.75)  # Adjust rate to 75%
            schema.log("⚙️ Active zone → bloom rate modulated to 75%")

        print("[PressureReflex] 🌱 Bloom rate boosted (active)")

    # 3. Handling surge zone (🔴 surge)
    elif pulse_zone == "🔴 surge":
        schema_state.suppression_active = False
        
        # Apply emotional override (focus in surge zone)
        result = apply_emotional_override(pulse_zone, bloom)
        schema_state.override_trigger = result

        # Optional: Override schema-level emotion based on surge
        if schema:
            schema.override_emotion("focused")
            schema.log(f"🔥 Surge zone → overriding mood to 'focused' | {result}")

        print(f"[PressureReflex] 🔥 {result} (surge)")

    # 4. Handling unknown pulse zone states
    else:
        print("[PressureReflex] ❓ Unknown pulse zone state")
        if schema:
            schema.log(f"❓ Unknown pulse zone: {pulse_zone}")

    return schema_state
