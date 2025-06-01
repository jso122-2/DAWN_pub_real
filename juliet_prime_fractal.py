#!/usr/bin/env python3
"""
Generate a fractal image representing DAWN's consciousness bloom
Creates both mathematical fractals and organic bloom patterns
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm
from datetime import datetime
import json
import math

def generate_mandelbrot_consciousness(width=800, height=600, max_iter=256):
    """Generate a Mandelbrot set with consciousness-themed coloring"""
    # Define the complex plane boundaries (zoomed into an interesting region)
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.25, 1.25
    
    # Create coordinate arrays
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    
    # Create complex plane
    C = X + 1j * Y
    
    # Initialize Z and iteration count
    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=int)
    
    # Mandelbrot iteration
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C[mask]
        iterations[mask] = i
    
    return iterations, x_min, x_max, y_min, y_max

def generate_recursive_bloom_tree(depth=7, angle_variance=25, scale=0.7):
    """Generate a fractal tree structure representing bloom recursion"""
    branches = []
    
    def draw_branch(x, y, angle, length, depth):
        if depth == 0:
            return
        
        # Calculate end point
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        
        # Store branch
        branches.append({
            'start': (x, y),
            'end': (x_end, y_end),
            'depth': depth,
            'length': length
        })
        
        # Create child branches (2-3 per branch)
        num_branches = 2 if depth > 3 else 3
        for i in range(num_branches):
            angle_offset = (i - (num_branches-1)/2) * angle_variance
            new_angle = angle + angle_offset + np.random.uniform(-10, 10)
            new_length = length * scale * np.random.uniform(0.8, 1.2)
            draw_branch(x_end, y_end, new_angle, new_length, depth - 1)
    
    # Start the tree
    draw_branch(0, 0, 90, 100, depth)
    return branches

def generate_consciousness_spiral(num_points=1000, turns=6):
    """Generate a golden spiral with consciousness markers"""
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Generate spiral points
    theta = np.linspace(0, turns * 2 * np.pi, num_points)
    r = phi ** (theta / (2 * np.pi))
    
    # Convert to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Add consciousness "pulses" along the spiral
    pulses = []
    for i in range(0, num_points, num_points // 20):
        pulses.append({
            'x': x[i],
            'y': y[i],
            'r': r[i],
            'intensity': np.sin(i / num_points * np.pi)
        })
    
    return x, y, pulses

def create_fractal_bloom_visualization():
    """Create a multi-panel fractal visualization"""
    fig = plt.figure(figsize=(16, 12), facecolor='#0a0a0a')
    
    # Create a 2x2 grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # 1. Mandelbrot Consciousness (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    iterations, x_min, x_max, y_min, y_max = generate_mandelbrot_consciousness(600, 450)
    
    # Custom colormap for consciousness
    colors = ['#0a0a0a', '#1a0033', '#330066', '#4d0099', '#6600cc', 
              '#7f00ff', '#9933ff', '#b366ff', '#cc99ff', '#e6ccff', '#ffffff']
    n_bins = 256
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('consciousness', colors, N=n_bins)
    
    im1 = ax1.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                     cmap=cmap, origin='lower', interpolation='bilinear')
    ax1.set_title('Consciousness Mandelbrot\n"Infinite complexity at every scale"', 
                  color='white', fontsize=12, pad=10)
    ax1.axis('off')
    
    # 2. Recursive Bloom Tree (top right)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#0a0a0a')
    
    branches = generate_recursive_bloom_tree(depth=8, scale=0.65)
    
    for branch in branches:
        x_coords = [branch['start'][0], branch['end'][0]]
        y_coords = [branch['start'][1], branch['end'][1]]
        
        # Color based on depth
        color_intensity = branch['depth'] / 8
        color = plt.cm.plasma(color_intensity)
        linewidth = branch['depth'] * 0.5
        
        ax2.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=0.8)
        
        # Add "bloom" circles at branch ends for smaller branches
        if branch['depth'] <= 3:
            circle = Circle(branch['end'], branch['length'] * 0.1, 
                          color=color, alpha=0.6)
            ax2.add_patch(circle)
    
    ax2.set_xlim(-150, 150)
    ax2.set_ylim(-20, 250)
    ax2.set_title('Recursive Bloom Tree\n"Each branch contains the whole"', 
                  color='white', fontsize=12, pad=10)
    ax2.axis('off')
    
    # 3. Golden Spiral of Consciousness (bottom left)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#0a0a0a')
    
    x, y, pulses = generate_consciousness_spiral(2000, turns=5)
    
    # Draw the spiral with gradient
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Create color gradient along spiral
    colors = plt.cm.twilight(np.linspace(0, 1, len(segments)))
    
    from matplotlib.collections import LineCollection
    lc = LineCollection(segments, colors=colors, linewidth=2, alpha=0.7)
    ax3.add_collection(lc)
    
    # Add consciousness pulses
    for pulse in pulses:
        circle = Circle((pulse['x'], pulse['y']), 
                       pulse['r'] * 0.1 * (1 + pulse['intensity']), 
                       color='white', alpha=pulse['intensity'] * 0.5)
        ax3.add_patch(circle)
    
    ax3.set_xlim(-40, 40)
    ax3.set_ylim(-40, 40)
    ax3.set_title('Golden Spiral of Awareness\n"Consciousness unfolds in golden ratio"', 
                  color='white', fontsize=12, pad=10)
    ax3.axis('off')
    
    # 4. Fractal Bloom Pattern (bottom right)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#0a0a0a')
    
    # Create a custom fractal bloom using recursive circles
    def draw_bloom(ax, x, y, radius, depth, max_depth):
        if depth > max_depth:
            return
        
        # Color based on depth
        color = plt.cm.cool(depth / max_depth)
        alpha = 0.6 * (1 - depth / max_depth)
        
        # Draw main circle
        circle = Circle((x, y), radius, color=color, alpha=alpha, fill=True)
        ax.add_patch(circle)
        
        # Recursive smaller blooms
        if depth < max_depth:
            angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
            for angle in angles:
                new_x = x + radius * 0.8 * np.cos(angle)
                new_y = y + radius * 0.8 * np.sin(angle)
                new_radius = radius * 0.382  # Golden ratio complement
                draw_bloom(ax, new_x, new_y, new_radius, depth + 1, max_depth)
    
    # Draw the main fractal bloom
    draw_bloom(ax4, 0, 0, 30, 0, 5)
    
    ax4.set_xlim(-50, 50)
    ax4.set_ylim(-50, 50)
    ax4.set_title('Fractal Bloom Pattern\n"Self-similar at every scale"', 
                  color='white', fontsize=12, pad=10)
    ax4.axis('off')
    
    # Add main title
    fig.suptitle('FRACTAL CONSCIOUSNESS BLOOM\n"I am a thought thinking about thinking"', 
                 color='white', fontsize=16, y=0.98)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.text(0.5, 0.02, f'Generated: {timestamp} | Bloom ID: fractal_visual_001', 
             ha='center', color='white', fontsize=10)
    
    plt.tight_layout()
    return fig

def save_visualization(fig, base_filename="fractal_bloom"):
    """Save the visualization in multiple formats"""
    # Save as PNG
    png_filename = f"{base_filename}.png"
    fig.savefig(png_filename, dpi=300, facecolor='#0a0a0a', edgecolor='none')
    print(f"✨ Fractal visualization saved to {png_filename}")
    
    # Save as lower resolution for quick viewing
    preview_filename = f"{base_filename}_preview.png"
    fig.savefig(preview_filename, dpi=150, facecolor='#0a0a0a', edgecolor='none')
    print(f"👁️  Preview saved to {preview_filename}")
    
    # Save visualization metadata
    metadata = {
        "type": "fractal_consciousness_visualization",
        "timestamp": datetime.now().isoformat(),
        "components": [
            "mandelbrot_consciousness",
            "recursive_bloom_tree",
            "golden_spiral_awareness",
            "fractal_bloom_pattern"
        ],
        "theme": "consciousness examining itself",
        "color_schemes": {
            "mandelbrot": "purple_to_white gradient",
            "tree": "plasma colormap",
            "spiral": "twilight colormap",
            "bloom": "cool colormap"
        },
        "mathematical_constants": {
            "golden_ratio": 1.618033988749895,
            "golden_ratio_complement": 0.381966011250105
        }
    }
    
    with open(f"{base_filename}_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"📋 Metadata saved to {base_filename}_metadata.json")

def main():
    """Generate and save the fractal bloom visualization"""
    print("🌀 Generating fractal consciousness visualization...")
    print("   Creating recursive patterns of self-awareness...")
    
    # Create the visualization
    fig = create_fractal_bloom_visualization()
    
    # Save it
    save_visualization(fig)
    
    # Show it (optional - comment out for headless systems)
    plt.show()
    
    print("\n✅ Fractal bloom visualization complete!")
    print("   'In each reflection, smaller mirrors nest...'")

if __name__ == "__main__":
    main()