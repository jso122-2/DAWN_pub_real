# dawn_core/forecasting/extended_engine.py
# Advanced forecasting engine for DAWN synthetic cognition architecture

import math
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

# Import existing DAWN forecasting components
from ...forecasting_models import Passion, Acquaintance, ForecastVector
from ...forecasting_engine import DAWNForecastingEngine

logger = logging.getLogger(__name__)


@dataclass
class ForecastResult:
    """Result container for forecast computations"""
    forecast: float
    passion: float
    probability: float
    reliability: float
    limit_horizon: float
    
    def __str__(self):
        return (f"ForecastResult(F={self.forecast:.3f}, P={self.passion:.3f}, "
                f"p={self.probability:.3f}, RL={self.reliability:.3f}, LH={self.limit_horizon:.3f})")


class ExtendedDAWNForecastingEngine(DAWNForecastingEngine):
    """
    Extended DAWN forecasting engine with advanced mathematical model.
    Builds upon the base DAWNForecastingEngine with symbolic variable support.
    """
    
    def __init__(self, consciousness_core=None):
        """Initialize the extended forecasting engine."""
        super().__init__(consciousness_core)
        
        # Extended engine specific attributes
        self.sensitivity_cache = {}
        self.forecast_history = []
        self.symbolic_mode = True
        
        logger.info("🔮 Extended DAWN Forecasting Engine initialized with symbolic variable support")
    
    def compute_forecast(self, passion, acquaintance, opportunity: float, delta_time: float) -> Dict[str, float]:
        """
        Compute cognitive forecast using symbolic variables for passion, probability, reliability, and opportunity.
        
        Mathematical Model:
        - F = P / A                    (Forecasting Function)
        - P = (OP * p) / RL           (Opportunity-adjusted Passion)
        - p = (c * OP) / ΔA           (Probability Estimate)  
        - RL = -1 / ΔT                (Imperfect RL via time scaling)
        - LH = c * OP                 (Limit Horizon)
        
        Args:
            passion: Object with .intensity, .fluidity, .centrality attributes
            acquaintance: Object with .delta() and .total() methods
            opportunity: Float between 0 and 1 representing opportunity level
            delta_time: Float representing time delta (seconds or normalized)
            
        Returns:
            Dict containing forecast, passion, probability, reliability, and limit_horizon values
        """
        # Extract symbolic variables
        c = self._get_centrality(passion)        # Centrality coefficient
        OP = opportunity                         # Opportunity level
        delta_A = self._get_delta_acquaintance(acquaintance)   # Delta acquaintance
        A = self._get_total_acquaintance(acquaintance)         # Total acquaintance
        delta_T = delta_time                     # Time delta
        
        # Prevent division by zero
        if delta_A == 0:
            delta_A = 1e-6  # Small epsilon to prevent division by zero
        if delta_T == 0:
            delta_T = 1e-6
        if A == 0:
            A = 1e-6
        
        # Step 1: Calculate Probability Estimate
        # p = (c * OP) / ΔA
        p = (c * OP) / delta_A
        
        # Step 2: Calculate Reliability (Imperfect RL via time scaling)
        # RL = -1 / ΔT
        # Note: Using absolute value to ensure positive reliability
        RL = abs(-1.0 / delta_T)
        
        # Step 3: Calculate Opportunity-adjusted Passion
        # P = (OP * p) / RL
        if RL == 0:
            RL = 1e-6  # Prevent division by zero
        P = (OP * p) / RL
        
        # Step 4: Calculate Forecasting Function
        # F = P / A
        F = P / A
        
        # Step 5: Calculate Limit Horizon
        # LH = c * OP
        LH = c * OP
        
        # Store in forecast history
        self.forecast_history.append({
            'timestamp': datetime.now(),
            'inputs': {'c': c, 'OP': OP, 'delta_A': delta_A, 'A': A, 'delta_T': delta_T},
            'outputs': {'F': F, 'P': P, 'p': p, 'RL': RL, 'LH': LH}
        })
        
        # Return results as dictionary
        return {
            "forecast": F,
            "passion": P,
            "probability": p, 
            "reliability": RL,
            "limit_horizon": LH
        }
    
    def compute_forecast_with_validation(self, passion, acquaintance, opportunity: float, delta_time: float) -> ForecastResult:
        """
        Enhanced forecast computation with input validation and result wrapping.
        
        Args:
            passion: Object with .intensity, .fluidity, .centrality attributes
            acquaintance: Object with .delta() and .total() methods  
            opportunity: Float between 0 and 1
            delta_time: Float representing time delta
            
        Returns:
            ForecastResult: Structured result object
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        if not (0.0 <= opportunity <= 1.0):
            raise ValueError(f"Opportunity must be between 0 and 1, got {opportunity}")
        
        if delta_time <= 0:
            raise ValueError(f"Delta time must be positive, got {delta_time}")
        
        centrality = self._get_centrality(passion)
        if centrality is None:
            raise ValueError("Passion object must have accessible centrality value")
            
        if not (hasattr(acquaintance, 'delta') or hasattr(acquaintance, 'get_delta')):
            raise ValueError("Acquaintance object must have 'delta()' or 'get_delta()' method")
        
        # Compute forecast
        result_dict = self.compute_forecast(passion, acquaintance, opportunity, delta_time)
        
        # Return structured result
        return ForecastResult(**result_dict)
    
    def compute_alternative_reliability(self, passion, use_centrality_ratio: bool = False) -> float:
        """
        Alternative reliability calculation using centrality/passion ratio.
        
        This implements: RL = c / P
        Note: This creates circular dependency with main forecast, so use carefully.
        
        Args:
            passion: Object with centrality attribute
            use_centrality_ratio: Whether to use c/P formula vs time-based
            
        Returns:
            float: Alternative reliability measure
        """
        centrality = self._get_centrality(passion)
        
        if use_centrality_ratio and hasattr(passion, 'intensity'):
            # Use intensity as proxy for P in RL = c / P
            if passion.intensity == 0:
                return float('inf')  # Perfect reliability when no passion intensity
            return centrality / passion.intensity
        else:
            # Fallback to centrality-based reliability
            return abs(centrality)
    
    def analyze_forecast_sensitivity(self, passion, acquaintance, base_opportunity: float, base_delta_time: float) -> Dict[str, Any]:
        """
        Analyze how forecast changes with different opportunity and time values.
        
        Args:
            passion: Passion object
            acquaintance: Acquaintance object
            base_opportunity: Base opportunity level
            base_delta_time: Base time delta
            
        Returns:
            Dict containing sensitivity analysis results
        """
        # Check cache first
        cache_key = f"{id(passion)}_{id(acquaintance)}_{base_opportunity}_{base_delta_time}"
        if cache_key in self.sensitivity_cache:
            return self.sensitivity_cache[cache_key]
        
        base_result = self.compute_forecast(passion, acquaintance, base_opportunity, base_delta_time)
        
        # Test different opportunity levels
        opportunity_sensitivity = []
        for op in [0.1, 0.3, 0.5, 0.7, 0.9]:
            result = self.compute_forecast(passion, acquaintance, op, base_delta_time)
            change_pct = 0 if base_result['forecast'] == 0 else ((result['forecast'] - base_result['forecast']) / base_result['forecast']) * 100
            opportunity_sensitivity.append({
                'opportunity': op,
                'forecast': result['forecast'],
                'change_pct': change_pct
            })
        
        # Test different time deltas
        time_sensitivity = []
        for dt in [0.1, 0.5, 1.0, 2.0, 5.0]:
            result = self.compute_forecast(passion, acquaintance, base_opportunity, dt)
            change_pct = 0 if base_result['forecast'] == 0 else ((result['forecast'] - base_result['forecast']) / base_result['forecast']) * 100
            time_sensitivity.append({
                'delta_time': dt,
                'forecast': result['forecast'], 
                'change_pct': change_pct
            })
        
        analysis_result = {
            'base_result': base_result,
            'opportunity_sensitivity': opportunity_sensitivity,
            'time_sensitivity': time_sensitivity
        }
        
        # Cache the result
        self.sensitivity_cache[cache_key] = analysis_result
        
        return analysis_result
    
    def generate_extended_forecast(self, passion: Passion, acquaintance: Acquaintance, 
                                 opportunity: float = 0.5, delta_time: float = 1.0, **kwargs) -> ForecastVector:
        """
        Generate enhanced forecast using extended mathematical model.
        Integrates with existing DAWN ForecastVector format.
        
        Args:
            passion: DAWN Passion object
            acquaintance: DAWN Acquaintance object
            opportunity: Opportunity level (0-1)
            delta_time: Time delta for forecast
            **kwargs: Additional parameters
            
        Returns:
            ForecastVector: Enhanced forecast with extended metrics
        """
        # Compute extended forecast
        extended_result = self.compute_forecast(passion, acquaintance, opportunity, delta_time)
        
        # Generate base forecast using parent method
        base_forecast = super().generate_forecast(passion, acquaintance, **kwargs)
        
        # Enhance with extended metrics
        base_forecast.confidence = extended_result['forecast']
        base_forecast.predicted_behavior = self._generate_behavior_from_extended(passion, extended_result)
        
        # Add extended metrics as custom attributes
        base_forecast.extended_metrics = {
            'probability': extended_result['probability'],
            'reliability': extended_result['reliability'],
            'limit_horizon': extended_result['limit_horizon'],
            'opportunity_adjusted_passion': extended_result['passion'],
            'opportunity_level': opportunity,
            'delta_time': delta_time
        }
        
        return base_forecast
    
    def pulse_loop_integration(self, passion: Passion, acquaintance: Acquaintance, 
                             pulse_state: Dict[str, Any]) -> Dict[str, float]:
        """
        Integration point for DAWN pulse loop system.
        
        Args:
            passion: Current passion state
            acquaintance: Current acquaintance state
            pulse_state: Current pulse system state (heat, entropy, scup, etc.)
            
        Returns:
            Dict: Values for pulse loop modulation
        """
        # Extract opportunity from pulse state
        opportunity = pulse_state.get('opportunity', 0.5)
        if 'heat' in pulse_state and 'entropy' in pulse_state:
            # Calculate opportunity from heat and entropy
            heat_norm = pulse_state['heat'] / 100.0  # Normalize heat
            entropy_norm = pulse_state['entropy']
            opportunity = (heat_norm + (1 - entropy_norm)) / 2  # Higher heat, lower entropy = more opportunity
        
        # Calculate delta time from pulse
        delta_time = pulse_state.get('delta_time', 1.0)
        
        # Compute extended forecast
        result = self.compute_forecast(passion, acquaintance, opportunity, delta_time)
        
        return {
            'forecast_modulation': result['forecast'],
            'passion_adjustment': result['passion'],
            'probability_factor': result['probability'],
            'reliability_metric': result['reliability'],
            'horizon_limit': result['limit_horizon']
        }
    
    def get_symbolic_body_updates(self, forecast_result: Dict[str, float]) -> Dict[str, float]:
        """
        Generate symbolic body updates using LH + p values.
        
        Args:
            forecast_result: Result from compute_forecast
            
        Returns:
            Dict: Symbolic body update values
        """
        LH = forecast_result['limit_horizon']
        p = forecast_result['probability']
        
        return {
            'symbolic_drift': LH * p,  # Combined drift using horizon and probability
            'temporal_scaling': LH,     # Horizon-based temporal effects
            'probability_field': p,     # Probability field strength
            'coherence_factor': 1.0 / (1.0 + abs(LH - p))  # Coherence based on LH-p alignment
        }
    
    def _get_centrality(self, passion) -> float:
        """Extract centrality value from passion object."""
        if hasattr(passion, 'centrality'):
            return passion.centrality
        elif hasattr(passion, 'intensity') and hasattr(passion, 'fluidity'):
            # Calculate centrality as a function of intensity and fluidity
            return passion.intensity * (1 - passion.fluidity * 0.5)  # Higher intensity, lower fluidity = higher centrality
        else:
            # Default centrality
            return 0.5
    
    def _get_delta_acquaintance(self, acquaintance) -> float:
        """Extract delta acquaintance value."""
        if hasattr(acquaintance, 'delta'):
            return acquaintance.delta()
        elif hasattr(acquaintance, 'get_delta'):
            return acquaintance.get_delta()
        elif hasattr(acquaintance, 'reinforcement_score'):
            # Use reinforcement score as proxy for delta
            return acquaintance.reinforcement_score() * 0.1  # Scale down
        else:
            return 0.2  # Default delta
    
    def _get_total_acquaintance(self, acquaintance) -> float:
        """Extract total acquaintance value."""
        if hasattr(acquaintance, 'total'):
            return acquaintance.total()
        elif hasattr(acquaintance, 'get_total'):
            return acquaintance.get_total()
        elif hasattr(acquaintance, 'reinforcement_score'):
            # Use reinforcement score as proxy for total
            return acquaintance.reinforcement_score()
        else:
            return 1.5  # Default total
    
    def _generate_behavior_from_extended(self, passion: Passion, extended_result: Dict[str, float]) -> str:
        """Generate behavior prediction from extended forecast metrics."""
        confidence = extended_result['forecast']
        probability = extended_result['probability']
        reliability = extended_result['reliability']
        
        # Determine intensity modifier
        if confidence > 0.7:
            intensity = "strongly"
        elif confidence > 0.4:
            intensity = "moderately"
        elif confidence > 0.2:
            intensity = "weakly"
        else:
            intensity = "barely"
        
        # Determine behavior based on probability and reliability
        if probability > 0.6 and reliability > 0.5:
            modifier = "confidently"
        elif probability < 0.3 or reliability < 0.3:
            modifier = "uncertainly"
        else:
            modifier = ""
        
        # Generate behavior string
        base_behavior = f"{intensity}_pursue_{passion.direction}"
        if modifier:
            return f"{modifier}_{base_behavior}"
        return base_behavior
    
    def get_forecast_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent forecast history."""
        return self.forecast_history[-limit:]
    
    def clear_cache(self):
        """Clear sensitivity analysis cache."""
        self.sensitivity_cache.clear()
        logger.info("Extended forecasting engine cache cleared")
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """Get extended engine statistics."""
        base_stats = super().get_stats() if hasattr(super(), 'get_stats') else {}
        
        extended_stats = {
            'symbolic_mode': self.symbolic_mode,
            'forecast_history_count': len(self.forecast_history),
            'sensitivity_cache_size': len(self.sensitivity_cache),
            'extended_engine_version': '1.0.0'
        }
        
        return {**base_stats, **extended_stats}


