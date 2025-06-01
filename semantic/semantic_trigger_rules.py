import json
import os

def load_charge_map(path="juliet_flowers/index/charge_map.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def trigger_rules(charge_map, thresholds=None):
    if thresholds is None:
        thresholds = {
            "rebloom": 0.75,
            "route": 0.60,
            "crystallize": 0.90
        }

    actions = {}

    for seed, charge in charge_map.items():
        charge_val = float(charge)
        action_list = []

        if charge_val >= thresholds["rebloom"]:
            action_list.append("REBLOOM")
        if charge_val >= thresholds["route"]:
            action_list.append("ROUTE")
        if charge_val >= thresholds["crystallize"]:
            action_list.append("CRYSTALLIZE")

        if action_list:
            actions[seed] = action_list

    return actions

def save_triggers(actions, path="juliet_flowers/index/trigger_actions.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(actions, f, indent=2)

def run_trigger_ruleset():
    charge_map = load_charge_map()
    actions = trigger_rules(charge_map)
    save_triggers(actions)
    print(f"[TriggerRuleset] ⚡ Triggers computed and saved for {len(actions)} seeds.")

if __name__ == "__main__":
    run_trigger_ruleset()
