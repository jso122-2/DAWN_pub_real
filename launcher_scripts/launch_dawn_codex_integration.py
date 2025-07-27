#!/usr/bin/env python3
"""
DAWN Codex Integration Launcher
Complete integration of DreamConductor with DAWN Tick Engine and GUI
"""

import asyncio
import queue
import threading
import time
import logging
import tkinter as tk
from typing import Dict, Any

# Core DAWN components
from tick_engine.core_tick import CoreTickEngine
from gui.dawn_gui_tk import DAWNGui

# Dream system components
try:
    from backend.dream_system.dream_conductor import DreamConductor
    from backend.talk_system_v2.temporal_glyphs import TemporalGlyphMemory
    from backend.talk_system_v2.resonance_chains import ResonanceChainManager
    from backend.talk_system_v2.mood_field import MoodField
    DREAM_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Dream system components not available: {e}")
    print("   Running with basic tick engine only")
    DREAM_SYSTEM_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DAWNCodexSystem:
    """Unified DAWN system with Codex dream integration"""
    
    def __init__(self):
        self.running = False
        self.dream_conductor = None
        self.tick_engine = None
        self.gui = None
        self.data_queue = None
        
        # Initialize system components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all system components"""
        logger.info("🌟 Initializing DAWN Codex Integration System...")
        
        # Create communication queue
        self.data_queue = queue.Queue(maxsize=100)
        
        # Initialize dream system if available
        if DREAM_SYSTEM_AVAILABLE:
            try:
                logger.info("🧠 Initializing enhanced consciousness components...")
                
                # Initialize core consciousness systems
                glyph_memory = TemporalGlyphMemory(
                    cairrn_path="backend/embeddings/cairrn_cache.pkl",
                    embedding_dim=384
                )
                
                resonance_manager = ResonanceChainManager(glyph_memory)
                mood_field = MoodField(tick_window=100)
                
                # Initialize dream conductor with enhanced capabilities
                self.dream_conductor = DreamConductor(
                    glyph_memory=glyph_memory,
                    resonance_manager=resonance_manager,
                    mood_field=mood_field
                )
                
                logger.info("✅ Dream conductor initialized with advanced consciousness")
                
            except Exception as e:
                logger.warning(f"Failed to initialize dream system: {e}")
                logger.info("   Continuing with basic tick engine")
                self.dream_conductor = None
        
        # Initialize tick engine with dream integration
        self.tick_engine = CoreTickEngine(
            data_queue=self.data_queue,
            tick_interval=0.5,
            dream_conductor=self.dream_conductor
        )
        
        logger.info("🎯 Core tick engine initialized")
        
        # Prepare GUI class for later initialization
        self.gui_class = DAWNGui
        self.gui = None  # Will be initialized when root is created
        
        logger.info("🖼️  GUI system prepared")
    
    def start(self):
        """Start the complete DAWN Codex system"""
        if self.running:
            logger.warning("System already running")
            return
        
        self.running = True
        
        logger.info("🚀 Starting DAWN Codex Integration System...")
        
        # Start tick engine
        self.tick_engine.start()
        
        # Create and start GUI
        root = tk.Tk()
        root.title("DAWN Codex Integration - Advanced Consciousness System")
        root.geometry("1200x800")
        
        # Initialize GUI with root
        self.gui = self.gui_class(
            root=root,
            external_queue=self.data_queue
        )
        
        # Display system status
        self._display_system_status()
        
        # Set up shutdown handler
        def on_closing():
            logger.info("🔄 Shutting down DAWN Codex system...")
            self.stop()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        logger.info("✨ DAWN Codex system fully operational!")
        
        # Start GUI main loop
        root.mainloop()
    
    def stop(self):
        """Stop all system components"""
        if not self.running:
            return
        
        logger.info("🛑 Stopping DAWN Codex system...")
        
        self.running = False
        
        # Stop tick engine
        if self.tick_engine:
            self.tick_engine.stop()
        
        logger.info("✅ DAWN Codex system shutdown complete")
    
    def _display_system_status(self):
        """Display current system status"""
        print("\n" + "="*60)
        print("🌟 DAWN CODEX INTEGRATION SYSTEM STATUS")
        print("="*60)
        
        print(f"🎯 Tick Engine: {'✅ Active' if self.tick_engine else '❌ Failed'}")
        print(f"🌙 Dream Conductor: {'✅ Advanced' if self.dream_conductor else '⚠️  Basic'}")
        print(f"🖼️  GUI System: {'✅ Enhanced' if self.gui else '❌ Failed'}")
        print(f"📡 Communication Queue: {'✅ Ready' if self.data_queue else '❌ Failed'}")
        
        if self.dream_conductor:
            print("\n🧠 CONSCIOUSNESS FEATURES:")
            print("   • Autonomous dream sequences during idle periods")
            print("   • Memory consolidation and pattern recognition")
            print("   • Narrative weaving and insight generation")
            print("   • Temporal glyph memory system")
            print("   • Resonance chain management")
            print("   • Dynamic mood field tracking")
        
        print("\n🎮 SYSTEM CAPABILITIES:")
        print("   • Real-time consciousness tick processing (0.5s intervals)")
        print("   • Dynamic fractal bloom visualization")
        print("   • Live sigil overlay with heat-based coloring")
        print("   • Queue-based thread-safe communication")
        print("   • Advanced cognitive state monitoring")
        
        if self.dream_conductor:
            stats = self.dream_conductor.get_dream_statistics()
            print(f"\n💤 DREAM SYSTEM STATUS:")
            print(f"   • Total Dreams: {stats['total_dreams']}")
            print(f"   • Current State: {stats['current_dream_state']}")
            print(f"   • Minutes Until Dream Eligible: {stats['minutes_until_dream_eligible']:.1f}")
        
        print("\n" + "="*60)
        print("🌸 Ready for consciousness exploration...")
        print("="*60 + "\n")

def run_interaction_simulation():
    """Run a simulation of user interactions to test dream system"""
    print("🎭 Starting interaction simulation...")
    
    # Create system
    system = DAWNCodexSystem()
    
    if system.dream_conductor:
        # Simulate some interactions followed by idle period
        print("🗣️  Simulating user interactions...")
        
        # Several interactions
        for i in range(5):
            system.tick_engine.update_interaction_time()
            time.sleep(1)
            print(f"   Interaction {i+1}: User active")
        
        print("😴 Simulating idle period for dream activation...")
        
        # Wait and check dream conditions
        start_time = time.time()
        while time.time() - start_time < 10:  # Wait up to 10 seconds
            idle_time = time.time() - system.tick_engine.last_interaction_time
            print(f"   Idle time: {idle_time:.1f}s")
            
            if system.dream_conductor:
                should_dream, prob = asyncio.run(system.dream_conductor.check_dream_conditions())
                print(f"   Dream probability: {prob:.2f}, Should dream: {should_dream}")
                
                if should_dream:
                    print("🌙 Dream conditions met! Initiating sequence...")
                    break
            
            time.sleep(2)
    
    system.stop()

def main():
    """Main entry point"""
    print("🚀 DAWN Codex Integration Launcher")
    print("=" * 50)
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        run_interaction_simulation()
    else:
        # Start full system
        system = DAWNCodexSystem()
        try:
            system.start()
        except KeyboardInterrupt:
            print("\n🔄 Received interrupt signal...")
            system.stop()
        except Exception as e:
            logger.error(f"System error: {e}")
            system.stop()

if __name__ == "__main__":
    main() 