# File Path: /src/rhizome/rhizome_map.py

import asyncio
from rhizome.rhizome_pathfinder import find_path_semantic  # Semantic pathfinding
from rhizome.rhizome_pathfinder import find_path  # Basic pathfinding for fallback
from rhizome.nutrient_flow import flow_nutrient
from rhizome.rhizome_node import RhizomeNode
from rhizome.nutrient_flow_logger import log_nutrient_transfer
from rhizome.decay_loss_logger import log_decay_loss
from schema.schema_state import get_current_zone
from schema.rebloom_queue import push_to_rebloom_queue
from schema.rebloom_summary import log_rebloom_trigger

class RhizomeMap:
    def __init__(self):
        self.nodes = {}  # seed_id → RhizomeNode

    def register_bloom(self, bloom):
        seed = bloom.seed_id
        if seed not in self.nodes:
            self.nodes[seed] = RhizomeNode(bloom)
        self.nodes[seed].update_vector(bloom.semantic_vector)

    def add_edge(self, seed_a, seed_b, weight=1.0):
        if seed_a in self.nodes and seed_b in self.nodes:
            self.nodes[seed_a].add_edge(seed_b, weight)
            self.nodes[seed_b].add_edge(seed_a, weight)

    async def route_nutrient(self, from_seed, to_seed, nutrient_type, strength=1.0, tick_id=None):
        """
        Async semantic routing with per-hop parallel flows.
        Tracks and logs decay loss.
        """
        if from_seed not in self.nodes or to_seed not in self.nodes:
            print(f"[RhizomeMap] ❌ Invalid seed(s): {from_seed}, {to_seed}")
            return False

        path = await find_path_semantic(from_seed, to_seed, self.nodes)
        if not path:
            print(f"[RhizomeMap] 🚫 No valid path from {from_seed} to {to_seed}")
            return False

        print(f"[RhizomeMap] 🌿 Routing {nutrient_type} via {path}")
        hop_losses = []
        tasks = []
        delivered = strength

        for i in range(len(path) - 1):
            src = self.nodes[path[i]]
            tgt = self.nodes[path[i + 1]]
            task = asyncio.create_task(flow_nutrient(src, tgt, nutrient_type, delivered, tick_id=tick_id))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        for result in results:
            loss = result["requested"] - result["delivered"]
            hop_losses.append((result["from"], result["to"], round(loss, 4)))
            delivered = result["delivered"]

        if tick_id:
            log_decay_loss(tick_id, from_seed, to_seed, nutrient_type, strength, delivered)

        for hop in hop_losses:
            print(f"[HopLoss] {hop[0]} → {hop[1]}: -{hop[2]} {nutrient_type}")

        return True

    def broadcast_nutrient(self, origin_seed, nutrient_type, base_strength=0.5, base_radius=2, tick_id=None):
        """
        Broadcasts nutrient outward with schema-pressure adjusted radius/strength.
        """
        if origin_seed not in self.nodes:
            return

        zone = get_current_zone()
        if zone == "🔴 surge":
            strength = base_strength * 1.5
            radius = base_radius + 1
        elif zone == "🟢 calm":
            strength = base_strength * 0.8
            radius = max(1, base_radius - 1)
        else:
            strength = base_strength
            radius = base_radius

        visited = set()
        queue = [(origin_seed, 0)]

        while queue:
            current, depth = queue.pop(0)
            if depth > radius:
                continue
            visited.add(current)
            node = self.nodes[current]

        for neighbor_seed in node.edges:
            if neighbor_seed not in visited:
                asyncio.create_task(self.route_nutrient(
                    origin_seed, neighbor_seed, nutrient_type,
                    strength / (depth + 1), tick_id=tick_id
                ))
                queue.append((neighbor_seed, depth + 1))
