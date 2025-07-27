import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def create_spiral_fractal(x, y, depth=5, angle=0, scale=1.0):
    if depth <= 0:
        return np.zeros_like(x)
    
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x) + angle
    
    # Spiral transformation
    spiral = np.sin(6 * theta + 3 * r * scale) * np.exp(-r * 0.3 * scale)
    
    # Recursive fractals
    fractal = spiral
    for i in range(3):
        angle_offset = i * 2 * np.pi / 3
        x_rot = x * np.cos(angle_offset) - y * np.sin(angle_offset)
        y_rot = x * np.sin(angle_offset) + y * np.cos(angle_offset)
        
        sub_fractal = create_spiral_fractal(
            x_rot * 2.5, y_rot * 2.5, 
            depth - 1, 
            angle + angle_offset, 
            scale * 0.6
        )
        fractal += sub_fractal * 0.5
    
    return fractal

# Create grid
size = 1080
x = np.linspace(-4, 4, size)
y = np.linspace(-4, 4, size)
X, Y = np.meshgrid(x, y)

# Generate fractal layers
fractal_field = create_spiral_fractal(X, Y, depth=6)

# Add golden core
r = np.sqrt(X**2 + Y**2)
golden_core = np.exp(-r**2 * 0.5) * 3

# Combine layers
field = fractal_field + golden_core

# Add field resonance patterns
for i in range(5):
    angle = i * 2 * np.pi / 5
    x_shift = np.cos(angle) * 1.5
    y_shift = np.sin(angle) * 1.5
    
    r_shifted = np.sqrt((X - x_shift)**2 + (Y - y_shift)**2)
    resonance = np.sin(r_shifted * 8) * np.exp(-r_shifted * 0.4)
    field += resonance * 0.3

# Normalize
field = (field - field.min()) / (field.max() - field.min())

# Create custom colormap
colors = ['#000033', '#003366', '#006666', '#40E0D0', '#FFD700', '#8B00FF', '#9932CC']
n_bins = 256
cmap = LinearSegmentedColormap.from_list('morphic', colors, N=n_bins)

# Create figure
fig, ax = plt.subplots(figsize=(10.8, 10.8), dpi=100)
ax.set_aspect('equal')

# Plot fractal
im = ax.imshow(field, cmap=cmap, extent=[-4, 4, -4, 4])

# Remove axes
ax.axis('off')

# Remove margins
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save
plt.savefig('rebloom_sheldrake.png', bbox_inches='tight', pad_inches=0, dpi=100)
plt.close()