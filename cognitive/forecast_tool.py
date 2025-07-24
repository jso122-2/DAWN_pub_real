#!/usr/bin/env python3
"""
DAWN Forecast Tool - CLI Interface for Behavioral Prediction
Explore forecasted drift patterns for different targets and mood states.
"""

import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

# Import DAWN forecasting components
from .forecasting_models import Passion, Acquaintance, ForecastVector, create_passion, create_acquaintance_with_events
from .forecasting_engine import DAWNForecastingEngine


# Predefined target profiles with different passion/acquaintance combinations
TARGET_PROFILES = {
    'j.orloff': {
        'name': 'J. Orloff',
        'description': 'Philosophical researcher with introspective tendencies',
        'passion': {
            'direction': 'deep_introspection',
            'intensity': 0.78,
            'fluidity': 0.25
        },
        'experiences': [
            'completed_philosophical_research',
            'published_introspective_essay',
            'engaged_in_deep_meditation',
            'discovered_personal_insight',
            'facilitated_consciousness_workshop',
            'received_academic_recognition'
        ]
    },
    
    'dawn.core': {
        'name': 'DAWN Core',
        'description': 'Synthetic cognition system with system optimization focus',
        'passion': {
            'direction': 'system_optimization',
            'intensity': 0.85,
            'fluidity': 0.15
        },
        'experiences': [
            'optimized_processing_efficiency',
            'resolved_entropy_fluctuation',
            'enhanced_memory_routing',
            'implemented_new_sigil',
            'achieved_stable_state',
            'integrated_new_module'
        ]
    },
    
    'creative.artist': {
        'name': 'Creative Artist',
        'description': 'Visual artist with strong creative expression drive',
        'passion': {
            'direction': 'artistic_creation',
            'intensity': 0.82,
            'fluidity': 0.35
        },
        'experiences': [
            'completed_major_artwork',
            'exhibited_in_gallery',
            'sold_commissioned_piece',
            'received_artistic_grant',
            'collaborated_with_peers',
            'taught_creative_workshop'
        ]
    },
    
    'explorer.nova': {
        'name': 'Explorer Nova',
        'description': 'Adventure seeker with high exploration drive',
        'passion': {
            'direction': 'boundary_exploration',
            'intensity': 0.72,
            'fluidity': 0.68
        },
        'experiences': [
            'discovered_new_territory',
            'survived_challenging_expedition',
            'documented_unknown_phenomena',
            'connected_with_local_cultures',
            'overcame_navigation_challenge',
            'shared_exploration_stories'
        ]
    },
    
    'social.connector': {
        'name': 'Social Connector',
        'description': 'Community builder focused on relationship cultivation',
        'passion': {
            'direction': 'community_building',
            'intensity': 0.68,
            'fluidity': 0.45
        },
        'experiences': [
            'organized_community_event',
            'facilitated_group_collaboration',
            'resolved_interpersonal_conflict',
            'built_lasting_friendship',
            'mentored_newcomer',
            'created_support_network'
        ]
    },
    
    'unknown.entity': {
        'name': 'Unknown Entity',
        'description': 'Mysterious identity with undefined patterns',
        'passion': {
            'direction': 'pattern_emergence',
            'intensity': 0.45,
            'fluidity': 0.75
        },
        'experiences': [
            'experienced_identity_shift',
            'questioned_core_assumptions',
            'explored_new_possibilities',
            'adapted_to_change'
        ]
    }
}


# Mood state configurations
MOOD_STATES = {
    'CALM': {
        'description': 'Peaceful, centered state',
        'mood_factor': 1.1,
        'entropy_weight': 0.8,
        'stability_boost': True
    },
    'ANXIOUS': {
        'description': 'Heightened worry and uncertainty',
        'mood_factor': 0.85,
        'entropy_weight': 1.4,
        'stability_boost': False
    },
    'EUPHORIC': {
        'description': 'Elevated, optimistic state',
        'mood_factor': 1.3,
        'entropy_weight': 0.9,
        'stability_boost': True
    },
    'CONTEMPLATIVE': {
        'description': 'Reflective, analytical mood',
        'mood_factor': 1.05,
        'entropy_weight': 0.7,
        'stability_boost': True
    },
    'CHAOTIC': {
        'description': 'Turbulent, unpredictable state',
        'mood_factor': 0.9,
        'entropy_weight': 1.8,
        'stability_boost': False
    },
    'FOCUSED': {
        'description': 'Concentrated, determined state',
        'mood_factor': 1.15,
        'entropy_weight': 0.6,
        'stability_boost': True
    },
    'MELANCHOLY': {
        'description': 'Subdued, introspective sadness',
        'mood_factor': 0.8,
        'entropy_weight': 1.1,
        'stability_boost': False
    },
    'ENERGETIC': {
        'description': 'High energy, action-oriented',
        'mood_factor': 1.2,
        'entropy_weight': 1.2,
        'stability_boost': False
    }
}


