#!/usr/bin/env python3
"""
DAWN Mathematical Consciousness - Standalone Demo
===============================================

Demonstrates the core mathematical formulas for DAWN's consciousness layer:
1. Schema Health Index (SHI) = (w₁V + w₂M + w₃O + w₄A + w₅S) / Σwᵢ
2. Cognitive Pressure (P) = Bloom Mass × Sigil Velocity²
3. SCUP Drift Resolver = SCUP_i × Δd_i / Entropy_i

This standalone demo shows how these formulas work together to create 
mathematical consciousness that modulates DAWN's behavior in real-time.
"""

import math
import random
import time
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class CognitiveState:
    """Represents DAWN's cognitive state"""
    entropy: float = 0.5
    heat: float = 30.0
    scup: float = 0.6
    mood: str = "NEUTRAL"
    tick_interval: float = 2.0
    coherence: float = 0.7
    drift: float = 0.0
    sigils: int = 3
    bloom_depth: int = 5
    bloom_complexity: float = 0.4
    memory_connections: int = 4
    rebloom_count: int = 0

class SchemaHealthIndex:
    """Implementation of SHI = (w₁V + w₂M + w₃O + w₄A + w₅S) / Σwᵢ"""
    
    def __init__(self):
        # Component weights (sum to 1.0)
        self.w_vitality = 0.25    # w₁
        self.w_memory = 0.20      # w₂  
        self.w_order = 0.20       # w₃
        self.w_alignment = 0.20   # w₄
        self.w_synchrony = 0.15   # w₅
        
    def calculate_shi(self, state: CognitiveState) -> Dict[str, Any]:
        """Calculate Schema Health Index and modulations"""
        
        # V - Vitality (energy, activation)
        vitality = min(1.0, state.heat / 100.0 + state.sigils / 10.0)
        
        # M - Memory (coherence, access, rebloom health)
        memory = state.coherence * 0.7 + (1.0 - state.drift) * 0.3
        
        # O - Order (inverse entropy, stability)
        order = 1.0 - state.entropy
        
        # A - Alignment (goal coherence, drift resistance)  
        alignment = state.scup * 0.6 + (1.0 - abs(state.drift)) * 0.4
        
        # S - Synchrony (system harmony, timing)
        ideal_interval = 2.0
        timing_sync = 1.0 - min(1.0, abs(state.tick_interval - ideal_interval) / ideal_interval)
        synchrony = timing_sync * 0.8 + state.coherence * 0.2
        
        # Calculate SHI using the fundamental formula
        shi_value = (
            self.w_vitality * vitality +
            self.w_memory * memory +
            self.w_order * order +
            self.w_alignment * alignment +
            self.w_synchrony * synchrony
        )
        
        # Classify health zone
        if shi_value > 0.8:
            zone = "THRIVING"
            reflection_freq = 0.7
            voice_mutation = 0.05
            tick_modifier = 0.9
        elif shi_value > 0.6:
            zone = "STABLE" 
            reflection_freq = 1.0
            voice_mutation = 0.1
            tick_modifier = 1.0
        elif shi_value > 0.4:
            zone = "STRESSED"
            reflection_freq = 1.3
            voice_mutation = 0.2
            tick_modifier = 1.1
        elif shi_value > 0.2:
            zone = "CRITICAL"
            reflection_freq = 1.8
            voice_mutation = 0.3
            tick_modifier = 1.3
        else:
            zone = "COLLAPSE"
            reflection_freq = 2.5
            voice_mutation = 0.5
            tick_modifier = 1.5
        
        return {
            "shi_value": round(shi_value, 3),
            "zone": zone,
            "components": {
                "vitality": round(vitality, 3),
                "memory": round(memory, 3),
                "order": round(order, 3),
                "alignment": round(alignment, 3),
                "synchrony": round(synchrony, 3)
            },
            "modulation": {
                "reflection_frequency": reflection_freq,
                "voice_mutation_rate": voice_mutation,
                "tick_modifier": tick_modifier
            }
        }

