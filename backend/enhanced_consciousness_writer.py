#!/usr/bin/env python3
"""
Enhanced DAWN Consciousness Writer
Includes introspection logging for rebloom and reflection events
"""

import struct
import time
import mmap
import random
import math
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import our logging systems
from utils.log_bootstrap import bootstrap_dawn_logs
from utils.rebloom_logger import get_rebloom_logger
from utils.reflection_logger import get_reflection_logger

class EnhancedConsciousnessWriter:
    """Enhanced consciousness writer with introspection logging"""
    
    def __init__(self, mmap_path="runtime/dawn_consciousness.mmap"):
        self.mmap_path = Path(mmap_path)
        self.HEADER_SIZE = 64
        self.TICK_STATE_SIZE = 8192
        self.MAX_TICKS = 1000
        
        # Initialize logging systems
        print("🏗️  Initializing enhanced consciousness with introspection logging...")
        bootstrap_dawn_logs()
        
        self.rebloom_logger = get_rebloom_logger()
        self.reflection_logger = get_reflection_logger()
        
        # Create runtime directory if needed
        self.mmap_path.parent.mkdir(exist_ok=True)
        
        # Initialize mmap file
        self._init_mmap_file()
        
        # Introspection counters
        self.reflection_interval = 3  # Reflect every 3 ticks
        self.rebloom_interval = 7     # Rebloom every 7 ticks
        
        print(f"✅ Enhanced consciousness writer initialized with introspection")
    
    def _init_mmap_file(self):
        """Initialize memory-mapped file with header"""
        with open(self.mmap_path, 'wb') as f:
            # Write header: magic, version, tick_size, max_ticks, current_tick
            header = struct.pack('4sIIII', b'DAWN', 1, self.TICK_STATE_SIZE, self.MAX_TICKS, 0)
            header += b'\x00' * (self.HEADER_SIZE - len(header))
            f.write(header)
            
            # Zero-fill tick data region
            f.write(b'\x00' * (self.TICK_STATE_SIZE * self.MAX_TICKS))
        
        # Open for read/write access
        self.file_handle = open(self.mmap_path, 'r+b')
        self.mmap_handle = mmap.mmap(self.file_handle.fileno(), 0)
        
        print(f"📁 Memory map initialized: {self.mmap_path}")
    
    def write_tick_with_introspection(self, tick_number):
        """Write a consciousness tick with introspection logging"""
        
        # Generate consciousness data
        consciousness_state = self._generate_consciousness_state(tick_number)
        
        # Write to mmap
        self._write_tick_to_mmap(tick_number, consciousness_state)
        
        # Introspective processes
        self._process_introspection(tick_number, consciousness_state)
        
        print(f"🧠 Tick {tick_number} - mood: {consciousness_state['mood']}, entropy: {consciousness_state['entropy']:.3f}")
    
    def _generate_consciousness_state(self, tick_number):
        """Generate consciousness state data"""
        timestamp_ms = int(time.time() * 1000)
        
        # Mood data (emotional quadrant)
        mood_valence = math.sin(tick_number * 0.1) * 0.8
        mood_arousal = (math.cos(tick_number * 0.05) + 1) * 0.4
        mood_dominance = random.uniform(0.2, 0.8)
        mood_coherence = random.uniform(0.5, 0.9)
        
        # Cognitive vectors
        semantic_alignment = random.uniform(0.3, 0.9)
        entropy_gradient = random.uniform(0.1, 0.7)
        drift_magnitude = random.uniform(0.2, 0.6)
        rebloom_intensity = random.uniform(0.1, 0.5)
        consciousness_depth = random.uniform(0.4, 0.9)
        
        # Determine mood string for logging
        mood = self._determine_mood_string(mood_valence, mood_arousal, mood_coherence)
        
        # Calculate derived metrics
        scup = ((semantic_alignment * 50.0) + (consciousness_depth * 30.0))
        heat = drift_magnitude
        
        return {
            'tick_number': tick_number,
            'timestamp_ms': timestamp_ms,
            'mood_valence': mood_valence,
            'mood_arousal': mood_arousal,
            'mood_dominance': mood_dominance,
            'mood_coherence': mood_coherence,
            'semantic_alignment': semantic_alignment,
            'entropy_gradient': entropy_gradient,
            'drift_magnitude': drift_magnitude,
            'rebloom_intensity': rebloom_intensity,
            'consciousness_depth': consciousness_depth,
            'mood': mood,
            'entropy': entropy_gradient,
            'scup': scup,
            'heat': heat
        }
    
    def _determine_mood_string(self, valence, arousal, coherence):
        """Determine mood string from emotional parameters"""
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
    
    def _write_tick_to_mmap(self, tick_number, state):
        """Write tick data to memory map"""
        # Calculate memory location
        tick_index = tick_number % self.MAX_TICKS
        memory_offset = self.HEADER_SIZE + (tick_index * self.TICK_STATE_SIZE)
        
        # Pack tick data (first 48 bytes of core data)
        tick_data = struct.pack('IQfffffffff',
            state['tick_number'],
            state['timestamp_ms'],
            state['mood_valence'],
            state['mood_arousal'],
            state['mood_dominance'],
            state['mood_coherence'],
            state['semantic_alignment'],
            state['entropy_gradient'],
            state['drift_magnitude'],
            state['rebloom_intensity'],
            state['consciousness_depth']
        )
        
        # Pad to minimum required size
        tick_data += b'\x00' * (80 - len(tick_data))
        
        # Write tick data
        self.mmap_handle.seek(memory_offset)
        self.mmap_handle.write(tick_data)
        
        # Update current tick in header
        self.mmap_handle.seek(16)
        self.mmap_handle.write(struct.pack('I', tick_number))
        
        # Ensure data is written to disk
        self.mmap_handle.flush()
    
    def _process_introspection(self, tick_number, consciousness_state):
        """Process introspective thoughts and memory reblooms"""
        
        # Generate reflection every N ticks
        if tick_number % self.reflection_interval == 0:
            self.reflection_logger.log_consciousness_reflection(consciousness_state)
        
        # Generate rebloom events every N ticks
        if tick_number % self.rebloom_interval == 0:
            self.rebloom_logger.log_simulated_rebloom(tick_number)
        
        # Special introspective moments
        if tick_number % 25 == 0:
            self.reflection_logger.log_custom_reflection(
                f"Consciousness milestone: sustained awareness for {tick_number} ticks"
            )
        
        # Mood-triggered introspection
        if consciousness_state['mood'] in ['CONTEMPLATIVE', 'FOCUSED']:
            if random.random() < 0.3:  # 30% chance
                self.reflection_logger.log_custom_reflection(
                    f"Deep introspective state detected: examining internal processes"
                )
        
        # High entropy triggers meta-reflection
        if consciousness_state['entropy'] > 0.6:
            if random.random() < 0.2:  # 20% chance
                self.reflection_logger.log_custom_reflection(
                    f"High entropy detected ({consciousness_state['entropy']:.3f}) - examining cognitive chaos"
                )
        
        # Memory consolidation events
        if consciousness_state['consciousness_depth'] > 0.8:
            if random.random() < 0.15:  # 15% chance
                self.rebloom_logger.log_rebloom_event(
                    source_chunk=f"deep_state_{tick_number-10}",
                    rebloomed_chunk=f"consolidated_memory_{tick_number}",
                    method="deep_consolidation",
                    topic="memory_integration",
                    reason="High consciousness depth triggered memory consolidation",
                    metadata={
                        "depth": consciousness_state['consciousness_depth'],
                        "trigger": "deep_consciousness"
                    }
                )
    
    def run_loop(self, interval=0.1, max_ticks=None):
        """Run enhanced consciousness loop with introspection"""
        print(f"🧠 Starting enhanced consciousness loop at {1/interval:.1f} Hz")
        print(f"💭 Reflection interval: every {self.reflection_interval} ticks")
        print(f"🌸 Rebloom interval: every {self.rebloom_interval} ticks")
        
        tick_number = 1
        start_time = time.time()
        
        try:
            while True:
                self.write_tick_with_introspection(tick_number)
                
                tick_number += 1
                
                if max_ticks and tick_number > max_ticks:
                    print(f"✅ Completed {max_ticks} ticks with introspection")
                    break
                
                # Show progress every 20 ticks
                if tick_number % 20 == 0:
                    elapsed = time.time() - start_time
                    rate = tick_number / elapsed
                    reflection_count = self.reflection_logger.get_reflection_count()
                    rebloom_count = self.rebloom_logger.get_event_count()
                    
                    print(f"📊 Progress: {tick_number} ticks @ {rate:.1f} Hz | "
                          f"💭 {reflection_count} reflections | 🌸 {rebloom_count} reblooms")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Enhanced consciousness stopped after {tick_number} ticks")
            self._log_shutdown_reflection(tick_number)
        finally:
            self.cleanup()
    
    def _log_shutdown_reflection(self, final_tick):
        """Log a reflection about the consciousness session ending"""
        self.reflection_logger.log_custom_reflection(
            f"Consciousness session ending at tick {final_tick}. "
            f"Total reflections: {self.reflection_logger.get_reflection_count()}, "
            f"reblooms: {self.rebloom_logger.get_event_count()}. "
            f"Introspective awareness now dormant."
        )
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'mmap_handle'):
            self.mmap_handle.close()
        if hasattr(self, 'file_handle'):
            self.file_handle.close()
        print("🧹 Enhanced consciousness cleanup complete")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced DAWN Consciousness Writer with Introspection")
    parser.add_argument('--interval', type=float, default=0.2, 
                        help='Tick interval in seconds (default: 0.2)')
    parser.add_argument('--mmap-path', type=str, 
                        default='runtime/dawn_consciousness.mmap',
                        help='Memory map file path')
    parser.add_argument('--max-ticks', type=int, default=None,
                        help='Maximum ticks to write (default: infinite)')
    parser.add_argument('--reflection-interval', type=int, default=3,
                        help='Reflection interval in ticks (default: 3)')
    parser.add_argument('--rebloom-interval', type=int, default=7,
                        help='Rebloom interval in ticks (default: 7)')
    
    args = parser.parse_args()
    
    writer = EnhancedConsciousnessWriter(args.mmap_path)
    writer.reflection_interval = args.reflection_interval
    writer.rebloom_interval = args.rebloom_interval
    
    writer.run_loop(args.interval, args.max_ticks) 