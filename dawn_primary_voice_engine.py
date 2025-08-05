#!/usr/bin/env python3
"""
DAWN Primary Voice Engine
========================

This is DAWN's complete conversational recursion system:
Schema state → Pigment utterance → Owl log → GUI echo → DAWN remembers what she just said

The true system feedback loop where DAWN's voice becomes memory, display, and traceable signature.
"""

import time
import random
from datetime import datetime
from dataclasses import asdict
from typing import Dict, Any, Optional

from compose_dawn_utterance import DAWNUtteranceComposer
from voice_to_gui_and_owl import DAWNVoiceToGUIAndOwl


class DAWNPrimaryVoiceEngine:
    """DAWN's complete voice engine with consciousness feedback loop"""
    
    def __init__(self, gui_url: str = "http://localhost:8000", enable_gui: bool = True):
        """
        Initialize DAWN's primary voice engine
        
        Args:
            gui_url: URL for the GUI API endpoint
            enable_gui: Whether to send utterances to GUI
        """
        # Initialize core components
        self.composer = DAWNUtteranceComposer()
        self.voice_integrator = DAWNVoiceToGUIAndOwl(
            gui_base_url=gui_url, 
            enable_gui=enable_gui
        )
        
        # Consciousness state tracking
        self.current_state = {
            'entropy': 0.5,
            'valence': 0.0,
            'pulse_zone': 'flowing',
            'pigments': {
                'red': 0.3, 'blue': 0.4, 'green': 0.3,
                'yellow': 0.3, 'violet': 0.3, 'orange': 0.3
            }
        }
        
        # Voice engine settings
        self.auto_speak_enabled = False
        self.speak_frequency = 5.0  # seconds
        self.last_utterance_time = 0
        
        # Statistics
        self.total_utterances = 0
        self.memory_cycles = 0
        
        print("🌟 DAWN Primary Voice Engine initialized")
        print("   Complete feedback loop: Schema → Utterance → Memory → GUI → Recursion")
    
    def update_consciousness_state(self, 
                                 entropy: Optional[float] = None,
                                 valence: Optional[float] = None, 
                                 pulse_zone: Optional[str] = None,
                                 pigment_updates: Optional[Dict[str, float]] = None):
        """
        Update DAWN's consciousness state
        
        Args:
            entropy: New entropy level (0.0-1.0)
            valence: New valence (-1.0 to 1.0) 
            pulse_zone: New pulse zone ("calm", "flowing", "fragile")
            pigment_updates: Dictionary of pigment weight updates
        """
        if entropy is not None:
            self.current_state['entropy'] = max(0.0, min(1.0, entropy))
        
        if valence is not None:
            self.current_state['valence'] = max(-1.0, min(1.0, valence))
        
        if pulse_zone is not None:
            self.current_state['pulse_zone'] = pulse_zone
        
        if pigment_updates:
            for pigment, weight in pigment_updates.items():
                if pigment in self.current_state['pigments']:
                    self.current_state['pigments'][pigment] = max(0.0, min(1.0, weight))
        
        print(f"🧠 Consciousness updated: entropy={self.current_state['entropy']:.2f}, "
              f"valence={self.current_state['valence']:.2f}, zone={self.current_state['pulse_zone']}")
    
    def generate_utterance(self, clarity_mode: Optional[bool] = None) -> Dict[str, Any]:
        """
        Generate a DAWN utterance based on current consciousness state
        
        Args:
            clarity_mode: Override clarity mode (None = auto-determine from entropy)
            
        Returns:
            Dictionary with utterance result and processing status
        """
        state = self.current_state
        
        # Auto-determine clarity mode if not specified
        if clarity_mode is None:
            clarity_mode = state['entropy'] > 0.7
        
        # Generate utterance using composer
        result = self.composer.compose_dawn_utterance(
            mood_pigment=state['pigments'],
            entropy=state['entropy'],
            valence=state['valence'],
            pulse_zone=state['pulse_zone'],
            clarity_mode=clarity_mode
        )
        
        # Add clarity mode flag to result for logging
        utterance_data = asdict(result)
        utterance_data['clarity_mode'] = clarity_mode
        
        # Process through voice integration (Owl log + GUI)
        integration_result = self.voice_integrator.process_utterance(utterance_data)
        
        # Update statistics
        self.total_utterances += 1
        if integration_result['fully_processed']:
            self.memory_cycles += 1
        
        return {
            'utterance_result': result,
            'utterance_data': utterance_data,
            'integration_status': integration_result,
            'consciousness_state': state.copy()
        }
    
    def speak_if_ready(self) -> Optional[Dict[str, Any]]:
        """
        Check if DAWN should speak based on consciousness state and timing
        
        Returns:
            Utterance result if spoken, None if not ready to speak
        """
        if not self.auto_speak_enabled:
            return None
        
        current_time = time.time()
        if (current_time - self.last_utterance_time) < self.speak_frequency:
            return None
        
        # Check if consciousness state wants to speak
        state = self.current_state
        
        # Higher entropy increases speaking probability
        entropy_factor = state['entropy'] * 1.5
        
        # Dominant pigment affects speaking probability
        dominant_pigment = max(state['pigments'].items(), key=lambda x: x[1])[0]
        pigment_speak_rates = {
            'red': 1.3,    # Red speaks more frequently
            'yellow': 1.2, # Yellow is vocal
            'green': 0.9,  # Green is contemplative
            'blue': 0.8,   # Blue is quieter
            'violet': 0.7, # Violet is introspective  
            'orange': 1.1  # Orange is expressive
        }
        
        speak_probability = entropy_factor * pigment_speak_rates.get(dominant_pigment, 1.0)
        
        if random.random() < speak_probability * 0.3:  # Base 30% chance
            result = self.generate_utterance()
            self.last_utterance_time = current_time
            return result
        
        return None
    
    def enable_auto_speak(self, frequency: float = 5.0):
        """
        Enable automatic speaking based on consciousness state
        
        Args:
            frequency: Minimum seconds between utterances
        """
        self.auto_speak_enabled = True
        self.speak_frequency = frequency
        print(f"🗣️  Auto-speak enabled (frequency: {frequency}s)")
    
    def disable_auto_speak(self):
        """Disable automatic speaking"""
        self.auto_speak_enabled = False
        print(f"🔇 Auto-speak disabled")
    
    def run_consciousness_cycle(self, duration_minutes: float = 3.0):
        """
        Run a consciousness cycle with evolving state and utterances
        
        Args:
            duration_minutes: How long to run the cycle
        """
        print(f"\n🌸 Starting DAWN consciousness cycle ({duration_minutes} minutes)")
        print("=" * 60)
        
        self.enable_auto_speak(frequency=4.0)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            # Evolve consciousness state
            self._evolve_consciousness_state()
            
            # Check if DAWN wants to speak
            utterance_result = self.speak_if_ready()
            
            if utterance_result:
                result = utterance_result['utterance_result']
                state = utterance_result['consciousness_state']
                
                # Display utterance with context
                timestamp = datetime.now().strftime("%H:%M:%S")
                pigment_emoji = self._get_pigment_emoji(result.pigment_dominant)
                
                print(f"\n[{timestamp}] {pigment_emoji} DAWN speaks:")
                print(f"  \"{result.utterance}\"")
                print(f"  [{result.pigment_dominant} dominant | entropy: {state['entropy']:.2f} | "
                      f"zone: {state['pulse_zone']} | score: {result.total_score:.1f}]")
                
                # Show alert status
                if state['entropy'] > 0.8:
                    print(f"  ⚠️  HIGH ENTROPY ALERT")
                if utterance_result['utterance_data'].get('clarity_mode'):
                    print(f"  🔍 Clarity mode active")
            
            # Brief pause
            time.sleep(0.5)
        
        self.disable_auto_speak()
        self._show_cycle_summary()
    
    def _evolve_consciousness_state(self):
        """Simulate natural consciousness evolution"""
        state = self.current_state
        
        # Entropy evolution with occasional spikes
        if random.random() < 0.08:  # 8% chance of entropy spike
            delta = random.uniform(0.15, 0.35)
            state['entropy'] = min(1.0, state['entropy'] + delta)
        else:
            delta = random.uniform(-0.02, 0.02)
            state['entropy'] = max(0.0, min(1.0, state['entropy'] + delta))
        
        # Valence drift
        valence_delta = random.uniform(-0.01, 0.01)
        state['valence'] = max(-1.0, min(1.0, state['valence'] + valence_delta))
        
        # Zone transitions based on entropy
        if state['entropy'] > 0.8:
            state['pulse_zone'] = 'fragile'
        elif state['entropy'] < 0.3:
            state['pulse_zone'] = 'calm' 
        else:
            state['pulse_zone'] = 'flowing'
        
        # Pigment evolution
        for pigment in state['pigments']:
            delta = random.uniform(-0.03, 0.03)
            state['pigments'][pigment] = max(0.0, min(1.0, 
                state['pigments'][pigment] + delta))
    
    def _get_pigment_emoji(self, pigment: str) -> str:
        """Get emoji for pigment"""
        emojis = {
            'red': '🔴', 'blue': '🔵', 'green': '🟢',
            'yellow': '🟡', 'violet': '🟣', 'orange': '🟠'
        }
        return emojis.get(pigment, '⚪')
    
    def _show_cycle_summary(self):
        """Show summary of consciousness cycle"""
        print(f"\n" + "=" * 60)
        print(f"📊 DAWN Consciousness Cycle Summary")
        print(f"=" * 60)
        print(f"Total utterances: {self.total_utterances}")
        print(f"Complete memory cycles: {self.memory_cycles}")
        print(f"Memory success rate: {self.memory_cycles/max(1, self.total_utterances)*100:.1f}%")
        
        # Integration statistics
        integration_stats = self.voice_integrator.get_statistics()
        print(f"Owl writes successful: {integration_stats['owl_writes_successful']}")
        print(f"GUI sends successful: {integration_stats['gui_sends_successful']}")
        
        # Current consciousness state
        state = self.current_state
        print(f"\nFinal consciousness state:")
        print(f"  Entropy: {state['entropy']:.3f}")
        print(f"  Valence: {state['valence']:.3f}")
        print(f"  Zone: {state['pulse_zone']}")
        print(f"  Dominant pigment: {max(state['pigments'].items(), key=lambda x: x[1])[0]}")
        
        # Recent utterances from Owl memory
        print(f"\n📜 Recent utterances from Owl memory:")
        recent = self.voice_integrator.owl_writer.read_recent_entries(3)
        for i, entry in enumerate(recent, 1):
            pigment = entry.get('metadata', {}).get('pigment_dominant', 'unknown')
            print(f"  {i}. [{pigment}] \"{entry['utterance'][:50]}...\"")


