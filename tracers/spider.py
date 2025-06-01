# File Path: /src/tracers/spider.py

from core.event_bus import TickEvent, event_bus, Event
from tracers.base import Tracer
from bloom.registry import get_active_blooms, get_dormant_blooms
from bloom.spawn_bloom import spawn_bloom
from owl.lineage_tools import check_lineage_contradictions
from owl.entropy import get_entropy_score
from owl.trust_model import get_trust_score
from owl.owl_tracer_log import owl_log
from semantic.edge_scanner import detect_glow_trace
import random

class SpiderTrace(Event):
    def __init__(self, action, bloom_id, reason):
        self.action = action
        self.bloom_id = bloom_id
        self.reason = reason

class SpiderTracer(Tracer):
    def __init__(self):
        super().__init__(
            name="Spider",
            role="weaver + examiner",
            watch=["/instability", "/contradiction", "/recur"],
            act=self.respond
        )
        event_bus.subscribe(TickEvent, self.on_tick)

        # Import rhizome_map inside the function to avoid circular imports
        self.rhizome_map = self.get_rhizome_map()

    def get_rhizome_map(self):
        from rhizome.rhizome_map import RhizomeMap
        return RhizomeMap()

    def get_scup_value(self):
        from schema.scup_loop import get_latest_scup  # Import moved inside
        return get_latest_scup()

    async def on_tick(self, event: TickEvent):
        scup_value = self.get_scup_value()  # Get SCUP value during each tick
        print(f"[SpiderTracer] SCUP value: {scup_value}")
        
        # Now you can use SCUP value for decision-making
        if scup_value < 0.4:
            print("[SpiderTracer] SCUP value low, pruning unstable blooms!")
            self.prune_unstable_blooms()  # Example action based on SCUP value
        elif scup_value > 0.8:
            print("[SpiderTracer] SCUP value high, reinforcing relevant blooms!")
            self.reactivate_relevant_blooms()  # Example action based on SCUP value

    def reactivate_relevant_blooms(self):
        dormant = get_dormant_blooms()
        for bloom in dormant:
            entropy = get_entropy_score(bloom)
            trust = get_trust_score(bloom)
            if entropy > 0.5 and trust > 0.6:
                owl_log(f"🕷️ Reactivating {bloom.seed_id} | entropy={entropy:.2f}, trust={trust:.2f}")
                spawn_bloom(bloom.to_dict())
                event_bus.publish(SpiderTrace("revive", bloom.seed_id, "entropy/trust rebalance"))

    def prune_unstable_blooms(self):
        active = get_active_blooms()
        for bloom in active:
            entropy = get_entropy_score(bloom)
            trust = get_trust_score(bloom)
            if entropy > 0.9 or trust < 0.3:
                owl_log(f"✂️ Pruning {bloom.seed_id} | entropy={entropy:.2f}, trust={trust:.2f}")
                bloom.mark_for_decay("Spider pruning due to entropy/trust")
                event_bus.publish(SpiderTrace("decay", bloom.seed_id, "high entropy or low trust"))

    def cross_examine_lineage(self):
        active = get_active_blooms()
        for bloom in active:
            contradictions = check_lineage_contradictions(bloom)
            if contradictions:
                owl_log(f"🕸️ Contradiction in {bloom.seed_id} → {contradictions}")
                bloom.mark_for_review("Spider contradiction detection")
                event_bus.publish(SpiderTrace("review", bloom.seed_id, "lineage contradiction"))
