import json
from semantic.vector_core import embed_text, similarity
from semantic.vector_model import model

def compute_transfer(seed_a, seed_b, charge_a, trust_a, text_map):
    sim = similarity(embed_text(text_map[seed_a], model), embed_text(text_map[seed_b], model))
    return round(charge_a * trust_a * sim, 4)

def run_seed_transfer():
    with open("juliet_flowers/index/charge_map.json", "r", encoding="utf-8") as f:
        charge_map = json.load(f)
    with open("juliet_flowers/index/seed_trust.json", "r", encoding="utf-8") as f:
        trust_map = json.load(f)
    with open("juliet_flowers/index/seed_texts.json", "r", encoding="utf-8") as f:
        text_map = json.load(f)

    transfers = {}
    for a in charge_map:
        for b in charge_map:
            if a != b:
                transfer_val = compute_transfer(a, b, charge_map[a], trust_map.get(a, 1.0), text_map)
                if transfer_val > 0.05:
                    transfers.setdefault(a, {})[b] = transfer_val

    with open("juliet_flowers/index/seed_transfer_map.json", "w", encoding="utf-8") as f:
        json.dump(transfers, f, indent=2)

    print(f"[Transfer] 🌐 Seed-to-seed charge map created.")

if __name__ == "__main__":
    run_seed_transfer()
