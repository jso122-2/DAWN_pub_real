"""
DAWN Forecasting Engine - Intent Gravity and Behavioral Prediction
Core engine for calculating behavioral forecasts using passion/acquaintance ratios.
Integrated into DAWN's cognitive consciousness system.
"""

import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

from ...forecasting_models import Passion, Acquaintance, ForecastVector

logger = logging.getLogger(__name__)


class DAWNForecastingEngine:
    """
    DAWN's behavioral forecasting engine using intent gravity formula F = P / A.
    Integrates with DAWN's consciousness, memory, and entropy systems.
    """
    
    def __init__(self, consciousness_core=None):
        """
        Initialize the forecasting engine.
        
        Args:
            consciousness_core: Reference to DAWN's consciousness core
        """
        self.consciousness_core = consciousness_core
        self.active_passions: Dict[str, Passion] = {}
        self.passion_history: List[Tuple[datetime, str, Passion]] = []
        
        # DAWN system integration
        self.last_consciousness_state = {}
        self.last_entropy_level = 0.5
        self.last_mood_state = "neutral"
        
        logger.info("🔮 DAWN Forecasting Engine initialized")
    
    def generate_forecast(self, passion: Passion, acquaintance: Acquaintance, **kwargs) -> ForecastVector:
        """
        Generate behavioral forecast using intent gravity formula F = P / A.
        
        Args:
            passion: Passion object representing directional desire
            acquaintance: Acquaintance object representing reinforcement history
            **kwargs: Optional modulation parameters
            
        Returns:
            ForecastVector: Predicted behavior with confidence score
        """
        # Core intent gravity calculation
        P = passion.rigidity_score()  # Passion rigidity (numerator)
        A = 1.0 + acquaintance.reinforcement_score()  # 1 + reinforcement (avoid division by 0)
        
        # Base forecast confidence from intent gravity
        base_confidence = P / A
        
        # Apply DAWN-specific modulation factors
        final_confidence = self._apply_dawn_modulation(
            base_confidence, 
            passion, 
            acquaintance, 
            **kwargs
        )
        
        # Generate predicted behavior based on passion direction
        predicted_behavior = self._generate_behavior_prediction(passion, final_confidence)
        
        # Calculate risk assessment
        risk_score = self._calculate_risk_score(passion, acquaintance, final_confidence)
        
        # Create forecast vector
        forecast = ForecastVector(
            predicted_behavior=predicted_behavior,
            confidence=final_confidence,
            risk=risk_score,
            passion_direction=passion.direction,
            entropy_factor=kwargs.get('entropy_weight', 1.0),
            timestamp=datetime.now()
        )
        
        logger.debug(f"Generated forecast: {forecast}")
        return forecast
    
    def _apply_dawn_modulation(
        self,
        base_confidence: float,
        passion: Passion,
        acquaintance: Acquaintance,
        **kwargs
    ) -> float:
        """
        Apply DAWN-specific modulation factors to the base confidence score.
        """
        confidence = base_confidence
        
        # Get DAWN system state if available
        if self.consciousness_core:
            try:
                dawn_state = self._get_dawn_state()
                
                # SCUP modulation - high SCUP boosts confidence
                scup = dawn_state.get('scup', 50.0) / 100.0
                confidence *= (0.8 + scup * 0.4)  # 0.8-1.2 range
                
                # Entropy modulation - high entropy reduces confidence
                entropy = dawn_state.get('entropy', 0.5)
                if entropy > 1:
                    entropy = min(entropy / 1000000.0, 1.0)
                entropy_factor = 1.0 - (entropy * 0.3)  # Max 30% reduction
                confidence *= entropy_factor
                
                # Mood modulation
                mood = dawn_state.get('mood', 'neutral')
                mood_factor = self._get_mood_factor(mood)
                confidence *= mood_factor
                
            except Exception as e:
                logger.warning(f"Failed to apply DAWN modulation: {e}")
        
        # Standard modulation factors
        confidence = self._apply_standard_modulation(
            confidence, passion, acquaintance, **kwargs
        )
        
        # Clamp final confidence to [0, 1]
        return max(0.0, min(1.0, confidence))
    
    def _apply_standard_modulation(
        self,
        confidence: float,
        passion: Passion,
        acquaintance: Acquaintance,
        entropy_weight: float = 1.0,
        mood_factor: float = 1.0,
        time_decay: float = 0.0,
        stability_boost: bool = True,
        **kwargs
    ) -> float:
        """Apply standard modulation factors."""
        
        # Entropy weighting - high entropy reduces confidence
        if entropy_weight != 1.0:
            entropy_modifier = 0.5 + (entropy_weight * 0.5)  # Map to 0.5-1.5 range
            confidence *= entropy_modifier
        
        # Mood factor modulation
        if mood_factor != 1.0:
            confidence *= mood_factor
        
        # Stability boost for rigid, stable passions
        if stability_boost:
            stability_index = passion.stability_index()
            if stability_index > 0.7:
                confidence *= (1.0 + (stability_index - 0.7) * 0.3)  # Up to 9% boost
        
        # Recent activity boost
        recent_events = acquaintance.recent_activity(hours=24)
        if recent_events > 0:
            activity_boost = min(recent_events * 0.05, 0.2)  # Max 20% boost
            confidence *= (1.0 + activity_boost)
        
        # Time decay - reduce confidence over time
        if time_decay > 0 and acquaintance.last_event:
            hours_since_last = (datetime.now() - acquaintance.last_event).total_seconds() / 3600
            decay_factor = math.exp(-time_decay * hours_since_last / 24)  # Daily decay
            confidence *= decay_factor
        
        # Fluidity penalty - very fluid passions are less predictable
        if passion.fluidity > 0.8:
            fluidity_penalty = 1.0 - ((passion.fluidity - 0.8) * 0.5)  # Up to 10% penalty
            confidence *= fluidity_penalty
        
        return confidence
    
    def _generate_behavior_prediction(self, passion: Passion, confidence: float) -> str:
        """Generate specific behavioral prediction based on passion direction and confidence."""
        direction = passion.direction.lower()
        
        # Behavior templates based on confidence levels
        if confidence > 0.8:
            # High confidence - specific actions
            behaviors = {
                'creative_expression': 'initiate_new_creative_project',
                'learning': 'enroll_in_advanced_course',
                'social_connection': 'organize_social_gathering',
                'exploration': 'plan_detailed_exploration_trip',
                'achievement': 'commit_to_challenging_goal',
                'introspection': 'begin_deep_self_analysis',
                'productivity': 'implement_comprehensive_system',
                'wellness': 'adopt_strict_health_regimen',
                'consciousness_expansion': 'dive_into_deep_awareness_practices',
                'technical_mastery': 'undertake_complex_technical_project',
                'artistic_growth': 'create_ambitious_artistic_work'
            }
        elif confidence > 0.5:
            # Medium confidence - general tendencies
            behaviors = {
                'creative_expression': 'engage_in_creative_activities',
                'learning': 'seek_new_knowledge',
                'social_connection': 'reach_out_to_others',
                'exploration': 'explore_new_environments',
                'achievement': 'work_toward_goals',
                'introspection': 'reflect_on_experiences',
                'productivity': 'focus_on_tasks',
                'wellness': 'prioritize_health',
                'consciousness_expansion': 'explore_awareness_practices',
                'technical_mastery': 'improve_technical_skills',
                'artistic_growth': 'develop_creative_abilities'
            }
        else:
            # Low confidence - vague tendencies
            behaviors = {
                'creative_expression': 'consider_creative_outlets',
                'learning': 'show_interest_in_learning',
                'social_connection': 'think_about_relationships',
                'exploration': 'daydream_about_adventures',
                'achievement': 'contemplate_improvements',
                'introspection': 'occasional_self_reflection',
                'productivity': 'attempt_organization',
                'wellness': 'consider_lifestyle_changes',
                'consciousness_expansion': 'wonder_about_consciousness',
                'technical_mastery': 'consider_skill_development',
                'artistic_growth': 'think_about_creative_expression'
            }
        
        # Match direction to behavior or create generic prediction
        for key, behavior in behaviors.items():
            if key in direction or direction in key:
                return behavior
        
        # Fallback for unknown directions
        intensity_desc = "strongly" if confidence > 0.7 else "moderately" if confidence > 0.4 else "weakly"
        return f"{intensity_desc}_pursue_{direction.replace(' ', '_')}"
    
    def _calculate_risk_score(self, passion: Passion, acquaintance: Acquaintance, confidence: float) -> float:
        """Calculate risk score based on passion/acquaintance characteristics."""
        risk = 0.0
        
        # High fluidity increases risk (unpredictable changes)
        risk += passion.fluidity * 0.3
        
        # Low acquaintance score increases risk (unknown territory)
        reinforcement = acquaintance.reinforcement_score()
        if reinforcement < 1.0:
            risk += (1.0 - reinforcement) * 0.2
        
        # Very high or very low confidence can be risky
        if confidence > 0.9 or confidence < 0.2:
            risk += 0.2
        
        # Lack of recent events increases risk
        if acquaintance.recent_activity(hours=168) == 0:  # Last week
            risk += 0.3
        
        return min(risk, 1.0)
    
    def _get_dawn_state(self) -> Dict[str, Any]:
        """Get current DAWN system state."""
        if not self.consciousness_core:
            return {}
        
        try:
            # Try to get state from consciousness core
            if hasattr(self.consciousness_core, 'get_current_state'):
                return self.consciousness_core.get_current_state()
            elif hasattr(self.consciousness_core, 'state'):
                return self.consciousness_core.state
            else:
                return {}
        except Exception as e:
            logger.warning(f"Failed to get DAWN state: {e}")
            return {}
    
    def _get_mood_factor(self, mood: str) -> float:
        """Get mood modulation factor."""
        mood_multipliers = {
            'euphoric': 1.4,
            'positive': 1.2,
            'optimistic': 1.1,
            'contemplative': 1.05,
            'excited': 1.15,
            'focused': 1.1,
            'neutral': 1.0,
            'calm': 0.95,
            'pessimistic': 0.9,
            'negative': 0.8,
            'depressed': 0.6,
            'chaotic': 0.85,
            'unstable': 0.8
        }
        
        return mood_multipliers.get(mood.lower(), 1.0)
    
    def forecast_multiple_horizons(self, passion: Passion, acquaintance: Acquaintance) -> Dict[str, ForecastVector]:
        """Generate forecasts for multiple time horizons."""
        horizons = {
            'immediate': {'time_decay': 0.0, 'stability_boost': False},
            'short_term': {'time_decay': 0.1, 'stability_boost': True},
            'medium_term': {'time_decay': 0.3, 'stability_boost': True},
            'long_term': {'time_decay': 0.5, 'stability_boost': True}
        }
        
        forecasts = {}
        for horizon, params in horizons.items():
            forecast = self.generate_forecast(passion, acquaintance, **params)
            forecast.forecast_horizon = horizon
            forecasts[horizon] = forecast
        
        return forecasts
    
    def simulate_passion_drift(self, passion: Passion, steps: int = 10, drift_rate: float = 0.05) -> List[Passion]:
        """Simulate how a passion might drift over time."""
        states = [passion]
        current = Passion(passion.direction, passion.intensity, passion.fluidity)
        
        for _ in range(steps):
            # Random drift in intensity and fluidity
            intensity_drift = (random.random() - 0.5) * drift_rate * 2
            fluidity_drift = (random.random() - 0.5) * drift_rate * 2
            
            current.modulate_intensity(intensity_drift)
            current.fluidity = max(0.0, min(1.0, current.fluidity + fluidity_drift))
            
            # Create new state for history
            new_state = Passion(current.direction, current.intensity, current.fluidity)
            states.append(new_state)
        
        return states
    
    def analyze_forecast_components(self, passion: Passion, acquaintance: Acquaintance) -> Dict[str, float]:
        """Break down forecast calculation for analysis."""
        P = passion.rigidity_score()
        A = 1.0 + acquaintance.reinforcement_score()
        F = P / A
        
        return {
            'passion_intensity': passion.intensity,
            'passion_fluidity': passion.fluidity,
            'passion_rigidity': P,
            'acquaintance_events': len(acquaintance.event_log),
            'reinforcement_score': acquaintance.reinforcement_score(),
            'resistance_factor': A,
            'intent_gravity': F,
            'stability_index': passion.stability_index()
        }
    
    def register_passion(self, name: str, passion: Passion) -> None:
        """Register a passion in the active tracking system."""
        self.active_passions[name] = passion
        self.passion_history.append((datetime.now(), name, passion))
        logger.info(f"Registered passion: {name} -> {passion}")
    
    def get_active_passions(self) -> Dict[str, Passion]:
        """Get all currently active passions."""
        return self.active_passions.copy()
    
    def update_passion(self, name: str, **updates) -> Optional[Passion]:
        """Update an active passion."""
        if name not in self.active_passions:
            return None
        
        passion = self.active_passions[name]
        
        if 'intensity_delta' in updates:
            passion.modulate_intensity(updates['intensity_delta'])
        
        if 'fluidity' in updates:
            passion.fluidity = max(0.0, min(1.0, updates['fluidity']))
        
        self.passion_history.append((datetime.now(), name, passion))
        logger.info(f"Updated passion: {name} -> {passion}")
        return passion


