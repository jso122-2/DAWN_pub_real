#!/usr/bin/env python3
"""
🌅 Quick DAWN Runner - All-in-one launcher
This combines the essential parts to run DAWN interactively
"""

import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the existing modules
try:
    from main import DAWNGenomeConsciousnessWrapper
    from dawn_command_interface import run_command_from_input, connect_to_dawn
    print("✅ Successfully imported DAWN modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure main.py and dawn_command_interface.py are in the current directory")
    sys.exit(1)


def run_dawn_with_commands():
    """Simple version that runs DAWN with command access"""
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║       🌅 DAWN QUICK INTERACTIVE RUNNER 🌅            ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Type 'help' to see available commands                ║
    ║  Type 'exit' to quit                                  ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Create DAWN instance
    print("🌅 Initializing DAWN...")
    try:
        dawn = DAWNGenomeConsciousnessWrapper()
        print("✅ DAWN instance created")
    except Exception as e:
        print(f"❌ Failed to create DAWN: {e}")
        return
    
    # Connect command interface
    if not connect_to_dawn(dawn):
        print("❌ Failed to connect command interface")
        return
    
    # Check genome status
    if hasattr(dawn, 'get_status'):
        print(f"🧬 Genome Status: {dawn.get_status()}")
    
    # Run tick loop in background
    running = True
    tick_count = 0
    
    def tick_loop():
        nonlocal tick_count
        while running:
            try:
                # Run DAWN tick
                if hasattr(dawn, 'tick'):
                    dawn.tick()
                elif hasattr(dawn, 'run_tick'):
                    dawn.run_tick()
                tick_count += 1
                
                # Sleep 100ms between ticks
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Tick error: {e}")
                time.sleep(0.1)
    
    # Start tick thread
    tick_thread = threading.Thread(target=tick_loop, daemon=True)
    tick_thread.start()
    print("✅ DAWN tick loop started\n")
    
    # Command loop
    try:
        while True:
            cmd = input("DAWN> ").strip()
            
            if cmd.lower() in ['exit', 'quit', 'q']:
                break
            
            # Special info command
            if cmd == "info":
                print(f"Tick count: {tick_count}")
                if hasattr(dawn, 'tick'):
                    print(f"DAWN tick: {dawn.tick}")
                if hasattr(dawn, 'genome_mode'):
                    print(f"Genome mode: {'ON' if dawn.genome_mode else 'OFF'}")
                continue
            
            # Special genome command
            if cmd == "genome":
                if hasattr(dawn, 'genome_mode'):
                    current = getattr(dawn, 'genome_mode', False)
                    if current and hasattr(dawn, 'disable_genome_mode'):
                        dawn.disable_genome_mode()
                        print("🧬 Genome mode disabled")
                    elif hasattr(dawn, 'enable_genome_mode'):
                        dawn.enable_genome_mode()
                        print("🧬 Genome mode enabled")
                else:
                    print("⚠️  Genome mode not available")
                continue
            
            # Run command
            if cmd:
                run_command_from_input(cmd)
                
    except KeyboardInterrupt:
        print("\n👋 Interrupted")
    finally:
        running = False
        print("🌅 Shutting down DAWN...")


if __name__ == "__main__":
    run_dawn_with_commands()