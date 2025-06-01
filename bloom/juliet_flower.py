
import os
import json
from datetime import datetime
from bloom.spawn_bloom import spawn_bloom
from owl.owl_rebloom_log import owl_log_rebloom
from owl.owl_synthesis_analysis import owl_analyze_synthesis
from mood.blend import blend_moods
from tracers.whale import nearest_belief, PIGMENTS

def assign_belief_resonance(fragment):
    mood_colors = {
        "joyful": (255, 215, 0),
        "anxious": (255, 69, 0),
        "reflective": (70, 130, 180),
        "focused": (34, 139, 34),
        "sad": (105, 105, 105),
        "curious": (255, 140, 0),
        "overload": (255, 0, 255)
    }
    rgb = mood_colors.get(fragment.get("mood", "reflective"), (200, 200, 200))
    belief = nearest_belief(rgb)
    belief_rgb, _ = PIGMENTS[belief]
    resonance = round(sum((a - b) ** 2 for a, b in zip(rgb, belief_rgb)) ** 0.5, 2)

    fragment["belief_resonance"] = {
        "belief": belief,
        "distance": resonance,
        "rgb": rgb
    }
    return fragment


class JulietFlower:
    def __init__(self, **data):
        self.seed_id = data.get("seed_id", "undefined")
        self.id = data.get("id", f"{self.seed_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
        self.mood = data.get("mood", "undefined")
        self.lineage_depth = data.get("lineage_depth", 0)
        self.entropy_score = data.get("entropy_score", 0.0)
        self.bloom_factor = data.get("bloom_factor", 1.0)
        self.agent = data.get("agent")
        self.seed_context = data.get("seed_context")
        self.sentences = data.get("sentences")
        self.tick = data.get("tick")
        self.urgency = data.get("urgency")
        self.commentary = data.get("commentary")

        # ✅ Emotional override control
        self.override_flags = {
            "reroute": False,
            "suppress_entropy": False,
            "drift_softening": False
        }


    def as_dict(self):
        return {
            "seed_id": self.seed_id,
            "mood": self.mood,
            "lineage_depth": self.lineage_depth,
            "entropy_score": self.entropy_score,
            "bloom_factor": self.bloom_factor,
            "agent": self.agent,
            "seed_context": self.seed_context,
            "sentences": self.sentences,
            "tick": self.tick,
            "urgency": self.urgency,
            "commentary": self.commentary
        }

    def __repr__(self):
        return (
            f"JulietFlower({self.seed_id}, mood={self.mood}, "
            f"lineage={self.lineage_depth}, entropy={self.entropy_score}, "
            f"agent={self.agent}, seed_context={self.seed_context})"
        )

    def compute_ash_soot_score(self):
        entropy = self.entropy_score
        lineage = self.lineage_depth
        urgency = self.urgency or 0.5

        ash_score = max(0, 1.0 - entropy) * (lineage / (lineage + 1))
        soot_score = entropy * urgency

        return round(ash_score, 3), round(soot_score, 3)

    def save(self, directory="juliet_flowers/bloom_metadata"):
        os.makedirs(directory, exist_ok=True)
        filename = f"{self.seed_id}_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.json"
        filepath = os.path.join(directory, filename)
        ash, soot = self.compute_ash_soot_score()
        print(f"[Ash/Soot] 🩶 Ash: {ash:.3f} | 🖤 Soot: {soot:.3f}")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.as_dict(), f, indent=2)

        if soot > 0.7:
            print(f"[Decay] 🖤 Soot threshold exceeded — recommend memory pruning or isolation.")

        if ash > 0.85:
            print(f"[Stability] 🩶 Ash threshold met — candidate for schema anchoring.")

        print(f"[Juliet] 🌸 Flower saved → {filepath}")
        return filepath


def load_all_blooms(directory="juliet_flowers/bloom_metadata"):
    blooms = []
    for f in os.listdir(directory):
        if f.endswith(".json"):
            with open(os.path.join(directory, f), "r", encoding="utf-8") as file:
                data = json.load(file)
                blooms.append(JulietFlower(**data))
    return blooms

def trigger_synthesis(n=3):
    from core.system_state import pulse
    bloom_dir = "juliet_flowers/bloom_metadata"
    files = sorted([f for f in os.listdir(bloom_dir) if f.endswith(".json")], reverse=True)[:n]

    if len(files) < n:
        print("[Synthesis] ⚠️ Not enough blooms to synthesize.")
        return

    traits = []
    for f in files:
        with open(os.path.join(bloom_dir, f), "r") as fp:
            traits.append(json.load(fp))

    mood = blend_moods(traits)
    lineage = max(t["lineage_depth"] for t in traits) + 1
    entropy = sum(t["entropy_score"] for t in traits) / n
    bloom_factor = sum(t["bloom_factor"] for t in traits) / n

    new_bloom = {
        "seed_id": f"synthesis-{datetime.now().strftime('%H%M%S')}",
        "lineage_depth": lineage,
        "entropy_score": entropy,
        "bloom_factor": bloom_factor,
        "mood": mood
    }
    assign_belief_resonance(new_bloom)


    print(f"[Synthesis] ✨ Generating fusion bloom from last {n}...")
    print(f"🧬 → Lineage: {lineage}, Entropy: {entropy:.2f}, Mood: {mood}")

    spawn_bloom(new_bloom, pulse=pulse)
    owl_log_rebloom(new_bloom)
    owl_analyze_synthesis(traits, new_bloom)


def mark_for_decay(self, reason=""):
    self.decay_flag = True
    self.decay_reason = reason
    print(f"[Juliet] ⚰️ Marked for decay: {self.seed_id} | Reason: {reason}")

def mark_for_review(self, reason=""):
    self.review_flag = True
    self.review_reason = reason
    print(f"[Juliet] 🔍 Marked for review: {self.seed_id} | Reason: {reason}")

