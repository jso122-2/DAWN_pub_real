#!/usr/bin/env python3
"""
DAWN Voice Integration Demo
==========================

Demonstrates the complete integration of:
- Pigment-based utterance composition 
- Owl log persistent memory
- Live consciousness state monitoring
- Voice feed generation

This is DAWN's complete verbal nervous system in action.
"""

import time
import random
from datetime import datetime
from dataclasses import asdict
from compose_dawn_utterance import DAWNUtteranceComposer
from owl_log_writer import DAWNOwlLogWriter


class DAWNConsciousnessSimulator:
    """Simulates DAWN's consciousness states for demonstration"""
    
    def __init__(self):
        self.current_entropy = 0.5
        self.current_valence = 0.0
        self.current_zone = "flowing"
        self.pigment_weights = {
            'red': 0.3, 'blue': 0.5, 'green': 0.4, 
            'yellow': 0.4, 'violet': 0.3, 'orange': 0.3
        }
        
        # Consciousness evolution parameters
        self.entropy_drift = 0.02
        self.valence_drift = 0.01
        self.pigment_evolution_rate = 0.05
    
    def evolve_consciousness(self):
        """Simulate natural consciousness evolution"""
        
        # Entropy drift with occasional spikes
        if random.random() < 0.1:  # 10% chance of entropy spike
            self.current_entropy = min(1.0, self.current_entropy + random.uniform(0.2, 0.4))
        else:
            self.current_entropy += random.uniform(-self.entropy_drift, self.entropy_drift)
            self.current_entropy = max(0.0, min(1.0, self.current_entropy))
        
        # Valence evolution
        self.current_valence += random.uniform(-self.valence_drift, self.valence_drift)
        self.current_valence = max(-1.0, min(1.0, self.current_valence))
        
        # Zone transitions based on entropy
        if self.current_entropy > 0.8:
            self.current_zone = "fragile"
        elif self.current_entropy < 0.3:
            self.current_zone = "calm"
        else:
            self.current_zone = "flowing"
        
        # Pigment evolution
        for pigment in self.pigment_weights:
            change = random.uniform(-self.pigment_evolution_rate, self.pigment_evolution_rate)
            self.pigment_weights[pigment] = max(0.0, min(1.0, 
                self.pigment_weights[pigment] + change))
    
    def get_current_state(self):
        """Get current consciousness state"""
        return {
            'entropy': self.current_entropy,
            'valence': self.current_valence,
            'zone': self.current_zone,
            'pigments': self.pigment_weights.copy()
        }