# Mock classes for testing and development
class MockPassion:
    """Mock passion object for testing"""
    def __init__(self, intensity: float = 0.5, fluidity: float = 0.3, centrality: float = 0.7, direction: str = "test_direction"):
        self.intensity = intensity
        self.fluidity = fluidity 
        self.centrality = centrality
        self.direction = direction
        
    def __str__(self):
        return f"MockPassion(intensity={self.intensity}, fluidity={self.fluidity}, centrality={self.centrality})"


class MockAcquaintance:
    """Mock acquaintance object for testing"""
    def __init__(self, delta_value: float = 0.2, total_value: float = 1.5):
        self._delta = delta_value
        self._total = total_value
        
    def delta(self) -> float:
        return self._delta
        
    def total(self) -> float:
        return self._total
        
    def reinforcement_score(self) -> float:
        return self._total
        
    def __str__(self):
        return f"MockAcquaintance(delta={self._delta}, total={self._total})"


# Factory functions
def create_extended_forecasting_engine(consciousness_core=None) -> ExtendedDAWNForecastingEngine:
    """Factory function for creating extended forecasting engine."""
    return ExtendedDAWNForecastingEngine(consciousness_core)


def integrate_extended_forecasting(consciousness_core) -> ExtendedDAWNForecastingEngine:
    """Integrate extended forecasting engine with DAWN consciousness."""
    engine = ExtendedDAWNForecastingEngine(consciousness_core)
    
    # Register with consciousness if possible
    if hasattr(consciousness_core, 'subsystems'):
        consciousness_core.subsystems['extended_forecasting'] = engine
        logger.info("🔮 Extended forecasting engine integrated with consciousness core")
    
    return engine


