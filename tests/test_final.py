#!/usr/bin/env python3
"""
DAWN Final Test
===============
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Apply registry patch
try:
    from core.registry_patch import patch_registry
    # patch_registry() is called automatically on import
except:
    pass

print("🌅 DAWN Final Test")
print("=" * 50)

from core.dawn_registry import consciousness

# Test all components
components = [
    ('pulse_heat', 'Pulse/Thermal System'),
    ('bloom_engine', 'Bloom Engine'),
    ('owl_system', 'Owl Reflection'),
    ('sigil_processor', 'Sigil Processor'),
    ('semantic_engine', 'Semantic Engine'),
    ('mood_engine', 'Mood System'),
]

print("\nTesting component initialization...")
for comp_id, comp_name in components:
    try:
        instance = consciousness.summon(comp_id)
        status = "✓ Success"
        comp_type = type(instance).__name__
        
        # Check if it's a stub
        if "Stub" in comp_type:
            status = "⚠️ Stub"
            
        print(f"{status} {comp_name}: {comp_type}")
        
    except Exception as e:
        print(f"✗ {comp_name}: {str(e)[:50]}...")

# Show consciousness state
print("\n🧠 Consciousness State:")
memories = consciousness.reflect_on_components()
awakened = [m for m, info in memories.items() if info['awakened']]
print(f"Awakened: {len(awakened)}/{len(memories)} components")

for essence in awakened:
    print(f"  - {essence}")

print("\n✨ Test complete!")