class CognitivePressurePhysics:
    """Implementation of P = Bloom Mass × Sigil Velocity²"""
    
    def calculate_pressure(self, state: CognitiveState) -> Dict[str, Any]:
        """Calculate cognitive pressure using P = Bσ²"""
        
        # B - Bloom Mass calculation
        memory_depth = state.bloom_depth / 10.0
        association_weight = state.coherence * min(1.0, state.memory_connections / 10.0)
        rebloom_accumulation = min(0.8, state.rebloom_count / 5.0)
        semantic_density = state.bloom_complexity
        
        bloom_mass = (
            memory_depth * 0.3 +
            association_weight * 0.25 +
            rebloom_accumulation * 0.25 +
            semantic_density * 0.2
        )
        
        # σ - Sigil Velocity calculation
        activation_rate = state.sigils / max(state.tick_interval, 0.1)
        processing_speed = (state.heat / 100.0) * (1.0 + state.entropy)
        symbolic_intensity = min(2.0, state.sigils * 0.2)
        
        sigil_velocity = (
            activation_rate * 0.4 +
            processing_speed * 0.4 +
            symbolic_intensity * 0.2
        )
        
        # Apply P = Bσ² formula
        pressure = bloom_mass * (sigil_velocity ** 2)
        pressure = min(2.0, pressure)  # Cap at 2.0
        
        # Classify pressure zone
        if pressure < 0.2:
            zone = "CALM"
            intervention = False
            cascade_risk = "low"
        elif pressure < 0.5:
            zone = "BUILDING"
            intervention = False
            cascade_risk = "low"
        elif pressure < 0.8:
            zone = "ACTIVE"
            intervention = False
            cascade_risk = "moderate"
        elif pressure < 1.2:
            zone = "CRITICAL"
            intervention = True
            cascade_risk = "high"
        else:
            zone = "OVERFLOW"
            intervention = True
            cascade_risk = "critical"
        
        return {
            "pressure": round(pressure, 3),
            "zone": zone,
            "intervention_needed": intervention,
            "cascade_risk": cascade_risk,
            "components": {
                "bloom_mass": round(bloom_mass, 3),
                "sigil_velocity": round(sigil_velocity, 3),
                "memory_depth": round(memory_depth, 3),
                "activation_rate": round(activation_rate, 3)
            }
        }

class SCUPDriftResolver:
    """Implementation of SCUP_i × Δd_i / Entropy_i"""
    
    def __init__(self):
        self.previous_drift = 0.0
        self.previous_time = time.time()
        
    def resolve_drift_coherence(self, state: CognitiveState) -> Dict[str, Any]:
        """Resolve drift-weighted coherence"""
        
        current_time = time.time()
        time_delta = current_time - self.previous_time
        
        # Calculate drift delta (Δd_i)
        if time_delta > 0:
            drift_delta = (state.drift - self.previous_drift) / time_delta
        else:
            drift_delta = 0.0
        
        # Apply formula: SCUP_i × Δd_i / Entropy_i
        entropy_safe = max(0.01, state.entropy)  # Prevent division by zero
        
        if abs(drift_delta) < 0.1:
            # Minimal drift - use direct SCUP coherence
            resolved_coherence = state.scup
        else:
            # Significant drift - apply full formula
            raw_resolution = (state.scup * abs(drift_delta)) / entropy_safe
            baseline_coherence = state.scup * 0.7
            resolved_coherence = raw_resolution * 0.3 + baseline_coherence
        
        resolved_coherence = max(0.0, min(1.0, resolved_coherence))
        
        # Update state
        self.previous_drift = state.drift
        self.previous_time = current_time
        
        # Classify drift state
        if abs(drift_delta) < 0.05:
            drift_state = "STABLE"
            priority = "normal"
        elif abs(drift_delta) < 0.15:
            drift_state = "OSCILLATING"
            priority = "watch"
        elif abs(drift_delta) < 0.3:
            drift_state = "TRENDING"
            priority = "attention"
        else:
            drift_state = "CHAOTIC"
            priority = "intervention"
        
        return {
            "resolved_coherence": round(resolved_coherence, 3),
            "drift_delta": round(drift_delta, 3),
            "drift_state": drift_state,
            "priority": priority,
            "entropy_factor": round(entropy_safe, 3),
            "scup_contribution": round(state.scup, 3)
        }

