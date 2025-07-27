import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/activations.npy")
    output_dir = Path("visual/outputs/activation_histogram")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "activation_histogram.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    activations = np.load(input_path)
    if activations.size == 0:
        print(f"ERROR: Input data is empty: {input_path}")
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(activations, bins=50, alpha=0.7, color='blue', edgecolor='black')
    mean_val = np.mean(activations)
    median_val = np.median(activations)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.3f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.3f}')
    ax.set_title('Activation Histogram')
    ax.set_xlabel('Activation Value')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend()
    textstr = f'Total: {len(activations)}\nStd: {np.std(activations):.3f}\nSparsity: {(activations == 0).sum()/len(activations):.1%}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.7, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Activation histogram saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 