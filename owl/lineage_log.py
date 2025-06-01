import os

LINEAGE_LOG = "owl/rebloom_lineage.log"

def log_rebloom_lineage(seed_id, ancestry_tag):
    os.makedirs("owl", exist_ok=True)
    with open(LINEAGE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{seed_id} ← {ancestry_tag}\n")
