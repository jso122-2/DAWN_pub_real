
import numpy as np

def generate_semantic_reasoning_field(seed_entropy_values):
    reasoning_field = {seed: entropy * np.random.uniform(0.8, 1.2) for seed, entropy in seed_entropy_values.items()}
    for seed, intensity in reasoning_field.items():
        print(f"[SemanticReasoningField] 🌱 Seed '{seed}' explicit reasoning intensity: {intensity:.2f}")
    return reasoning_field

if __name__ == "__main__":
    example_entropy_values = {"seed-∆test": 0.5, "seed-∆2143FJ": 0.6}
    generate_semantic_reasoning_field(example_entropy_values)
