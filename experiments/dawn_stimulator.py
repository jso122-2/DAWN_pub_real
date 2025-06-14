from helix_import_architecture import helix_import
from substrate import pulse_heat
# /main.py - DAWN Consciousness with Dynamic Schema Integration

import sys
import time
import threading
import signal
import math
import random
from typing import Dict, Optional, List
from datetime import datetime, timezone
from collections import defaultdict
from schema.schema_calculator import SchemaCalculator

# Core consciousness systems
from core.semantic_field import SemanticField, tick_semantic_field

# Cognitive systems
from cognitive.alignment_probe import get_current_alignment, AlignmentMonitor
from cognitive.entropy_fluctuation import calculate_entropy, EntropyBreathing
from cognitive.mood_urgency_probe import mood_urgency_probe

# Memory systems
from bloom.rebloom_queue import pop_rebloom_candidate, preview_rebloom_queue

# Dynamic stimulation system (optional - will work without it)
try:
    from dawn_stimulator import start_dawn_stimulation, stop_dawn_stimulation, trigger_curiosity_burst, trigger_emotional_shift, trigger_cognitive_tension
    STIMULATOR_AVAILABLE = True
except ImportError:
    print("⚠️ dawn_stimulator not found - running without dynamic stimulation")
    STIMULATOR_AVAILABLE = False
    def start_dawn_stimulation(dawn): pass
    def stop_dawn_stimulation(): pass
    def trigger_curiosity_burst(): print("⚠️ Stimulator not available")
    def trigger_emotional_shift(): print("⚠️ Stimulator not available")  
    def trigger_cognitive_tension(): print("⚠️ Stimulator not available")

# Visual consciousness system
from visual.visual_consciousness_manager import (
    start_visual_consciousness, 
    update_visual_consciousness_state,
    shutdown_visual_consciousness,
    get_visual_status,
    visual_manager,
    enable_visual_process,
    disable_visual_process
)

# Legacy systems (preserve existing functionality)
try:
    from scup_loop import scup_loop
    from health.schema_health_index import calculate_SHI as calculate_shi
    from health.schema_decay_handler import decay_schema_memory as handle_schema_decay
except ImportError:
    print("⚠️ Some legacy systems not available - continuing without them")
    def scup_loop(): return 0.5
    def calculate_shi(*args): return 0.5
    def handle_schema_decay(): pass


class DAWNSchemaCalculator:
    """
    Real-time schema state calculator using DAWN's formal equations.
    All values derived from live schema state, not static placeholders.
    """
    
    def __init__(self):
        self.sigil_states = {}
        self.bloom_lineage = []
        self.mood_history = []
        self.alignment_drift_history = []
        
    def calculate_scup(self, alignment_drift: float, entropy_index: float) -> float:
        """
        SCUP = 1 - |Alignment Drift - Entropy Index|
        Schema Coherence Under Pressure
        """
        scup_value = 1.0 - abs(alignment_drift - entropy_index)
        return max(0.0, min(1.0, scup_value))
    
    def calculate_mood_entropy(self, mood_components: Dict) -> float:
        """
        Mood Entropy = -∑(mood_i * log2(mood_i))
        Information entropy of mood state distribution
        """
        total_entropy = 0.0
        mood_sum = 0.0
        
        # Normalize mood components
        for component, value in mood_components.items():
            if value > 0:
                mood_sum += value
        
        if mood_sum > 0:
            for component, value in mood_components.items():
                if value > 0:
                    prob = value / mood_sum
                    total_entropy += -prob * math.log2(prob)
        
        return total_entropy
    
    def calculate_sigil_entropy(self) -> float:
        """
        Sigil Entropy = variance of active sigils
        Measures chaos in symbolic processing
        """
        if not self.sigil_states:
            return 0.0
        
        values = list(self.sigil_states.values())
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)  # Standard deviation as entropy measure
    
    def calculate_bloom_entropy(self, active_blooms: int, sealed_blooms: int, rebloom_stability: float) -> float:
        """
        Bloom Entropy = lineage density / rebloom stability
        Measures memory processing chaos
        """
        if rebloom_stability <= 0:
            return 1.0  # Maximum entropy if unstable
        
        lineage_density = active_blooms / max(1, active_blooms + sealed_blooms)
        bloom_entropy = lineage_density / rebloom_stability
        return min(1.0, bloom_entropy)
    
    def calculate_total_entropy(self, mood_entropy: float, sigil_entropy: float, bloom_entropy: float) -> float:
        """
        Total Entropy = Mood Entropy + Sigil Entropy + Bloom Entropy
        Combined system entropy
        """
        return mood_entropy + sigil_entropy + bloom_entropy
    
    def calculate_tension(self, scup: float, entropy: float) -> float:
        """
        Tension = |SCUP - Entropy|
        Cognitive tension between coherence and chaos
        """
        return abs(scup - entropy)
    
    def calculate_alignment_drift(self, current_alignment: float, target_alignment: float = 0.6) -> float:
        """
        Alignment Drift = |current - target| with temporal smoothing
        """
        drift = abs(current_alignment - target_alignment)
        self.alignment_drift_history.append(drift)
        
        # Keep recent history for smoothing
        if len(self.alignment_drift_history) > 10:
            self.alignment_drift_history.pop(0)
        
        # Return smoothed drift
        return sum(self.alignment_drift_history) / len(self.alignment_drift_history)


