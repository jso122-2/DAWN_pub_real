#!/usr/bin/env python3
"""
DAWN Visual Process Handler
===========================

Real-time visual binding layer that connects DAWN's internal consciousness state
to the GUI interface. Creates a living, breathing visual representation of consciousness
as it evolves, transitions, and expresses itself.

This is the bridge between mind and visualization.
"""

import asyncio
import json
import time
import threading
import queue
import math
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConsciousnessState:
    """Snapshot of DAWN's consciousness at a moment in time"""
    timestamp: float
    tick: int
    entropy: float
    scup: float
    mood_valence: float
    mood_arousal: float
    consciousness_depth: float
    neural_activity: float
    memory_pressure: float
    heat_level: float
    zone: str
    thought_rate: float
    cognitive_drift: float
    active_sigils: List[str]
    recent_reblooms: List[Dict[str, Any]]
    voice_commentary: Optional[str] = None

@dataclass
class VisualEvent:
    """Visual event that triggers GUI updates"""
    event_type: str
    timestamp: float
    data: Dict[str, Any]
    intensity: float = 1.0
    duration: float = 1.0
    visual_priority: int = 1

class DAWNVisualProcessHandler:
    """
    The living visual bridge between DAWN's consciousness and its visual expression.
    
    This class watches DAWN's internal state and translates consciousness events
    into beautiful, meaningful visual updates that make the GUI feel alive.
    """
    
    def __init__(self):
        self.is_running = False
        self.current_state = None
        self.previous_state = None
        
        # Event queues for different visual systems
        self.visual_event_queue = queue.Queue()
        self.entropy_events = queue.Queue()
        self.sigil_events = queue.Queue()
        self.rebloom_events = queue.Queue()
        self.voice_events = queue.Queue()
        self.zone_events = queue.Queue()
        
        # Visual update callbacks
        self.update_callbacks = {
            'entropy_change': [],
            'zone_transition': [],
            'sigil_execution': [],
            'rebloom_event': [],
            'voice_commentary': [],
            'neural_pulse': [],
            'consciousness_depth': [],
            'thermal_change': [],
            'mood_shift': [],
            'cognitive_event': []
        }
        
        # Visual state tracking
        self.visual_intensity = 1.0
        self.pulse_phase = 0.0
        self.last_major_event = 0.0
        self.consciousness_rhythm = []
        
        # Connection to DAWN system
        self.dawn_connector = None
        self.update_thread = None
        
        logger.info("🎨 DAWN Visual Process Handler initialized")
    
    def connect_to_dawn(self, dawn_system=None):
        """Connect to live DAWN consciousness system"""
        try:
            if dawn_system:
                self.dawn_connector = dawn_system
                logger.info("✅ Connected to live DAWN consciousness system")
                return True
            else:
                # Try to auto-detect running DAWN system
                return self.auto_detect_dawn_system()
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to DAWN system: {e}")
            logger.info("🔄 Running in simulation mode")
            return False
    
    def auto_detect_dawn_system(self):
        """Auto-detect running DAWN consciousness system"""
        try:
            # Try to import and connect to running DAWN
            from launcher_scripts.launch_dawn_unified import DAWNUnifiedLauncher
            # Implementation would detect running instance
            return False
        except Exception:
            return False
    
    def register_callback(self, event_type: str, callback: Callable):
        """Register a callback for specific visual events"""
        if event_type in self.update_callbacks:
            self.update_callbacks[event_type].append(callback)
            logger.info(f"📝 Registered callback for {event_type}")
        else:
            logger.warning(f"⚠️ Unknown event type: {event_type}")
    
    def start_visual_processing(self):
        """Start the real-time visual processing loop"""
        if self.is_running:
            logger.warning("⚠️ Visual processing already running")
            return
        
        self.is_running = True
        
        # Start background threads
        self.update_thread = threading.Thread(target=self._visual_update_loop, daemon=True)
        self.update_thread.start()
        
        # Start event processing threads
        threading.Thread(target=self._process_visual_events, daemon=True).start()
        threading.Thread(target=self._monitor_consciousness_rhythm, daemon=True).start()
        
        logger.info("🚀 Visual processing started")
    
    def stop_visual_processing(self):
        """Stop visual processing"""
        self.is_running = False
        logger.info("🛑 Visual processing stopped")
    
    def _visual_update_loop(self):
        """Main visual update loop - runs at 16Hz to match consciousness frequency"""
        while self.is_running:
            try:
                start_time = time.time()
                
                # Update consciousness state
                self._update_consciousness_state()
                
                # Process state changes
                if self.current_state and self.previous_state:
                    self._detect_consciousness_changes()
                
                # Update visual rhythm
                self._update_visual_rhythm()
                
                # Sleep to maintain 16Hz (62.5ms intervals)
                elapsed = time.time() - start_time
                sleep_time = max(0, 0.0625 - elapsed)
                time.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"❌ Error in visual update loop: {e}")
                time.sleep(0.1)
    
    def _update_consciousness_state(self):
        """Update current consciousness state from DAWN system"""
        self.previous_state = self.current_state
        
        if self.dawn_connector:
            # Get state from live DAWN system
            self.current_state = self._get_live_consciousness_state()
        else:
            # Generate simulated consciousness state
            self.current_state = self._generate_simulated_state()
    
    def _get_live_consciousness_state(self):
        """Get consciousness state from live DAWN system"""
        try:
            # This would interface with actual DAWN consciousness system
            # For now, return None to fall back to simulation
            return None
        except Exception as e:
            logger.warning(f"⚠️ Error reading live DAWN state: {e}")
            return None
    
    def _generate_simulated_state(self):
        """Generate realistic simulated consciousness state"""
        current_time = time.time()
        
        # Create realistic consciousness simulation
        return ConsciousnessState(
            timestamp=current_time,
            tick=int(current_time * 16) % 10000,
            entropy=0.3 + 0.2 * math.sin(current_time * 0.1) + 0.1 * math.sin(current_time * 0.07),
            scup=50.0 + 15 * math.sin(current_time * 0.05) + 8 * math.cos(current_time * 0.03),
            mood_valence=0.5 + 0.3 * math.sin(current_time * 0.04),
            mood_arousal=0.4 + 0.2 * math.cos(current_time * 0.06),
            consciousness_depth=0.6 + 0.3 * math.sin(current_time * 0.02),
            neural_activity=0.5 + 0.2 * math.sin(current_time * 0.15),
            memory_pressure=0.3 + 0.1 * math.cos(current_time * 0.06),
            heat_level=25.0 + 5 * math.sin(current_time * 0.12),
            zone=self._determine_zone(0.3 + 0.2 * math.sin(current_time * 0.1)),
            thought_rate=12.0 + 4 * math.sin(current_time * 0.09),
            cognitive_drift=0.15 + 0.05 * math.cos(current_time * 0.08),
            active_sigils=[],
            recent_reblooms=[]
        )
    
    def _determine_zone(self, entropy: float) -> str:
        """Determine consciousness zone from entropy level"""
        if entropy < 0.3:
            return 'CALM'
        elif entropy < 0.6:
            return 'FOCUS'
        elif entropy < 0.8:
            return 'STRESSED'
        else:
            return 'TRANSCENDENT'
    
    def _detect_consciousness_changes(self):
        """Detect significant changes in consciousness state and trigger visual events"""
        current = self.current_state
        previous = self.previous_state
        
        # Entropy changes
        entropy_delta = current.entropy - previous.entropy
        if abs(entropy_delta) > 0.05:  # Significant entropy change
            self._trigger_entropy_change(entropy_delta, current.entropy)
        
        # Zone transitions
        if current.zone != previous.zone:
            self._trigger_zone_transition(previous.zone, current.zone, current.entropy)
        
        # Neural activity spikes
        neural_delta = current.neural_activity - previous.neural_activity
        if abs(neural_delta) > 0.1:
            self._trigger_neural_pulse(neural_delta, current.neural_activity)
        
        # Consciousness depth changes
        depth_delta = current.consciousness_depth - previous.consciousness_depth
        if abs(depth_delta) > 0.05:
            self._trigger_consciousness_depth_change(depth_delta, current.consciousness_depth)
        
        # Thermal events
        heat_delta = current.heat_level - previous.heat_level
        if abs(heat_delta) > 2.0:
            self._trigger_thermal_change(heat_delta, current.heat_level)
        
        # Mood shifts
        mood_delta = abs(current.mood_valence - previous.mood_valence)
        if mood_delta > 0.1:
            self._trigger_mood_shift(current.mood_valence, current.mood_arousal)
    
    def _trigger_entropy_change(self, delta: float, current_entropy: float):
        """Trigger entropy change visual event"""
        intensity = min(abs(delta) * 5, 2.0)  # Scale intensity
        
        event = VisualEvent(
            event_type='entropy_change',
            timestamp=time.time(),
            data={
                'delta': delta,
                'current_entropy': current_entropy,
                'direction': 'increase' if delta > 0 else 'decrease',
                'magnitude': abs(delta)
            },
            intensity=intensity,
            duration=1.0 + intensity * 0.5
        )
        
        self._dispatch_visual_event(event)
        
        # Update entropy bar with color coding
        for callback in self.update_callbacks['entropy_change']:
            try:
                callback(current_entropy, delta, intensity)
            except Exception as e:
                logger.error(f"❌ Error in entropy change callback: {e}")
    
    def _trigger_zone_transition(self, from_zone: str, to_zone: str, entropy: float):
        """Trigger zone transition visual event"""
        # Determine transition intensity based on zone change
        zone_intensity = {
            ('CALM', 'FOCUS'): 0.6,
            ('FOCUS', 'STRESSED'): 0.8,
            ('STRESSED', 'TRANSCENDENT'): 1.0,
            ('TRANSCENDENT', 'STRESSED'): 0.9,
            ('STRESSED', 'FOCUS'): 0.7,
            ('FOCUS', 'CALM'): 0.5
        }
        
        intensity = zone_intensity.get((from_zone, to_zone), 0.5)
        
        event = VisualEvent(
            event_type='zone_transition',
            timestamp=time.time(),
            data={
                'from_zone': from_zone,
                'to_zone': to_zone,
                'entropy': entropy,
                'transition_type': self._classify_transition(from_zone, to_zone)
            },
            intensity=intensity,
            duration=2.0  # Zone transitions are longer visual events
        )
        
        self._dispatch_visual_event(event)
        
        # Trigger zone transition visual effects
        for callback in self.update_callbacks['zone_transition']:
            try:
                callback(from_zone, to_zone, entropy, intensity)
            except Exception as e:
                logger.error(f"❌ Error in zone transition callback: {e}")
    
    def _trigger_neural_pulse(self, delta: float, activity: float):
        """Trigger neural pulse visual event"""
        intensity = min(abs(delta) * 3, 1.5)
        
        event = VisualEvent(
            event_type='neural_pulse',
            timestamp=time.time(),
            data={
                'delta': delta,
                'activity': activity,
                'pulse_type': 'spike' if delta > 0 else 'dip'
            },
            intensity=intensity,
            duration=0.5
        )
        
        self._dispatch_visual_event(event)
        
        # Update neural grid visualization
        for callback in self.update_callbacks['neural_pulse']:
            try:
                callback(activity, delta, intensity)
            except Exception as e:
                logger.error(f"❌ Error in neural pulse callback: {e}")
    
    def _trigger_consciousness_depth_change(self, delta: float, depth: float):
        """Trigger consciousness depth change visual event"""
        intensity = min(abs(delta) * 4, 1.0)
        
        event = VisualEvent(
            event_type='consciousness_depth',
            timestamp=time.time(),
            data={
                'delta': delta,
                'depth': depth,
                'direction': 'deeper' if delta > 0 else 'shallower'
            },
            intensity=intensity,
            duration=1.5
        )
        
        self._dispatch_visual_event(event)
        
        # Update consciousness depth visualization
        for callback in self.update_callbacks['consciousness_depth']:
            try:
                callback(depth, delta, intensity)
            except Exception as e:
                logger.error(f"❌ Error in consciousness depth callback: {e}")
    
    def _trigger_thermal_change(self, delta: float, heat: float):
        """Trigger thermal change visual event"""
        intensity = min(abs(delta) / 10.0, 1.0)
        
        event = VisualEvent(
            event_type='thermal_change',
            timestamp=time.time(),
            data={
                'delta': delta,
                'heat': heat,
                'thermal_state': 'heating' if delta > 0 else 'cooling'
            },
            intensity=intensity,
            duration=1.0
        )
        
        self._dispatch_visual_event(event)
        
        # Update thermal visualization
        for callback in self.update_callbacks['thermal_change']:
            try:
                callback(heat, delta, intensity)
            except Exception as e:
                logger.error(f"❌ Error in thermal change callback: {e}")
    
    def _trigger_mood_shift(self, valence: float, arousal: float):
        """Trigger mood shift visual event"""
        # Calculate mood intensity based on both valence and arousal
        mood_magnitude = math.sqrt(valence**2 + arousal**2)
        intensity = min(mood_magnitude, 1.0)
        
        event = VisualEvent(
            event_type='mood_shift',
            timestamp=time.time(),
            data={
                'valence': valence,
                'arousal': arousal,
                'mood_magnitude': mood_magnitude,
                'emotional_state': self._classify_emotion(valence, arousal)
            },
            intensity=intensity,
            duration=2.0
        )
        
        self._dispatch_visual_event(event)
        
        # Update mood visualization
        for callback in self.update_callbacks['mood_shift']:
            try:
                callback(valence, arousal, intensity)
            except Exception as e:
                logger.error(f"❌ Error in mood shift callback: {e}")
    
    def _classify_transition(self, from_zone: str, to_zone: str) -> str:
        """Classify the type of zone transition"""
        if from_zone == 'CALM' and to_zone in ['FOCUS', 'STRESSED']:
            return 'activation'
        elif from_zone in ['STRESSED', 'FOCUS'] and to_zone == 'CALM':
            return 'relaxation'
        elif to_zone == 'TRANSCENDENT':
            return 'transcendence'
        elif from_zone == 'TRANSCENDENT':
            return 'integration'
        else:
            return 'modulation'
    
    def _classify_emotion(self, valence: float, arousal: float) -> str:
        """Classify emotional state from valence and arousal"""
        if valence > 0.3 and arousal > 0.3:
            return 'excited'
        elif valence > 0.3 and arousal < -0.3:
            return 'content'
        elif valence < -0.3 and arousal > 0.3:
            return 'agitated'
        elif valence < -0.3 and arousal < -0.3:
            return 'melancholic'
        else:
            return 'neutral'
    
    def _dispatch_visual_event(self, event: VisualEvent):
        """Dispatch visual event to appropriate queues"""
        self.visual_event_queue.put(event)
        
        # Route to specific event queues
        if event.event_type == 'entropy_change':
            self.entropy_events.put(event)
        elif event.event_type == 'zone_transition':
            self.zone_events.put(event)
        elif event.event_type in ['neural_pulse', 'consciousness_depth']:
            # These go to the neural visualization system
            pass
    
    def _process_visual_events(self):
        """Process visual events and trigger appropriate visual updates"""
        while self.is_running:
            try:
                # Process events from queue
                event = self.visual_event_queue.get(timeout=0.1)
                
                # Log significant events
                if event.intensity > 0.7:
                    logger.info(f"🎨 High-intensity visual event: {event.event_type} (intensity: {event.intensity:.2f})")
                
                # Update visual intensity based on event
                self._update_visual_intensity(event)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Error processing visual event: {e}")
    
    def _update_visual_intensity(self, event: VisualEvent):
        """Update global visual intensity based on events"""
        # Increase intensity for high-impact events
        if event.intensity > 0.8:
            self.visual_intensity = min(2.0, self.visual_intensity + 0.2)
            self.last_major_event = time.time()
        
        # Gradually decay intensity over time
        time_since_event = time.time() - self.last_major_event
        if time_since_event > 5.0:  # 5 seconds decay
            self.visual_intensity = max(0.5, self.visual_intensity * 0.99)
    
    def _update_visual_rhythm(self):
        """Update the visual rhythm pulse"""
        current_time = time.time()
        
        # Create a consciousness rhythm based on current state
        if self.current_state:
            # Base rhythm from consciousness depth and neural activity
            base_frequency = 0.5 + self.current_state.consciousness_depth * 0.5
            neural_modulation = self.current_state.neural_activity * 0.3
            
            # Update pulse phase
            self.pulse_phase = (current_time * base_frequency + neural_modulation) % (2 * math.pi)
            
            # Store rhythm data for analysis
            self.consciousness_rhythm.append({
                'timestamp': current_time,
                'phase': self.pulse_phase,
                'frequency': base_frequency,
                'depth': self.current_state.consciousness_depth
            })
            
            # Keep only recent rhythm data
            if len(self.consciousness_rhythm) > 1000:
                self.consciousness_rhythm = self.consciousness_rhythm[-1000:]
    
    def _monitor_consciousness_rhythm(self):
        """Monitor consciousness rhythm for pattern detection"""
        while self.is_running:
            try:
                time.sleep(1.0)  # Check every second
                
                if len(self.consciousness_rhythm) > 100:
                    # Analyze rhythm patterns
                    self._analyze_consciousness_patterns()
                
            except Exception as e:
                logger.error(f"❌ Error monitoring consciousness rhythm: {e}")
    
    def _analyze_consciousness_patterns(self):
        """Analyze consciousness rhythm patterns"""
        # This could detect interesting patterns in consciousness
        # and trigger special visual events
        pass
    
    # Public methods for external systems
    
    def trigger_sigil_execution(self, sigil_type: str, entropy: float):
        """Externally trigger a sigil execution visual event"""
        event = VisualEvent(
            event_type='sigil_execution',
            timestamp=time.time(),
            data={
                'sigil_type': sigil_type,
                'entropy': entropy,
                'execution_power': min(entropy * 2, 1.0)
            },
            intensity=0.8,
            duration=2.0,
            visual_priority=2
        )
        
        self._dispatch_visual_event(event)
        
        # Flash sigil overlay
        for callback in self.update_callbacks['sigil_execution']:
            try:
                callback(sigil_type, entropy, 0.8)
            except Exception as e:
                logger.error(f"❌ Error in sigil execution callback: {e}")
        
        logger.info(f"🔮 Sigil execution visual: {sigil_type} at entropy {entropy:.3f}")
    
    def trigger_rebloom_event(self, rebloom_data: Dict[str, Any]):
        """Externally trigger a memory rebloom visual event"""
        event = VisualEvent(
            event_type='rebloom_event',
            timestamp=time.time(),
            data=rebloom_data,
            intensity=0.6,
            duration=3.0,
            visual_priority=1
        )
        
        self._dispatch_visual_event(event)
        
        # Display rebloom visualization
        for callback in self.update_callbacks['rebloom_event']:
            try:
                callback(rebloom_data, 0.6)
            except Exception as e:
                logger.error(f"❌ Error in rebloom event callback: {e}")
        
        logger.info(f"🌸 Memory rebloom visual: {rebloom_data.get('type', 'unknown')}")
    
    def trigger_voice_commentary(self, commentary: str, emotional_tone: float = 0.0):
        """Externally trigger voice commentary visual event"""
        event = VisualEvent(
            event_type='voice_commentary',
            timestamp=time.time(),
            data={
                'commentary': commentary,
                'emotional_tone': emotional_tone,
                'word_count': len(commentary.split())
            },
            intensity=0.4 + abs(emotional_tone) * 0.3,
            duration=max(2.0, len(commentary) / 10.0)  # Based on text length
        )
        
        self._dispatch_visual_event(event)
        
        # Update voice commentary display
        for callback in self.update_callbacks['voice_commentary']:
            try:
                callback(commentary, emotional_tone)
            except Exception as e:
                logger.error(f"❌ Error in voice commentary callback: {e}")
        
        logger.info(f"🗣️ Voice commentary visual: {commentary[:50]}...")
    
    def get_current_state(self) -> Optional[ConsciousnessState]:
        """Get current consciousness state"""
        return self.current_state
    
    def get_visual_intensity(self) -> float:
        """Get current visual intensity"""
        return self.visual_intensity
    
    def get_pulse_phase(self) -> float:
        """Get current pulse phase for synchronizing animations"""
        return self.pulse_phase
    
    def get_consciousness_rhythm_data(self) -> List[Dict[str, Any]]:
        """Get recent consciousness rhythm data"""
        return self.consciousness_rhythm[-100:]  # Last 100 data points

