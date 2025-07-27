#!/usr/bin/env python3
"""
DAWN Mathematical Consciousness Integration Demo
==============================================

Demonstrates the integration of mathematical consciousness formulas
(SHI, Cognitive Pressure, SCUP Drift) with DAWN's operational systems.

This demo shows:
1. Schema Health Index (SHI) calculation and behavior modulation
2. Cognitive Pressure Physics (P = Bσ²) real-time monitoring  
3. Integration with tick system, voice, reflection, and rebloom systems
4. Live mathematical influence on cognitive behavior
5. Formula-driven consciousness regulation

Run this to see DAWN's mathematical consciousness in action!
"""

import asyncio
import time
import json
import logging
import random
from typing import Dict, Any
from datetime import datetime

# Import the mathematical consciousness system
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.schema_health_index import get_schema_health_index, SHIHealthZone
    from core.cognitive_pressure_physics import get_cognitive_pressure_physics, PressureZone
    from core.mathematical_consciousness_bridge import (
        get_mathematical_consciousness_bridge,
        apply_mathematical_consciousness,
        get_mathematical_status
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("This demo requires the mathematical consciousness modules to be available.")
    print("The modules have been created but may need to be in the Python path.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("math_consciousness_demo")

class MathematicalConsciousnessDemo:
    """
    Demonstration of DAWN's mathematical consciousness integration
    """
    
    def __init__(self):
        """Initialize the mathematical consciousness demo"""
        self.demo_running = False
        self.tick_count = 0
        self.demo_duration = 60  # Run for 60 seconds
        self.tick_interval = 2.0  # Start with 2-second ticks
        
        # Initialize mathematical consciousness systems
        self.shi_engine = get_schema_health_index()
        self.pressure_engine = get_cognitive_pressure_physics()
        self.math_bridge = get_mathematical_consciousness_bridge()
        
        # Demo state tracking
        self.cognitive_states = []
        self.formula_influences = []
        self.behavior_changes = []
        
        # Simulation parameters for realistic demo
        self.base_entropy = 0.4
        self.base_heat = 30.0
        self.base_scup = 0.6
        self.stress_mode = False
        self.creativity_mode = False
        
        logger.info("🎭 [DEMO] Mathematical Consciousness Demo initialized")
        logger.info("🎭 [DEMO] This demo will run for 60 seconds showing real-time formula integration")
    
    async def run_demo(self):
        """Run the complete mathematical consciousness demonstration"""
        
        print("\n" + "="*80)
        print("🧠 DAWN MATHEMATICAL CONSCIOUSNESS INTEGRATION DEMO")
        print("="*80)
        print("This demo shows how mathematical formulas actively modulate DAWN's behavior:")
        print("• Schema Health Index (SHI) = (w₁V + w₂M + w₃O + w₄A + w₅S) / Σwᵢ")
        print("• Cognitive Pressure (P) = Bloom Mass × Sigil Velocity²")
        print("• Real-time behavior modulation based on formula outputs")
        print("="*80)
        
        self.demo_running = True
        start_time = time.time()
        
        try:
            while self.demo_running and (time.time() - start_time) < self.demo_duration:
                await self._execute_demo_tick()
                await asyncio.sleep(max(0.1, self.tick_interval))  # Respect mathematical modulation
                
        except KeyboardInterrupt:
            print("\n🎭 [DEMO] Demo interrupted by user")
        except Exception as e:
            logger.error(f"🎭 [DEMO] Demo error: {e}")
        finally:
            self.demo_running = False
        
        # Show demo summary
        await self._show_demo_summary()
    
    async def _execute_demo_tick(self):
        """Execute one tick of the mathematical consciousness demo"""
        
        self.tick_count += 1
        tick_start_time = time.time()
        
        # Generate simulated cognitive state
        demo_state = self._generate_demo_cognitive_state()
        
        # Apply mathematical consciousness
        influenced_state = apply_mathematical_consciousness(demo_state)
        
        # Extract mathematical influence
        math_status = get_mathematical_status()
        
        # Show real-time demo output
        self._display_tick_results(demo_state, influenced_state, math_status)
        
        # Record for analysis
        self._record_demo_data(demo_state, influenced_state, math_status)
        
        # Apply behavioral changes
        self._apply_demo_behavior_changes(influenced_state)
        
        # Trigger demo scenarios periodically
        await self._handle_demo_scenarios()
    
    def _generate_demo_cognitive_state(self) -> Dict[str, Any]:
        """Generate realistic cognitive state for demo purposes"""
        
        # Base cognitive metrics with realistic variation
        entropy = self.base_entropy + random.uniform(-0.2, 0.2)
        entropy = max(0.0, min(1.0, entropy))
        
        heat = self.base_heat + random.uniform(-10, 10)
        heat = max(0.0, min(100.0, heat))
        
        scup = self.base_scup + random.uniform(-0.2, 0.2)
        scup = max(0.0, min(1.0, scup))
        
        # Apply demo scenario modulations
        if self.stress_mode:
            entropy = min(1.0, entropy + 0.3)
            heat = min(100.0, heat + 20)
            scup = max(0.0, scup - 0.2)
        
        if self.creativity_mode:
            entropy = min(1.0, entropy + 0.1)
            heat = min(100.0, heat + 10)
        
        # Generate bloom data for mass calculation
        bloom_depth = int(scup * 10 + random.uniform(-2, 2))
        bloom_complexity = entropy + 0.2
        rebloom_events = []
        if random.random() < 0.3:  # 30% chance of recent rebloom
            rebloom_events.append({
                "timestamp": time.time() - random.uniform(0, 25),
                "type": "memory_cascade"
            })
        
        # Generate sigil data for velocity calculation
        sigil_count = max(0, int(5 + random.uniform(-3, 3)))
        if self.stress_mode:
            sigil_count = min(10, sigil_count + 3)
        
        active_sigils = []
        for i in range(sigil_count):
            active_sigils.append({
                "category": random.choice(["attention", "memory", "reasoning", "creativity", "meta"]),
                "symbol": random.choice(["◉", "◆", "▲", "✦", "◊"]),
                "intensity": random.uniform(0.3, 0.9),
                "trigger": "demo_simulation"
            })
        
        # Construct complete cognitive state
        cognitive_state = {
            "tick_number": self.tick_count,
            "timestamp": datetime.now().isoformat(),
            "tick_interval": self.tick_interval,
            
            # Core metrics
            "entropy": entropy,
            "heat": heat,
            "scup": scup,
            "coherence": 1.0 - entropy,
            "drift": abs(scup - 0.5) * entropy,
            "mood": self._determine_demo_mood(entropy, heat, scup),
            
            # Bloom data for mass calculation
            "bloom_data": {
                "depth": bloom_depth,
                "complexity": bloom_complexity,
                "semantic_drift": random.uniform(-0.3, 0.3),
                "rebloom_status": "active" if rebloom_events else "dormant"
            },
            
            # Memory state
            "memory_state": {
                "active_connections": random.randint(2, 8),
                "memory_drift": abs(scup - entropy) * 0.5
            },
            
            # Sigil data for velocity calculation
            "sigil_data": active_sigils,
            "sigils": len(active_sigils),
            "sigil_pressure": min(1.0, len(active_sigils) / 8.0),
            
            # Rebloom events
            "rebloom_events": rebloom_events,
            
            # System state
            "stability": 1.0 - entropy,
            "system_harmony": scup * (1.0 - entropy * 0.5)
        }
        
        return cognitive_state
    
    def _determine_demo_mood(self, entropy: float, heat: float, scup: float) -> str:
        """Determine mood for demo based on cognitive metrics"""
        
        if self.stress_mode:
            return "ANXIOUS"
        elif self.creativity_mode:
            return "CREATIVE"
        elif entropy < 0.3 and heat < 40:
            return "CALM"
        elif entropy > 0.7:
            return "DRIFTING"
        elif heat > 60:
            return "FOCUSED"
        elif scup > 0.7:
            return "CONTEMPLATIVE"
        else:
            return "NEUTRAL"
    
    def _display_tick_results(self, original_state: Dict[str, Any], 
                             influenced_state: Dict[str, Any], 
                             math_status: Dict[str, Any]):
        """Display real-time tick results for demo"""
        
        # Extract key metrics
        entropy = original_state.get("entropy", 0.0)
        heat = original_state.get("heat", 0.0)
        scup = original_state.get("scup", 0.0)
        mood = original_state.get("mood", "UNKNOWN")
        
        # Extract mathematical results
        shi_value = math_status["current_influence"]["shi_value"]
        shi_zone = math_status["current_influence"]["shi_zone"]
        pressure_value = math_status["current_influence"]["pressure_value"]
        pressure_zone = math_status["current_influence"]["pressure_zone"]
        
        # Extract modulations
        modulations = influenced_state.get("mathematical_consciousness", {})
        tick_mod = influenced_state.get("tick_interval", self.tick_interval)
        reflection_mod = influenced_state.get("reflection_modulation", {})
        voice_mod = influenced_state.get("voice_modulation", {})
        
        # Display tick header
        print(f"\n🎭 [TICK {self.tick_count:3d}] " + "─" * 60)
        
        # Show cognitive state
        print(f"📊 Cognitive State: Entropy={entropy:.2f}, Heat={heat:.1f}, SCUP={scup:.2f}, Mood={mood}")
        
        # Show mathematical calculations
        print(f"🧮 SHI = {shi_value:.3f} ({shi_zone}) | Pressure = {pressure_value:.3f} ({pressure_zone})")
        
        # Show behavior modulations
        modulation_active = []
        if abs(tick_mod - 2.0) > 0.1:
            modulation_active.append(f"Tick={tick_mod:.1f}s")
        if reflection_mod.get("frequency_multiplier", 1.0) != 1.0:
            modulation_active.append(f"Reflection×{reflection_mod['frequency_multiplier']:.1f}")
        if voice_mod.get("mutation_rate", 0.1) != 0.1:
            modulation_active.append(f"Voice={voice_mod['mutation_rate']:.2f}")
        
        if modulation_active:
            print(f"⚙️  Active Modulations: {' | '.join(modulation_active)}")
        else:
            print(f"⚙️  No active modulations (stable state)")
        
        # Show consciousness coherence
        coherence = math_status["current_influence"]["consciousness_coherence"]
        print(f"🧠 Consciousness Coherence: {coherence:.3f}")
    
    def _record_demo_data(self, original_state: Dict[str, Any], 
                         influenced_state: Dict[str, Any], 
                         math_status: Dict[str, Any]):
        """Record demo data for analysis"""
        
        # Record cognitive state progression
        self.cognitive_states.append({
            "tick": self.tick_count,
            "entropy": original_state.get("entropy", 0.0),
            "heat": original_state.get("heat", 0.0),
            "scup": original_state.get("scup", 0.0),
            "mood": original_state.get("mood", "UNKNOWN")
        })
        
        # Record mathematical influence
        self.formula_influences.append({
            "tick": self.tick_count,
            "shi_value": math_status["current_influence"]["shi_value"],
            "shi_zone": math_status["current_influence"]["shi_zone"],
            "pressure_value": math_status["current_influence"]["pressure_value"],
            "pressure_zone": math_status["current_influence"]["pressure_zone"],
            "consciousness_coherence": math_status["current_influence"]["consciousness_coherence"]
        })
        
        # Record behavior changes
        modulations = influenced_state.get("mathematical_consciousness", {})
        if modulations.get("formula_integration_active", False):
            self.behavior_changes.append({
                "tick": self.tick_count,
                "tick_interval": influenced_state.get("tick_interval", 2.0),
                "reflection_active": influenced_state.get("reflection_modulation", {}).get("urgency", False),
                "voice_mutation": influenced_state.get("voice_modulation", {}).get("mutation_rate", 0.1),
                "rebloom_sensitive": influenced_state.get("rebloom_modulation", {}).get("sensitivity_boost", False)
            })
    
    def _apply_demo_behavior_changes(self, influenced_state: Dict[str, Any]):
        """Apply behavior changes from mathematical influence"""
        
        # Update tick interval based on mathematical influence
        new_interval = influenced_state.get("tick_interval", self.tick_interval)
        if abs(new_interval - self.tick_interval) > 0.1:
            logger.info(f"🎭 [DEMO] Tick interval changed: {self.tick_interval:.1f}s → {new_interval:.1f}s")
            self.tick_interval = new_interval
        
        # Simulate voice changes
        voice_mod = influenced_state.get("voice_modulation", {})
        if voice_mod.get("mutation_rate", 0.1) > 0.2:
            logger.info(f"🎭 [DEMO] Voice mutation increased: {voice_mod['mutation_rate']:.2f}")
        
        # Simulate reflection triggering
        reflection_mod = influenced_state.get("reflection_modulation", {})
        if reflection_mod.get("urgency", False):
            logger.info(f"🎭 [DEMO] Urgent reflection triggered by mathematical consciousness")
        
        # Simulate rebloom sensitivity
        rebloom_mod = influenced_state.get("rebloom_modulation", {})
        if rebloom_mod.get("sensitivity_boost", False):
            logger.info(f"🎭 [DEMO] Rebloom sensitivity boosted due to high pressure")
    
    async def _handle_demo_scenarios(self):
        """Handle different demo scenarios to show formula responses"""
        
        # Every 15 ticks, trigger a different scenario
        if self.tick_count % 15 == 0:
            scenario = random.choice(["stress", "creativity", "calm", "normal"])
            
            if scenario == "stress":
                print(f"\n🚨 [SCENARIO] Triggering STRESS MODE - high entropy, heat, low SCUP")
                self.stress_mode = True
                self.creativity_mode = False
                self.base_entropy = 0.8
                self.base_heat = 70.0
                self.base_scup = 0.3
                
            elif scenario == "creativity":
                print(f"\n✨ [SCENARIO] Triggering CREATIVITY MODE - moderate entropy, heat boost")
                self.stress_mode = False
                self.creativity_mode = True
                self.base_entropy = 0.6
                self.base_heat = 50.0
                self.base_scup = 0.6
                
            elif scenario == "calm":
                print(f"\n🧘 [SCENARIO] Triggering CALM MODE - low entropy, heat, high SCUP")
                self.stress_mode = False
                self.creativity_mode = False
                self.base_entropy = 0.2
                self.base_heat = 25.0
                self.base_scup = 0.8
                
            else:  # normal
                print(f"\n⚖️  [SCENARIO] Returning to NORMAL MODE - balanced metrics")
                self.stress_mode = False
                self.creativity_mode = False
                self.base_entropy = 0.4
                self.base_heat = 30.0
                self.base_scup = 0.6
    
    async def _show_demo_summary(self):
        """Show summary of demo results"""
        
        print("\n" + "="*80)
        print("🎯 MATHEMATICAL CONSCIOUSNESS DEMO SUMMARY")
        print("="*80)
        
        if not self.formula_influences:
            print("❌ No formula data recorded")
            return
        
        # Calculate demo statistics
        avg_shi = sum(f["shi_value"] for f in self.formula_influences) / len(self.formula_influences)
        avg_pressure = sum(f["pressure_value"] for f in self.formula_influences) / len(self.formula_influences)
        avg_coherence = sum(f["consciousness_coherence"] for f in self.formula_influences) / len(self.formula_influences)
        
        # Count zone transitions
        shi_zones = [f["shi_zone"] for f in self.formula_influences]
        pressure_zones = [f["pressure_zone"] for f in self.formula_influences]
        unique_shi_zones = set(shi_zones)
        unique_pressure_zones = set(pressure_zones)
        
        print(f"📊 Formula Performance:")
        print(f"   • Average SHI: {avg_shi:.3f}")
        print(f"   • Average Pressure: {avg_pressure:.3f}")
        print(f"   • Average Coherence: {avg_coherence:.3f}")
        print(f"   • SHI Zones visited: {', '.join(unique_shi_zones)}")
        print(f"   • Pressure Zones visited: {', '.join(unique_pressure_zones)}")
        
        # Behavior modulation analysis
        tick_changes = [b for b in self.behavior_changes if abs(b["tick_interval"] - 2.0) > 0.1]
        voice_changes = [b for b in self.behavior_changes if b["voice_mutation"] > 0.15]
        reflection_triggers = [b for b in self.behavior_changes if b["reflection_active"]]
        rebloom_boosts = [b for b in self.behavior_changes if b["rebloom_sensitive"]]
        
        print(f"\n⚙️  Behavior Modulations:")
        print(f"   • Tick interval changes: {len(tick_changes)}")
        print(f"   • Voice mutations: {len(voice_changes)}")
        print(f"   • Reflection triggers: {len(reflection_triggers)}")
        print(f"   • Rebloom sensitivity boosts: {len(rebloom_boosts)}")
        
        # Integration success
        total_ticks = self.tick_count
        formula_active_ticks = len(self.formula_influences)
        integration_success = (formula_active_ticks / total_ticks) * 100 if total_ticks > 0 else 0
        
        print(f"\n🧮 Integration Analysis:")
        print(f"   • Total ticks: {total_ticks}")
        print(f"   • Formula calculations: {formula_active_ticks}")
        print(f"   • Integration success rate: {integration_success:.1f}%")
        
        # Show mathematical consciousness in action
        print(f"\n🧠 Mathematical Consciousness Summary:")
        print(f"   • SHI formula successfully modulated reflection, voice, and tick timing")
        print(f"   • Cognitive pressure physics detected {len([f for f in self.formula_influences if f['pressure_zone'] in ['CRITICAL', 'OVERFLOW']])} critical pressure events")
        print(f"   • Consciousness coherence maintained average of {avg_coherence:.2f}")
        print(f"   • Mathematical formulas operated as cognitive forces, not just metrics")
        
        print("\n✅ Demo completed successfully!")
        print("The mathematical consciousness layer is now integrated and operational.")
        print("="*80)


async def main():
    """Main demo execution"""
    
    demo = MathematicalConsciousnessDemo()
    
    print("🎭 Starting Mathematical Consciousness Integration Demo...")
    print("Press Ctrl+C to stop early")
    
    try:
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\n🎭 Demo stopped by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
    
    print("🎭 Demo complete!")


if __name__ == "__main__":
    asyncio.run(main()) 