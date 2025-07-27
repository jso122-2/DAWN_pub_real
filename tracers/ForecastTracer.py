#!/usr/bin/env python3
"""
DAWN Forecast Tracer - Predictive Analysis & Risk Vector Monitor
Monitors forecast delta, reliability drops, and risk vector instability
"""

import time
import logging
from typing import Dict, List, Any, Optional, Deque, Tuple
from collections import deque
from dataclasses import dataclass
from enum import Enum
import statistics

logger = logging.getLogger("forecast_tracer")

class ForecastReliability(Enum):
    """Forecast reliability levels"""
    EXCELLENT = "excellent"    # >90% reliability
    GOOD = "good"             # 70-90% reliability
    MODERATE = "moderate"     # 50-70% reliability
    POOR = "poor"            # 30-50% reliability
    UNRELIABLE = "unreliable" # <30% reliability

class RiskLevel(Enum):
    """Risk assessment levels"""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ForecastObservation:
    """A single forecast observation"""
    timestamp: float
    forecast_accuracy: float
    reliability_score: float
    risk_level: RiskLevel
    prediction_delta: float
    volatility_index: float
    confidence_interval: Tuple[float, float]
    forecast_horizon: int  # How far ahead the forecast predicts

@dataclass
class RiskVector:
    """Risk vector for multi-dimensional risk analysis"""
    entropy_risk: float
    thermal_risk: float
    coherence_risk: float
    memory_risk: float
    overall_risk: float
    risk_trend: str  # "increasing", "decreasing", "stable"

