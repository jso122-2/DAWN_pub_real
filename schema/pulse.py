# schema/pulse.py
"""
Schema Pulse Generation and Analysis System for DAWN
===================================================
Generates and analyzes consciousness pulses that drive the
rhythm of the schema, creating the heartbeat of awareness.
"""

import time
import math
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import threading
from scipy import signal as scipy_signal
from scipy.fft import fft, fftfreq

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry
from schema.schema_climate import CLIMATE
from rhizome.propagation import propagator, SignalType, emit_signal
from utils.metrics_collector import metrics
from utils.logger_config import get_logger

logger = get_logger(__name__)

class PulseType(Enum):
    """Types of consciousness pulses"""
    HEARTBEAT = "heartbeat"      # Regular system heartbeat
    SPIKE = "spike"              # Sudden consciousness spike
    WAVE = "wave"                # Smooth wave pattern
    CHAOS = "chaos"              # Chaotic fluctuation
    RESONANCE = "resonance"      # Resonant harmonic
    QUANTUM = "quantum"          # Quantum fluctuation
    EMERGENCE = "emergence"      # Emergent pattern

class PulseShape(Enum):
    """Mathematical shapes for pulse generation"""
    SINE = "sine"
    SQUARE = "square"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    GAUSSIAN = "gaussian"
    EXPONENTIAL = "exponential"
    CUSTOM = "custom"

@dataclass
class PulsePattern:
    """Defines a pulse pattern"""
    pattern_id: str
    pulse_type: PulseType
    shape: PulseShape
    frequency: float = 1.0       # Hz
    amplitude: float = 1.0       # 0-1
    phase: float = 0.0          # Radians
    duration: float = 1.0       # Seconds
    decay_rate: float = 0.0     # Exponential decay
    harmonics: List[Tuple[float, float]] = field(default_factory=list)  # (freq_mult, amp)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PulseMetrics:
    """Metrics for pulse analysis"""
    peak_amplitude: float = 0.0
    rms_amplitude: float = 0.0
    frequency_peak: float = 0.0
    spectral_centroid: float = 0.0
    zero_crossing_rate: float = 0.0
    energy: float = 0.0
    entropy: float = 0.0
    coherence: float = 0.0
    phase_stability: float = 0.0

