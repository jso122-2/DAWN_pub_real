import os
from semantic.vector_core import embed_text, similarity
from semantic.vector_model import model

def log_vector_drift_auto(parent_text, child_text, bloom_id, log_dir="juliet_flowers/cluster_report"):
    parent_vec = embed_text(parent_text, model)
    child_vec = embed_text(child_text, model)
    drift_score = 1 - similarity(parent_vec, child_vec)

    log_path = os.path.join(log_dir, f"vector_drift_{bloom_id}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("🌱 Drift between reblooms:\n")
        f.write(f"Bloom ID: {bloom_id}\n")
        f.write(f"Semantic Drift Score: {drift_score:.4f}\n")

    return drift_score
