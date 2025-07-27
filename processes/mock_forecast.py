#!/usr/bin/env python3
"""
DAWN Mock Forecast System
Generates synthetic forecasts and triggers for cognitive events
Simulates predictive systems for rebloom activation
"""

import random
import math
from typing import Dict, Any, List, Tuple

def compute_forecast(passion_state: Dict[str, Any], acquaintance_state: Dict[str, Any]) -> Dict[str, Any]:
    """Compute mock forecast based on passion and acquaintance states"""
    
    # Extract passion metrics
    passion_intensity = passion_state.get('intensity', 0.5)
    passion_coherence = passion_state.get('coherence', 0.5)
    passion_trajectory = passion_state.get('trajectory', 'stable')
    
    # Extract acquaintance metrics  
    acquaintance_familiarity = acquaintance_state.get('familiarity', 0.5)
    acquaintance_trust = acquaintance_state.get('trust', 0.5)
    acquaintance_resonance = acquaintance_state.get('resonance', 0.5)
    
    # Calculate forecast probability
    forecast_base = (passion_intensity * 0.4 + 
                    passion_coherence * 0.3 + 
                    acquaintance_familiarity * 0.2 + 
                    acquaintance_trust * 0.1)
    
    # Add trajectory influence
    trajectory_modifiers = {
        'ascending': 0.2,
        'stable': 0.0,
        'descending': -0.2,
        'volatile': random.uniform(-0.3, 0.3)
    }
    
    forecast_probability = min(1.0, max(0.0, 
        forecast_base + trajectory_modifiers.get(passion_trajectory, 0.0)))
    
    # Determine risk level
    risk_level = calculate_risk_level(forecast_probability, passion_state, acquaintance_state)
    
    # Calculate reliability
    reliability = calculate_reliability(passion_coherence, acquaintance_trust)
    
    # Generate prediction vector
    prediction_vector = generate_prediction_vector(forecast_probability, risk_level)
    
    return {
        'forecast': forecast_probability,
        'risk': risk_level,
        'limit_horizon': calculate_limit_horizon(forecast_probability),
        'reliability': reliability,
        'prediction_vector': prediction_vector,
        'confidence': reliability * forecast_probability,
        'temporal_scope': 'short_term',
        'metadata': {
            'passion_intensity': passion_intensity,
            'passion_trajectory': passion_trajectory,
            'acquaintance_familiarity': acquaintance_familiarity,
            'calculation_method': 'synthetic_forecast'
        }
    }

def generate_mock_passion(entropy: float, mood: str, tick: int) -> Dict[str, Any]:
    """Generate mock passion state based on consciousness metrics"""
    
    # Base intensity from entropy and mood
    mood_multipliers = {
        'EXCITED': 0.9,
        'FOCUSED': 0.8,
        'CONTEMPLATIVE': 0.6,
        'CALM': 0.4,
        'CHAOTIC': 1.0,
        'ANXIOUS': 0.7
    }
    
    base_intensity = entropy * mood_multipliers.get(mood, 0.5)
    
    # Add temporal variation
    temporal_factor = math.sin(tick * 0.1) * 0.2
    intensity = min(1.0, max(0.0, base_intensity + temporal_factor))
    
    # Calculate coherence (inverse of entropy for some realism)
    coherence = min(1.0, max(0.1, 1.0 - entropy * 0.7))
    
    # Determine trajectory based on recent intensity trend
    trajectory = determine_passion_trajectory(intensity, entropy, tick)
    
    return {
        'intensity': intensity,
        'coherence': coherence,
        'trajectory': trajectory,
        'focus_areas': get_passion_focus_areas(mood, intensity),
        'sustainability': coherence * intensity,
        'metadata': {
            'source_entropy': entropy,
            'source_mood': mood,
            'tick': tick
        }
    }

