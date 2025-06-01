from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
import os
import json
import time
import pandas as pd
from datetime import datetime
from collections import defaultdict
from typing import Optional, Dict, Any, List
from schema.schema_state import get_current_zone, get_zone_streak
from core.event_bus import event_bus, BloomEmitted, TickEvent
from tracers.spider import SpiderTrace
from semantic.vector_core import similarity, embed_text
from semantic.vector_model import model
from bloom.juliet_flower import JulietFlower
from codex.sigil_emitter import scup_sigil_emitter
from owl.visual_inspector import run_visual
from owl.visual_registry import get_visual_modules
from owl.owl_tracer_log import owl_log
from schema.scup_loop import get_latest_scup


# Configuration paths
TRUST_FILE = "juliet_flowers/cluster_report/seed_trust_scores.json"
ANCESTRY_LOG_PATH = "logs/rebloom_ancestry.json"
VECTOR_DRIFT_DIR = "juliet_flowers/cluster_report"

# Ensure directories exist
os.makedirs(os.path.dirname(ANCESTRY_LOG_PATH), exist_ok=True)
os.makedirs(VECTOR_DRIFT_DIR, exist_ok=True)


class OwlAuditor:
    """
    The Owl Auditor observes system events, tracks trust scores,
    manages mood pressure, and triggers visual inspections.
    """
    
    def __init__(self, pulse=None):
        """
        Initialize the Owl Auditor
        
        Args:
            pulse: Optional pulse heat system instance
        """
        self.pulse = pulse or self._get_global_pulse()
        self.last_moods = defaultdict(set)
        self.mood_pressure = defaultdict(int)
        self.seed_penalties = {}
        self.last_decay = time.time()
        self.enabled = False
        self.tick_count = 0
        self.tick_interval = 50
        self.trust_scores = self.load_trust_scores()
        
        # Visual module triggers based on spider actions
        self.spider_visual_map = {
            "revive": ["belief_zone_animator"],
            "prune": ["entropy_cluster_plot"],
            "review": ["drift_compass", "rebloom_lineage_animator"]
        }
        
        # Mood weight configuration
        self.mood_weights = {
            "calm": 0.5,
            "curious": 0.8,
            "reflective": 1.0,
            "anxious": 1.3,
            "overload": 1.6,
            "transcendent": 0.3,
            "emergent": 1.2
        }
        
        # Subscribe to events
        event_bus.subscribe(SpiderTrace, self.on_spider_trace)
        
        print("[OwlAuditor] 🦉 Initialized with enhanced monitoring")
    
    def _get_global_pulse(self):
        """Get pulse from global context if available"""
        try:
            import builtins
            return getattr(builtins, 'pulse', None)
        except:
            return None
    
    def enable_scheduling(self, tick_interval: int = 50):
        """
        Enable periodic scheduling of owl activities
        
        Args:
            tick_interval: How often to perform scheduled tasks
        """
        self.enabled = True
        self.tick_interval = tick_interval
        event_bus.subscribe(BloomEmitted, self.on_bloom)
        event_bus.subscribe(TickEvent, self._on_tick)
        print(f"[OwlAuditor] 📅 Scheduling enabled (interval: {tick_interval} ticks)")
    
    async def on_spider_trace(self, event: SpiderTrace):
        """Handle spider trace events by triggering appropriate visuals"""
        print(f"[OwlAuditor] 🧠 Received SpiderTrace: {event.action} → {event.bloom_id} | {event.reason}")
        
        # Get visual modules to trigger based on action
        visuals_to_trigger = self.spider_visual_map.get(event.action, [])
        available_visuals = get_visual_modules()
        
        for visual_name in visuals_to_trigger:
            if visual_name in available_visuals:
                try:
                    run_visual(visual_name)
                    owl_log(f"[OwlAuditor] Triggered '{visual_name}' from Spider action '{event.action}': {event.bloom_id}")
                except Exception as e:
                    print(f"[OwlAuditor] ❌ Failed to run visual '{visual_name}': {e}")
            else:
                print(f"[OwlAuditor] ⚠️ Visual '{visual_name}' not available")
    
    async def on_bloom(self, event: BloomEmitted):
        """Process bloom events and update trust/pressure metrics"""
        print(f"[OwlAuditor] 🌸 Bloom received from {event.source} | mood: {event.mood_tag}")
        
        for seed in event.semantic_seeds:
            # Check trust score and apply penalties
            trust = self.trust_scores.get(seed, 0.5)
            if trust < 0.3:
                if self.pulse and hasattr(self.pulse, 'apply_penalty'):
                    self.pulse.apply_penalty(seed, factor=0.7)
                print(f"[OwlAuditor] ❌ Pruning low-trust seed {seed} | trust={trust:.2f}")
            
            # Track mood transitions
            previous = self.last_moods[seed]
            if event.source not in previous:
                if self.pulse and hasattr(self.pulse, 'decay_penalty_for_seed'):
                    self.pulse.decay_penalty_for_seed(seed, 0.1)
            previous.add(event.source)
            self.last_moods[seed] = previous
            
            # Create reflection flower for certain moods
            if event.mood_tag in ["reflective", "anxious", "overload", "emergent"]:
                await self._create_reflection_flower(event, seed)
        
        # Update mood pressure
        self.mood_pressure[event.mood_tag] += 1
        self._update_heat()
        
        # Log bloom statistics
        self._log_bloom_stats(event)
    
    async def _create_reflection_flower(self, event: BloomEmitted, seed: str):
        """Create a reflection flower for introspective moods"""
        try:
            flower = JulietFlower(
                agent=event.source,
                mood=event.mood_tag,
                seed_context=event.semantic_seeds,
                sentences=[
                    f"I am {event.source}.",
                    f"My mood is {event.mood_tag}.",
                    f"I passed through {seed} again.",
                    "The memory is faint, but returning.",
                    "I suspect a pattern in this reflection.",
                    "Calm or not, I have seen this node before.",
                    "Drift feels gentle now.",
                    "The rhythm of pulses remains steady.",
                    "I sense the weight of past iterations.",
                    "This sentence completes the thought bloom."
                ]
            )
            flower.save()
            print(f"[OwlAuditor] 🌺 Created reflection flower for {event.mood_tag} mood")
        except Exception as e:
            print(f"[OwlAuditor] ❌ Failed to create reflection flower: {e}")
    
    async def _on_tick(self, event: TickEvent):
        """Handle periodic tick events"""
        if not self.enabled:
            return
        
        self.tick_count += 1
        
        # Periodic decay
        if self.tick_count % self.tick_interval == 0:
            self._decay_pressure()
            self._update_heat()
        
        # Zone-aware reflex
        await self._check_zone_reflex()
        
        # Periodic visual audit
        if self.tick_count % 150 == 0:
            await self._perform_visual_audit()
        
        # Periodic sigil emission
        if self.tick_count % 25 == 0:
            try:
                await scup_sigil_emitter(self.pulse)
            except Exception as e:
                print(f"[OwlAuditor] ⚠️ Sigil emission error: {e}")
    
    async def _check_zone_reflex(self):
        """Check thermal zones and trigger reflexes if needed"""
        try:
            if self.pulse:
                zone = get_current_zone(self.pulse)
                current_zone, streak = get_zone_streak()
                
                if current_zone == "🔴 surge" and streak >= 5:
                    print("[OwlAuditor] ⚠️ Sustained surge zone — invoking decay reflex")
                    self._decay_pressure()
                    owl_log(f"[Reflex] 🔥 Decay triggered at tick {self.tick_count} due to surge streak")
                    
                    # Additional surge mitigation
                    if self.pulse and hasattr(self.pulse, 'remove_heat'):
                        self.pulse.remove_heat(0.5, "owl_surge_mitigation")
                
                elif current_zone == "🟢 calm" and streak >= 10:
                    # Inject some activity during prolonged calm
                    if self.pulse and hasattr(self.pulse, 'add_heat'):
                        self.pulse.add_heat(0.2, "owl_activity_injection", "preventing stasis")
                    
        except Exception as e:
            print(f"[OwlAuditor] ❌ Zone reflex error: {e}")
    
    async def _perform_visual_audit(self):
        """Perform periodic visual system audit"""
        print(f"[OwlAuditor] 🧠 Visual audit at tick {self.tick_count}")
        
        try:
            visual_modules = get_visual_modules()
            
            # Prioritize certain visuals based on system state
            priority_visuals = []
            
            if self.get_current_heat() > 7.0:
                priority_visuals.extend(["pulse_map_renderer", "entropy_cluster_plot"])
            
            scup = get_latest_scup()
            if scup < 0.3:
                priority_visuals.append("belief_zone_animator")
            
            # Run priority visuals first
            for visual in priority_visuals:
                if visual in visual_modules:
                    run_visual(visual)
                    owl_log(f"[Audit] Priority visual: {visual}")
            
            # Run remaining visuals
            for visual in visual_modules:
                if visual not in priority_visuals:
                    run_visual(visual)
                    
        except Exception as e:
            print(f"[OwlAuditor] ❌ Visual audit error: {e}")
    
    def log_vector_drift(self, parent_text: str, child_text: str, bloom_id: str) -> float:
        """
        Log semantic drift between parent and child texts
        
        Returns:
            Drift score (0.0 = identical, 1.0 = completely different)
        """
        try:
            parent_vec = embed_text(parent_text, model)
            child_vec = embed_text(child_text, model)
            drift_score = 1 - similarity(parent_vec, child_vec)
            
            log_path = os.path.join(VECTOR_DRIFT_DIR, f"vector_drift_{bloom_id}.log")
            
            drift_data = {
                "bloom_id": bloom_id,
                "timestamp": datetime.now().isoformat(),
                "drift_score": drift_score,
                "parent_preview": parent_text[:100] + "..." if len(parent_text) > 100 else parent_text,
                "child_preview": child_text[:100] + "..." if len(child_text) > 100 else child_text
            }
            
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(drift_data, f, indent=2)
            
            print(f"[OwlAuditor] 🧠 Vector drift logged for {bloom_id} | Δ = {drift_score:.4f}")
            
            # Alert if drift is significant
            if drift_score > 0.7:
                owl_log(f"⚠️ High semantic drift detected: {bloom_id} (Δ={drift_score:.4f})")
            
            return drift_score
            
        except Exception as e:
            print(f"[OwlAuditor] ❌ Vector drift logging error: {e}")
            return 0.0
    
    def reflect_on_zone_pulse(self) -> Dict[str, Any]:
        """Analyze recent zone patterns and generate insights"""
        try:
            if not self.pulse or not hasattr(self.pulse, 'get_recent_zone_window'):
                return {}
            
            history = self.pulse.get_recent_zone_window(15)
            if not history:
                return {}
            
            zone_counts = pd.DataFrame(history)["zone"].value_counts().to_dict()
            most_common = max(zone_counts, key=zone_counts.get)
            
            reflection = {
                "zone_distribution": zone_counts,
                "dominant_zone": most_common,
                "analysis_window": len(history),
                "timestamp": datetime.now().isoformat()
            }
            
            # Generate insight
            if most_common == "🔴 surge":
                reflection["insight"] = "System experiencing sustained high activity"
            elif most_common == "🟢 calm":
                reflection["insight"] = "System in stable, low-activity state"
            else:
                reflection["insight"] = "System in balanced operational state"
            
            owl_log(f"📊 Zone reflection: {zone_counts} | Dominant: {most_common}")
            
            return reflection
            
        except Exception as e:
            print(f"[OwlAuditor] ❌ Zone reflection error: {e}")
            return {}
    
    def load_trust_scores(self) -> Dict[str, float]:
        """Load seed trust scores from file"""
        try:
            os.makedirs(os.path.dirname(TRUST_FILE), exist_ok=True)
            
            if os.path.exists(TRUST_FILE):
                with open(TRUST_FILE, "r") as f:
                    return json.load(f)
            else:
                # Initialize with default trust scores
                default_scores = {}
                with open(TRUST_FILE, "w") as f:
                    json.dump(default_scores, f)
                return default_scores
                
        except Exception as e:
            print(f"[OwlAuditor] ⚠️ Could not load trust scores: {e}")
            return {}
    
    def update_trust_score(self, seed: str, delta: float):
        """Update trust score for a seed"""
        current = self.trust_scores.get(seed, 0.5)
        new_score = max(0.0, min(1.0, current + delta))
        self.trust_scores[seed] = new_score
        
        # Save updated scores
        try:
            with open(TRUST_FILE, "w") as f:
                json.dump(self.trust_scores, f, indent=2)
        except Exception as e:
            print(f"[OwlAuditor] ❌ Failed to save trust scores: {e}")
    
    def _decay_pressure(self):
        """Decay mood pressure over time"""
        now = time.time()
        if now - self.last_decay >= 5:
            for mood in list(self.mood_pressure):
                self.mood_pressure[mood] = max(0, self.mood_pressure[mood] - 1)
            self.last_decay = now
            
            # Log significant pressure changes
            total_pressure = sum(self.mood_pressure.values())
            if total_pressure > 10:
                owl_log(f"💨 High mood pressure: {total_pressure} | Distribution: {dict(self.mood_pressure)}")
    
    def _update_heat(self):
        """Update pulse heat based on mood pressure"""
        if not self.pulse or not hasattr(self.pulse, 'heat'):
            return
        
        total = sum(self.mood_pressure.values())
        if total == 0:
            self.pulse.heat = 1.0
            return
        
        # Calculate weighted mood pressure
        weighted_sum = sum(
            self.mood_pressure[mood] * self.mood_weights.get(mood, 1.0)
            for mood in self.mood_pressure
        )
        
        # Update heat with bounds
        new_heat = weighted_sum / total
        self.pulse.heat = min(2.0, max(0.3, new_heat))
        
        # Log if heat is getting high
        if self.pulse.heat > 1.5:
            print(f"[OwlAuditor] 🔥 Heat elevated: {self.pulse.heat:.2f} | Mood pressure: {dict(self.mood_pressure)}")
    
    def get_current_heat(self) -> float:
        """Get current heat value safely"""
        if self.pulse and hasattr(self.pulse, 'heat'):
            return self.pulse.heat
        elif self.pulse and hasattr(self.pulse, 'get_heat'):
            return self.pulse.get_heat()
        return 1.0
    
    def _log_bloom_stats(self, event: BloomEmitted):
        """Log bloom statistics for analysis"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "source": event.source,
            "mood": event.mood_tag,
            "seed_count": len(event.semantic_seeds),
            "total_mood_pressure": sum(self.mood_pressure.values()),
            "current_heat": self.get_current_heat()
        }
        
        # You could write this to a file or just keep in memory
        # For now, just log significant events
        if stats["total_mood_pressure"] > 15:
            owl_log(f"📈 High activity bloom: {stats}")
    
    def get_auditor_stats(self) -> Dict[str, Any]:
        """Get comprehensive auditor statistics"""
        return {
            "tick_count": self.tick_count,
            "enabled": self.enabled,
            "mood_pressure": dict(self.mood_pressure),
            "total_pressure": sum(self.mood_pressure.values()),
            "trust_score_count": len(self.trust_scores),
            "average_trust": sum(self.trust_scores.values()) / max(1, len(self.trust_scores)),
            "current_heat": self.get_current_heat(),
            "last_decay": datetime.fromtimestamp(self.last_decay).isoformat()
        }


def run_entropy_scan():
    """
    Run entropy analysis scan
    """
    try:
        # Try to get pulse from global context
        import builtins
        pulse = getattr(builtins, 'pulse', None)
        
        if pulse:
            current_heat = pulse.get_heat() if hasattr(pulse, 'get_heat') else getattr(pulse, 'heat', 0.0)
            print(f"[OwlAuditor] 🔎 Entropy Scan → Pulse Heat: {current_heat:.3f}")
            
            # Get SCUP
            try:
                scup = get_latest_scup()
                print(f"[OwlAuditor] 📊 Current SCUP: {scup:.3f}")
            except:
                pass
        else:
            print("[OwlAuditor] 🔎 Entropy Scan → No pulse available")
            
    except Exception as e:
        print(f"[OwlAuditor] ❌ Entropy scan error: {e}")


# === Reblooms: Ancestry Tracking ===

def track_rebloom_ancestry(bloom_data: Dict[str, Any], parent_bloom: Optional[Any] = None) -> Dict[str, Any]:
    """
    Track ancestry lineage for reblooms
    
    Args:
        bloom_data: Current bloom data
        parent_bloom: Parent bloom object (if any)
        
    Returns:
        Updated bloom data with ancestry information
    """
    parent_id = getattr(parent_bloom, "seed_id", None) if parent_bloom else None
    parent_line = getattr(parent_bloom, "ancestry_line", []) if parent_bloom else []
    
    # Build ancestry line
    ancestry_line = parent_line + [parent_id] if parent_id else parent_line
    bloom_data["parent_id"] = parent_id
    bloom_data["ancestry_line"] = ancestry_line
    bloom_data["generation"] = len(ancestry_line) + 1
    
    # Lock deep ancestries to prevent infinite chains
    if len(ancestry_line) > 10:
        bloom_data["ancestry_locked"] = True
        print(f"[OwlAuditor] 🔒 Ancestry locked for {bloom_data.get('seed_id')} - depth limit reached")
    
    # Log the ancestry
    log_ancestry(bloom_data.get("seed_id", "unknown"), ancestry_line)
    
    return bloom_data


def log_ancestry(seed_id: str, lineage: List[str]):
    """Log bloom ancestry to file"""
    try:
        os.makedirs(os.path.dirname(ANCESTRY_LOG_PATH), exist_ok=True)
        
        # Load existing data
        if os.path.exists(ANCESTRY_LOG_PATH):
            with open(ANCESTRY_LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        
        # Update with new ancestry
        data[seed_id] = {
            "timestamp": datetime.now().isoformat(),
            "lineage": lineage,
            "depth": len(lineage)
        }
        
        # Save back
        with open(ANCESTRY_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print(f"[OwlAuditor] 🧬 Tracked ancestry for {seed_id}: depth={len(lineage)}")
        
    except Exception as e:
        print(f"[OwlAuditor] ❌ Failed to log ancestry: {e}")


# Module initialization
print("[OwlAuditor] 🦉 Owl auditing system initialized")