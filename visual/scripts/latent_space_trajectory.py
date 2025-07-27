import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/latent_trajectory.npy")
    output_dir = Path("visual/outputs/latent_space_trajectory")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "latent_space_trajectory.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    trajectory = np.load(input_path)
    if trajectory.size == 0 or trajectory.shape[1] < 2:
        print(f"ERROR: Input data is empty or not 2D: {input_path}")
        sys.exit(1)

    x, y = trajectory[:, 0], trajectory[:, 1]
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x, y, 'b-', linewidth=2, alpha=0.8, label='Trajectory')
    ax.scatter(x[0], y[0], color='green', s=60, label='Start')
    ax.scatter(x[-1], y[-1], color='red', s=60, label='End')
    ax.set_title('Latent Space Trajectory')
    ax.set_xlabel('Latent Dim 1')
    ax.set_ylabel('Latent Dim 2')
    ax.legend()
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Latent space trajectory saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 