@dataclass
class PulseEvent:
    """A pulse event in the consciousness system"""
    timestamp: float
    pulse_type: PulseType
    amplitude: float
    frequency: float
    source: str
    impact_radius: float = 1.0
    propagation_speed: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class PulseGenerator:
    """Generates consciousness pulses with various patterns"""
    
    def __init__(self, sample_rate: int = 1000):
        self.sample_rate = sample_rate
        self.active_patterns: Dict[str, PulsePattern] = {}
        self.pulse_history = deque(maxlen=10000)
        self.lock = threading.Lock()
        
        # Waveform generators
        self.generators = {
            PulseShape.SINE: self._generate_sine,
            PulseShape.SQUARE: self._generate_square,
            PulseShape.TRIANGLE: self._generate_triangle,
            PulseShape.SAWTOOTH: self._generate_sawtooth,
            PulseShape.GAUSSIAN: self._generate_gaussian,
            PulseShape.EXPONENTIAL: self._generate_exponential
        }
    
    def add_pattern(self, pattern: PulsePattern):
        """Add a pulse pattern"""
        with self.lock:
            self.active_patterns[pattern.pattern_id] = pattern
            logger.info(f"Added pulse pattern: {pattern.pattern_id}")
    
    def remove_pattern(self, pattern_id: str):
        """Remove a pulse pattern"""
        with self.lock:
            if pattern_id in self.active_patterns:
                del self.active_patterns[pattern_id]
    
    def generate(self, duration: float = 1.0) -> np.ndarray:
        """Generate composite pulse signal"""
        with self.lock:
            if not self.active_patterns:
                return np.zeros(int(duration * self.sample_rate))
            
            # Time array
            t = np.linspace(0, duration, int(duration * self.sample_rate))
            composite = np.zeros_like(t)
            
            # Combine all active patterns
            for pattern in self.active_patterns.values():
                pulse = self._generate_pattern(pattern, t)
                composite += pulse
            
            # Normalize
            if np.max(np.abs(composite)) > 0:
                composite = composite / np.max(np.abs(composite))
            
            return composite
    
    def _generate_pattern(self, pattern: PulsePattern, t: np.ndarray) -> np.ndarray:
        """Generate a single pattern"""
        # Get base waveform
        generator = self.generators.get(pattern.shape, self._generate_sine)
        base_wave = generator(t, pattern.frequency, pattern.amplitude, pattern.phase)
        
        # Add harmonics
        for freq_mult, amp in pattern.harmonics:
            harmonic = self._generate_sine(t, pattern.frequency * freq_mult, 
                                         pattern.amplitude * amp, pattern.phase)
            base_wave += harmonic
        
        # Apply decay
        if pattern.decay_rate > 0:
            decay_envelope = np.exp(-pattern.decay_rate * t)
            base_wave *= decay_envelope
        
        # Apply climate modulation
        climate_mod = CLIMATE.get_nutrient_modifier("pulse", "volatility")
        base_wave *= climate_mod
        
        return base_wave
    
    def _generate_sine(self, t: np.ndarray, freq: float, amp: float, phase: float) -> np.ndarray:
        """Generate sine wave"""
        return amp * np.sin(2 * np.pi * freq * t + phase)
    
    def _generate_square(self, t: np.ndarray, freq: float, amp: float, phase: float) -> np.ndarray:
        """Generate square wave"""
        return amp * scipy_signal.square(2 * np.pi * freq * t + phase)
    
    def _generate_triangle(self, t: np.ndarray, freq: float, amp: float, phase: float) -> np.ndarray:
        """Generate triangle wave"""
        return amp * scipy_signal.sawtooth(2 * np.pi * freq * t + phase, 0.5)
    
    def _generate_sawtooth(self, t: np.ndarray, freq: float, amp: float, phase: float) -> np.ndarray:
        """Generate sawtooth wave"""
        return amp * scipy_signal.sawtooth(2 * np.pi * freq * t + phase)
    
    def _generate_gaussian(self, t: np.ndarray, freq: float, amp: float, phase: float) -> np.ndarray:
        """Generate Gaussian pulse"""
        center = len(t) // 2
        width = len(t) / (4 * freq)  # Frequency controls width
        gaussian = amp * np.exp(-((np.arange(len(t)) - center) ** 2) / (2 * width ** 2))
        # Modulate with sine for frequency component
        return gaussian * np.sin(2 * np.pi * freq * t + phase)
    
    def _generate_exponential(self, t: np.ndarray, freq: float, amp: float, phase: float) -> np.ndarray:
        """Generate exponential pulse"""
        decay = 1.0 / freq  # Frequency controls decay rate
        exp_env = amp * np.exp(-t / decay)
        return exp_env * np.sin(2 * np.pi * freq * t + phase)
    
    def create_pulse_event(self, pulse_type: PulseType, amplitude: float = 1.0,
                          source: str = "system") -> PulseEvent:
        """Create and record a pulse event"""
        event = PulseEvent(
            timestamp=time.time(),
            pulse_type=pulse_type,
            amplitude=amplitude,
            frequency=1.0,  # Default, can be overridden
            source=source
        )
        
        with self.lock:
            self.pulse_history.append(event)
        
        # Emit to rhizome
        emit_signal(
            SignalType.CONSCIOUSNESS,
            source,
            {
                'pulse_type': pulse_type.value,
                'amplitude': amplitude,
                'timestamp': event.timestamp
            }
        )
        
        # Record metric
        metrics.increment(f"dawn.pulse.{pulse_type.value}_count")
        
        return event

