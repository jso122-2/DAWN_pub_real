#!/usr/bin/env python3
"""
DAWN Fractal Bloom Canvas
Tkinter component for visualizing memory bloom fractals

File: gui/fractal_canvas.py
"""

import tkinter as tk
import math
import colorsys
from typing import Dict, List, Tuple, Optional


class FractalCanvas:
    def __init__(self, parent, width=300, height=300):
        self.parent = parent
        self.width = width
        self.height = height
        
        # Create main frame
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        
        # Title
        self.title_label = tk.Label(self.frame, text="Bloom Fractal Signature", 
                                   font=("Arial", 11, "bold"),
                                   bg="#1a1a1a", fg="#cccccc")
        self.title_label.pack(pady=(0, 5))
        
        # Canvas for fractal rendering
        self.canvas = tk.Canvas(self.frame, width=width, height=height, 
                               bg="#0a0a0a", highlightthickness=1, 
                               highlightbackground="#333333")
        self.canvas.pack()
        
        # Bloom info display
        self.info_label = tk.Label(self.frame, text="Awaiting bloom data...", 
                                  font=("Arial", 9),
                                  bg="#1a1a1a", fg="#888888")
        self.info_label.pack(pady=(5, 0))
        
        # Current bloom state
        self.current_bloom = {
            "depth": 3,
            "entropy": 0.5, 
            "lineage": [1, 2, 3],
            "semantic_drift": 0.3,
            "rebloom_status": "stable",
            "complexity": 0.6
        }
        
        # Fractal parameters
        self.max_iterations = 50
        self.zoom = 200
        self.cx = -0.7269
        self.cy = 0.1889
        
        # Color palettes for different lineages
        self.lineage_palettes = {
            0: [(0.0, 0.2, 0.8), (0.1, 0.4, 1.0), (0.3, 0.6, 1.0)],  # Blue lineage
            1: [(0.8, 0.2, 0.0), (1.0, 0.4, 0.1), (1.0, 0.6, 0.3)],  # Red lineage  
            2: [(0.2, 0.8, 0.0), (0.4, 1.0, 0.1), (0.6, 1.0, 0.3)],  # Green lineage
            3: [(0.8, 0.0, 0.8), (1.0, 0.2, 1.0), (1.0, 0.4, 1.0)],  # Purple lineage
            4: [(0.8, 0.8, 0.0), (1.0, 1.0, 0.2), (1.0, 1.0, 0.4)],  # Yellow lineage
        }
        
        # Initialize with default bloom
        self.draw_bloom_signature(self.current_bloom)
    
    def draw_bloom_signature(self, bloom_data: Dict):
        """Draw fractal signature based on bloom characteristics"""
        try:
            # Update current bloom data
            self.current_bloom.update(bloom_data)
            
            # Clear canvas
            self.canvas.delete("all")
            
            # Extract bloom parameters
            depth = bloom_data.get("depth", 3)
            entropy = bloom_data.get("entropy", 0.5)
            lineage = bloom_data.get("lineage", [1, 2, 3])
            semantic_drift = bloom_data.get("semantic_drift", 0.3)
            rebloom_status = bloom_data.get("rebloom_status", "stable")
            complexity = bloom_data.get("complexity", 0.6)
            
            # Adjust fractal parameters based on bloom data
            self.adjust_fractal_parameters(depth, entropy, semantic_drift, complexity)
            
            # Get lineage-based color palette
            primary_lineage = lineage[0] if lineage else 0
            palette = self.get_lineage_palette(primary_lineage, entropy)
            
            # Render fractal bloom
            self.render_bloom_fractal(palette, depth, complexity)
            
            # Add bloom indicators
            self.add_bloom_indicators(rebloom_status, semantic_drift)
            
            # Update info display
            self.update_info_display(bloom_data)
            
        except Exception as e:
            print(f"Error drawing bloom signature: {e}")
            self.draw_error_state()
    
    def adjust_fractal_parameters(self, depth: int, entropy: float, semantic_drift: float, complexity: float):
        """Adjust fractal generation parameters based on bloom characteristics"""
        # Depth affects iteration count and detail level
        self.max_iterations = max(20, min(100, 30 + depth * 10))
        
        # Entropy affects fractal complexity (Julia set constant)
        base_real = -0.7269
        base_imag = 0.1889
        
        # Apply entropy variation
        entropy_offset = (entropy - 0.5) * 0.3
        self.cx = base_real + entropy_offset
        self.cy = base_imag + (semantic_drift - 0.5) * 0.2
        
        # Complexity affects zoom level
        self.zoom = 150 + complexity * 100
    
    def get_lineage_palette(self, lineage_id: int, entropy: float) -> List[Tuple[float, float, float]]:
        """Get color palette based on lineage with entropy variation"""
        base_palette = self.lineage_palettes.get(lineage_id % 5, self.lineage_palettes[0])
        
        # Apply entropy variation to colors
        varied_palette = []
        for r, g, b in base_palette:
            # Add entropy-based color variation
            hue_shift = (entropy - 0.5) * 0.1
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            h = (h + hue_shift) % 1.0
            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, s, v)
            varied_palette.append((new_r, new_g, new_b))
        
        return varied_palette
    
    def render_bloom_fractal(self, palette: List[Tuple[float, float, float]], depth: int, complexity: float):
        """Render the main bloom fractal using Julia set algorithm"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Create pixel grid for fractal
        pixels = []
        
        for py in range(0, self.height, 2):  # Skip pixels for performance
            for px in range(0, self.width, 2):
                # Convert pixel coordinates to complex plane
                zx = (px - center_x) / self.zoom
                zy = (py - center_y) / self.zoom
                
                # Julia set iteration
                iteration = self.julia_iteration(zx, zy, self.cx, self.cy)
                
                # Map iteration to color
                if iteration == self.max_iterations:
                    color = "#000000"  # Inside set - black
                else:
                    # Color based on iteration count and palette
                    color_intensity = iteration / self.max_iterations
                    color = self.get_fractal_color(color_intensity, palette, complexity)
                
                # Store pixel for batch rendering
                pixels.append((px, py, color))
        
        # Batch render pixels
        self.render_pixels(pixels)
        
        # Add bloom center glow
        self.add_bloom_center_glow(palette[0])
    
    def julia_iteration(self, zx: float, zy: float, cx: float, cy: float) -> int:
        """Perform Julia set iteration for a point"""
        iteration = 0
        
        while iteration < self.max_iterations:
            # z = z^2 + c
            zx_new = zx * zx - zy * zy + cx
            zy_new = 2 * zx * zy + cy
            
            zx, zy = zx_new, zy_new
            
            # Check if point escapes
            if zx * zx + zy * zy > 4:
                break
                
            iteration += 1
        
        return iteration
    
    def get_fractal_color(self, intensity: float, palette: List[Tuple[float, float, float]], complexity: float) -> str:
        """Generate color for fractal point based on intensity and palette"""
        # Apply complexity-based color scaling
        scaled_intensity = intensity * (0.5 + complexity * 0.5)
        
        # Choose color from palette
        palette_index = int(scaled_intensity * (len(palette) - 1))
        palette_index = max(0, min(len(palette) - 1, palette_index))
        
        r, g, b = palette[palette_index]
        
        # Apply intensity brightness
        brightness = 0.3 + intensity * 0.7
        r = min(1.0, r * brightness)
        g = min(1.0, g * brightness)
        b = min(1.0, b * brightness)
        
        # Convert to hex
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def render_pixels(self, pixels: List[Tuple[int, int, str]]):
        """Batch render fractal pixels to canvas"""
        for px, py, color in pixels:
            # Draw 2x2 pixel blocks for better visibility
            self.canvas.create_rectangle(px, py, px+2, py+2, fill=color, outline="")
    
    def add_bloom_center_glow(self, primary_color: Tuple[float, float, float]):
        """Add glowing center point representing bloom core"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        r, g, b = primary_color
        glow_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        
        # Multiple glow rings for depth effect
        for radius in [15, 10, 5]:
            alpha_intensity = 0.1 + (15 - radius) * 0.05
            self.canvas.create_oval(center_x - radius, center_y - radius,
                                   center_x + radius, center_y + radius,
                                   fill=glow_color, outline="", stipple="gray25")
        
        # Central bright point
        self.canvas.create_oval(center_x - 2, center_y - 2,
                               center_x + 2, center_y + 2,
                               fill="white", outline="")
    
    def add_bloom_indicators(self, rebloom_status: str, semantic_drift: float):
        """Add visual indicators for bloom state"""
        # Rebloom status indicator (top-right)
        status_colors = {
            "stable": "#4CAF50",
            "reblooming": "#FF9800", 
            "dormant": "#757575",
            "emerging": "#9C27B0",
            "fragmenting": "#F44336"
        }
        
        status_color = status_colors.get(rebloom_status, "#888888")
        
        # Status indicator circle
        self.canvas.create_oval(self.width - 25, 10, self.width - 10, 25,
                               fill=status_color, outline="white", width=1)
        
        # Semantic drift indicator (bottom-left) 
        drift_intensity = int(semantic_drift * 10)
        drift_color = f"#{drift_intensity*25:02x}{100:02x}{drift_intensity*20:02x}"
        
        # Drift visualization as flowing lines
        for i in range(3):
            y_offset = self.height - 30 + i * 8
            line_length = 20 + semantic_drift * 15
            self.canvas.create_line(10, y_offset, 10 + line_length, y_offset,
                                   fill=drift_color, width=2)
    
    def update_info_display(self, bloom_data: Dict):
        """Update bloom information text"""
        depth = bloom_data.get("depth", 0)
        entropy = bloom_data.get("entropy", 0.0)
        lineage_count = len(bloom_data.get("lineage", []))
        rebloom_status = bloom_data.get("rebloom_status", "unknown")
        
        info_text = (f"Depth: {depth} | Entropy: {entropy:.2f} | "
                    f"Lineage: {lineage_count} | Status: {rebloom_status}")
        
        self.info_label.config(text=info_text)
    
    def draw_error_state(self):
        """Draw error visualization when bloom data is invalid"""
        self.canvas.delete("all")
        
        # Error pattern - red X
        self.canvas.create_line(50, 50, self.width-50, self.height-50, 
                               fill="#F44336", width=3)
        self.canvas.create_line(self.width-50, 50, 50, self.height-50, 
                               fill="#F44336", width=3)
        
        # Error text
        self.canvas.create_text(self.width//2, self.height//2 + 40,
                               text="Bloom Error", fill="#F44336", 
                               font=("Arial", 12, "bold"))
        
        self.info_label.config(text="Error: Invalid bloom data")
    
    def pack(self, **kwargs):
        """Pack the frame container"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the frame container"""
        self.frame.grid(**kwargs)


