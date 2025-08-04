#!/usr/bin/env python3
"""
Test script to check GIF saving functionality
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import os

# Import GIF saver

    from ...gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

def create_test_animation():
    """Create a simple test animation"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    def animate(frame):
        ax.clear()
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x + frame * 0.1)
        ax.plot(x, y, 'b-', linewidth=2)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(f'Test Animation Frame {frame}')
        return ax,
    
    anim = animation.FuncAnimation(frames=1000, fig, animate, frames=50, interval=100, blit=False)
    return anim

def test_gif_saving():
    """Test GIF saving functionality"""
    print("Creating test animation...")
    anim = create_test_animation()
    
    print("Setting up GIF saver...")
    gif_saver = setup_gif_saver("test")
    
    print("Saving animation as GIF...")

        gif_path = gif_saver.save_animation_as_gif(anim, fps=5, dpi=100)
        if gif_path:
            print(f"SUCCESS: GIF saved to {gif_path}")
            return True
        else:
            print("FAILED: GIF save returned None")
            return False
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_gif_saving()
    sys.exit(0 if success else 1) 