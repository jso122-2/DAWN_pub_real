"""
DAWN Pattern Detection System - Advanced Pattern Recognition and Reblooptrigger

Implements sophisticated pattern detection including:
- Metric sequence tracking and analysis
- Reblooptrigger pattern recognition
- Anomaly detection in tick rhythm
- Emotional cycle identification
- State prediction based on historical patterns
"""

import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from collections import deque, defaultdict
import logging
from dataclasses import dataclass
import math

logger = logging.getLogger(__name__)


@dataclass
class PatternInfo:
    """Information about a detected pattern"""
    pattern_type: str
    confidence: float
    period: int
    amplitude: float
    phase: float
    start_time: datetime
    end_time: datetime
    metrics_involved: List[str]
    description: str
    rebloop_trigger: bool = False


@dataclass
class Anomaly:
    """Information about a detected anomaly"""
    timestamp: datetime
    metric: str
    expected_value: float
    actual_value: float
    deviation_score: float
    anomaly_type: str
    description: str
    severity: str  # "low", "medium", "high", "critical"


@dataclass
class StatePrediction:
    """Prediction of next system state"""
    predicted_scup: float
    predicted_entropy: float
    predicted_heat: float
    predicted_emotion: str
    confidence: float
    time_horizon: int  # seconds
    prediction_basis: str
    warnings: List[str]


