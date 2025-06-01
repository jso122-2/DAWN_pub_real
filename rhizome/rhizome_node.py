# /rhizome/rhizome_node.py

class RhizomeNode:
    def __init__(self, bloom):
        """
        Initialize a rhizome node based on a Juliet bloom.
        """
        self.seed_id = bloom.seed_id
        self.edges = {}  # target_seed_id → edge weight
        self.semantic_vector = None
        self.nutrient_reservoir = {}  # nutrient_type → float
        self.activity_log = []  # optional debug trace

    def update_vector(self, vector):
        """
        Update the node’s semantic vector.
        """
        self.semantic_vector = vector
        self.activity_log.append(f"🔄 Vector updated")

    def add_edge(self, target_seed, weight=1.0):
        """
        Create or update an edge to another node with metadata.
        """
        if target_seed not in self.edges:
            self.edges[target_seed] = {
                "weight": weight,
                "reinforcement_score": 0.0
            }
        else:
            self.edges[target_seed]["weight"] = weight  # update weight if exists


    def send_nutrient(self, target_seed, nutrient_type, strength):
        """
        Send nutrient along a path to a neighbor.
        """
        prev = self.nutrient_reservoir.get(nutrient_type, 0.0)
        self.nutrient_reservoir[nutrient_type] = max(0.0, prev - strength)
        self.activity_log.append(f"🪴 Sent {nutrient_type} → {target_seed} [{strength:.2f}]")

    def receive_nutrient(self, nutrient_type, amount):
        """
        Receive nutrient from a neighbor or system.
        """
        prev = self.nutrient_reservoir.get(nutrient_type, 0.0)
        self.nutrient_reservoir[nutrient_type] = prev + amount
        self.activity_log.append(f"🌿 Received {nutrient_type} [+{amount:.2f}]")

    def get_nutrient_level(self, nutrient_type):
        """
        Query current level of a given nutrient.
        """
        return self.nutrient_reservoir.get(nutrient_type, 0.0)

    def summary(self):
        return {
            "seed_id": self.seed_id,
            "edges": self.edges,
            "nutrient_reservoir": self.nutrient_reservoir,
            "vector_len": len(self.semantic_vector) if self.semantic_vector else 0
        }

    def check_and_seal(self, entropy_threshold=0.7, nutrient_threshold=0.05):
        """
        Seal node if low flow and high entropy.
        """
        total_flow = sum(self.nutrient_reservoir.values())
        entropy = getattr(self, "entropy_score", 0.0)

        if total_flow < nutrient_threshold and entropy > entropy_threshold:
            self.sealed = True
            self.activity_log.append(f"🧊 Auto-sealed due to low flow + high entropy (e={entropy:.2f})")
            print(f"[RhizomeNode] 🧊 Sealed {self.seed_id} — low flow ({total_flow:.2f}), high entropy ({entropy:.2f})")
            return True

        return False

