#!/usr/bin/env python3
"""
DAWN Fractal Canvas - Blueprint Implementation
Simple fractal visualization and GUI component
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, Canvas
import numpy as np
import threading
import time
from typing import Dict, Any, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DAWNGui:
    """Simple DAWN GUI with fractal canvas"""
    
    def __init__(self):
        self.root = None
        self.canvas = None
        self.is_running = False
        self.data = {}
        
    def create_gui(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("🌅 DAWN Fractal Canvas")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🌅 DAWN Consciousness Visualization", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Canvas for fractal visualization
        self.canvas = Canvas(main_frame, width=600, height=400, bg='#000000')
        self.canvas.pack(pady=10)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Status: Initializing...")
        self.status_label.pack(side='left')
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side='left', padx=5)
        
        self.clear_button = ttk.Button(control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side='left', padx=5)
        
        return self.root
    
    def start(self):
        """Start the visualization"""
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Status: Running")
            # Start animation thread
            threading.Thread(target=self._animation_loop, daemon=True).start()
    
    def stop(self):
        """Stop the visualization"""
        self.is_running = False
        self.status_label.config(text="Status: Stopped")
    
    def clear_canvas(self):
        """Clear the canvas"""
        if self.canvas:
            self.canvas.delete('all')
    
    def _animation_loop(self):
        """Simple animation loop"""
        frame = 0
        while self.is_running:
            try:
                self._draw_fractal_frame(frame)
                frame += 1
                time.sleep(0.1)  # 10 FPS
            except Exception as e:
                print(f"Animation error: {e}")
                break
    
    def _draw_fractal_frame(self, frame):
        """Draw a simple fractal pattern"""
        if not self.canvas:
            return
            
        # Clear previous frame
        self.canvas.delete('all')
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            width, height = 600, 400
        
        # Simple spiral pattern
        center_x = width // 2
        center_y = height // 2
        
        for i in range(50):
            angle = (frame * 0.1 + i * 0.3) % (2 * np.pi)
            radius = 2 + i * 3
            
            x = center_x + int(radius * np.cos(angle))
            y = center_y + int(radius * np.sin(angle))
            
            # Color based on time and position
            color_val = int(128 + 127 * np.sin(frame * 0.05 + i * 0.2))
            color = f"#{color_val:02x}{(255-color_val):02x}ff"
            
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline="")
    
    def update_data(self, data: Dict[str, Any]):
        """Update visualization with new data"""
        self.data = data
        
    def run(self):
        """Run the GUI"""
        if not self.root:
            self.create_gui()
        
        self.start()
        self.root.mainloop()

def create_dawn_gui():
    """Factory function to create DAWN GUI"""
    return DAWNGui()

def main():
    """Main entry point"""
    print("🌅 Starting DAWN Fractal Canvas...")
    gui = create_dawn_gui()
    gui.run()

if __name__ == "__main__":
    main()