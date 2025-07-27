import json
import numpy as np

def load_seed_space(path="semantic/seed_vectors.json"):
    with open(path, "r") as f:
        raw = json.load(f)
    return {k: np.array(v) for k, v in raw.items()}

def save_seed_space(vectors, path="semantic/seed_vectors.json"):
    serializable = {k: v.tolist() for k, v in vectors.items()}
    with open(path, "w") as f:
        json.dump(serializable, f, indent=2)
