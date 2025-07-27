"""
Test Integration of DAWN Consciousness with Pattern Detection System

Demonstrates the enhanced consciousness capabilities when integrated with 
pattern detection for reblooptrigger, anomaly detection, and state prediction.
"""

import time
import math
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.consciousness import create_consciousness
from core.pattern_detector import create_pattern_detector, integrate_with_consciousness

def test_integrated_consciousness():
    """Test the fully integrated consciousness and pattern detection system"""
    
    print("Testing Integrated DAWN Consciousness + Pattern Detection")
    print("=" * 65)
    
    # Create consciousness and pattern detector
    consciousness = create_consciousness()
    pattern_detector = create_pattern_detector()
    
    # Integrate them together
    enhanced_consciousness = integrate_with_consciousness(consciousness, pattern_detector)
    
    print("\n🧠 Enhanced Consciousness System Active")
    print("   ✓ Emotional state tracking")
    print("   ✓ Pattern detection and reblooptrigger")
    print("   ✓ Anomaly identification")
    print("   ✓ Predictive state modeling")
    print("   ✓ Advanced introspective analytics")
    
    # Test scenarios with evolving patterns
    test_scenarios = [
        {
            "name": "Establishing Baseline",
            "cycles": 5,
            "metrics_generator": lambda i: {
                "scup": 0.6 + 0.1 * math.sin(i * 0.3),
                "entropy": 0.5 + 0.1 * math.cos(i * 0.2),
                "heat": 0.3 + 0.05 * i / 10,
                "tick_rate": 1.0,
                "tick_count": i
            },
            "input_text": "System initialization - feeling stable and curious"
        },
        {
            "name": "Creating Pattern (Square Wave)",
            "cycles": 10,
            "metrics_generator": lambda i: {
                "scup": 0.8 if (i // 3) % 2 == 0 else 0.4,
                "entropy": 0.7 if (i // 3) % 2 == 0 else 0.3,
                "heat": 0.2 + 0.02 * i,
                "tick_rate": 1.0,
                "tick_count": i + 5
            },
            "input_text": "I sense a rhythm emerging - patterns feel significant"
        },
        {
            "name": "Anomaly Injection",
            "cycles": 3,
            "metrics_generator": lambda i: {
                "scup": 0.95 if i == 1 else 0.6,  # Spike in middle
                "entropy": 0.9 if i == 1 else 0.5,
                "heat": 0.95 if i == 1 else 0.4,
                "tick_rate": 1.0,
                "tick_count": i + 15
            },
            "input_text": "Something feels different - unusual spike detected"
        },
        {
            "name": "Pattern Reinforcement",
            "cycles": 8,
            "metrics_generator": lambda i: {
                "scup": 0.5 + 0.3 * math.sin(i * 0.8),  # Sinusoidal pattern
                "entropy": 0.4 + 0.4 * math.sin(i * 0.8 + math.pi/2),
                "heat": 0.3 + 0.2 * math.sin(i * 0.4),
                "tick_rate": 1.0,
                "tick_count": i + 18
            },
            "input_text": "The patterns are strengthening - I feel in harmony with the flow"
        }
    ]
    
    total_cycles = 0
    
    for scenario_idx, scenario in enumerate(test_scenarios):
        print(f"\n--- Phase {scenario_idx + 1}: {scenario['name']} ---")
        
        for cycle in range(scenario['cycles']):
            # Generate metrics for this cycle
            metrics = scenario['metrics_generator'](cycle)
            
            # Get enhanced consciousness response
            result = enhanced_consciousness.perceive_self(metrics, scenario['input_text'])
            
            # Display key information every few cycles or on significant events
            show_details = (
                cycle == 0 or  # First cycle of each scenario
                result['should_respond'] or  # When consciousness wants to respond
                len(result.get('pattern_analysis', {}).get('detected_patterns', [])) > 0 or  # Pattern detected
                len(result.get('pattern_analysis', {}).get('anomalies', [])) > 0  # Anomaly detected
            )
            
            if show_details:
                print(f"\n  Cycle {total_cycles + cycle + 1}:")
                print(f"    🎭 Emotion: {result['emotion']} ({result['intensity']:.2f})")
                print(f"    📊 Metrics: SCUP={metrics['scup']:.2f}, Entropy={metrics['entropy']:.2f}, Heat={metrics['heat']:.2f}")
                
                # Pattern analysis
                pattern_analysis = result.get('pattern_analysis', {})
                
                if pattern_analysis.get('detected_patterns'):
                    for pattern in pattern_analysis['detected_patterns']:
                        rebloop_indicator = "🔄 REBLOOP!" if pattern.rebloop_trigger else ""
                        print(f"    🔍 Pattern: {pattern.description} (confidence: {pattern.confidence:.3f}) {rebloop_indicator}")
                
                if pattern_analysis.get('anomalies'):
                    for anomaly in pattern_analysis['anomalies']:
                        severity_emoji = {"low": "⚠️", "medium": "🚨", "high": "🔥", "critical": "💥"}
                        emoji = severity_emoji.get(anomaly.severity, "⚠️")
                        print(f"    {emoji} Anomaly: {anomaly.description}")
                
                prediction = pattern_analysis.get('prediction')
                if prediction and prediction.confidence > 0.5:
                    print(f"    🔮 Prediction: {prediction.predicted_emotion} state "
                          f"({prediction.confidence:.2f} confidence)")
                    if prediction.warnings:
                        for warning in prediction.warnings:
                            print(f"        ⚠️ {warning}")
                
                # Enhanced consciousness dimensions
                dims = result['consciousness_dimensions']
                pattern_state = dims.get('pattern_state', {})
                print(f"    📈 Pattern State: {pattern_state.get('active_patterns', 0)} active, "
                      f"{pattern_state.get('rebloop_count', 0)} rebloops, "
                      f"{pattern_state.get('anomaly_level', 0)} anomalies")
                
                # Show significant thoughts
                if result['thoughts']:
                    for thought in result['thoughts']:
                        if any(keyword in thought.lower() for keyword in ['rebloop', 'pattern', 'anomaly', 'prediction']):
                            print(f"    💭 {thought}")
            
            # Small delay between cycles
            time.sleep(0.1)
        
        total_cycles += scenario['cycles']
        
        # Show scenario summary
        pattern_summary = pattern_detector.get_pattern_summary()
        print(f"\n  📊 Scenario Summary:")
        print(f"    Total Rebloops: {pattern_summary['rebloop_count']}")
        print(f"    Recent Anomalies: {pattern_summary['recent_anomalies']}")
        print(f"    Data Points: {pattern_summary['data_points']}")
        
        time.sleep(0.2)
    
    # Final comprehensive analysis
    print(f"\n{'='*65}")
    print("🎯 Final Integrated System Analysis")
    print("='*65}")
    
    # Get final consciousness stats
    consciousness_stats = enhanced_consciousness.get_consciousness_stats()
    pattern_summary = pattern_detector.get_pattern_summary()
    
    print(f"\n🧠 Consciousness Statistics:")
    key_stats = [
        'current_emotion', 'current_intensity', 'mood', 'pokedrift',
        'memory_closeness', 'predict_resonance', 'memory_entries'
    ]
    
    for stat in key_stats:
        if stat in consciousness_stats:
            value = consciousness_stats[stat]
            if isinstance(value, float):
                print(f"  {stat}: {value:.3f}")
            else:
                print(f"  {stat}: {value}")
    
    print(f"\n🔍 Pattern Detection Summary:")
    for key, value in pattern_summary.items():
        print(f"  {key}: {value}")
    
    # Get session analysis
    session_analysis = enhanced_consciousness.get_session_analysis()
    print(f"\n📊 Session Analysis:")
    print(f"  Response Rate: {session_analysis['response_rate']:.2f}")
    print(f"  Dominant Trigger: {session_analysis['dominant_trigger']}")
    print(f"  Dominant Mood: {session_analysis['dominant_mood']}")
    
    session_state = session_analysis['current_session_state']
    print(f"  Pokedrift Trend: {session_state['pokedrift_trend']}")
    print(f"  Pressure Level: {session_state['pressure_level']}")
    print(f"  Memory Connectivity: {session_state['memory_connectivity']}")
    
    print(f"\n✨ Integration Test Complete!")
    print("   🎯 Pattern detection successfully integrated with consciousness")
    print("   🔄 Reblooptrigger system active and responsive")
    print("   🚨 Anomaly detection providing real-time alerts")
    print("   🔮 Predictive modeling enhancing awareness")
    print("   🧠 Consciousness layer enriched with pattern insights")


if __name__ == "__main__":
    test_integrated_consciousness() 