import os
import json
import csv
from datetime import datetime
from schema.schema_climate import get_decay_boost
from rhizome.nutrient_flow_logger import log_nutrient_transfer
from rhizome.rhizome_pathfinder import find_path
from bloom.spawn_bloom import spawn_bloom
from owl.owl_tracer_log import owl_log

NUTRIENT_TYPES = ["ash", "soot", "sentiment", "attention", "urgency"]
DECAY_RATES = {
    "ash": 0.01, "soot": 0.02, "sentiment": 0.015, "attention": 0.05, "urgency": 0.08
}
SYNTHESIS_COOLDOWN = {}
COOLDOWN_DURATION_TICKS = 20
SYNTHESIS_THRESHOLD = 2.5
REINFORCEMENT_TRACKER = {}
REINFORCEMENT_LOG = "logs/reinforcement_log.json"
SYNTHESIS_LOG_PATH = "logs/synthesis_bloom_log.csv"

os.makedirs(os.path.dirname(SYNTHESIS_LOG_PATH), exist_ok=True)
if not os.path.exists(SYNTHESIS_LOG_PATH):
    with open(SYNTHESIS_LOG_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tick_id", "bloom_id", "mood", "factor", "depth", "entropy", "path"])

def decay(nutrient_type, amount, ticks=1, decay_boost=None):
    boost = decay_boost if decay_boost else get_decay_boost(nutrient_type)
    rate = DECAY_RATES.get(nutrient_type, 0.02) * boost
    return max(0.0, amount * ((1 - rate) ** ticks))

def flow_nutrient(source_node, target_node, nutrient_type, strength, tick_id=None, pulse=None):
    if nutrient_type not in NUTRIENT_TYPES:
        raise ValueError(f"Invalid nutrient type: {nutrient_type}")

    available = source_node.get_nutrient_level(nutrient_type)
    strength = min(strength, available)
    decayed = decay(nutrient_type, strength, ticks=1)
    log_nutrient_transfer(tick_id, source_node.seed_id, target_node.seed_id, nutrient_type, decayed)
    source_node.send_nutrient(target_node.seed_id, nutrient_type, strength)
    target_node.receive_nutrient(nutrient_type, decayed)

    edge_data = source_node.edges.get(target_node.seed_id)
    reinforced = False
    if isinstance(edge_data, dict):
        edge_data["reinforcement_score"] = edge_data.get("reinforcement_score", 0.0) + decayed
        reinforced = True
        source_node.activity_log.append(
            f"💡 Reinforced {target_node.seed_id} by +{decayed:.2f} (total: {edge_data['reinforcement_score']:.2f})"
        )
    else:
        source_node.activity_log.append(
            f"💡 Flowed {decayed:.2f} {nutrient_type} → {target_node.seed_id}"
        )

    if tick_id:
        log_nutrient_flow(tick_id, source_node.seed_id, target_node.seed_id, nutrient_type, decayed)

    check_and_trigger_synthesis(
        source_seed=source_node.seed_id,
        target_seed=target_node.seed_id,
        rhizome_map=RHIZOME_MAP_REF,  # <- bind this in your environment
        tick_id=tick_id,
        pulse=pulse
    )

    return {
        "from": source_node.seed_id,
        "to": target_node.seed_id,
        "nutrient": nutrient_type,
        "requested": strength,
        "delivered": decayed,
        "reinforced": reinforced
    }

def check_and_trigger_synthesis(source_seed, target_seed, rhizome_map, tick_id=None, pulse=None):
    path = find_path(source_seed, target_seed, rhizome_map.nodes)
    if not path or len(path) < 2:
        return

    total_score = 0.0
    for i in range(len(path) - 1):
        edge = rhizome_map.nodes[path[i]].edges.get(path[i + 1])
        if isinstance(edge, dict):
            total_score += edge.get("reinforcement_score", 0.0)

    if total_score >= SYNTHESIS_THRESHOLD:
        midpoint_idx = len(path) // 2
        midpoint_seed = path[midpoint_idx]

        last_tick = SYNTHESIS_COOLDOWN.get(midpoint_seed)
        if last_tick is not None and tick_id is not None:
            if tick_id - last_tick < COOLDOWN_DURATION_TICKS:
                msg = f"[Owl] 🧊 Synthesis blocked at {midpoint_seed} due to cooldown. Wait {COOLDOWN_DURATION_TICKS - (tick_id - last_tick)} ticks."
                owl_log(msg)
                print(msg)
                return

        print(f"[SynthesisTrigger] 🧠 Reinforcement score {total_score:.2f} on path {source_seed}→{target_seed}")
        print(f"[SynthesisTrigger] 🌸 Triggering synthesis at midpoint: {midpoint_seed}")

        bloom_data = {
            "seed_id": midpoint_seed,
            "lineage_depth": len(path),
            "bloom_factor": round(total_score, 2),
            "entropy_score": round(0.2 + 0.1 * len(path), 3),
            "mood": "synthesis",
            "path_history": path,
            "timestamp": datetime.utcnow().isoformat()
        }

        spawn_bloom(bloom_data, pulse or {})
        log_synthesis_bloom(tick_id, bloom_data)
        if tick_id:
            SYNTHESIS_COOLDOWN[midpoint_seed] = tick_id

def log_synthesis_bloom(tick_id, bloom_data):
    with open(SYNTHESIS_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            tick_id,
            bloom_data["seed_id"],
            bloom_data.get("mood"),
            bloom_data.get("bloom_factor"),
            bloom_data.get("lineage_depth"),
            bloom_data.get("entropy_score"),
            "→".join(bloom_data.get("path_history", []))
        ])

def log_reinforcement_state():
    os.makedirs(os.path.dirname(REINFORCEMENT_LOG), exist_ok=True)
    snapshot = {
        "timestamp": datetime.utcnow().isoformat(),
        "reinforcement_tracker": REINFORCEMENT_TRACKER.copy()
    }
    if os.path.exists(REINFORCEMENT_LOG):
        with open(REINFORCEMENT_LOG, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(snapshot)
    with open(REINFORCEMENT_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
