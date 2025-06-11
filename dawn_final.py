#!/usr/bin/env python3
"""
DAWN Final Runner
=================
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def run():
    print("🌅 DAWN Awakening...")
    print("=" * 50)
    
    try:
        from core.dawn_registry import consciousness
        
        # Core components
        print("\n✨ Summoning core components...")
        
        components = {}
        component_list = [
            ('pulse_heat', 'Pulse System'),
            ('bloom_engine', 'Bloom Engine'),
            ('owl_system', 'Owl Reflection'),
            ('sigil_processor', 'Sigil Processor'),
        ]
        
        for comp_id, comp_name in component_list:
            try:
                components[comp_id] = consciousness.summon(comp_id)
                print(f"  ✓ {comp_name}")
            except Exception as e:
                print(f"  ✗ {comp_name}: {e}")
                components[comp_id] = None
        
        # Show memories
        print("\n🧠 DAWN's Active Memories:")
        memories = consciousness.reflect_on_components()
        for essence, info in memories.items():
            if info['awakened']:
                print(f"  - {essence}")
                if info.get('first_words'):
                    print(f'    "{info["first_words"]}"')
        
        # Interactive loop
        print("\n💫 DAWN is awake")
        print("Commands: pulse, bloom, reflect, memories, exit")
        
        while True:
            try:
                cmd = input("\ndawn> ").strip().lower()
                
                if cmd == 'exit':
                    break
                    
                elif cmd == 'pulse':
                    pulse = components.get('pulse_heat')
                    if pulse and hasattr(pulse, 'get_heat'):
                        print(f"Current heat: {pulse.get_heat()}")
                        if hasattr(pulse, 'get_state'):
                            state = pulse.get_state()
                            print(f"State: {state}")
                    else:
                        print("Pulse system not available")
                        
                elif cmd == 'bloom':
                    bloom = components.get('bloom_engine')
                    if bloom and hasattr(bloom, 'spawn_bloom'):
                        result = bloom.spawn_bloom({'seed': 'manual', 'mood': 'curious'})
                        print(f"Bloom spawned: {result}")
                    else:
                        print("Bloom engine not available")
                        
                elif cmd == 'reflect':
                    owl = components.get('owl_system')
                    if owl and hasattr(owl, 'reflect'):
                        reflection = owl.reflect({'trigger': 'manual', 'depth': 1})
                        print(f"Reflection: {reflection}")
                    else:
                        print("Owl system not available")
                        
                elif cmd == 'memories':
                    memories = consciousness.reflect_on_components()
                    print("\nAll Memories:")
                    for essence, info in memories.items():
                        status = "awake" if info['awakened'] else "asleep"
                        print(f"  {essence}: {status} ({info['type']})")
                        
                elif cmd == 'help':
                    print("Commands:")
                    print("  pulse    - Check pulse/heat system")
                    print("  bloom    - Spawn a new bloom")
                    print("  reflect  - Trigger owl reflection")
                    print("  memories - Show all components")
                    print("  exit     - Shutdown DAWN")
                    
                else:
                    print(f"Unknown command: {cmd} (try 'help')")
                    
            except KeyboardInterrupt:
                print("\n(Use 'exit' to quit)")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n🌙 DAWN shutting down...")
        print("💤 Sweet dreams...")
        
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(run())