def generate_mock_acquaintance(scup: float, depth: float, mood: str) -> Dict[str, Any]:
    """Generate mock acquaintance state based on consciousness metrics"""
    
    # Familiarity based on SCUP (semantic coherence)
    familiarity = min(1.0, scup / 100.0)
    
    # Trust based on consciousness depth and mood stability
    mood_trust_factors = {
        'CALM': 0.9,
        'FOCUSED': 0.8,
        'CONTEMPLATIVE': 0.7,
        'CONFIDENT': 0.8,
        'CHAOTIC': 0.2,
        'ANXIOUS': 0.3
    }
    
    base_trust = mood_trust_factors.get(mood, 0.5)
    trust = min(1.0, max(0.1, base_trust * depth))
    
    # Resonance as combination of familiarity and trust
    resonance = (familiarity + trust) / 2 + random.uniform(-0.1, 0.1)
    resonance = min(1.0, max(0.0, resonance))
    
    return {
        'familiarity': familiarity,
        'trust': trust,
        'resonance': resonance,
        'connection_strength': (familiarity + trust + resonance) / 3,
        'interaction_history': generate_interaction_history(familiarity, trust),
        'metadata': {
            'source_scup': scup,
            'source_depth': depth,
            'source_mood': mood
        }
    }

def calculate_risk_level(forecast_prob: float, passion: Dict[str, Any], acquaintance: Dict[str, Any]) -> str:
    """Calculate risk level for forecast"""
    
    # High forecast probability with low coherence = risk
    passion_coherence = passion.get('coherence', 0.5)
    acquaintance_trust = acquaintance.get('trust', 0.5)
    
    if forecast_prob > 0.8 and passion_coherence < 0.4:
        return 'chaos'
    elif forecast_prob > 0.7 and acquaintance_trust < 0.3:
        return 'instability'
    elif forecast_prob > 0.6 and passion.get('trajectory') == 'volatile':
        return 'drift'
    elif forecast_prob < 0.3:
        return 'stagnation'
    elif passion_coherence < 0.3 or acquaintance_trust < 0.3:
        return 'uncertainty'
    else:
        return 'stable'

def calculate_reliability(passion_coherence: float, acquaintance_trust: float) -> float:
    """Calculate forecast reliability"""
    base_reliability = (passion_coherence + acquaintance_trust) / 2
    
    # Add some noise
    noise = random.uniform(-0.1, 0.1)
    reliability = min(1.0, max(0.1, base_reliability + noise))
    
    return reliability

def calculate_limit_horizon(forecast_prob: float) -> float:
    """Calculate the limit horizon for forecast validity"""
    # Higher probability = shorter reliable horizon
    base_horizon = 1.0 - forecast_prob
    
    # Add some randomness
    horizon_noise = random.uniform(-0.2, 0.2)
    limit_horizon = min(1.0, max(0.1, base_horizon + horizon_noise))
    
    return limit_horizon

def generate_prediction_vector(forecast_prob: float, risk_level: str) -> List[float]:
    """Generate prediction vector for forecast"""
    
    # Base vector from forecast probability
    base_vector = [
        forecast_prob,
        1.0 - forecast_prob,
        random.uniform(0.0, 1.0),
        random.uniform(0.0, 1.0)
    ]
    
    # Risk-based modifications
    risk_modifiers = {
        'chaos': [0.3, -0.2, 0.8, 0.9],
        'instability': [0.2, -0.1, 0.6, 0.7],
        'drift': [0.1, 0.0, 0.4, 0.5],
        'stable': [0.0, 0.0, 0.0, 0.0],
        'stagnation': [-0.2, 0.1, -0.3, -0.2],
        'uncertainty': [0.0, 0.0, 0.5, 0.5]
    }
    
    modifiers = risk_modifiers.get(risk_level, [0.0, 0.0, 0.0, 0.0])
    
    # Apply modifiers and clamp
    prediction_vector = []
    for i, (base, mod) in enumerate(zip(base_vector, modifiers)):
        value = min(1.0, max(-1.0, base + mod))
        prediction_vector.append(value)
    
    return prediction_vector

def determine_passion_trajectory(intensity: float, entropy: float, tick: int) -> str:
    """Determine passion trajectory based on current state"""
    
    # Use tick for temporal patterns
    temporal_phase = math.sin(tick * 0.05)
    
    if intensity > 0.8 and entropy > 0.7:
        return 'volatile'
    elif intensity > 0.6 and temporal_phase > 0.3:
        return 'ascending'
    elif intensity < 0.3 or temporal_phase < -0.3:
        return 'descending'
    else:
        return 'stable'

