#!/usr/bin/env python3
"""
Demo: SigilOverlayPanel with Realistic DAWN Data - Clean Version
Professional sigil visualization demo without emoji characters
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
import time
import threading
import random
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.sigil_overlay_panel import SigilOverlayPanel
from utils.clean_logger import CleanLogger

class DAWNSigilDemo:
    """Demo application showcasing the SigilOverlayPanel"""
    
    def __init__(self):
        self.logger = CleanLogger("SIGIL-DEMO")
        self.root = tk.Tk()
        self.root.title("DAWN Sigil Overlay Panel - Live Demo")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")
        
        # Demo data state
        self.demo_running = True
        self.current_heat = 45
        self.current_entropy = 0.5
        self.current_coherence = 0.7
        self.mood_cycle = 0
        
        self.setup_demo()
        
    def setup_demo(self):
        """Setup the demo interface"""
        # Title
        title_label = tk.Label(self.root, 
                              text="DAWN Sigil Overlay Panel Demo",
                              font=("Arial", 16, "bold"),
                              bg="#1a1a1a", fg="#00ff88")
        title_label.pack(pady=10)
        
        # Description
        desc_text = """Living Symbolic Radar for DAWN Consciousness
        
Bee House: Motion/Search processes
Whale House: Pressure/Depth analysis  
Owl House: Memory/Wisdom operations
Ant House: Loop/Recursion patterns

Features:
• Heat-based color coding (blue->yellow->red)
• Real-time decay animation (20 FPS)
• House-grouped cognitive processes
• Hover tooltips with bloom sources
• Dynamic sigil generation from DAWN state"""
        
        desc_label = tk.Label(self.root, text=desc_text, 
                             font=("Arial", 9),
                             bg="#1a1a1a", fg="#cccccc",
                             justify=tk.LEFT)
        desc_label.pack(pady=(0, 10))
        
        # Create the SigilOverlayPanel
        self.sigil_panel = SigilOverlayPanel(self.root, max_sigils=12)
        self.sigil_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#1a1a1a")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Test buttons
        tk.Button(control_frame, text="Generate Random Sigils",
                 command=self.generate_random_sigils,
                 bg="#2a2a2a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="High Creativity Mode",
                 command=self.creativity_burst,
                 bg="#2a2a2a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Deep Analysis Mode", 
                 command=self.analysis_mode,
                 bg="#2a2a2a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Thermal Spike",
                 command=self.thermal_spike,
                 bg="#2a2a2a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        # Status display
        self.status_label = tk.Label(self.root,
                                    text="Demo running - Watch sigils decay in real-time",
                                    font=("Arial", 10),
                                    bg="#1a1a1a", fg="#00ff88")
        self.status_label.pack(pady=5)
        
        # Start automatic demo cycle
        self.start_demo_cycle()
        
    def generate_random_sigils(self):
        """Generate a random set of test sigils"""
        dawn_data = {
            "heat": random.randint(20, 90),
            "entropy": random.uniform(0.3, 0.8),
            "scup": random.uniform(0.4, 0.9),
            "mood": random.choice(["CREATIVE", "CONTEMPLATIVE", "FOCUSED", "TRANSCENDENT"])
        }
        
        self.sigil_panel.generate_sigils_from_dawn_state(dawn_data)
        self.status_label.config(text=f"Random sigils generated - Heat: {dawn_data['heat']}%, Mood: {dawn_data['mood']}")
        self.logger.tick("Random sigils generated", dawn_data)
        
    def creativity_burst(self):
        """Simulate high creativity cognitive state"""
        dawn_data = {
            "heat": random.randint(60, 85),
            "entropy": random.uniform(0.7, 0.9),  # High entropy = creative
            "scup": random.uniform(0.6, 0.8),
            "mood": "CREATIVE"
        }
        
        self.sigil_panel.generate_sigils_from_dawn_state(dawn_data)
        self.status_label.config(text="Creativity burst activated - High entropy sigils generated")
        self.logger.success("Creativity burst activated", dawn_data)
        
    def analysis_mode(self):
        """Simulate deep analysis cognitive state"""
        dawn_data = {
            "heat": random.randint(70, 95),  # High heat for intense processing
            "entropy": random.uniform(0.2, 0.4),  # Low entropy = focused
            "scup": random.uniform(0.8, 0.95),  # High coherence
            "mood": "FOCUSED"
        }
        
        self.sigil_panel.generate_sigils_from_dawn_state(dawn_data)
        self.status_label.config(text="Deep analysis mode - High coherence, focused processing")
        self.logger.info("Deep analysis mode activated", dawn_data)
        
    def thermal_spike(self):
        """Simulate thermal processing spike"""
        dawn_data = {
            "heat": random.randint(85, 100),  # Very high heat
            "entropy": random.uniform(0.5, 0.7),
            "scup": random.uniform(0.5, 0.7),
            "mood": "ONLINE"
        }
        
        self.sigil_panel.generate_sigils_from_dawn_state(dawn_data)
        self.status_label.config(text="Thermal spike detected - System running hot")
        self.logger.warning("Thermal spike detected", dawn_data)
        
    def start_demo_cycle(self):
        """Start the automatic demo cycle"""
        def demo_cycle():
            while self.demo_running:
                try:
                    # Cycle through different cognitive states
                    self.mood_cycle += 1
                    
                    if self.mood_cycle % 4 == 0:
                        self.generate_random_sigils()
                    elif self.mood_cycle % 4 == 1:
                        self.creativity_burst()
                    elif self.mood_cycle % 4 == 2:
                        self.analysis_mode()
                    else:
                        self.thermal_spike()
                    
                    # Wait between cycles
                    time.sleep(8)  # 8 seconds between automatic changes
                    
                except Exception as e:
                    self.logger.error("Demo cycle error", {"error": str(e)})
                    time.sleep(1)
        
        # Start demo cycle in background
        demo_thread = threading.Thread(target=demo_cycle, daemon=True)
        demo_thread.start()
        
    def run(self):
        """Run the demo"""
        self.logger.system("DAWN Sigil Overlay Panel Demo", {
            "status": "Starting live sigil visualization",
            "controls": "Use buttons to trigger different cognitive states",
            "features": "Real-time decay, house grouping, heat coloring",
            "interaction": "Hover over sigils for tooltips"
        })
        
        try:
            # Start with initial sigils
            self.generate_random_sigils()
            
            # Run GUI
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.warning("Demo interrupted by user")
        finally:
            self.demo_running = False
            self.logger.success("Demo complete")


def main():
    """Main demo entry point"""
    demo = DAWNSigilDemo()
    demo.run()


if __name__ == "__main__":
    main() 