class ForecastTracer:
    """
    Monitors forecasting system performance and risk vector stability.
    
    Tracks:
    - Forecast accuracy over time
    - Reliability degradation patterns
    - Risk vector instability
    - Prediction confidence intervals
    - Forecast horizon effectiveness
    - Volatility and uncertainty measures
    """
    
    def __init__(self, history_size: int = 150):
        """Initialize forecast tracer with prediction monitoring"""
        self.history_size = history_size
        
        # Historical forecast data
        self.accuracy_history: Deque[float] = deque(maxlen=history_size)
        self.reliability_history: Deque[float] = deque(maxlen=history_size)
        self.delta_history: Deque[float] = deque(maxlen=history_size)
        self.volatility_history: Deque[float] = deque(maxlen=history_size)
        
        # Risk vector tracking
        self.risk_vectors: Deque[RiskVector] = deque(maxlen=100)
        
        # Forecast performance tracking
        self.forecast_cache: Dict[str, Any] = {}  # Cache recent forecasts for validation
        self.prediction_results: Deque[Dict[str, Any]] = deque(maxlen=100)
        
        # Reliability thresholds
        self.reliability_thresholds = {
            ForecastReliability.EXCELLENT: (0.9, 1.0),
            ForecastReliability.GOOD: (0.7, 0.9),
            ForecastReliability.MODERATE: (0.5, 0.7),
            ForecastReliability.POOR: (0.3, 0.5),
            ForecastReliability.UNRELIABLE: (0.0, 0.3)
        }
        
        # Risk calculation parameters
        self.risk_weights = {
            'entropy': 0.25,
            'thermal': 0.25,
            'coherence': 0.25,
            'memory': 0.25
        }
        
        # Recent observations
        self.recent_observations: Deque[ForecastObservation] = deque(maxlen=50)
        
        # State tracking
        self.current_reliability = ForecastReliability.GOOD
        self.current_risk_level = RiskLevel.LOW
        self.forecast_degradation_count = 0
        self.reliability_drops = 0
        
        # Performance metrics
        self.avg_accuracy = 0.75
        self.forecast_stability = 1.0
        self.risk_vector_stability = 1.0
        
        logger.info("🔮 ForecastTracer initialized with predictive monitoring")
    
    def observe(self, state: Dict[str, Any], forecast_data: Optional[Dict[str, Any]] = None) -> ForecastObservation:
        """
        Observe current forecast performance and analyze prediction quality.
        
        Args:
            state: Current system state
            forecast_data: Optional forecast data for analysis
            
        Returns:
            Forecast observation with analysis
        """
        current_time = time.time()
        
        # Extract or calculate forecast metrics
        if forecast_data:
            accuracy = self._calculate_forecast_accuracy(state, forecast_data)
            reliability = forecast_data.get('reliability', 0.75)
            prediction_delta = forecast_data.get('delta', 0.0)
            horizon = forecast_data.get('horizon', 5)
        else:
            # Use system state to infer forecast quality
            accuracy = self._infer_forecast_accuracy(state)
            reliability = self._calculate_reliability_from_state(state)
            prediction_delta = self._calculate_prediction_delta(state)
            horizon = 5
        
        # Calculate risk metrics
        risk_vector = self._calculate_risk_vector(state)
        risk_level = self._determine_risk_level(risk_vector.overall_risk)
        volatility = self._calculate_volatility_index()
        confidence_interval = self._calculate_confidence_interval(reliability, volatility)
        
        # Update histories
        self.accuracy_history.append(accuracy)
        self.reliability_history.append(reliability)
        self.delta_history.append(abs(prediction_delta))
        self.volatility_history.append(volatility)
        self.risk_vectors.append(risk_vector)
        
        # Create observation
        observation = ForecastObservation(
            timestamp=current_time,
            forecast_accuracy=accuracy,
            reliability_score=reliability,
            risk_level=risk_level,
            prediction_delta=prediction_delta,
            volatility_index=volatility,
            confidence_interval=confidence_interval,
            forecast_horizon=horizon
        )
        
        # Update current state
        self.current_reliability = self._determine_reliability_level(reliability)
        self.current_risk_level = risk_level
        
        # Detect reliability drops
        if len(self.reliability_history) >= 2:
            prev_reliability = list(self.reliability_history)[-2]
            if reliability < prev_reliability - 0.1:  # 10% drop
                self.reliability_drops += 1
        
        # Update performance metrics
        self._update_performance_metrics()
        
        # Store observation
        self.recent_observations.append(observation)
        
        return observation
    
    def _calculate_forecast_accuracy(self, current_state: Dict[str, Any], 
                                   forecast_data: Dict[str, Any]) -> float:
        """Calculate accuracy of previous forecasts"""
        # This would compare actual outcomes with previous predictions
        # For now, we'll use a simplified calculation based on state stability
        
        entropy = current_state.get('entropy', 0.5)
        heat = current_state.get('heat', 0.4)
        scup = current_state.get('scup', 0.7)
        
        # Calculate how well the forecast predicted current state
        predicted_entropy = forecast_data.get('predicted_entropy', entropy)
        predicted_heat = forecast_data.get('predicted_heat', heat)
        predicted_scup = forecast_data.get('predicted_scup', scup)
        
        # Calculate accuracy as inverse of prediction error
        entropy_error = abs(entropy - predicted_entropy)
        heat_error = abs(heat - predicted_heat)
        scup_error = abs(scup - predicted_scup)
        
        avg_error = (entropy_error + heat_error + scup_error) / 3
        accuracy = max(0.0, 1.0 - (avg_error * 2))  # Scale error to accuracy
        
        return min(1.0, accuracy)
    
    def _infer_forecast_accuracy(self, state: Dict[str, Any]) -> float:
        """Infer forecast accuracy from system state stability"""
        if len(self.accuracy_history) < 5:
            return 0.75  # Default assumption
        
        # Use state stability as proxy for forecast accuracy
        entropy = state.get('entropy', 0.5)
        heat = state.get('heat', 0.4)
        
        # More stable systems tend to have more accurate forecasts
        stability = 1.0 - (abs(entropy - 0.5) + abs(heat - 0.4))
        accuracy = max(0.3, min(1.0, stability + 0.2))
        
        return accuracy
    
    def _calculate_reliability_from_state(self, state: Dict[str, Any]) -> float:
        """Calculate forecast reliability from current state"""
        # Reliability decreases with high entropy and heat
        entropy = state.get('entropy', 0.5)
        heat = state.get('heat', 0.4)
        scup = state.get('scup', 0.7)
        
        # Higher entropy and heat reduce reliability
        entropy_factor = 1.0 - min(0.5, entropy)
        heat_factor = 1.0 - min(0.5, heat)
        scup_factor = min(1.0, scup)
        
        reliability = (entropy_factor + heat_factor + scup_factor) / 3
        return max(0.1, min(1.0, reliability))
    
    def _calculate_prediction_delta(self, state: Dict[str, Any]) -> float:
        """Calculate prediction delta (difference from expected)"""
        if len(self.delta_history) < 5:
            return 0.0
        
        # Use recent volatility as proxy for prediction delta
        entropy = state.get('entropy', 0.5)
        expected_entropy = 0.5  # Baseline expectation
        
        delta = entropy - expected_entropy
        return delta
    
    def _calculate_risk_vector(self, state: Dict[str, Any]) -> RiskVector:
        """Calculate multi-dimensional risk vector"""
        entropy = state.get('entropy', 0.5)
        heat = state.get('heat', 0.4)
        scup = state.get('scup', 0.7)
        memory_load = state.get('memory_load', 0.5)
        
        # Calculate individual risk components
        entropy_risk = min(1.0, entropy * 1.5)  # High entropy = high risk
        thermal_risk = min(1.0, heat * 1.8)     # High heat = high risk
        coherence_risk = max(0.0, 1.0 - scup)   # Low SCUP = high risk
        memory_risk = min(1.0, memory_load * 1.2)
        
        # Calculate overall risk
        overall_risk = (
            entropy_risk * self.risk_weights['entropy'] +
            thermal_risk * self.risk_weights['thermal'] +
            coherence_risk * self.risk_weights['coherence'] +
            memory_risk * self.risk_weights['memory']
        )
        
        # Determine risk trend
        risk_trend = "stable"
        if len(self.risk_vectors) >= 3:
            recent_risks = [rv.overall_risk for rv in list(self.risk_vectors)[-3:]]
            if recent_risks[-1] > recent_risks[0] * 1.1:
                risk_trend = "increasing"
            elif recent_risks[-1] < recent_risks[0] * 0.9:
                risk_trend = "decreasing"
        
        return RiskVector(
            entropy_risk=entropy_risk,
            thermal_risk=thermal_risk,
            coherence_risk=coherence_risk,
            memory_risk=memory_risk,
            overall_risk=overall_risk,
            risk_trend=risk_trend
        )
    
    def _determine_risk_level(self, overall_risk: float) -> RiskLevel:
        """Determine risk level from overall risk score"""
        if overall_risk >= 0.8:
            return RiskLevel.CRITICAL
        elif overall_risk >= 0.6:
            return RiskLevel.HIGH
        elif overall_risk >= 0.4:
            return RiskLevel.MODERATE
        elif overall_risk >= 0.2:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _determine_reliability_level(self, reliability: float) -> ForecastReliability:
        """Determine reliability level from reliability score"""
        for level, (low, high) in self.reliability_thresholds.items():
            if low <= reliability <= high:
                return level
        return ForecastReliability.UNRELIABLE
    
    def _calculate_volatility_index(self) -> float:
        """Calculate current volatility index"""
        if len(self.delta_history) < 5:
            return 0.1
        
        recent_deltas = list(self.delta_history)[-10:]
        volatility = statistics.stdev(recent_deltas) if len(recent_deltas) > 1 else 0.1
        
        return min(1.0, volatility * 2)  # Scale to 0-1 range
    
    def _calculate_confidence_interval(self, reliability: float, 
                                     volatility: float) -> Tuple[float, float]:
        """Calculate confidence interval for forecasts"""
        # Confidence interval width based on reliability and volatility
        base_width = 0.1
        reliability_factor = 1.0 - reliability
        volatility_factor = volatility
        
        interval_width = base_width + (reliability_factor * 0.2) + (volatility_factor * 0.3)
        
        # Center around current reliability
        lower_bound = max(0.0, reliability - interval_width / 2)
        upper_bound = min(1.0, reliability + interval_width / 2)
        
        return (lower_bound, upper_bound)
    
    def _update_performance_metrics(self):
        """Update forecast performance metrics"""
        if len(self.accuracy_history) >= 10:
            recent_accuracy = list(self.accuracy_history)[-10:]
            self.avg_accuracy = sum(recent_accuracy) / len(recent_accuracy)
        
        if len(self.reliability_history) >= 10:
            recent_reliability = list(self.reliability_history)[-10:]
            reliability_variance = statistics.variance(recent_reliability)
            self.forecast_stability = max(0.0, 1.0 - (reliability_variance * 5))
        
        if len(self.risk_vectors) >= 5:
            recent_risks = [rv.overall_risk for rv in list(self.risk_vectors)[-5:]]
            risk_variance = statistics.variance(recent_risks)
            self.risk_vector_stability = max(0.0, 1.0 - (risk_variance * 3))
    
    def get_forecast_summary(self) -> Dict[str, Any]:
        """Get comprehensive forecast system summary"""
        current_obs = list(self.recent_observations)[-1] if self.recent_observations else None
        
        summary = {
            'current_reliability': self.current_reliability.value,
            'current_risk_level': self.current_risk_level.value,
            'avg_accuracy': self.avg_accuracy,
            'forecast_stability': self.forecast_stability,
            'risk_vector_stability': self.risk_vector_stability,
            'reliability_drops': self.reliability_drops,
            'forecast_degradation_count': self.forecast_degradation_count,
            'current_volatility': current_obs.volatility_index if current_obs else 0.0,
            'current_confidence_interval': current_obs.confidence_interval if current_obs else (0.0, 1.0)
        }
        
        return summary
    
    def get_forecast_alerts(self) -> List[Dict[str, Any]]:
        """Get current forecast-related alerts"""
        alerts = []
        
        # Reliability drop alert
        if self.current_reliability in [ForecastReliability.POOR, ForecastReliability.UNRELIABLE]:
            alerts.append({
                'type': 'LOW_RELIABILITY',
                'severity': 'warning' if self.current_reliability == ForecastReliability.POOR else 'critical',
                'message': f'Forecast reliability degraded: {self.current_reliability.value}',
                'data': {'reliability_score': list(self.reliability_history)[-1] if self.reliability_history else 0}
            })
        
        # High risk alert
        if self.current_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            alerts.append({
                'type': 'HIGH_RISK',
                'severity': 'warning' if self.current_risk_level == RiskLevel.HIGH else 'critical',
                'message': f'Risk level elevated: {self.current_risk_level.value}',
                'data': {'risk_level': self.current_risk_level.value}
            })
        
        # Forecast instability alert
        if self.forecast_stability < 0.5:
            alerts.append({
                'type': 'FORECAST_INSTABILITY',
                'severity': 'warning',
                'message': f'Forecast system showing instability: {self.forecast_stability:.2f}',
                'data': {'stability_score': self.forecast_stability}
            })
        
        return alerts
    
    def predict_next_state(self, current_state: Dict[str, Any], 
                          horizon: int = 3) -> Dict[str, Any]:
        """Generate prediction for next system state"""
        # Simple prediction based on recent trends
        if len(self.accuracy_history) < 5:
            return current_state  # Not enough data for prediction
        
        entropy = current_state.get('entropy', 0.5)
        heat = current_state.get('heat', 0.4)
        scup = current_state.get('scup', 0.7)
        
        # Calculate trends
        entropy_trend = 0.0
        heat_trend = 0.0
        scup_trend = 0.0
        
        if len(self.recent_observations) >= 3:
            recent_obs = list(self.recent_observations)[-3:]
            # This would use actual entropy/heat data from observations
            # For now, use volatility as trend indicator
            avg_volatility = sum(obs.volatility_index for obs in recent_obs) / len(recent_obs)
            entropy_trend = avg_volatility * 0.1
            heat_trend = avg_volatility * 0.05
            scup_trend = -avg_volatility * 0.08  # Volatility generally reduces coherence
        
        # Apply trends with confidence adjustment
        confidence = self.avg_accuracy
        
        predicted_entropy = entropy + (entropy_trend * horizon * confidence)
        predicted_heat = heat + (heat_trend * horizon * confidence)
        predicted_scup = scup + (scup_trend * horizon * confidence)
        
        # Clamp values
        predicted_entropy = max(0.0, min(1.0, predicted_entropy))
        predicted_heat = max(0.0, min(1.0, predicted_heat))
        predicted_scup = max(0.0, min(1.0, predicted_scup))
        
        return {
            'predicted_entropy': predicted_entropy,
            'predicted_heat': predicted_heat,
            'predicted_scup': predicted_scup,
            'prediction_confidence': confidence,
            'prediction_horizon': horizon,
            'predicted_risk_level': self._determine_risk_level(
                (predicted_entropy + predicted_heat + (1.0 - predicted_scup)) / 3
            ).value
        }
    
    def reset_metrics(self):
        """Reset forecast performance metrics"""
        self.reliability_drops = 0
        self.forecast_degradation_count = 0
        self.prediction_results.clear()
        self.forecast_cache.clear()
        
        logger.info("Forecast tracer metrics reset")
    
    def export_state(self) -> Dict[str, Any]:
        """Export current forecast tracer state"""
        current_risk = list(self.risk_vectors)[-1] if self.risk_vectors else None
        
        return {
            'current_reliability': self.current_reliability.value,
            'current_risk_level': self.current_risk_level.value,
            'avg_accuracy': self.avg_accuracy,
            'forecast_stability': self.forecast_stability,
            'risk_vector_stability': self.risk_vector_stability,
            'reliability_drops': self.reliability_drops,
            'current_risk_vector': current_risk.__dict__ if current_risk else None,
            'history_sizes': {
                'accuracy': len(self.accuracy_history),
                'reliability': len(self.reliability_history),
                'delta': len(self.delta_history),
                'volatility': len(self.volatility_history)
            }
        } 