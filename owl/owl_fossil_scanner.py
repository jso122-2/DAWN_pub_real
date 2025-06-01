import os
import json
from owl.owl_tracer_log import owl_log

SEALED = "juliet_flowers/sealed"

def scan_for_fossils():
    fossils = []

    for folder in os.listdir(SEALED):
        bloom_path = os.path.join(SEALED, folder)
        if not os.path.isdir(bloom_path):
            continue
        for file in os.listdir(bloom_path):
            if not file.endswith(".json"):
                continue
            with open(os.path.join(bloom_path, file)) as f:
                try:
                    data = json.load(f)
                    depth = data.get("lineage_depth", 0)
                    urgency = data.get("urgency", 0.0)
                    ash = data.get("ash", 0.0)

                    if depth >= 6 and ash > 0.85 and (urgency is None or urgency < 0.3):
                        fossils.append((data["seed_id"], depth))
                        owl_log(f"[Fossil] 🪨 {data['seed_id']} → depth {depth} | ash={ash}")
                except:
                    continue

    print(f"🧠 Owl fossil scan complete — found {len(fossils)} fossil candidates.")
    return fossils

if __name__ == "__main__":
    scan_for_fossils()