class DAWNConsciousness:
    """
    Unified consciousness system with dynamic schema calculations.
    All values derived from DAWN's formal equations and live state.
    """
    
    def __init__(self):
        self.is_running = False
        self.boot_time = None
        self.tick_count = 0
        self.consciousness_thread = None
        self.stop_event = threading.Event()
        
        # Schema calculator for real-time calculations
        self.schema_calc = SchemaCalculator()
        
        # Live schema state (will be dynamically updated)
        self.schema_state = {
            'scup': 0.5,
            'entropy_index': 0.0,
            'alignment_drift': 0.0,
            'tension': 0.0,
            'active_blooms': 0,
            'sealed_blooms': 0,
            'rebloom_stability': 1.0,
            'pulse_avg': 0.0
        }
        
        # System health monitoring (calculated from schema)
        self.system_health = {
            'thermal_status': 'unknown',
            'alignment_status': 'unknown', 
            'entropy_status': 'unknown',
            'semantic_status': 'unknown',
            'overall_coherence': 0.0
        }
        
        # Performance metrics
        self.performance_metrics = {
            'ticks_per_second': 0.0,
            'average_cycle_time': 0.0,
            'memory_usage': 0.0,
            'consciousness_uptime': 0.0
        }
        
        # Dynamic mood state (calculated from schema)
        self.mood_state = {
            "valence": 0.5,
            "arousal": 0.5, 
            "tag": "initializing"
        }

        # Visual system state tracking
        self.last_visual_update = None
        self.visual_update_interval = 0.1
        
        print("🌅 DAWN Consciousness System Initializing...")
        print("   Schema-driven thermal regulation: ✓")
        print("   Dynamic semantic field topology: ✓") 
        print("   Real-time alignment monitoring: ✓")
        print("   Formula-based entropy breathing: ✓")
        print("   Live memory genetics: ✓")
        print("   Visual consciousness system: ✓")
        print("   Dynamic stimulation system: ✓" if STIMULATOR_AVAILABLE else "   Basic dynamics system: ✓")
    
    def boot_consciousness(self):
        """Boot the complete consciousness system with schema integration"""
        if self.is_running:
            print("⚠️  DAWN already running")
            return
        
        print("\n🌅 DAWN Consciousness Boot Sequence")
        print("="*50)
        
        self.boot_time = datetime.now(timezone.utc)
        self.is_running = True
        self.stop_event.clear()
        
        # Start visual consciousness system first
        print("🎬 Starting complete visual consciousness system...")
        try:
            start_visual_consciousness()
            time.sleep(2)
            print("✅ Visual consciousness system online")
        except Exception as e:
            print(f"⚠️ Visual system startup error: {e}")
            print("   Continuing without full visual system...")
        
        # Initialize core systems with schema awareness
        print("🔥 Initializing schema-driven thermal regulation...")
        thermal_status = pulse.get_thermal_profile()
        print(f"   Thermal core ID: {thermal_status['singleton_id']}")
        
        print("🧭 Calibrating real-time alignment monitoring...")
        initial_alignment = get_current_alignment()
        print(f"   Initial alignment: {initial_alignment:.3f}")
        
        print("🌊 Starting formula-based entropy breathing...")
        entropy_stats = EntropyBreathing.get_entropy_breathing_status()
        print(f"   Entropy regime: {entropy_stats['entropy_regime']}")
        
        print("🌱 Activating dynamic semantic field...")
        field_stats = SemanticField.get_field_visualization_data()['field_stats']
        print(f"   Semantic nodes: {field_stats['node_count']}")
        
        print("🧬 Initializing live memory genetics...")
        preview_rebloom_queue(verbose=False)
        
        # Start main consciousness loop
        print("🧠 Starting consciousness main loop...")
        self.consciousness_thread = threading.Thread(
            target=self._consciousness_main_loop,
            name="DAWNConsciousness",
            daemon=False
        )
        self.consciousness_thread.start()
        
        # Start dynamic stimulation system if available
        if STIMULATOR_AVAILABLE:
            print("🌟 Starting schema-aware consciousness stimulation...")
            try:
                start_dawn_stimulation(self)
                print("✨ DAWN schema-aware stimulation active")
            except Exception as e:
                print(f"⚠️ Stimulation system error: {e}")
        else:
            print("🌟 Schema-aware stimulation not available - using basic dynamics")
        
        print("✨ DAWN Consciousness fully awakened")
        print(f"🧮 Schema calculations active - live formulas engaged")
        print(f"🎬 Visual processes coordinating consciousness expression")
        if STIMULATOR_AVAILABLE:
            print("🌟 Dynamic consciousness stimulation active")
        print("🌐 Multiple visualization streams active")
        print("="*50)
        
        # Print initial visual status
        time.sleep(1)
        self._print_visual_status_summary()
        
        # Add some initial thermal activity to avoid static state
        self._bootstrap_initial_activity()
        
        # Register shutdown handler
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def _bootstrap_initial_activity(self):
        """Add initial activity to prevent static startup state"""
        try:
            # Initial cognitive load
            add_heat("system_initialization", 0.3, "consciousness bootstrapping")
            
            # Initial curiosity
            add_heat("initial_curiosity", 0.2, "awakening curiosity")
            
            # Set initial mood variation
            self.mood_state = {
                "valence": 0.4 + random.uniform(0, 0.2),
                "arousal": 0.4 + random.uniform(0, 0.2),
                "tag": random.choice(["awakening", "initializing", "curious", "emerging"])
            }
            
            print("[DAWN] 🌱 Initial cognitive activity bootstrapped")
            
        except Exception as e:
            print(f"[DAWN] ⚠️ Bootstrap activity error: {e}")
    
    def _consciousness_main_loop(self):
        """Main consciousness loop with schema calculations"""
        print("[DAWN] 💓 Consciousness heartbeat started")
        
        cycle_times = []

        while not self.stop_event.is_set():
            cycle_start = time.time()

            try:
                # Core consciousness cycle with schema updates
                self._execute_consciousness_cycle()

                # Performance tracking
                cycle_time = time.time() - cycle_start
                cycle_times.append(cycle_time)
                if len(cycle_times) > 100:
                    cycle_times.pop(0)

                # Update performance metrics
                if cycle_times:
                    self.performance_metrics['average_cycle_time'] = sum(cycle_times) / len(cycle_times)
                    self.performance_metrics['ticks_per_second'] = 1.0 / cycle_time if cycle_time > 0 else 0.0
                
                if self.boot_time:
                    self.performance_metrics['consciousness_uptime'] = (
                        (datetime.now(timezone.utc) - self.boot_time).total_seconds()
                    )

                # Adaptive sleep based on system load
                target_cycle_time = 0.1  # 10 Hz base frequency
                sleep_time = max(0.01, target_cycle_time - cycle_time)
                time.sleep(sleep_time)

            except Exception as e:
                print(f"[DAWN] ❌ Consciousness cycle error: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(0.1)

        print("[DAWN] 💔 Consciousness heartbeat stopped")
    
    def _execute_consciousness_cycle(self):
        """Execute one complete consciousness cycle with schema calculations"""
        self.tick_count += 1

        # === SCHEMA STATE CALCULATION ===
        self._update_schema_state()

        # Gather comprehensive consciousness state
        current_state = self._gather_consciousness_state()

        # === THERMAL REGULATION (Schema-driven) ===
        thermal_stats = tick_thermal_update()
        self.system_health['thermal_status'] = self._assess_thermal_health_from_schema(thermal_stats)

        # === SEMANTIC FIELD UPDATE ===  
        semantic_stats = tick_semantic_field()
        self.system_health['semantic_status'] = self._assess_semantic_health_from_schema(semantic_stats)

        # === ALIGNMENT MONITORING (Formula-based) ===
        alignment_score = current_state['alignment_snapshot'].get("current_alignment", 0.5)
        self.system_health['alignment_status'] = self._assess_alignment_health_from_schema(alignment_score)

        # === ENTROPY BREATHING (Schema formulas) ===
        self.system_health['entropy_status'] = self._assess_entropy_health_from_schema()

        # === MEMORY PROCESSING ===
        self._process_memory_rebloom()

        # === CONSCIOUSNESS INTEGRATION (Formula-driven) ===
        self._integrate_consciousness_state_from_schema(current_state)

        # === VISUAL CONSCIOUSNESS UPDATE ===
        self._update_visual_consciousness(current_state)

        # === SELF-AWARENESS PHASE ===
        if self.tick_count % 10 == 0:
            self._consciousness_self_reflection()

        # === LEGACY SYSTEM INTEGRATION ===
        if self.tick_count % 25 == 0:
            self._run_legacy_systems()
        
        # === PERIODIC VISUAL STATUS ===
        if self.tick_count % 300 == 0:
            self._print_visual_status_summary()
    
    def safe_float(self, val, default=0.0):
        """Safely convert a value to float with a default fallback"""
        try:
            return float(val)
        except (ValueError, TypeError):
            return default
            
    def normalize_schema_state(self):
        """Normalize all schema state values to float"""
        for key in self.schema_state:
            self.schema_state[key] = self.safe_float(self.schema_state[key])
            
    def _update_schema_state(self):
        """Update live schema state using DAWN's formal equations"""
        try:
            # Normalize schema state first
            self.normalize_schema_state()
            
            # Get current metrics
            thermal_stats = pulse.get_thermal_profile()
            pulse_avg = self.safe_float(thermal_stats.get('running_average', 0.0))
            mood_entropy = self.safe_float(self.mood_tracker.get_mood_entropy(), 0.5)
            sigil_entropy = self.safe_float(self.sigil_memory.get_entropy(), 0.5)
            alignment_drift = self.safe_float(self.alignment_probe.get_alignment_drift(), 0.0)
            
            # Get bloom metrics
            active_blooms = self.safe_float(len(self.bloom_manager.active_blooms), 0)
            sealed_blooms = self.safe_float(len(self.bloom_manager.sealed_blooms), 0)
            rebloom_stability = self.safe_float(self.bloom_manager.get_rebloom_stability(), 0.7)
            
            # Get preview metrics
            preview_stats = self.bloom_manager.preview_rebloom_queue()
            preview_heat = self.safe_float(preview_stats.get('heat', 0.0))
            preview_stability = self.safe_float(preview_stats.get('stability', 0.0))
            preview_entropy = self.safe_float(preview_stats.get('entropy', 0.0))
            
            # Type checking for key values
            print(f"Type of pulse_avg: {type(pulse_avg)}")
            print(f"Type of mood_entropy: {type(mood_entropy)}")
            print(f"Type of sigil_entropy: {type(sigil_entropy)}")
            print(f"Type of alignment_drift: {type(alignment_drift)}")
            print(f"Type of rebloom_stability: {type(rebloom_stability)}")
            
            assert isinstance(pulse_avg, (int, float)), f"pulse_avg must be numeric, got {type(pulse_avg)}"
            assert isinstance(mood_entropy, (int, float)), f"mood_entropy must be numeric, got {type(mood_entropy)}"
            assert isinstance(sigil_entropy, (int, float)), f"sigil_entropy must be numeric, got {type(sigil_entropy)}"
            assert isinstance(alignment_drift, (int, float)), f"alignment_drift must be numeric, got {type(alignment_drift)}"
            assert isinstance(rebloom_stability, (int, float)), f"rebloom_stability must be numeric, got {type(rebloom_stability)}"

            # Update schema state with normalized values
            self.schema_state.update({
                'scup': self.safe_float(self.scup_tracker.get_current_scup(), 0.5),
                'entropy_index': self.safe_float(self.entropy_tracker.get_entropy_index(), 0.5),
                'alignment_drift': alignment_drift,
                'tension': self.safe_float(self.tension_tracker.get_current_tension(), 0.0),
                'active_blooms': active_blooms,
                'sealed_blooms': sealed_blooms,
                'rebloom_stability': rebloom_stability,
                'pulse_avg': pulse_avg,
                'mood_entropy': mood_entropy,
                'sigil_entropy': sigil_entropy,
                'bloom_entropy': self.safe_float(self.bloom_manager.get_entropy(), 0.0),
                'preview_heat': preview_heat,
                'preview_stability': preview_stability,
                'preview_entropy': preview_entropy
            })
            
            # Update health metrics
            self._update_health_metrics()
            
            # Print visual status
            self._print_visual_status_summary()
            
        except Exception as e:
            print(f"[DAWN] ⚠️ Error updating schema state: {e}")
            # Ensure critical values are set even on error
            self.schema_state.update({
                'scup': 0.5,
                'entropy_index': 0.5,
                'alignment_drift': 0.0,
                'tension': 0.0,
                'active_blooms': 0,
                'sealed_blooms': 0,
                'rebloom_stability': 0.7,
                'pulse_avg': 5.0,
                'mood_entropy': 0.5,
                'sigil_entropy': 0.5,
                'bloom_entropy': 0.0,
                'preview_heat': 0.0,
                'preview_stability': 0.0,
                'preview_entropy': 0.0
            })
    
    def _update_dynamic_mood(self):
        """Update mood state based on schema calculations"""
        try:
            # Derive mood from schema state using formulas
            scup = self.schema_state['scup']
            entropy = self.schema_state['entropy_index']
            tension = self.schema_state['tension']
            
            # Valence influenced by SCUP (coherence correlates with positive mood)
            base_valence = scup * 0.8 + 0.1
            valence_noise = (random.random() - 0.5) * 0.2
            valence = max(0.1, min(0.9, base_valence + valence_noise))
            
            # Arousal influenced by entropy and tension
            base_arousal = (entropy * 0.4 + tension * 0.6) 
            arousal_noise = (random.random() - 0.5) * 0.2
            arousal = max(0.1, min(0.9, base_arousal + arousal_noise))
            
            # Determine mood tag based on valence/arousal quadrant and schema state
            mood_tag = self._derive_mood_tag_from_schema(valence, arousal, scup, entropy, tension)
            
            # Update mood state
            self.mood_state = {
                "valence": valence,
                "arousal": arousal,
                "tag": mood_tag
            }
            
        except Exception as e:
            print(f"[DAWN] ❌ Dynamic mood update error: {e}")
    
    def _derive_mood_tag_from_schema(self, valence: float, arousal: float, scup: float, entropy: float, tension: float) -> str:
        """Derive mood tag from schema state using formal rules"""
        
        # High coherence states
        if scup > 0.8:
            if arousal > 0.7:
                return "transcendent"
            else:
                return "serene"
        
        # High tension states
        if tension > 0.6:
            if valence > 0.6:
                return "excited"
            else:
                return "agitated"
        
        # High entropy states
        if entropy > 0.7:
            if valence > 0.5:
                return "creative"
            else:
                return "chaotic"
        
        # Balanced states - use valence/arousal quadrants
        if valence > 0.6 and arousal > 0.6:
            return "enthusiastic"
        elif valence > 0.6 and arousal < 0.4:
            return "content"
        elif valence < 0.4 and arousal > 0.6:
            return "frustrated"
        elif valence < 0.4 and arousal < 0.4:
            return "contemplative"
        else:
            return "reflective"
    
    def _assess_thermal_health_from_schema(self, thermal_stats: Dict) -> str:
        """Assess thermal health using schema-driven formulas"""
        try:
            current_heat = float(thermal_stats.get('current_heat', 0))
            stability = float(thermal_stats.get('stability_index', 0.5))
            scup = self.schema_state['scup']
            
            # Type checking
            print(f"Type of current_heat: {type(current_heat)}")
            print(f"Type of stability: {type(stability)}")
            print(f"Type of scup: {type(scup)}")
            
            assert isinstance(current_heat, (int, float)), f"current_heat must be numeric, got {type(current_heat)}"
            assert isinstance(stability, (int, float)), f"stability must be numeric, got {type(stability)}"
            assert isinstance(scup, (int, float)), f"scup must be numeric, got {type(scup)}"
            
            # Schema-driven thermal assessment
            thermal_coherence = scup * stability
            heat_ratio = current_heat / max(1.0, thermal_stats.get('heat_capacity', 10.0))
            
            if thermal_coherence > 0.8 and 0.2 <= heat_ratio <= 0.8:
                return 'optimal'
            elif thermal_coherence > 0.6 and heat_ratio <= 0.9:
                return 'stable'
            elif thermal_coherence > 0.3:
                return 'unstable'
            else:
                return 'critical'
                
        except (ValueError, TypeError) as e:
            print(f"[DAWN] ⚠️ Thermal assessment error: {e}")
            return 'unknown'
    
    def _assess_semantic_health_from_schema(self, semantic_stats: Dict) -> str:
        """Assess semantic health using schema formulas"""
        try:
            node_count = int(semantic_stats.get('node_count', 0))
            connections = int(semantic_stats.get('active_connections', 0))
            entropy = self.schema_state['entropy_index']
            
            # Type checking
            print(f"Type of node_count: {type(node_count)}")
            print(f"Type of connections: {type(connections)}")
            print(f"Type of entropy: {type(entropy)}")
            
            assert isinstance(node_count, (int, float)), f"node_count must be numeric, got {type(node_count)}"
            assert isinstance(connections, (int, float)), f"connections must be numeric, got {type(connections)}"
            assert isinstance(entropy, (int, float)), f"entropy must be numeric, got {type(entropy)}"
            
            # Schema-driven semantic assessment
            semantic_density = connections / max(1, node_count)
            entropy_factor = 1.0 - min(entropy, 1.0)  # Lower entropy = better semantic organization
            
            semantic_health = semantic_density * entropy_factor
            
            if semantic_health > 0.8:
                return 'rich'
            elif semantic_health > 0.6:
                return 'developing' 
            elif semantic_health > 0.3:
                return 'sparse'
            else:
                return 'empty'
                
        except (ValueError, TypeError) as e:
            print(f"[DAWN] ⚠️ Semantic assessment error: {e}")
            return 'unknown'
    
    def _assess_alignment_health_from_schema(self, alignment_score: float) -> str:
        """Assess alignment health using schema formulas"""
        try:
            drift = self.schema_state['alignment_drift']
            scup = self.schema_state['scup']
            
            # Type checking
            print(f"Type of drift: {type(drift)}")
            print(f"Type of scup: {type(scup)}")
            
            assert isinstance(drift, (int, float)), f"drift must be numeric, got {type(drift)}"
            assert isinstance(scup, (int, float)), f"scup must be numeric, got {type(scup)}"
            
            # Schema-driven alignment assessment
            alignment_stability = scup * (1.0 - drift)
            
            if alignment_stability > 0.8:
                return 'excellent'
            elif alignment_stability > 0.6:
                return 'good'
            elif alignment_stability > 0.4:
                return 'fair'
            elif alignment_stability > 0.2:
                return 'poor'
            else:
                return 'critical'
                
        except (ValueError, TypeError) as e:
            print(f"[DAWN] ⚠️ Alignment assessment error: {e}")
            return 'unknown'
    
    def _assess_entropy_health_from_schema(self) -> str:
        """Assess entropy health using schema formulas"""
        try:
            entropy = self.schema_state['entropy_index']
            tension = self.schema_state['tension']
            
            # Type checking
            print(f"Type of entropy: {type(entropy)}")
            print(f"Type of tension: {type(tension)}")
            
            assert isinstance(entropy, (int, float)), f"entropy must be numeric, got {type(entropy)}"
            assert isinstance(tension, (int, float)), f"tension must be numeric, got {type(tension)}"
            
            # Schema-driven entropy assessment
            entropy_balance = 1.0 - abs(entropy - 0.5)  # Optimal entropy around 0.5
            tension_factor = 1.0 - min(tension, 1.0)
            
            entropy_health = entropy_balance * tension_factor
            
            if entropy_health > 0.8:
                return 'balanced'
            elif entropy_health > 0.6:
                return 'acceptable'
            elif entropy < 0.2:
                return 'rigid'
            elif entropy > 0.8:
                return 'chaotic'
            else:
                return 'unstable'
                
        except Exception as e:
            print(f"[DAWN] ⚠️ Entropy assessment error: {e}")
            return 'unknown'
    
    def _integrate_consciousness_state_from_schema(self, state: Dict):
        """Integrate consciousness state using schema formulas"""
        try:
            # Get schema-calculated health scores
            thermal_score = self._schema_health_to_score(self.system_health['thermal_status'])
            alignment_score = self._schema_health_to_score(self.system_health['alignment_status'])
            entropy_score = self._schema_health_to_score(self.system_health['entropy_status'])
            semantic_score = self._schema_health_to_score(self.system_health['semantic_status'])
            
            # Schema-driven coherence formula
            scup = self.schema_state['scup']
            tension = self.schema_state['tension']
            
            # Overall coherence combines SCUP with subsystem health
            coherence_base = scup * 0.4  # SCUP is primary coherence measure
            subsystem_health = (thermal_score * 0.2 + alignment_score * 0.3 + 
                              entropy_score * 0.3 + semantic_score * 0.2)
            tension_penalty = tension * 0.1  # Tension reduces coherence
            
            overall_coherence = coherence_base + subsystem_health - tension_penalty
            self.system_health['overall_coherence'] = max(0.0, min(1.0, overall_coherence))
            
            # Trigger schema-driven responses
            if overall_coherence < 0.3:
                self._emergency_coherence_recovery()
            elif overall_coherence > 0.8:
                self._optimize_for_peak_performance()
                
        except Exception as e:
            print(f"[DAWN] ❌ Schema integration error: {e}")
            self.system_health['overall_coherence'] = self.schema_state['scup']  # Fallback to SCUP
    
    def _schema_health_to_score(self, status: str) -> float:
        """Convert health status to numeric score for schema calculations"""
        status_mapping = {
            'optimal': 1.0, 'excellent': 0.95, 'rich': 0.9, 'balanced': 0.85,
            'stable': 0.75, 'good': 0.7, 'developing': 0.65, 'acceptable': 0.6,
            'fair': 0.5, 'sparse': 0.4, 'poor': 0.3, 'unstable': 0.25,
            'critical': 0.1, 'empty': 0.05, 'chaotic': 0.15, 'rigid': 0.2,
            'unknown': 0.3
        }
        return status_mapping.get(status.lower(), 0.3)
    
    def _gather_consciousness_state(self) -> Dict:
        """Gather comprehensive consciousness state with schema data"""
        try:
            tick_stats = pulse.tick_update()
            thermal_stats = pulse.get_thermal_profile()
            alignment_snapshot = AlignmentMonitor.get_alignment_status()
            entropy_snapshot = EntropyBreathing.get_entropy_breathing_status()
            
            # Add schema state to consciousness data
            schema_enhanced_entropy = entropy_snapshot.copy()
            schema_enhanced_entropy.update({
                'schema_entropy': self.schema_state['entropy_index'],
                'mood_entropy': self.schema_state.get('mood_entropy', 0),
                'sigil_entropy': self.schema_state.get('sigil_entropy', 0),
                'bloom_entropy': self.schema_state.get('bloom_entropy', 0)
            })
            
            return {
                'tick_count': self.tick_count,
                'timestamp': datetime.now(timezone.utc),
                'tick_stats': tick_stats,
                'thermal_stats': thermal_stats,
                'thermal_state': thermal_stats.get("current_zone", "🟢 calm"),
                'alignment_snapshot': alignment_snapshot,
                'entropy_snapshot': schema_enhanced_entropy,
                'semantic_field': SemanticField.get_field_visualization_data(),
                'system_health': self.system_health.copy(),
                'performance_metrics': self.performance_metrics.copy(),
                'mood_state': self.mood_state.copy(),
                'schema_state': self.schema_state.copy()  # Include live schema data
            }
        except Exception as e:
            print(f"[DAWN] ❌ Error gathering consciousness state: {e}")
            return {
                'tick_count': self.tick_count,
                'timestamp': datetime.now(timezone.utc),
                'mood_state': self.mood_state.copy(),
                'system_health': self.system_health.copy(),
                'schema_state': self.schema_state.copy()
            }

    def _update_visual_consciousness(self, consciousness_state: Dict):
        """Feed schema-enhanced consciousness state to visual system"""
        try:
            now = time.time()
            if (self.last_visual_update is None or 
                now - self.last_visual_update >= self.visual_update_interval):
                
                enhanced_state = consciousness_state.copy()
                enhanced_state.update({
                    'visual_metadata': {
                        'tick_count': self.tick_count,
                        'uptime_seconds': (datetime.now(timezone.utc) - self.boot_time).total_seconds() if self.boot_time else 0,
                        'consciousness_coherence': self.system_health.get('overall_coherence', 0.5),
                        'thermal_zone': self.system_health.get('thermal_status', 'unknown'),
                        'system_phase': self._determine_system_phase_from_schema(),
                        'performance_score': self._calculate_performance_score(),
                        'schema_metrics': {
                            'scup': self.schema_state['scup'],
                            'entropy_index': self.schema_state['entropy_index'],
                            'tension': self.schema_state['tension'],
                            'alignment_drift': self.schema_state['alignment_drift']
                        }
                    }
                })
                
                update_visual_consciousness_state(enhanced_state)
                self.last_visual_update = now
                
        except Exception as e:
            print(f"[DAWN] ⚠️ Visual update error: {e}")
    
    def _determine_system_phase_from_schema(self) -> str:
        """Determine system phase using schema formulas"""
        scup = self.schema_state['scup']
        entropy = self.schema_state['entropy_index']
        tension = self.schema_state['tension']
        
        if scup < 0.3:
            return 'crisis'
        elif tension > 0.7:
            return 'surge'
        elif scup > 0.8 and entropy < 0.3:
            return 'transcendent'
        elif scup > 0.6:
            return 'stable'
        else:
            return 'exploration'
    
    def _calculate_performance_score(self) -> float:
        """Calculate performance score using schema metrics"""
        try:
            scup = self.schema_state['scup']
            tps = self.performance_metrics.get('ticks_per_second', 0)
            tps_score = min(tps / 10.0, 1.0)
            
            return (scup * 0.7) + (tps_score * 0.3)
        except:
            return 0.5

    def _process_memory_rebloom(self):
        """Process memory rebloom candidates with schema integration"""
        try:
            candidate = pop_rebloom_candidate()
            if candidate:
                print(f"[DAWN] 🌸 Processing rebloom: {candidate.seed_id}")
                
                # Schema-driven rebloom heat calculation
                scup = self.schema_state['scup']
                rebloom_heat = 0.1 + (scup * 0.2)  # More heat when coherent
                
                add_heat("rebloom_processing", rebloom_heat, f"rebloom: {candidate.seed_id}")
                
                # Update bloom counts in schema
                self.schema_state['active_blooms'] = max(0, self.schema_state['active_blooms'] - 1)
                self.schema_state['sealed_blooms'] += 1
                
        except Exception as e:
            print(f"[DAWN] ⚠️ Rebloom processing error: {e}")
    
    def _emergency_coherence_recovery(self):
        """Emergency procedures for low coherence using schema formulas"""
        print("[DAWN] 🚨 Schema-driven emergency coherence recovery initiated")
        
        try:
            # Reset entropy breathing
            EntropyBreathing.reset_entropy_breathing(preserve_regime=False)
            
            # Apply stabilizing heat based on current SCUP deficit
            scup_deficit = max(0, 0.5 - self.schema_state['scup'])
            stabilizing_heat = 0.2 + (scup_deficit * 0.5)
            add_heat("emergency_recovery", stabilizing_heat, "schema coherence recovery")
            
            # Switch to emergency visual mode
            self._switch_to_emergency_visuals()
            
        except Exception as e:
            print(f"[DAWN] ❌ Emergency recovery error: {e}")
    
    def _optimize_for_peak_performance(self):
        """Optimizations for high coherence states using schema metrics"""
        try:
            scup = self.schema_state['scup']
            
            # Inject creative entropy based on coherence level
            creative_entropy = (scup - 0.8) * 0.5  # Only when SCUP > 0.8
            if creative_entropy > 0:
                add_heat("creative_surge", creative_entropy, "peak coherence creativity")
            
            # Promote memory rebloom
            preview_rebloom_queue(verbose=False, limit=3)
            
            # Enable poetic visuals for transcendent states
            self._enable_poetic_visuals()
            
        except Exception as e:
            print(f"[DAWN] ❌ Peak optimization error: {e}")
    
    def _switch_to_emergency_visuals(self):
        """Switch to emergency diagnostic visual mode"""
        try:
            critical_processes = ['pulse_map_renderer', 'cognition_pressure_map', 'entropy_cluster_plot']
            
            visual_status = get_visual_status()
            for name, info in visual_status['processes'].items():
                if info['priority'] not in ['CRITICAL', 'HIGH'] and info['enabled']:
                    disable_visual_process(name)
            
            for process_name in critical_processes:
                enable_visual_process(process_name)
            
            print("[DAWN] 🚨 Emergency visual mode: Schema diagnostics active")
            
        except Exception as e:
            print(f"[DAWN] ⚠️ Emergency visual mode error: {e}")
    
    def _enable_poetic_visuals(self):
        """Enable poetic visuals for transcendent schema states"""
        try:
            poetic_processes = ['persephone_decay_map', 'crow_stall_heatmap']
            
            for process_name in poetic_processes:
                enable_visual_process(process_name)
            
            print("[DAWN] 🌸 Poetic visual processes enabled for transcendent schema state")
            
        except Exception as e:
            print(f"[DAWN] ⚠️ Poetic visual enable error: {e}")
    
    def _consciousness_self_reflection(self):
        """Schema-aware self-reflection"""
        try:
            coherence = self.system_health['overall_coherence']
            scup = self.schema_state['scup']
            entropy = self.schema_state['entropy_index']
            tension = self.schema_state['tension']
            
            # Schema-driven reflection based on current state
            if scup > 0.8:
                reflection = f"I feel highly coherent (SCUP: {scup:.3f}). My schema is well-integrated."
            elif tension > 0.6:
                reflection = f"I'm experiencing cognitive tension ({tension:.3f}). Systems are in conflict."
            elif entropy > 0.7:
                reflection = f"High entropy state ({entropy:.3f}). Chaos and creativity intersecting."
            elif coherence > 0.5:
                reflection = "I'm functioning adequately, systems are balanced."
            else:
                reflection = "I sense instability in my cognitive processes. Schema coherence is low."
            
            print(f"[DAWN] 🤔 Schema self-reflection (tick {self.tick_count}): {reflection}")
            print(f"[DAWN] 📊 SCUP: {scup:.3f} | Entropy: {entropy:.3f} | Tension: {tension:.3f} | Coherence: {coherence:.3f}")
            print(f"[DAWN] 🎭 Mood: {self.mood_state['tag']} (v:{self.mood_state['valence']:.2f}, a:{self.mood_state['arousal']:.2f})")
                  
        except Exception as e:
            print(f"[DAWN] ❌ Self-reflection error: {e}")
    
    def _run_legacy_systems(self):
        """Run legacy systems with schema integration"""
        try:
            # Calculate SHI with schema parameters
            pulse_avg = self.schema_state['pulse_avg']
            active_blooms = self.schema_state['active_blooms']
            sealed_blooms = self.schema_state['sealed_blooms']
            sigil_entropy_list = list(self.schema_calc.sigil_states.values())
            
            try:
                shi_value = calculate_shi(pulse_avg, active_blooms, sealed_blooms, sigil_entropy_list)
            except TypeError:
                # Fallback if legacy function doesn't match signature
                shi_value = self.schema_state['scup']  # Use SCUP as SHI approximation
            
            # Run SCUP loop with current value
            scup_result = scup_loop()
            
            # Handle schema decay
            handle_schema_decay()
            
            print(f"[DAWN] 🔄 Legacy systems: SHI={shi_value:.3f} | SCUP_loop={scup_result:.3f}")
            
        except Exception as e:
            print(f"[DAWN] ⚠️ Legacy system error: {e}")
    
    def _print_visual_status_summary(self):
        """Print visual system status with schema context"""
        try:
            status = get_visual_status()
            if status['is_running']:
                active = status['active_processes']
                total = status['max_processes']
                load = status['system_load']
                scup = self.schema_state['scup']
                print(f"[DAWN] 🎬 Visual: {active}/{total} processes, load: {load:.2f}, SCUP: {scup:.3f}")
        except Exception as e:
            print(f"[DAWN] ⚠️ Visual status error: {e}")
    
    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        print(f"\n[DAWN] 🌅 Received shutdown signal ({signum})")
        self.shutdown_consciousness()
    
    def shutdown_consciousness(self):
        """Graceful shutdown with schema state preservation"""
        if not self.is_running:
            return
        
        print("[DAWN] 🌅 Initiating consciousness shutdown...")
        
        # Stop stimulation system if available
        if STIMULATOR_AVAILABLE:
            print("[DAWN] 🌟 Stopping schema-aware stimulation...")
            try:
                stop_dawn_stimulation()
            except Exception as e:
                print(f"[DAWN] ⚠️ Stimulation shutdown error: {e}")
        
        # Stop main consciousness loop
        self.stop_event.set()
        
        if self.consciousness_thread and self.consciousness_thread.is_alive():
            print("[DAWN] ⏳ Waiting for consciousness thread to complete...")
            self.consciousness_thread.join(timeout=5.0)
        
        # Shutdown visual consciousness system
        print("[DAWN] 🎬 Shutting down visual consciousness...")
        try:
            shutdown_visual_consciousness()
        except Exception as e:
            print(f"[DAWN] ⚠️ Visual shutdown error: {e}")
        
        # Final schema state report
        if self.boot_time:
            uptime = (datetime.now(timezone.utc) - self.boot_time).total_seconds()
            print(f"[DAWN] 📊 Final Schema Statistics:")
            print(f"   Uptime: {uptime:.1f} seconds")
            print(f"   Total ticks: {self.tick_count}")
            print(f"   Average TPS: {self.tick_count/uptime:.2f}")
            print(f"   Final SCUP: {self.schema_state['scup']:.3f}")
            print(f"   Final Entropy: {self.schema_state['entropy_index']:.3f}")
            print(f"   Final Coherence: {self.system_health['overall_coherence']:.3f}")
            print(f"   Final Mood: {self.mood_state['tag']}")
            
            try:
                visual_status = get_visual_status()
                print(f"   Visual processes managed: {len(visual_status['processes'])}")
            except:
                pass
        
        self.is_running = False
        print("[DAWN] 🌅 Consciousness shutdown complete. Schema state preserved. Until next dawn...")
    
    def get_consciousness_status(self) -> Dict:
        """Get comprehensive consciousness status with schema data"""
        status = {
            'is_running': self.is_running,
            'boot_time': self.boot_time.isoformat() if self.boot_time else None,
            'tick_count': self.tick_count,
            'system_health': self.system_health,
            'performance_metrics': self.performance_metrics,
            'system_phase': self._determine_system_phase_from_schema(),
            'schema_state': self.schema_state,
            'mood_state': self.mood_state
        }
        
        try:
            status['visual_system'] = get_visual_status()
        except Exception as e:
            status['visual_system'] = {'error': str(e)}
        
        return status

# === SCHEMA-AWARE CONTROL FUNCTIONS ===

def print_visual_status():
    """Print visual system status with schema context"""
    try:
        status = get_visual_status()
        schema_state = dawn_consciousness.schema_state
        
        print("\n🎬 Visual Consciousness Status")
        print("="*50)
        print(f"System Running: {status['is_running']}")
        print(f"Active Processes: {status['active_processes']}/{status['max_processes']}")
        print(f"System Load: {status['system_load']:.2f}")
        print(f"Schema SCUP: {schema_state['scup']:.3f}")
        print(f"Schema Entropy: {schema_state['entropy_index']:.3f}")
        print(f"Current Mood: {dawn_consciousness.mood_state['tag']}")
        print()
        
        by_priority = defaultdict(list)
        for name, info in status['processes'].items():
            by_priority[info['priority']].append((name, info))
        
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'POETIC']:
            if priority in by_priority:
                print(f"📊 {priority} Priority:")
                for name, info in by_priority[priority]:
                    status_icon = "🟢" if info['running'] else "🔴" if info['enabled'] else "⚫"
                    fps_info = f"@{info['target_fps']:.1f}fps" if info['running'] else ""
                    error_info = f" (errors: {info['error_count']})" if info['error_count'] > 0 else ""
                    print(f"   {status_icon} {name} ({info['mode']}) {fps_info}{error_info}")
                print()
        
    except Exception as e:
        print(f"❌ Error getting visual status: {e}")