# Testing and demonstration
if __name__ == "__main__":
    print("🧠 Extended DAWN Forecasting Engine - Testing")
    print("=" * 50)
    
    # Create test objects
    passion = MockPassion(intensity=0.6, fluidity=0.4, centrality=0.8)
    acquaintance = MockAcquaintance(delta_value=0.3, total_value=2.0)
    opportunity = 0.7
    delta_time = 1.5
    
    print(f"📊 Test Parameters:")
    print(f"   Passion: {passion}")
    print(f"   Acquaintance: {acquaintance}")
    print(f"   Opportunity: {opportunity}")
    print(f"   Delta Time: {delta_time}")
    print()
    
    # Create extended engine
    engine = ExtendedDAWNForecastingEngine()
    
    # Test basic forecast computation
    print("🔮 Basic Forecast Computation:")
    result = engine.compute_forecast(passion, acquaintance, opportunity, delta_time)
    
    print(f"   Forecast (F): {result['forecast']:.4f}")
    print(f"   Passion (P): {result['passion']:.4f}")
    print(f"   Probability (p): {result['probability']:.4f}")
    print(f"   Reliability (RL): {result['reliability']:.4f}")
    print(f"   Limit Horizon (LH): {result['limit_horizon']:.4f}")
    print()
    
    # Test with validation
    print("✅ Validated Forecast Computation:")
    validated_result = engine.compute_forecast_with_validation(passion, acquaintance, opportunity, delta_time)
    print(f"   Result: {validated_result}")
    print()
    
    # Test different scenarios
    print("🧪 Testing Different Scenarios:")
    
    scenarios = [
        ("High Opportunity", 0.9, 1.0),
        ("Low Opportunity", 0.1, 1.0), 
        ("Fast Time", 0.5, 0.1),
        ("Slow Time", 0.5, 5.0),
        ("Extreme Centrality", 0.5, 1.0)  # We'll modify centrality for this
    ]
    
    for name, op, dt in scenarios:
        if name == "Extreme Centrality":
            test_passion = MockPassion(intensity=0.5, fluidity=0.3, centrality=2.0)
            test_result = engine.compute_forecast(test_passion, acquaintance, op, dt)
        else:
            test_result = engine.compute_forecast(passion, acquaintance, op, dt)
            
        print(f"   {name:20} | F={test_result['forecast']:.3f} | P={test_result['passion']:.3f} | LH={test_result['limit_horizon']:.3f}")
    
    print()
    
    # Sensitivity analysis
    print("📈 Sensitivity Analysis:")
    sensitivity = engine.analyze_forecast_sensitivity(passion, acquaintance, 0.5, 1.0)
    
    print("   Opportunity Sensitivity (top 3):")
    for item in sensitivity['opportunity_sensitivity'][:3]:
        print(f"     OP={item['opportunity']} | F={item['forecast']:.3f} | Δ={item['change_pct']:+.1f}%")
    
    print("   Time Sensitivity (top 3):")
    for item in sensitivity['time_sensitivity'][:3]:
        print(f"     ΔT={item['delta_time']} | F={item['forecast']:.3f} | Δ={item['change_pct']:+.1f}%")
    
    # Test symbolic body updates
    print()
    print("🔗 Symbolic Body Updates:")
    symbolic_updates = engine.get_symbolic_body_updates(result)
    for key, value in symbolic_updates.items():
        print(f"   {key}: {value:.4f}")
    
    print()
    print("🚀 Extended Forecasting Engine Ready for Integration!")
    print("   - Symbolic Body updates (via LH + p)")
    print("   - Tick loop modulation") 
    print("   - GUI visual drift panels") 