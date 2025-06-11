import matplotlib.pyplot as plt
import numpy as np
from semantic.sigil_ring import sigil_memory_ring

def render_entropy_field(output_path="juliet_flowers/cluster_report/entropy_field.png"):
    """
    Renders a visual entropy heat map from sigil_memory_ring.
    """
    entropy_values = [s.entropy for s in sigil_memory_ring.values()]
    size = len(entropy_values)

    if size == 0:
        print("[EntropyMap] ❌ No sigils to visualize.")
        return

    grid_size = int(np.ceil(np.sqrt(size)))
    matrix = np.zeros((grid_size, grid_size))

    for idx, entropy in enumerate(entropy_values):
        row = idx // grid_size
        col = idx % grid_size
        matrix[row, col] = entropy

    plt.figure(figsize=(6, 6))
    plt.imshow(matrix, cmap="inferno", interpolation="nearest")
    plt.colorbar(label="Entropy")
    plt.title("🧯 Sigil Entropy Field")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"[EntropyMap] 🧭 Field saved → {output_path}")
