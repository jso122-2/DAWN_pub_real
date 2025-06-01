
import os
import json
from datetime import datetime

SYNTHESIS_LOG = "owl/synthesis_analysis.log"

def owl_analyze_synthesis(source_blooms, result_bloom):
    log_entries = []
    log_entries.append(f"🪶 {datetime.now().isoformat()} | SYNTHESIS: {result_bloom['seed_id']}")
    log_entries.append(f"→ Lineage Depth: {result_bloom['lineage_depth']}")
    log_entries.append(f"→ Entropy Score: {result_bloom['entropy_score']:.2f}")
    log_entries.append(f"→ Mood: {result_bloom['mood']}")
    log_entries.append("↪ Source Blooms:")

    for bloom in source_blooms:
        log_entries.append(
            f"   - {bloom.get('seed_id')} | L:{bloom.get('lineage_depth')} E:{bloom.get('entropy_score', 0.0):.2f} M:{bloom.get('mood', 'undefined')}"
        )

    log_entries.append("")

    with open(SYNTHESIS_LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(log_entries) + "\n")

    print(f"[Owl] 🪶 Synthesis analysis logged → {SYNTHESIS_LOG}")
