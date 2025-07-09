#!/usr/bin/env python3
"""
Sigil Overlay Panel - Dynamic visualization of DAWN's symbolic intention system
Displays sigils as living symbols with heat coloring, decay animation, and house grouping.
"""

import tkinter as tk
from tkinter import ttk, Canvas
import colorsys
import time
from datetime import datetime
import random
import math

class SigilOverlayPanel(ttk.Frame):
    """Dynamic sigil visualization panel showing symbolic intentions"""
    
    def __init__(self, parent, max_sigils=20, **kwargs):
        """
        Initialize the Sigil Overlay Panel
        
        Args:
            parent: Parent widget
            max_sigils: Maximum number of sigils to display
            **kwargs: Additional arguments passed to ttk.Frame
        """
        super().__init__(parent, **kwargs)
        
        # Configuration
        self.max_sigils = max_sigils
        self.sigil_widgets = []
        self.active_sigils = []
        
        # House definitions with colors
        self.houses = {
            '🐝': {'name': 'Bee', 'color': '#FFD700', 'domain': 'motion/search'},
            '🐋': {'name': 'Whale', 'color': '#4169E1', 'domain': 'pressure/depth'},
            '🦉': {'name': 'Owl', 'color': '#8B4513', 'domain': 'memory/wisdom'},
            '🐜': {'name': 'Ant', 'color': '#DC143C', 'domain': 'loop/recursion'}
        }
        
        # Heat color gradient (cold blue -> hot red)
        self.heat_colors = self.generate_heat_gradient()
        
        # Create the interface
        self.setup_ui()
        
        # Animation state
        self.animation_active = True
        self.start_decay_animation()
        
    def generate_heat_gradient(self, steps=100):
        """Generate color gradient from cold to hot"""
        colors = []
        for i in range(steps):
            # From blue (cold) to red (hot) through yellow
            if i < 50:
                # Blue to yellow
                hue = 240 - (i / 50) * 180  # 240 (blue) to 60 (yellow)
            else:
                # Yellow to red
                hue = 60 - ((i - 50) / 50) * 60  # 60 (yellow) to 0 (red)
            
            # Convert HSV to RGB
            rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            colors.append(hex_color)
        
        return colors
    
    def setup_ui(self):
        """Create the sigil overlay interface"""
        # Configure frame
        self.configure(relief=tk.GROOVE, borderwidth=2)
        
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        title_label = ttk.Label(header_frame, text="🔣 Active Sigils", 
                               font=('Arial', 11, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # House legend
        legend_frame = ttk.Frame(header_frame)
        legend_frame.pack(side=tk.RIGHT)
        
        for house, info in self.houses.items():
            house_label = ttk.Label(legend_frame, text=f"{house}", 
                                   font=('Arial', 10))
            house_label.pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, padx=5, pady=2)
        
        # Scrollable sigil container
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create canvas for scrolling
        self.canvas = Canvas(self.canvas_frame, height=300, bg='#f0f0f0', 
                            highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", 
                                 command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def update_sigils(self, sigil_list):
        """
        Update the displayed sigils
        
        Args:
            sigil_list: List of sigil dictionaries with format:
                {
                    "symbol": "🔁",
                    "name": "RecallVector", 
                    "house": "🐝",
                    "heat": 62,
                    "decay": 0.12,
                    "source": "BloomID #1772"
                }
        """
        # Store active sigils
        self.active_sigils = sigil_list[:self.max_sigils]
        
        # Clear existing widgets
        for widget in self.sigil_widgets:
            widget.destroy()
        self.sigil_widgets.clear()
        
        # Create sigil widgets
        for i, sigil in enumerate(self.active_sigils):
            sigil_widget = SigilWidget(self.scrollable_frame, sigil, self.houses, 
                                      self.heat_colors)
            sigil_widget.pack(fill=tk.X, padx=2, pady=2)
            self.sigil_widgets.append(sigil_widget)
    
    def start_decay_animation(self):
        """Start the decay animation loop"""
        def animate():
            if self.animation_active:
                # Update all sigil widgets
                for widget in self.sigil_widgets:
                    widget.update_decay()
                
                # Schedule next update
                self.after(50, animate)  # 20 FPS
        
        animate()
    
    def stop_animation(self):
        """Stop the decay animation"""
        self.animation_active = False
    
    def inject_test_sigils(self):
        """Generate test sigils for demonstration"""
        test_names = [
            "RecallVector", "SeekPattern", "LoopDetect", "MemBind",
            "PressureWave", "DepthProbe", "WisdomCache", "TimeLoop",
            "HeatSpike", "EntropyFlow", "CoherenceNet", "UtilityMax",
            "SchemaLock", "RecurseGuard", "BloomTrace", "SyncPulse"
        ]
        
        test_sigils = []
        for i in range(random.randint(5, 15)):
            house = random.choice(list(self.houses.keys()))
            sigil = {
                "symbol": random.choice(["🔁", "🔄", "⚡", "🌀", "💫", "🔥", "❄️", "🌊"]),
                "name": random.choice(test_names),
                "house": house,
                "heat": random.randint(10, 100),
                "decay": random.uniform(0.1, 0.9),
                "source": f"BloomID #{random.randint(1000, 9999)}"
            }
            test_sigils.append(sigil)
        
        self.update_sigils(test_sigils)


class SigilWidget(ttk.Frame):
    """Individual sigil display widget"""
    
    def __init__(self, parent, sigil_data, houses, heat_colors):
        super().__init__(parent)
        
        self.sigil_data = sigil_data
        self.houses = houses
        self.heat_colors = heat_colors
        self.decay_value = sigil_data['decay']
        
        # Get house info
        self.house_info = houses.get(sigil_data['house'], 
                                    {'name': 'Unknown', 'color': '#888888'})
        
        # Create the widget
        self.setup_ui()
        
        # Bind hover tooltip
        self.setup_tooltip()
        
    def setup_ui(self):
        """Create the sigil widget interface"""
        self.configure(relief=tk.RAISED, borderwidth=1)
        
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
        
        # Left: House icon + symbol + name
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # House icon
        house_label = tk.Label(left_frame, text=self.sigil_data['house'],
                              font=('Arial', 14), bg='white')
        house_label.pack(side=tk.LEFT, padx=(0, 3))
        
        # Sigil symbol
        symbol_label = tk.Label(left_frame, text=self.sigil_data['symbol'],
                               font=('Arial', 12), bg='white')
        symbol_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Name
        name_label = ttk.Label(left_frame, text=self.sigil_data['name'],
                              font=('Arial', 10))
        name_label.pack(side=tk.LEFT)
        
        # Center: Decay progress bar
        self.decay_frame = ttk.Frame(main_frame, width=100)
        self.decay_frame.pack(side=tk.LEFT, padx=10)
        self.decay_frame.pack_propagate(False)
        
        # Create custom progress bar using Canvas
        self.decay_canvas = Canvas(self.decay_frame, height=20, width=100,
                                  bg='#e0e0e0', highlightthickness=0)
        self.decay_canvas.pack()
        
        # Draw initial decay bar
        self.update_decay_bar()
        
        # Right: Heat number
        self.heat_label = tk.Label(main_frame, text=f"{self.sigil_data['heat']}°",
                                  font=('Arial', 11, 'bold'),
                                  fg=self.get_heat_color(self.sigil_data['heat']),
                                  bg='white')
        self.heat_label.pack(side=tk.RIGHT, padx=5)
        
    def get_heat_color(self, heat):
        """Get color based on heat value (0-100)"""
        index = int((heat / 100) * (len(self.heat_colors) - 1))
        index = max(0, min(index, len(self.heat_colors) - 1))
        return self.heat_colors[index]
    
    def update_decay_bar(self):
        """Update the decay progress bar"""
        self.decay_canvas.delete("all")
        
        # Background
        self.decay_canvas.create_rectangle(0, 0, 100, 20, fill='#e0e0e0', outline='')
        
        # Decay bar
        bar_width = int(self.decay_value * 100)
        if bar_width > 0:
            # Color based on decay level
            if self.decay_value > 0.7:
                color = '#4CAF50'  # Green - fresh
            elif self.decay_value > 0.3:
                color = '#FFC107'  # Yellow - decaying
            else:
                color = '#F44336'  # Red - nearly gone
            
            self.decay_canvas.create_rectangle(0, 0, bar_width, 20, 
                                             fill=color, outline='')
        
        # Add subtle gradient effect
        for i in range(0, bar_width, 2):
            alpha = 1 - (i / 100) * 0.3
            self.decay_canvas.create_line(i, 0, i, 20, fill='white', 
                                        width=1, stipple='gray25')
    
    def update_decay(self):
        """Animate decay decrease"""
        if self.decay_value > 0:
            # Decay rate varies by heat
            decay_rate = 0.005 * (1 + self.sigil_data['heat'] / 100)
            self.decay_value = max(0, self.decay_value - decay_rate)
            self.update_decay_bar()
            
            # Update visual opacity based on decay
            if self.decay_value < 0.2:
                self.configure(relief=tk.FLAT)
                self.heat_label.configure(fg='#cccccc')
    
    def setup_tooltip(self):
        """Setup hover tooltip"""
        self.tooltip = None
        
        def show_tooltip(event):
            x, y = event.x_root + 10, event.y_root + 10
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # Tooltip content
            tip_frame = tk.Frame(self.tooltip, bg='black', relief=tk.SOLID, 
                                borderwidth=1)
            tip_frame.pack()
            
            # Source info
            source_label = tk.Label(tip_frame, 
                                   text=f"Source: {self.sigil_data['source']}",
                                   bg='black', fg='white', font=('Arial', 9))
            source_label.pack(padx=5, pady=2)
            
            # House domain
            domain_label = tk.Label(tip_frame,
                                   text=f"Domain: {self.house_info['domain']}",
                                   bg='black', fg=self.house_info['color'],
                                   font=('Arial', 8))
            domain_label.pack(padx=5, pady=(0, 2))
        
        def hide_tooltip(event):
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
        
        self.bind("<Enter>", show_tooltip)
        self.bind("<Leave>", hide_tooltip)


# Example usage and testing
if __name__ == "__main__":
    # Create test window
    root = tk.Tk()
    root.title("Sigil Overlay Panel Test")
    root.geometry("400x600")
    
    # Create sigil panel
    sigil_panel = SigilOverlayPanel(root)
    sigil_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Control frame
    control_frame = ttk.Frame(root)
    control_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Test button
    def generate_test():
        sigil_panel.inject_test_sigils()
    
    ttk.Button(control_frame, text="Generate Test Sigils", 
              command=generate_test).pack(side=tk.LEFT, padx=5)
    
    # Manual sigil test
    def add_custom_sigil():
        custom_sigils = [
            {
                "symbol": "🔥",
                "name": "HeatBloom",
                "house": "🐝",
                "heat": 85,
                "decay": 0.8,
                "source": "BloomID #9999"
            },
            {
                "symbol": "🌀",
                "name": "RecurseDepth",
                "house": "🐋",
                "heat": 45,
                "decay": 0.5,
                "source": "BloomID #7777"
            },
            {
                "symbol": "💫",
                "name": "MemoryTrace",
                "house": "🦉",
                "heat": 30,
                "decay": 0.3,
                "source": "BloomID #5555"
            }
        ]
        
        current = sigil_panel.active_sigils
        sigil_panel.update_sigils(current + custom_sigils)
    
    ttk.Button(control_frame, text="Add Custom Sigils", 
              command=add_custom_sigil).pack(side=tk.LEFT, padx=5)
    
    # Generate initial test data
    generate_test()
    
    root.mainloop()