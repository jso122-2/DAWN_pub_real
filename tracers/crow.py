from tracers.base import Tracer, TRACER_REGISTRY
from core.event_bus import event_bus, TickEvent, Event
from core.system_state import pulse
from owl.owl_tracer_log import owl_log
import random
from collections import defaultdict
from visuals.stall_density_animator import save_stall_snapshot
save_stall_snapshot()

# Event emitted when Crow detects schema issues
class CrowPing(Event):
    def __init__(self, tracer_id, node, comment):
        self.tracer_id = tracer_id
        self.node = node
        self.comment = comment

# Sigil-triggered contradiction scan
def crow_action():
    contradiction_found = random.choice([True, False])
    if contradiction_found:
        msg = "[🦅 Crow] Schema contradiction detected."
        owl_log(msg)
        print(msg)
    else:
        print("[🦅 Crow] Scan clean.")

# Crow with drift tracking + contradiction stall map
class Crow(Tracer):
    def __init__(self, tracer_id="crow-003", start="B2"):
        super().__init__(
            name=tracer_id,
            role="Contradiction detector and schema break auditor",
            watch=["⟁", "/X-"],
            act=crow_action
        )
        self.current_node = start
        self.recent_seeds = []
        self.belief_stall_count = defaultdict(int)
        TRACER_REGISTRY[tracer_id] = self
        event_bus.subscribe(TickEvent, self.on_tick)

    async def on_tick(self, event: TickEvent):
        if random.random() < 0.6:
            self.current_node = random.choice(["A2", "B2", "C3"])
            self.recent_seeds.append(self.current_node)

            if len(self.recent_seeds) >= 3 and len(set(self.recent_seeds[-3:])) == 1:
                node = self.current_node
                self.belief_stall_count[node] += 1

    def update_stall_log(node):
        path = "owl/logs/crow_stall_log.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                log = json.load(f)
        else:
            log = {}
        log[node] = log.get(node, 0) + 1
        with open(path, "w") as f:
            json.dump(log, f, indent=2)

        update_stall_log(node)

                comment = f"⚠️ Crow detected loop stall at {node} (count={self.belief_stall_count[node]})"
                owl_log(comment)
                await event_bus.publish(CrowPing(self.name, node, comment))
                print(f"[🦅 Crow] Pinged: {comment}")

                # Optional: Penalize node if loop count is high
                if self.belief_stall_count[node] >= 2:
                    pulse.apply_penalty(node, factor=0.5)
                    print(f"[Crow] Applied penalty to {node} due to repeated stalls.")
            else:
                print(f"[🦅 Crow] Watching → {self.current_node}")
        else:
            print(f"[🦅 Crow] Perched silently.")