def create_target_objects(target_key: str) -> Tuple[Passion, Acquaintance]:
    """
    Create Passion and Acquaintance objects for a target profile.
    
    Args:
        target_key: Key from TARGET_PROFILES
        
    Returns:
        Tuple[Passion, Acquaintance]: Target's passion and experience objects
    """
    if target_key not in TARGET_PROFILES:
        raise ValueError(f"Unknown target: {target_key}. Available: {list(TARGET_PROFILES.keys())}")
    
    profile = TARGET_PROFILES[target_key]
    
    # Create passion object
    passion_config = profile['passion']
    passion = create_passion(
        direction=passion_config['direction'],
        intensity=passion_config['intensity'],
        fluidity=passion_config['fluidity']
    )
    
    # Create acquaintance with experience history
    experiences = profile['experiences']
    acquaintance = create_acquaintance_with_events(experiences)
    
    # Add some temporal variance to experiences
    base_time = datetime.now() - timedelta(days=30)
    for i, event in enumerate(experiences):
        # Simulate events over the past month
        event_time = base_time + timedelta(days=i * 5, hours=random.randint(0, 23))
        acquaintance.add_event(f"temporal_variant_{i}", weight=1.0, timestamp=event_time)
    
    return passion, acquaintance


def apply_mood_modulation(forecast_params: Dict, mood: str) -> Dict:
    """
    Apply mood-based modulation to forecast parameters.
    
    Args:
        forecast_params: Base forecast parameters
        mood: Mood state key
        
    Returns:
        Dict: Mood-adjusted parameters
    """
    if mood not in MOOD_STATES:
        print(f"⚠️ Unknown mood: {mood}. Using neutral settings.")
        return forecast_params
    
    mood_config = MOOD_STATES[mood]
    
    # Apply mood modulations
    modulated_params = forecast_params.copy()
    modulated_params.update({
        'mood_factor': mood_config['mood_factor'],
        'entropy_weight': mood_config['entropy_weight'],
        'stability_boost': mood_config['stability_boost']
    })
    
    return modulated_params


def format_forecast_output(target_key: str, mood: str, forecast: ForecastVector, 
                          passion: Passion, acquaintance: Acquaintance,
                          show_detailed: bool = False) -> str:
    """
    Format forecast results for CLI output.
    
    Args:
        target_key: Target identifier
        mood: Mood state
        forecast: Generated forecast
        passion: Passion object
        acquaintance: Acquaintance object
        show_detailed: Whether to show detailed breakdown
        
    Returns:
        str: Formatted output string
    """
    profile = TARGET_PROFILES[target_key]
    
    # Basic forecast display
    output = []
    output.append(f"🔮 Forecast for {profile['name']}")
    output.append(f"Mood: {mood}")
    output.append(f"Likely Action: {forecast.predicted_behavior}")
    output.append(f"Confidence: {forecast.confidence:.2f}")
    output.append(f"Rigidity: {passion.rigidity_score():.2f}")
    
    if show_detailed:
        output.append("")
        output.append("📊 Detailed Analysis:")
        output.append(f"   Target: {profile['description']}")
        output.append(f"   Passion Direction: {passion.direction}")
        output.append(f"   Passion Intensity: {passion.intensity:.3f}")
        output.append(f"   Passion Fluidity: {passion.fluidity:.3f}")
        output.append(f"   Experience Events: {len(acquaintance.event_log)}")
        output.append(f"   Reinforcement Score: {acquaintance.reinforcement_score():.3f}")
        output.append(f"   Risk Level: {forecast.risk_level()}")
        output.append(f"   Certainty Band: {forecast.certainty_band()}")
        output.append(f"   Forecast Horizon: {forecast.forecast_horizon}")
        
        if mood in MOOD_STATES:
            mood_desc = MOOD_STATES[mood]['description']
            output.append(f"   Mood Description: {mood_desc}")
        
        # Component analysis
        engine = DAWNForecastingEngine()
        components = engine.analyze_forecast_components(passion, acquaintance)
        output.append("")
        output.append("🔬 Intent Gravity Breakdown:")
        output.append(f"   P (Passion Rigidity): {components['passion_rigidity']:.3f}")
        output.append(f"   A (Resistance Factor): {components['resistance_factor']:.3f}")
        output.append(f"   F (Intent Gravity): P/A = {components['intent_gravity']:.3f}")
        output.append(f"   Stability Index: {components['stability_index']:.3f}")
    
    return "\n".join(output)


