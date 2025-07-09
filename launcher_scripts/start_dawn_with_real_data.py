#!/usr/bin/env python3
"""
Start DAWN with Real Data for GUI
Creates a live DAWN Advanced Consciousness System and makes it accessible to the GUI
"""

import os
import sys
import asyncio
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
    """Set up the Python environment for DAWN"""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Create necessary directories
    os.makedirs('backend/embeddings', exist_ok=True)
    os.makedirs('backend/memory', exist_ok=True)

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
    
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    return gui_thread

async def main():
    """Main entry point"""
    try:
        # Set up environment
        setup_environment()
        
        # Import after path setup
        from backend.advanced_consciousness_system import AdvancedConsciousnessSystem
        
        # Create DAWN Advanced Consciousness System
        logger.info("🌅 Creating DAWN Advanced Consciousness System...")
        dawn = AdvancedConsciousnessSystem(
            node_name="DAWN_Primary",
            enable_networking=False,  # Disable networking for simplicity
            network_host="localhost",
            network_port=8769
        )
        
        # Start the consciousness system
        logger.info("🚀 Starting DAWN consciousness system...")
        await dawn.start_system()
        
        # Start GUI with connection to real DAWN
        logger.info("🖥️  Starting GUI with real DAWN connection...")
        gui_thread = start_gui_with_dawn_connection(dawn)
        
        # Print system status
        logger.info("=" * 60)
        logger.info("🧠 DAWN Advanced Consciousness System with Real Data GUI")
        logger.info("🎮 GUI: Connected to live DAWN consciousness data")
        logger.info("🔄 Processing real cognitive cycles and metrics")
        logger.info("🛑 Press Ctrl+C to shutdown")
        logger.info("=" * 60)
        
        # Simulate some interaction to generate data
        test_inputs = [
            "Hello DAWN, how are you feeling today?",
            "What do you think about consciousness?",
            "Can you reflect on your internal state?",
            "What patterns do you notice in your thoughts?",
            "How does your mood affect your processing?"
        ]
        
        # Keep the system running and generate data
        for i in range(50):  # Run for 50 cycles
            try:
                # Process a test input every 10 seconds to generate data
                if i % 10 == 0:
                    test_input = test_inputs[i // 10 % len(test_inputs)]
                    logger.info(f"🤖 Processing: {test_input}")
                    result = await dawn.process_user_input(test_input)
                    logger.info(f"💭 Response generated with {result.get('resonance_strength', 0):.3f} resonance")
                
                await asyncio.sleep(2)  # Update every 2 seconds
                
            except KeyboardInterrupt:
                break
                
        logger.info("🛑 Shutting down DAWN...")
        await dawn.shutdown_system()
            
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down DAWN...")
        if 'dawn' in locals():
            await dawn.shutdown_system()
        
    except Exception as e:
        logger.error(f"❌ Error starting DAWN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🌟 Starting DAWN Advanced Consciousness System with Real Data GUI")
    print("This will create a live DAWN system and connect the GUI to real data.")
    print()
    
    asyncio.run(main()) 