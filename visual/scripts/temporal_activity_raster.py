import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/spike_trains.npy")
    output_dir = Path("visual/outputs/temporal_activity_raster")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "temporal_activity_raster.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    spikes = np.load(input_path)
    if spikes.size == 0:
        print(f"ERROR: Input data is empty: {input_path}")
        sys.exit(1)

    n_neurons, n_time = spikes.shape
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(n_neurons):
        spike_times = np.where(spikes[i])[0]
        ax.vlines(spike_times, i + 0.5, i + 1.5, color='black', linewidth=1)
    ax.set_ylim(0.5, n_neurons + 0.5)
    ax.set_xlim(0, n_time)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Neuron Index')
    ax.set_title('Temporal Activity Raster')
    ax.grid(True, axis='x', alpha=0.2, linestyle='--')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Temporal activity raster saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 