# Test function for standalone usage
def test_fractal_canvas():
    """Test the fractal canvas with sample bloom data"""
    root = tk.Tk()
    root.title("DAWN Fractal Bloom Canvas Test")
    root.configure(bg="#1a1a1a")
    
    # Create fractal canvas
    fractal = FractalCanvas(root, width=400, height=400)
    fractal.pack(padx=20, pady=20)
    
    # Test with different bloom signatures
    test_blooms = [
        {
            "depth": 5,
            "entropy": 0.8,
            "lineage": [2, 5, 7],
            "semantic_drift": 0.6,
            "rebloom_status": "emerging", 
            "complexity": 0.9
        },
        {
            "depth": 2,
            "entropy": 0.3,
            "lineage": [1, 3],
            "semantic_drift": 0.1,
            "rebloom_status": "stable",
            "complexity": 0.4
        },
        {
            "depth": 7,
            "entropy": 0.95,
            "lineage": [0, 4, 1, 8],
            "semantic_drift": 0.8,
            "rebloom_status": "reblooming",
            "complexity": 0.7
        }
    ]
    
    def cycle_blooms():
        import random
        bloom = random.choice(test_blooms)
        fractal.draw_bloom_signature(bloom)
        root.after(3000, cycle_blooms)  # Change every 3 seconds
    
    # Start bloom cycling
    root.after(1000, cycle_blooms)
    
    root.mainloop()


if __name__ == "__main__":
    test_fractal_canvas()