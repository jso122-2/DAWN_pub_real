import json
import os
from juliet_field_summary import summarize_fields
from datetime import datetime

def generate_field_summary():
    summary = summarize_fields()
    timestamp = datetime.utcnow().isoformat().replace(":", "-")

    cluster_dir = os.path.join("juliet_flowers", "cluster_report")
    os.makedirs(cluster_dir, exist_ok=True)

    # Save latest snapshot
    with open(os.path.join(cluster_dir, "field_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Save versioned snapshot for drift tracking
    versioned = os.path.join(cluster_dir, f"field_summary_{timestamp}.json")
    with open(versioned, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[FieldDrift] 🧾 Saved snapshot {versioned}")
