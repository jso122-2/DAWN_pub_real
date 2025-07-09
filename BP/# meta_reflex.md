# meta_reflex.py

class MetaReflex:
    def __init__(self):
        self.log = []

    def evaluate_system_state(self, scup, entropy, zone):
        triggers = []

        if scup < 0.5:
            triggers.append("LOW_SCUP")
        if entropy > 0.75:
            triggers.append("HIGH_ENTROPY")
        if zone.upper() == "SURGE":
            triggers.append("ZONE_SURGE")

        return triggers

    def generate_reflex_commands(self, triggers):
        reflex_map = {
            "LOW_SCUP": "slow_tick",
            "HIGH_ENTROPY": "suppress_rebloom",
            "ZONE_SURGE": "prune_sigils"
        }

        commands = [reflex_map[t] for t in triggers if t in reflex_map]
        return commands

    def log_intervention(self, reason):
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        self.log.append(f"[{timestamp}] Reflex activated due to: {reason}")

    def get_log(self):
        return self.log
