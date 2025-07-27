import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/correlation_data.npy")
    output_dir = Path("visual/outputs/correlation_matrix")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "correlation_matrix.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    data = np.load(input_path)
    if data.size == 0:
        print(f"ERROR: Input data is empty: {input_path}")
        sys.exit(1)

    corr_matrix = np.corrcoef(data.T)
    n_vars = corr_matrix.shape[0]
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlation Coefficient', rotation=270, labelpad=15)
    for i in range(n_vars):
        for j in range(n_vars):
            text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                          ha='center', va='center', color='black' if abs(corr_matrix[i, j]) < 0.5 else 'white',
                          fontsize=8)
    ax.set_title('Correlation Matrix')
    ax.set_xlabel('Variable Index')
    ax.set_ylabel('Variable Index')
    ax.set_xticks(range(n_vars))
    ax.set_yticks(range(n_vars))
    ax.set_xticklabels([f'V{i}' for i in range(n_vars)])
    ax.set_yticklabels([f'V{i}' for i in range(n_vars)])
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Correlation matrix saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 