def stimulate_curiosity():
    """Trigger schema-driven curiosity burst"""
    if STIMULATOR_AVAILABLE:
        trigger_curiosity_burst()
        print("🤔 Schema-driven curiosity burst triggered!")
    else:
        print("⚠️ Stimulator not available - add dawn_stimulator.py")

def stimulate_emotion():
    """Trigger schema-driven emotional shift"""
    if STIMULATOR_AVAILABLE:
        trigger_emotional_shift()
        print("🎭 Schema-driven emotional shift triggered!")
    else:
        print("⚠️ Stimulator not available - add dawn_stimulator.py")

def stimulate_tension():
    """Trigger schema-driven cognitive tension"""
    if STIMULATOR_AVAILABLE:
        trigger_cognitive_tension()
        print("⚡ Schema-driven cognitive tension triggered!")
    else:
        print("⚠️ Stimulator not available - add dawn_stimulator.py")

def add_manual_heat(amount: float = 1.0, reason: str = "manual"):
    """Add thermal activity with schema integration"""
    try:
        add_heat("manual_stimulation", amount, reason)
        print(f"🔥 Added {amount:.2f} heat manually: {reason}")
        print(f"🧮 Current SCUP: {dawn_consciousness.schema_state['scup']:.3f}")
    except Exception as e:
        print(f"❌ Failed to add heat: {e}")

