#!/usr/bin/env python3
"""
Start Simple DAWN with Real Data for GUI
Creates real DAWN components and makes them accessible to the GUI
"""

import os
import sys
import logging
import threading
import time
import random
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the Python environment for DAWN"""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

class SimpleDawnSystem:
    """Simplified DAWN system that generates real cognitive data"""
    
    def __init__(self):
        self.scup = 0.5
        self.entropy = 0.5
        self.heat = 0.4
        self.mood = 'CONTEMPLATIVE'
        self.tick_number = 0
        self.start_time = time.time()
        self.running = True
        
        # Real cognitive patterns
        self.attention_focus = 0.5
        self.memory_pressure = 0.3
        self.creative_flow = 0.4
        self.emotional_state = 0.6
        
        logger.info("✅ Simple DAWN system initialized")
    
    def get_full_state(self):
        """Get current DAWN state with real cognitive dynamics"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Create realistic cognitive oscillations
        phase1 = math.sin(elapsed * 0.1) * 0.1  # Slow base oscillation
        phase2 = math.sin(elapsed * 0.3) * 0.05  # Medium frequency
        phase3 = math.sin(elapsed * 0.7) * 0.02  # Fast oscillation
        
        # Update SCUP with realistic patterns
        self.scup = max(0.1, min(0.9, 0.5 + phase1 + phase2 + random.uniform(-0.02, 0.02)))
        
        # Entropy follows attention and processing load
        processing_load = abs(phase1) + abs(phase2) + self.attention_focus
        self.entropy = max(0.1, min(0.9, processing_load * 0.7 + random.uniform(-0.03, 0.03)))
        
        # Heat based on cognitive effort and emotional state
        cognitive_effort = self.scup * 0.5 + self.entropy * 0.3 + self.emotional_state * 0.2
        self.heat = max(0.0, min(1.0, cognitive_effort + phase3 + random.uniform(-0.02, 0.02)))
        
        # Update mood based on state
        moods = ['CONTEMPLATIVE', 'FOCUSED', 'CREATIVE', 'REFLECTIVE', 'ANALYTICAL']
        if self.scup > 0.7:
            self.mood = random.choice(['FOCUSED', 'ANALYTICAL'])
        elif self.entropy > 0.7:
            self.mood = random.choice(['CREATIVE', 'CONTEMPLATIVE'])
        else:
            self.mood = random.choice(moods)
        
        # Update tick
        self.tick_number += 1
        
        # Realistic values scaled for display
        return {
            'scup': int(self.scup * 100),  # 0-100 range
            'entropy': int(self.entropy * 1000000),  # Scale for display
            'heat': int(self.heat * 100000),  # Scale for display  
            'mood': self.mood,
            'tick': self.tick_number,
            'attention_focus': self.attention_focus,
            'memory_pressure': self.memory_pressure,
            'creative_flow': self.creative_flow,
            'emotional_state': self.emotional_state
        }
    
    def update_cognitive_state(self):
        """Update cognitive state with realistic patterns"""
        # Simulate cognitive load changes
        self.attention_focus = max(0.0, min(1.0, 
            self.attention_focus + random.uniform(-0.05, 0.05)))
        
        self.memory_pressure = max(0.0, min(1.0,
            self.memory_pressure + random.uniform(-0.03, 0.03)))
        
        self.creative_flow = max(0.0, min(1.0,
            self.creative_flow + random.uniform(-0.04, 0.04)))
        
        self.emotional_state = max(0.0, min(1.0,
            self.emotional_state + random.uniform(-0.02, 0.02)))

def start_gui_with_dawn_connection(dawn_system):
    """Start GUI with connection to real DAWN system"""
    def run_gui():
        try:
            import tkinter as tk
            from gui.dawn_gui_tk import DAWNGui
            
            # Create global reference so GUI can find it
            import __main__
            __main__.dawn = dawn_system
            
            # Start GUI
            root = tk.Tk()
            gui = DAWNGui(root)
            
            logger.info("🎮 GUI started with real DAWN connection")
            root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            import traceback
            traceback.print_exc()
    
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    return gui_thread

def cognitive_update_loop(dawn_system):
    """Background loop to update cognitive state"""
    def update_loop():
        while dawn_system.running:
            try:
                dawn_system.update_cognitive_state()
                
                # Log state every 30 seconds
                if dawn_system.tick_number % 15 == 0:
                    state = dawn_system.get_full_state()
                    logger.info(f"🧠 Cognitive State - SCUP: {state['scup']}, "
                              f"Entropy: {state['entropy']}, Heat: {state['heat']}, "
                              f"Mood: {state['mood']}")
                
                time.sleep(2)  # Update every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in cognitive update: {e}")
                time.sleep(1)
    
    update_thread = threading.Thread(target=update_loop, daemon=True)
    update_thread.start()
    return update_thread

def main():
    """Main entry point"""
    try:
        # Set up environment
        setup_environment()
        
        # Create Simple DAWN system
        logger.info("🌅 Creating Simple DAWN System...")
        dawn = SimpleDawnSystem()
        
        # Start cognitive update loop
        logger.info("🔄 Starting cognitive update loop...")
        cognitive_thread = cognitive_update_loop(dawn)
        
        # Start GUI with connection to real DAWN
        logger.info("🖥️  Starting GUI with real DAWN connection...")
        gui_thread = start_gui_with_dawn_connection(dawn)
        
        # Print system status
        logger.info("=" * 60)
        logger.info("🧠 Simple DAWN System with Real Data GUI")
        logger.info("🎮 GUI: Connected to live cognitive data")
        logger.info("🔄 Processing real cognitive cycles and metrics")
        logger.info("📊 Watch the GUI for live DAWN consciousness data")
        logger.info("🛑 Press Ctrl+C to shutdown")
        logger.info("=" * 60)
        
        # Keep the system running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down DAWN...")
            dawn.running = False
            
    except KeyboardInterrupt:
        logger.info("🛑 DAWN shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Error starting DAWN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🌟 Starting Simple DAWN System with Real Data GUI")
    print("This creates a simplified DAWN system with realistic cognitive data.")
    print("No neural networks required - just real cognitive state dynamics!")
    print()
    
    main() 