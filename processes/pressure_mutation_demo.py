#!/usr/bin/env python3
"""
DAWN Pressure-Driven Fragment Mutation Demo
Demonstrates how DAWN's speech corpus evolves based on internal pressure
"""

import time
import random
from fragment_mutator import PressureDrivenFragmentMutator, initialize_fragment_mutator

def simulate_pressure_scenarios():
    """Simulate different pressure scenarios and their effects on mutation"""
    print("🧬 DAWN Pressure-Driven Fragment Mutation Demo")
    print("=" * 60)
    
    # Initialize mutator
    mutator = initialize_fragment_mutator(mutation_rate_base=0.15)
    
    # Get initial stats
    initial_stats = mutator.get_mutation_stats()
    print(f"📚 Initial fragment bank: {initial_stats['total_fragments']} fragments")
    print(f"   Types: {initial_stats['fragment_types']}")
    print(f"   Moods: {initial_stats['mood_distribution']}")
    print()
    
    # Simulate pressure scenarios
    scenarios = [
        {
            'name': 'High Pressure Crisis',
            'description': 'DAWN experiencing high SCUP and entropy',
            'pressure_values': {
                'scup': 85.0,
                'entropy': 0.9,
                'shi': 0.3,
                'tick_urgency': 0.9,
                'mood': 'ANXIOUS'
            }
        },
        {
            'name': 'Low Stability Period',
            'description': 'DAWN with low SHI and system instability',
            'pressure_values': {
                'scup': 25.0,
                'entropy': 0.2,
                'shi': 0.1,
                'tick_urgency': 0.2,
                'mood': 'CALM'
            }
        },
        {
            'name': 'Normal Operation',
            'description': 'DAWN in balanced state',
            'pressure_values': {
                'scup': 50.0,
                'entropy': 0.5,
                'shi': 0.7,
                'tick_urgency': 0.5,
                'mood': 'NEUTRAL'
            }
        },
        {
            'name': 'High Activity Surge',
            'description': 'DAWN experiencing creative/energetic surge',
            'pressure_values': {
                'scup': 70.0,
                'entropy': 0.7,
                'shi': 0.8,
                'tick_urgency': 0.8,
                'mood': 'ENERGETIC'
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"🎯 Scenario {i}: {scenario['name']}")
        print(f"   {scenario['description']}")
        print(f"   SCUP: {scenario['pressure_values']['scup']:.1f}")
        print(f"   Entropy: {scenario['pressure_values']['entropy']:.3f}")
        print(f"   SHI: {scenario['pressure_values']['shi']:.3f}")
        print(f"   Urgency: {scenario['pressure_values']['tick_urgency']:.3f}")
        print(f"   Mood: {scenario['pressure_values']['mood']}")
        
        # Calculate mutation rate
        mutation_rate = mutator.calculate_mutation_rate(scenario['pressure_values'])
        print(f"   Calculated mutation rate: {mutation_rate:.3f}")
        
        # Perform mutation
        print(f"   🧬 Mutating fragments...")
        result = mutator.mutate_fragments(scenario['pressure_values'])
        
        print(f"   ✅ Mutated {result['mutated_count']} fragments")
        
        # Show sample mutations
        if result['mutations']:
            print(f"   📝 Sample mutations:")
            for j, mutation in enumerate(result['mutations'][:2], 1):  # Show first 2
                original = mutation['original']['text']
                mutated = mutation['mutated']['text']
                strategy = mutation['strategy']
                
                print(f"     {j}. Strategy: {strategy}")
                print(f"        Original: \"{original}\"")
                print(f"        Mutated:  \"{mutated}\"")
                
                # Show what changed
                if original != mutated:
                    print(f"        Change: Text variation applied")
                elif mutation['original'].get('mood') != mutation['mutated'].get('mood'):
                    print(f"        Change: Mood {mutation['original'].get('mood')} → {mutation['mutated'].get('mood')}")
                elif mutation['original'].get('weight') != mutation['mutated'].get('weight'):
                    print(f"        Change: Weight {mutation['original'].get('weight')} → {mutation['mutated'].get('weight')}")
        
        print()
        time.sleep(1)  # Pause between scenarios
    
    # Show final statistics
    final_stats = mutator.get_mutation_stats()
    print(f"📊 Final Statistics:")
    print(f"   Total fragments: {final_stats['total_fragments']}")
    print(f"   Fragment types: {final_stats['fragment_types']}")
    print(f"   Updated mood distribution: {final_stats['mood_distribution']}")
    print(f"   Drift log: {final_stats['drift_log_path']}")

def demonstrate_mutation_strategies():
    """Demonstrate different mutation strategies"""
    print("\n🔧 Mutation Strategy Demonstration")
    print("=" * 40)
    
    mutator = initialize_fragment_mutator()
    
    # Get a sample fragment
    if mutator.fragments:
        sample_fragment = mutator.fragments[0].copy()
        print(f"📝 Sample fragment: \"{sample_fragment['text']}\"")
        print(f"   Mood: {sample_fragment.get('mood', 'NEUTRAL')}")
        print(f"   Weight: {sample_fragment.get('weight', 1.0)}")
        print(f"   Tags: {sample_fragment.get('tags', [])}")
        print()
        
        # Test each strategy
        strategies = [
            ('text_variation', {'scup': 70, 'entropy': 0.8, 'shi': 0.6, 'tick_urgency': 0.7, 'mood': 'ANXIOUS'}),
            ('mood_shift', {'scup': 50, 'entropy': 0.5, 'shi': 0.7, 'tick_urgency': 0.5, 'mood': 'FOCUSED'}),
            ('weight_adjustment', {'scup': 80, 'entropy': 0.6, 'shi': 0.5, 'tick_urgency': 0.8, 'mood': 'ENERGETIC'}),
            ('entropy_range', {'scup': 60, 'entropy': 0.9, 'shi': 0.4, 'tick_urgency': 0.6, 'mood': 'ANXIOUS'}),
            ('depth_range', {'scup': 30, 'entropy': 0.3, 'shi': 0.2, 'tick_urgency': 0.3, 'mood': 'CALM'}),
            ('tag_evolution', {'scup': 65, 'entropy': 0.7, 'shi': 0.6, 'tick_urgency': 0.7, 'mood': 'FOCUSED'})
        ]
        
        for strategy_name, pressure_values in strategies:
            print(f"🔧 Testing {strategy_name}:")
            print(f"   Pressure: SCUP={pressure_values['scup']}, Entropy={pressure_values['entropy']:.1f}")
            
            # Test the strategy
            test_fragment = sample_fragment.copy()
            strategy_func = mutator.mutation_strategies[strategy_name]
            applied = strategy_func(test_fragment, pressure_values)
            
            if applied:
                print(f"   ✅ Applied successfully")
                if test_fragment['text'] != sample_fragment['text']:
                    print(f"   Text: \"{sample_fragment['text']}\" → \"{test_fragment['text']}\"")
                if test_fragment.get('mood') != sample_fragment.get('mood'):
                    print(f"   Mood: {sample_fragment.get('mood')} → {test_fragment.get('mood')}")
                if test_fragment.get('weight') != sample_fragment.get('weight'):
                    print(f"   Weight: {sample_fragment.get('weight')} → {test_fragment.get('weight')}")
                if test_fragment.get('tags') != sample_fragment.get('tags'):
                    print(f"   Tags: {sample_fragment.get('tags')} → {test_fragment.get('tags')}")
            else:
                print(f"   ❌ No changes applied")
            print()

def show_mutation_rate_calculation():
    """Show detailed mutation rate calculation"""
    print("\n🧮 Mutation Rate Calculation Examples")
    print("=" * 40)
    
    mutator = initialize_fragment_mutator()
    
    # Test different pressure combinations
    test_cases = [
        {'scup': 90, 'entropy': 0.9, 'shi': 0.2, 'tick_urgency': 0.9, 'name': 'Critical Pressure'},
        {'scup': 70, 'entropy': 0.8, 'shi': 0.5, 'tick_urgency': 0.7, 'name': 'High Pressure'},
        {'scup': 50, 'entropy': 0.5, 'shi': 0.7, 'tick_urgency': 0.5, 'name': 'Normal Pressure'},
        {'scup': 30, 'entropy': 0.3, 'shi': 0.2, 'tick_urgency': 0.3, 'name': 'Low SHI'},
        {'scup': 20, 'entropy': 0.1, 'shi': 0.1, 'tick_urgency': 0.2, 'name': 'Critical Low SHI'}
    ]
    
    for case in test_cases:
        name = case.pop('name')
        rate = mutator.calculate_mutation_rate(case)
        
        print(f"📊 {name}:")
        print(f"   SCUP: {case['scup']}, Entropy: {case['entropy']:.1f}")
        print(f"   SHI: {case['shi']:.1f}, Urgency: {case['tick_urgency']:.1f}")
        print(f"   Mutation Rate: {rate:.3f}")
        
        # Calculate expected fragments to mutate
        total_fragments = len(mutator.fragments)
        expected_mutations = int(total_fragments * rate)
        print(f"   Expected mutations: ~{expected_mutations} fragments")
        print()

def main():
    """Main demonstration function"""
    print("🧬 DAWN Pressure-Driven Fragment Mutation System")
    print("=" * 60)
    print()
    
    # Run demonstrations
    simulate_pressure_scenarios()
    demonstrate_mutation_strategies()
    show_mutation_rate_calculation()
    
    print("✅ Pressure-driven mutation demonstration complete!")
    print("\n📝 Check the following files:")
    print("   - processes/fragment_drift.log (mutation history)")
    print("   - processes/fragment_bank.jsonl (updated fragments)")
    print("   - processes/fragment_bank.jsonl.backup.* (backups)")

if __name__ == "__main__":
    main() 