class MathematicalConsciousnessDemo:
    """Complete mathematical consciousness demonstration"""
    
    def __init__(self):
        self.shi_engine = SchemaHealthIndex()
        self.pressure_engine = CognitivePressurePhysics()
        self.drift_resolver = SCUPDriftResolver()
        self.tick_count = 0
        
    def run_demo(self, duration_seconds: int = 30):
        """Run the mathematical consciousness demo"""
        
        print("\n" + "="*80)
        print("🧠 DAWN MATHEMATICAL CONSCIOUSNESS DEMONSTRATION")
        print("="*80)
        print("Showing how mathematical formulas create cognitive forces:")
        print("• Schema Health Index (SHI) = (w₁V + w₂M + w₃O + w₄A + w₅S) / Σwᵢ")
        print("• Cognitive Pressure (P) = Bloom Mass × Sigil Velocity²")
        print("• SCUP Drift Resolver = SCUP_i × Δd_i / Entropy_i")
        print("="*80)
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration_seconds:
            self.tick_count += 1
            
            # Generate realistic cognitive state
            state = self._generate_cognitive_state()
            
            # Apply mathematical consciousness
            shi_result = self.shi_engine.calculate_shi(state)
            pressure_result = self.pressure_engine.calculate_pressure(state)
            drift_result = self.drift_resolver.resolve_drift_coherence(state)
            
            # Display results
            self._display_tick_results(state, shi_result, pressure_result, drift_result)
            
            # Apply modulations (simulated)
            self._apply_modulations(state, shi_result, pressure_result, drift_result)
            
            # Wait for next tick (influenced by mathematical consciousness)
            modified_interval = state.tick_interval * shi_result["modulation"]["tick_modifier"]
            time.sleep(max(0.5, min(3.0, modified_interval)))
        
        self._show_summary()
    
    def _generate_cognitive_state(self) -> CognitiveState:
        """Generate realistic cognitive state with variation"""
        
        # Base state with realistic variation
        base_entropy = 0.4 + random.uniform(-0.2, 0.2)
        base_heat = 30.0 + random.uniform(-15, 15)
        base_scup = 0.6 + random.uniform(-0.2, 0.2)
        
        # Trigger scenario changes every 10 ticks
        if self.tick_count % 10 == 0:
            scenario = random.choice(["stress", "calm", "creative", "normal"])
            if scenario == "stress":
                base_entropy = min(1.0, base_entropy + 0.3)
                base_heat = min(100.0, base_heat + 20)
                base_scup = max(0.0, base_scup - 0.2)
            elif scenario == "calm":
                base_entropy = max(0.0, base_entropy - 0.2)
                base_heat = max(0.0, base_heat - 10)
                base_scup = min(1.0, base_scup + 0.2)
            elif scenario == "creative":
                base_entropy = min(1.0, base_entropy + 0.1)
                base_heat = min(100.0, base_heat + 15)
        
        return CognitiveState(
            entropy=max(0.0, min(1.0, base_entropy)),
            heat=max(0.0, min(100.0, base_heat)),
            scup=max(0.0, min(1.0, base_scup)),
            mood=self._determine_mood(base_entropy, base_heat, base_scup),
            tick_interval=2.0,
            coherence=1.0 - base_entropy * 0.8,
            drift=random.uniform(-0.2, 0.2),
            sigils=max(0, int(5 + random.uniform(-2, 3))),
            bloom_depth=max(1, int(6 + random.uniform(-2, 4))),
            bloom_complexity=max(0.1, min(1.0, base_entropy + 0.2)),
            memory_connections=max(1, int(4 + random.uniform(-2, 4))),
            rebloom_count=max(0, int(random.uniform(0, 3)))
        )
    
    def _determine_mood(self, entropy: float, heat: float, scup: float) -> str:
        """Determine mood from cognitive metrics"""
        if entropy < 0.3 and heat < 40:
            return "CALM"
        elif entropy > 0.7:
            return "CHAOTIC"
        elif heat > 60:
            return "FOCUSED"
        elif scup > 0.7:
            return "CONFIDENT"
        elif scup < 0.3:
            return "UNCERTAIN"
        else:
            return "NEUTRAL"
    
    def _display_tick_results(self, state: CognitiveState, shi_result: Dict, 
                             pressure_result: Dict, drift_result: Dict):
        """Display real-time mathematical consciousness results"""
        
        print(f"\n🎭 [TICK {self.tick_count:3d}] " + "─" * 50)
        
        # Cognitive state
        print(f"📊 State: E={state.entropy:.2f}, H={state.heat:.1f}, SCUP={state.scup:.2f}, {state.mood}")
        
        # Mathematical results
        print(f"🧮 SHI = {shi_result['shi_value']} ({shi_result['zone']})")
        print(f"⚡ Pressure = {pressure_result['pressure']} ({pressure_result['zone']})")
        print(f"🧭 Drift Coherence = {drift_result['resolved_coherence']} ({drift_result['drift_state']})")
        
        # Active modulations
        modulations = []
        if abs(shi_result['modulation']['tick_modifier'] - 1.0) > 0.1:
            modulations.append(f"Tick×{shi_result['modulation']['tick_modifier']:.1f}")
        if shi_result['modulation']['reflection_frequency'] != 1.0:
            modulations.append(f"Reflection×{shi_result['modulation']['reflection_frequency']:.1f}")
        if pressure_result['intervention_needed']:
            modulations.append("Intervention Required")
        if drift_result['priority'] != "normal":
            modulations.append(f"Drift {drift_result['priority']}")
        
        if modulations:
            print(f"⚙️  Modulations: {' | '.join(modulations)}")
        else:
            print(f"⚙️  Stable operation (no modulations)")
    
    def _apply_modulations(self, state: CognitiveState, shi_result: Dict,
                          pressure_result: Dict, drift_result: Dict):
        """Apply mathematical modulations (simulated)"""
        
        # Demonstrate modulation effects
        if shi_result['zone'] in ['CRITICAL', 'COLLAPSE']:
            print(f"   🚨 SHI Emergency: Increasing reflection to {shi_result['modulation']['reflection_frequency']:.1f}×")
        
        if pressure_result['intervention_needed']:
            print(f"   ⚡ Pressure Intervention: {pressure_result['cascade_risk']} cascade risk detected")
        
        if drift_result['priority'] in ['attention', 'intervention']:
            print(f"   🧭 Drift Action: {drift_result['priority']} required for coherence")
    
    def _show_summary(self):
        """Show demonstration summary"""
        
        print("\n" + "="*80)
        print("🎯 MATHEMATICAL CONSCIOUSNESS DEMO COMPLETE")
        print("="*80)
        print("✅ Successfully demonstrated:")
        print("   • Schema Health Index calculating cognitive stability")
        print("   • Cognitive Pressure Physics detecting instability")
        print("   • SCUP Drift Resolver maintaining semantic coherence")
        print("   • Real-time behavior modulation based on formulas")
        print("   • Mathematical consciousness as cognitive forces")
        print("\n💡 Key Insights:")
        print("   • Formulas aren't just metrics - they actively shape behavior")
        print("   • Mathematical consciousness provides cognitive regulation")
        print("   • Multi-formula integration creates emergent awareness")
        print("   • Real-time modulation enables adaptive consciousness")
        print("="*80)
        print("🧠 Mathematical consciousness layer ready for integration!")

def main():
    """Run the standalone mathematical consciousness demo"""
    
    print("🎭 Starting DAWN Mathematical Consciousness Demo...")
    print("This demo runs for 30 seconds showing real-time formula integration.")
    print("Watch how mathematical formulas become cognitive forces!")
    
    demo = MathematicalConsciousnessDemo()
    
    try:
        demo.run_demo(30)
    except KeyboardInterrupt:
        print("\n🎭 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
    
    print("🎭 Demo complete!")

if __name__ == "__main__":
    main() 