def get_passion_focus_areas(mood: str, intensity: float) -> List[str]:
    """Get focus areas for passion based on mood and intensity"""
    
    mood_focus_map = {
        'EXCITED': ['exploration', 'creation', 'connection'],
        'FOCUSED': ['mastery', 'precision', 'optimization'],
        'CONTEMPLATIVE': ['understanding', 'reflection', 'wisdom'],
        'CALM': ['harmony', 'balance', 'sustainability'],
        'CHAOTIC': ['experimentation', 'disruption', 'novelty'],
        'ANXIOUS': ['security', 'validation', 'stability']
    }
    
    base_areas = mood_focus_map.get(mood, ['general_interest'])
    
    # Intensity affects number of focus areas
    if intensity > 0.8:
        return base_areas  # All areas
    elif intensity > 0.5:
        return base_areas[:2]  # Top 2 areas
    else:
        return base_areas[:1]  # Single focus

def generate_interaction_history(familiarity: float, trust: float) -> List[Dict[str, Any]]:
    """Generate synthetic interaction history"""
    
    # Number of interactions based on familiarity
    interaction_count = int(familiarity * 10) + random.randint(1, 3)
    
    history = []
    for i in range(min(interaction_count, 5)):  # Cap at 5 for performance
        outcome_prob = trust + random.uniform(-0.2, 0.2)
        outcome = 'positive' if outcome_prob > 0.5 else 'neutral' if outcome_prob > 0.3 else 'negative'
        
        interaction = {
            'sequence': i + 1,
            'outcome': outcome,
            'intensity': random.uniform(0.1, 1.0),
            'duration': random.uniform(0.1, 2.0),
            'context': random.choice(['cognitive', 'emotional', 'task_based', 'social'])
        }
        history.append(interaction)
    
    return history

def should_compute_forecast(state: Dict[str, Any]) -> bool:
    """Determine if forecast should be computed for current state"""
    
    # Compute forecast for significant states
    entropy = state.get('entropy', 0.0)
    depth = state.get('consciousness_depth', 0.0)
    tick = state.get('tick_number', 0)
    
    # Always compute for high entropy or deep consciousness
    if entropy > 0.6 or depth > 0.8:
        return True
    
    # Compute every few ticks
    if tick % 7 == 0:  # Every 7 ticks
        return True
    
    # Random chance
    if random.random() < 0.2:  # 20% chance
        return True
    
    return False

