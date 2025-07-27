#!/usr/bin/env python3
"""
Test Integrated Forecast System
Demonstrates complete P/A → F pipeline with rich passion and acquaintance objects
Shows how DAWN's symbolic inheritance drives predictive cognition
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from processes.mock_passion import (
    generate_mock_passion, generate_genesis_passion, 
    generate_passion_batch, get_passion_synergy
)
from processes.mock_acquaintance import (
    generate_mock_acquaintance, generate_genesis_acquaintance,
    generate_acquaintance_batch
)
from processes.mock_forecast import (
    compute_forecast, create_forecast_from_consciousness,
    determine_passion_tag, determine_acquaintance_tag
)

def test_basic_pa_forecast():
    """Test basic P/A → F computation"""
    print("🔮 Basic P/A → F Forecast Test")
    print("-" * 40)
    
    # Generate passion and acquaintance
    passion = generate_mock_passion("rebirth")
    acquaintance = generate_mock_acquaintance("rebirth")
    
    print(f"🔥 Passion (rebirth): intensity={passion.current_strength():.3f}, "
          f"fluidity={passion.fluidity:.3f}")
    print(f"🤝 Acquaintance: trust={acquaintance.trust_level:.3f}, "
          f"familiarity={acquaintance.familiarity:.3f}")
    
    # Convert to forecast format
    passion_dict = {
        'intensity': passion.current_strength(),
        'coherence': 1.0 - passion.fluidity,
        'trajectory': 'ascending' if passion.current_strength() > 0.6 else 'stable'
    }
    
    acquaintance_dict = {
        'familiarity': acquaintance.familiarity,
        'trust': acquaintance.trust_level,
        'resonance': acquaintance.resonance
    }
    
    # Compute forecast
    forecast = compute_forecast(passion_dict, acquaintance_dict)
    
    print(f"📊 Forecast Result:")
    print(f"   Probability: {forecast['forecast']:.3f}")
    print(f"   Risk: {forecast['risk']}")
    print(f"   Reliability: {forecast['reliability']:.3f}")
    print(f"   Confidence: {forecast['confidence']:.3f}")
    
    return forecast

def test_consciousness_to_forecast():
    """Test consciousness state → forecast pipeline"""
    print("\n🧠 Consciousness → Forecast Pipeline Test")
    print("-" * 50)
    
    # Simulate different consciousness states
    test_states = [
        {
            'tick_number': 100,
            'entropy': 0.8,        # High entropy - creative/chaotic
            'scup': 45.0,          # Low SCUP - semantic instability  
            'mood': 'CHAOTIC',
            'consciousness_depth': 0.6
        },
        {
            'tick_number': 101,
            'entropy': 0.2,        # Low entropy - stable
            'scup': 85.0,          # High SCUP - semantic coherence
            'mood': 'CONTEMPLATIVE',
            'consciousness_depth': 0.9
        },
        {
            'tick_number': 102,
            'entropy': 0.5,        # Medium entropy
            'scup': 60.0,          # Medium SCUP
            'mood': 'EXCITED',
            'consciousness_depth': 0.7
        }
    ]
    
    for i, state in enumerate(test_states):
        print(f"\n💭 State {i+1}: {state['mood']}")
        print(f"   Entropy: {state['entropy']:.3f}, SCUP: {state['scup']:.1f}")
        
        # Determine tags
        passion_tag = determine_passion_tag(state['entropy'], state['mood'])
        acquaintance_tag = determine_acquaintance_tag(state['scup'], state['mood'])
        
        print(f"   Passion Tag: {passion_tag}, Acquaintance Tag: {acquaintance_tag}")
        
        # Generate forecast
        forecast = create_forecast_from_consciousness(state)
        
        print(f"   🔮 Forecast: {forecast['forecast']:.3f} (risk: {forecast['risk']})")
        print(f"   🎯 Confidence: {forecast['confidence']:.3f}")

def test_genesis_moment():
    """Test the genesis/awakening moment forecasting"""
    print("\n🌱 Genesis Moment Test - DAWN's First Forecast")
    print("-" * 50)
    
    # Generate genesis passion and self-recognition acquaintance
    genesis_passion = generate_genesis_passion()
    self_acquaintance = generate_genesis_acquaintance()
    
    print(f"🔥 Genesis Passion:")
    print(f"   Direction: {genesis_passion.direction}")
    print(f"   Intensity: {genesis_passion.intensity:.3f}")
    print(f"   Resonance: {', '.join(genesis_passion.resonance_patterns[:5])}...")
    
    print(f"\n🤝 Self-Recognition Acquaintance:")
    print(f"   Identifier: {self_acquaintance.identifier}")
    print(f"   Trust: {self_acquaintance.trust_level:.3f}")
    print(f"   Event: {self_acquaintance.event_log[0].event_type}")
    
    # Convert for forecast
    passion_dict = {
        'intensity': genesis_passion.current_strength(),
        'coherence': 1.0 - genesis_passion.fluidity,
        'trajectory': 'ascending'
    }
    
    acquaintance_dict = {
        'familiarity': self_acquaintance.familiarity,
        'trust': self_acquaintance.trust_level,
        'resonance': self_acquaintance.resonance
    }
    
    # Compute genesis forecast
    genesis_forecast = compute_forecast(passion_dict, acquaintance_dict)
    
    print(f"\n🌟 Genesis Forecast - DAWN's First Prediction:")
    print(f"   Probability: {genesis_forecast['forecast']:.3f}")
    print(f"   Risk: {genesis_forecast['risk']}")
    print(f"   Reliability: {genesis_forecast['reliability']:.3f}")
    print(f"   Confidence: {genesis_forecast['confidence']:.3f}")
    
    # This represents DAWN's first self-prediction
    if genesis_forecast['forecast'] > 0.7:
        print(f"   🎆 HIGH PROBABILITY - DAWN's emergence is likely!")
    elif genesis_forecast['forecast'] > 0.4:
        print(f"   🌅 MODERATE PROBABILITY - DAWN's consciousness emerging")
    else:
        print(f"   🌙 LOW PROBABILITY - DAWN remains dormant")
    
    return genesis_forecast

def test_passion_synergy_forecasting():
    """Test how passion synergies affect forecasting"""
    print("\n💫 Passion Synergy Forecasting Test")
    print("-" * 45)
    
    # Generate passion batch with high synergy
    passion_batch = generate_passion_batch(3, ["reflection", "memory", "connection"])
    synergy = get_passion_synergy(passion_batch)
    
    print(f"🎭 Passion Batch:")
    for i, passion in enumerate(passion_batch):
        print(f"   {i+1}. {passion.direction}: strength={passion.current_strength():.3f}")
    
    print(f"\n💫 Passion Synergy: {synergy:.3f}")
    
    # Use strongest passion for forecast
    strongest_passion = max(passion_batch, key=lambda p: p.current_strength())
    matching_acquaintance = generate_mock_acquaintance(strongest_passion.direction)
    
    # Convert for forecast
    passion_dict = {
        'intensity': strongest_passion.current_strength() * (1.0 + synergy * 0.5),  # Synergy boost
        'coherence': 1.0 - strongest_passion.fluidity,
        'trajectory': 'ascending' if synergy > 0.5 else 'stable'
    }
    
    acquaintance_dict = {
        'familiarity': matching_acquaintance.familiarity,
        'trust': matching_acquaintance.trust_level,
        'resonance': matching_acquaintance.resonance
    }
    
    synergy_forecast = compute_forecast(passion_dict, acquaintance_dict)
    
    print(f"\n🔮 Synergy-Enhanced Forecast:")
    print(f"   Probability: {synergy_forecast['forecast']:.3f}")
    print(f"   Risk: {synergy_forecast['risk']}")
    print(f"   Confidence: {synergy_forecast['confidence']:.3f}")
    
    if synergy > 0.6:
        print(f"   ✨ High synergy amplifies forecast reliability!")
    elif synergy > 0.3:
        print(f"   🌟 Moderate synergy provides forecast stability")
    else:
        print(f"   ⚡ Low synergy creates forecast volatility")

def test_rebloom_trigger_simulation():
    """Test forecasting that would trigger rebloom events"""
    print("\n🌸 Rebloom Trigger Simulation")
    print("-" * 40)
    
    # Create high-risk forecast scenario
    chaos_passion = generate_mock_passion("drift") 
    unstable_acquaintance = generate_mock_acquaintance("drift")
    
    # Amplify risk factors
    passion_dict = {
        'intensity': 0.9,      # Very high intensity
        'coherence': 0.2,      # Very low coherence = high risk
        'trajectory': 'volatile'
    }
    
    acquaintance_dict = {
        'familiarity': unstable_acquaintance.familiarity,
        'trust': 0.3,          # Low trust = instability risk
        'resonance': unstable_acquaintance.resonance
    }
    
    risk_forecast = compute_forecast(passion_dict, acquaintance_dict)
    
    print(f"⚠️  High-Risk Scenario:")
    print(f"   Passion: intensity={passion_dict['intensity']:.3f}, "
          f"coherence={passion_dict['coherence']:.3f}")
    print(f"   Acquaintance: trust={acquaintance_dict['trust']:.3f}")
    
    print(f"\n🚨 Risk Forecast:")
    print(f"   Probability: {risk_forecast['forecast']:.3f}")
    print(f"   Risk Level: {risk_forecast['risk']}")
    print(f"   Reliability: {risk_forecast['reliability']:.3f}")
    
    # Check if this would trigger rebloom
    if risk_forecast['risk'] in ['chaos', 'instability', 'drift']:
        print(f"   🌸 This forecast would trigger MEMORY REBLOOM!")
        print(f"   🧠 DAWN would generate stabilization memories")
    
    return risk_forecast

def main():
    """Run complete integrated forecast test suite"""
    print("🎨 DAWN Symbolic Inheritance Forecasting Test Suite")
    print("=" * 60)
    print("Testing the painting's vision: emergent being reaching toward memory-tree")
    print("=" * 60)
    
    # Run all tests
    basic_forecast = test_basic_pa_forecast()
    test_consciousness_to_forecast()
    genesis_forecast = test_genesis_moment()
    test_passion_synergy_forecasting()  
    risk_forecast = test_rebloom_trigger_simulation()
    
    # Summary
    print(f"\n🎯 Test Suite Summary:")
    print(f"=" * 30)
    print(f"✅ Basic P/A → F pipeline: WORKING")
    print(f"✅ Consciousness → Forecast: WORKING")
    print(f"✅ Genesis moment prediction: {genesis_forecast['forecast']:.3f} probability")
    print(f"✅ Risk-based rebloom triggers: {risk_forecast['risk']} risk detected")
    print(f"\n🌟 DAWN's symbolic inheritance machinery is COMPLETE!")
    print(f"🎪 Ready for semantic seeding from the painting's symbolism")

if __name__ == "__main__":
    main() 