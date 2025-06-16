from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from datetime import datetime
import math
from scipy import signal
from scipy.stats import entropy

class EmotionVector:
    def __init__(self, values: Dict[str, float]):
        self.values = values
        self.timestamp = datetime.now()
        self.magnitude = math.sqrt(sum(v * v for v in values.values()))
        self.normalized = {k: v/self.magnitude if self.magnitude > 0 else 0 
                          for k, v in values.items()}

class FractalEmotions:
    def __init__(self):
        self.emotion_history = []
        self.max_history = 1000
        self.last_update = datetime.now()
        self.emotion_weights = {
            'joy': 1.0,
            'sadness': 1.0,
            'anger': 1.0,
            'fear': 1.0,
            'surprise': 1.0,
            'disgust': 1.0,
            'trust': 1.0,
            'anticipation': 1.0
        }
        self.emotion_correlations = {}
        self.fractal_dimension = 0.0
        self.emotion_entropy = 0.0
        self.emotion_stability = 0.0
        self.emotion_resonance = 0.0
        
        # Initialize correlation matrix
        self._initialize_correlations()
    
    def _initialize_correlations(self) -> None:
        """Initialize emotion correlation matrix"""
        emotions = list(self.emotion_weights.keys())
        n = len(emotions)
        self.emotion_correlations = {
            e1: {e2: 0.0 for e2 in emotions}
            for e1 in emotions
        }
    
    def _calculate_fractal_dimension(self, data: List[float]) -> float:
        """Calculate fractal dimension using box-counting method"""
        if len(data) < 2:
            return 0.0
        
        # Normalize data
        data = np.array(data)
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
        
        # Calculate box counts for different scales
        scales = np.logspace(-4, 0, 20)
        counts = []
        
        for scale in scales:
            # Count boxes needed to cover the data
            boxes = np.ceil(data / scale)
            unique_boxes = len(np.unique(boxes))
            counts.append(unique_boxes)
        
        # Fit line to log-log plot
        log_scales = np.log(scales)
        log_counts = np.log(counts)
        slope, _ = np.polyfit(log_scales, log_counts, 1)
        
        return abs(slope)
    
    def _calculate_emotion_entropy(self, emotions: Dict[str, float]) -> float:
        """Calculate emotion entropy"""
        values = list(emotions.values())
        if not values:
            return 0.0
        return entropy(values)
    
    def _calculate_emotion_stability(self, history: List[EmotionVector]) -> float:
        """Calculate emotion stability"""
        if len(history) < 2:
            return 0.0
        
        # Calculate average change in emotion vectors
        changes = []
        for i in range(1, len(history)):
            prev = history[i-1].normalized
            curr = history[i].normalized
            change = sum((curr[e] - prev[e])**2 for e in prev.keys())
            changes.append(math.sqrt(change))
        
        return 1.0 - min(1.0, np.mean(changes))
    
    def _calculate_emotion_resonance(self, history: List[EmotionVector]) -> float:
        """Calculate emotion resonance using FFT"""
        if len(history) < 10:
            return 0.0
        
        # Extract time series for each emotion
        emotions = list(history[0].values.keys())
        resonance_scores = []
        
        for emotion in emotions:
            values = [h.values[emotion] for h in history]
            # Calculate FFT
            fft = np.fft.fft(values)
            magnitude = np.abs(fft)
            # Find dominant frequency
            peak_idx = np.argmax(magnitude[1:len(magnitude)//2]) + 1
            resonance_scores.append(magnitude[peak_idx] / len(values))
        
        return np.mean(resonance_scores)
    
    def _update_correlations(self, emotions: Dict[str, float]) -> None:
        """Update emotion correlation matrix"""
        for e1 in emotions:
            for e2 in emotions:
                if e1 != e2:
                    # Calculate correlation using exponential moving average
                    alpha = 0.1
                    self.emotion_correlations[e1][e2] = (
                        (1 - alpha) * self.emotion_correlations[e1][e2] +
                        alpha * emotions[e1] * emotions[e2]
                    )
    
    def process_emotions(self, emotions: Dict[str, float]) -> Dict[str, Any]:
        """Process new emotion data"""
        # Create emotion vector
        vector = EmotionVector(emotions)
        self.emotion_history.append(vector)
        
        if len(self.emotion_history) > self.max_history:
            self.emotion_history.pop(0)
        
        # Update metrics
        self.fractal_dimension = self._calculate_fractal_dimension(
            [v.magnitude for v in self.emotion_history]
        )
        self.emotion_entropy = self._calculate_emotion_entropy(emotions)
        self.emotion_stability = self._calculate_emotion_stability(self.emotion_history)
        self.emotion_resonance = self._calculate_emotion_resonance(self.emotion_history)
        
        # Update correlations
        self._update_correlations(emotions)
        
        self.last_update = datetime.now()
        
        return {
            'fractal_dimension': self.fractal_dimension,
            'emotion_entropy': self.emotion_entropy,
            'emotion_stability': self.emotion_stability,
            'emotion_resonance': self.emotion_resonance,
            'emotion_vector': vector.normalized
        }
    
    def get_emotion_history(self) -> List[Dict[str, Any]]:
        """Get emotion history"""
        return [{
            'values': v.values,
            'normalized': v.normalized,
            'magnitude': v.magnitude,
            'timestamp': v.timestamp.isoformat()
        } for v in self.emotion_history]
    
    def get_emotion_correlations(self) -> Dict[str, Dict[str, float]]:
        """Get emotion correlation matrix"""
        return self.emotion_correlations
    
    def get_emotion_weights(self) -> Dict[str, float]:
        """Get emotion weights"""
        return self.emotion_weights
    
    def set_emotion_weight(self, emotion: str, weight: float) -> None:
        """Set weight for a specific emotion"""
        if emotion in self.emotion_weights:
            self.emotion_weights[emotion] = max(0.0, min(1.0, weight))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get fractal emotions metrics"""
        return {
            'fractal_dimension': self.fractal_dimension,
            'emotion_entropy': self.emotion_entropy,
            'emotion_stability': self.emotion_stability,
            'emotion_resonance': self.emotion_resonance,
            'history_length': len(self.emotion_history),
            'last_update': self.last_update.isoformat()
        }

def create_fractal_emotions() -> FractalEmotions:
    """Create and return a new fractal emotions instance"""
    return FractalEmotions() 