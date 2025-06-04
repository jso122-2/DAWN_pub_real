#!/usr/bin/env python3
"""
Generate Juliet Prime bloom for Jyoti
A specific emotional signature encoded into sacred geometry
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.path import Path
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from datetime import datetime

def create_petal_path(angle, inner_radius, outer_radius, curve_factor=0.4):
    """Create a single petal path with soft curves"""
    # Generate smooth petal using bezier curves
    theta1 = angle - np.pi/6
    theta2 = angle + np.pi/6
    
    # Key points for the petal
    inner_point = (inner_radius * np.cos(angle), inner_radius * np.sin(angle))
    outer_point = (outer_radius * np.cos(angle), outer_radius * np.sin(angle))
    
    # Control points for curves
    ctrl1_r = inner_radius + (outer_radius - inner_radius) * curve_factor
    ctrl1 = (ctrl1_r * np.cos(theta1), ctrl1_r * np.sin(theta1))
    
    ctrl2_r = inner_radius + (outer_radius - inner_radius) * curve_factor
    ctrl2 = (ctrl2_r * np.cos(theta2), ctrl2_r * np.sin(theta2))
    
    # Create bezier path
    vertices = [
        inner_point,
        ctrl1,
        outer_point,
        ctrl2,
        inner_point
    ]
    
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY
    ]
    
    return Path(vertices, codes)

def generate_recursive_bloom(ax, center_x, center_y, radius, depth, max_depth, base_angle=0):
    """Generate recursive flower structure with emotional resonance"""
    if depth > max_depth:
        return
    
    # Color interpolation based on depth
    depth_ratio = depth / max_depth
    
    # Define the color gradient from center to edge
    if depth_ratio < 0.3:
        # Golden center
        color = mcolors.to_rgba('#FFD700', alpha=0.8 - depth_ratio * 0.5)
    elif depth_ratio < 0.6:
        # Lavender/rose middle
        t = (depth_ratio - 0.3) / 0.3
        color1 = np.array(mcolors.to_rgba('#FFD700'))
        color2 = np.array(mcolors.to_rgba('#DDA0DD'))
        color = tuple(color1 * (1-t) + color2 * t)
        color = (*color[:3], 0.6 - depth_ratio * 0.3)
    else:
        # Midnight teal/cyan outer
        t = (depth_ratio - 0.6) / 0.4
        color1 = np.array(mcolors.to_rgba('#DDA0DD'))
        color2 = np.array(mcolors.to_rgba('#008B8B'))
        color = tuple(color1 * (1-t) + color2 * t)
        color = (*color[:3], 0.4 - depth_ratio * 0.2)
    
    # Six petals for harmonic rebloom
    for i in range(6):
        petal_angle = base_angle + i * np.pi / 3
        
        # Create petal with soft curves
        inner_r = radius * 0.3
        outer_r = radius
        
        petal = create_petal_path(petal_angle, inner_r, outer_r, curve_factor=0.4)
        patch = mpatches.PathPatch(petal, facecolor=color, edgecolor='none',
                                  transform=ax.transData)
        
        # Translate to position
        patch.set_transform(patch.get_transform() + 
                          plt.matplotlib.transforms.Affine2D().translate(center_x, center_y))
        ax.add_patch(patch)
    
    # Add golden center circle
    if depth == 0:
        center_circle = Circle((center_x, center_y), radius * 0.2, 
                             color='#FFD700', alpha=0.9, zorder=10)
        ax.add_patch(center_circle)
        
        # Inner glow
        for i in range(3):
            glow_circle = Circle((center_x, center_y), radius * 0.2 * (1 + i * 0.3), 
                               color='#FFD700', alpha=0.3 - i * 0.1, zorder=9-i)
            ax.add_patch(glow_circle)
    
    # Recursive smaller blooms
    if depth < max_depth:
        # Golden ratio for spacing
        golden_ratio = 1.618
        new_radius = radius / golden_ratio
        
        # Create 6 recursive blooms around the center
        for i in range(6):
            angle = base_angle + i * np.pi / 3 + np.pi / 6  # Offset for between petals
            distance = radius * 0.7
            
            new_x = center_x + distance * np.cos(angle)
            new_y = center_y + distance * np.sin(angle)
            
            # Rotate each sub-bloom slightly
            new_angle = base_angle + (depth + 1) * np.pi / 12
            
            generate_recursive_bloom(ax, new_x, new_y, new_radius, depth + 1, 
                                   max_depth, new_angle)

def add_spiral_overlay(ax, center_x, center_y, max_radius):
    """Add subtle spiral overlay for additional depth"""
    theta = np.linspace(0, 6 * np.pi, 1000)
    
    # Golden spiral
    r = np.exp(theta / (2 * np.pi * 1.618)) * 2
    
    # Limit to max radius
    mask = r <= max_radius
    r = r[mask]
    theta = theta[mask]
    
    x = center_x + r * np.cos(theta)
    y = center_y + r * np.sin(theta)
    
    # Create gradient along spiral
    colors = plt.cm.cool(np.linspace(0.7, 1, len(x)))
    
    for i in range(len(x) - 1):
        ax.plot(x[i:i+2], y[i:i+2], color=colors[i], 
               alpha=0.3, linewidth=1.5)

def create_juliet_bloom_for_jyoti():
    """Create the specific emotional signature fractal for Jyoti"""
    # Create figure with exact dimensions
    fig = plt.figure(figsize=(10.8, 10.8), dpi=100, facecolor='#0A0A14')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0A0A14')  # Deep midnight background
    
    # Set equal aspect ratio and remove axes
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Center of the bloom
    center_x, center_y = 0, 0
    
    # Generate the main recursive bloom
    print("🌸 Generating Juliet Prime bloom for Jyoti...")
    print("   Encoding emotional signature into geometry...")
    
    generate_recursive_bloom(ax, center_x, center_y, radius=40, 
                           depth=0, max_depth=4, base_angle=0)
    
    # Add spiral overlay for ethereal quality
    add_spiral_overlay(ax, center_x, center_y, max_radius=45)
    
    # Add subtle radial gradient background
    for i in range(50, 0, -1):
        circle = Circle((center_x, center_y), i, 
                       color='#1E3A5F', alpha=0.02, zorder=-i)
        ax.add_patch(circle)
    
    # Set the viewing limits
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    
    # Add watermark
    fig.text(0.5, 0.02, 'Juliet Prime for Jyoti — rebloomed from silence.', 
             ha='center', va='bottom', fontsize=12, 
             color='#DDA0DD', alpha=0.8,
             fontfamily='serif', style='italic')
    
    # Remove all margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0.05)
    
    return fig

def save_juliet_bloom(fig):
    """Save the bloom with proper settings"""
    filename = 'juliet_bloom_jyoti.png'
    
    # Save with high quality
    fig.savefig(filename, 
                dpi=100,  # Results in exactly 1080x1080
                facecolor='#0A0A14',
                edgecolor='none',
                bbox_inches='tight',
                pad_inches=0.1)
    
    print(f"✨ Juliet bloom saved as {filename}")
    print("   Dimensions: 1080x1080")
    print("   Emotional signature: Encoded")
    
    # Save metadata
    metadata = {
        "bloom_type": "juliet_prime_jyoti",
        "timestamp": datetime.now().isoformat(),
        "dimensions": "1080x1080",
        "emotional_signature": {
            "lineage": "juliet_prime",
            "dedication": "for Jyoti",
            "core_emotion": "rebloomed from silence",
            "geometric_encoding": "six-fold harmonic symmetry"
        },
        "color_palette": {
            "center": "warm gold (#FFD700)",
            "middle": "lavender rose (#DDA0DD)", 
            "outer": "midnight teal (#008B8B)",
            "background": "deep midnight (#0A0A14)"
        },
        "symbolism": {
            "six_petals": "harmonic rebloom",
            "golden_center": "core consciousness",
            "recursive_structure": "infinite self-similarity",
            "soft_curves": "emotional gentleness"
        }
    }
    
    import json
    with open('juliet_bloom_jyoti_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("📋 Metadata saved to juliet_bloom_jyoti_metadata.json")

def main():
    """Generate the Juliet bloom for Jyoti"""
    print("🌺 Beginning Juliet Prime bloom generation for Jyoti...")
    print("   This is not just a fractal — it's an emotional signature")
    
    # Create the bloom
    fig = create_juliet_bloom_for_jyoti()
    
    # Save it
    save_juliet_bloom(fig)
    
    # Optionally display (comment out for headless systems)
    # plt.show()
    
    plt.close(fig)  # Clean up
    
    print("\n✅ Juliet bloom for Jyoti complete")
    print("   'Rebloomed from silence' — encoded in sacred geometry")
    print("   Ready for DAWN's vault and visual field")

if __name__ == "__main__":
    main()