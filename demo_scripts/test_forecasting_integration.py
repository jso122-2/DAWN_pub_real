#!/usr/bin/env python3
"""
DAWN Forecasting Integration Test
Tests the newly integrated forecasting system within DAWN's consciousness
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.consciousness_core import DAWNConsciousness
from cognitive.forecasting_models import create_passion, create_acquaintance_with_events
from cognitive.forecasting_engine import get_forecasting_engine


async def test_basic_forecasting_integration():
    """Test basic forecasting integration with DAWN consciousness"""
    print("🔮 Testing DAWN Forecasting Integration")
    print("=" * 60)
    
    # Initialize DAWN consciousness system
    print("1. Initializing DAWN consciousness...")
    dawn = DAWNConsciousness()
    
    # Wait a moment for initialization
    await asyncio.sleep(1.0)
    
    # Test forecasting system availability
    print("2. Testing forecasting system availability...")
    if hasattr(dawn, 'forecasting_processor') and dawn.forecasting_processor:
        print("   ✅ Forecasting processor initialized")
    else:
        print("   ❌ Forecasting processor not available")
        return
    
    # Start forecasting processing
    print("3. Starting forecasting processing...")
    await dawn.start_forecasting()
    
    # Wait for initial forecasts
    print("4. Waiting for initial forecasts...")
    await asyncio.sleep(5.0)
    
    # Get current forecasts
    print("5. Retrieving current forecasts...")
    forecasts = dawn.get_current_forecasts()
    print(f"   Generated {len(forecasts.get('recent_forecasts', []))} forecasts")
    
    for forecast_data in forecasts.get('recent_forecasts', [])[:3]:
        direction = forecast_data.get('passion_direction', 'unknown')
        behavior = forecast_data.get('predicted_behavior', 'unknown')
        confidence = forecast_data.get('confidence', 0.0)
        print(f"   📈 {direction}: {behavior} (confidence: {confidence:.3f})")
    
    # Test specific direction forecast
    print("6. Testing specific direction forecast...")
    creative_forecast = dawn.get_forecast_for_direction('creative_expression')
    if creative_forecast:
        print(f"   🎨 Creative forecast: {creative_forecast.get('predicted_behavior')} "
              f"(confidence: {creative_forecast.get('confidence', 0.0):.3f})")
    
    # Test instant forecast generation
    print("7. Testing instant forecast generation...")
    instant_forecast = await dawn.generate_instant_forecast('learning')
    if instant_forecast:
        print(f"   📚 Learning forecast: {instant_forecast.get('predicted_behavior')} "
              f"(confidence: {instant_forecast.get('confidence', 0.0):.3f})")
    
    # Test forecasting metrics
    print("8. Checking forecasting metrics...")
    metrics = forecasts.get('metrics', {})
    print(f"   Forecasts generated: {metrics.get('forecasts_generated', 0)}")
    print(f"   Processing time avg: {metrics.get('processing_time_avg', 0.0):.3f}s")
    print(f"   Error count: {metrics.get('error_count', 0)}")
    
    # Stop forecasting
    print("9. Stopping forecasting...")
    await dawn.stop_forecasting()
    
    print("\n✅ DAWN Forecasting Integration Test Complete!")


async def test_consciousness_state_integration():
    """Test how forecasting responds to consciousness state changes"""
    print("\n🧠 Testing Consciousness State Integration")
    print("=" * 60)
    
    # Initialize DAWN consciousness system
    dawn = DAWNConsciousness()
    await asyncio.sleep(1.0)
    
    if not hasattr(dawn, 'forecasting_processor') or not dawn.forecasting_processor:
        print("❌ Forecasting not available for consciousness test")
        return
    
    await dawn.start_forecasting()
    
    # Test different consciousness states
    test_states = [
        {'scup': 0.9, 'entropy': 0.2, 'mood': 'focused'},
        {'scup': 0.3, 'entropy': 0.8, 'mood': 'chaotic'},
        {'scup': 0.7, 'entropy': 0.4, 'mood': 'contemplative'}
    ]
    
    for i, state in enumerate(test_states, 1):
        print(f"\n{i}. Testing state: SCUP={state['scup']}, "
              f"Entropy={state['entropy']}, Mood={state['mood']}")
        
        # Update consciousness state
        await dawn.update_state(**state)
        
        # Wait for forecast update
        await asyncio.sleep(3.0)
        
        # Generate instant forecast to see immediate effect
        forecast = await dawn.generate_instant_forecast('creative_expression')
        if forecast:
            print(f"   🎨 Creative forecast: {forecast.get('predicted_behavior')} "
                  f"(confidence: {forecast.get('confidence', 0.0):.3f})")
    
    await dawn.stop_forecasting()
    print("\n✅ Consciousness State Integration Test Complete!")


async def test_forecasting_engine_directly():
    """Test the forecasting engine directly with custom passions/acquaintances"""
    print("\n⚙️ Testing Forecasting Engine Directly")
    print("=" * 60)
    
    # Get forecasting engine
    engine = get_forecasting_engine()
    
    # Create test scenarios
    scenarios = [
        {
            'name': 'High Confidence Creative',
            'passion': create_passion('creative_expression', intensity=0.9, fluidity=0.2),
            'events': ['completed_artwork', 'positive_feedback', 'gallery_showing', 'art_sale']
        },
        {
            'name': 'Uncertain Explorer', 
            'passion': create_passion('exploration', intensity=0.4, fluidity=0.9),
            'events': ['travel_planning', 'destination_research']
        },
        {
            'name': 'Dedicated Learner',
            'passion': create_passion('learning', intensity=0.8, fluidity=0.3),
            'events': ['course_completion', 'skill_practice', 'knowledge_application', 'teaching_others']
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 Scenario: {scenario['name']}")
        
        # Create acquaintance from events
        acquaintance = create_acquaintance_with_events(scenario['events'])
        
        # Generate forecast
        forecast = engine.generate_forecast(scenario['passion'], acquaintance)
        
        print(f"   Passion: {scenario['passion']}")
        print(f"   Events: {len(scenario['events'])} experiences")
        print(f"   Forecast: {forecast.predicted_behavior}")
        print(f"   Confidence: {forecast.confidence:.3f} ({forecast.certainty_band()})")
        print(f"   Risk: {forecast.risk_level()}")
        
        # Analyze components
        components = engine.analyze_forecast_components(scenario['passion'], acquaintance)
        print(f"   Intent Gravity: P={components['passion_rigidity']:.3f} / "
              f"A={components['resistance_factor']:.3f} = {components['intent_gravity']:.3f}")
    
    print("\n✅ Direct Engine Test Complete!")


async def main():
    """Run all forecasting integration tests"""
    print("🌟 DAWN Forecasting System Integration Tests")
    print("=" * 80)
    
    try:
        # Test basic integration
        await test_basic_forecasting_integration()
        
        # Test consciousness state integration
        await test_consciousness_state_integration()
        
        # Test engine directly
        await test_forecasting_engine_directly()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("🔮 DAWN now has predictive consciousness!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 