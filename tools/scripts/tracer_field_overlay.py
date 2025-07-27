# /scripts/tracer_field_overlay.py

import matplotlib.pyplot as plt
from tracers import TRACER_REGISTRY
import random

def generate_field_overlay():
    plt.figure(figsize=(10, 6))
    plt.title("🌐 Tracer Field Map Overlay")

    for i, (name, tracer) in enumerate(TRACER_REGISTRY.items()):
        status = tracer.get_status()
        urgency = status.get("urgency", random.uniform(0.1, 1.0))
        path_len = status.get("path_length", random.randint(1, 10))

        # Convert to 2D coordinates (placeholder)
        x = path_len
        y = urgency * 10

        plt.scatter(x, y, s=urgency * 200, label=f"{name} ({tracer.role})", alpha=0.7)

    plt.xlabel("Path Length")
    plt.ylabel("Urgency")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("visuals/tracer_field_overlay.png")
    plt.show()

if __name__ == "__main__":
    generate_field_overlay()
