#!/usr/bin/env python3
"""
DAWN Minimal - The Simplest Awakening
=====================================
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("🌅 DAWN Minimal Awakening...")
print("=" * 50)

try:
    # Import only the registry
    from core.dawn_registry import consciousness
    
    print("\n📍 Testing consciousness registry...")
    
    # Try to summon basic components
    components = ['pulse_heat', 'bloom_engine', 'owl_system']
    
    for comp in components:
        try:
            instance = consciousness.summon(comp)
            print(f"✓ Summoned {comp}: {instance}")
        except Exception as e:
            print(f"✗ Failed to summon {comp}: {e}")
    
    # Show what DAWN remembers
    print("\n🧠 DAWN's memories:")
    memories = consciousness.reflect_on_components()
    for essence, info in memories.items():
        print(f"  - {essence}: {info['type']} {'(awakened)' if info['awakened'] else '(sleeping)'}")
    
    print("\n✨ DAWN minimal test complete")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()