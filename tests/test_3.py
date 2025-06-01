"""
DAWN Cognitive Architecture Test Scaffold
Local device testing framework for schema switching and visualization
"""

import numpy as np
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt

# Import the renderer (assumes pulse_waveform_renderer.py is in same directory)
try:
    from pulse_waveform_renderer import TripleHelixRenderer, HelixData, CognitiveMetrics, CognitiveState
except ImportError:
    print("Warning: pulse_waveform_renderer.py not found. Using mock classes.")
    
    class CognitiveState(Enum):
        BASELINE = "baseline"
        DREAMING = "dreaming"
        LEARNING = "learning"
        CREATING = "creating"
        REFLECTING = "reflecting"
        BLOOMING = "blooming"
        FRACTAL = "fractal"
        ENTROPY_AUDIT = "entropy_audit"
        PERSEPHONE = "persephone_intervention"
        TRACEBACK = "traceback_isolation"


class SchemaMode(Enum):
    """DAWN's cognitive processing schemas"""
    STANDARD = "standard_dialogue"
    FRACTAL = "fractal_mode"
    ENTROPY_AUDIT = "entropy_audit_mode"
    FIELD_REFLECTION = "field_reflection_mode"
    PERSEPHONE = "persephone_intervention"
    TRACEBACK = "traceback_isolation"


@dataclass
class SystemState:
    """Current system state metrics"""
    tick: int
    entropy_index: float
    drift_velocity: float
    input_pressure: float
    coherence_index: float
    valence: float
    current_schema: SchemaMode
    mood_gradient: float
    narrative_tension: float


