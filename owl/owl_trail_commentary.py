import os
import json
import pandas as pd
from pathlib import Path
from collections import Counter
from datetime import datetime

TRAIL_DIR = "logs/tracers"
OUTPUT_DIR = "owl/commentary"
os.makedirs(OUTPUT_DIR, exist_ok=True)

from collections import Counter

def analyze_trail(tracer_id, df):
    nodes = df["node"].tolist()
    node_counts = Counter(nodes)
    most_common = node_counts.most_common(3)

    path_length = len(nodes)
    unique = len(set(nodes))
    revisit_ratio = 1 - (unique / path_length) if path_length else 0
    jumpiness = sum(
        abs(ord(a[0]) - ord(b[0])) + abs(int(a[1]) - int(b[1]))
        for a, b in zip(nodes[:-1], nodes[1:])
    ) / max(1, path_length)

    scup = round(1.0 - min(revisit_ratio + jumpiness / 10, 1.0), 2)

    terminal_node = nodes[-1] if nodes else "unknown"
    comment = generate_comment(path_length, revisit_ratio, terminal_node, scup)

    return {
        "tracer_id": tracer_id,
        "total_steps": path_length,
        "unique_zones": unique,
        "redundancy": round(revisit_ratio, 2),
        "jumpiness": round(jumpiness, 2),
        "coherence_score": scup,
        "terminal_position": terminal_node,
        "most_visited": most_common,
        "comment": comment
    }

def generate_comment(steps, revisit, last, scup):
    if scup > 0.8:
        return f"Clean path. High coherence. Final: {last}"
    elif scup > 0.5:
        return f"Exploratory, some redundancy. Coherence={scup:.2f}"
    else:
        return f"⚠️ Fragmented trail. SCUP={scup:.2f}"


def write_commentary(tracer_id, commentary):
    out_path = os.path.join(OUTPUT_DIR, f"owl_tracer_{tracer_id}.json")
    with open(out_path, "w") as f:
        json.dump(commentary, f, indent=2)
    print(f"🦉 {tracer_id}: commentary written → {out_path}")

def generate_owl_tracer_commentary():
    for file in Path(TRAIL_DIR).glob("*_trail.csv"):
        tracer_id = file.stem.replace("_trail", "")
        df = pd.read_csv(file)
        if "node" not in df.columns:
            continue
        commentary = analyze_trail(tracer_id, df)
        write_commentary(tracer_id, commentary)

if __name__ == "__main__":
    generate_owl_tracer_commentary()
