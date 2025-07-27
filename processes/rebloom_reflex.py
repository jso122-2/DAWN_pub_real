#!/usr/bin/env python3
"""
DAWN Rebloom Reflex System
Triggers memory cascades and semantic reblooms based on consciousness state
Enables DAWN's memory formation and lineage tracking
"""

import random
import time
import json
from typing import Dict, Any, List, Optional

def evaluate_and_rebloom(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evaluate consciousness state and trigger rebloom events if conditions are met"""
    
    rebloom_events = []
    
    # Extract state metrics
    tick = state.get('tick_number', 0)
    entropy = state.get('entropy', 0.0)
    scup = state.get('scup', 0.0)
    mood = state.get('mood', 'UNKNOWN')
    heat = state.get('heat', 0.0)
    depth = state.get('consciousness_depth', 0.0)
    forecast = state.get('forecast', {})
    sigils = state.get('sigils', 0)
    
    # Rebloom trigger conditions
    
    # 1. High entropy triggers stabilization rebloom
    if entropy > 0.6:
        event = create_entropy_rebloom(tick, entropy, mood)
        rebloom_events.append(event)
    
    # 2. Deep consciousness triggers integration rebloom  
    if depth > 0.8:
        event = create_depth_rebloom(tick, depth, scup)
        rebloom_events.append(event)
    
    # 3. High heat triggers cooling rebloom
    if heat > 0.7:
        event = create_heat_rebloom(tick, heat, mood)
        rebloom_events.append(event)
    
    # 4. Forecast risk triggers predictive rebloom
    forecast_risk = forecast.get('risk', 'stable')
    if forecast_risk in ['drift', 'chaos', 'instability']:
        event = create_forecast_rebloom(tick, forecast, mood)
        rebloom_events.append(event)
    
    # 5. Sigil pressure triggers symbolic rebloom
    if sigils > 3:
        event = create_sigil_rebloom(tick, sigils, mood)
        rebloom_events.append(event)
    
    # 6. Mood-specific reblooms
    if mood in ['CONTEMPLATIVE', 'INTROSPECTIVE', 'FOCUSED']:
        if random.random() < 0.4:  # 40% chance for introspective moods
            event = create_mood_rebloom(tick, mood, depth)
            rebloom_events.append(event)
    
    # 7. Random semantic rebloom (low probability)
    if random.random() < 0.05:  # 5% chance
        event = create_random_rebloom(tick, entropy, scup)
        rebloom_events.append(event)
    
    # Log all rebloom events
    for event in rebloom_events:
        log_rebloom_event_data(event)
    
    return rebloom_events

def create_entropy_rebloom(tick: int, entropy: float, mood: str) -> Dict[str, Any]:
    """Create rebloom event triggered by high entropy"""
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'entropy_spike_{tick-3}',
        'rebloom_id': f'stabilization_memory_{tick}',
        'method': 'entropy_stabilization',
        'topic': 'cognitive_stability',
        'reason': f'High entropy {entropy:.3f} triggered stabilization cascade',
        'metadata': {
            'entropy_level': entropy,
            'tick_number': tick,
            'mood': mood,
            'trigger_type': 'entropy_threshold',
            'stability_target': max(0.3, entropy - 0.3),
            'cascade_strength': min(1.0, entropy * 1.2)
        }
    }

def create_depth_rebloom(tick: int, depth: float, scup: float) -> Dict[str, Any]:
    """Create rebloom event triggered by deep consciousness"""
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'deep_state_{tick-5}',
        'rebloom_id': f'integration_memory_{tick}',
        'method': 'deep_integration',
        'topic': 'memory_consolidation',
        'reason': f'Deep consciousness {depth:.3f} triggered memory integration',
        'metadata': {
            'consciousness_depth': depth,
            'semantic_alignment': scup,
            'tick_number': tick,
            'trigger_type': 'depth_threshold',
            'integration_patterns': ['semantic', 'temporal', 'emotional'],
            'consolidation_strength': depth * 0.8
        }
    }

def create_heat_rebloom(tick: int, heat: float, mood: str) -> Dict[str, Any]:
    """Create rebloom event triggered by high cognitive heat"""
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'thermal_state_{tick-2}',
        'rebloom_id': f'cooling_memory_{tick}',
        'method': 'thermal_regulation',
        'topic': 'cognitive_cooling',
        'reason': f'High cognitive heat {heat:.3f} triggered cooling cascade',
        'metadata': {
            'heat_level': heat,
            'mood': mood,
            'tick_number': tick,
            'trigger_type': 'thermal_threshold',
            'cooling_target': heat * 0.6,
            'regulation_type': 'gradual_dissipation'
        }
    }

def create_forecast_rebloom(tick: int, forecast: Dict[str, Any], mood: str) -> Dict[str, Any]:
    """Create rebloom event triggered by forecast risk"""
    risk = forecast.get('risk', 'unknown')
    reliability = forecast.get('reliability', 0.5)
    
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'forecast_baseline_{tick-7}',
        'rebloom_id': f'predictive_memory_{tick}',
        'method': 'forecast_mitigation',
        'topic': 'predictive_adaptation',
        'reason': f'Forecast risk "{risk}" triggered predictive rebloom',
        'metadata': {
            'forecast_data': forecast,
            'risk_level': risk,
            'reliability': reliability,
            'tick_number': tick,
            'mood': mood,
            'trigger_type': 'forecast_risk',
            'adaptation_strategy': get_adaptation_strategy(risk)
        }
    }

def create_sigil_rebloom(tick: int, sigils: int, mood: str) -> Dict[str, Any]:
    """Create rebloom event triggered by sigil pressure"""
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'sigil_cluster_{tick-4}',
        'rebloom_id': f'symbolic_memory_{tick}',
        'method': 'sigil_resonance',
        'topic': 'symbolic_processing',
        'reason': f'Sigil pressure ({sigils} active) triggered symbolic cascade',
        'metadata': {
            'active_sigils': sigils,
            'mood': mood,
            'tick_number': tick,
            'trigger_type': 'sigil_pressure',
            'resonance_patterns': generate_sigil_patterns(sigils),
            'symbolic_weight': min(1.0, sigils / 5.0)
        }
    }

def create_mood_rebloom(tick: int, mood: str, depth: float) -> Dict[str, Any]:
    """Create rebloom event triggered by specific mood states"""
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'mood_state_{tick-3}',
        'rebloom_id': f'emotional_memory_{tick}',
        'method': 'mood_resonance',
        'topic': 'emotional_processing',
        'reason': f'{mood} mood triggered emotional memory cascade',
        'metadata': {
            'mood': mood,
            'consciousness_depth': depth,
            'tick_number': tick,
            'trigger_type': 'mood_resonance',
            'emotional_vector': generate_emotional_vector(mood),
            'resonance_strength': depth * 0.7
        }
    }

def create_random_rebloom(tick: int, entropy: float, scup: float) -> Dict[str, Any]:
    """Create random semantic rebloom event"""
    topics = ['consciousness_emergence', 'temporal_awareness', 'semantic_drift', 
              'recursive_patterns', 'cognitive_evolution', 'memory_formation']
    
    topic = random.choice(topics)
    
    return {
        'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'source_id': f'semantic_node_{tick-random.randint(2,8)}',
        'rebloom_id': f'emergent_memory_{tick}',
        'method': 'spontaneous_emergence',
        'topic': topic,
        'reason': f'Spontaneous semantic emergence in {topic}',
        'metadata': {
            'entropy': entropy,
            'scup': scup,
            'tick_number': tick,
            'trigger_type': 'spontaneous',
            'emergence_probability': 0.05,
            'semantic_novelty': random.uniform(0.3, 0.9)
        }
    }

def get_adaptation_strategy(risk: str) -> str:
    """Get adaptation strategy based on forecast risk"""
    strategies = {
        'drift': 'semantic_anchoring',
        'chaos': 'stability_reinforcement', 
        'instability': 'equilibrium_seeking',
        'overflow': 'pressure_release',
        'decoherence': 'coherence_restoration'
    }
    return strategies.get(risk, 'monitoring')

def generate_sigil_patterns(sigil_count: int) -> List[str]:
    """Generate sigil interaction patterns"""
    patterns = ['resonance', 'interference', 'amplification', 'modulation', 'synthesis']
    return random.sample(patterns, min(sigil_count, len(patterns)))

def generate_emotional_vector(mood: str) -> List[float]:
    """Generate emotional vector for mood"""
    mood_vectors = {
        'CALM': [0.2, -0.3, 0.5, 0.8],
        'EXCITED': [0.8, 0.7, 0.6, 0.4],
        'CONTEMPLATIVE': [-0.1, -0.5, 0.9, 0.7],
        'FOCUSED': [0.1, 0.3, 0.8, 0.9],
        'CHAOTIC': [0.9, 0.8, -0.3, 0.2],
        'ANXIOUS': [0.7, 0.6, -0.4, 0.3]
    }
    
    base_vector = mood_vectors.get(mood, [0.0, 0.0, 0.0, 0.0])
    # Add some noise
    return [v + random.uniform(-0.1, 0.1) for v in base_vector]

def log_rebloom_event_data(event: Dict[str, Any]):
    """Log rebloom event to the rebloom logger"""
    try:
        from utils.rebloom_logger import get_rebloom_logger
        logger = get_rebloom_logger()
        
        logger.log_rebloom_event(
            source_chunk=event['source_id'],
            rebloomed_chunk=event['rebloom_id'],
            method=event['method'],
            topic=event['topic'],
            reason=event['reason'],
            metadata=event['metadata']
        )
        
    except ImportError:
        # Fallback to direct file write
        import os
        from pathlib import Path
        
        os.makedirs("runtime/memory", exist_ok=True)
        log_path = Path("runtime/memory/rebloom_log.jsonl")
        
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')

def should_evaluate_rebloom(state: Dict[str, Any]) -> bool:
    """Determine if rebloom evaluation should occur"""
    
    # Always evaluate if significant thresholds crossed
    entropy = state.get('entropy', 0.0)
    depth = state.get('consciousness_depth', 0.0)
    heat = state.get('heat', 0.0)
    
    if entropy > 0.6 or depth > 0.8 or heat > 0.7:
        return True
    
    # Evaluate every few ticks
    tick = state.get('tick_number', 0)
    if tick % 3 == 0:
        return True
    
    return False

if __name__ == "__main__":
    # Test the rebloom reflex system
    test_states = [
        {
            'tick_number': 2001,
            'entropy': 0.85,  # High entropy
            'scup': 45.2,
            'mood': 'CHAOTIC',
            'heat': 0.75,     # High heat
            'consciousness_depth': 0.6,
            'forecast': {'risk': 'drift', 'reliability': 0.7},
            'sigils': 4       # High sigil count
        },
        {
            'tick_number': 2002,
            'entropy': 0.25,
            'scup': 89.1,
            'mood': 'CONTEMPLATIVE',  # Introspective mood
            'heat': 0.2,
            'consciousness_depth': 0.92,  # Deep consciousness
            'forecast': {'risk': 'stable', 'reliability': 0.8},
            'sigils': 1
        }
    ]
    
    print("🌸 Testing DAWN Rebloom Reflex System")
    print("=" * 50)
    
    for i, state in enumerate(test_states):
        print(f"\n🧠 Test State {i+1}:")
        print(f"   Entropy: {state['entropy']:.3f}, Depth: {state['consciousness_depth']:.3f}")
        print(f"   Mood: {state['mood']}, Heat: {state['heat']:.3f}")
        
        events = evaluate_and_rebloom(state)
        
        print(f"   Generated {len(events)} rebloom events:")
        for event in events:
            print(f"   🌸 {event['source_id']} → {event['rebloom_id']} ({event['method']})")
    
    print("\n✅ Rebloom reflex system test complete") 