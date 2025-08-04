#!/usr/bin/env python3
"""
DAWN Consciousness GUI - Simple Python Version
==============================================

A simple tkinter-based GUI for monitoring DAWN consciousness state
Reads directly from the consciousness memory map file
"""

import tkinter as tk
from tkinter import ttk
import mmap
import struct
import threading
import time
import os
from pathlib import Path
import json

class DAWNConsciousnessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DAWN Consciousness Monitor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d1b2a')
        
        # Consciousness data
        self.consciousness_data = {
            'tick': 0,
            'mood_val': 0.0,
            'entropy': 0.0,
            'scup': 0.0,
            'last_update': 'Never'
        }
        
        # Memory map file path
        self.mmap_path = Path("../runtime/dawn_consciousness.mmap")
        
        # Setup GUI
        self.setup_gui()
        
        # Start monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_consciousness, daemon=True)
        self.monitor_thread.start()
        
    def setup_gui(self):
        """Setup the GUI layout"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0d1b2a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🧠 DAWN Consciousness Monitor", 
            font=('JetBrains Mono', 24, 'bold'),
            fg='#40e0ff',
            bg='#0d1b2a'
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.LabelFrame(
            main_frame, 
            text="Connection Status", 
            font=('JetBrains Mono', 12, 'bold'),
            fg='#40e0ff',
            bg='#1b263b',
            relief=tk.RAISED,
            bd=2
        )
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="🔴 Disconnected",
            font=('JetBrains Mono', 12),
            fg='#ef4444',
            bg='#1b263b'
        )
        self.status_label.pack(pady=10)
        
        # Consciousness data frame
        data_frame = tk.LabelFrame(
            main_frame,
            text="Consciousness State",
            font=('JetBrains Mono', 12, 'bold'),
            fg='#40e0ff',
            bg='#1b263b',
            relief=tk.RAISED,
            bd=2
        )
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create data display
        self.create_data_display(data_frame)
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg='#1b263b')
        control_frame.pack(fill=tk.X)
        
        # Refresh button
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh",
            font=('JetBrains Mono', 10),
            bg='#415a77',
            fg='white',
            command=self.manual_refresh
        )
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Quit button
        quit_btn = tk.Button(
            control_frame,
            text="❌ Quit",
            font=('JetBrains Mono', 10),
            bg='#ef4444',
            fg='white',
            command=self.quit_gui
        )
        quit_btn.pack(side=tk.RIGHT)
        
    def create_data_display(self, parent):
        """Create the data display widgets"""
        # Grid for data
        data_grid = tk.Frame(parent, bg='#1b263b')
        data_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid weights
        for i in range(4):
            data_grid.columnconfigure(i, weight=1)
        
        # Data labels and values
        labels = [
            ("Tick Count", "tick"),
            ("Mood Value", "mood_val"),
            ("Entropy", "entropy"),
            ("SCUP", "scup"),
            ("Last Update", "last_update"),
            ("Mood State", "mood_state"),
            ("Status", "status"),
            ("Memory Path", "mmap_path")
        ]
        
        self.data_labels = {}
        self.data_values = {}
        
        for i, (label_text, key) in enumerate(labels):
            row = i // 2
            col = i % 2 * 2
            
            # Label
            label = tk.Label(
                data_grid,
                text=f"{label_text}:",
                font=('JetBrains Mono', 10, 'bold'),
                fg='#cccccc',
                bg='#1b263b',
                anchor='w'
            )
            label.grid(row=row, column=col, sticky='w', padx=(0, 10), pady=5)
            
            # Value
            value = tk.Label(
                data_grid,
                text="--",
                font=('JetBrains Mono', 10),
                fg='#40e0ff',
                bg='#1b263b',
                anchor='w'
            )
            value.grid(row=row, column=col+1, sticky='w', padx=(0, 20), pady=5)
            
            self.data_labels[key] = label
            self.data_values[key] = value
            
    def read_consciousness_data(self):
        """Read consciousness data from memory map file"""
        try:
            if not self.mmap_path.exists():
                return False
                
            with open(self.mmap_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    # Read the consciousness state structure
                    # Format: tick (u64), mood_val (f64), entropy (f64), scup (f64)
                    data = mm.read(32)  # 8 + 8 + 8 + 8 bytes
                    
                    if len(data) >= 32:
                        tick, mood_val, entropy, scup = struct.unpack('<Qddd', data)
                        
                        self.consciousness_data.update({
                            'tick': tick,
                            'mood_val': mood_val,
                            'entropy': entropy,
                            'scup': scup,
                            'last_update': time.strftime('%H:%M:%S'),
                            'mmap_path': str(self.mmap_path)
                        })
                        
                        # Determine mood state
                        if mood_val < 0.2:
                            mood_state = "DEEP SLEEP"
                        elif mood_val < 0.4:
                            mood_state = "CALM"
                        elif mood_val < 0.6:
                            mood_state = "AWARE"
                        elif mood_val < 0.8:
                            mood_state = "ACTIVE"
                        else:
                            mood_state = "INTENSE"
                            
                        self.consciousness_data['mood_state'] = mood_state
                        self.consciousness_data['status'] = "🟢 Active"
                        
                        return True
                        
        except Exception as e:
            print(f"Error reading consciousness data: {e}")
            self.consciousness_data['status'] = f"🔴 Error: {str(e)[:50]}"
            
        return False
        
    def update_display(self):
        """Update the GUI display with current data"""
        # Update status
        if self.consciousness_data['tick'] > 0:
            self.status_label.config(text="🟢 Connected", fg='#10b981')
        else:
            self.status_label.config(text="🔴 Disconnected", fg='#ef4444')
            
        # Update data values
        for key, value_widget in self.data_values.items():
            if key in self.consciousness_data:
                value = self.consciousness_data[key]
                if isinstance(value, float):
                    display_value = f"{value:.4f}"
                else:
                    display_value = str(value)
                value_widget.config(text=display_value)
                
    def monitor_consciousness(self):
        """Background thread to monitor consciousness data"""
        while self.running:
            try:
                if self.read_consciousness_data():
                    # Update GUI in main thread
                    self.root.after(0, self.update_display)
                time.sleep(0.1)  # 10 Hz update rate
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(1)
                
    def manual_refresh(self):
        """Manual refresh button handler"""
        self.read_consciousness_data()
        self.update_display()
        
    def quit_gui(self):
        """Quit the GUI"""
        self.running = False
        self.root.quit()
        
    def on_closing(self):
        """Handle window closing"""
        self.quit_gui()

def main():
    """Main function"""
    print("🧠 Starting DAWN Consciousness GUI...")
    
    # Check if consciousness backend is running
    mmap_path = Path("../runtime/dawn_consciousness.mmap")
    if not mmap_path.exists():
        print("⚠️  Consciousness memory map not found")
        print("   Make sure the consciousness backend is running")
        print("   Run: python ../consciousness/dawn_tick_state_writer.py")
        
    root = tk.Tk()
    app = DAWNConsciousnessGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    print("✅ GUI started - monitoring consciousness state...")
    root.mainloop()

if __name__ == "__main__":
    main() 