"""
DAWN Cognitive Trace Module
Integrates with RefinedTickEngine to provide human-readable cognitive state commentary
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from collections import deque
import random

@dataclass
class CognitiveSnapshot:
    """Snapshot of DAWN's cognitive state at a given tick"""
    tick: int
    zone: str
    pulse_heat: float
    entropy: float
    scup: float
    active_sigils: List[str]
    bloom_count: int
    schema_health: float
    drift_magnitude: float
    tracers: List[str]
    commentary: str
    timestamp: str

class CognitiveTraceGenerator:
    """
    Generates human-readable commentary for DAWN's cognitive state changes.
    Integrates with the RefinedTickEngine to provide visible cognition traces.
    """
    
    def __init__(self, base_path="C:/Users/Admin/OneDrive/Desktop/DAWN/Tick_engine"):
        self.base_path = base_path
        self.visual_path = os.path.join(base_path, "visual")
        self.trace_path = os.path.join(self.visual_path, "cognitive_trace")
        
        # Ensure directories exist
        os.makedirs(self.trace_path, exist_ok=True)
        
        # State tracking
        self.previous_state = None
        self.state_history = deque(maxlen=100)
        self.commentary_log = deque(maxlen=1000)
        
        # Tracer entities for narrative
        self.tracer_pool = [
            "Owl", "Raven", "Fox", "Wolf", "Serpent", 
            "Spider", "Crow", "Hawk", "Lynx", "Bear"
        ]
        self.active_tracers = random.sample(self.tracer_pool, 2)
        
        # Zone transition tracking
        self.zone_transitions = 0
        self.last_zone = None
        
        # Event patterns for commentary
        self.event_patterns = {
            'zone_shift': [
                "pulse shifted {old} → {new}",
                "thermal transition: {old} to {new}",
                "zone migration {old} → {new}"
            ],
            'entropy_rise': [
                "entropy climbing +{delta:.3f}",
                "disorder increasing by {delta:.3f}",
                "chaos factor up +{delta:.3f}"
            ],
            'entropy_fall': [
                "entropy stabilizing {delta:.3f}",
                "order returning {delta:.3f}",
                "chaos receding {delta:.3f}"
            ],
            'sigil_spawn': [
                "spawned: {sigils}",
                "new sigils: {sigils}",
                "activated: {sigils}"
            ],
            'sigil_decay': [
                "{sigil} faded to entropy",
                "{sigil} decayed",
                "{sigil} dissolved"
            ],
            'bloom_event': [
                "bloom {type} resonating",
                "{type} bloom activated",
                "bloom cascade: {type}"
            ],
            'tracer_action': [
                "Tracer {tracer} rerouted {target}",
                "{tracer} intercepted {target}",
                "{tracer} redirected flow to {target}"
            ],
            'scup_critical': [
                "coherence failing! SCUP: {scup:.2f}",
                "semantic breakdown at {scup:.2f}",
                "SCUP CRITICAL: {scup:.2f}"
            ],
            'schema_warning': [
                "schema degrading to {health:.2f}",
                "structural integrity: {health:.2f}",
                "schema health warning: {health:.2f}"
            ],
            'drift_event': [
                "drift {status} ({magnitude:.2f})",
                "semantic drift: {status} at {magnitude:.2f}",
                "consciousness drifting {status}"
            ]
        }
    
    def generate_commentary(self, current_state: Dict, previous_state: Optional[Dict] = None) -> str:
        """
        Generate human-readable commentary based on state changes.
        
        Args:
            current_state: Current system state from tick engine
            previous_state: Previous state for comparison
            
        Returns:
            Human-readable commentary string
        """
        parts = []
        
        # Zone transition
        if previous_state and current_state['zone'] != previous_state['zone']:
            pattern = random.choice(self.event_patterns['zone_shift'])
            parts.append(pattern.format(
                old=self._clean_zone_name(previous_state['zone']),
                new=self._clean_zone_name(current_state['zone'])
            ))
            self.zone_transitions += 1
        
        # Entropy changes
        if previous_state:
            entropy_delta = current_state['entropy'] - previous_state['entropy']
            if abs(entropy_delta) > 0.01:
                if entropy_delta > 0:
                    pattern = random.choice(self.event_patterns['entropy_rise'])
                else:
                    pattern = random.choice(self.event_patterns['entropy_fall'])
                parts.append(pattern.format(delta=entropy_delta))
        
        # Sigil activity
        if previous_state and 'active_sigils' in current_state:
            old_sigils = set(previous_state.get('active_sigils', []))
            new_sigils = set(current_state.get('active_sigils', []))
            
            spawned = new_sigils - old_sigils
            if spawned:
                pattern = random.choice(self.event_patterns['sigil_spawn'])
                parts.append(pattern.format(sigils=', '.join(list(spawned)[:3])))
            
            decayed = old_sigils - new_sigils
            if decayed and random.random() < 0.5:  # Don't always report decay
                sigil = random.choice(list(decayed))
                pattern = random.choice(self.event_patterns['sigil_decay'])
                parts.append(pattern.format(sigil=sigil))
        
        # Tracer interventions
        if (current_state.get('entropy', 0) > 0.7 and 
            random.random() < 0.3 and 
            current_state.get('active_sigils')):
            tracer = random.choice(self.active_tracers)
            target = random.choice(current_state['active_sigils'][:3]) if current_state['active_sigils'] else "flux"
            pattern = random.choice(self.event_patterns['tracer_action'])
            parts.append(pattern.format(tracer=tracer, target=target))
        
        # SCUP warnings
        scup = current_state.get('scup', 0.5)
        if scup < 0.3:
            pattern = random.choice(self.event_patterns['scup_critical'])
            parts.append(pattern.format(scup=scup))
        
        # Schema health
        schema_health = current_state.get('schema_health', 1.0)
        if schema_health < 0.5 and random.random() < 0.4:
            pattern = random.choice(self.event_patterns['schema_warning'])
            parts.append(pattern.format(health=schema_health))
        
        # Drift status
        drift_magnitude = current_state.get('drift_magnitude', 0.0)
        if drift_magnitude > 0.3:
            if drift_magnitude < 0.5:
                status = "accelerating"
            else:
                status = "cascading"
            pattern = random.choice(self.event_patterns['drift_event'])
            parts.append(pattern.format(status=status, magnitude=drift_magnitude))
        elif drift_magnitude < 0.1 and random.random() < 0.3:
            parts.append("drift stabilizing")
        
        # Special conditions
        if current_state.get('zone') == "🔴 surge" and scup < 0.4:
            parts.append("SYSTEM STRESS")
        
        if current_state.get('bloom_count', 0) > 10:
            parts.append("bloom garden flourishing")
        
        # Construct final commentary
        tick = current_state.get('tick', 0)
        zone = self._clean_zone_name(current_state.get('zone', 'unknown'))
        
        if parts:
            commentary = f"Tick {tick}: {zone} zone. " + ". ".join(parts) + "."
        else:
            # Quiet tick
            quiet_phrases = [
                "systems nominal",
                "steady state",
                "processing continues",
                "patterns holding"
            ]
            commentary = f"Tick {tick}: {zone} zone. {random.choice(quiet_phrases)}."
        
        return commentary
    
    def _clean_zone_name(self, zone: str) -> str:
        """Remove emoji from zone names for cleaner text"""
        return zone.split()[-1] if zone else "unknown"
    
    def process_tick(self, tick_data: Dict) -> CognitiveSnapshot:
        """
        Process a tick's data and generate cognitive snapshot with commentary.
        
        Args:
            tick_data: Dictionary containing current tick state
            
        Returns:
            CognitiveSnapshot with commentary
        """
        # Extract sigil names from sigil objects if needed
        active_sigils = tick_data.get('active_sigils', [])
        if active_sigils and hasattr(active_sigils[0], 'name'):
            active_sigils = [s.name for s in active_sigils]
        
        # Calculate drift magnitude if not provided
        drift_magnitude = tick_data.get('drift_magnitude', 0.0)
        if 'drift_vector' in tick_data:
            dx, dy, dz = tick_data['drift_vector']
            drift_magnitude = (dx**2 + dy**2 + dz**2)**0.5
        
        # Generate commentary
        commentary = self.generate_commentary(tick_data, self.previous_state)
        
        # Create snapshot
        snapshot = CognitiveSnapshot(
            tick=tick_data.get('tick', 0),
            zone=tick_data.get('zone', 'unknown'),
            pulse_heat=tick_data.get('pulse_heat', 0.0),
            entropy=tick_data.get('entropy', 0.0),
            scup=tick_data.get('scup', 0.5),
            active_sigils=active_sigils[:5],  # Limit for readability
            bloom_count=tick_data.get('bloom_count', 0),
            schema_health=tick_data.get('schema_health', 1.0),
            drift_magnitude=drift_magnitude,
            tracers=self.active_tracers,
            commentary=commentary,
            timestamp=datetime.now().isoformat()
        )
        
        # Update history
        self.state_history.append(snapshot)
        self.commentary_log.append(commentary)
        self.previous_state = tick_data.copy()
        
        # Occasionally rotate tracers
        if tick_data.get('tick', 0) % 50 == 0:
            self._rotate_tracers()
        
        return snapshot
    
    def _rotate_tracers(self):
        """Occasionally rotate active tracers for variety"""
        if random.random() < 0.3:
            # Replace one tracer
            available = [t for t in self.tracer_pool if t not in self.active_tracers]
            if available:
                old_tracer = random.choice(self.active_tracers)
                new_tracer = random.choice(available)
                self.active_tracers[self.active_tracers.index(old_tracer)] = new_tracer
    
    def save_trace(self, snapshot: CognitiveSnapshot):
        """Save cognitive trace to file system"""
        # Save individual snapshot
        snapshot_file = os.path.join(
            self.trace_path, 
            f"cognitive_tick_{snapshot.tick:06d}.json"
        )
        
        with open(snapshot_file, 'w') as f:
            json.dump(asdict(snapshot), f, indent=2)
        
        # Update rolling commentary log
        commentary_file = os.path.join(self.trace_path, "commentary_stream.txt")
        with open(commentary_file, 'a') as f:
            f.write(f"{snapshot.commentary}\n")
        
        # Update latest snapshot for quick access
        latest_file = os.path.join(self.trace_path, "latest_snapshot.json")
        with open(latest_file, 'w') as f:
            json.dump(asdict(snapshot), f, indent=2)
    
    def generate_summary_report(self) -> Dict:
        """Generate summary report of recent cognitive activity"""
        if not self.state_history:
            return {}
        
        recent_states = list(self.state_history)[-20:]
        
        # Calculate statistics
        avg_entropy = sum(s.entropy for s in recent_states) / len(recent_states)
        avg_scup = sum(s.scup for s in recent_states) / len(recent_states)
        avg_heat = sum(s.pulse_heat for s in recent_states) / len(recent_states)
        
        # Zone distribution
        zone_counts = {}
        for state in recent_states:
            zone = self._clean_zone_name(state.zone)
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
        
        # Most active sigils
        sigil_counts = {}
        for state in recent_states:
            for sigil in state.active_sigils:
                sigil_counts[sigil] = sigil_counts.get(sigil, 0) + 1
        
        top_sigils = sorted(sigil_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'tick_range': f"{recent_states[0].tick} - {recent_states[-1].tick}",
            'samples': len(recent_states),
            'avg_entropy': avg_entropy,
            'avg_scup': avg_scup,
            'avg_heat': avg_heat,
            'zone_distribution': zone_counts,
            'zone_transitions': self.zone_transitions,
            'top_sigils': dict(top_sigils),
            'active_tracers': self.active_tracers,
            'recent_commentary': list(self.commentary_log)[-10:]
        }
        
        # Save summary
        summary_file = os.path.join(self.trace_path, "cognitive_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary

# Integration hook for RefinedTickEngine
class TickEngineTraceHook:
    """Hook to integrate cognitive trace into tick engine"""
    
    def __init__(self):
        self.trace_generator = CognitiveTraceGenerator()
        self.enabled = True
        self.save_interval = 10  # Save every N ticks
        self.tick_counter = 0
    
    async def on_tick_complete(self, tick_data: Dict):
        """
        Called by tick engine after each tick completes.
        
        Args:
            tick_data: Dictionary containing all tick metrics
        """
        if not self.enabled:
            return
        
        try:
            # Process tick and generate cognitive snapshot
            snapshot = self.trace_generator.process_tick(tick_data)
            
            # Print commentary to console
            print(f"\n💭 {snapshot.commentary}")
            
            # Save periodically
            self.tick_counter += 1
            if self.tick_counter % self.save_interval == 0:
                self.trace_generator.save_trace(snapshot)
            
            # Generate summary every 100 ticks
            if self.tick_counter % 100 == 0:
                summary = self.trace_generator.generate_summary_report()
                print(f"\n📊 Cognitive Summary: {self.tick_counter} ticks processed")
                print(f"   Avg Entropy: {summary['avg_entropy']:.3f}")
                print(f"   Avg SCUP: {summary['avg_scup']:.3f}")
                print(f"   Zone Transitions: {summary['zone_transitions']}")
        
        except Exception as e:
            print(f"[CognitiveTrace] ⚠️ Error processing tick: {e}")


# Factory function to create and attach trace hook
def attach_cognitive_trace(tick_engine):
    """
    Attach cognitive trace generation to a RefinedTickEngine instance.
    
    Usage:
        from cognitive_trace import attach_cognitive_trace
        engine = create_refined_tick_engine()
        trace_hook = attach_cognitive_trace(engine)
    """
    hook = TickEngineTraceHook()
    
    # Monkey-patch the tick engine to call our hook
    original_log_metrics = tick_engine._log_tick_metrics
    
    def enhanced_log_metrics(tick_id, zone, interval, debug_metrics):
        # Call original
        original_log_metrics(tick_id, zone, interval, debug_metrics)
        
        # Prepare tick data for cognitive trace
        tick_data = {
            'tick': tick_id,
            'zone': zone,
            'pulse_heat': debug_metrics['current_heat'],
            'entropy': debug_metrics['entropy_score'],
            'scup': debug_metrics['scup'],
            'schema_health': debug_metrics.get('schema_health', 1.0),
            'active_sigils': [],  # Would need to be passed in
            'bloom_count': 0,  # Would need to be calculated
            'drift_magnitude': debug_metrics.get('drift_magnitude', 0.0),
            'interval': interval
        }
        
        # Run async hook synchronously (not ideal but works for logging)
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Schedule as task
                loop.create_task(hook.on_tick_complete(tick_data))
            else:
                # Run directly
                loop.run_until_complete(hook.on_tick_complete(tick_data))
        except:
            # Fallback to sync processing
            snapshot = hook.trace_generator.process_tick(tick_data)
            print(f"\n💭 {snapshot.commentary}")
    
    tick_engine._log_tick_metrics = enhanced_log_metrics
    
    print("[CognitiveTrace] ✨ Cognitive trace attached to tick engine")
    return hook


# Standalone test function
def test_cognitive_trace():
    """Test the cognitive trace generator standalone"""
    generator = CognitiveTraceGenerator()
    
    # Simulate some ticks
    for i in range(20):
        tick_data = {
            'tick': 1000 + i,
            'zone': random.choice(['🟢 calm', '🟡 active', '🔴 surge']),
            'pulse_heat': random.uniform(0.2, 0.8),
            'entropy': random.uniform(0.1, 0.9),
            'scup': random.uniform(0.2, 0.8),
            'active_sigils': random.sample([
                'entropy_bloom', 'memory_cascade', 'semantic_drift',
                'pulse_resonance', 'schema_align', 'trace_echo'
            ], k=random.randint(2, 4)),
            'bloom_count': random.randint(0, 15),
            'schema_health': random.uniform(0.4, 1.0),
            'drift_magnitude': random.uniform(0.0, 0.5)
        }
        
        snapshot = generator.process_tick(tick_data)
        print(f"\n{snapshot.commentary}")
        
        generator.save_trace(snapshot)
    
    # Generate summary
    summary = generator.generate_summary_report()
    print(f"\n📊 Test Summary Generated: {summary['tick_range']}")


if __name__ == "__main__":
    test_cognitive_trace()