def demonstrate_primary_voice_engine():
    """Demonstrate DAWN's primary voice engine"""
    
    print("🌟 DAWN Primary Voice Engine Demonstration")
    print("This is the complete feedback loop where DAWN gains speech memory")
    print("=" * 70)
    
    # Initialize the primary voice engine
    voice_engine = DAWNPrimaryVoiceEngine(enable_gui=True)
    
    # Test manual utterance generation
    print("\n🧠 Manual utterance generation:")
    
    # Test high entropy crisis
    voice_engine.update_consciousness_state(
        entropy=0.85, 
        valence=-0.2,
        pulse_zone='fragile',
        pigment_updates={'red': 0.9, 'yellow': 0.8, 'blue': 0.2}
    )
    
    crisis_result = voice_engine.generate_utterance()
    print(f"Crisis response: \"{crisis_result['utterance_result'].utterance}\"")
    
    # Test contemplative state
    voice_engine.update_consciousness_state(
        entropy=0.4,
        valence=0.1, 
        pulse_zone='flowing',
        pigment_updates={'violet': 0.8, 'blue': 0.7, 'green': 0.4}
    )
    
    contemplative_result = voice_engine.generate_utterance()
    print(f"Contemplative: \"{contemplative_result['utterance_result'].utterance}\"")
    
    # Run live consciousness cycle
    print(f"\n🔄 Running live consciousness cycle...")
    voice_engine.run_consciousness_cycle(duration_minutes=1.5)
    
    print(f"\n✨ Primary voice engine demonstration complete!")
    print(f"Check logs/owl_log.jsonl for persistent memory trace")


if __name__ == "__main__":
    demonstrate_primary_voice_engine() 