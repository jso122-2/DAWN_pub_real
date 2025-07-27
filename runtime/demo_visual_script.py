#!/usr/bin/env python3
"""
Sample Tick Visualization Script
Demonstrates how to create DAWN-compatible visualizations
"""

import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Check for tick data from environment or file
tick_data = {}
if 'TICK_DATA_PATH' in os.environ:
    try:
        with open(os.environ['TICK_DATA_PATH'], 'r') as f:
            tick_data = json.load(f)
    except:
        pass

if 'CURRENT_TICK_DATA' in globals():
    tick_data = CURRENT_TICK_DATA

# Default values if no tick data available
tick = tick_data.get('tick', 0)
scup = tick_data.get('scup', 0.5)
entropy = tick_data.get('entropy', 0.3)
heat = tick_data.get('heat', 0.25)
mood = tick_data.get('mood', 'contemplative')

# Create visualization
plt.style.use('dark_background')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
fig.patch.set_facecolor('#0a0a0a')

# SCUP visualization
ax1.bar(['SCUP'], [scup], color='#4a9eff', alpha=0.8)
ax1.set_ylim(0, 1)
ax1.set_title(f'SCUP: {scup:.3f}', color='#4a9eff')
ax1.set_facecolor('#0a0a0a')

# Entropy flow
x = np.linspace(0, 10, 100)
y = entropy * np.sin(x + time.time() * 0.1)
ax2.plot(x, y, color='#ff6b4a', linewidth=2)
ax2.set_title(f'Entropy Flow: {entropy:.3f}', color='#ff6b4a')
ax2.set_facecolor('#0a0a0a')

# Heat visualization
theta = np.linspace(0, 2*np.pi, 100)
r = heat * (1 + 0.3 * np.sin(5 * theta))
ax3.polar(theta, r, color='#ffa94a', linewidth=3)
ax3.set_title(f'Heat Pattern: {heat:.3f}', color='#ffa94a')
ax3.set_facecolor('#0a0a0a')

# Tick and mood info
ax4.text(0.5, 0.7, f'Tick: {tick}', ha='center', va='center', 
         color='#e8f4f8', fontsize=16, transform=ax4.transAxes)
ax4.text(0.5, 0.3, f'Mood: {mood}', ha='center', va='center',
         color='#8ba4c7', fontsize=14, transform=ax4.transAxes)
ax4.set_facecolor('#0a0a0a')
ax4.set_xticks([])
ax4.set_yticks([])

plt.tight_layout()

# Save the visualization
output_path = os.environ.get('OUTPUT_PATH', f'runtime/snapshots/demo_visualization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', 
           facecolor='#0a0a0a', edgecolor='none')
plt.close()

print(f"Demo visualization saved to: {output_path}")