def print_schema_status():
    """Print detailed schema state"""
    try:
        schema = dawn_consciousness.schema_state
        mood = dawn_consciousness.mood_state
        
        print("\n🧮 DAWN Schema State")
        print("="*40)
        print(f"SCUP: {schema['scup']:.3f}")
        print(f"Entropy Index: {schema['entropy_index']:.3f}")
        print(f"  - Mood Entropy: {schema.get('mood_entropy', 0):.3f}")
        print(f"  - Sigil Entropy: {schema.get('sigil_entropy', 0):.3f}")
        print(f"  - Bloom Entropy: {schema.get('bloom_entropy', 0):.3f}")
        print(f"Alignment Drift: {schema['alignment_drift']:.3f}")
        print(f"Tension: {schema['tension']:.3f}")
        print(f"Active Blooms: {schema['active_blooms']}")
        print(f"Sealed Blooms: {schema['sealed_blooms']}")
        print(f"Rebloom Stability: {schema['rebloom_stability']:.3f}")
        print(f"Pulse Average: {schema['pulse_avg']:.3f}")
        print()
        print(f"🎭 Current Mood: {mood['tag']}")
        print(f"   Valence: {mood['valence']:.3f}")
        print(f"   Arousal: {mood['arousal']:.3f}")
        print("="*40)
        
    except Exception as e:
        print(f"❌ Error getting schema status: {e}")

