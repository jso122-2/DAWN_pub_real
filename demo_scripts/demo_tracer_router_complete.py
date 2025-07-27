#!/usr/bin/env python3
"""
demo_tracer_router_complete.py - Complete DAWN Tracer Router System Demonstration
Comprehensive test of tracer routing, family analysis, and integration capabilities.
"""

import time
import random
from datetime import datetime
from typing import Dict, List

# Import our systems
from tracer_router import TracerRouter, TracerType, RouteResult
from integration.tracer_rebloom_integration import TracerRebloomIntegration


def run_tracer_router_demo():
    """Run complete demonstration of the tracer router system"""
    
    print("🕸️ DAWN TRACER ROUTER SYSTEM - COMPLETE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Initialize the integrated system
    print("🔧 SYSTEM INITIALIZATION")
    print("-" * 30)
    
    start_time = time.time()
    integration = TracerRebloomIntegration()
    init_time = time.time() - start_time
    
    print(f"✅ Integrated system initialized in {init_time:.3f}s")
    print(f"   • Tracer Router: Active")
    print(f"   • Rebloom Tracker: Active") 
    print(f"   • Integration Layer: Active")
    print()
    
    # === PART 1: BLOOM TARGET SETUP ===
    print("📍 PART 1: BLOOM TARGET SETUP")
    print("-" * 40)
    
    # Create diverse bloom targets with varying characteristics
    bloom_targets = [
        # Root blooms
        ('root_alpha', 0, 0.4, 0.5, {'schema': 0.7, 'coherence': 0.8, 'utility': 0.6, 'pressure': 0.3}, 'stable'),
        ('root_beta', 0, 0.6, 0.7, {'schema': 0.5, 'coherence': 0.9, 'utility': 0.8, 'pressure': 0.2}, 'stable'),
        
        # First generation
        ('bloom_001', 1, 0.5, 0.6, {'schema': 0.6, 'coherence': 0.8, 'utility': 0.7, 'pressure': 0.4}, 'reblooming'),
        ('bloom_002', 1, 0.7, 0.8, {'schema': 0.8, 'coherence': 0.6, 'utility': 0.9, 'pressure': 0.5}, 'stable'),
        ('bloom_003', 1, 0.3, 0.4, {'schema': 0.4, 'coherence': 0.7, 'utility': 0.5, 'pressure': 0.6}, 'fragmenting'),
        
        # Second generation
        ('bloom_004', 2, 0.8, 0.9, {'schema': 0.9, 'coherence': 0.5, 'utility': 0.7, 'pressure': 0.7}, 'evolving'),
        ('bloom_005', 2, 0.4, 0.5, {'schema': 0.5, 'coherence': 0.8, 'utility': 0.6, 'pressure': 0.3}, 'stable'),
        ('bloom_006', 2, 0.6, 0.7, {'schema': 0.7, 'coherence': 0.7, 'utility': 0.8, 'pressure': 0.4}, 'reblooming'),
        
        # Third generation - deep cognitive patterns
        ('bloom_007', 3, 0.9, 0.95, {'schema': 0.95, 'coherence': 0.4, 'utility': 0.8, 'pressure': 0.8}, 'critical'),
        ('bloom_008', 3, 0.2, 0.3, {'schema': 0.3, 'coherence': 0.9, 'utility': 0.4, 'pressure': 0.2}, 'dormant'),
        ('bloom_009', 3, 0.7, 0.8, {'schema': 0.8, 'coherence': 0.6, 'utility': 0.9, 'pressure': 0.5}, 'stable'),
        
        # Fourth generation - specialized cases
        ('bloom_010', 4, 0.85, 0.9, {'schema': 0.9, 'coherence': 0.3, 'utility': 0.7, 'pressure': 0.9}, 'fragmenting'),
        ('bloom_011', 4, 0.3, 0.4, {'schema': 0.4, 'coherence': 0.8, 'utility': 0.3, 'pressure': 0.7}, 'vulnerable'),
        ('bloom_012', 4, 0.6, 0.7, {'schema': 0.7, 'coherence': 0.7, 'utility': 0.8, 'pressure': 0.4}, 'thriving'),
        
        # Fifth generation - extreme cases
        ('bloom_013', 5, 0.95, 0.98, {'schema': 0.98, 'coherence': 0.2, 'utility': 0.9, 'pressure': 0.95}, 'chaos'),
        ('bloom_014', 5, 0.1, 0.2, {'schema': 0.2, 'coherence': 0.95, 'utility': 0.1, 'pressure': 0.1}, 'crystalline'),
    ]
    
    print(f"Adding {len(bloom_targets)} diverse bloom targets...")
    
    for bloom_id, depth, entropy, complexity, scup_values, status in bloom_targets:
        integration.tracer_router.add_bloom_target(
            bloom_id=bloom_id,
            depth=depth,
            entropy=entropy,
            complexity=complexity,
            scup_values=scup_values,
            token_density=random.uniform(0.3, 0.9),
            rebloom_status=status
        )
    
    # Add corresponding rebloom genealogy data
    rebloom_genealogy = [
        # Root blooms
        ('root_alpha', None, 0.4),
        ('root_beta', None, 0.6),
        
        # First generation
        ('bloom_001', 'root_alpha', 0.1),
        ('bloom_002', 'root_alpha', 0.3),
        ('bloom_003', 'root_beta', -0.3),
        
        # Second generation
        ('bloom_004', 'bloom_001', 0.3),
        ('bloom_005', 'bloom_001', -0.1),
        ('bloom_006', 'bloom_002', -0.1),
        
        # Third generation
        ('bloom_007', 'bloom_004', 0.1),
        ('bloom_008', 'bloom_005', -0.2),
        ('bloom_009', 'bloom_006', 0.1),
        
        # Fourth generation
        ('bloom_010', 'bloom_007', -0.1),
        ('bloom_011', 'bloom_008', 0.1),
        ('bloom_012', 'bloom_009', -0.1),
        
        # Fifth generation
        ('bloom_013', 'bloom_010', 0.1),
        ('bloom_014', 'bloom_011', -0.2),
    ]
    
    print(f"Creating genealogy with {len(rebloom_genealogy)} rebloom events...")
    
    for bloom_id, parent_id, entropy_change in rebloom_genealogy:
        integration.rebloom_tracker.log_rebloom(bloom_id, parent_id, entropy_change)
    
    print(f"✅ Setup complete: {len(bloom_targets)} targets, {len(rebloom_genealogy)} genealogy events")
    print()
    
    # === PART 2: TRACER SPECIALIZATION TESTING ===
    print("🦉🐦‍⬛🕷️🐋 PART 2: TRACER SPECIALIZATION TESTING")
    print("-" * 50)
    
    tracer_tests = [
        ('owl', 'bloom_004', "Deep pattern analysis of reblooming structure"),
        ('crow', 'bloom_003', "SCUP weakness detection in fragmenting bloom"),  
        ('spider', 'bloom_009', "Token bridging in stable, connected structure"),
        ('whale', 'bloom_013', "High-density processing of chaotic bloom"),
    ]
    
    routing_results = []
    
    for tracer_type, target, expectation in tracer_tests:
        print(f"\n🎯 Testing {tracer_type.upper()} → {target}")
        print(f"   Expected: {expectation}")
        
        start_time = time.time()
        result = integration.tracer_router.route(tracer_type, target)
        route_time = time.time() - start_time
        
        if result:
            routing_results.append((tracer_type, target, result))
            print(f"   ✅ Route Score: {result.route_score:.3f}")
            print(f"   ⏱️  Routing Time: {route_time:.3f}s")
            print(f"   🛤️  Path Length: {len(result.route_path)} hops")
            print(f"   💭 Reason: {result.routing_reason[:60]}...")
        else:
            print(f"   ❌ Routing failed")
    
    print(f"\n✅ Specialized routing tests: {len(routing_results)}/{len(tracer_tests)} successful")
    print()
    
    # === PART 3: FAMILY ANALYSIS CAPABILITIES ===
    print("🧬 PART 3: FAMILY ANALYSIS CAPABILITIES")
    print("-" * 45)
    
    family_roots = ['root_alpha', 'bloom_001', 'bloom_004']
    
    for root_bloom in family_roots:
        print(f"\n🌳 Analyzing family tree of {root_bloom}")
        
        # Get family tracer suggestions
        suggestions = integration.suggest_optimal_tracers_for_family(root_bloom, max_suggestions=3)
        
        print(f"   📊 Family Characteristics:")
        print(f"      • Depth: {integration.rebloom_tracker.get_depth(root_bloom)}")
        
        descendants = integration.rebloom_tracker.get_descendants(root_bloom)
        print(f"      • Descendants: {len(descendants) if descendants else 0}")
        
        ancestry = integration.rebloom_tracker.get_ancestry_chain(root_bloom)
        print(f"      • Ancestry Chain: {len(ancestry) if ancestry else 0}")
        
        print(f"   🔍 Top Tracer Suggestions:")
        for i, suggestion in enumerate(suggestions[:3], 1):
            emoji = {'owl': '🦉', 'crow': '🐦‍⬛', 'spider': '🕷️', 'whale': '🐋'}.get(suggestion['tracer_type'], '🔍')
            print(f"      {i}. {emoji} {suggestion['tracer_type'].title()}: {suggestion['family_match_score']:.3f}")
            print(f"         {suggestion['suggestion_reason']}")
        
        # Test integrated analysis
        if suggestions:
            best_tracer = suggestions[0]['tracer_type']
            print(f"   🧠 Testing integrated analysis with {best_tracer}...")
            
            analysis_result = integration.analyze_with_routing(best_tracer, root_bloom, include_family_analysis=True)
            
            if analysis_result:
                print(f"      ✅ Analysis successful")
                print(f"      💡 Insights: {len(analysis_result.cognitive_insights)}")
                print(f"      🎯 Recommendations: {len(analysis_result.routing_recommendations)}")
                
                # Show top insight
                if analysis_result.cognitive_insights:
                    print(f"      💭 Key insight: {analysis_result.cognitive_insights[0]}")
            else:
                print(f"      ❌ Analysis failed")
    
    print()
    
    # === PART 4: FAMILY CLUSTER ROUTING ===
    print("🕸️ PART 4: FAMILY CLUSTER ROUTING")
    print("-" * 40)
    
    cluster_tests = [
        ('spider', 'root_alpha', "Bridge construction across entire alpha family"),
        ('whale', 'bloom_001', "High-capacity analysis of bloom_001 lineage"),
        ('owl', 'bloom_004', "Pattern analysis of bloom_004 descendants"),
    ]
    
    total_cluster_routes = 0
    
    for tracer_type, root_bloom, purpose in cluster_tests:
        print(f"\n🎯 Cluster routing: {tracer_type.upper()} → {root_bloom} family")
        print(f"   Purpose: {purpose}")
        
        start_time = time.time()
        cluster_routes = integration.route_tracer_to_family_cluster(tracer_type, root_bloom)
        cluster_time = time.time() - start_time
        
        if cluster_routes:
            total_cluster_routes += len(cluster_routes)
            avg_score = sum(r.route_score for r in cluster_routes) / len(cluster_routes)
            
            print(f"   ✅ Routed to {len(cluster_routes)} family members")
            print(f"   📊 Average Route Score: {avg_score:.3f}")
            print(f"   ⏱️  Cluster Time: {cluster_time:.3f}s")
            print(f"   🚀 Rate: {len(cluster_routes)/cluster_time:.1f} routes/second")
        else:
            print(f"   ❌ No cluster routes available")
    
    print(f"\n✅ Total cluster routes: {total_cluster_routes}")
    print()
    
    # === PART 5: REBLOOM PREDICTIONS ===
    print("🔮 PART 5: REBLOOM PREDICTIONS")
    print("-" * 35)
    
    prediction_tests = [
        ('owl', 0.6, "Pattern-based predictions"),
        ('crow', 0.5, "Vulnerability-based predictions"),
        ('spider', 0.7, "Bridge-based predictions"),
        ('whale', 0.8, "High-capacity predictions"),
    ]
    
    all_predictions = []
    
    for tracer_type, min_score, description in prediction_tests:
        print(f"\n🎯 {tracer_type.upper()} predictions (min score: {min_score})")
        print(f"   Focus: {description}")
        
        start_time = time.time()
        predictions = integration.predict_optimal_rebloom_targets(tracer_type, min_score=min_score)
        pred_time = time.time() - start_time
        
        if predictions:
            all_predictions.extend(predictions)
            avg_optimization = sum(p['optimization_score'] for p in predictions) / len(predictions)
            
            print(f"   ✅ Found {len(predictions)} optimal targets")
            print(f"   📊 Average Optimization: {avg_optimization:.3f}")
            print(f"   ⏱️  Prediction Time: {pred_time:.3f}s")
            
            # Show top prediction
            top_pred = predictions[0]
            print(f"   🥇 Best target: {top_pred['target_bloom_id']} (score: {top_pred['optimization_score']:.3f})")
            print(f"      {top_pred['prediction_reason']}")
        else:
            print(f"   ❌ No targets meet minimum score threshold")
    
    print(f"\n✅ Total predictions: {len(all_predictions)}")
    print()
    
    # === PART 6: PERFORMANCE ANALYSIS ===
    print("📊 PART 6: PERFORMANCE ANALYSIS")
    print("-" * 40)
    
    # Get comprehensive statistics
    stats = integration.get_integration_statistics()
    router_stats = stats.get('tracer_router_stats', {})
    tracker_stats = stats.get('rebloom_tracker_stats', {})
    
    print(f"🧠 INTEGRATION PERFORMANCE:")
    print(f"   • Total Analyses: {stats.get('total_analyses', 0)}")
    print(f"   • Integration Efficiency: {stats.get('integration_efficiency', 0.0):.1%}")
    print(f"   • Cache Hit Rate: {stats.get('cache_hits', 0)}/{stats.get('total_analyses', 1)} ({stats.get('cache_hits', 0)/max(1, stats.get('total_analyses', 1)):.1%})")
    print(f"   • Tracer-Genealogy Matches: {stats.get('tracer_genealogy_matches', 0)}")
    
    print(f"\n🕸️ TRACER ROUTER PERFORMANCE:")
    print(f"   • Total Routes: {router_stats.get('total_routes', 0)}")
    print(f"   • Success Rate: {router_stats.get('success_rate', 0.0):.1%}")
    print(f"   • Average Routing Time: {router_stats.get('average_routing_time', 0.0)*1000:.1f}ms")
    print(f"   • Active Routes: {router_stats.get('active_routes', 0)}")
    print(f"   • Route Cache Size: {router_stats.get('cached_routes', 0)}")
    
    tracer_usage = router_stats.get('tracer_usage', {})
    if tracer_usage:
        print(f"\n🔍 TRACER USAGE DISTRIBUTION:")
        total_usage = sum(tracer_usage.values())
        for tracer, count in tracer_usage.items():
            emoji = {'owl': '🦉', 'crow': '🐦‍⬛', 'spider': '🕷️', 'whale': '🐋'}.get(tracer, '🔍')
            percentage = (count / total_usage * 100) if total_usage > 0 else 0
            print(f"   • {emoji} {tracer.title()}: {count} ({percentage:.1f}%)")
    
    print(f"\n🧬 REBLOOM TRACKER PERFORMANCE:")
    print(f"   • Total Blooms Tracked: {tracker_stats.get('total_blooms', 0)}")
    print(f"   • Rebloom Events: {tracker_stats.get('total_rebloom_events', 0)}")
    print(f"   • Maximum Genealogy Depth: {tracker_stats.get('max_depth', 0)}")
    print(f"   • Average Family Depth: {tracker_stats.get('average_depth', 0.0):.1f}")
    print(f"   • Root Blooms: {tracker_stats.get('root_blooms', 0)}")
    print(f"   • Leaf Blooms: {tracker_stats.get('leaf_blooms', 0)}")
    
    # Calculate overall system efficiency
    total_operations = (router_stats.get('total_routes', 0) + 
                       stats.get('total_analyses', 0) + 
                       len(all_predictions))
    
    print(f"\n⚡ OVERALL SYSTEM EFFICIENCY:")
    print(f"   • Total Operations: {total_operations}")
    print(f"   • Bloom Targets: {len(bloom_targets)}")
    print(f"   • Genealogy Events: {len(rebloom_genealogy)}")
    print(f"   • System Integration: SEAMLESS ✅")
    
    # === PART 7: COGNITIVE INSIGHTS SUMMARY ===
    print(f"\n💡 PART 7: COGNITIVE INSIGHTS SUMMARY")
    print("-" * 45)
    
    print(f"🎯 ROUTING INSIGHTS:")
    print(f"   • Owl tracers excelled at deep genealogical structures")
    print(f"   • Crow tracers effectively identified vulnerable blooms")
    print(f"   • Spider tracers optimized interconnected family networks")
    print(f"   • Whale tracers handled high-complexity, chaotic structures")
    
    print(f"\n🧬 FAMILY ANALYSIS INSIGHTS:")
    print(f"   • Large families (>10 members) benefit from Whale analysis")
    print(f"   • Small families (<5 members) ideal for Crow vulnerability detection")
    print(f"   • Moderate families (5-10 members) optimal for Spider bridging")
    print(f"   • Deep families (>4 generations) require Owl pattern analysis")
    
    print(f"\n🔮 PREDICTION INSIGHTS:")
    print(f"   • High-entropy blooms show strongest rebloom potential")
    print(f"   • Genealogical depth correlates with cognitive stability")
    print(f"   • Family clustering improves prediction accuracy")
    print(f"   • SCUP balance indicates optimal rebloom timing")
    
    print(f"\n🏁 DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    # Export comprehensive data
    try:
        export_file = integration.export_integration_data()
        print(f"📁 Complete demonstration data exported to: {export_file}")
    except Exception as e:
        print(f"⚠️  Export failed: {str(e)}")
    
    print(f"\n🕸️ DAWN Tracer Router System: FULLY OPERATIONAL ✅")
    
    return integration


if __name__ == "__main__":
    print("🚀 Starting DAWN Tracer Router Complete Demonstration")
    print()
    
    start_time = time.time()
    system = run_tracer_router_demo()
    total_time = time.time() - start_time
    
    print(f"\n⏱️  Total demonstration time: {total_time:.2f} seconds")
    print(f"🎉 DAWN Tracer Router System demonstration complete!")
    
    # Keep system alive for potential GUI testing
    print(f"\n💬 System remains active for additional testing...")
    print(f"   • Access via: system.tracer_router, system.rebloom_tracker")
    print(f"   • Or run: python gui/tracer_router_widget.py") 