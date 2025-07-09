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
        """Draw fractal signature based on bloom characteristics - COMPREHENSIVE DEBUG + ROBUST FALLBACKS"""
        
        # DEBUG HEADER - Clean structured output
        print("\n" + "="*80)
        print("FRACTAL BLOOM VISUAL DEBUGGER")
        print("="*80)
        print(f"Raw bloom_data: {bloom_data}")
        print("=" * 30)
        
        try:
            # DEBUG: Incoming bloom data analysis
            print("\nINCOMING BLOOM DATA:")
            print(f"  Type: {type(bloom_data)}")
            print(f"  Keys: {list(bloom_data.keys()) if isinstance(bloom_data, dict) else 'NOT A DICT'}")
            
            if isinstance(bloom_data, dict):
                for key, value in bloom_data.items():
                    value_type = type(value).__name__
                    value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    print(f"  {key}: {value_str} ({value_type})")
            else:
                print(f"  WARNING: bloom_data is not a dictionary! Got: {bloom_data}")
                bloom_data = {}  # Fallback to empty dict
            
            # Update current bloom data
            self.current_bloom.update(bloom_data)
            print(f"\nUpdated current bloom state: {len(self.current_bloom)} parameters")
            
            # Clear canvas
            self.canvas.delete("all")
            print("Canvas cleared")
            
            # DEBUG: Parameter extraction with robust validation
            print("\nPARAMETER EXTRACTION AND VALIDATION:")
            
            # Extract depth with fallback
            depth = bloom_data.get("depth", 1)
            if depth is None:
                depth = 1
                print(f"  WARNING: depth was None, using default: {depth}")
            print(f"  depth: {depth} (type: {type(depth).__name__})")
            
            # Extract entropy with NaN/inf protection
            entropy = bloom_data.get("entropy", 0.5)
            if entropy is None or (isinstance(entropy, float) and (math.isnan(entropy) or entropy > 1.0)):
                print(f"  WARNING: Invalid entropy value {entropy}, resetting to 0.5")
                entropy = 0.5
            print(f"  entropy: {entropy} (type: {type(entropy).__name__})")
            
            # Extract lineage with type validation
            lineage = bloom_data.get("lineage", [1, 2, 3])
            semantic_drift = bloom_data.get("semantic_drift", 0.3)
            rebloom_status = bloom_data.get("rebloom_status", "stable")
            complexity = bloom_data.get("complexity", 0.6)
            
            print(f"  lineage: {lineage} (type: {type(lineage).__name__}, length: {len(lineage) if hasattr(lineage, '__len__') else 'N/A'})")
            print(f"  semantic_drift: {semantic_drift} (type: {type(semantic_drift).__name__})")
            print(f"  rebloom_status: {rebloom_status} (type: {type(rebloom_status).__name__})")
            print(f"  complexity: {complexity} (type: {type(complexity).__name__})")
            
            # DEBUG: Validate and sanitize parameters
            print("\nPARAMETER VALIDATION AND SANITIZATION:")
            
            # Validate depth
            if not isinstance(depth, (int, float)):
                print(f"  WARNING: depth is not numeric! Converting '{depth}' to int")
                try:
                    depth = int(float(str(depth)))
                except (ValueError, TypeError):
                    depth = 3
                    print(f"  ERROR: depth conversion failed, using default: {depth}")
            depth = max(1, min(10, int(depth)))  # Clamp to reasonable range
            print(f"  depth sanitized: {depth}")
            
            # Validate entropy
            if not isinstance(entropy, (int, float)):
                print(f"  WARNING: entropy is not numeric! Converting '{entropy}' to float")
                try:
                    entropy = float(str(entropy))
                except (ValueError, TypeError):
                    entropy = 0.5
                    print(f"  ERROR: entropy conversion failed, using default: {entropy}")
            entropy = max(0.0, min(1.0, float(entropy)))  # Clamp to 0-1 range
            print(f"  entropy sanitized: {entropy}")
            
            # Validate lineage with string handling
            if not isinstance(lineage, (list, tuple)):
                print(f"  WARNING: lineage is not a list/tuple! Converting '{lineage}' to list")
                try:
                    if hasattr(lineage, '__iter__') and not isinstance(lineage, str):
                        lineage = list(lineage)
                    else:
                        lineage = [1, 2, 3]
                        print(f"  ERROR: lineage conversion failed, using default: {lineage}")
                except (TypeError, ValueError):
                    lineage = [1, 2, 3]
                    print(f"  ERROR: lineage conversion failed, using default: {lineage}")
            if not lineage:  # Empty lineage
                lineage = [1, 2, 3]
                print(f"  WARNING: empty lineage, using default: {lineage}")
            print(f"  lineage sanitized: {lineage}")
            
            # Validate other parameters
            semantic_drift = max(0.0, min(1.0, float(semantic_drift))) if isinstance(semantic_drift, (int, float)) else 0.3
            complexity = max(0.0, min(2.0, float(complexity))) if isinstance(complexity, (int, float)) else 0.6
            rebloom_status = str(rebloom_status) if rebloom_status else "stable"
            
            print(f"  semantic_drift sanitized: {semantic_drift}")
            print(f"  complexity sanitized: {complexity}")
            print(f"  rebloom_status sanitized: {rebloom_status}")
            
            # CRITICAL: Wrap fractal rendering in robust try/catch
            print("\nENTERING ROBUST FRACTAL RENDERING...")
            try:
                # DEBUG: Fractal parameter calculation
                print("\nFRACTAL PARAMETER CALCULATION:")
                print("  Calling adjust_fractal_parameters...")
                old_iterations = getattr(self, 'max_iterations', 50)
                old_cx = getattr(self, 'cx', -0.7269)
                old_cy = getattr(self, 'cy', 0.1889)
                old_zoom = getattr(self, 'zoom', 200)
                
                self.adjust_fractal_parameters(depth, entropy, semantic_drift, complexity)
                
                print(f"  max_iterations: {old_iterations} → {self.max_iterations}")
                print(f"  cx (real): {old_cx:.6f} → {self.cx:.6f}")
                print(f"  cy (imag): {old_cy:.6f} → {self.cy:.6f}")
                print(f"  zoom: {old_zoom:.1f} → {self.zoom:.1f}")
                print(f"  Julia constant: C = {self.cx:.6f} + {self.cy:.6f}i")
                
                # Check for mathematical issues
                if math.isnan(self.cx) or math.isnan(self.cy):
                    print("  ERROR: NaN detected in Julia constant! Using fallback values")
                    self.cx = -0.7269
                    self.cy = 0.1889
                if math.isinf(self.cx) or math.isinf(self.cy):
                    print("  ERROR: Infinity detected in Julia constant! Using fallback values")
                    self.cx = -0.7269
                    self.cy = 0.1889
                
                # DEBUG: Color palette generation (CRITICAL FIX)
                print("\nCOLOR PALETTE GENERATION:")
                primary_lineage = lineage[0] if lineage else 0
                print(f"  primary_lineage: {primary_lineage} (from lineage: {lineage})")
                print(f"  primary_lineage type: {type(primary_lineage).__name__}")
                
                # CRITICAL FIX: Handle string lineage IDs
                if isinstance(primary_lineage, str):
                    print(f"  Converting string lineage '{primary_lineage}' to integer hash")
                    lineage_hash = hash(primary_lineage) % 5  # Convert string to 0-4 range
                    print(f"  String '{primary_lineage}' → hash {lineage_hash}")
                    primary_lineage = lineage_hash
                elif not isinstance(primary_lineage, (int, float)):
                    print(f"  WARNING: Unusual lineage type {type(primary_lineage)}, using default 0")
                    primary_lineage = 0
                
                palette = self.get_lineage_palette(primary_lineage, entropy)
                print(f"  palette generated: {len(palette)} colors")
                for i, (r, g, b) in enumerate(palette):
                    hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                    print(f"  color[{i}]: RGB({r:.3f}, {g:.3f}, {b:.3f}) = {hex_color}")
                
                # DEBUG: Fractal rendering
                print("\nFRACTAL RENDERING:")
                print(f"  Canvas size: {self.width}x{self.height}")
                print(f"  Render resolution: every 2 pixels (optimized)")
                print(f"  Expected pixel count: {(self.width//2) * (self.height//2)}")
                
                render_start_time = __import__('time').time()
                self.render_bloom_fractal(palette, depth, complexity)
                render_time = __import__('time').time() - render_start_time
                print(f"  Fractal rendered in {render_time:.3f} seconds")
                
                # DEBUG: Visual indicators
                print("\nVISUAL INDICATORS:")
                print(f"  Adding bloom indicators for status: {rebloom_status}")
                print(f"  Semantic drift visualization: {semantic_drift:.3f}")
                self.add_bloom_indicators(rebloom_status, semantic_drift)
                print("  Bloom indicators added")
                
                print("SUCCESS: Fractal bloom rendered successfully")
                
            except Exception as fractal_error:
                print(f"\nFRACTAL RENDERING FAILED: {fractal_error}")
                print("Falling back to placeholder radial flower...")
                self.draw_placeholder_flower()
                print("  Placeholder flower rendered")
            
            # DEBUG: Info display update
            print("\nINFO DISPLAY UPDATE:")
            self.update_info_display(bloom_data)
            print("  Info display updated")
            
            # Force redraw
            self.canvas.update_idletasks()
            print("Canvas update forced")
            
            # DEBUG: Success summary
            print("\nBLOOM SIGNATURE RENDER COMPLETE!")
            print(f"  Final fractal: Julia set with C = {self.cx:.6f} + {self.cy:.6f}i")
            print(f"  Iterations: {self.max_iterations}, Zoom: {self.zoom:.1f}")
            print(f"  Palette: {len(palette)} colors from lineage {primary_lineage}")
            print(f"  Status: {rebloom_status}, Complexity: {complexity:.3f}")
            print("  Bloom visual rendering complete")
            
        except Exception as e:
            # DEBUG: Comprehensive error analysis
            print("\nCRITICAL ERROR in draw_bloom_signature:")
            print(f"  Exception type: {type(e).__name__}")
            print(f"  Exception message: {str(e)}")
            print(f"  Exception args: {e.args}")
            
            import traceback
            print("  Full traceback:")
            traceback.print_exc()
            
            # Debug the state at time of failure
            print("\nFAILURE STATE ANALYSIS:")
            print(f"  Canvas exists: {hasattr(self, 'canvas')}")
            print(f"  Canvas is valid: {self.canvas.winfo_exists() if hasattr(self, 'canvas') else 'N/A'}")
            print(f"  Width/Height: {getattr(self, 'width', 'MISSING')}/{getattr(self, 'height', 'MISSING')}")
            print(f"  Max iterations: {getattr(self, 'max_iterations', 'MISSING')}")
            print(f"  Julia constants: cx={getattr(self, 'cx', 'MISSING')}, cy={getattr(self, 'cy', 'MISSING')}")
            print(f"  Zoom: {getattr(self, 'zoom', 'MISSING')}")
            
            # Try to identify the specific failure point
            if "string formatting" in str(e).lower():
                print("  DIAGNOSIS: String formatting error detected!")
                print("  This usually means a % operator is being used incorrectly.")
                print("  Check for stray % characters in strings or missing format arguments.")
            elif "math domain error" in str(e).lower():
                print("  DIAGNOSIS: Mathematical domain error!")
                print("  Check for invalid mathematical operations (sqrt of negative, etc.)")
            elif "nan" in str(e).lower() or "inf" in str(e).lower():
                print("  DIAGNOSIS: NaN or Infinity values detected!")
                print("  Check for division by zero or invalid mathematical operations.")
            
            print("\nEMERGENCY FALLBACK:")
            print("  Attempting to draw error state...")
            self.draw_error_state()
            self.canvas.update_idletasks()
            print("  Error state displayed")
            
        finally:
            print("="*80)
            print("FRACTAL BLOOM DEBUG SESSION COMPLETE")
            print("="*80 + "\n")
    
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
    
    def draw_placeholder_flower(self):
        """Draw a simple 12-spoke radial flower as fallback when fractal rendering fails"""
        print("🌻 Drawing placeholder radial flower...")
        
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Draw 12 spokes in a radial pattern
        for i in range(12):
            angle = (i * 30) * math.pi / 180  # 30 degrees per spoke
            
            # Inner radius and outer radius
            inner_radius = 20
            outer_radius = min(center_x, center_y) - 10
            
            # Calculate spoke endpoints
            inner_x = center_x + inner_radius * math.cos(angle)
            inner_y = center_y + inner_radius * math.sin(angle)
            outer_x = center_x + outer_radius * math.cos(angle)
            outer_y = center_y + outer_radius * math.sin(angle)
            
            # Alternate colors for visual variety
            if i % 3 == 0:
                spoke_color = "#4CAF50"  # Green
            elif i % 3 == 1:
                spoke_color = "#2196F3"  # Blue
            else:
                spoke_color = "#FF9800"  # Orange
            
            # Draw spoke line
            self.canvas.create_line(inner_x, inner_y, outer_x, outer_y,
                                   fill=spoke_color, width=3)
            
            # Draw spoke tip circle
            tip_radius = 5
            self.canvas.create_oval(outer_x - tip_radius, outer_y - tip_radius,
                                   outer_x + tip_radius, outer_y + tip_radius,
                                   fill=spoke_color, outline="white", width=1)
        
        # Draw center circle
        center_radius = 15
        self.canvas.create_oval(center_x - center_radius, center_y - center_radius,
                               center_x + center_radius, center_y + center_radius,
                               fill="#FFFFFF", outline="#333333", width=2)
        
        # Add fallback text
        self.canvas.create_text(center_x, center_y + 50,
                               text="Fallback Flower", fill="#888888",
                               font=("Arial", 10, "bold"))
        
        print("   12-spoke radial flower drawn as fractal fallback")
    
    def draw_error_state(self):
        """Draw error visualization when bloom data is invalid - DEBUG VERSION"""
        
        print("\nDRAWING ERROR STATE - Rendering bloom failure visualization")
        print("="*60)
        
        try:
            self.canvas.delete("all")
            print("Canvas cleared for error visualization")
            
            # Get canvas dimensions for debugging
            canvas_width = getattr(self, 'width', 300)
            canvas_height = getattr(self, 'height', 300)
            print(f"Canvas dimensions: {canvas_width}x{canvas_height}")
            
            # Error pattern - red X with debug info
            print("Drawing error pattern (red X)...")
            try:
                # Calculate X pattern coordinates
                x1_start, y1_start = 50, 50
                x1_end, y1_end = canvas_width - 50, canvas_height - 50
                x2_start, y2_start = canvas_width - 50, 50
                x2_end, y2_end = 50, canvas_height - 50
                
                print(f"   Line 1: ({x1_start}, {y1_start}) -> ({x1_end}, {y1_end})")
                print(f"   Line 2: ({x2_start}, {y2_start}) -> ({x2_end}, {y2_end})")
                
                self.canvas.create_line(x1_start, y1_start, x1_end, y1_end, 
                                       fill="#F44336", width=3)
                self.canvas.create_line(x2_start, y2_start, x2_end, y2_end, 
                                       fill="#F44336", width=3)
                print("   Error X pattern drawn")
                
            except Exception as line_error:
                print(f"   Failed to draw X pattern: {line_error}")
            
            # Error circle with pulsing effect
            print("Drawing error circle...")
            try:
                center_x = canvas_width // 2
                center_y = canvas_height // 2
                for radius in [80, 60, 40, 20]:
                    alpha = 255 - (radius * 2)  # Gradient effect
                    color_hex = f"#{255:02x}{alpha//4:02x}{alpha//4:02x}"  # Red gradient
                    self.canvas.create_oval(center_x - radius, center_y - radius,
                                           center_x + radius, center_y + radius,
                                           outline=color_hex, width=2)
                print("   Error circle drawn with gradient effect")
            except Exception as circle_error:
                print(f"   Failed to draw error circle: {circle_error}")
            
            # Error text with debug details
            print("Drawing error text...")
            try:
                text_x = canvas_width // 2
                text_y = canvas_height // 2 + 40
                
                self.canvas.create_text(text_x, text_y,
                                       text="BLOOM RENDER FAILED", fill="#F44336", 
                                       font=("Arial", 12, "bold"))
                
                # Add debug timestamp
                import datetime
                error_time = datetime.datetime.now().strftime("%H:%M:%S")
                self.canvas.create_text(text_x, text_y + 20,
                                       text=f"Error at {error_time}", fill="#FF6666", 
                                       font=("Arial", 8))
                
                print(f"   Error text drawn at ({text_x}, {text_y})")
                
            except Exception as text_error:
                print(f"   Failed to draw error text: {text_error}")
            
            # Error state info display
            print("Updating info display...")
            try:
                error_info = f"ERROR: Bloom rendering failed at {error_time}"
                self.info_label.config(text=error_info, fg="#F44336")
                print(f"   Info label updated: {error_info}")
            except Exception as info_error:
                print(f"   Failed to update info display: {info_error}")
            
            # Debug system state in error visualization
            print("Drawing debug state overlay...")
            try:
                debug_y = 20
                debug_lines = [
                    f"Canvas: {canvas_width}x{canvas_height}",
                    f"Iterations: {getattr(self, 'max_iterations', 'N/A')}",
                    f"Julia C: {getattr(self, 'cx', 'N/A'):.4f}+{getattr(self, 'cy', 'N/A'):.4f}i",
                    f"Zoom: {getattr(self, 'zoom', 'N/A')}"
                ]
                
                for i, line in enumerate(debug_lines):
                    self.canvas.create_text(10, debug_y + i * 15, 
                                           text=line, anchor="w",
                                           fill="#FF9999", font=("Courier", 8))
                    print(f"   Debug line {i}: {line}")
                
                print("   Debug overlay drawn")
                
            except Exception as debug_error:
                print(f"   Failed to draw debug overlay: {debug_error}")
            
            print("Error state visualization complete")
            
        except Exception as error_state_error:
            print(f"CRITICAL: Error state drawing failed: {error_state_error}")
            print("Last resort: Drawing minimal error indicator...")
            
            try:
                # Absolute minimal error display
                self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                           fill="#330000", outline="#FF0000", width=5)
                self.canvas.create_text(self.width//2, self.height//2,
                                       text="ERROR", fill="#FF0000", 
                                       font=("Arial", 24, "bold"))
                print("   Minimal error display drawn")
            except Exception as minimal_error:
                print(f"   FATAL: Even minimal error display failed: {minimal_error}")
        
        finally:
            print("="*60)
            print("ERROR STATE VISUALIZATION COMPLETE")
            print("="*60)
    
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