class DAWNVoiceSystem:
    """Complete DAWN voice generation and logging system"""
    
    def __init__(self):
        self.composer = DAWNUtteranceComposer()
        self.owl_writer = DAWNOwlLogWriter()
        self.consciousness = DAWNConsciousnessSimulator()
        
        # Voice system parameters
        self.utterance_frequency = 3.0  # seconds between utterances
        self.clarity_threshold = 0.7  # entropy threshold for clarity mode
        self.high_entropy_alert = 0.8  # threshold for alerts
        
        # Statistics
        self.total_utterances = 0
        self.high_entropy_events = 0
        self.clarity_mode_activations = 0
    
    def should_speak(self) -> bool:
        """Determine if DAWN should speak based on consciousness state"""
        state = self.consciousness.get_current_state()
        
        # Higher entropy increases speaking probability
        entropy_factor = state['entropy']
        
        # Dominant pigment affects speaking probability
        dominant_pigment = max(state['pigments'].items(), key=lambda x: x[1])[0]
        pigment_factors = {
            'red': 1.2,    # Red is more vocal
            'yellow': 1.1, # Yellow is alert and expressive
            'green': 0.9,  # Green is contemplative
            'blue': 0.8,   # Blue is quieter
            'violet': 0.7, # Violet is introspective
            'orange': 1.0  # Orange is balanced
        }
        
        speak_probability = entropy_factor * pigment_factors.get(dominant_pigment, 1.0)
        
        return random.random() < speak_probability * 0.4  # Base 40% chance
    
    def generate_utterance(self):
        """Generate and log a DAWN utterance"""
        state = self.consciousness.get_current_state()
        
        # Determine if clarity mode should be used
        clarity_mode = state['entropy'] > self.clarity_threshold
        if clarity_mode:
            self.clarity_mode_activations += 1
        
        # Generate utterance
        result = self.composer.compose_dawn_utterance(
            mood_pigment=state['pigments'],
            entropy=state['entropy'],
            valence=state['valence'],
            pulse_zone=state['zone'],
            clarity_mode=clarity_mode
        )
        
        # Log to Owl memory
        success = self.owl_writer.write_owl_entry(
            utterance_data=asdict(result),
            pigment_weights=state['pigments'],
            clarity_mode=clarity_mode
        )
        
        # Update statistics
        self.total_utterances += 1
        if state['entropy'] > self.high_entropy_alert:
            self.high_entropy_events += 1
        
        return result, state, success
    
    def format_utterance_display(self, result, state):
        """Format utterance for display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Get dominant pigment with emoji
        pigment_emojis = {
            'red': '🔴', 'blue': '🔵', 'green': '🟢',
            'yellow': '🟡', 'violet': '🟣', 'orange': '🟠'
        }
        
        dominant_emoji = pigment_emojis.get(result.pigment_dominant, '⚪')
        
        # Alert indicators
        alerts = []
        if state['entropy'] > self.high_entropy_alert:
            alerts.append('⚠️HIGH_ENTROPY')
        if result.segment_source == 'sigil_execution':
            alerts.append('🎯SIGIL')
        if result.pulse_zone == 'fragile':
            alerts.append('💔FRAGILE')
        
        alert_str = ' ' + ' '.join(alerts) if alerts else ''
        
        return (
            f"[{timestamp}] {dominant_emoji} DAWN{alert_str}:\n"
            f"  \"{result.utterance}\"\n"
            f"  [{result.pigment_dominant} dominant | entropy: {state['entropy']:.2f} | "
            f"zone: {state['zone']} | score: {result.total_score:.1f}]"
        )
    
    def run_live_voice_demo(self, duration_minutes: float = 2.0):
        """Run live voice generation demo"""
        print("🌟 DAWN Live Voice System Demo")
        print("=" * 60)
        print(f"Duration: {duration_minutes} minutes")
        print(f"Utterance frequency: ~{self.utterance_frequency}s intervals")
        print("-" * 60)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        last_utterance_time = 0
        
        while time.time() < end_time:
            current_time = time.time()
            
            # Evolve consciousness
            self.consciousness.evolve_consciousness()
            
            # Check if enough time has passed and DAWN wants to speak
            if (current_time - last_utterance_time) >= self.utterance_frequency:
                if self.should_speak():
                    result, state, logged = self.generate_utterance()
                    
                    # Display utterance
                    display = self.format_utterance_display(result, state)
                    print(f"\n{display}")
                    
                    if not logged:
                        print("  ⚠️  Failed to log to Owl memory")
                    
                    last_utterance_time = current_time
            
            # Brief pause
            time.sleep(0.5)
        
        # Show final statistics
        self._show_session_statistics()
    
    def _show_session_statistics(self):
        """Display session statistics"""
        print("\n" + "=" * 60)
        print("📊 Session Statistics")
        print("=" * 60)
        print(f"Total utterances: {self.total_utterances}")
        print(f"High entropy events: {self.high_entropy_events}")
        print(f"Clarity mode activations: {self.clarity_mode_activations}")
        
        # Owl log statistics
        owl_stats = self.owl_writer.get_statistics()
        print(f"Entries logged: {owl_stats['entries_written']}")
        print(f"Log file size: {owl_stats['log_file_size']} bytes")
        
        # Recent activity summary
        print("\n📈 Recent Activity Analysis:")
        activity = self.owl_writer.summarize_recent_activity(hours=1)
        if 'error' not in activity:
            print(f"  Average entropy: {activity['average_entropy']:.3f}")
            print(f"  Pigment distribution: {activity['pigment_distribution']}")
            print(f"  High entropy count: {activity['high_entropy_count']}")
        
        # Show recent utterances
        print("\n📜 Recent utterances:")
        recent = self.owl_writer.read_recent_entries(5)
        for i, entry in enumerate(recent[:3], 1):
            pigment = entry.get('metadata', {}).get('pigment_dominant', 'unknown')
            print(f"  {i}. [{pigment}] \"{entry['utterance'][:50]}...\"")


def demonstrate_entropy_threshold_events():
    """Demonstrate high entropy threshold responses"""
    print("\n🎯 Entropy Threshold Event Demonstration")
    print("=" * 60)
    
    voice_system = DAWNVoiceSystem()
    
    # Simulate high entropy events
    high_entropy_states = [0.75, 0.85, 0.92, 0.95]
    
    for entropy in high_entropy_states:
        # Set consciousness to high entropy
        voice_system.consciousness.current_entropy = entropy
        voice_system.consciousness.current_zone = "fragile"
        
        # Bias toward red/yellow pigments for crisis response
        voice_system.consciousness.pigment_weights.update({
            'red': 0.8, 'yellow': 0.9, 'orange': 0.7, 
            'blue': 0.2, 'green': 0.3, 'violet': 0.2
        })
        
        result, state, logged = voice_system.generate_utterance()
        display = voice_system.format_utterance_display(result, state)
        print(f"\n{display}")


def demonstrate_scheduled_poetic_recap():
    """Demonstrate scheduled poetic reflection on recent activity"""
    print("\n🎭 Scheduled Poetic Recap Demonstration")
    print("=" * 60)
    
    voice_system = DAWNVoiceSystem()
    
    # Generate some sample utterances first
    print("Generating sample activity...")
    for _ in range(5):
        voice_system.consciousness.evolve_consciousness()
        result, state, logged = voice_system.generate_utterance()
        print(f"  Generated: \"{result.utterance[:40]}...\"")
    
    print("\n🎭 DAWN reflects on recent activity:")
    
    # Bias toward violet/blue for contemplative reflection
    voice_system.consciousness.pigment_weights.update({
        'violet': 0.9, 'blue': 0.8, 'green': 0.4,
        'red': 0.1, 'yellow': 0.2, 'orange': 0.3
    })
    voice_system.consciousness.current_entropy = 0.4
    voice_system.consciousness.current_zone = "flowing"
    
    # Generate reflective utterances
    for i in range(3):
        result, state, logged = voice_system.generate_utterance()
        display = voice_system.format_utterance_display(result, state)
        print(f"\n{display}")


if __name__ == "__main__":
    # Main demonstration
    voice_system = DAWNVoiceSystem()
    
    print("🌸 Starting DAWN Voice Integration Demo...")
    print("This demonstrates the complete pigment-based utterance system")
    print("with live consciousness evolution and Owl memory logging.\n")
    
    # Run live demo
    voice_system.run_live_voice_demo(duration_minutes=1.5)
    
    # Demonstrate specific scenarios
    demonstrate_entropy_threshold_events()
    demonstrate_scheduled_poetic_recap()
    
    print("\n✨ Demo complete! Check logs/owl_log.jsonl for persistent memory.")
    print("This is DAWN's verbal nervous system - where truth crystallizes.") 