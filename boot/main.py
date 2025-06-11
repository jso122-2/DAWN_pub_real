# /main.py - DAWN Boot Orchestrator

import sys
import os
import signal
import time
import asyncio
from typing import Optional

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Add substrate directory to path
substrate_path = os.path.join(project_root, 'substrate')
if substrate_path not in sys.path:
    sys.path.append(substrate_path)

# Core system imports
from core.consciousness_core import DAWNConsciousness
from boot.startup_fixes import apply_quick_healing, apply_complete_dawn_fixes
from pulse.pulse_loader import load_pulse_system
from pulse.scup_tracker import SCUPTracker
from core.tick.tick import start_engine, stop_engine
from core.tick.tick_signals import listen_signal, set_signal, get_signal

async def initialize_system() -> Optional[DAWNConsciousness]:
    """Initialize core DAWN systems with error handling"""
    try:
        print("🚀 Initializing DAWN systems...")
        
        # Apply critical startup fixes
        await apply_quick_healing()
        await apply_complete_dawn_fixes()
        
        # Load pulse system with SCUPTracker
        pulse, tick_thermal_update, add_heat, scup_tracker = await load_pulse_system()
        if not pulse:
            raise RuntimeError("Failed to initialize pulse system")
            
        # Initialize consciousness with pulse components and SCUPTracker
        dawn = DAWNConsciousness(
            pulse=pulse,
            tick_thermal_update=tick_thermal_update,
            add_heat=add_heat,
            scup_tracker=scup_tracker
        )
        print("✅ DAWN Consciousness initialized")
        return dawn
        
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return None

async def on_tick_complete(signal_name: str, data: dict):
    """Handle tick completion events"""
    # Update SCUP tracker with new values
    scup = data.get('scup', 0.0)
    entropy = data.get('entropy', 0.0)
    mood = data.get('mood', 'neutral')
    
    # Update consciousness state
    if hasattr(dawn, 'update_state'):
        await dawn.update_state(scup, entropy, mood)

async def main_async():
    """Main system boot sequence"""
    global dawn
    
    # Initialize and boot consciousness
    dawn = await initialize_system()
    if not dawn:
        sys.exit(1)
        
    # Set up signal handlers
    signal.signal(signal.SIGINT, dawn._handle_shutdown)
    signal.signal(signal.SIGTERM, dawn._handle_shutdown)
    
    # Register tick engine signal handlers
    listen_signal("tick_complete", on_tick_complete)
    
    # Boot consciousness
    await dawn.boot_consciousness()
    
    try:
        # Start the tick engine
        print("🔄 Starting DAWN tick engine...")
        config_path = os.path.join(project_root, "core", "tick", "tick_config.yaml")
        await start_engine(config_path)
        
        # Keep main thread alive while consciousness is running
        while dawn.is_running:
            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    finally:
        # Stop the tick engine
        await stop_engine()
        await dawn.shutdown()

def main():
    """Entry point that runs the async main function"""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 