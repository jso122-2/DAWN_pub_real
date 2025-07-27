import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_signal_path = Path("data/anomaly_signal.npy")
    input_anomaly_path = Path("data/anomaly_flags.npy")
    output_dir = Path("visual/outputs/anomaly_timeline")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "anomaly_timeline.png"

    if not input_signal_path.exists() or not input_anomaly_path.exists():
        print(f"ERROR: Input data not found: {input_signal_path} or {input_anomaly_path}")
        sys.exit(1)

    signal = np.load(input_signal_path)
    anomalies = np.load(input_anomaly_path)
    if signal.size == 0 or anomalies.size == 0:
        print(f"ERROR: Input data is empty: {input_signal_path} or {input_anomaly_path}")
        sys.exit(1)
    if signal.shape != anomalies.shape:
        print(f"ERROR: Signal and anomaly arrays must have the same shape.")
        sys.exit(1)
    time = np.arange(signal.size)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(time, signal, 'b-', linewidth=1.5, label='Signal', alpha=0.8)
    ax1.scatter(time[anomalies.astype(bool)], signal[anomalies.astype(bool)], color='red', s=100, marker='o', label='Anomalies', zorder=5, edgecolor='black')
    rolling_mean = np.convolve(signal, np.ones(10)/10, mode='same')
    rolling_std = np.array([signal[max(0,i-5):i+5].std() for i in range(signal.size)])
    ax1.fill_between(time, rolling_mean - 2*rolling_std, rolling_mean + 2*rolling_std, alpha=0.2, color='blue')
    ax1.set_title('Anomaly Timeline')
    ax1.set_ylabel('Signal Value')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend()
    ax2.bar(time, anomalies.astype(int), color='red', alpha=0.7)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Anomaly')
    ax2.set_ylim(0, 1.5)
    ax2.set_yticks([0, 1])
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xlim(ax1.get_xlim())
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: Anomaly timeline saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 