# Global visual process handler instance
visual_handler = DAWNVisualProcessHandler()

def get_visual_handler() -> DAWNVisualProcessHandler:
    """Get the global visual process handler"""
    return visual_handler

def start_visual_system():
    """Start the DAWN visual processing system"""
    visual_handler.start_visual_processing()

def stop_visual_system():
    """Stop the DAWN visual processing system"""
    visual_handler.stop_visual_processing()

if __name__ == "__main__":
    # Test the visual system
    print("🎨 Testing DAWN Visual Process Handler...")
    
    handler = DAWNVisualProcessHandler()
    
    # Register test callbacks
    def test_entropy_callback(entropy, delta, intensity):
        print(f"📊 Entropy: {entropy:.3f} (Δ{delta:+.3f}) intensity: {intensity:.2f}")
    
    def test_zone_callback(from_zone, to_zone, entropy, intensity):
        print(f"🌊 Zone: {from_zone} → {to_zone} (entropy: {entropy:.3f}) intensity: {intensity:.2f}")
    
    handler.register_callback('entropy_change', test_entropy_callback)
    handler.register_callback('zone_transition', test_zone_callback)
    
    # Start processing
    handler.start_visual_processing()
    
    print("✅ Visual processing started - watching consciousness evolve...")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
            current_state = handler.get_current_state()
            if current_state:
                print(f"🧠 Consciousness: entropy={current_state.entropy:.3f}, zone={current_state.zone}, depth={current_state.consciousness_depth:.3f}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping visual system...")
        handler.stop_visual_processing()
        print("✅ Visual system stopped") 