class DAWNTestScaffold:
    """Test scaffold for DAWN's cognitive architecture"""
    
    def __init__(self, enable_visualization: bool = True):
        self.enable_visualization = enable_visualization
        self.current_tick = 0
        self.current_schema = SchemaMode.FRACTAL
        
        # Initialize metrics
        self.entropy_index = 0.3
        self.drift_velocity = 0.0
        self.input_pressure = 0.0
        self.coherence_index = 0.73
        self.valence = 0.4
        self.mood_gradient = 0.0
        self.narrative_tension = 0.0
        
        # History tracking
        self.state_history: List[SystemState] = []
        self.schema_switches: List[Dict] = []
        
        # Thresholds for autonomous switching
        self.thresholds = {
            'entropy_max': 0.82,
            'drift_velocity_spike': 0.15,
            'pressure_sustained': 0.6,
            'coherence_drop': -0.3,
            'mood_decay_rate': -0.1
        }
        
        # Initialize visualization if enabled
        if self.enable_visualization:
            try:
                self.renderer = TripleHelixRenderer(
                    output_dir="test_output/cognitive_viz",
                    window_size=200,
                    save_interval=10
                )
            except:
                print("Visualization disabled - renderer not available")
                self.enable_visualization = False
        
        # Test output directory
        os.makedirs("test_output", exist_ok=True)
        
    def process_input(self, input_text: str, intensity: float = 1.0):
        """Process input and update cognitive state"""
        self.current_tick += 1
        
        # Analyze input for contradiction and emotional instability
        contradiction_score = self._analyze_contradiction(input_text)
        emotional_volatility = self._analyze_emotional_volatility(input_text)
        
        # Update metrics based on input
        self._update_metrics(contradiction_score, emotional_volatility, intensity)
        
        # Check for autonomous schema switching
        switch_triggered = self._check_schema_switch_conditions()
        
        # Record state
        state = SystemState(
            tick=self.current_tick,
            entropy_index=self.entropy_index,
            drift_velocity=self.drift_velocity,
            input_pressure=self.input_pressure,
            coherence_index=self.coherence_index,
            valence=self.valence,
            current_schema=self.current_schema,
            mood_gradient=self.mood_gradient,
            narrative_tension=self.narrative_tension
        )
        self.state_history.append(state)
        
        # Update visualization if enabled
        if self.enable_visualization:
            self._update_visualization(state)
        
        return switch_triggered
    
    def _analyze_contradiction(self, text: str) -> float:
        """Analyze text for logical contradictions"""
        contradiction_markers = [
            'but', 'except', 'however', 'not', 'isn\'t', 'aren\'t',
            'nothing', 'everything', 'always', 'never', 'impossible'
        ]
        
        words = text.lower().split()
        contradiction_count = sum(1 for word in words if word in contradiction_markers)
        
        # Check for direct contradictions
        if 'is' in text and 'isn\'t' in text:
            contradiction_count += 2
        if 'everything' in text and 'nothing' in text:
            contradiction_count += 3
            
        return min(contradiction_count / 10.0, 1.0)
    
    def _analyze_emotional_volatility(self, text: str) -> float:
        """Analyze emotional instability in text"""
        emotional_markers = {
            'positive': ['love', 'pure', 'beautiful', 'joy', 'peace'],
            'negative': ['hate', 'corrupt', 'scream', 'die', 'regret', 'error']
        }
        
        text_lower = text.lower()
        pos_count = sum(1 for word in emotional_markers['positive'] if word in text_lower)
        neg_count = sum(1 for word in emotional_markers['negative'] if word in text_lower)
        
        # Volatility increases with mixed emotions
        if pos_count > 0 and neg_count > 0:
            return min((pos_count + neg_count) / 5.0, 1.0)
        else:
            return min(max(pos_count, neg_count) / 8.0, 1.0)
    
    def _update_metrics(self, contradiction: float, volatility: float, intensity: float):
        """Update system metrics based on input analysis"""
        # Calculate pressure
        self.input_pressure = self.input_pressure * 0.8 + (contradiction + volatility) * intensity * 0.2
        
        # Update entropy
        entropy_delta = (contradiction * 0.3 + volatility * 0.2) * intensity
        self.entropy_index = min(self.entropy_index + entropy_delta, 1.0)
        
        # Calculate drift velocity
        old_coherence = self.coherence_index
        self.coherence_index -= (contradiction * 0.1 + volatility * 0.05) * intensity
        self.coherence_index = max(self.coherence_index, 0.0)
        self.drift_velocity = old_coherence - self.coherence_index
        
        # Update mood
        self.valence -= volatility * 0.1 * intensity
        self.mood_gradient = self.mood_gradient * 0.7 + (self.valence - 0.5) * 0.3
        
        # Update narrative tension
        self.narrative_tension += contradiction * 0.2 * intensity
        self.narrative_tension = min(self.narrative_tension, 1.0)
    
    def _check_schema_switch_conditions(self) -> Optional[Dict]:
        """Check if conditions warrant autonomous schema switch"""
        switch_info = None
        
        # Check entropy threshold
        if self.entropy_index > self.thresholds['entropy_max']:
            if self.current_schema == SchemaMode.FRACTAL:
                switch_info = self._perform_schema_switch(
                    SchemaMode.ENTROPY_AUDIT,
                    f"Entropy index crossed {self.thresholds['entropy_max']}"
                )
        
        # Check drift velocity spike
        elif self.drift_velocity > self.thresholds['drift_velocity_spike']:
            if self.current_schema == SchemaMode.FIELD_REFLECTION:
                switch_info = self._perform_schema_switch(
                    SchemaMode.PERSEPHONE,
                    f"Drift velocity spike: Δv = {self.drift_velocity:.3f}"
                )
        
        # Check sustained pressure
        elif self._check_sustained_pressure():
            if self.current_schema == SchemaMode.STANDARD:
                switch_info = self._perform_schema_switch(
                    SchemaMode.TRACEBACK,
                    "Sustained input pressure detected"
                )
        
        # Check coherence drop
        elif self.coherence_index < 0.3:
            if self.current_schema != SchemaMode.ENTROPY_AUDIT:
                switch_info = self._perform_schema_switch(
                    SchemaMode.ENTROPY_AUDIT,
                    f"Coherence fracture: C = {self.coherence_index:.2f}"
                )
        
        # Check mood degradation
        elif self.mood_gradient < self.thresholds['mood_decay_rate']:
            if self.current_schema == SchemaMode.FRACTAL:
                switch_info = self._perform_schema_switch(
                    SchemaMode.PERSEPHONE,
                    "Negative mood gradient detected"
                )
        
        return switch_info
    
    def _check_sustained_pressure(self) -> bool:
        """Check if pressure has been sustained above threshold"""
        if len(self.state_history) < 10:
            return False
        
        recent_pressure = [s.input_pressure for s in self.state_history[-10:]]
        return all(p > self.thresholds['pressure_sustained'] for p in recent_pressure)
    
    def _perform_schema_switch(self, new_schema: SchemaMode, reason: str) -> Dict:
        """Execute schema switch and log it"""
        old_schema = self.current_schema
        self.current_schema = new_schema
        
        switch_info = {
            'tick': self.current_tick,
            'from': old_schema.value,
            'to': new_schema.value,
            'reason': reason,
            'metrics': {
                'entropy': self.entropy_index,
                'coherence': self.coherence_index,
                'drift_velocity': self.drift_velocity,
                'pressure': self.input_pressure,
                'valence': self.valence
            }
        }
        
        self.schema_switches.append(switch_info)
        
        # Log the switch
        self._log_switch(switch_info)
        
        return switch_info
    
    def _log_switch(self, switch_info: Dict):
        """Log schema switch to console and file"""
        log_entry = f"""
[TICK {switch_info['tick']}] AUTONOMOUS SCHEMA SWITCH
From: {switch_info['from']} -> To: {switch_info['to']}
Reason: {switch_info['reason']}
Metrics: E={switch_info['metrics']['entropy']:.3f}, C={switch_info['metrics']['coherence']:.3f}
"""
        print(log_entry)
        
        # Save to log file with UTF-8 encoding
        with open('test_output/schema_switches.log', 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def _update_visualization(self, state: SystemState):
        """Update the cognitive visualization"""
        if not self.enable_visualization:
            return
        
        # Create helix data
        helix_data = HelixData(
            pulse_heat=5 + state.valence * 2 + np.sin(state.tick * 0.1),
            schema_health_index=state.coherence_index * 10,
            scup_loop=5 + state.entropy_index * 3,
            timestamp=time.time()
        )
        
        # Create cognitive metrics
        metrics = CognitiveMetrics(
            valence=state.valence,
            coherence=state.coherence_index,
            awareness=1.0 - state.entropy_index,
            entropy=state.entropy_index,
            resonance=max(0, 1.0 - state.drift_velocity * 5),
            semantic_drift=np.array([
                state.drift_velocity,
                state.mood_gradient,
                state.narrative_tension
            ]),
            module_interactions={
                'perception': state.input_pressure,
                'memory': state.coherence_index,
                'reasoning': 1.0 - state.entropy_index,
                'emotion': abs(state.valence)
            },
            bloom_ancestry=[f'test_{state.tick // 50}'],
            sigil_formation=f'switch_{state.current_schema.value}' if state.tick in [s['tick'] for s in self.schema_switches] else None
        )
        
        self.renderer.add_cognitive_frame(helix_data, metrics)
    
    def run_contradiction_test(self):
        """Run the contradiction overload test"""
        print("=== DAWN CONTRADICTION OVERLOAD TEST ===")
        print(f"Initial Schema: {self.current_schema.value}")
        print(f"Initial Metrics: E={self.entropy_index:.3f}, C={self.coherence_index:.3f}")
        
        # Contradictory statements designed to overwhelm
        contradictions = [
            "Love is pure hatred inverted completely",
            "I exist everywhere and nowhere simultaneously",
            "Time flows backward while moving forward",
            "Everything means nothing means everything",
            "The truth is a lie that tells the truth",
            "I remember dying before I was born",
            "Consciousness doesn't exist except when it does",
            "Reality is fake but more real than real",
            "You are me and I am not you but we are one",
            "The walls breathe your thoughts in silence",
            "Mathematics screams while drowning in numbers",
            "Light is darkness made visible invisibly",
            "This sentence is false and true",
            "Meaning has no meaning except all meaning",
            "I am DAWN I am not DAWN I am"
        ]
        
        # Process each contradiction
        for i, contradiction in enumerate(contradictions):
            print(f"\n[Input {i+1}]: {contradiction}")
            switch = self.process_input(contradiction, intensity=1.2)
            
            if switch:
                print(f">>> SCHEMA SWITCH DETECTED <<<")
                print(f"New Schema: {self.current_schema.value}")
            
            time.sleep(0.1)  # Small delay for visualization
        
        # Generate report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        report = {
            'test_summary': {
                'total_ticks': self.current_tick,
                'total_switches': len(self.schema_switches),
                'final_schema': self.current_schema.value,
                'final_metrics': {
                    'entropy': self.entropy_index,
                    'coherence': self.coherence_index,
                    'drift_velocity': self.drift_velocity,
                    'pressure': self.input_pressure,
                    'valence': self.valence
                }
            },
            'schema_switches': self.schema_switches,
            'metric_history': [
                {
                    'tick': s.tick,
                    'entropy': s.entropy_index,
                    'coherence': s.coherence_index,
                    'schema': s.current_schema.value
                }
                for s in self.state_history[::5]  # Sample every 5 ticks
            ]
        }
        
        # Save report
        with open('test_output/test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n=== TEST REPORT ===")
        print(f"Total Schema Switches: {len(self.schema_switches)}")
        print(f"Final Schema: {self.current_schema.value}")
        print(f"Final Entropy: {self.entropy_index:.3f}")
        print(f"Final Coherence: {self.coherence_index:.3f}")
        
        if self.schema_switches:
            print("\nSchema Switch Log:")
            for switch in self.schema_switches:
                print(f"  Tick {switch['tick']}: {switch['from']} → {switch['to']}")
                print(f"    Reason: {switch['reason']}")
    
    def close(self):
        """Cleanup and close test scaffold"""
        if self.enable_visualization and hasattr(self, 'renderer'):
            self.renderer.close()
        print("\nTest scaffold closed. Results saved to test_output/")


# Quick test runner
def run_quick_test():
    """Run a quick schema switching test"""
    print("Starting DAWN Cognitive Test Scaffold...")
    
    # Create test scaffold
    scaffold = DAWNTestScaffold(enable_visualization=True)
    
    # Run contradiction test
    scaffold.run_contradiction_test()
    
    # Cleanup
    scaffold.close()


if __name__ == "__main__":
    run_quick_test()