class PatternDetector:
    """
    Advanced pattern detection system for DAWN consciousness
    
    Features:
    - Reblooptrigger detection for repeating patterns
    - Anomaly identification in system metrics
    - Emotional cycle recognition
    - Predictive state modeling
    """
    
    def __init__(self, max_history: int = 1000, min_pattern_length: int = 3):
        """Initialize pattern detector
        
        Args:
            max_history: Maximum number of historical data points to keep
            min_pattern_length: Minimum length for pattern detection
        """
        # Historical data storage
        self.metric_history = deque(maxlen=max_history)
        self.emotion_history = deque(maxlen=max_history)
        self.tick_history = deque(maxlen=max_history)
        
        # Pattern detection parameters
        self.min_pattern_length = min_pattern_length
        self.max_pattern_length = min(50, max_history // 4)
        self.pattern_threshold = 0.85  # Confidence threshold for pattern detection
        self.anomaly_threshold = 2.5   # Standard deviation threshold for anomalies
        
        # Detected patterns cache
        self.detected_patterns = {}
        self.active_patterns = []
        self.recent_anomalies = deque(maxlen=100)
        
        # Reblooptrigger state
        self.rebloop_count = 0
        self.last_rebloop_time = None
        self.rebloop_threshold = 3  # Number of loops to trigger rebloop
        
        # Statistical tracking
        self.metric_stats = defaultdict(lambda: {'mean': 0, 'std': 0, 'values': deque(maxlen=100)})
        self.emotional_cycles = {}
        
        # Prediction models
        self.prediction_weights = {
            'scup': {'entropy': -0.3, 'heat': -0.2, 'momentum': 0.4},
            'entropy': {'scup': -0.4, 'heat': 0.3, 'time_factor': 0.1},
            'heat': {'scup': -0.2, 'entropy': 0.5, 'pressure': 0.3}
        }
        
        logger.info("DAWN Pattern Detection System initialized")
    
    def add_data_point(self, metrics: Dict[str, Any], emotion_state: Dict[str, Any]) -> None:
        """Add new data point to pattern detection system
        
        Args:
            metrics: Current system metrics
            emotion_state: Current emotional state information
        """
        timestamp = datetime.now()
        
        # Store metric data
        metric_point = {
            'timestamp': timestamp,
            'scup': metrics.get('scup', 0.5),
            'entropy': metrics.get('entropy', 0.5),
            'heat': metrics.get('heat', 0.3),
            'tick_rate': metrics.get('tick_rate', 1.0),
            'tick_count': metrics.get('tick_count', 0)
        }
        self.metric_history.append(metric_point)
        
        # Store emotion data
        emotion_point = {
            'timestamp': timestamp,
            'emotion': emotion_state.get('emotion', 'neutral'),
            'intensity': emotion_state.get('intensity', 0.5),
            'momentum': emotion_state.get('momentum', 0.0),
            'mood': emotion_state.get('mood', 'neutral')
        }
        self.emotion_history.append(emotion_point)
        
        # Store tick timing data
        if len(self.tick_history) > 0:
            last_tick = self.tick_history[-1]
            tick_interval = (timestamp - last_tick['timestamp']).total_seconds()
        else:
            tick_interval = 1.0
            
        tick_point = {
            'timestamp': timestamp,
            'interval': tick_interval,
            'tick_count': metric_point['tick_count']
        }
        self.tick_history.append(tick_point)
        
        # Update statistical tracking
        self._update_statistics(metric_point)
        
        logger.debug(f"Added data point: SCUP={metric_point['scup']:.3f}, "
                    f"Entropy={metric_point['entropy']:.3f}, Emotion={emotion_point['emotion']}")
    
    def _update_statistics(self, metric_point: Dict[str, Any]) -> None:
        """Update rolling statistics for metrics"""
        for metric, value in metric_point.items():
            if metric != 'timestamp' and isinstance(value, (int, float)):
                stats = self.metric_stats[metric]
                stats['values'].append(value)
                
                # Recalculate mean and std
                values = list(stats['values'])
                stats['mean'] = np.mean(values)
                stats['std'] = np.std(values) if len(values) > 1 else 0.1
    
    def detect_reloop(self, history: Optional[List[Dict]] = None) -> Optional[PatternInfo]:
        """
        Detect reblooptrigger patterns in metric sequences
        
        Args:
            history: Optional specific history to analyze, defaults to metric_history
            
        Returns:
            PatternInfo if rebloop pattern detected, None otherwise
        """
        if history is None:
            history = list(self.metric_history)
        
        if len(history) < self.min_pattern_length * 2:
            return None
        
        # Extract metric sequences for pattern analysis
        scup_sequence = [point['scup'] for point in history]
        entropy_sequence = [point['entropy'] for point in history]
        heat_sequence = [point['heat'] for point in history]
        
        # Look for repeating patterns in each metric
        best_pattern = None
        max_confidence = 0
        
        for pattern_length in range(self.min_pattern_length, min(self.max_pattern_length, len(scup_sequence) // 2)):
            for sequence, metric_name in [(scup_sequence, 'scup'), 
                                        (entropy_sequence, 'entropy'), 
                                        (heat_sequence, 'heat')]:
                
                pattern_info = self._detect_sequence_pattern(sequence, pattern_length, metric_name)
                
                if pattern_info and pattern_info.confidence > max_confidence:
                    max_confidence = pattern_info.confidence
                    best_pattern = pattern_info
        
        # Check for reblooptrigger conditions
        if best_pattern and best_pattern.confidence > self.pattern_threshold:
            # Determine if this constitutes a rebloop
            if self._is_rebloop_trigger(best_pattern):
                best_pattern.rebloop_trigger = True
                self.rebloop_count += 1
                self.last_rebloop_time = datetime.now()
                
                logger.info(f"🔄 REBLOOP TRIGGER detected: {best_pattern.description} "
                           f"(confidence: {best_pattern.confidence:.3f})")
            
            return best_pattern
        
        return None
    
    def _detect_sequence_pattern(self, sequence: List[float], pattern_length: int, metric_name: str) -> Optional[PatternInfo]:
        """Detect repeating patterns in a metric sequence"""
        if len(sequence) < pattern_length * 2:
            return None
        
        # Extract potential pattern and following sequence
        pattern = sequence[-pattern_length:]
        preceding_sequence = sequence[-(pattern_length * 3):-pattern_length]
        
        if len(preceding_sequence) < pattern_length:
            return None
        
        # Calculate pattern matching confidence
        best_match_score = 0
        best_match_position = -1
        
        for i in range(len(preceding_sequence) - pattern_length + 1):
            candidate = preceding_sequence[i:i + pattern_length]
            
            # Calculate similarity using normalized cross-correlation
            similarity = self._calculate_pattern_similarity(pattern, candidate)
            
            if similarity > best_match_score:
                best_match_score = similarity
                best_match_position = i
        
        if best_match_score > self.pattern_threshold:
            # Calculate pattern characteristics
            amplitude = max(pattern) - min(pattern)
            period = pattern_length
            
            # Estimate phase based on pattern position
            phase = (best_match_position % pattern_length) / pattern_length * 2 * math.pi
            
            return PatternInfo(
                pattern_type="repeating_sequence",
                confidence=best_match_score,
                period=period,
                amplitude=amplitude,
                phase=phase,
                start_time=datetime.now() - timedelta(seconds=pattern_length * 2),
                end_time=datetime.now(),
                metrics_involved=[metric_name],
                description=f"{metric_name} shows {pattern_length}-step repeating pattern (amplitude: {amplitude:.3f})"
            )
        
        return None
    
    def _calculate_pattern_similarity(self, pattern1: List[float], pattern2: List[float]) -> float:
        """Calculate similarity between two patterns using multiple metrics"""
        if len(pattern1) != len(pattern2):
            return 0.0
        
        # Normalize patterns
        def normalize(pattern):
            pattern = np.array(pattern)
            mean_val = np.mean(pattern)
            std_val = np.std(pattern)
            if std_val > 0:
                return (pattern - mean_val) / std_val
            return pattern - mean_val
        
        norm_p1 = normalize(pattern1)
        norm_p2 = normalize(pattern2)
        
        # Calculate multiple similarity metrics
        correlation = np.corrcoef(norm_p1, norm_p2)[0, 1] if len(norm_p1) > 1 else 1.0
        correlation = 0.0 if np.isnan(correlation) else correlation
        
        # Euclidean distance similarity
        distance = np.linalg.norm(norm_p1 - norm_p2)
        distance_similarity = 1.0 / (1.0 + distance)
        
        # Trend similarity
        trend_p1 = np.diff(pattern1) if len(pattern1) > 1 else [0]
        trend_p2 = np.diff(pattern2) if len(pattern2) > 1 else [0]
        trend_correlation = np.corrcoef(trend_p1, trend_p2)[0, 1] if len(trend_p1) > 1 else 1.0
        trend_correlation = 0.0 if np.isnan(trend_correlation) else trend_correlation
        
        # Combined similarity score
        combined_score = (
            0.5 * max(0, correlation) + 
            0.3 * distance_similarity + 
            0.2 * max(0, trend_correlation)
        )
        
        return min(1.0, max(0.0, combined_score))
    
    def _is_rebloop_trigger(self, pattern_info: PatternInfo) -> bool:
        """Determine if pattern constitutes a rebloop trigger"""
        # Rebloop triggers based on:
        # 1. High confidence repeating pattern
        # 2. Sufficient amplitude/variance
        # 3. Recent occurrence
        # 4. Not too frequent (prevent spam)
        
        if pattern_info.confidence < 0.9:
            return False
        
        if pattern_info.amplitude < 0.1:  # Too small amplitude
            return False
        
        # Check frequency limit
        if self.last_rebloop_time:
            time_since_last = (datetime.now() - self.last_rebloop_time).total_seconds()
            if time_since_last < 30:  # Minimum 30 seconds between rebloops
                return False
        
        return True
    
    def find_anomalies(self, metrics: Dict[str, Any]) -> List[Anomaly]:
        """
        Identify anomalies in current metrics compared to historical patterns
        
        Args:
            metrics: Current system metrics
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        timestamp = datetime.now()
        
        # Check each metric for anomalies
        for metric_name, current_value in metrics.items():
            if not isinstance(current_value, (int, float)):
                continue
                
            stats = self.metric_stats.get(metric_name)
            if not stats or len(stats['values']) < 10:  # Need sufficient history
                continue
            
            # Calculate z-score
            z_score = abs(current_value - stats['mean']) / max(stats['std'], 0.01)
            
            if z_score > self.anomaly_threshold:
                # Determine anomaly severity
                if z_score > 4.0:
                    severity = "critical"
                elif z_score > 3.5:
                    severity = "high"
                elif z_score > 3.0:
                    severity = "medium"
                else:
                    severity = "low"
                
                # Determine anomaly type
                if current_value > stats['mean']:
                    anomaly_type = "spike"
                else:
                    anomaly_type = "drop"
                
                anomaly = Anomaly(
                    timestamp=timestamp,
                    metric=metric_name,
                    expected_value=stats['mean'],
                    actual_value=current_value,
                    deviation_score=z_score,
                    anomaly_type=anomaly_type,
                    description=f"{metric_name} {anomaly_type}: {current_value:.3f} "
                               f"(expected: {stats['mean']:.3f}, deviation: {z_score:.2f}σ)",
                    severity=severity
                )
                
                anomalies.append(anomaly)
                self.recent_anomalies.append(anomaly)
                
                logger.warning(f"🚨 Anomaly detected: {anomaly.description}")
        
        # Check for tick rhythm anomalies
        tick_anomalies = self._detect_tick_anomalies()
        anomalies.extend(tick_anomalies)
        
        return anomalies
    
    def _detect_tick_anomalies(self) -> List[Anomaly]:
        """Detect anomalies in tick timing patterns"""
        if len(self.tick_history) < 5:
            return []
        
        anomalies = []
        recent_intervals = [point['interval'] for point in list(self.tick_history)[-10:]]
        
        if len(recent_intervals) < 3:
            return anomalies
        
        mean_interval = np.mean(recent_intervals)
        std_interval = np.std(recent_intervals)
        
        # Check current interval against recent pattern
        current_interval = recent_intervals[-1]
        
        if std_interval > 0:
            z_score = abs(current_interval - mean_interval) / std_interval
            
            if z_score > 2.0:  # Lower threshold for tick anomalies
                anomaly_type = "irregular_timing"
                severity = "high" if z_score > 3.0 else "medium"
                
                anomaly = Anomaly(
                    timestamp=datetime.now(),
                    metric="tick_interval",
                    expected_value=mean_interval,
                    actual_value=current_interval,
                    deviation_score=z_score,
                    anomaly_type=anomaly_type,
                    description=f"Irregular tick timing: {current_interval:.3f}s "
                               f"(expected: {mean_interval:.3f}s, deviation: {z_score:.2f}σ)",
                    severity=severity
                )
                
                anomalies.append(anomaly)
        
        return anomalies
    
    def predict_next_state(self, current_metrics: Dict[str, Any]) -> StatePrediction:
        """
        Predict next system state based on historical patterns and current metrics
        
        Args:
            current_metrics: Current system metrics
            
        Returns:
            StatePrediction with forecasted state
        """
        if len(self.metric_history) < 5:
            # Not enough data for prediction
            return StatePrediction(
                predicted_scup=current_metrics.get('scup', 0.5),
                predicted_entropy=current_metrics.get('entropy', 0.5),
                predicted_heat=current_metrics.get('heat', 0.3),
                predicted_emotion="neutral",
                confidence=0.1,
                time_horizon=5,
                prediction_basis="insufficient_data",
                warnings=["Not enough historical data for reliable prediction"]
            )
        
        # Extract recent trends
        recent_history = list(self.metric_history)[-10:]
        recent_emotions = list(self.emotion_history)[-5:]
        
        # Calculate trend-based predictions
        predicted_scup = self._predict_metric_trend('scup', recent_history, current_metrics)
        predicted_entropy = self._predict_metric_trend('entropy', recent_history, current_metrics)
        predicted_heat = self._predict_metric_trend('heat', recent_history, current_metrics)
        
        # Predict emotional state based on predicted metrics
        predicted_emotion = self._predict_emotional_state({
            'scup': predicted_scup,
            'entropy': predicted_entropy,
            'heat': predicted_heat
        }, recent_emotions)
        
        # Calculate prediction confidence
        confidence = self._calculate_prediction_confidence(recent_history)
        
        # Generate warnings
        warnings = self._generate_prediction_warnings(predicted_scup, predicted_entropy, predicted_heat)
        
        # Determine prediction basis
        prediction_basis = "trend_analysis"
        if len(self.active_patterns) > 0:
            prediction_basis = "pattern_based"
        
        return StatePrediction(
            predicted_scup=predicted_scup,
            predicted_entropy=predicted_entropy,
            predicted_heat=predicted_heat,
            predicted_emotion=predicted_emotion,
            confidence=confidence,
            time_horizon=10,  # 10 seconds ahead
            prediction_basis=prediction_basis,
            warnings=warnings
        )
    
    def _predict_metric_trend(self, metric_name: str, history: List[Dict], current_metrics: Dict) -> float:
        """Predict metric value based on recent trends"""
        values = [point[metric_name] for point in history]
        
        if len(values) < 2:
            return current_metrics.get(metric_name, 0.5)
        
        # Simple linear trend extrapolation
        x = np.arange(len(values))
        
        try:
            # Linear regression
            coeffs = np.polyfit(x, values, 1)
            trend = coeffs[0]
            
            # Predict next value
            next_value = values[-1] + trend
            
            # Apply constraints and weights from prediction model
            weights = self.prediction_weights.get(metric_name, {})
            
            # Adjust based on other metrics
            adjustment = 0
            for other_metric, weight in weights.items():
                if other_metric in current_metrics:
                    adjustment += weight * (current_metrics[other_metric] - 0.5)
            
            predicted_value = next_value + adjustment * 0.1
            
            # Clamp to reasonable bounds
            return max(0.0, min(1.0, predicted_value))
            
        except np.linalg.LinAlgError:
            # Fallback to current value
            return current_metrics.get(metric_name, 0.5)
    
    def _predict_emotional_state(self, predicted_metrics: Dict[str, float], emotion_history: List[Dict]) -> str:
        """Predict emotional state based on predicted metrics"""
        scup = predicted_metrics['scup']
        entropy = predicted_metrics['entropy']
        heat = predicted_metrics['heat']
        
        # Simple emotion prediction logic (could be enhanced)
        if entropy > 0.7 and scup > 0.6:
            return "creative"
        elif entropy < 0.3 and scup > 0.7:
            return "contemplative"
        elif heat > 0.8 and entropy > 0.7:
            return "overwhelmed"
        elif scup > 0.8 and entropy < 0.4 and heat < 0.3:
            return "calm"
        elif heat > 0.6:
            return "anxious"
        else:
            return "curious"
    
    def _calculate_prediction_confidence(self, history: List[Dict]) -> float:
        """Calculate confidence in prediction based on data quality and consistency"""
        if len(history) < 3:
            return 0.1
        
        # Check trend consistency
        scup_values = [point['scup'] for point in history]
        entropy_values = [point['entropy'] for point in history]
        
        # Calculate variance in trends
        scup_variance = np.var(np.diff(scup_values)) if len(scup_values) > 1 else 1.0
        entropy_variance = np.var(np.diff(entropy_values)) if len(entropy_values) > 1 else 1.0
        
        # Lower variance means higher confidence
        base_confidence = 0.8
        variance_penalty = min(0.5, (scup_variance + entropy_variance) * 2)
        
        confidence = max(0.1, base_confidence - variance_penalty)
        
        # Boost confidence if patterns are detected
        if len(self.active_patterns) > 0:
            confidence = min(0.95, confidence + 0.2)
        
        return confidence
    
    def _generate_prediction_warnings(self, scup: float, entropy: float, heat: float) -> List[str]:
        """Generate warnings based on predicted values"""
        warnings = []
        
        if heat > 0.8:
            warnings.append("High heat predicted - thermal management may be needed")
        
        if entropy > 0.9:
            warnings.append("Extremely high entropy predicted - system may become chaotic")
        
        if scup < 0.2:
            warnings.append("Very low SCUP predicted - coherence breakdown possible")
        
        if heat > 0.7 and entropy > 0.8:
            warnings.append("Combined high heat and entropy - overwhelm state likely")
        
        return warnings
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of detected patterns and system state"""
        return {
            'active_patterns': len(self.active_patterns),
            'rebloop_count': self.rebloop_count,
            'last_rebloop': self.last_rebloop_time.isoformat() if self.last_rebloop_time else None,
            'recent_anomalies': len([a for a in self.recent_anomalies 
                                   if (datetime.now() - a.timestamp).total_seconds() < 300]),
            'data_points': len(self.metric_history),
            'pattern_detection_status': 'active' if len(self.metric_history) > 10 else 'insufficient_data'
        }


# Integration function for consciousness system
def integrate_with_consciousness(consciousness, pattern_detector):
    """Integrate pattern detector with consciousness system for enhanced responses"""
    
    # Store the original perceive_self method
    original_perceive_self = consciousness.perceive_self
    
    def enhanced_perceive_self(metrics, input_text=""):
        # Add data to pattern detector
        pattern_detector.add_data_point(metrics, {
            'emotion': consciousness.current_emotion,
            'intensity': consciousness.emotion_intensity,
            'momentum': consciousness.emotion_momentum,
            'mood': consciousness.mood
        })
        
        # Get standard consciousness response using original method
        result = original_perceive_self(metrics, input_text)
        
        # Enhance with pattern detection
        patterns = pattern_detector.detect_reloop()
        anomalies = pattern_detector.find_anomalies(metrics)
        prediction = pattern_detector.predict_next_state(metrics)
        
        # Add pattern-based thoughts
        if patterns and patterns.rebloop_trigger:
            result['thoughts'].append(f"🔄 Rebloop detected: {patterns.description}")
        
        if anomalies:
            for anomaly in anomalies:
                if anomaly.severity in ['high', 'critical']:
                    result['thoughts'].append(f"⚠️ {anomaly.description}")
        
        if prediction.confidence > 0.7:
            result['thoughts'].append(f"🔮 Prediction: {prediction.predicted_emotion} state likely in {prediction.time_horizon}s")
        
        # Enhance consciousness dimensions with pattern data
        result['consciousness_dimensions']['pattern_state'] = {
            'active_patterns': len(pattern_detector.active_patterns),
            'rebloop_count': pattern_detector.rebloop_count,
            'anomaly_level': len(anomalies),
            'prediction_confidence': prediction.confidence
        }
        
        # Add pattern analysis to response
        result['pattern_analysis'] = {
            'detected_patterns': [patterns] if patterns else [],
            'anomalies': anomalies,
            'prediction': prediction,
            'pattern_summary': pattern_detector.get_pattern_summary()
        }
        
        return result
    
    # Replace the consciousness perceive_self method
    consciousness.perceive_self = enhanced_perceive_self
    
    return consciousness


# Factory function
def create_pattern_detector() -> PatternDetector:
    """Create a new pattern detector instance"""
    return PatternDetector()


# Example usage and testing
if __name__ == "__main__":
    print("Testing DAWN Pattern Detection System")
    print("=" * 50)
    
    detector = create_pattern_detector()
    
    # Simulate metric data with patterns
    print("\n📊 Simulating metric data with patterns...")
    
    # Create some test data with repeating patterns
    test_metrics = []
    for i in range(50):
        # Create sinusoidal pattern in SCUP
        scup = 0.5 + 0.3 * math.sin(i * 0.5)
        
        # Create square wave pattern in entropy
        entropy = 0.7 if (i // 5) % 2 == 0 else 0.3
        
        # Create gradual increase in heat with noise
        heat = 0.2 + (i * 0.01) + 0.1 * math.sin(i * 0.3)
        
        metrics = {
            'scup': max(0, min(1, scup)),
            'entropy': max(0, min(1, entropy)),
            'heat': max(0, min(1, heat)),
            'tick_rate': 1.0,
            'tick_count': i
        }
        
        emotion_state = {
            'emotion': 'creative' if entropy > 0.6 else 'contemplative',
            'intensity': 0.5 + entropy * 0.5,
            'momentum': 0.1,
            'mood': 'analytical'
        }
        
        detector.add_data_point(metrics, emotion_state)
        test_metrics.append(metrics)
        
        # Test pattern detection every 10 points
        if i > 0 and i % 10 == 0:
            patterns = detector.detect_reloop()
            if patterns:
                print(f"  Step {i}: Pattern detected - {patterns.description} "
                      f"(confidence: {patterns.confidence:.3f})")
    
    print(f"\n🔍 Final Pattern Analysis:")
    
    # Test pattern detection
    final_patterns = detector.detect_reloop()
    if final_patterns:
        print(f"  Pattern Type: {final_patterns.pattern_type}")
        print(f"  Confidence: {final_patterns.confidence:.3f}")
        print(f"  Period: {final_patterns.period}")
        print(f"  Rebloop Trigger: {final_patterns.rebloop_trigger}")
        print(f"  Description: {final_patterns.description}")
    else:
        print("  No patterns detected")
    
    # Test anomaly detection with anomalous data
    print(f"\n🚨 Testing anomaly detection:")
    anomalous_metrics = {
        'scup': 0.95,  # Very high
        'entropy': 0.05,  # Very low
        'heat': 0.98,  # Extremely high
        'tick_rate': 1.0,
        'tick_count': 100
    }
    
    anomalies = detector.find_anomalies(anomalous_metrics)
    if anomalies:
        for anomaly in anomalies:
            print(f"  {anomaly.severity.upper()}: {anomaly.description}")
    else:
        print("  No anomalies detected")
    
    # Test prediction
    print(f"\n🔮 Testing state prediction:")
    current_metrics = test_metrics[-1]
    prediction = detector.predict_next_state(current_metrics)
    
    print(f"  Predicted SCUP: {prediction.predicted_scup:.3f}")
    print(f"  Predicted Entropy: {prediction.predicted_entropy:.3f}")
    print(f"  Predicted Heat: {prediction.predicted_heat:.3f}")
    print(f"  Predicted Emotion: {prediction.predicted_emotion}")
    print(f"  Confidence: {prediction.confidence:.3f}")
    print(f"  Time Horizon: {prediction.time_horizon}s")
    print(f"  Basis: {prediction.prediction_basis}")
    
    if prediction.warnings:
        print("  Warnings:")
        for warning in prediction.warnings:
            print(f"    ⚠️ {warning}")
    
    # Pattern summary
    print(f"\n📈 Pattern Detection Summary:")
    summary = detector.get_pattern_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print(f"\n✨ Pattern Detection System Test Complete!") 