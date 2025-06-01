# /src/tracers/ant.py

from tracers.base import Tracer
from bloom.registry import get_active_blooms
from rhizome.trail_tracker import validate_path, is_dead_end, reinforce_path
from owl.owl_tracer_log import owl_log
from schema.registry import rhizome  # 🔌 Nutrient routing
from schema.rebloom_queue import push_to_rebloom_queue

class AntTracer(Tracer):
    def __init__(self):
        super().__init__(
            name="Ant",
            role="path validator in rhizome",
            watch=["/path_check", "/trail_loop", "/deadend"],
            act=self.respond
        )

    def respond(self, sigil):
        print(f"[AntTracer] 🐜 Responding to sigil: {sigil}")
        if sigil == "/path_check":
            self.validate_all_paths()
        if bloom.reinforcement_count >= 3:
            push_to_rebloom_queue(bloom)
        elif sigil == "/trail_loop":
            self.detect_loops()
        elif sigil == "/deadend":
            self.check_for_dead_ends()

    def validate_all_paths(self):
        blooms = get_active_blooms()
        for bloom in blooms:
            result = validate_path(bloom)
            if not result["valid"]:
                reason = result["reason"]
                print(f"[Ant] ❌ Invalid path: {bloom.seed_id} | Reason: {reason}")
                bloom.mark_for_review(f"Ant: path invalid – {reason}")
                owl_log(f"[Ant] ❌ Invalid path: {bloom.seed_id} | Reason: {reason}")
                rhizome.broadcast_nutrient(bloom.seed_id, "urgency", strength=0.6, radius=2)
            else:
                reinforce_path(bloom)
                print(f"[Ant] ✅ Valid path reinforced: {bloom.seed_id}")
                owl_log(f"[Ant] ✅ Reinforced path: {bloom.seed_id}")
                rhizome.broadcast_nutrient(bloom.seed_id, "ash", strength=0.4, radius=1)

                # 🌱 Track reinforcement count
                if not hasattr(bloom, "reinforcement_count"):
                    bloom.reinforcement_count = 0
                    bloom.reinforcement_count += 1

                if bloom.reinforcement_count >= 3:
                    print(f"[Ant] 🌱 Rebloom priority triggered: {bloom.seed_id}")
                    bloom.mark_for_review("Ant: high-reinforcement → rebloom candidate")
                    owl_log(f"[Ant] 🌱 Rebloom priority → {bloom.seed_id} (reinforced {bloom.reinforcement_count}×)")

    def detect_loops(self):
        blooms = get_active_blooms()
        for bloom in blooms:
            result = validate_path(bloom)
            if result.get("loop"):
                print(f"[Ant] ♻️ Loop detected in: {bloom.seed_id}")
                bloom.mark_for_review("Ant: looped trail")
                owl_log(f"[Ant] ♻️ Loop detected: {bloom.seed_id}")
                rhizome.broadcast_nutrient(bloom.seed_id, "urgency", strength=0.5, radius=2)

    def check_for_dead_ends(self):
        blooms = get_active_blooms()
        for bloom in blooms:
            if is_dead_end(bloom):
                print(f"[Ant] 🪦 Dead-end bloom: {bloom.seed_id}")
                bloom.mark_for_decay("Ant: dead-end node")
                owl_log(f"[Ant] 🪦 Marked dead-end: {bloom.seed_id}")
                rhizome.broadcast_nutrient(bloom.seed_id, "urgency", strength=0.7, radius=3)
