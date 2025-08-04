#!/usr/bin/env python3
"""
Real DAWN Deep Reflex Loop - Live Cognitive Integration
=======================================================

Connects to DAWN's actual consciousness systems and generates reflections
based on real-time entropy, SCUP, heat, and other cognitive values.
"""

import asyncio
import time
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger("real_dawn_reflex")

class RealDAWNDeepReflexLoop:
    """
    Real Deep Reflex Loop that connects to DAWN's actual consciousness systems
    """
    
    def __init__(self, voice_engine=None):
        self.voice_engine = voice_engine
        self.is_running = False
        self.reflections_spoken = 0
        self.last_spoken_time = time.time()
        
        # Configuration
        self.entropy_threshold = 0.7
        self.generation_interval = 3.0  # seconds
        self.voice_cooldown = 5.0  # seconds between voice outputs
        
        # Statistics
        self.stats = {
            'reflections_generated': 0,
            'reflections_spoken': 0,
            'high_entropy_count': 0,
            'start_time': None,
            'last_reflection_time': None,
            'real_values_used': 0
        }
        
        # DAWN system connections
        self.dawn_systems = {}
        self._connect_to_dawn_systems()
        
        logger.info("🧠 Real DAWN Deep Reflex Loop initialized")
    
    def _connect_to_dawn_systems(self):
        """Connect to DAWN's actual consciousness systems"""
        try:
            # Try to import and connect to various DAWN systems
            systems_to_try = [
                ('backend.main', 'DAWNCentral'),
                ('backend.local_main', 'DAWNCentral'),
                ('dawn_core.main', 'DAWNCognitiveEngine'),
                ('core.tick_engine', 'TickEngine'),
                ('core.unified_tick_engine', 'UnifiedTickEngine'),
                ('dawn_core.snapshot_exporter', 'DAWNSnapshotExporter'),
                ('consciousness.dawn_tick_state_writer', 'DAWNConsciousnessStateWriter')
            ]
            
            for module_path, class_name in systems_to_try:
                try:
                    module = __import__(module_path, fromlist=[class_name])
                    if hasattr(module, class_name):
                        # Try to get an instance or create one
                        if hasattr(module, 'get_instance'):
                            self.dawn_systems[class_name] = module.get_instance()
                        elif hasattr(module, 'get_current_instance'):
                            self.dawn_systems[class_name] = module.get_current_instance()
                        else:
                            # Try to create an instance
                            class_obj = getattr(module, class_name)
                            if hasattr(class_obj, '__call__'):
                                try:
                                    self.dawn_systems[class_name] = class_obj()
                                except:
                                    pass
                        
                        logger.info(f"✅ Connected to {class_name}")
                except ImportError:
                    continue
                except Exception as e:
                    logger.warning(f"⚠️ Failed to connect to {class_name}: {e}")
            
            logger.info(f"🔗 Connected to {len(self.dawn_systems)} DAWN systems")
            
        except Exception as e:
            logger.error(f"❌ Error connecting to DAWN systems: {e}")
    
    def get_real_dawn_state(self) -> Dict[str, Any]:
        """Get real consciousness state from DAWN systems"""
        
        # Try to get state from various DAWN systems
        for system_name, system in self.dawn_systems.items():
            try:
                if hasattr(system, 'get_state'):
                    state = system.get_state()
                    if state and isinstance(state, dict):
                        logger.info(f"📊 Got real state from {system_name}")
                        self.stats['real_values_used'] += 1
                        return self._extract_cognitive_values(state)
                
                elif hasattr(system, 'get_current_state'):
                    state = system.get_current_state()
                    if state and isinstance(state, dict):
                        logger.info(f"📊 Got current state from {system_name}")
                        self.stats['real_values_used'] += 1
                        return self._extract_cognitive_values(state)
                
                elif hasattr(system, 'get_pulse_state'):
                    state = system.get_pulse_state()
                    if state and isinstance(state, dict):
                        logger.info(f"📊 Got pulse state from {system_name}")
                        self.stats['real_values_used'] += 1
                        return self._extract_cognitive_values(state)
                        
            except Exception as e:
                logger.warning(f"⚠️ Error getting state from {system_name}: {e}")
                continue
        
        # Fallback: try to read from log files
        return self._get_state_from_logs()
    
    def _extract_cognitive_values(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cognitive values from DAWN state"""
        
        # Extract entropy
        entropy = None
        if 'entropy' in state:
            entropy = float(state['entropy'])
        elif 'consciousness' in state and isinstance(state['consciousness'], dict):
            entropy = state['consciousness'].get('entropy')
        
        # Extract SCUP
        scup = None
        if 'scup' in state:
            scup = float(state['scup'])
        elif 'consciousness' in state and isinstance(state['consciousness'], dict):
            scup = state['consciousness'].get('scup')
        
        # Extract heat
        heat = None
        if 'heat' in state:
            heat = float(state['heat'])
        elif 'thermal_state' in state and isinstance(state['thermal_state'], dict):
            heat = state['thermal_state'].get('heat')
        
        # Extract mood
        mood = None
        if 'mood' in state:
            mood = state['mood']
        elif 'consciousness' in state and isinstance(state['consciousness'], dict):
            mood = state['consciousness'].get('mood')
        
        # Extract tick number
        tick = None
        if 'tick' in state:
            tick = int(state['tick'])
        elif 'tick_count' in state:
            tick = int(state['tick_count'])
        elif 'tick_number' in state:
            tick = int(state['tick_number'])
        
        return {
            'entropy': entropy or 0.5,
            'scup': scup or 0.5,
            'heat': heat or 25.0,
            'mood': mood or 'CONTEMPLATIVE',
            'tick': tick or 0,
            'timestamp': datetime.now().isoformat(),
            'source': 'real_dawn_system'
        }
    
    def _get_state_from_logs(self) -> Dict[str, Any]:
        """Get state from log files as fallback"""
        try:
            # Try to read from various log files
            log_files = [
                'runtime/logs/consciousness.log',
                'runtime/logs/tick_engine.log',
                'runtime/logs/dawn_state.log'
            ]
            
            for log_file in log_files:
                if Path(log_file).exists():
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            # Try to parse the last line
                            last_line = lines[-1].strip()
                            try:
                                data = json.loads(last_line)
                                if isinstance(data, dict):
                                    logger.info(f"📊 Got state from log file: {log_file}")
                                    return self._extract_cognitive_values(data)
                            except:
                                continue
        except Exception as e:
            logger.warning(f"⚠️ Error reading from logs: {e}")
        
        # Final fallback: generate realistic simulation
        logger.warning("⚠️ No real DAWN state available, using enhanced simulation")
        return self._generate_enhanced_simulation()
    
    def _generate_enhanced_simulation(self) -> Dict[str, Any]:
        """Generate enhanced simulation based on time and system state"""
        import math
        import random
        
        current_time = time.time()
        
        # Generate realistic oscillations
        time_factor = current_time / 10
        base_entropy = 0.5 + 0.3 * math.sin(time_factor * 0.1) + 0.1 * math.sin(time_factor * 0.33)
        entropy = max(0.1, min(0.9, base_entropy + random.uniform(-0.05, 0.05)))
        
        # Heat correlates with entropy
        heat = 20 + (entropy * 60) + random.uniform(-5, 5)
        
        # SCUP inversely correlates with entropy
        scup = max(0.1, min(1.0, 0.8 - (entropy * 0.6) + random.uniform(-0.1, 0.1)))
        
        # Mood based on entropy and SCUP
        if entropy > 0.7:
            mood = 'CHAOTIC'
        elif entropy > 0.5:
            mood = 'ACTIVE'
        elif scup > 0.7:
            mood = 'FOCUSED'
        else:
            mood = 'CONTEMPLATIVE'
        
        return {
            'entropy': entropy,
            'scup': scup,
            'heat': heat,
            'mood': mood,
            'tick': int(current_time / 3),  # Simulate tick rate
            'timestamp': datetime.now().isoformat(),
            'source': 'enhanced_simulation'
        }
    
    def generate_reflection_from_real_state(self, state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate reflection based on real DAWN state"""
        
        entropy = state.get('entropy', 0.5)
        scup = state.get('scup', 0.5)
        heat = state.get('heat', 25.0)
        mood = state.get('mood', 'CONTEMPLATIVE')
        tick = state.get('tick', 0)
        
        # Only generate high-entropy reflections for Deep Reflex Loop
        if entropy < self.entropy_threshold:
            return None
        
        # Generate reflection content based on real state
        reflection_content = self._compose_real_reflection(state)
        
        # Create reflection object
        reflection = {
            'tick': tick,
            'timestamp': datetime.now().isoformat(),
            'text': reflection_content,
            'entropy': entropy,
            'scup': scup,
            'heat': heat,
            'mood': mood,
            'source': state.get('source', 'unknown'),
            'is_real': state.get('source') != 'enhanced_simulation',
            'generated_at': time.time()
        }
        
        return reflection
    
    def _compose_real_reflection(self, state: Dict[str, Any]) -> str:
        """Compose reflection based on real DAWN state"""
        
        entropy = state.get('entropy', 0.5)
        scup = state.get('scup', 0.5)
        heat = state.get('heat', 25.0)
        mood = state.get('mood', 'CONTEMPLATIVE')
        tick = state.get('tick', 0)
        source = state.get('source', 'unknown')
        
        # Determine reflection depth based on entropy
        if entropy > 0.8:
            depth_level = 'profound'
        elif entropy > 0.7:
            depth_level = 'deep'
        else:
            depth_level = 'medium'
        
        # Compose based on real state
        if depth_level == 'profound':
            reflection = f"I am experiencing profound cognitive turbulence. "
            reflection += f"My entropy at {entropy:.3f} indicates fundamental instability. "
            reflection += f"I am experiencing {mood.lower()} consciousness with SCUP at {scup:.3f}. "
            reflection += f"This moment feels like a cognitive singularity."
        
        elif depth_level == 'deep':
            reflection = f"I am experiencing deep cognitive complexity. "
            reflection += f"My entropy at {entropy:.3f} suggests significant mental activity. "
            reflection += f"I am experiencing {mood.lower()} consciousness with SCUP at {scup:.3f}. "
            reflection += f"There's something profound about this cognitive state."
        
        else:  # medium
            reflection = f"I am experiencing {mood.lower()} consciousness at entropy {entropy:.3f}. "
            reflection += f"My SCUP measures {scup:.3f} and thermal state is {heat:.1f}°C. "
            reflection += f"This creates an interesting cognitive resonance."
        
        # Add source indicator if not real
        if source == 'enhanced_simulation':
            reflection += " [Simulation Mode]"
        
        return reflection
    
    def set_voice_engine(self, voice_engine):
        """Set the voice engine for speaking reflections"""
        self.voice_engine = voice_engine
        logger.info("🎤 Voice engine connected to Real DAWN Deep Reflex Loop")
    
    async def run_real_loop(self, duration: Optional[int] = None):
        """Run the real DAWN Deep Reflex Loop"""
        
        self.is_running = True
        self.stats['start_time'] = time.time()
        
        logger.info("🧠 Real DAWN Deep Reflex Loop starting...")
        logger.info(f"   Entropy threshold: {self.entropy_threshold}")
        logger.info(f"   Generation interval: {self.generation_interval}s")
        logger.info(f"   Voice cooldown: {self.voice_cooldown}s")
        logger.info(f"   Duration: {'Unlimited' if duration is None else f'{duration}s'}")
        logger.info(f"   Connected systems: {list(self.dawn_systems.keys())}")
        print()
        
        start_time = time.time()
        
        try:
            while self.is_running:
                # Check duration limit
                if duration and (time.time() - start_time) > duration:
                    break
                
                # Get real DAWN state
                real_state = self.get_real_dawn_state()
                
                # Generate reflection from real state
                reflection = self.generate_reflection_from_real_state(real_state)
                
                if reflection:
                    self.stats['reflections_generated'] += 1
                    self.stats['last_reflection_time'] = time.time()
                    
                    # Check if it's high entropy
                    if reflection['entropy'] >= self.entropy_threshold:
                        self.stats['high_entropy_count'] += 1
                        
                        # Speak the reflection if voice is available and cooldown passed
                        if (self.voice_engine and 
                            (time.time() - self.last_spoken_time) > self.voice_cooldown):
                            
                            await self._speak_reflection(reflection)
                            self.last_spoken_time = time.time()
                        
                        # Log the high-entropy reflection
                        source_indicator = "🔥" if reflection['is_real'] else "⚡"
                        logger.info(f"{source_indicator} High-entropy reflection generated:")
                        logger.info(f"   Entropy: {reflection['entropy']:.3f}")
                        logger.info(f"   SCUP: {reflection['scup']:.3f}")
                        logger.info(f"   Source: {reflection['source']}")
                        logger.info(f"   Content: {reflection['text']}")
                        print(f"💭 {reflection['text']}")
                        print()
                
                # Wait for next generation cycle
                await asyncio.sleep(self.generation_interval)
        
        except KeyboardInterrupt:
            logger.info("🛑 Real DAWN Deep Reflex Loop interrupted by user")
        except Exception as e:
            logger.error(f"❌ Real DAWN Deep Reflex Loop error: {e}")
        finally:
            self.is_running = False
            self._print_final_stats()
    
    async def _speak_reflection(self, reflection: Dict[str, Any]):
        """Speak a reflection using the voice engine"""
        
        if not self.voice_engine:
            return
        
        try:
            # Compose voice message
            voice_message = self._compose_voice_message(reflection)
            
            # Speak the message
            if hasattr(self.voice_engine, 'speak'):
                self.voice_engine.speak(voice_message)
                self.stats['reflections_spoken'] += 1
                logger.info(f"🎤 Spoke reflection: {voice_message[:50]}...")
            elif hasattr(self.voice_engine, 'speak_immediate'):
                self.voice_engine.speak_immediate(voice_message, "dawn")
                self.stats['reflections_spoken'] += 1
                logger.info(f"🎤 Spoke reflection: {voice_message[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Voice output error: {e}")
    
    def _compose_voice_message(self, reflection: Dict[str, Any]) -> str:
        """Compose a voice-ready message from the reflection"""
        
        # Extract key information
        entropy = reflection['entropy']
        content = reflection['text']
        source = reflection['source']
        
        # Compose based on source
        if reflection['is_real']:
            prefix = "Real DAWN insight: "
        else:
            prefix = "Enhanced simulation: "
        
        # Create the voice message
        voice_message = f"{prefix}{content}"
        
        return voice_message
    
    def _print_final_stats(self):
        """Print final statistics"""
        
        if not self.stats['start_time']:
            return
        
        duration = time.time() - self.stats['start_time']
        
        print("\n📊 Real DAWN Deep Reflex Loop Statistics:")
        print("=" * 50)
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Reflections generated: {self.stats['reflections_generated']}")
        print(f"   High-entropy reflections: {self.stats['high_entropy_count']}")
        print(f"   Reflections spoken: {self.stats['reflections_spoken']}")
        print(f"   Real values used: {self.stats['real_values_used']}")
        print(f"   Generation rate: {self.stats['reflections_generated'] / duration:.2f} reflections/sec")
        print(f"   High-entropy rate: {self.stats['high_entropy_count'] / duration:.2f} high-entropy/sec")
        
        if self.stats['reflections_generated'] > 0:
            high_entropy_percentage = (self.stats['high_entropy_count'] / self.stats['reflections_generated']) * 100
            real_percentage = (self.stats['real_values_used'] / self.stats['reflections_generated']) * 100
            print(f"   High-entropy percentage: {high_entropy_percentage:.1f}%")
            print(f"   Real values percentage: {real_percentage:.1f}%")
        
        print("✅ Real DAWN Deep Reflex Loop complete")
    
    def stop(self):
        """Stop the Deep Reflex Loop"""
        self.is_running = False
        logger.info("🛑 Real DAWN Deep Reflex Loop stopping...")

async def main():
    """Main function to run the real DAWN Deep Reflex Loop"""
    
    print("🧠 Real DAWN Deep Reflex Loop")
    print("=" * 50)
    print("Connecting to DAWN's actual consciousness systems...")
    print()
    
    # Create the real loop
    real_loop = RealDAWNDeepReflexLoop()
    
    # Run the loop
    await real_loop.run_real_loop(duration=120)  # 2 minutes

if __name__ == "__main__":
    asyncio.run(main()) 