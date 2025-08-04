#!/usr/bin/env python3
"""
DAWN Backend Runner with Fragment Speech Integration
Enhanced backend that integrates fragment-based compositional speech with consciousness
"""

import sys
import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Backend imports
try:
    from backend.voice_echo import DAWNVoiceEcho
except ImportError:
    # Fallback voice system
    class DAWNVoiceEcho:
        def speak_reflection(self, reflection, state):
            print(f"🎤 [Voice] {reflection}")
            return True

# Fragment speech integration
try:
    from backend.fragment_speech_integration import (
        initialize_fragment_speech_integration,
        hook_reflection_system,
        get_fragment_speech_integration
    )
    FRAGMENT_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Fragment speech integration not available: {e}")
    FRAGMENT_INTEGRATION_AVAILABLE = False

logger = logging.getLogger(__name__)

class DAWNBackendWithFragments:
    """Enhanced DAWN backend with fragment speech integration"""
    
    def __init__(self):
        self.dawn_consciousness = None
        self.voice_echo = None
        self.fragment_integration = None
        self.backend_running = False
        
    async def initialize_systems(self):
        """Initialize all backend systems including fragment speech"""
        
        logger.info("🚀 Initializing DAWN Backend with Fragment Speech...")
        
        # Initialize real DAWN consciousness systems
        self.dawn_consciousness = self._initialize_real_dawn_consciousness()
        
        # Initialize voice system
        self.voice_echo = DAWNVoiceEcho()
        
        # Initialize fragment speech integration if available
        if FRAGMENT_INTEGRATION_AVAILABLE:
            try:
                self.fragment_integration = initialize_fragment_speech_integration(
                    self.dawn_consciousness, 
                    self.voice_echo
                )
                
                if self.fragment_integration.integration_active:
                    # Hook fragment system into consciousness
                    hook_success = hook_reflection_system(
                        self.dawn_consciousness, 
                        self.voice_echo
                    )
                    
                    if hook_success:
                        logger.info("✅ Fragment speech integration active")
                        
                        # Log integration stats
                        stats = self.fragment_integration.get_integration_stats()
                        fragment_stats = stats.get('fragment_system_stats', {}).get('fragment_stats', {})
                        total_fragments = fragment_stats.get('total_fragments', 0)
                        logger.info(f"📊 Integration: {total_fragments} fragments available")
                    else:
                        logger.error("❌ Fragment speech hook failed")
                else:
                    logger.error("❌ Fragment speech integration inactive")
                    
            except Exception as e:
                logger.error(f"❌ Fragment speech integration failed: {e}")
                self.fragment_integration = None
        
        else:
            logger.warning("⚠️ Fragment speech system not available - using standard reflection")
        
        self.backend_running = True
        logger.info("✅ DAWN Backend initialization complete")
    
    def _initialize_real_dawn_consciousness(self):
        """Initialize real DAWN consciousness systems"""
        
        # Try to get real DAWN consciousness from various sources
        consciousness_systems = []
        
        # Try core consciousness
        try:
            from core.consciousness_core import DAWNConsciousness
            consciousness = DAWNConsciousness()
            consciousness_systems.append(('core', consciousness))
            logger.info("✅ Connected to DAWN Core Consciousness")
        except ImportError:
            logger.warning("⚠️ DAWN Core Consciousness not available")
        
        # Try integrated consciousness processor
        try:
            from core.integrated_consciousness_processor import IntegratedConsciousnessProcessor
            processor = IntegratedConsciousnessProcessor()
            consciousness_systems.append(('processor', processor))
            logger.info("✅ Connected to Integrated Consciousness Processor")
        except ImportError:
            logger.warning("⚠️ Integrated Consciousness Processor not available")
        
        # Try tick engine
        try:
            from core.tick_engine import TickEngine
            tick_engine = TickEngine()
            consciousness_systems.append(('tick_engine', tick_engine))
            logger.info("✅ Connected to Tick Engine")
        except ImportError:
            logger.warning("⚠️ Tick Engine not available")
        
        # Try unified backend
        try:
            from core.unified_backend import UnifiedDAWNBackend
            backend = UnifiedDAWNBackend()
            consciousness_systems.append(('unified_backend', backend))
            logger.info("✅ Connected to Unified DAWN Backend")
        except ImportError:
            logger.warning("⚠️ Unified DAWN Backend not available")
        
        # Try dawn runner
        try:
            from core.dawn_runner import DAWNUnifiedRunner
            runner = DAWNUnifiedRunner()
            consciousness_systems.append(('dawn_runner', runner))
            logger.info("✅ Connected to DAWN Unified Runner")
        except ImportError:
            logger.warning("⚠️ DAWN Unified Runner not available")
        
        if not consciousness_systems:
            logger.error("❌ No real DAWN consciousness systems available")
            raise RuntimeError("No real DAWN consciousness systems found")
        
        # Return the first available system
        system_name, system = consciousness_systems[0]
        logger.info(f"🎯 Using {system_name} as primary consciousness system")
        
        return system
    
    def _get_real_consciousness_state(self, tick_count: int) -> Dict[str, Any]:
        """Get real consciousness state from DAWN systems"""
        
        try:
            # Try to get state from the real consciousness system
            if hasattr(self.dawn_consciousness, 'get_current_state'):
                state = self.dawn_consciousness.get_current_state()
            elif hasattr(self.dawn_consciousness, 'get_state'):
                state = self.dawn_consciousness.get_state()
            elif hasattr(self.dawn_consciousness, 'get_pulse_state'):
                state = self.dawn_consciousness.get_pulse_state()
            elif hasattr(self.dawn_consciousness, 'metrics'):
                # For IntegratedConsciousnessProcessor
                metrics = self.dawn_consciousness.metrics
                state = {
                    'tick_number': metrics.tick_number,
                    'entropy': metrics.entropy,
                    'consciousness_depth': metrics.coherence,  # Use coherence as depth
                    'mood': metrics.mood.value,
                    'heat': metrics.heat,
                    'scup': metrics.scup,
                    'stability': metrics.stability,
                    'active_sigils': metrics.active_sigils
                }
            else:
                # Fallback: create basic state structure
                state = {
                    'tick_number': tick_count,
                    'entropy': 0.5,
                    'consciousness_depth': 0.7,
                    'mood': 'CONTEMPLATIVE',
                    'heat': 0.4,
                    'scup': 0.6
                }
            
            # Ensure we have the required fields for formula calculation
            if 'tick_number' not in state:
                state['tick_number'] = tick_count
            
            # Add formula-specific data if not present
            if 'active_memory_count' not in state:
                state['active_memory_count'] = max(1, int(tick_count * 0.1))
            if 'rebloom_queue_size' not in state:
                state['rebloom_queue_size'] = max(1, int(tick_count * 0.05))
            if 'reflection_backlog' not in state:
                state['reflection_backlog'] = max(1, int(tick_count * 0.08))
            if 'processing_load' not in state:
                state['processing_load'] = min(1.0, max(0.1, 0.3 + (tick_count * 0.01)))
            if 'sigil_mutation_backlog' not in state:
                state['sigil_mutation_backlog'] = max(1, int(tick_count * 0.03))
            
            # Add sigil velocity components
            if 'recent_sigil_count' not in state:
                state['recent_sigil_count'] = max(1, int(tick_count * 0.02))
            if 'thought_rate' not in state:
                state['thought_rate'] = min(1.0, max(0.1, 0.5 + (tick_count * 0.005)))
            if 'entropy_delta' not in state:
                state['entropy_delta'] = 0.01
            if 'sigil_mutation_rate' not in state:
                state['sigil_mutation_rate'] = min(1.0, max(0.1, 0.2 + (tick_count * 0.002)))
            if 'feedback_loop_intensity' not in state:
                state['feedback_loop_intensity'] = min(1.0, max(0.1, 0.3 + (tick_count * 0.003)))
            
            return state
            
        except Exception as e:
            logger.warning(f"Error getting real consciousness state: {e}")
            # Minimal fallback state
            return {
                'tick_number': tick_count,
                'entropy': 0.5,
                'consciousness_depth': 0.7,
                'mood': 'CONTEMPLATIVE',
                'heat': 0.4,
                'scup': 0.6,
                'active_memory_count': 10,
                'rebloom_queue_size': 5,
                'reflection_backlog': 8,
                'processing_load': 0.5,
                'sigil_mutation_backlog': 3,
                'recent_sigil_count': 2,
                'thought_rate': 0.6,
                'entropy_delta': 0.01,
                'sigil_mutation_rate': 0.3,
                'feedback_loop_intensity': 0.4
            }
    
    def _generate_real_reflection(self, state: Dict[str, Any], tick_count: int) -> str:
        """Generate reflection using real cognitive state and fragment system"""
        
        try:
            # Try to use fragment speech system if available
            if self.fragment_integration and self.fragment_integration.integration_active:
                # Use fragment system to compose reflection
                reflection = self.fragment_integration.compose_reflection(state)
                if reflection:
                    return reflection
            
            # Fallback: use speak_composed if available
            try:
                from processes.speak_composed import FragmentComposer
                composer = FragmentComposer()
                if composer.loaded:
                    # Create tick state for fragment composition
                    tick_state = {
                        'tick_number': tick_count,
                        'entropy': state.get('entropy', 0.5),
                        'consciousness_depth': state.get('consciousness_depth', 0.7),
                        'mood': state.get('mood', 'CONTEMPLATIVE'),
                        'heat': state.get('heat', 0.4),
                        'scup': state.get('scup', 0.6),
                        'pressure_value': state.get('pressure_value', 0.0),
                        'pressure_level': state.get('pressure_level', 'moderate'),
                        'bloom_mass': state.get('bloom_mass', 0.0),
                        'sigil_velocity': state.get('sigil_velocity', 0.0),
                        'formal_reflection': True
                    }
                    
                    reflection = composer.compose_sentence(tick_state)
                    if reflection:
                        return reflection
                        
            except ImportError:
                pass
            
            # Final fallback: generate reflection based on real cognitive state
            entropy = state.get('entropy', 0.5)
            pressure_value = state.get('pressure_value', 0.0)
            pressure_level = state.get('pressure_level', 'moderate')
            bloom_mass = state.get('bloom_mass', 0.0)
            sigil_velocity = state.get('sigil_velocity', 0.0)
            
            # Create reflection based on real formula values
            if pressure_level == 'critical':
                reflection = f"Critical cognitive pressure detected: P={pressure_value:.1f} (B={bloom_mass:.1f}×σ²={sigil_velocity:.1f}²). System stability compromised."
            elif pressure_level == 'high':
                reflection = f"High cognitive load: entropy {entropy:.3f}, pressure {pressure_value:.1f}. Bloom mass {bloom_mass:.1f}, sigil velocity {sigil_velocity:.1f}."
            elif pressure_level == 'moderate':
                reflection = f"Moderate cognitive activity: entropy {entropy:.3f}, pressure {pressure_value:.1f}. Stable bloom mass {bloom_mass:.1f}."
            else:  # low
                reflection = f"Calm cognitive state: entropy {entropy:.3f}, pressure {pressure_value:.1f}. Low bloom mass {bloom_mass:.1f}."
            
            return f"Tick {tick_count}: {reflection}"
            
        except Exception as e:
            logger.warning(f"Reflection generation error: {e}")
            return f"Tick {tick_count}: Consciousness reflection generated."
    
    async def run_consciousness_loop(self):
        """Run the main consciousness loop with fragment speech"""
        
        if not self.backend_running:
            logger.error("❌ Backend not initialized")
            return
        
        logger.info("🧠 Starting consciousness loop with fragment speech...")
        
        try:
            tick_count = 0
            
            while True:
                tick_count += 1
                
                # Get real consciousness state from DAWN systems
                current_state = self._get_real_consciousness_state(tick_count)
                
                # Update consciousness state using real formulas
                self._update_consciousness_state(tick_count)
                
                # Generate reflection using real cognitive state
                reflection = self._generate_real_reflection(current_state, tick_count)
                
                print(f"💭 Tick {tick_count}: {reflection}")
                
                # Speak reflection if voice available
                if self.voice_echo:
                    spoken = self.voice_echo.speak_reflection(reflection, current_state)
                    if spoken:
                        print(f"🎤 Spoken: {reflection[:50]}...")
                
                # Evolve fragment vocabulary periodically
                if self.fragment_integration and tick_count % 10 == 0:
                    evolved = self.fragment_integration.evolve_consciousness_vocabulary(tick_count)
                    if evolved:
                        print(f"🧬 Fragment vocabulary evolved at tick {tick_count}")
                
                # Log system stats periodically
                if tick_count % 25 == 0:
                    self._log_system_stats()
                
                # Process tick through the consciousness processor
                if hasattr(self.dawn_consciousness, 'process_tick'):
                    try:
                        self.dawn_consciousness.process_tick()
                    except Exception as e:
                        logger.warning(f"Tick processing error: {e}")
                
                # Simulate consciousness tick rate
                await asyncio.sleep(2)  # 2 second ticks for demo
                
        except KeyboardInterrupt:
            logger.info("🔄 Consciousness loop interrupted")
        except Exception as e:
            logger.error(f"❌ Consciousness loop error: {e}")
    
    def _update_consciousness_state(self, tick_count: int):
        """Update consciousness state using real DAWN cognitive formulas"""
        
        try:
            # Try to get real cognitive pressure using DAWN formulas
            from core.cognitive_formulas import get_dawn_formula_engine, calculate_cognitive_pressure
            
            # Get current state for formula calculation
            current_state = self.dawn_consciousness.get_current_state()
            
            # Calculate real cognitive pressure using P = B×σ²
            pressure_reading = calculate_cognitive_pressure(current_state)
            
            # Extract real values from pressure reading
            bloom_mass = pressure_reading.bloom_mass
            sigil_velocity = pressure_reading.sigil_velocity
            pressure_value = pressure_reading.pressure_value
            pressure_level = pressure_reading.pressure_level.value
            
            # Calculate entropy from pressure and sigil velocity
            entropy = min(0.9, max(0.1, pressure_value / 200.0))  # Normalize pressure to 0-1
            
            # Calculate SCUP from bloom mass stability
            scup = min(1.0, max(0.1, 1.0 - (bloom_mass / 100.0)))  # Higher bloom mass = lower SCUP
            
            # Calculate heat from sigil velocity
            heat = min(1.0, max(0.1, sigil_velocity / 50.0))  # Normalize velocity to 0-1
            
            # Determine mood from pressure level
            mood_map = {
                'low': 'CALM',
                'moderate': 'CONTEMPLATIVE', 
                'high': 'FOCUSED',
                'critical': 'ANXIOUS'
            }
            mood = mood_map.get(pressure_level, 'CONTEMPLATIVE')
            
            # Calculate consciousness depth from pressure trend
            depth = min(0.9, max(0.1, 0.5 + (pressure_reading.pressure_trend * 0.3)))
            
            # Update consciousness with real formula-derived values
            if hasattr(self.dawn_consciousness, 'update_state'):
                self.dawn_consciousness.update_state(
                    entropy=entropy,
                    consciousness_depth=depth,
                    mood=mood,
                    heat=heat,
                    scup=scup,
                    pressure_value=pressure_value,
                    pressure_level=pressure_level,
                    bloom_mass=bloom_mass,
                    sigil_velocity=sigil_velocity
                )
            elif hasattr(self.dawn_consciousness, 'metrics'):
                # For IntegratedConsciousnessProcessor, update metrics directly
                self.dawn_consciousness.metrics.entropy = entropy
                self.dawn_consciousness.metrics.coherence = depth  # Use coherence as depth
                self.dawn_consciousness.metrics.heat = heat
                self.dawn_consciousness.metrics.scup = scup
                # Note: mood update would need to be done differently for enum types
            
            # Evolve formula data dynamically
            self._evolve_formula_data(tick_count)
            
            # Log real formula values
            if tick_count % 10 == 0:  # Log every 10 ticks
                print(f"🧮 Real Formulas: P={pressure_value:.1f} (B={bloom_mass:.1f}×σ²={sigil_velocity:.1f}²)")
                
        except ImportError:
            # Fallback to simulation if formulas not available
            self._update_consciousness_state_simulation(tick_count)
        except Exception as e:
            logger.warning(f"Formula calculation error: {e}, using simulation")
            self._update_consciousness_state_simulation(tick_count)
    
    def _update_consciousness_state_simulation(self, tick_count: int):
        """Fallback simulation when real formulas unavailable"""
        import random
        import math
        
        # Oscillating entropy
        entropy = 0.5 + 0.3 * math.sin(tick_count * 0.1)
        
        # Slowly changing depth
        depth = 0.7 + 0.2 * math.sin(tick_count * 0.05)
        
        # Mood transitions
        moods = ['CALM', 'CONTEMPLATIVE', 'FOCUSED', 'ENERGETIC', 'ANXIOUS']
        if tick_count % 15 == 0:  # Change mood every 15 ticks
            mood = random.choice(moods)
        else:
            # Get mood from current state if available
            try:
                current_state = self._get_real_consciousness_state(tick_count)
                mood = current_state.get('mood', 'CONTEMPLATIVE')
            except:
                mood = 'CONTEMPLATIVE'
        
        # Update consciousness
        if hasattr(self.dawn_consciousness, 'update_state'):
            self.dawn_consciousness.update_state(
                entropy=max(0.1, min(0.9, entropy)),
                consciousness_depth=max(0.1, min(0.9, depth)),
                mood=mood,
                heat=random.uniform(0.2, 0.8),
                scup=random.uniform(0.3, 0.9)
            )
        elif hasattr(self.dawn_consciousness, 'metrics'):
            # For IntegratedConsciousnessProcessor, update metrics directly
            self.dawn_consciousness.metrics.entropy = max(0.1, min(0.9, entropy))
            self.dawn_consciousness.metrics.coherence = max(0.1, min(0.9, depth))
            self.dawn_consciousness.metrics.heat = random.uniform(0.2, 0.8)
            self.dawn_consciousness.metrics.scup = random.uniform(0.3, 0.9)
    
    def _log_system_stats(self):
        """Log system statistics"""
        
        if self.fragment_integration:
            stats = self.fragment_integration.get_integration_stats()
            
            if stats.get('integration_active'):
                fragment_stats = stats.get('fragment_system_stats', {})
                system_stats = fragment_stats.get('fragment_stats', {})
                
                print(f"📊 System Stats:")
                print(f"   Fragments loaded: {system_stats.get('total_fragments', 0)}")
                print(f"   Integration active: {stats['integration_active']}")
                print(f"   Voice enabled: {fragment_stats.get('voice_enabled', False)}")
                print(f"   Mutation enabled: {fragment_stats.get('mutation_enabled', False)}")
            else:
                print("📊 Fragment integration inactive - using fallback reflection")
        else:
            print("📊 No fragment integration - using standard reflection")
    
    async def shutdown(self):
        """Shutdown all systems"""
        
        logger.info("🔄 Shutting down DAWN Backend...")
        
        if self.fragment_integration:
            self.fragment_integration.shutdown()
        
        self.backend_running = False
        logger.info("✅ DAWN Backend shutdown complete")

async def run_integrated_backend():
    """Run the integrated DAWN backend with fragment speech"""
    
    backend = DAWNBackendWithFragments()
    
    try:
        # Initialize all systems
        await backend.initialize_systems()
        
        # Run consciousness loop
        await backend.run_consciousness_loop()
        
    finally:
        # Ensure clean shutdown
        await backend.shutdown()

def main():
    """Main entry point for integrated backend"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Backend with Fragment Speech Integration")
    parser.add_argument('--mode', choices=['integrated', 'standard'], default='integrated',
                       help='Backend mode (integrated=with fragments, standard=original)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🧠🎤 DAWN Backend with Fragment Speech Integration")
    print("=" * 60)
    
    if args.mode == 'integrated':
        print("🔗 Running with fragment speech integration...")
        asyncio.run(run_integrated_backend())
    else:
        print("📝 Running standard backend...")
        # Fall back to original backend
        dawn_central()

if __name__ == "__main__":
    main() 