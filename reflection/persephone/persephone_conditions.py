# Tracks sustained semantic conditions over ticks for pruning, rebloom, and anchoring

condition_tracker = {}

def update_condition(seed_id, condition):
    if seed_id not in condition_tracker:
        condition_tracker[seed_id] = {
            "ash": 0,
            "soot": 0,
            "drift": 0,
            "entropy": 0
        }

    for key in condition_tracker[seed_id]:
        if key == condition:
            condition_tracker[seed_id][key] += 1
        else:
            condition_tracker[seed_id][key] = 0

    return condition_tracker[seed_id][condition]

def should_trigger(seed_id, condition, threshold=5):
    return update_condition(seed_id, condition) >= threshold