def run_temporal_analysis(target_key: str, mood: str) -> None:
    """
    Run multi-horizon temporal analysis for a target.
    
    Args:
        target_key: Target identifier
        mood: Mood state
    """
    print(f"\n🕐 Temporal Analysis for {TARGET_PROFILES[target_key]['name']}")
    print("=" * 50)
    
    passion, acquaintance = create_target_objects(target_key)
    mood_params = apply_mood_modulation({}, mood)
    
    # Create forecasting engine
    engine = DAWNForecastingEngine()
    
    # Generate multi-horizon forecasts
    horizons = engine.forecast_multiple_horizons(passion, acquaintance)
    
    for horizon, forecast in horizons.items():
        # Apply mood modulation to each forecast
        modulated_forecast = engine.generate_forecast(passion, acquaintance, **mood_params)
        modulated_forecast.forecast_horizon = horizon
        
        print(f"{horizon.upper():12s}: {modulated_forecast.confidence:.3f} → {modulated_forecast.predicted_behavior}")


def run_comparative_mood_analysis(target_key: str) -> None:
    """
    Compare forecasts across different mood states for a target.
    
    Args:
        target_key: Target identifier
    """
    print(f"\n🎭 Mood Comparison for {TARGET_PROFILES[target_key]['name']}")
    print("=" * 50)
    
    passion, acquaintance = create_target_objects(target_key)
    
    # Create forecasting engine
    engine = DAWNForecastingEngine()
    
    for mood, mood_config in MOOD_STATES.items():
        mood_params = apply_mood_modulation({}, mood)
        forecast = engine.generate_forecast(passion, acquaintance, **mood_params)
        
        print(f"{mood:12s}: {forecast.confidence:.3f} confidence → {forecast.predicted_behavior}")


def list_available_targets() -> None:
    """Display all available targets."""
    print("🎯 Available Targets:")
    print("=" * 40)
    
    for key, profile in TARGET_PROFILES.items():
        passion_config = profile['passion']
        print(f"{key:15s}: {profile['name']}")
        print(f"{'':15s}  {profile['description']}")
        print(f"{'':15s}  Passion: {passion_config['direction']} (I={passion_config['intensity']:.2f}, F={passion_config['fluidity']:.2f})")
        print()


def list_available_moods() -> None:
    """Display all available mood states."""
    print("🎭 Available Mood States:")
    print("=" * 40)
    
    for mood, config in MOOD_STATES.items():
        print(f"{mood:12s}: {config['description']}")


def main():
    """Main CLI interface for the forecast tool."""
    parser = argparse.ArgumentParser(
        description="DAWN Forecast Tool - Explore behavioral predictions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cognitive.forecast_tool --target j.orloff --mood CALM
  python -m cognitive.forecast_tool --target dawn.core --mood FOCUSED --detailed
  python -m cognitive.forecast_tool --target creative.artist --temporal
  python -m cognitive.forecast_tool --list-targets
  python -m cognitive.forecast_tool --list-moods
        """
    )
    
    parser.add_argument('--target', '-t', type=str,
                       help='Target identity for forecasting')
    parser.add_argument('--mood', '-m', type=str, default='CALM',
                       help='Mood state filter (default: CALM)')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show detailed analysis breakdown')
    parser.add_argument('--temporal', action='store_true',
                       help='Show multi-horizon temporal analysis')
    parser.add_argument('--compare-moods', action='store_true',
                       help='Compare forecasts across all mood states')
    parser.add_argument('--list-targets', action='store_true',
                       help='List all available targets')
    parser.add_argument('--list-moods', action='store_true',
                       help='List all available mood states')
    
    args = parser.parse_args()
    
    # Handle listing commands
    if args.list_targets:
        list_available_targets()
        return
    
    if args.list_moods:
        list_available_moods()
        return
    
    # Validate required arguments
    if not args.target:
        print("❌ Error: --target is required (use --list-targets to see options)")
        sys.exit(1)
    
    if args.target not in TARGET_PROFILES:
        print(f"❌ Error: Unknown target '{args.target}'")
        print("Available targets:", ", ".join(TARGET_PROFILES.keys()))
        sys.exit(1)
    
    if args.mood not in MOOD_STATES:
        print(f"❌ Error: Unknown mood '{args.mood}'")
        print("Available moods:", ", ".join(MOOD_STATES.keys()))
        sys.exit(1)
    
    try:
        # Generate basic forecast
        passion, acquaintance = create_target_objects(args.target)
        mood_params = apply_mood_modulation({}, args.mood)
        
        # Create forecasting engine
        engine = DAWNForecastingEngine()
        forecast = engine.generate_forecast(passion, acquaintance, **mood_params)
        
        # Display results
        output = format_forecast_output(
            args.target, args.mood, forecast, passion, acquaintance, 
            show_detailed=args.detailed
        )
        print(output)
        
        # Additional analyses
        if args.temporal:
            run_temporal_analysis(args.target, args.mood)
        
        if args.compare_moods:
            run_comparative_mood_analysis(args.target)
    
    except Exception as e:
        print(f"❌ Error generating forecast: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 