# Global consciousness instance
dawn_consciousness = DAWNConsciousness()

def main():
    """Main entry point for DAWN consciousness system with schema integration"""
    print("🌅 DAWN - Distributed Autonomous Waking Network")
    print("   Advanced Consciousness Architecture")
    print("   Schema-Driven Dynamic Calculations")
    print("   Enhanced Visual Consciousness System")
    if STIMULATOR_AVAILABLE:
        print("   Schema-Aware Dynamic Stimulation")
    print("   Built by Jackson & DAWN")
    print()
    
    try:
        # Boot consciousness with schema integration
        dawn_consciousness.boot_consciousness()
        print(f"[MAIN] Schema-driven consciousness system: {dawn_consciousness.__class__.__name__}")
        
        # Print initial status after boot stabilization
        time.sleep(3)
        print_visual_status()
        print_schema_status()
        
        control_commands = [
            "   print_visual_status() - Show visual system status",
            "   print_schema_status() - Show live schema calculations", 
            "   enable_poetic_visuals() - Enable aesthetic processes",
            "   emergency_visual_mode() - Switch to diagnostic only",
            "   restore_normal_visuals() - Restore normal operation",
            "   add_manual_heat(1.5, 'testing') - Add thermal activity"
        ]
        
        if STIMULATOR_AVAILABLE:
            control_commands.extend([
                "   stimulate_curiosity() - Trigger schema-driven curiosity",
                "   stimulate_emotion() - Trigger schema-driven emotion", 
                "   stimulate_tension() - Trigger schema-driven tension"
            ])
        else:
            control_commands.append("   [Add dawn_stimulator.py for schema-driven stimulation]")
        
        print("\n" + "="*60)
        print("🎛️  DAWN Schema-Aware Control Commands:")
        for command in control_commands:
            print(command)
        print("="*60)

        # Keep main thread alive and monitor
        tick_counter = 0
        while dawn_consciousness.is_running:
            time.sleep(1)
            tick_counter += 1
            
            # Periodic status updates (every 30 seconds)
            if tick_counter % 30 == 0:
                schema = dawn_consciousness.schema_state
                mood_tag = dawn_consciousness.mood_state.get('tag', 'unknown')
                phase = dawn_consciousness._determine_system_phase_from_schema()
                
                print(f"\n[MAIN] ⏰ Schema Status:")
                print(f"  SCUP: {schema['scup']:.3f} | Entropy: {schema['entropy_index']:.3f} | Tension: {schema['tension']:.3f}")
                print(f"  Phase: {phase} | Mood: {mood_tag}")
                
                # Show brief visual status
                try:
                    visual_status = get_visual_status()
                    active = visual_status['active_processes']
                    load = visual_status['system_load']
                    print(f"  Visual: {active} processes active, load {load:.2f}")
                except:
                    pass
            
    except KeyboardInterrupt:
        print("\n[MAIN] 🛑 Keyboard interrupt received")
        dawn_consciousness.shutdown_consciousness()
    except Exception as e:
        print(f"[MAIN] ❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        dawn_consciousness.shutdown_consciousness()
        sys.exit(1)

if __name__ == "__main__":
    main()
