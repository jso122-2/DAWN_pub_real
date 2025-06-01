import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def embed_text(text: str, model) -> np.ndarray:
    return model.encode([text])[0]

def similarity(a: np.ndarray, b: np.ndarray) -> float:
    return cosine_similarity([a], [b])[0][0]

def map_to_field(vector: np.ndarray, seed_space: dict) -> str:
    scores = {sid: similarity(vector, vec) for sid, vec in seed_space.items()}
    return max(scores, key=scores.get)