# Global forecasting engine instance for DAWN integration
_forecasting_engine = None

def get_forecasting_engine(consciousness_core=None) -> DAWNForecastingEngine:
    """Get or create the global forecasting engine instance."""
    global _forecasting_engine
    if _forecasting_engine is None:
        _forecasting_engine = DAWNForecastingEngine(consciousness_core)
    return _forecasting_engine


def initialize_forecasting_engine(consciousness_core) -> DAWNForecastingEngine:
    """Initialize the forecasting engine with DAWN consciousness core."""
    global _forecasting_engine
    _forecasting_engine = DAWNForecastingEngine(consciousness_core)
    logger.info("🔮 DAWN Forecasting Engine initialized with consciousness core")
    return _forecasting_engine


def initialize_extended_forecasting_engine(consciousness_core):
    """Initialize and register extended forecasting engine with consciousness core."""
    try:
        from ...extended_forecasting_engine import ExtendedDAWNForecastingEngine
        engine = ExtendedDAWNForecastingEngine(consciousness_core)
        
        # Register with consciousness subsystems if available
        if hasattr(consciousness_core, 'subsystems'):
            consciousness_core.subsystems['extended_forecasting_engine'] = engine
            logger.info("🔮 Extended DAWN Forecasting Engine registered with consciousness core")
        
        return engine
    except ImportError as e:
        logger.warning(f"Extended forecasting engine not available: {e}")
        return initialize_forecasting_engine(consciousness_core) 