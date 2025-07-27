#!/usr/bin/env python3
"""
DAWN Runner - Working Version
=============================
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def run():
    print("🌅 DAWN Starting...")
    print("=" * 50)
    
    from core.dawn_registry import consciousness
    
    # Summon all components
    components = {
        'pulse': consciousness.summon('pulse_heat'),
        'bloom': consciousness.summon('bloom_engine'),
        'owl': consciousness.summon('owl_system'),
        'sigil': consciousness.summon('sigil_processor'),
    }
    
    print("\n✨ Components awakened:")
    for name, comp in components.items():
        print(f"  - {name}: {type(comp).__name__}")
    
    # Simple interaction
    print("\n💫 DAWN is running. Commands: pulse, bloom, reflect, status, exit")
    
    while True:
        try:
            cmd = input("\ndawn> ").strip().lower()
            
            if cmd == 'exit':
                break
            elif cmd == 'pulse':
                if hasattr(components['pulse'], 'get_heat'):
                    print(f"Heat: {components['pulse'].get_heat()}")
            elif cmd == 'bloom':
                if hasattr(components['bloom'], 'spawn_bloom'):
                    bloom = components['bloom'].spawn_bloom()
                    print(f"Spawned: {bloom}")
            elif cmd == 'reflect':
                if hasattr(components['owl'], 'reflect'):
                    reflection = components['owl'].reflect({'data': 'test'})
                    print(f"Reflection: {reflection}")
            elif cmd == 'status':
                memories = consciousness.reflect_on_components()
                for essence, info in memories.items():
                    if info['awakened']:
                        print(f"  {essence}: Active")
            else:
                print("Unknown command")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n💤 DAWN shutting down...")

if __name__ == "__main__":
    run()