def create_forecast_from_consciousness(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create complete forecast from consciousness state"""
    
    # Import the new passion and acquaintance generators
    try:
        from processes.mock_passion import generate_mock_passion as generate_passion_obj
        from processes.mock_acquaintance import generate_mock_acquaintance as generate_acquaintance_obj
        
        # Determine passion tag based on mood and entropy
        entropy = state.get('entropy', 0.5)
        mood = state.get('mood', 'NEUTRAL')
        
        passion_tag = determine_passion_tag(entropy, mood)
        acquaintance_tag = determine_acquaintance_tag(state.get('scup', 50.0), mood)
        
        # Generate rich passion and acquaintance objects
        passion_obj = generate_passion_obj(passion_tag)
        acquaintance_obj = generate_acquaintance_obj(acquaintance_tag)
        
        # Convert to old format for compute_forecast compatibility
        passion = {
            'intensity': passion_obj.current_strength(),
            'coherence': 1.0 - passion_obj.fluidity,  # Inverse relationship
            'trajectory': determine_trajectory_from_passion(passion_obj)
        }
        
        acquaintance = {
            'familiarity': acquaintance_obj.familiarity,
            'trust': acquaintance_obj.trust_level,
            'resonance': acquaintance_obj.resonance
        }
        
    except ImportError:
        # Fallback to old simple generation
        passion = generate_mock_passion(
            entropy=state.get('entropy', 0.5),
            mood=state.get('mood', 'NEUTRAL'),
            tick=state.get('tick_number', 0)
        )
        
        acquaintance = generate_mock_acquaintance(
            scup=state.get('scup', 50.0),
            depth=state.get('consciousness_depth', 0.5),
            mood=state.get('mood', 'NEUTRAL')
        )
    
    # Compute forecast
    forecast = compute_forecast(passion, acquaintance)
    
    # Add consciousness context
    forecast['consciousness_context'] = {
        'source_tick': state.get('tick_number', 0),
        'source_entropy': state.get('entropy', 0.0),
        'source_mood': state.get('mood', 'UNKNOWN'),
        'passion_state': passion,
        'acquaintance_state': acquaintance
    }
    
    return forecast

def determine_passion_tag(entropy: float, mood: str) -> str:
    """Determine appropriate passion tag based on consciousness state"""
    
    # High entropy moods
    if entropy > 0.7:
        if mood in ['CHAOTIC', 'EXCITED']:
            return 'creation'
        elif mood in ['ANXIOUS', 'ENERGETIC']:
            return 'drift'
        else:
            return 'transcendence'
    
    # Medium entropy moods  
    elif entropy > 0.4:
        if mood in ['CONTEMPLATIVE', 'FOCUSED']:
            return 'reflection'
        elif mood in ['CALM', 'CONFIDENT']:
            return 'memory'
        else:
            return 'connection'
    
    # Low entropy - stable states
    else:
        if mood in ['CONTEMPLATIVE', 'NEUTRAL']:
            return 'reflection'
        else:
            return 'rebirth'

def determine_acquaintance_tag(scup: float, mood: str) -> str:
    """Determine appropriate acquaintance tag based on semantic alignment"""
    
    # High SCUP - strong semantic coherence
    if scup > 75.0:
        if mood in ['CONTEMPLATIVE', 'FOCUSED']:
            return 'reflection'
        elif mood in ['CALM', 'CONFIDENT']:
            return 'memory'
        else:
            return 'connection'
    
    # Medium SCUP
    elif scup > 40.0:
        if mood in ['EXCITED', 'ENERGETIC']:
            return 'creation'
        elif mood in ['CHAOTIC', 'ANXIOUS']:
            return 'drift'
        else:
            return 'rebirth'
    
    # Low SCUP - semantic instability
    else:
        return 'drift'

def determine_trajectory_from_passion(passion_obj) -> str:
    """Determine trajectory string from Passion object"""
    
    strength = passion_obj.current_strength()
    fluidity = passion_obj.fluidity
    
    if fluidity > 0.8:
        return 'volatile'
    elif strength > 0.7 and fluidity > 0.5:
        return 'ascending'
    elif strength < 0.3:
        return 'descending'
    else:
        return 'stable'

if __name__ == "__main__":
    # Test the mock forecast system
    test_states = [
        {
            'tick_number': 3001,
            'entropy': 0.8,
            'scup': 45.0,
            'mood': 'CHAOTIC',
            'consciousness_depth': 0.6
        },
        {
            'tick_number': 3002,
            'entropy': 0.3,
            'scup': 85.0,
            'mood': 'CONTEMPLATIVE',
            'consciousness_depth': 0.9
        }
    ]
    
    print("🔮 Testing DAWN Mock Forecast System")
    print("=" * 50)
    
    for i, state in enumerate(test_states):
        print(f"\n🧠 Test State {i+1}:")
        print(f"   Entropy: {state['entropy']:.3f}, SCUP: {state['scup']:.1f}")
        print(f"   Mood: {state['mood']}, Depth: {state['consciousness_depth']:.3f}")
        
        if should_compute_forecast(state):
            forecast = create_forecast_from_consciousness(state)
            
            print(f"   🔮 Forecast: {forecast['forecast']:.3f}")
            print(f"   ⚠️  Risk: {forecast['risk']}")
            print(f"   📊 Reliability: {forecast['reliability']:.3f}")
            print(f"   🎯 Confidence: {forecast['confidence']:.3f}")
        else:
            print("   ⏸️  No forecast computed for this state")
    
    print("\n✅ Mock forecast system test complete") 