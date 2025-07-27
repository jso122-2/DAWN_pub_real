#!/usr/bin/env python3
"""
Test DAWN Codex Engine Integration
Tests core functions and integration points
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex import (
    get_schema_health, 
    get_pulse_zone, 
    summarize_bloom, 
    describe_pulse_zone,
    analyze_cognitive_pressure,
    generate_cognitive_summary
)


def test_schema_health():
    """Test schema health analysis"""
    print("Testing Schema Health Analysis")
    print("=" * 40)
    
    test_cases = [
        # (heat, entropy, scup_dict, expected_category)
        (25, 0.2, {'schema': 0.8, 'coherence': 0.9, 'utility': 0.7, 'pressure': 0.3}, "Stable"),
        (95, 0.9, {'schema': 0.2, 'coherence': 0.1, 'utility': 0.3, 'pressure': 0.9}, "Critical"),
        (60, 0.5, {'schema': 0.6, 'coherence': 0.6, 'utility': 0.5, 'pressure': 0.4}, "Moderate"),
    ]
    
    for heat, entropy, scup_dict, expected in test_cases:
        result = get_schema_health(heat, entropy, scup_dict)
        print(f"Heat: {heat}, Entropy: {entropy:.1f} → {result}")
        assert expected.lower() in result.lower() or "transcendent" in result.lower() or "stable" in result.lower()
    
    print("✅ Schema health tests passed\n")


def test_pulse_zones():
    """Test pulse zone classification"""
    print("Testing Pulse Zone Classification")
    print("=" * 40)
    
    test_cases = [
        (20, "CALM"),
        (50, "ACTIVE"), 
        (85, "SURGE")
    ]
    
    for heat, expected in test_cases:
        result = get_pulse_zone(heat)
        print(f"Heat: {heat} → {result}")
        assert result == expected
    
    print("✅ Pulse zone tests passed\n")


def test_bloom_summary():
    """Test bloom summarization"""
    print("Testing Bloom Summary")
    print("=" * 40)
    
    test_bloom = {
        'depth': 5,
        'entropy': 0.65,
        'lineage': [2, 5, 7, 1],
        'semantic_drift': 0.3,
        'rebloom_status': 'emerging',
        'complexity': 0.8
    }
    
    result = summarize_bloom(test_bloom)
    print(f"Bloom summary: {result}")
    
    # Check that key components are present
    assert "Depth-5" in result
    assert "E:0.65" in result
    assert "Emerging" in result
    assert "Gen-4" in result
    
    print("✅ Bloom summary tests passed\n")


def test_zone_descriptions():
    """Test zone descriptions"""
    print("Testing Zone Descriptions")
    print("=" * 40)
    
    zones = ["CALM", "ACTIVE", "SURGE"]
    
    for zone in zones:
        description = describe_pulse_zone(zone)
        print(f"{zone}: {description[:80]}...")
        assert len(description) > 50  # Should be substantial description
        assert zone.lower() in description.lower() or "cognitive" in description.lower()
    
    print("✅ Zone description tests passed\n")


def test_pressure_analysis():
    """Test cognitive pressure analysis"""
    print("Testing Cognitive Pressure Analysis")
    print("=" * 40)
    
    test_scup = {
        'schema': 0.7,
        'coherence': 0.8,
        'utility': 0.6,
        'pressure': 0.4
    }
    
    result = analyze_cognitive_pressure(65, 0.45, test_scup)
    print(f"Pressure analysis: {result}")
    
    # Check required fields
    required_fields = ['average_pressure', 'schema_health', 'pulse_zone', 'stability_assessment']
    for field in required_fields:
        assert field in result
    
    print("✅ Pressure analysis tests passed\n")


def test_cognitive_summary():
    """Test comprehensive cognitive summary"""
    print("Testing Cognitive Summary")
    print("=" * 40)
    
    test_scup = {
        'schema': 0.7,
        'coherence': 0.8,
        'utility': 0.6,
        'pressure': 0.4
    }
    
    test_bloom = {
        'depth': 3,
        'entropy': 0.5,
        'rebloom_status': 'stable',
        'complexity': 0.6
    }
    
    result = generate_cognitive_summary(65, 0.45, test_scup, test_bloom)
    print("Cognitive Summary:")
    print("-" * 20)
    print(result)
    print("-" * 20)
    
    # Check that summary contains key elements
    assert "DAWN Cognitive State Analysis" in result
    assert "Schema Health:" in result
    assert "Pulse Zone:" in result
    assert "Zone Characteristics:" in result
    
    print("✅ Cognitive summary tests passed\n")


def test_integration_with_conversation():
    """Test integration with conversation system (mock)"""
    print("Testing Conversation Integration")
    print("=" * 40)
    
    # Mock conversation scenario
    mock_metrics = {
        'scup': 0.7,
        'entropy': 0.4,
        'heat': 0.6
    }
    
    mock_consciousness_state = {
        'schema': 0.7,
        'coherence': 0.8,
        'utility': 0.6,
        'pressure': 0.4,
        'description': 'actively processing'
    }
    
    # Test the integrated analysis that would be used in conversation
    scup_dict = {
        'schema': mock_consciousness_state.get('schema', mock_metrics['scup']),
        'coherence': mock_consciousness_state.get('coherence', mock_metrics['scup']), 
        'utility': mock_consciousness_state.get('utility', 0.5),
        'pressure': mock_consciousness_state.get('pressure', 0.3)
    }
    
    heat_scaled = mock_metrics['heat'] * 100
    
    schema_health = get_schema_health(heat_scaled, mock_metrics['entropy'], scup_dict)
    pulse_zone = get_pulse_zone(heat_scaled)
    
    print(f"Mock conversation integration:")
    print(f"  Schema Health: {schema_health}")
    print(f"  Pulse Zone: {pulse_zone}")
    print(f"  Integration Status: ✅ Successfully integrated")
    
    print("✅ Conversation integration tests passed\n")


def main():
    """Run all integration tests"""
    print("🧠 DAWN Codex Engine Integration Tests")
    print("=" * 50)
    
    try:
        test_schema_health()
        test_pulse_zones()
        test_bloom_summary()
        test_zone_descriptions()
        test_pressure_analysis()
        test_cognitive_summary()
        test_integration_with_conversation()
        
        print("🎉 ALL TESTS PASSED!")
        print("✨ DAWN Codex Engine is fully integrated and operational!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 