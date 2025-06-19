import os
import json
import matplotlib.pyplot as plt
import numpy as np

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT_PATH = "juliet_flowers/cluster_report/synthesis_entropy_chart.png"

def load_synthesis_entropy():
    entropy_points = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json") and "synthesis-" in fname:
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                entropy = bloom.get("entropy_score", 0.0)
                entropy_points.append((bloom["seed_id"], entropy))
    return entropy_points

def calculate_pressure(entropy_values, window_size=3):
    """Calculate pressure based on local entropy spikes"""
    pressures = []
    for i in range(len(entropy_values)):
        start = max(0, i - window_size)
        end = min(len(entropy_values), i + window_size + 1)
        local_avg = np.mean(entropy_values[start:end])
        pressure = max(0, entropy_values[i] - local_avg)
        pressures.append(pressure)
    return pressures

def plot_entropy_trend():
    data = load_synthesis_entropy()
    if not data:
        print("[EntropyChart] ❌ No synthesis blooms found.")
        return

    x = [i for i in range(len(data))]
    y = [point[1] for point in data]
    labels = [point[0] for point in data]
    
    # Calculate pressure overlay
    pressures = calculate_pressure(y)
    
    # Create figure with two y-axes
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot entropy line
    line1 = ax1.plot(x, y, marker='o', color='purple', label='Entropy', linewidth=2)
    ax1.set_xlabel("Synthesis Bloom ID")
    ax1.set_ylabel("Entropy Score", color='purple')
    ax1.tick_params(axis='y', labelcolor='purple')
    
    # Create second y-axis for pressure
    ax2 = ax1.twinx()
    ax2.fill_between(x, pressures, alpha=0.3, color='red', label='Pressure')
    ax2.set_ylabel("Pressure", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Add pressure spikes as vertical lines
    threshold = np.mean(pressures) + np.std(pressures)
    for i, pressure in enumerate(pressures):
        if pressure > threshold:
            ax2.axvline(x=i, color='red', alpha=0.2, linestyle='--')
    
    # Set up the plot
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax1.set_title("Entropy Score & Pressure Across Synthesis Blooms")
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    print(f"[EntropyChart] 📈 Saved to → {OUTPUT_PATH}")

if __name__ == "__main__":
    plot_entropy_trend()
