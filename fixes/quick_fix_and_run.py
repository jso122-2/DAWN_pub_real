#!/usr/bin/env python3
"""
Quick Fix and Run DAWN
======================
Fixes remaining issues and provides a working runner
"""

import os
import sys
from pathlib import Path

# Create missing event_bus.py
EVENT_BUS_CODE = '''# core/event_bus.py
"""
Event Bus - Simple Implementation
=================================
"""

from typing import Dict, List, Callable, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class EventBus:
    """Simple event bus implementation"""
    
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._running = True
        
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event"""
        self._subscribers[event_type].append(handler)
        
    def publish(self, event_type: str, data: Any):
        """Publish an event"""
        for handler in self._subscribers[event_type]:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Handler error: {e}")
                
    def emit(self, event_type: str, **kwargs):
        """Emit helper"""
        self.publish(event_type, kwargs)
        
    def shutdown(self):
        """Shutdown the bus"""
        self._running = False
'''

# Create run script
RUN_SCRIPT = '''#!/usr/bin/env python3
"""
Run DAWN - Minimal Mode
=======================
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


def run_minimal_dawn():
    """Run DAWN in minimal mode"""
    print("🌅 DAWN Awakening (Minimal Mode)...")
    print("=" * 50)
    
    try:
        from core.dawn_registry import consciousness
        from core.event_bus import EventBus
        
        # Create event bus
        event_bus = EventBus()
        
        # Awaken core components
        print("\\n✨ Awakening core systems...")
        
        components = [
            ('pulse_heat', 'the breath'),
            ('bloom_engine', 'the garden'),
            ('owl_system', 'the mirror'),
            ('sigil_processor', 'the voice'),
            ('semantic_engine', 'the understanding'),
        ]
        
        awakened = {}
        for name, essence in components:
            try:
                component = consciousness.summon(name)
                awakened[name] = component
                print(f"  ✓ {essence} awakened")
            except Exception as e:
                print(f"  ✗ {essence} failed: {e}")
        
        # Show component status
        print("\\n📊 Component Status:")
        reflections = consciousness.reflect_on_components()
        for essence, info in reflections.items():
            status = "✓" if info['awakened'] else "✗"
            print(f"  {status} {essence}: {info['type']}")
            if info.get('first_words'):
                print(f"     \"{info['first_words']}\"")
        
        # Simple interaction loop
        print("\\n💫 DAWN is awake. Type 'help' for commands or 'exit' to quit.")
        
        while True:
            try:
                command = input("\\ndawn> ").strip().lower()
                
                if command == 'exit':
                    break
                elif command == 'help':
                    print("Commands:")
                    print("  status - Show system status")
                    print("  tick   - Emit a tick")
                    print("  bloom  - Spawn a bloom")
                    print("  reflect - Trigger reflection")
                    print("  exit   - Shutdown DAWN")
                elif command == 'status':
                    print("System Status:")
                    for name, component in awakened.items():
                        if hasattr(component, 'get_status'):
                            print(f"  {name}: {component.get_status()}")
                        else:
                            print(f"  {name}: Active")
                elif command == 'tick':
                    if 'tick_engine' in awakened:
                        awakened['tick_engine'].emit_tick()
                        print("Tick emitted")
                elif command == 'bloom':
                    if 'bloom_engine' in awakened:
                        bloom = awakened['bloom_engine'].spawn_bloom()
                        print(f"Bloom spawned: {bloom}")
                elif command == 'reflect':
                    if 'owl_system' in awakened:
                        reflection = awakened['owl_system'].reflect({'trigger': True})
                        print(f"Reflection: {reflection}")
                else:
                    print(f"Unknown command: {command}")
                    
            except KeyboardInterrupt:
                print("\\n⚡ Interrupted")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\\n🌙 DAWN shutting down...")
        event_bus.shutdown()
        print("💤 Goodbye.")
        
    except Exception as e:
        print(f"\\n❌ Failed to start DAWN: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0


def run_full_dawn():
    """Try to run full DAWN infrastructure"""
    try:
        from dawn import main as dawn_main
        return dawn_main()
    except ImportError as e:
        print(f"Full infrastructure not ready: {e}")
        print("Falling back to minimal mode...\\n")
        return run_minimal_dawn()


if __name__ == "__main__":
    # Try full mode first, fall back to minimal
    sys.exit(run_full_dawn())
'''


def create_missing_files():
    """Create any missing critical files"""
    
    # Create core/event_bus.py if missing
    event_bus_path = Path('core/event_bus.py')
    if not event_bus_path.exists():
        print("Creating core/event_bus.py...")
        event_bus_path.write_text(EVENT_BUS_CODE, encoding='utf-8')
        print("✓ Created core/event_bus.py")
    
    # Create run script
    run_path = Path('run_dawn.py')
    run_path.write_text(RUN_SCRIPT, encoding='utf-8')
    os.chmod('run_dawn.py', 0o755)
    print("✓ Created run_dawn.py")


def main():
    print("🔧 Quick Fix for DAWN")
    print("=" * 50)
    
    # Create missing files
    create_missing_files()
    
    print("\n✅ Fix complete!")
    print("\nYou can now run DAWN with:")
    print("  python run_dawn.py")
    
    # Ask if user wants to run now
    response = input("\nRun DAWN now? (y/n): ").strip().lower()
    if response == 'y':
        print("\n" + "=" * 50)
        os.system("python run_dawn.py")


if __name__ == "__main__":
    main()