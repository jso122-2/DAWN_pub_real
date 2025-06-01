
# schema_health.py
# Calculates Schema Health Index (SHI) from pulse, entropy, and cluster coherence

class SchemaHealthIndex:
    def __init__(self):
        self.entropies = []
        self.pressures = []
        self.cluster_variance = []

    def record(self, entropy, pressure, variance):
        self.entropies.append(entropy)
        self.pressures.append(pressure)
        self.cluster_variance.append(variance)

    def compute(self):
        if not self.entropies:
            return 1.0
        avg_entropy = sum(self.entropies[-50:]) / len(self.entropies[-50:])
        avg_pressure = sum(self.pressures[-50:]) / len(self.pressures[-50:])
        avg_variance = sum(self.cluster_variance[-50:]) / len(self.cluster_variance[-50:])
        return round(1.0 - (0.4 * avg_entropy + 0.3 * avg_pressure + 0.3 * avg_variance), 3)
