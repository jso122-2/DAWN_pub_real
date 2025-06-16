from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from datetime import datetime
import math
from scipy import signal
from scipy.stats import entropy
from collections import deque

class ConsciousnessState:
    def __init__(self, timestamp: Optional[datetime] = None):
        self.timestamp = timestamp or datetime.now()
        self.scup = 0.0  # Subsystem Coherence and Unity Parameter
        self.entropy = 0.0
        self.heat = 0.0
        self.intensity = 0.0
        self.coherence = 0.0
        self.stability = 0.0
        self.focus = 0.0
        self.awareness = 0.0
        self.phase = 0.0
        self.frequency = 0.0
        self.amplitude = 0.0

class ConsciousnessTracer:
    def __init__(self, window_size: int = 1000):
        self.state_history = deque(maxlen=window_size)
        self.last_update = datetime.now()
        self.current_state = ConsciousnessState()
        self.phase_history = deque(maxlen=window_size)
        self.frequency_history = deque(maxlen=window_size)
        self.amplitude_history = deque(maxlen=window_size)
        self.stability_threshold = 0.7
        self.coherence_threshold = 0.6
        self.focus_threshold = 0.5
        self.awareness_threshold = 0.4
        
        # Initialize with default state
        self._update_state({
            'scup': 0.5,
            'entropy': 0.5,
            'heat': 0.3,
            'intensity': 0.5,
            'coherence': 0.5,
            'stability': 0.5,
            'focus': 0.5,
            'awareness': 0.5
        })
    
    def _calculate_phase(self, state: ConsciousnessState) -> float:
        """Calculate consciousness phase using Hilbert transform"""
        if len(self.phase_history) < 2:
            return 0.0
        
        # Use SCUP as the main signal
        signal_data = np.array([s.scup for s in self.state_history])
        analytic_signal = signal.hilbert(signal_data)
        phase = np.unwrap(np.angle(analytic_signal))
        return float(phase[-1] % (2 * np.pi))
    
    def _calculate_frequency(self, state: ConsciousnessState) -> float:
        """Calculate consciousness frequency using FFT"""
        if len(self.frequency_history) < 10:
            return 1.0
        
        # Use SCUP as the main signal
        signal_data = np.array([s.scup for s in self.state_history])
        fft = np.fft.fft(signal_data)
        freqs = np.fft.fftfreq(len(signal_data))
        peak_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
        return float(abs(freqs[peak_idx]))
    
    def _calculate_amplitude(self, state: ConsciousnessState) -> float:
        """Calculate consciousness amplitude"""
        if len(self.amplitude_history) < 2:
            return 1.0
        
        # Use SCUP as the main signal
        signal_data = np.array([s.scup for s in self.state_history])
        return float(np.std(signal_data))
    
    def _calculate_stability(self, state: ConsciousnessState) -> float:
        """Calculate consciousness stability"""
        if len(self.state_history) < 10:
            return 0.5
        
        # Calculate stability based on SCUP variance
        scup_values = np.array([s.scup for s in self.state_history])
        stability = 1.0 - min(1.0, np.std(scup_values))
        return float(stability)
    
    def _calculate_coherence(self, state: ConsciousnessState) -> float:
        """Calculate consciousness coherence"""
        if len(self.state_history) < 10:
            return 0.5
        
        # Calculate coherence between different metrics
        metrics = ['scup', 'entropy', 'heat', 'intensity']
        coherence_matrix = np.zeros((len(metrics), len(metrics)))
        
        for i, metric1 in enumerate(metrics):
            for j, metric2 in enumerate(metrics):
                if i != j:
                    values1 = np.array([getattr(s, metric1) for s in self.state_history])
                    values2 = np.array([getattr(s, metric2) for s in self.state_history])
                    coherence = np.corrcoef(values1, values2)[0, 1]
                    coherence_matrix[i, j] = coherence
        
        return float(np.mean(coherence_matrix))
    
    def _calculate_focus(self, state: ConsciousnessState) -> float:
        """Calculate consciousness focus"""
        if len(self.state_history) < 10:
            return 0.5
        
        # Calculate focus based on entropy and coherence
        entropy_values = np.array([s.entropy for s in self.state_history])
        coherence_values = np.array([s.coherence for s in self.state_history])
        
        focus = (1.0 - np.mean(entropy_values)) * np.mean(coherence_values)
        return float(focus)
    
    def _calculate_awareness(self, state: ConsciousnessState) -> float:
        """Calculate consciousness awareness"""
        if len(self.state_history) < 10:
            return 0.5
        
        # Calculate awareness based on multiple factors
        factors = [
            state.stability,
            state.coherence,
            state.focus,
            1.0 - state.entropy,
            state.intensity
        ]
        
        return float(np.mean(factors))
    
    def _update_state(self, metrics: Dict[str, float]) -> None:
        """Update current consciousness state"""
        # Update basic metrics
        for key, value in metrics.items():
            if hasattr(self.current_state, key):
                setattr(self.current_state, key, value)
        
        # Calculate derived metrics
        self.current_state.phase = self._calculate_phase(self.current_state)
        self.current_state.frequency = self._calculate_frequency(self.current_state)
        self.current_state.amplitude = self._calculate_amplitude(self.current_state)
        self.current_state.stability = self._calculate_stability(self.current_state)
        self.current_state.coherence = self._calculate_coherence(self.current_state)
        self.current_state.focus = self._calculate_focus(self.current_state)
        self.current_state.awareness = self._calculate_awareness(self.current_state)
        
        # Update histories
        self.state_history.append(self.current_state)
        self.phase_history.append(self.current_state.phase)
        self.frequency_history.append(self.current_state.frequency)
        self.amplitude_history.append(self.current_state.amplitude)
        
        self.last_update = datetime.now()
    
    def update_metrics(self, metrics: Dict[str, float]) -> None:
        """Update consciousness metrics"""
        self._update_state(metrics)
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        return {
            'scup': self.current_state.scup,
            'entropy': self.current_state.entropy,
            'heat': self.current_state.heat,
            'intensity': self.current_state.intensity,
            'coherence': self.current_state.coherence,
            'stability': self.current_state.stability,
            'focus': self.current_state.focus,
            'awareness': self.current_state.awareness,
            'phase': self.current_state.phase,
            'frequency': self.current_state.frequency,
            'amplitude': self.current_state.amplitude,
            'timestamp': self.current_state.timestamp.isoformat()
        }
    
    def get_state_history(self) -> List[Dict[str, Any]]:
        """Get consciousness state history"""
        return [{
            'scup': state.scup,
            'entropy': state.entropy,
            'heat': state.heat,
            'intensity': state.intensity,
            'coherence': state.coherence,
            'stability': state.stability,
            'focus': state.focus,
            'awareness': state.awareness,
            'phase': state.phase,
            'frequency': state.frequency,
            'amplitude': state.amplitude,
            'timestamp': state.timestamp.isoformat()
        } for state in self.state_history]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get consciousness tracer metrics"""
        return {
            'current_state': self.get_current_state(),
            'history_length': len(self.state_history),
            'phase_stats': {
                'mean': float(np.mean(self.phase_history)),
                'std': float(np.std(self.phase_history))
            },
            'frequency_stats': {
                'mean': float(np.mean(self.frequency_history)),
                'std': float(np.std(self.frequency_history))
            },
            'amplitude_stats': {
                'mean': float(np.mean(self.amplitude_history)),
                'std': float(np.std(self.amplitude_history))
            },
            'last_update': self.last_update.isoformat()
        }

def create_consciousness_tracer(window_size: int = 1000) -> ConsciousnessTracer:
    """Create and return a new consciousness tracer instance"""
    return ConsciousnessTracer(window_size) 