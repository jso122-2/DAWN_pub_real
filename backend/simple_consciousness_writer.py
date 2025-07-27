#!/usr/bin/env python3
"""
Simple DAWN Consciousness Writer - Guaranteed to work
Writes test data to mmap file for GUI debugging
"""

import struct
import time
import mmap
import random
import math
from pathlib import Path

class SimpleConsciousnessWriter:
    def __init__(self, mmap_path="runtime/dawn_consciousness.mmap"):
        self.mmap_path = Path(mmap_path)
        self.HEADER_SIZE = 64
        self.TICK_STATE_SIZE = 8192
        self.MAX_TICKS = 1000
        
        # Create runtime directory if needed
        self.mmap_path.parent.mkdir(exist_ok=True)
        
        # Initialize mmap file
        self._init_mmap_file()
        
        print(f"✅ Simple consciousness writer initialized: {self.mmap_path}")
    
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
    
    def write_tick(self, tick_number):
        """Write a single tick to memory"""
        # Generate simulated consciousness data
        timestamp_ms = int(time.time() * 1000)
        
        # Mood data (emotional quadrant)
        mood_valence = math.sin(tick_number * 0.1) * 0.8  # -0.8 to 0.8
        mood_arousal = (math.cos(tick_number * 0.05) + 1) * 0.4  # 0 to 0.8
        mood_dominance = random.uniform(0.2, 0.8)
        mood_coherence = random.uniform(0.5, 0.9)
        
        # Cognitive vectors
        semantic_alignment = random.uniform(0.3, 0.9)
        entropy_gradient = random.uniform(0.1, 0.7)
        drift_magnitude = random.uniform(0.2, 0.6)
        rebloom_intensity = random.uniform(0.1, 0.5)
        consciousness_depth = random.uniform(0.4, 0.9)
        
        # Calculate memory location
        tick_index = tick_number % self.MAX_TICKS
        memory_offset = self.HEADER_SIZE + (tick_index * self.TICK_STATE_SIZE)
        
        # Pack tick data (first 48 bytes of core data)
        tick_data = struct.pack('IQfffffffff',
            tick_number,           # 4 bytes
            timestamp_ms,          # 8 bytes
            mood_valence,          # 4 bytes
            mood_arousal,          # 4 bytes
            mood_dominance,        # 4 bytes
            mood_coherence,        # 4 bytes
            semantic_alignment,    # 4 bytes
            entropy_gradient,      # 4 bytes
            drift_magnitude,       # 4 bytes
            rebloom_intensity,     # 4 bytes
            consciousness_depth    # 4 bytes
        )
        
        # Pad to 80 bytes minimum
        tick_data += b'\x00' * (80 - len(tick_data))
        
        # Write tick data
        self.mmap_handle.seek(memory_offset)
        self.mmap_handle.write(tick_data)
        
        # Update current tick in header
        self.mmap_handle.seek(16)
        self.mmap_handle.write(struct.pack('I', tick_number))
        
        # Ensure data is written to disk
        self.mmap_handle.flush()
        
        print(f"🎯 Tick {tick_number} written - mood: {mood_valence:.2f}, entropy: {entropy_gradient:.2f}")
    
    def run_loop(self, interval=0.1, max_ticks=None):
        """Run consciousness loop"""
        print(f"🔄 Starting consciousness loop at {1/interval:.1f} Hz")
        
        tick_number = 1
        start_time = time.time()
        
        try:
            while True:
                self.write_tick(tick_number)
                
                tick_number += 1
                
                if max_ticks and tick_number > max_ticks:
                    print(f"✅ Completed {max_ticks} ticks")
                    break
                
                # Show progress every 10 ticks
                if tick_number % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = tick_number / elapsed
                    print(f"📊 Progress: {tick_number} ticks, {rate:.1f} Hz")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Stopped after {tick_number} ticks")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'mmap_handle'):
            self.mmap_handle.close()
        if hasattr(self, 'file_handle'):
            self.file_handle.close()
        print("🧹 Cleanup complete")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple DAWN Consciousness Writer")
    parser.add_argument('--interval', type=float, default=0.1, 
                        help='Tick interval in seconds (default: 0.1)')
    parser.add_argument('--mmap-path', type=str, 
                        default='runtime/dawn_consciousness.mmap',
                        help='Memory map file path')
    parser.add_argument('--max-ticks', type=int, default=None,
                        help='Maximum ticks to write (default: infinite)')
    
    args = parser.parse_args()
    
    writer = SimpleConsciousnessWriter(args.mmap_path)
    writer.run_loop(args.interval, args.max_ticks) 