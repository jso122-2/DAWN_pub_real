#!/usr/bin/env python3
"""
Examples of integrating DAWN GUI with different DAWN system configurations
"""

import sys
import os
import asyncio
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def example_1_basic_integration():
    """Example 1: Basic integration with existing tick engine"""
    print("Example 1: Basic Integration")
    print("-" * 40)
    
    try:
        # Import your tick engine (adjust import path as needed)
        from core.tick.tick_engine import TickEngine
        from gui.dawn_gui_integration import integrate_gui_with_tick_engine
        
        # Create or get your tick engine
        tick_engine = TickEngine()
        
        # Integrate GUI
        gui_integration = integrate_gui_with_tick_engine(tick_engine)
        
        if gui_integration:
            print("✅ GUI integrated successfully!")
            print("🎮 GUI should now be running...")
            
            # Your application continues here
            time.sleep(10)  # Run for 10 seconds as example
            
            gui_integration.shutdown()
        else:
            print("❌ GUI integration failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_dawn_central_integration():
    """Example 2: Integration with DAWNCentral system"""
    print("Example 2: DAWNCentral Integration")
    print("-" * 40)
    
    try:
        # Import DAWNCentral (adjust path as needed)
        from backend.main import DAWNCentral
        from gui.dawn_gui_integration import integrate_gui_with_tick_engine
        
        # Create DAWN Central
        dawn_central = DAWNCentral()
        
        # Get the tick engine from DAWN Central
        tick_engine = dawn_central.tick_engine
        
        # Integrate GUI
        gui_integration = integrate_gui_with_tick_engine(tick_engine)
        
        if gui_integration:
            print("✅ GUI integrated with DAWNCentral!")
            print("🎮 GUI monitoring DAWN Central systems...")
            
            # Start DAWN Central systems
            # dawn_central.start()  # Uncomment if you want to start the full system
            
            time.sleep(10)  # Example runtime
            
            gui_integration.shutdown()
        else:
            print("❌ GUI integration failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def example_3_async_system_integration():
    """Example 3: Integration with async DAWN system"""
    print("Example 3: Async System Integration")
    print("-" * 40)
    
    try:
        # Import async components
        from backend.advanced_consciousness_system import AdvancedConsciousnessSystem
        from gui.dawn_gui_integration import DAWNGuiIntegration
        
        # Create consciousness system
        consciousness = AdvancedConsciousnessSystem()
        
        # Create GUI integration
        gui_integration = DAWNGuiIntegration()
        
        # Start GUI in standalone mode (consciousness system manages its own loops)
        if gui_integration.start_standalone_gui():
            print("✅ GUI started in standalone mode")
            print("🧠 Advanced Consciousness System with GUI monitoring...")
            
            # Start consciousness system
            await consciousness.start_system()
            
            # Run for a while
            await asyncio.sleep(10)
            
            # Cleanup
            await consciousness.shutdown_system()
            gui_integration.shutdown()
        else:
            print("❌ GUI integration failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_manual_tick_loop_integration():
    """Example 4: Manual integration with custom tick loop"""
    print("Example 4: Manual Tick Loop Integration")
    print("-" * 40)
    
    try:
        from core.tick.tick_loop import TickLoop
        from core.tick.tick_engine import TickEngine
        from gui.dawn_gui_integration import integrate_gui_with_tick_engine
        
        # Create tick engine and loop
        tick_engine = TickEngine()
        tick_loop = TickLoop(tick_engine, {"tick_rate": 1.0})
        
        # Integrate GUI with the tick loop
        gui_integration = integrate_gui_with_tick_engine(tick_loop)
        
        if gui_integration:
            print("✅ GUI integrated with tick loop!")
            print("🔄 Starting tick loop with GUI monitoring...")
            
            # Start the tick loop (this will run the GUI automatically)
            # In a real scenario, you'd use asyncio.run(tick_loop.start())
            
            # Simulate running
            time.sleep(10)
            
            gui_integration.shutdown()
        else:
            print("❌ GUI integration failed")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_5_standalone_gui():
    """Example 5: Standalone GUI without DAWN system"""
    print("Example 5: Standalone GUI")
    print("-" * 40)
    
    try:
        from gui.dawn_gui_integration import start_standalone_gui
        
        # Start GUI in standalone mode
        gui_integration = start_standalone_gui()
        
        if gui_integration:
            print("✅ Standalone GUI started!")
            print("🎮 GUI running in simulation mode...")
            print("💡 This is useful for testing the GUI without DAWN systems")
            
            # Let it run for a while
            time.sleep(10)
            
            gui_integration.shutdown()
        else:
            print("❌ Failed to start standalone GUI")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_6_add_to_existing_main():
    """Example 6: Code to add to your existing main.py"""
    print("Example 6: Code for existing main.py")
    print("-" * 40)
    
    code_example = '''
# Add this to your existing DAWN main.py file:

# At the top with other imports:
from gui.dawn_gui_integration import integrate_gui_with_tick_engine

# After you create your tick engine:
# tick_engine = YourTickEngine()  # Your existing code

# Add GUI integration:
gui_integration = integrate_gui_with_tick_engine(tick_engine)
if gui_integration:
    print("✅ DAWN GUI integrated!")
else:
    print("⚠️  GUI integration failed, continuing without GUI")

# Your existing code continues...
# When shutting down, add:
# if gui_integration:
#     gui_integration.shutdown()
'''
    
    print(code_example)


def main():
    """Run all examples"""
    print("🌅 DAWN GUI Integration Examples")
    print("=" * 50)
    
    examples = [
        ("Basic Integration", example_1_basic_integration),
        ("DAWNCentral Integration", example_2_dawn_central_integration),
        ("Async System Integration", lambda: asyncio.run(example_3_async_system_integration())),
        ("Manual Tick Loop", example_4_manual_tick_loop_integration),
        ("Standalone GUI", example_5_standalone_gui),
        ("Code for main.py", example_6_add_to_existing_main)
    ]
    
    for name, example_func in examples:
        print(f"\n{'='*20}")
        print(f"Running: {name}")
        print('='*20)
        
        try:
            example_func()
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
            break
        except Exception as e:
            print(f"❌ Example failed: {e}")
        
        # Small pause between examples
        time.sleep(2)
    
    print("\n✅ All examples completed!")
    print("\n💡 To integrate GUI with your DAWN system:")
    print("   1. Import: from gui.dawn_gui_integration import integrate_gui_with_tick_engine")
    print("   2. Integrate: gui_integration = integrate_gui_with_tick_engine(your_tick_engine)")
    print("   3. Shutdown: gui_integration.shutdown()  # when done")


if __name__ == "__main__":
    main() 