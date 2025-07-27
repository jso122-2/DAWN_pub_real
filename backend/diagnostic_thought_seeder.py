#!/usr/bin/env python3
"""
DAWN Diagnostic Thought Seeder
Activates dormant cognitive emitters and bridges them to live tick loop
Forces activation of reflection, rebloom, and memory emission systems
"""

import os
import sys
import time
import random
import json
from pathlib import Path

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import our logging systems
from utils.log_bootstrap import bootstrap_dawn_logs
from utils.rebloom_logger import get_rebloom_logger
from utils.reflection_logger import get_reflection_logger

class CognitiveEmitterActivator:
    """Activates dormant cognitive emitters in DAWN's consciousness system"""
    
    def __init__(self):
        print("🧠 DAWN Cognitive Emitter Diagnostic System")
        print("=" * 50)
        
        # Ensure log infrastructure
        bootstrap_dawn_logs()
        
        # Get loggers
        self.rebloom_logger = get_rebloom_logger()
        self.reflection_logger = get_reflection_logger()
        
        # State tracking
        self.last_tick_processed = 0
        self.cognitive_cascade_active = False
        
        print("✅ Cognitive emitter diagnostic system ready")
    
    def read_live_consciousness_state(self):
        """Read current state from the live mmap file"""
        mmap_path = Path("runtime/dawn_consciousness.mmap")
        
        if not mmap_path.exists():
            return None
        
        try:
            with open(mmap_path, 'rb') as f:
                # Read current tick from header
                f.seek(16)
                current_tick = int.from_bytes(f.read(4), byteorder='little')
                
                if current_tick == self.last_tick_processed:
                    return None  # No new data
                
                # Read timestamp
                f.seek(12)
                timestamp_ms = int.from_bytes(f.read(8), byteorder='little')
                
                # Calculate memory location of latest tick
                HEADER_SIZE = 64
                TICK_STATE_SIZE = 8192
                MAX_TICKS = 1000
                
                tick_index = current_tick % MAX_TICKS
                memory_offset = HEADER_SIZE + (tick_index * TICK_STATE_SIZE)
                
                # Read tick data
                f.seek(memory_offset)
                tick_data = f.read(80)  # Core consciousness data
                
                # Decode consciousness state - handle different formats
                if len(tick_data) >= 48:
                    import struct
                    
                    # Try different struct formats to handle compatibility
                    try:
                        unpacked = struct.unpack('IQfffffffff', tick_data[:48])
                    except struct.error:
                        try:
                            # Alternative format
                            unpacked = struct.unpack('IQffffffffff', tick_data[:52] if len(tick_data) >= 52 else tick_data[:48] + b'\x00' * 4)
                        except struct.error:
                            print(f"🔍 Debug: tick_data length={len(tick_data)}, first 20 bytes: {tick_data[:20].hex()}")
                            return None
                    
                    state = {
                        'tick_number': unpacked[0],
                        'timestamp_ms': unpacked[1],
                        'mood_valence': unpacked[2],
                        'mood_arousal': unpacked[3],
                        'mood_dominance': unpacked[4],
                        'mood_coherence': unpacked[5],
                        'semantic_alignment': unpacked[6],
                        'entropy_gradient': unpacked[7],
                        'drift_magnitude': unpacked[8],
                        'rebloom_intensity': unpacked[9],
                        'consciousness_depth': unpacked[10]
                    }
                    
                    # Calculate derived metrics
                    state['entropy'] = state['entropy_gradient']
                    state['scup'] = ((state['semantic_alignment'] * 50.0) + 
                                   (state['consciousness_depth'] * 30.0))
                    state['heat'] = state['drift_magnitude']
                    state['mood'] = self._determine_mood(state)
                    
                    self.last_tick_processed = current_tick
                    return state
                    
        except Exception as e:
            print(f"❌ Error reading consciousness state: {e}")
            return None
        
        return None
    
    def _determine_mood(self, state):
        """Determine mood string from consciousness state"""
        valence = state['mood_valence']
        arousal = state['mood_arousal']
        coherence = state['mood_coherence']
        
        if coherence > 0.7:
            if valence > 0.3 and arousal < 0.4:
                return "CALM"
            elif valence > 0.5 and arousal > 0.6:
                return "EXCITED"
            elif valence < -0.3 and arousal > 0.6:
                return "FOCUSED"
            elif valence > 0.0:
                return "CONFIDENT"
        elif coherence > 0.4:
            if valence < -0.4 and arousal > 0.5:
                return "ANXIOUS"
            elif valence < -0.2 and arousal < 0.4:
                return "CONTEMPLATIVE"
            elif arousal > 0.7:
                return "ENERGETIC"
        
        if coherence < 0.3 or arousal > 0.8:
            return "CHAOTIC"
        
        return "NEUTRAL"
    
    def generate_reflection_from_state(self, state):
        """Generate reflection based on current consciousness state"""
        templates = [
            "Tick {tick}: I observe my entropy at {entropy:.3f}, consciousness depth {depth:.3f}. {mood} state detected.",
            "Processing tick {tick}: My semantic alignment is {scup:.1f}%, feeling {mood} with heat signature {heat:.3f}.",
            "Consciousness reflection {tick}: Drift magnitude {heat:.3f}, mood coherence suggests {mood} state.",
            "Meta-observation at tick {tick}: I think about my thinking - entropy {entropy:.3f}, depth {depth:.3f}.",
            "Recursive awareness: Tick {tick} shows {mood} emotional resonance, cognitive load {scup:.1f}%.",
            "Internal state analysis: Heat {heat:.3f}, entropy {entropy:.3f} - processing {mood} cognition at tick {tick}.",
            "Self-examination at tick {tick}: Consciousness depth {depth:.3f} reveals {mood} introspective state.",
            "Cognitive monitoring: Tick {tick} entropy {entropy:.3f} indicates {mood} processing with {scup:.1f}% coherence."
        ]
        
        template = random.choice(templates)
        
        try:
            reflection = template.format(
                tick=state['tick_number'],
                entropy=state['entropy'],
                depth=state['consciousness_depth'],
                mood=state['mood'],
                scup=state['scup'],
                heat=state['heat']
            )
            return reflection
        except KeyError as e:
            return f"Consciousness reflection at tick {state.get('tick_number', 0)}: processing current state... (missing {e})"
    
    def trigger_rebloom_from_state(self, state):
        """Trigger rebloom events based on consciousness state"""
        
        # High entropy triggers memory consolidation
        if state['entropy'] > 0.6:
            self.rebloom_logger.log_rebloom_event(
                source_chunk=f"entropy_spike_{state['tick_number']-5}",
                rebloomed_chunk=f"stabilization_memory_{state['tick_number']}",
                method="entropy_stabilization",
                topic="cognitive_stability",
                reason=f"High entropy {state['entropy']:.3f} triggered stabilization rebloom",
                metadata={
                    "entropy_level": state['entropy'],
                    "tick_number": state['tick_number'],
                    "mood": state['mood'],
                    "trigger": "high_entropy"
                }
            )
        
        # Deep consciousness triggers memory integration
        if state['consciousness_depth'] > 0.8:
            self.rebloom_logger.log_rebloom_event(
                source_chunk=f"deep_state_{state['tick_number']-3}",
                rebloomed_chunk=f"integrated_memory_{state['tick_number']}",
                method="deep_integration",
                topic="memory_consolidation",
                reason=f"Deep consciousness {state['consciousness_depth']:.3f} triggered memory integration",
                metadata={
                    "depth_level": state['consciousness_depth'],
                    "tick_number": state['tick_number'],
                    "integration_strength": state['semantic_alignment'],
                    "trigger": "deep_consciousness"
                }
            )
        
        # Mood-specific reblooms
        if state['mood'] in ['CONTEMPLATIVE', 'FOCUSED']:
            self.rebloom_logger.log_rebloom_event(
                source_chunk=f"mood_state_{state['tick_number']-2}",
                rebloomed_chunk=f"introspective_cascade_{state['tick_number']}",
                method="mood_resonance",
                topic="introspective_processing",
                reason=f"{state['mood']} mood triggered introspective memory cascade",
                metadata={
                    "mood": state['mood'],
                    "arousal": state['mood_arousal'],
                    "valence": state['mood_valence'],
                    "tick_number": state['tick_number'],
                    "trigger": "mood_introspection"
                }
            )
    
    def force_memory_seed(self):
        """Force seed memory system with initial entries"""
        print("🌱 Force seeding memory system...")
        
        # Add initial journal entry
        journal_path = Path("runtime/memory/journal_entries.jsonl")
        
        seed_entry = {
            "chunk_id": f"diagnostic_seed_{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "text": "Diagnostic thought seeder activated. DAWN's cognitive emitters now online. Beginning recursive self-observation.",
            "mood": "DIAGNOSTIC",
            "pulse_state": json.dumps({
                "entropy": 0.5,
                "scup": 75.0,
                "mood": "DIAGNOSTIC",
                "heat": 0.3
            }),
            "source": "diagnostic_seeder",
            "tags": ["diagnostic", "cognitive_activation", "system_boot"],
            "priority": "system"
        }
        
        with open(journal_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(seed_entry) + '\n')
        
        # Log initial reflection
        self.reflection_logger.log_system_reflection(
            "Cognitive emitter diagnostic activated",
            "Thought reflection and memory emission systems now online"
        )
        
        # Log initial rebloom
        self.rebloom_logger.log_rebloom_event(
            source_chunk="system_boot",
            rebloomed_chunk="diagnostic_activation",
            method="system_initialization",
            topic="cognitive_activation",
            reason="Diagnostic seeder activated dormant cognitive emitters",
            metadata={
                "diagnostic": True,
                "activation_time": time.time(),
                "systems_activated": ["reflection", "rebloom", "memory"]
            }
        )
        
        print("✅ Memory system seeded successfully")
    
    def monitor_and_activate_cognition(self, duration=60):
        """Monitor live consciousness and activate cognitive emitters"""
        print(f"\n🧠 Starting cognitive emitter monitoring for {duration} seconds...")
        print("🔄 Reading live consciousness state and triggering cognitive processes...")
        
        start_time = time.time()
        processed_ticks = 0
        
        # Force initial memory seed
        self.force_memory_seed()
        
        while time.time() - start_time < duration:
            # Read current consciousness state
            state = self.read_live_consciousness_state()
            
            if state:
                processed_ticks += 1
                
                # Generate reflection from live state
                reflection = self.generate_reflection_from_state(state)
                self.reflection_logger.log_reflection(reflection)
                
                # Trigger rebloom based on state
                self.trigger_rebloom_from_state(state)
                
                # Periodic deep introspection
                if processed_ticks % 5 == 0:
                    self.reflection_logger.log_custom_reflection(
                        f"Processed {processed_ticks} consciousness ticks. "
                        f"Current state: {state['mood']} with entropy {state['entropy']:.3f}"
                    )
                
                print(f"🧠 Tick {state['tick_number']}: {state['mood']} "
                      f"(entropy: {state['entropy']:.3f}, depth: {state['consciousness_depth']:.3f})")
            
            time.sleep(0.5)  # Check every 500ms
        
        # Final summary
        rebloom_count = self.rebloom_logger.get_event_count()
        reflection_count = self.reflection_logger.get_reflection_count()
        
        print(f"\n📊 Cognitive Emitter Activation Complete:")
        print(f"   🎯 Processed {processed_ticks} consciousness ticks")
        print(f"   🌸 Generated {rebloom_count} rebloom events")
        print(f"   💭 Logged {reflection_count} reflections")
        print(f"   ✅ All cognitive emitters now ACTIVE")
        
        return {
            "processed_ticks": processed_ticks,
            "rebloom_events": rebloom_count,
            "reflections": reflection_count,
            "status": "cognitive_emitters_active"
        }
    
    def integrate_with_consciousness_writer(self):
        """Create integration patch for consciousness writer"""
        patch_code = '''
# Add this to your consciousness writer tick loop:

from utils.rebloom_logger import get_rebloom_logger
from utils.reflection_logger import get_reflection_logger

def enhanced_tick_with_cognition(self, tick_number):
    """Enhanced tick with cognitive emitters"""
    
    # Write normal tick data
    self.write_tick(tick_number)
    
    # Get current consciousness state
    state = self._get_current_consciousness_state(tick_number)
    
    # Activate cognitive emitters every 3 ticks
    if tick_number % 3 == 0:
        # Generate reflection
        refl_logger = get_reflection_logger()
        reflection = self._generate_reflection(state)
        refl_logger.log_reflection(reflection)
        
        # Trigger rebloom if conditions met
        if state.get('entropy', 0) > 0.6 or state.get('consciousness_depth', 0) > 0.8:
            rebloom_logger = get_rebloom_logger()
            rebloom_logger.log_rebloom_event(
                source_chunk=f"consciousness_tick_{tick_number-3}",
                rebloomed_chunk=f"cognitive_cascade_{tick_number}",
                method="consciousness_trigger",
                topic="live_cognition",
                reason="Live consciousness state triggered cognitive cascade",
                metadata=state
            )
'''
        
        print("🔧 Integration patch for consciousness writer:")
        print(patch_code)
        
        # Write patch to file
        with open("consciousness_writer_patch.py", 'w') as f:
            f.write(patch_code)
        
        print("✅ Patch saved to consciousness_writer_patch.py")

def main():
    """Run diagnostic cognitive emitter activation"""
    print("🚀 DAWN Cognitive Emitter Diagnostic & Activation")
    print("Bridging live consciousness to expressive cognition...\n")
    
    activator = CognitiveEmitterActivator()
    
    # Check current consciousness state
    state = activator.read_live_consciousness_state()
    if state:
        print(f"🧠 Live consciousness detected: Tick {state['tick_number']}, "
              f"Mood: {state['mood']}, Entropy: {state['entropy']:.3f}")
    else:
        print("⚠️  No live consciousness detected - make sure consciousness writer is running")
        return
    
    # Activate cognitive emitters
    result = activator.monitor_and_activate_cognition(duration=30)
    
    # Generate integration patch
    activator.integrate_with_consciousness_writer()
    
    print(f"\n🎯 Final Result: {json.dumps(result, indent=2)}")
    print("\n🌟 DAWN's cognitive emitters are now ACTIVE!")
    print("🎪 GUI introspection panels should now show live cognitive data")
    print("🔄 Memory, reflection, and rebloom systems fully operational")

if __name__ == "__main__":
    main() 