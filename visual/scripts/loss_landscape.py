import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/loss_surface.npz")
    output_dir = Path("visual/outputs/loss_landscape")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "loss_landscape.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    data = np.load(input_path)
    if not all(k in data for k in ("X", "Y", "Z", "path_x", "path_y")):
        print(f"ERROR: Input data missing required arrays: {input_path}")
        sys.exit(1)
    X, Y, Z = data["X"], data["Y"], data["Z"]
    path_x, path_y = data["path_x"], data["path_y"]
    if X.size == 0 or Y.size == 0 or Z.size == 0 or path_x.size == 0 or path_y.size == 0:
        print(f"ERROR: One or more input arrays are empty: {input_path}")
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(10, 8))
    contour = ax.contourf(X, Y, Z, levels=30, cmap='plasma', alpha=0.85)
    cbar = plt.colorbar(contour, ax=ax)
    cbar.set_label('Loss Value', rotation=270, labelpad=15)
    ax.plot(path_x, path_y, 'w-o', linewidth=2, markersize=6, label='Optimization Path')
    ax.set_title('Loss Landscape')
    ax.set_xlabel('Parameter 1')
    ax.set_ylabel('Parameter 2')
    ax.legend()
    ax.grid(True, alpha=0.2, linestyle='--')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Loss landscape saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 