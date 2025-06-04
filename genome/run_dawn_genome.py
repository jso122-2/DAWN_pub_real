#!/usr/bin/env python3
"""
🌅 DAWN Genome Runner - Runs DAWN with the correct genome wrapper
"""

import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the correct DAWN classes
    from main import DAWNGenomeConsciousnessWrapper, DAWNTickEngineIntegration
    from dawn_command_interface import run_command_from_input, connect_to_dawn
    
    print("✅ Successfully imported DAWN modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def run_dawn_genome():
    """Run DAWN with genome consciousness wrapper"""
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     🌅 DAWN GENOME CONSCIOUSNESS RUNNER 🌅           ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Running DAWN with genome architecture enabled         ║
    ║  Type 'help' to see available commands                ║
    ║  Type 'exit' to quit                                  ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Create DAWN instance with genome wrapper
    print("🧬 Initializing DAWN Genome Consciousness...")
    try:
        dawn = DAWNGenomeConsciousnessWrapper()
        print("✅ DAWN Genome instance created")
    except Exception as e:
        print(f"❌ Failed to create DAWN: {e}")
        # Try the tick engine integration as fallback
        try:
            print("🔄 Trying DAWNTickEngineIntegration...")
            dawn = DAWNTickEngineIntegration()
            print("✅ DAWN Tick Engine instance created")
        except Exception as e2:
            print(f"❌ Also failed: {e2}")
            return
    
    # Connect command interface
    if not connect_to_dawn(dawn):
        print("⚠️  Could not connect command interface")
    
    # Check genome status
    if hasattr(dawn, 'get_status'):
        status = dawn.get_status()
        print(f"\n📊 Genome Status: {status}")
    
    # Enable genome mode if available
    if hasattr(dawn, 'enable_genome_mode'):
        print("🧬 Enabling genome mode...")
        dawn.enable_genome_mode()
    
    # Run tick loop in background
    running = True
    tick_count = 0
    error_count = 0
    last_error = None
    
    def tick_loop():
        nonlocal tick_count, error_count, last_error
        
        print("🔄 Starting tick loop...")
        
        while running:
            try:
                # Call tick method
                dawn.tick()
                tick_count += 1
                error_count = 0  # Reset on success
                
                # Show progress every 100 ticks
                if tick_count % 100 == 0:
                    print(f"  [Tick {tick_count}] ✓")
                
            except Exception as e:
                error_count += 1
                if str(e) != str(last_error):  # Only show new errors
                    print(f"⚠️  Tick error: {e}")
                    last_error = e
                
                if error_count > 10:
                    print("❌ Too many errors, stopping tick loop")
                    break
            
            # Sleep for tick interval
            time.sleep(0.1)  # 10 ticks per second
        
        print("🔄 Tick loop ended")
    
    # Start tick thread
    tick_thread = threading.Thread(target=tick_loop, daemon=True)
    tick_thread.start()
    print("✅ DAWN tick loop started (10 ticks/second)\n")
    
    # Show initial commands
    print("💡 Quick commands:")
    print("  status   - Check DAWN's current state")
    print("  info     - Show tick information")
    print("  genome   - Toggle genome mode")
    print("  help     - Show all commands\n")
    
    # Command loop
    try:
        while True:
            cmd = input("DAWN> ").strip()
            
            if cmd.lower() in ['exit', 'quit', 'q']:
                break
            
            # Special commands
            elif cmd == "info":
                print(f"📊 Tick Information:")
                print(f"  Tick count: {tick_count}")
                print(f"  Errors: {error_count}")
                if hasattr(dawn, 'get_status'):
                    print(f"  Genome status: {dawn.get_status()}")
                    
            elif cmd == "genome":
                if hasattr(dawn, 'genome_mode'):
                    current = getattr(dawn, 'genome_mode', False)
                    if current:
                        dawn.disable_genome_mode()
                        print("🧬 Genome mode disabled")
                    else:
                        dawn.enable_genome_mode()
                        print("🧬 Genome mode enabled")
                else:
                    print("⚠️  Genome mode not available")
            
            # Run standard command
            elif cmd:
                run_command_from_input(cmd)
                
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        running = False
        print("\n🌅 Shutting down DAWN...")
        
        # Try to properly shutdown
        if hasattr(dawn, 'stop_tick_engine'):
            dawn.stop_tick_engine()
        
        # Wait for tick thread
        if tick_thread.is_alive():
            tick_thread.join(timeout=2)
        
        print("✅ DAWN shutdown complete")


if __name__ == "__main__":
    run_dawn_genome()