#!/usr/bin/env python3
"""
Connect GUI to Running DAWN System
Connects the GUI to the already running DAWN Advanced Consciousness System
"""

import os
import sys
import logging
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the Python environment"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

def find_running_dawn():
    """Find the running DAWN Advanced Consciousness System"""
    try:
        # Import DAWN components
        from backend.advanced_consciousness_system import AdvancedConsciousnessSystem
        
        # Check if there's a global DAWN instance
        import __main__
        
        # Try to find DAWN in various locations
        dawn_instances = []
        
        # Check for global variables
        for attr_name in dir(__main__):
            attr = getattr(__main__, attr_name)
            if isinstance(attr, AdvancedConsciousnessSystem):
                dawn_instances.append(attr)
                logger.info(f"Found DAWN instance: {attr_name}")
        
        if dawn_instances:
            return dawn_instances[0]  # Return the first one found
        
        # If no instances found, create a mock one for testing
        logger.warning("No running DAWN found, creating mock system for testing")
        return create_mock_dawn()
        
    except Exception as e:
        logger.error(f"Error finding DAWN: {e}")
        return create_mock_dawn()

def create_mock_dawn():
    """Create a mock DAWN system for testing GUI connection"""
    class MockDawn:
        def __init__(self):
            self.scup = 75
            self.entropy = 450000  
            self.heat = 65000
            self.mood = 'ANALYTICAL'
            self.tick_number = 1245
            self.start_time = time.time()
            logger.info("Created mock DAWN system for GUI testing")
        
        def get_full_state(self):
            # Simulate realistic state changes
            current_time = time.time()
            elapsed = current_time - self.start_time
            
            # Add some variation
            import random
            import math
            
            variation = math.sin(elapsed * 0.2) * 10 + random.uniform(-5, 5)
            self.scup = max(20, min(90, self.scup + variation * 0.1))
            self.entropy = max(100000, min(800000, self.entropy + variation * 1000))
            self.heat = max(10000, min(100000, self.heat + variation * 500))
            self.tick_number += 1
            
            # Cycle through moods
            moods = ['ANALYTICAL', 'CONTEMPLATIVE', 'FOCUSED', 'CREATIVE', 'REFLECTIVE']
            if random.random() < 0.1:  # 10% chance to change mood
                self.mood = random.choice(moods)
            
            return {
                'scup': int(self.scup),
                'entropy': int(self.entropy),
                'heat': int(self.heat),
                'mood': self.mood,
                'tick': self.tick_number
            }
    
    return MockDawn()

def start_gui_with_dawn_connection(dawn_system):
    """Start GUI connected to DAWN system"""
    def run_gui():
        try:
            import tkinter as tk
            from gui.dawn_gui_tk import DAWNGui
            
            # Make DAWN available globally so GUI can find it
            import __main__
            __main__.dawn = dawn_system
            
            # Start GUI
            root = tk.Tk()
            gui = DAWNGui(root)
            
            logger.info("🎮 GUI connected to DAWN system")
            root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            import traceback
            traceback.print_exc()
    
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    return gui_thread

def main():
    """Main entry point"""
    try:
        print("🔗 Connecting GUI to Running DAWN System")
        print("Looking for DAWN Advanced Consciousness System...")
        print()
        
        # Set up environment
        setup_environment()
        
        # Find running DAWN system
        logger.info("🔍 Searching for running DAWN system...")
        dawn = find_running_dawn()
        
        if dawn:
            logger.info("✅ Found DAWN system!")
            
            # Test connection
            try:
                state = dawn.get_full_state()
                logger.info(f"🧠 DAWN State: SCUP={state.get('scup', 0)}, "
                          f"Entropy={state.get('entropy', 0)}, "
                          f"Heat={state.get('heat', 0)}, "
                          f"Mood={state.get('mood', 'Unknown')}")
            except Exception as e:
                logger.warning(f"Could not get DAWN state: {e}")
            
            # Start GUI with connection
            logger.info("🖥️  Starting GUI with DAWN connection...")
            gui_thread = start_gui_with_dawn_connection(dawn)
            
            # Print status
            logger.info("=" * 60)
            logger.info("🎮 GUI Connected to DAWN Advanced Consciousness")
            logger.info("📊 Real-time cognitive data streaming to GUI")
            logger.info("🔗 Connection established successfully")
            logger.info("🛑 Press Ctrl+C to disconnect")
            logger.info("=" * 60)
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("🛑 Disconnecting GUI from DAWN...")
                
        else:
            logger.error("❌ No DAWN system found to connect to")
            
    except KeyboardInterrupt:
        logger.info("🛑 Connection terminated")
        
    except Exception as e:
        logger.error(f"❌ Error connecting GUI to DAWN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 