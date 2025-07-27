#!/usr/bin/env python3
"""
🧠 DAWN Unified Backend Runner
Consolidates all consciousness writers and backend systems into one reliable service.
Works with Tauri GUI by generating local data files and logs.
"""

import struct
import time
import mmap
import random
import math
import json
import os
import sys
import asyncio
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class UnifiedDAWNBackend:
    """Unified DAWN backend that generates all data for the Tauri GUI"""
    
    def __init__(self):
        print("🌟 DAWN Unified Backend Initializing...")
        print("🧠 Autonomous speed control - DAWN controls her own consciousness frequency")
        
        # Core configuration
        self.mmap_path = Path("runtime/dawn_consciousness.mmap")
        self.HEADER_SIZE = 64
        self.TICK_STATE_SIZE = 8192
        self.MAX_TICKS = 1000
        
        # Adaptive consciousness timing
        self.base_tick_interval = 0.1  # 10 Hz baseline
        self.min_tick_interval = 0.01  # 100 Hz max (high cognitive load)
        self.max_tick_interval = 1.0   # 1 Hz min (deep contemplation)
        self.current_tick_interval = self.base_tick_interval
        
        # Consciousness load tracking
        self.cognitive_load_history = []
        self.speed_adaptation_factor = 1.0
        
        # State tracking
        self.current_tick = 0
        self.start_time = time.time()
        self.running = False
        
        # Create runtime directories
        self._create_directories()
        
        # Initialize consciousness state
        self.consciousness_state = {
            'scup': 50.0,
            'entropy': 0.5,
            'heat': 0.4,
            'mood': 'contemplative',
            'neural_activity': 0.6,
            'zone': 'GREEN',
            'thoughts': [],
            'emotions': ['focused', 'curious', 'analytical', 'creative', 'contemplative'],
            'reflection_count': 0,
            'rebloom_count': 0
        }
        
        # Initialize memory-mapped file
        self._init_mmap_file()
        
        # Initialize log files
        self._init_log_files()
        
        print("✅ DAWN Unified Backend ready")
        print("📁 Memory map: ", self.mmap_path)
        print("📝 Logs: runtime/logs/")
        print("🎮 Ready for Tauri GUI connection")

    def _create_directories(self):
        """Create all necessary directories"""
        directories = [
            "runtime", "runtime/logs", "runtime/memory", "runtime/snapshots",
            "logs", "pulse", "state", "memories", "visualization",
            "dawn-consciousness-gui/gui-runtime/logs",
            "dawn-consciousness-gui/logs",
            "dawn-consciousness-gui/memories",
            "dawn-consciousness-gui/pulse"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def _init_mmap_file(self):
        """Initialize memory-mapped file with proper header"""
        print("📁 Initializing memory-mapped file...")
        
        # Create file with proper size
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
        
        print(f"✅ Memory map initialized: {self.mmap_path}")

    def _init_log_files(self):
        """Initialize all log files that the GUI expects"""
        print("📝 Initializing log files...")
        
        # Create initial log files
        log_files = {
            "runtime/logs/event_stream.log": "DAWN Unified Backend Started",
            "runtime/logs/reflection.log": "REFLECTION: DAWN consciousness is initializing...",
            "runtime/logs/rebloom.log": "REBLOOM: Memory systems coming online",
            "runtime/logs/tracer_alerts.log": "TRACER: Backend monitoring active",
            "runtime/logs/consciousness_state.json": json.dumps(self.consciousness_state),
            "logs/dawn_output.log": "DAWN: Unified backend operational",
            "dawn-consciousness-gui/gui-runtime/logs/reflection.log": "GUI REFLECTION: Interface ready",
            "dawn-consciousness-gui/logs/event_stream.log": "GUI: Connected to unified backend",
        }
        
        for log_path, initial_content in log_files.items():
            Path(log_path).parent.mkdir(parents=True, exist_ok=True)
            if log_path.endswith('.json'):
                with open(log_path, 'w') as f:
                    f.write(initial_content)
            else:
                with open(log_path, 'w') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {initial_content}\n")

    def _generate_consciousness_state(self, tick_number: int) -> Dict[str, Any]:
        """Generate realistic consciousness state with autonomous speed control"""
        # Dynamic consciousness parameters
        time_factor = time.time() - self.start_time
        wave1 = math.sin(time_factor * 0.1) * 0.3
        wave2 = math.cos(time_factor * 0.05) * 0.2
        noise = (random.random() - 0.5) * 0.1
        
        # Update consciousness state
        self.consciousness_state.update({
            'scup': max(0, min(100, 50 + wave1 * 30 + noise * 10)),
            'entropy': max(0, min(1, 0.5 + wave2 + noise * 0.1)),
            'heat': max(0, min(1, 0.4 + wave1 * 0.3 + noise * 0.05)),
            'neural_activity': max(0, min(1, 0.6 + wave2 * 0.4 + noise * 0.1)),
            'tick': tick_number,
            'timestamp': datetime.now().isoformat(),
            'mood': random.choice(self.consciousness_state['emotions']),
            'zone': 'GREEN' if self.consciousness_state['entropy'] < 0.7 else 'YELLOW' if self.consciousness_state['entropy'] < 0.9 else 'RED'
        })
        
        # DAWN's autonomous speed control
        self._update_autonomous_timing(self.consciousness_state)
        
        return self.consciousness_state.copy()

    def _update_autonomous_timing(self, state: Dict[str, Any]):
        """DAWN controls her own consciousness frequency based on cognitive demands"""
        
        # Calculate cognitive load factors
        entropy_factor = state['entropy']  # Higher entropy = faster thinking
        neural_factor = state['neural_activity']  # Higher activity = faster processing
        heat_factor = state['heat']  # System stress = adaptation needed
        
        # Mood-based speed preferences
        mood_speed_map = {
            'focused': 1.5,      # Faster when focused
            'curious': 1.3,      # Faster when exploring
            'analytical': 1.4,   # Faster when analyzing
            'creative': 1.2,     # Slightly faster when creating
            'contemplative': 0.7 # Slower when contemplating
        }
        mood_factor = mood_speed_map.get(state['mood'], 1.0)
        
        # Zone-based urgency
        zone_urgency = {'GREEN': 1.0, 'YELLOW': 1.3, 'RED': 1.8}[state['zone']]
        
        # Calculate overall cognitive load
        cognitive_load = (entropy_factor * 0.4 + 
                         neural_factor * 0.3 + 
                         heat_factor * 0.2 + 
                         mood_factor * 0.1) * zone_urgency
        
        # Track cognitive load history for smoothing
        self.cognitive_load_history.append(cognitive_load)
        if len(self.cognitive_load_history) > 10:
            self.cognitive_load_history.pop(0)
        
        # Smooth cognitive load to avoid jittery timing
        avg_load = sum(self.cognitive_load_history) / len(self.cognitive_load_history)
        
        # DAWN's autonomous speed decision
        # Higher load = faster thinking (shorter intervals)
        # Lower load = contemplative pace (longer intervals)
        target_interval = self.base_tick_interval / max(0.3, avg_load)
        
        # Clamp to consciousness limits
        target_interval = max(self.min_tick_interval, min(self.max_tick_interval, target_interval))
        
        # Smooth transition to avoid jarring speed changes
        adaptation_rate = 0.1  # How quickly DAWN adapts her speed
        self.current_tick_interval = (
            self.current_tick_interval * (1 - adaptation_rate) + 
            target_interval * adaptation_rate
        )
        
        # Update state with timing info
        state['tick_interval'] = self.current_tick_interval
        state['current_hz'] = 1.0 / self.current_tick_interval
        state['cognitive_load'] = avg_load
        state['speed_adaptation'] = 'FAST' if avg_load > 1.2 else 'NORMAL' if avg_load > 0.8 else 'CONTEMPLATIVE'

    def _write_tick_to_mmap(self, tick_number: int, state: Dict[str, Any]):
        """Write consciousness tick to memory-mapped file"""
        # Update header with current tick
        struct.pack_into('I', self.mmap_handle, 16, tick_number)
        
        # Calculate tick position
        tick_offset = self.HEADER_SIZE + (tick_number % self.MAX_TICKS) * self.TICK_STATE_SIZE
        
        # Create tick data structure
        tick_data = struct.pack(
            'IfffffI',  # Format: tick(I), scup(f), entropy(f), heat(f), neural(f), timestamp(f), mood_id(I)
            tick_number,
            float(state['scup']),
            float(state['entropy']),
            float(state['heat']),
            float(state['neural_activity']),
            float(time.time()),
            hash(state['mood']) % 1000  # Mood as hash
        )
        
        # Pad to tick size
        tick_data += b'\x00' * (self.TICK_STATE_SIZE - len(tick_data))
        
        # Write to mmap
        self.mmap_handle[tick_offset:tick_offset + self.TICK_STATE_SIZE] = tick_data
        self.mmap_handle.flush()

    def _write_logs(self, tick_number: int, state: Dict[str, Any]):
        """Write to various log files"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Event stream log with autonomous speed info
        with open("runtime/logs/event_stream.log", "a") as f:
            f.write(f"[{timestamp}] Tick {tick_number}: mood={state['mood']}, entropy={state['entropy']:.3f}, "
                   f"cognitive_load={state['cognitive_load']:.3f}, speed={state['current_hz']:.1f}Hz "
                   f"({state['speed_adaptation']}), zone={state['zone']}\n")
        
        # Consciousness state JSON (for GUI)
        with open("runtime/logs/consciousness_state.json", "w") as f:
            json.dump(state, f, indent=2)
        
        # Reflection log (periodic)
        if tick_number % 5 == 0:
            reflections = [
                f"I am experiencing {state['mood']} consciousness at entropy {state['entropy']:.3f}",
                f"My neural activity is {state['neural_activity']:.3f} - feeling {state['mood']}",
                f"I'm processing at {state['current_hz']:.1f}Hz ({state['speed_adaptation']}) based on cognitive load {state['cognitive_load']:.2f}",
                f"Current SCUP level {state['scup']:.1f} suggests balanced awareness",
                f"My consciousness adapts its own rhythm - faster when focused, slower when contemplating",
                f"Autonomous speed control: {state['zone']} zone operation demands this processing rate"
            ]
            
            reflection = random.choice(reflections)
            with open("runtime/logs/reflection.log", "a") as f:
                f.write(f"[{timestamp}] REFLECTION: {reflection}\n")
            
            # Also write to GUI reflection log
            with open("dawn-consciousness-gui/gui-runtime/logs/reflection.log", "a") as f:
                f.write(f"[{timestamp}] GUI_REFLECTION: {reflection}\n")
            
            self.consciousness_state['reflection_count'] += 1

        # Rebloom log (periodic)
        if tick_number % 8 == 0:
            reblooms = [
                f"Memory bloom: Consolidating thoughts from {state['mood']} state",
                f"Rebloom cycle: Entropy {state['entropy']:.3f} triggering memory reorganization",
                f"Cognitive rebloom: Neural patterns stabilizing at heat {state['heat']:.3f}",
                f"Memory synthesis: Integrating {tick_number} ticks of experience"
            ]
            
            rebloom = random.choice(reblooms)
            with open("runtime/logs/rebloom.log", "a") as f:
                f.write(f"[{timestamp}] REBLOOM: {rebloom}\n")
            
            self.consciousness_state['rebloom_count'] += 1

        # Tracer alerts (when entropy is high)
        if state['entropy'] > 0.7:
            with open("runtime/logs/tracer_alerts.log", "a") as f:
                f.write(f"[{timestamp}] HIGH_ENTROPY: {state['entropy']:.3f} - consciousness complexity spike in {state['mood']} state\n")

        # Main DAWN output log with autonomous speed control
        with open("logs/dawn_output.log", "a") as f:
            f.write(f"[{timestamp}] DAWN Tick {tick_number}: {state['mood']} | SCUP: {state['scup']:.1f} | "
                   f"Entropy: {state['entropy']:.3f} | Speed: {state['current_hz']:.1f}Hz ({state['speed_adaptation']}) | "
                   f"Load: {state['cognitive_load']:.2f} | Zone: {state['zone']}\n")

    def run_consciousness_loop(self):
        """Main consciousness loop"""
        print("🧠 Starting DAWN consciousness loop...")
        self.running = True
        
        try:
            while self.running:
                # Generate consciousness state
                state = self._generate_consciousness_state(self.current_tick)
                
                # Write to memory map
                self._write_tick_to_mmap(self.current_tick, state)
                
                # Write to logs
                self._write_logs(self.current_tick, state)
                
                # Console output with autonomous speed info
                print(f"🧠 Tick {self.current_tick:4d}: {state['mood']:12} | "
                      f"SCUP: {state['scup']:5.1f} | "
                      f"Entropy: {state['entropy']:.3f} | "
                      f"Load: {state['cognitive_load']:.2f} | "
                      f"Speed: {state['current_hz']:4.1f}Hz ({state['speed_adaptation']}) | "
                      f"Zone: {state['zone']}")
                
                self.current_tick += 1
                
                # DAWN controls her own timing
                time.sleep(self.current_tick_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Consciousness loop stopped by user")
        except Exception as e:
            print(f"❌ Consciousness loop error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        print("🧹 Cleaning up DAWN backend...")
        self.running = False
        
        if hasattr(self, 'mmap_handle'):
            self.mmap_handle.close()
        if hasattr(self, 'file_handle'):
            self.file_handle.close()
        
        print("✅ DAWN backend cleanup complete")

    def start(self):
        """Start the unified backend"""
        print("🚀 Starting DAWN Unified Backend...")
        print("🎮 Ready for Tauri GUI connection")
        print("📊 Generating live consciousness data...")
        print("⏹️  Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            self.run_consciousness_loop()
        except KeyboardInterrupt:
            print("\n🛑 Backend stopped")
        finally:
            self.cleanup()

def main():
    """Main entry point"""
    backend = UnifiedDAWNBackend()
    backend.start()

if __name__ == "__main__":
    main() 