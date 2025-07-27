"""
Simple working visualization for DAWN
Save as simple_visual.py in Tick_engine directory
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd

# Create output directory
output_dir = Path("visual_output")
output_dir.mkdir(exist_ok=True)

print("🎨 Creating DAWN visualization...")

# Create synthetic tick data
ticks = np.arange(1000, 1200)
zones = ['calm', 'active', 'surge']
zone_colors = {'calm': '#4CAF50', 'active': '#FFC107', 'surge': '#F44336'}

# Generate data
data = []
for i, tick in enumerate(ticks):
    zone = zones[i % 3]
    heat = 0.3 + (i % 10) * 0.05 + np.random.normal(0, 0.02)
    entropy = 0.2 + (i % 20) * 0.02 + np.random.normal(0, 0.01)
    scup = 0.8 - (i % 30) * 0.01 + np.random.normal(0, 0.01)
    data.append([tick, zone, heat, entropy, scup])

# Create figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('DAWN System Dynamics', fontsize=16)

# 1. Zone transitions over time
ax1 = axes[0, 0]
zone_numeric = [zones.index(d[1]) for d in data]
colors = [zone_colors[d[1]] for d in data]
ax1.scatter(ticks, zone_numeric, c=colors, alpha=0.6, s=50)
ax1.set_yticks([0, 1, 2])
ax1.set_yticklabels(zones)
ax1.set_xlabel('Tick')
ax1.set_title('Zone Transitions')
ax1.grid(True, alpha=0.3)

# 2. Pulse heat over time
ax2 = axes[0, 1]
heats = [d[2] for d in data]
ax2.plot(ticks, heats, 'r-', linewidth=2, label='Pulse Heat')
ax2.fill_between(ticks, heats, alpha=0.3, color='red')
ax2.set_xlabel('Tick')
ax2.set_ylabel('Heat Level')
ax2.set_title('Thermal Dynamics')
ax2.grid(True, alpha=0.3)
ax2.legend()

# 3. Entropy evolution
ax3 = axes[1, 0]
entropies = [d[3] for d in data]
ax3.plot(ticks, entropies, 'b-', linewidth=2)
ax3.scatter(ticks[::10], entropies[::10], color='blue', s=50, zorder=5)
ax3.set_xlabel('Tick')
ax3.set_ylabel('Entropy')
ax3.set_title('System Entropy')
ax3.grid(True, alpha=0.3)

# 4. SCUP (Semantic Coherence Under Pressure)
ax4 = axes[1, 1]
scups = [d[4] for d in data]
ax4.plot(ticks, scups, 'g-', linewidth=2)
ax4.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Critical SCUP')
ax4.fill_between(ticks, 0, scups, where=[s < 0.3 for s in scups], 
                 color='red', alpha=0.2, label='Danger Zone')
ax4.set_xlabel('Tick')
ax4.set_ylabel('SCUP Score')
ax4.set_title('Semantic Coherence')
ax4.grid(True, alpha=0.3)
ax4.legend()

plt.tight_layout()

# Save the visualization
output_path = output_dir / "dawn_system_overview.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"✅ Saved visualization to: {output_path}")

# Also create a simple animation-style plot
fig2, ax = plt.subplots(figsize=(10, 6))

# Create a phase space plot
ax.scatter(heats, entropies, c=range(len(heats)), cmap='viridis', 
          s=50, alpha=0.6)
ax.set_xlabel('Pulse Heat')
ax.set_ylabel('Entropy')
ax.set_title('DAWN Phase Space')

# Add trajectory lines
ax.plot(heats, entropies, 'k-', alpha=0.2, linewidth=1)

# Mark zones
for zone in zones:
    zone_heats = [h for h, d in zip(heats, data) if d[1] == zone]
    zone_entropies = [e for e, d in zip(entropies, data) if d[1] == zone]
    if zone_heats:
        ax.scatter(zone_heats[0], zone_entropies[0], 
                  color=zone_colors[zone], s=200, marker='s', 
                  label=f'{zone} zone', edgecolor='black', linewidth=2)

ax.legend()
ax.grid(True, alpha=0.3)

output_path2 = output_dir / "dawn_phase_space.png"
plt.savefig(output_path2, dpi=150, bbox_inches='tight')
print(f"✅ Saved phase space to: {output_path2}")

plt.show()

print("\n🎉 Visualization complete!")
print("Check the visual_output directory for the generated images.")