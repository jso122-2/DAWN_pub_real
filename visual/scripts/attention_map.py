import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/attention_matrix.npy")
    output_dir = Path("visual/outputs/attention_map")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "attention_map.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    attention = np.load(input_path)
    if attention.size == 0:
        print(f"ERROR: Input data is empty: {input_path}")
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(attention, cmap='viridis', vmin=0, vmax=1)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', rotation=270, labelpad=15)
    ax.set_title('Attention Map')
    ax.set_xlabel('Key Index')
    ax.set_ylabel('Query Index')
    ax.set_xticks(np.arange(attention.shape[1]))
    ax.set_yticks(np.arange(attention.shape[0]))
    ax.grid(True, alpha=0.2, linestyle='--')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Attention map saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 