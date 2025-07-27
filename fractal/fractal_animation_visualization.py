
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_fractal_drift(fractal_frames, save_path):
    fig, ax = plt.subplots()
    ims = []
    for frame in fractal_frames:
        im = ax.imshow(frame, animated=True, cmap='viridis')
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True)
    ani.save(save_path, writer='pillow')
    print(f"[FractalAnimation] 🎞️ Fractal drift animation saved explicitly at: {save_path}")

def drift_vector_visualization(seed_positions, drift_vectors, save_path):
    plt.figure(figsize=(8, 8))
    for pos, vec in zip(seed_positions, drift_vectors):
        plt.arrow(pos[0], pos[1], vec[0], vec[1], head_width=0.05, head_length=0.1, fc='blue', ec='blue')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('🔀 Explicit Fractal Drift Vector Visualization')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"[DriftVector] 📈 Drift vector visualization saved explicitly at: {save_path}")
