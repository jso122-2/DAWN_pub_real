import matplotlib.pyplot as plt

class ContextVisualizer:
    def __init__(self):
        self.history = []

    def log_tick(self, context_snapshot):
        self.history.append(context_snapshot)

    def plot_heatmap(self):
        ticks = [snap['tick'] for snap in self.history]
        seeds = sorted(set(k for snap in self.history for k in snap['drift_vectors'].keys()))

        heatmap = []
        for snap in self.history:
            row = [snap['drift_vectors'].get(seed, 0) for seed in seeds]
            heatmap.append(row)

        plt.figure(figsize=(12, 6))
        plt.imshow(heatmap, cmap='hot', interpolation='nearest', aspect='auto')
        plt.xticks(range(len(seeds)), seeds, rotation=90)
        plt.yticks(range(len(ticks)), ticks)
        plt.colorbar(label='Drift Heat')
        plt.title('Semantic Drift Over Time')
        plt.tight_layout()
        plt.show()