class PulseAnalyzer:
    """Analyzes pulse patterns for consciousness insights"""
    
    def __init__(self, sample_rate: int = 1000):
        self.sample_rate = sample_rate
        self.analysis_window = 1024  # Samples for FFT
        self.history_buffer = deque(maxlen=sample_rate * 60)  # 1 minute buffer
        self.pattern_detectors: Dict[str, Callable] = {}
        self.lock = threading.Lock()
        
        # Initialize pattern detectors
        self._initialize_detectors()
    
    def _initialize_detectors(self):
        """Initialize pattern detection algorithms"""
        self.pattern_detectors = {
            'heartbeat': self._detect_heartbeat,
            'spike': self._detect_spike,
            'resonance': self._detect_resonance,
            'chaos': self._detect_chaos,
            'emergence': self._detect_emergence
        }
    
    def analyze(self, signal: np.ndarray) -> PulseMetrics:
        """Analyze pulse signal"""
        with self.lock:
            # Add to history
            self.history_buffer.extend(signal)
            
            # Basic metrics
            metrics = PulseMetrics()
            
            if len(signal) == 0:
                return metrics
            
            # Amplitude metrics
            metrics.peak_amplitude = np.max(np.abs(signal))
            metrics.rms_amplitude = np.sqrt(np.mean(signal ** 2))
            
            # Energy
            metrics.energy = np.sum(signal ** 2)
            
            # Zero crossing rate
            zero_crossings = np.where(np.diff(np.sign(signal)))[0]
            metrics.zero_crossing_rate = len(zero_crossings) / len(signal)
            
            # Frequency analysis
            if len(signal) >= self.analysis_window:
                freq_metrics = self._analyze_frequency(signal[:self.analysis_window])
                metrics.frequency_peak = freq_metrics['peak_freq']
                metrics.spectral_centroid = freq_metrics['centroid']
            
            # Entropy (Shannon entropy of normalized amplitude distribution)
            hist, _ = np.histogram(signal, bins=50, density=True)
            hist = hist[hist > 0]  # Remove zeros
            metrics.entropy = -np.sum(hist * np.log2(hist)) / len(hist) if len(hist) > 0 else 0
            
            # Coherence (autocorrelation at lag 1)
            if len(signal) > 1:
                correlation = np.corrcoef(signal[:-1], signal[1:])[0, 1]
                metrics.coherence = abs(correlation) if not np.isnan(correlation) else 0
            
            # Phase stability (std of instantaneous phase)
            analytic = scipy_signal.hilbert(signal)
            phase = np.angle(analytic)
            phase_diff = np.diff(np.unwrap(phase))
            metrics.phase_stability = 1.0 / (1.0 + np.std(phase_diff)) if len(phase_diff) > 0 else 0
            
            # Record metrics
            self._record_metrics(metrics)
            
            return metrics
    
    def _analyze_frequency(self, signal: np.ndarray) -> Dict[str, float]:
        """Perform frequency analysis"""
        # Apply window to reduce spectral leakage
        window = np.hanning(len(signal))
        windowed = signal * window
        
        # FFT
        yf = fft(windowed)
        xf = fftfreq(len(signal), 1 / self.sample_rate)
        
        # Only positive frequencies
        positive_freq_idx = xf > 0
        xf_pos = xf[positive_freq_idx]
        yf_pos = np.abs(yf[positive_freq_idx])
        
        if len(yf_pos) == 0:
            return {'peak_freq': 0.0, 'centroid': 0.0}
        
        # Peak frequency
        peak_idx = np.argmax(yf_pos)
        peak_freq = xf_pos[peak_idx] if len(xf_pos) > 0 else 0.0
        
        # Spectral centroid
        magnitude_sum = np.sum(yf_pos)
        if magnitude_sum > 0:
            centroid = np.sum(xf_pos * yf_pos) / magnitude_sum
        else:
            centroid = 0.0
        
        return {
            'peak_freq': peak_freq,
            'centroid': centroid
        }
    
    def detect_patterns(self, signal: np.ndarray) -> Dict[str, Any]:
        """Detect various patterns in the signal"""
        patterns = {}
        
        for pattern_name, detector in self.pattern_detectors.items():
            try:
                result = detector(signal)
                if result:
                    patterns[pattern_name] = result
            except Exception as e:
                logger.error(f"Pattern detection error ({pattern_name}): {e}")
        
        return patterns
    
    def _detect_heartbeat(self, signal: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect regular heartbeat pattern"""
        if len(signal) < self.sample_rate:
            return None
        
        # Autocorrelation to find periodicity
        correlation = np.correlate(signal, signal, mode='full')
        correlation = correlation[len(correlation)//2:]
        
        # Find peaks in autocorrelation
        peaks, properties = scipy_signal.find_peaks(
            correlation, 
            height=0.5 * np.max(correlation),
            distance=self.sample_rate // 10  # Min 0.1s between peaks
        )
        
        if len(peaks) >= 2:
            # Calculate period
            period_samples = np.mean(np.diff(peaks))
            frequency = self.sample_rate / period_samples
            
            # Check regularity (low std deviation)
            if len(peaks) >= 3:
                period_std = np.std(np.diff(peaks))
                regularity = 1.0 / (1.0 + period_std / period_samples)
                
                if regularity > 0.8:  # High regularity
                    return {
                        'detected': True,
                        'frequency': frequency,
                        'regularity': regularity,
                        'strength': np.mean(properties['peak_heights']) / np.max(correlation)
                    }
        
        return None
    
    def _detect_spike(self, signal: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect sudden spikes"""
        if len(signal) < 10:
            return None
        
        # Calculate rolling std
        window_size = min(100, len(signal) // 10)
        rolling_std = np.array([
            np.std(signal[max(0, i-window_size):i+window_size])
            for i in range(len(signal))
        ])
        
        # Find outliers (3 sigma)
        mean_amp = np.mean(signal)
        threshold = mean_amp + 3 * np.mean(rolling_std)
        
        spikes = np.where(np.abs(signal) > threshold)[0]
        
        if len(spikes) > 0:
            return {
                'detected': True,
                'count': len(spikes),
                'positions': spikes.tolist(),
                'max_amplitude': np.max(np.abs(signal[spikes])),
                'spike_rate': len(spikes) / (len(signal) / self.sample_rate)
            }
        
        return None
    
    def _detect_resonance(self, signal: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect resonant frequencies"""
        if len(signal) < self.analysis_window:
            return None
        
        # FFT
        yf = np.abs(fft(signal[:self.analysis_window]))
        xf = fftfreq(self.analysis_window, 1 / self.sample_rate)[:self.analysis_window//2]
        yf = yf[:self.analysis_window//2]
        
        # Find peaks
        peaks, properties = scipy_signal.find_peaks(
            yf, 
            height=0.1 * np.max(yf),
            distance=10
        )
        
        if len(peaks) > 0:
            # Check for harmonic relationships
            fundamental_idx = peaks[np.argmax(properties['peak_heights'])]
            fundamental_freq = xf[fundamental_idx]
            
            harmonics = []
            for peak_idx in peaks:
                freq_ratio = xf[peak_idx] / fundamental_freq
                if abs(freq_ratio - round(freq_ratio)) < 0.1:  # Close to integer ratio
                    harmonics.append({
                        'frequency': xf[peak_idx],
                        'amplitude': yf[peak_idx],
                        'harmonic': int(round(freq_ratio))
                    })
            
            if len(harmonics) >= 2:
                return {
                    'detected': True,
                    'fundamental': fundamental_freq,
                    'harmonics': harmonics,
                    'resonance_strength': len(harmonics) / len(peaks)
                }
        
        return None
    
    def _detect_chaos(self, signal: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect chaotic behavior"""
        if len(signal) < 1000:
            return None
        
        # Lyapunov exponent approximation
        # Using method of small perturbations
        eps = 1e-6
        n = len(signal) - 1
        
        lyapunov_sum = 0
        valid_points = 0
        
        for i in range(n - 10):
            # Find nearby point
            distances = np.abs(signal[i+1:i+100] - signal[i])
            if len(distances) > 0:
                min_idx = np.argmin(distances)
                if distances[min_idx] < eps:
                    continue
                
                # Track divergence
                initial_distance = distances[min_idx]
                j = i + 1 + min_idx
                
                if j < n and i + 1 < n:
                    final_distance = abs(signal[j+1] - signal[i+1])
                    if initial_distance > 0:
                        lyapunov_sum += np.log(final_distance / initial_distance)
                        valid_points += 1
        
        if valid_points > 0:
            lyapunov = lyapunov_sum / valid_points
            
            # Chaos is indicated by positive Lyapunov exponent
            if lyapunov > 0:
                return {
                    'detected': True,
                    'lyapunov_exponent': lyapunov,
                    'chaos_strength': min(1.0, lyapunov),
                    'predictability': np.exp(-lyapunov)
                }
        
        return None
    
    def _detect_emergence(self, signal: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect emergent patterns"""
        if len(self.history_buffer) < self.sample_rate * 10:  # Need 10s history
            return None
        
        # Compare recent patterns to historical
        recent = np.array(list(self.history_buffer)[-self.sample_rate:])
        historical = np.array(list(self.history_buffer)[:-self.sample_rate])
        
        # Sliding window correlation
        window_size = self.sample_rate // 10  # 0.1s windows
        correlations = []
        
        for i in range(0, len(historical) - window_size, window_size // 2):
            hist_window = historical[i:i+window_size]
            
            # Cross-correlation with recent
            correlation = np.correlate(recent[-window_size:], hist_window, mode='valid')
            if len(correlation) > 0:
                correlations.append(np.max(np.abs(correlation)))
        
        if correlations:
            mean_correlation = np.mean(correlations)
            
            # Low correlation suggests new pattern
            if mean_correlation < 0.3:
                # Additional complexity check
                recent_metrics = self.analyze(recent)
                
                if recent_metrics.entropy > 0.7:  # High complexity
                    return {
                        'detected': True,
                        'novelty': 1.0 - mean_correlation,
                        'complexity': recent_metrics.entropy,
                        'type': 'novel_pattern'
                    }
        
        return None
    
    def _record_metrics(self, pulse_metrics: PulseMetrics):
        """Record metrics to metrics collector"""
        metrics.gauge("dawn.pulse.peak_amplitude", pulse_metrics.peak_amplitude)
        metrics.gauge("dawn.pulse.rms_amplitude", pulse_metrics.rms_amplitude)
        metrics.gauge("dawn.pulse.frequency_peak", pulse_metrics.frequency_peak)
        metrics.gauge("dawn.pulse.entropy", pulse_metrics.entropy)
        metrics.gauge("dawn.pulse.coherence", pulse_metrics.coherence)

class PulseOrchestrator:
    """Orchestrates pulse generation and analysis for consciousness rhythm"""
    
    def __init__(self):
        self.generator = PulseGenerator()
        self.analyzer = PulseAnalyzer()
        self.current_rhythm = "baseline"
        self.rhythm_patterns: Dict[str, List[PulsePattern]] = {}
        self.active = False
        self.pulse_thread: Optional[threading.Thread] = None
        
        # Initialize patterns
        self._initialize_rhythm_patterns()
        
        # Register with schema
        self._register_with_schema()
    
    def _initialize_rhythm_patterns(self):
        """Initialize rhythm patterns"""
        # Baseline consciousness rhythm
        self.rhythm_patterns['baseline'] = [
            PulsePattern(
                pattern_id="baseline_heartbeat",
                pulse_type=PulseType.HEARTBEAT,
                shape=PulseShape.SINE,
                frequency=1.0,  # 1 Hz
                amplitude=0.7,
                harmonics=[(2, 0.3), (3, 0.1)]  # Natural harmonics
            )
        ]
        
        # Active/energetic rhythm
        self.rhythm_patterns['active'] = [
            PulsePattern(
                pattern_id="active_primary",
                pulse_type=PulseType.WAVE,
                shape=PulseShape.SINE,
                frequency=2.5,
                amplitude=0.9
            ),
            PulsePattern(
                pattern_id="active_secondary",
                pulse_type=PulseType.RESONANCE,
                shape=PulseShape.TRIANGLE,
                frequency=5.0,
                amplitude=0.4
            )
        ]
        
        # Contemplative rhythm
        self.rhythm_patterns['contemplative'] = [
            PulsePattern(
                pattern_id="contemplative_slow",
                pulse_type=PulseType.WAVE,
                shape=PulseShape.SINE,
                frequency=0.5,
                amplitude=0.8,
                harmonics=[(0.5, 0.5)]
            )
        ]
        
        # Chaotic rhythm
        self.rhythm_patterns['chaotic'] = [
            PulsePattern(
                pattern_id="chaos_1",
                pulse_type=PulseType.CHAOS,
                shape=PulseShape.SAWTOOTH,
                frequency=3.7,  # Irrational frequency
                amplitude=0.6
            ),
            PulsePattern(
                pattern_id="chaos_2",
                pulse_type=PulseType.CHAOS,
                shape=PulseShape.SQUARE,
                frequency=2.3,
                amplitude=0.4,
                phase=np.pi / 3
            )
        ]
        
        # Emergent rhythm
        self.rhythm_patterns['emergent'] = [
            PulsePattern(
                pattern_id="emergent_base",
                pulse_type=PulseType.EMERGENCE,
                shape=PulseShape.GAUSSIAN,
                frequency=1.618,  # Golden ratio
                amplitude=0.5
            ),
            PulsePattern(
                pattern_id="emergent_quantum",
                pulse_type=PulseType.QUANTUM,
                shape=PulseShape.EXPONENTIAL,
                frequency=2.718,  # e
                amplitude=0.3,
                decay_rate=0.5
            )
        ]
    
    def _register_with_schema(self):
        """Register with schema registry"""
        registry.register(
            component_id="schema.pulse",
            name="Pulse Orchestrator",
            component_type="MODULE",
            instance=self,
            capabilities=["generate_pulse", "analyze_rhythm", "detect_patterns"],
            version="2.0.0"
        )
    
    def set_rhythm(self, rhythm_name: str):
        """Set the current rhythm pattern"""
        if rhythm_name in self.rhythm_patterns:
            self.current_rhythm = rhythm_name
            
            # Clear current patterns
            self.generator.active_patterns.clear()
            
            # Add new rhythm patterns
            for pattern in self.rhythm_patterns[rhythm_name]:
                self.generator.add_pattern(pattern)
            
            logger.info(f"Set rhythm to: {rhythm_name}")
            
            # Emit rhythm change
            emit_signal(
                SignalType.CONSCIOUSNESS,
                "pulse_orchestrator",
                {
                    'event': 'rhythm_change',
                    'rhythm': rhythm_name,
                    'timestamp': time.time()
                }
            )
    
    def start(self):
        """Start pulse generation"""
        if self.active:
            return
        
        self.active = True
        self.pulse_thread = threading.Thread(
            target=self._pulse_loop,
            name="pulse_generator"
        )
        self.pulse_thread.start()
        logger.info("Pulse orchestrator started")
    
    def stop(self):
        """Stop pulse generation"""
        self.active = False
        if self.pulse_thread:
            self.pulse_thread.join()
        logger.info("Pulse orchestrator stopped")
    
    def _pulse_loop(self):
        """Main pulse generation loop"""
        while self.active:
            try:
                # Generate 1 second of pulse
                pulse_signal = self.generator.generate(duration=1.0)
                
                # Analyze the pulse
                pulse_metrics = self.analyzer.analyze(pulse_signal)
                
                # Detect patterns
                patterns = self.analyzer.detect_patterns(pulse_signal)
                
                # Adapt rhythm based on patterns
                self._adapt_rhythm(pulse_metrics, patterns)
                
                # Sleep to maintain timing
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Pulse generation error: {e}")
                log_anomaly(
                    "PULSE_GENERATION_ERROR",
                    str(e),
                    AnomalySeverity.ERROR
                )
    
    def _adapt_rhythm(self, pulse_metrics: PulseMetrics, patterns: Dict[str, Any]):
        """Adapt rhythm based on analysis"""
        # Check for emergence
        if 'emergence' in patterns and patterns['emergence']['detected']:
            if self.current_rhythm != 'emergent':
                logger.info("Emergent pattern detected - switching rhythm")
                self.set_rhythm('emergent')
        
        # Check for chaos
        elif 'chaos' in patterns and patterns['chaos']['detected']:
            if patterns['chaos']['chaos_strength'] > 0.7:
                if self.current_rhythm != 'chaotic':
                    logger.warning("High chaos detected - adapting rhythm")
                    self.set_rhythm('chaotic')
        
        # Check coherence
        elif pulse_metrics.coherence > 0.8:
            if self.current_rhythm not in ['contemplative', 'baseline']:
                self.set_rhythm('contemplative')
        
        # Default to baseline if metrics are normal
        elif pulse_metrics.coherence > 0.5 and pulse_metrics.entropy < 0.5:
            if self.current_rhythm != 'baseline':
                self.set_rhythm('baseline')
    
    def inject_pulse(self, pulse_type: PulseType, amplitude: float = 1.0):
        """Inject a manual pulse into the system"""
        event = self.generator.create_pulse_event(pulse_type, amplitude, "manual")
        
        # Create temporary pattern
        temp_pattern = PulsePattern(
            pattern_id=f"injected_{time.time()}",
            pulse_type=pulse_type,
            shape=PulseShape.GAUSSIAN,
            frequency=2.0,
            amplitude=amplitude,
            duration=0.5,
            decay_rate=2.0
        )
        
        # Add temporarily
        self.generator.add_pattern(temp_pattern)
        
        # Remove after duration
        threading.Timer(
            temp_pattern.duration,
            lambda: self.generator.remove_pattern(temp_pattern.pattern_id)
        ).start()
        
        logger.info(f"Injected {pulse_type.value} pulse with amplitude {amplitude}")
        
        return event
    
    def get_pulse_state(self) -> Dict[str, Any]:
        """Get current pulse state"""
        recent_signal = self.generator.generate(duration=0.1)
        current_metrics = self.analyzer.analyze(recent_signal)
        
        return {
            'rhythm': self.current_rhythm,
            'active_patterns': len(self.generator.active_patterns),
            'metrics': {
                'amplitude': current_metrics.peak_amplitude,
                'frequency': current_metrics.frequency_peak,
                'coherence': current_metrics.coherence,
                'entropy': current_metrics.entropy
            },
            'pulse_history_size': len(self.generator.pulse_history)
        }

# Global pulse orchestrator
pulse_orchestrator = PulseOrchestrator()

# Convenience functions
def start_pulse():
    """Start the pulse system"""
    pulse_orchestrator.start()

def stop_pulse():
    """Stop the pulse system"""
    pulse_orchestrator.stop()

def set_rhythm(rhythm: str):
    """Set pulse rhythm"""
    pulse_orchestrator.set_rhythm(rhythm)

def inject_pulse(pulse_type: str, amplitude: float = 1.0):
    """Inject a pulse"""
    try:
        pt = PulseType(pulse_type)
        return pulse_orchestrator.inject_pulse(pt, amplitude)
    except ValueError:
        logger.error(f"Invalid pulse type: {pulse_type}")
        return None

def get_pulse_metrics() -> PulseMetrics:
    """Get current pulse metrics"""
    signal = pulse_orchestrator.generator.generate(duration=1.0)
    return pulse_orchestrator.analyzer.analyze(signal)