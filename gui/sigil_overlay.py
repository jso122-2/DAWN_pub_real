#!/usr/bin/env python3
"""
DAWN Sigil Stream Overlay Panel
Visual panel showing active sigils, decay percentages, and pressure alignment

File: gui/sigil_overlay.py
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional
import math


class SigilRow:
    """Individual sigil display row component"""
    
    def __init__(self, parent, sigil_data: Dict):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.FLAT, bd=1)
        
        # Sigil data
        self.sigil_data = sigil_data
        self.symbol = sigil_data.get("symbol", "◉")
        self.name = sigil_data.get("name", "Unknown")
        self.task_class = sigil_data.get("class", "🔮")
        self.heat = sigil_data.get("heat", 0)
        self.decay = sigil_data.get("decay", 0.0)
        
        # UI Components
        self.symbol_label = None
        self.name_label = None
        self.class_label = None
        self.heat_canvas = None
        self.decay_label = None
        
        self.setup_row()
        self.update_display()
    
    def setup_row(self):
        """Setup the sigil row layout"""
        # Row container with hover effect
        self.frame.configure(highlightbackground="#333333", highlightthickness=1)
        
        # Left section: Symbol and Class
        left_frame = tk.Frame(self.frame, bg="#1a1a1a")
        left_frame.pack(side=tk.LEFT, padx=(8, 5), pady=4)
        
        # Sigil symbol (large)
        self.symbol_label = tk.Label(left_frame, text=self.symbol, 
                                    font=("Arial", 16), bg="#1a1a1a", fg="#ffffff")
        self.symbol_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Task class emoji
        self.class_label = tk.Label(left_frame, text=self.task_class, 
                                   font=("Arial", 14), bg="#1a1a1a")
        self.class_label.pack(side=tk.LEFT)
        
        # Center section: Name and Heat Bar
        center_frame = tk.Frame(self.frame, bg="#1a1a1a")
        center_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=4)
        
        # Sigil name
        self.name_label = tk.Label(center_frame, text=self.name, 
                                  font=("Arial", 10, "bold"), bg="#1a1a1a", fg="#cccccc",
                                  anchor=tk.W)
        self.name_label.pack(fill=tk.X)
        
        # Heat bar container
        heat_frame = tk.Frame(center_frame, bg="#1a1a1a")
        heat_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Heat label
        heat_label = tk.Label(heat_frame, text="Heat:", 
                             font=("Arial", 8), bg="#1a1a1a", fg="#888888")
        heat_label.pack(side=tk.LEFT)
        
        # Heat progress bar (custom canvas)
        self.heat_canvas = tk.Canvas(heat_frame, width=100, height=8, 
                                    bg="#333333", highlightthickness=0)
        self.heat_canvas.pack(side=tk.LEFT, padx=(5, 0))
        
        # Heat background
        self.heat_bg = self.heat_canvas.create_rectangle(1, 1, 99, 7, 
                                                        fill="#444444", outline="#666666")
        
        # Heat foreground bar
        self.heat_bar = self.heat_canvas.create_rectangle(1, 1, 1, 7, 
                                                         fill="#00ff88", outline="")
        
        # Right section: Decay Status
        right_frame = tk.Frame(self.frame, bg="#1a1a1a")
        right_frame.pack(side=tk.RIGHT, padx=(5, 8), pady=4)
        
        # Decay percentage
        self.decay_label = tk.Label(right_frame, text="100%", 
                                   font=("Arial", 9, "bold"), bg="#1a1a1a", fg="#00ff88")
        self.decay_label.pack()
        
        # Decay status text
        self.decay_status_label = tk.Label(right_frame, text="Active", 
                                          font=("Arial", 7), bg="#1a1a1a", fg="#888888")
        self.decay_status_label.pack()
    
    def update_display(self):
        """Update the sigil row display with current data"""
        try:
            # Update basic info
            self.symbol_label.config(text=self.symbol)
            self.name_label.config(text=self.name)
            self.class_label.config(text=self.task_class)
            
            # Update heat bar
            heat_percentage = max(0, min(100, self.heat))
            bar_width = int((heat_percentage / 100.0) * 98)  # 98 = 99 - 1 (padding)
            
            # Heat color based on intensity
            heat_color = self.get_heat_color(heat_percentage)
            self.heat_canvas.coords(self.heat_bar, 1, 1, 1 + bar_width, 7)
            self.heat_canvas.itemconfig(self.heat_bar, fill=heat_color)
            
            # Update decay status
            decay_percentage = max(0.0, min(1.0, self.decay))
            remaining = int((1.0 - decay_percentage) * 100)
            
            self.decay_label.config(text=f"{remaining}%")
            
            # Decay color and status
            decay_color, decay_status = self.get_decay_status(decay_percentage)
            self.decay_label.config(fg=decay_color)
            self.decay_status_label.config(text=decay_status)
            
            # Row urgency highlighting
            urgency_level = self.calculate_urgency()
            self.update_row_urgency(urgency_level)
            
        except Exception as e:
            print(f"Error updating sigil row display: {e}")
    
    def get_heat_color(self, heat: int) -> str:
        """Get color for heat level"""
        if heat < 20:
            return "#4CAF50"      # Green - low heat
        elif heat < 40:
            return "#8BC34A"      # Light green
        elif heat < 60:
            return "#FFC107"      # Yellow
        elif heat < 80:
            return "#FF9800"      # Orange
        else:
            return "#F44336"      # Red - high heat
    
    def get_decay_status(self, decay: float) -> tuple:
        """Get decay color and status text"""
        remaining = 1.0 - decay
        
        if remaining > 0.8:
            return "#00ff88", "Active"      # Green - fresh
        elif remaining > 0.6:
            return "#8BC34A", "Stable"      # Light green - stable  
        elif remaining > 0.4:
            return "#FFC107", "Fading"      # Yellow - fading
        elif remaining > 0.2:
            return "#FF9800", "Weak"        # Orange - weak
        else:
            return "#F44336", "Critical"    # Red - critical
    
    def calculate_urgency(self) -> float:
        """Calculate overall urgency level (0.0 - 1.0)"""
        # High heat + low remaining time = high urgency
        heat_factor = self.heat / 100.0
        decay_factor = self.decay  # Higher decay = more urgent
        
        urgency = (heat_factor * 0.6) + (decay_factor * 0.4)
        return min(1.0, urgency)
    
    def update_row_urgency(self, urgency: float):
        """Update row visual urgency indicators"""
        if urgency > 0.8:
            # Critical urgency - red highlight
            self.frame.config(bg="#331a1a", highlightbackground="#ff4444")
            self.name_label.config(fg="#ff8888")
        elif urgency > 0.6:
            # High urgency - orange highlight  
            self.frame.config(bg="#332a1a", highlightbackground="#ff8800")
            self.name_label.config(fg="#ffaa88")
        elif urgency > 0.4:
            # Medium urgency - yellow highlight
            self.frame.config(bg="#333a1a", highlightbackground="#ffcc00")
            self.name_label.config(fg="#ffcc88")
        else:
            # Normal - default colors
            self.frame.config(bg="#1a1a1a", highlightbackground="#333333")
            self.name_label.config(fg="#cccccc")
    
    def update_data(self, sigil_data: Dict):
        """Update sigil data and refresh display"""
        self.sigil_data = sigil_data
        self.symbol = sigil_data.get("symbol", self.symbol)
        self.name = sigil_data.get("name", self.name)
        self.task_class = sigil_data.get("class", self.task_class)
        self.heat = sigil_data.get("heat", self.heat)
        self.decay = sigil_data.get("decay", self.decay)
        
        self.update_display()
    
    def pack(self, **kwargs):
        """Pack the sigil row frame"""
        self.frame.pack(**kwargs)
    
    def destroy(self):
        """Destroy the sigil row"""
        self.frame.destroy()


class SigilOverlayPanel:
    """Main sigil overlay panel containing multiple sigil rows"""
    
    def __init__(self, parent, max_sigils=8):
        self.parent = parent
        self.max_sigils = max_sigils
        
        # Main container frame
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        
        # Current sigil rows
        self.sigil_rows = {}  # sigil_id -> SigilRow
        self.sigil_order = []  # Maintain display order
        
        # Task class definitions
        self.task_classes = {
            "memory": "🐝",      # Memory operations
            "analysis": "🐋",    # Deep analysis
            "synthesis": "🦋",   # Creative synthesis  
            "attention": "🦅",   # Focus operations
            "integration": "🐙", # Information integration
            "meta": "🦉",        # Meta-cognitive operations
            "action": "🐺",      # Action execution
            "monitor": "🐱",     # Monitoring operations
            "reasoning": "🦎",   # Logical reasoning
            "creativity": "🦚"   # Creative processes
        }
        
        self.setup_panel()
    
    def setup_panel(self):
        """Setup the main sigil overlay panel"""
        # Panel title
        title_frame = tk.Frame(self.frame, bg="#1a1a1a")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, text="🔮 Active Sigil Stream", 
                              font=("Arial", 12, "bold"),
                              bg="#1a1a1a", fg="#cccccc")
        title_label.pack(side=tk.LEFT)
        
        # Sigil count indicator
        self.count_label = tk.Label(title_frame, text="0 sigils", 
                                   font=("Arial", 9),
                                   bg="#1a1a1a", fg="#888888")
        self.count_label.pack(side=tk.RIGHT)
        
        # Scrollable sigil container
        self.setup_scrollable_container()
        
        # Status bar
        self.setup_status_bar()
    
    def setup_scrollable_container(self):
        """Setup scrollable container for sigil rows"""
        # Container frame with scrollbar
        container_frame = tk.Frame(self.frame, bg="#1a1a1a")
        container_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(container_frame, bg="#0a0a0a", 
                               highlightthickness=1, highlightbackground="#333333")
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=self.canvas.yview)
        
        # Scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0a0a0a")
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrolling components
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def setup_status_bar(self):
        """Setup status bar with sigil statistics"""
        status_frame = tk.Frame(self.frame, bg="#1a1a1a")
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(status_frame, text="No active sigils", 
                                    font=("Arial", 8),
                                    bg="#1a1a1a", fg="#888888")
        self.status_label.pack(side=tk.LEFT)
        
        self.urgency_label = tk.Label(status_frame, text="", 
                                     font=("Arial", 8),
                                     bg="#1a1a1a", fg="#888888")
        self.urgency_label.pack(side=tk.RIGHT)
    
    def update_sigils(self, sigils: List[Dict]):
        """Update the sigil display with new sigil data"""
        try:
            # Create sigil ID mapping
            new_sigil_ids = set()
            
            for i, sigil_data in enumerate(sigils):
                # Generate unique sigil ID
                sigil_id = f"{sigil_data.get('name', 'unknown')}_{i}"
                new_sigil_ids.add(sigil_id)
                
                # Normalize task class
                sigil_data = self.normalize_sigil_data(sigil_data)
                
                if sigil_id in self.sigil_rows:
                    # Update existing sigil
                    self.sigil_rows[sigil_id].update_data(sigil_data)
                else:
                    # Create new sigil row
                    self.create_sigil_row(sigil_id, sigil_data)
            
            # Remove outdated sigils
            self.cleanup_old_sigils(new_sigil_ids)
            
            # Update display
            self.refresh_display()
            
            # Update statistics
            self.update_statistics(sigils)
            
        except Exception as e:
            print(f"Error updating sigils: {e}")
    
    def normalize_sigil_data(self, sigil_data: Dict) -> Dict:
        """Normalize and validate sigil data"""
        # Ensure all required fields exist
        normalized = {
            "symbol": sigil_data.get("symbol", "◉"),
            "name": sigil_data.get("name", "Unknown Sigil"),
            "class": sigil_data.get("class", "monitor"),
            "heat": max(0, min(100, sigil_data.get("heat", 0))),
            "decay": max(0.0, min(1.0, sigil_data.get("decay", 0.0)))
        }
        
        # Map class to emoji if it's a string
        if isinstance(normalized["class"], str):
            normalized["class"] = self.task_classes.get(normalized["class"], "🔮")
        
        return normalized
    
    def create_sigil_row(self, sigil_id: str, sigil_data: Dict):
        """Create new sigil row"""
        # Limit number of sigils
        if len(self.sigil_rows) >= self.max_sigils:
            # Remove oldest sigil
            oldest_id = self.sigil_order.pop(0)
            if oldest_id in self.sigil_rows:
                self.sigil_rows[oldest_id].destroy()
                del self.sigil_rows[oldest_id]
        
        # Create new sigil row
        sigil_row = SigilRow(self.scrollable_frame, sigil_data)
        sigil_row.pack(fill=tk.X, padx=5, pady=2)
        
        self.sigil_rows[sigil_id] = sigil_row
        self.sigil_order.append(sigil_id)
    
    def cleanup_old_sigils(self, current_ids: set):
        """Remove sigils that are no longer active"""
        to_remove = []
        
        for sigil_id in self.sigil_rows:
            if sigil_id not in current_ids:
                to_remove.append(sigil_id)
        
        for sigil_id in to_remove:
            self.sigil_rows[sigil_id].destroy()
            del self.sigil_rows[sigil_id]
            if sigil_id in self.sigil_order:
                self.sigil_order.remove(sigil_id)
    
    def refresh_display(self):
        """Refresh the overall display"""
        # Update sigil count
        count = len(self.sigil_rows)
        self.count_label.config(text=f"{count} sigil{'s' if count != 1 else ''}")
        
        # Update canvas scroll region
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def update_statistics(self, sigils: List[Dict]):
        """Update status bar with sigil statistics"""
        if not sigils:
            self.status_label.config(text="No active sigils")
            self.urgency_label.config(text="")
            return
        
        # Calculate statistics
        total_heat = sum(s.get("heat", 0) for s in sigils)
        avg_heat = total_heat / len(sigils) if sigils else 0
        
        critical_count = sum(1 for s in sigils if s.get("decay", 0) > 0.8)
        active_count = len(sigils)
        
        # Status text
        status_text = f"Avg Heat: {avg_heat:.0f}% | Active: {active_count}"
        if critical_count > 0:
            status_text += f" | Critical: {critical_count}"
        
        self.status_label.config(text=status_text)
        
        # Urgency indicator
        if critical_count > 0:
            self.urgency_label.config(text="⚠️ Critical", fg="#ff4444")
        elif avg_heat > 70:
            self.urgency_label.config(text="🔥 High Load", fg="#ff8800")
        elif avg_heat > 40:
            self.urgency_label.config(text="⚡ Active", fg="#ffcc00")
        else:
            self.urgency_label.config(text="✓ Stable", fg="#88ff88")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def pack(self, **kwargs):
        """Pack the main frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the main frame"""
        self.frame.grid(**kwargs)


# Test function for standalone usage
def test_sigil_overlay():
    """Test the sigil overlay panel with sample data"""
    import random
    import time
    
    root = tk.Tk()
    root.title("DAWN Sigil Overlay Panel Test")
    root.configure(bg="#1a1a1a")
    root.geometry("400x600")
    
    # Create sigil overlay
    overlay = SigilOverlayPanel(root, max_sigils=6)
    overlay.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Sample sigil data
    sample_sigils = [
        {"symbol": "⚙️", "name": "SigilRecall", "class": "memory", "heat": 72, "decay": 0.33},
        {"symbol": "🔍", "name": "DeepAnalysis", "class": "analysis", "heat": 45, "decay": 0.15},
        {"symbol": "🌟", "name": "CreativeSynth", "class": "synthesis", "heat": 89, "decay": 0.67},
        {"symbol": "👁️", "name": "FocusLock", "class": "attention", "heat": 92, "decay": 0.82},
        {"symbol": "🔗", "name": "DataIntegrate", "class": "integration", "heat": 34, "decay": 0.21},
        {"symbol": "🧠", "name": "MetaMonitor", "class": "meta", "heat": 56, "decay": 0.45}
    ]
    
    def update_sigils():
        # Generate dynamic sigil data
        active_sigils = []
        
        for i, base_sigil in enumerate(sample_sigils):
            if random.random() > 0.3:  # 70% chance sigil is active
                sigil = base_sigil.copy()
                
                # Add some random variation
                sigil["heat"] = max(0, min(100, sigil["heat"] + random.randint(-20, 20)))
                sigil["decay"] = max(0.0, min(1.0, sigil["decay"] + random.uniform(-0.1, 0.1)))
                
                active_sigils.append(sigil)
        
        overlay.update_sigils(active_sigils)
        
        # Schedule next update
        root.after(2000, update_sigils)  # Update every 2 seconds
    
    # Start updates
    root.after(500, update_sigils)
    
    root.mainloop()


if __name__ == "__main__":
    test_sigil_overlay() 