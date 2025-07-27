#!/usr/bin/env python3
"""
tracer_rebloom_integration.py - Unified Tracer Router and Rebloom Tracker Integration
Combines intelligent tracer routing with genealogical rebloom tracking for
comprehensive cognitive analysis and family tree routing.
"""

import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

# Import our systems
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracer_router import TracerRouter, TracerType, RouteResult, BloomTarget
from rebloom_tracker import RebloomTracker, RebloomEvent, BloomNode


@dataclass
class IntegratedAnalysisResult:
    """Combined result from tracer routing and rebloom genealogy analysis"""
    tracer_route: RouteResult
    genealogy_analysis: Dict[str, Any]
    family_context: Dict[str, Any]
    cognitive_insights: List[str]
    routing_recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'tracer_route': {
                'tracer_type': self.tracer_route.tracer_type,
                'target_bloom_id': self.tracer_route.target_bloom_id,
                'route_path': self.tracer_route.route_path,
                'route_score': self.tracer_route.route_score,
                'estimated_time': self.tracer_route.estimated_time,
                'routing_reason': self.tracer_route.routing_reason
            },
            'genealogy_analysis': self.genealogy_analysis,
            'family_context': self.family_context,
            'cognitive_insights': self.cognitive_insights,
            'routing_recommendations': self.routing_recommendations,
            'timestamp': self.timestamp.isoformat()
        }


class TracerRebloomIntegration:
    """
    Unified system that combines tracer routing with rebloom genealogy tracking
    for comprehensive cognitive analysis and intelligent routing decisions.
    """
    
    def __init__(self):
        """Initialize the integrated system"""
        # Core systems
        self.tracer_router = TracerRouter()
        self.rebloom_tracker = RebloomTracker()
        
        # Integration cache and history
        self.analysis_cache: Dict[str, IntegratedAnalysisResult] = {}
        self.analysis_history: List[IntegratedAnalysisResult] = []
        
        # Performance tracking
        self.integration_stats = {
            'total_analyses': 0,
            'successful_integrations': 0,
            'cache_hits': 0,
            'tracer_genealogy_matches': 0,
            'optimal_route_suggestions': 0
        }
        
        # Cognitive insights patterns
        self.insight_patterns = {
            'family_clustering': "Tracer routing to genealogical clusters",
            'entropy_inheritance': "Entropy patterns in family lineages", 
            'specialization_matching': "Optimal tracer-genealogy pairing",
            'rebloom_prediction': "Predicting optimal rebloom targets",
            'cognitive_efficiency': "Maximizing analysis efficiency"
        }
        
        print("[TracerRebloomIntegration] 🧠🕸️ Unified cognitive routing and genealogy system initialized")
    
    def analyze_with_routing(self, tracer_type: str, target_bloom_id: str, 
                           include_family_analysis: bool = True) -> Optional[IntegratedAnalysisResult]:
        """
        Perform integrated analysis combining tracer routing with genealogy
        
        Args:
            tracer_type: Type of tracer to route
            target_bloom_id: Target bloom for analysis
            include_family_analysis: Whether to include full family tree analysis
            
        Returns:
            IntegratedAnalysisResult with combined insights
        """
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{tracer_type}:{target_bloom_id}:{include_family_analysis}"
        if cache_key in self.analysis_cache:
            self.integration_stats['cache_hits'] += 1
            return self.analysis_cache[cache_key]
        
        # Route the tracer
        tracer_route = self.tracer_router.route(tracer_type, target_bloom_id)
        if not tracer_route:
            print(f"[TracerRebloomIntegration] ❌ Failed to route {tracer_type} to {target_bloom_id}")
            return None
        
        # Get genealogy analysis
        genealogy_analysis = self._analyze_bloom_genealogy(target_bloom_id, include_family_analysis)
        
        # Analyze family context
        family_context = self._analyze_family_context(target_bloom_id, tracer_type)
        
        # Generate cognitive insights
        cognitive_insights = self._generate_cognitive_insights(tracer_route, genealogy_analysis, family_context)
        
        # Generate routing recommendations
        routing_recommendations = self._generate_routing_recommendations(
            tracer_type, target_bloom_id, genealogy_analysis, family_context
        )
        
        # Create integrated result
        result = IntegratedAnalysisResult(
            tracer_route=tracer_route,
            genealogy_analysis=genealogy_analysis,
            family_context=family_context,
            cognitive_insights=cognitive_insights,
            routing_recommendations=routing_recommendations
        )
        
        # Cache and track
        self.analysis_cache[cache_key] = result
        self.analysis_history.append(result)
        
        # Update statistics
        analysis_time = time.time() - start_time
        self._update_integration_stats(True, analysis_time)
        
        print(f"[TracerRebloomIntegration] ✅ Integrated analysis complete for {tracer_type} → {target_bloom_id}")
        print(f"  🧬 Family depth: {genealogy_analysis.get('depth', 0)}")
        print(f"  🎯 Route score: {tracer_route.route_score:.2f}")
        print(f"  💡 Insights: {len(cognitive_insights)}")
        
        return result
    
    def suggest_optimal_tracers_for_family(self, bloom_id: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
        """
        Suggest optimal tracers for analyzing a bloom's entire family tree
        
        Args:
            bloom_id: Root bloom for family analysis
            max_suggestions: Maximum number of tracer suggestions
            
        Returns:
            List of tracer suggestions with reasoning
        """
        # Get family tree information
        family_stats = self.rebloom_tracker.get_lineage_statistics()
        ancestry = self.rebloom_tracker.get_ancestry_chain(bloom_id)
        descendants = self.rebloom_tracker.get_descendants(bloom_id)
        
        suggestions = []
        
        # Analyze family characteristics
        family_depth = len(ancestry) if ancestry else 0
        family_size = len(descendants) if descendants else 0
        
        # Get entropy patterns in the family
        family_members = (ancestry or []) + (descendants or []) + [bloom_id]
        family_entropy_values = []
        
        for member_id in family_members:
            entropy_evolution = self.rebloom_tracker.get_entropy_evolution(member_id)
            if entropy_evolution:
                # entropy_evolution returns list of (bloom_id, total_entropy_drift) tuples
                family_entropy_values.extend([drift for _, drift in entropy_evolution])
        
        avg_entropy = sum(family_entropy_values) / len(family_entropy_values) if family_entropy_values else 0.5
        
        # Suggest tracers based on family characteristics
        for tracer_type in ['owl', 'crow', 'spider', 'whale']:
            try:
                tracer_enum = TracerType(tracer_type)
                capabilities = self.tracer_router.tracer_capabilities[tracer_enum]
                
                # Calculate family match score
                family_score = self._calculate_family_match_score(
                    tracer_type, family_depth, family_size, avg_entropy, capabilities
                )
                
                if family_score > 0.4:  # Only suggest viable options
                    reason = self._generate_family_suggestion_reason(
                        tracer_type, family_depth, family_size, avg_entropy
                    )
                    
                    suggestions.append({
                        'tracer_type': tracer_type,
                        'family_match_score': family_score,
                        'suggestion_reason': reason,
                        'family_depth': family_depth,
                        'family_size': family_size,
                        'estimated_coverage': min(1.0, family_score * 1.2)
                    })
                    
            except ValueError:
                continue
        
        # Sort by match score and limit results
        suggestions.sort(key=lambda x: x['family_match_score'], reverse=True)
        
        print(f"[TracerRebloomIntegration] 🔍 Generated {len(suggestions)} tracer suggestions for family of {bloom_id}")
        
        return suggestions[:max_suggestions]
    
    def route_tracer_to_family_cluster(self, tracer_type: str, root_bloom_id: str) -> List[RouteResult]:
        """
        Route a tracer to analyze an entire family cluster efficiently
        
        Args:
            tracer_type: Type of tracer to route
            root_bloom_id: Root bloom of the family cluster
            
        Returns:
            List of route results for the family cluster analysis
        """
        # Get family members
        descendants = self.rebloom_tracker.get_descendants(root_bloom_id)
        ancestry = self.rebloom_tracker.get_ancestry_chain(root_bloom_id)
        
        family_members = set([root_bloom_id] + (descendants or []) + (ancestry or []))
        
        routes = []
        successful_routes = 0
        
        print(f"[TracerRebloomIntegration] 🕸️ Routing {tracer_type} to family cluster of {len(family_members)} blooms")
        
        for bloom_id in family_members:
            # Ensure bloom target exists in router
            if bloom_id not in self.tracer_router.bloom_targets:
                # Create a bloom target based on rebloom data
                self._create_bloom_target_from_rebloom_data(bloom_id)
            
            # Route the tracer
            route_result = self.tracer_router.route(tracer_type, bloom_id)
            if route_result:
                routes.append(route_result)
                successful_routes += 1
        
        # Update statistics
        if successful_routes > 0:
            self.integration_stats['tracer_genealogy_matches'] += successful_routes
        
        print(f"[TracerRebloomIntegration] ✅ Successfully routed to {successful_routes}/{len(family_members)} family members")
        
        return routes
    
    def predict_optimal_rebloom_targets(self, tracer_type: str, min_score: float = 0.6) -> List[Dict[str, Any]]:
        """
        Predict optimal targets for future reblooms based on tracer capabilities and genealogy
        
        Args:
            tracer_type: Type of tracer for predictions
            min_score: Minimum optimization score for predictions
            
        Returns:
            List of predicted optimal rebloom targets
        """
        # Get available routes for the tracer
        available_routes = self.tracer_router.get_available_routes(tracer_type, limit=20)
        
        predictions = []
        
        for route in available_routes:
            bloom_id = route['bloom_id']
            
            # Get genealogy context
            depth = self.rebloom_tracker.get_depth(bloom_id)
            descendants = self.rebloom_tracker.get_descendants(bloom_id)
            siblings = self.rebloom_tracker.get_siblings(bloom_id)
            
            # Calculate rebloom potential
            rebloom_potential = self._calculate_rebloom_potential(
                route, depth, len(descendants or []), len(siblings or [])
            )
            
            if rebloom_potential >= min_score:
                prediction_reason = self._generate_rebloom_prediction_reason(
                    tracer_type, bloom_id, route, rebloom_potential
                )
                
                predictions.append({
                    'target_bloom_id': bloom_id,
                    'tracer_type': tracer_type,
                    'optimization_score': rebloom_potential,
                    'route_score': route['route_score'],
                    'genealogy_depth': depth,
                    'family_size': len(descendants or []),
                    'prediction_reason': prediction_reason,
                    'estimated_impact': min(1.0, rebloom_potential * 1.3)
                })
        
        # Sort by optimization score
        predictions.sort(key=lambda x: x['optimization_score'], reverse=True)
        
        print(f"[TracerRebloomIntegration] 🔮 Predicted {len(predictions)} optimal rebloom targets for {tracer_type}")
        
        return predictions
    
    def _analyze_bloom_genealogy(self, bloom_id: str, include_full_analysis: bool) -> Dict[str, Any]:
        """Analyze the genealogical context of a bloom"""
        analysis = {
            'bloom_id': bloom_id,
            'depth': self.rebloom_tracker.get_depth(bloom_id),
            'has_genealogy_data': bloom_id in self.rebloom_tracker.nodes
        }
        
        if not analysis['has_genealogy_data']:
            return analysis
        
        if include_full_analysis:
            analysis.update({
                'ancestry_chain': self.rebloom_tracker.get_ancestry_chain(bloom_id),
                'descendants': self.rebloom_tracker.get_descendants(bloom_id),
                'siblings': self.rebloom_tracker.get_siblings(bloom_id),
                'entropy_evolution': self.rebloom_tracker.get_entropy_evolution(bloom_id)
            })
            
            # Calculate family statistics
            descendants = analysis.get('descendants', [])
            ancestry = analysis.get('ancestry_chain', [])
            
            analysis['family_statistics'] = {
                'total_family_size': len(set(descendants + ancestry + [bloom_id])),
                'generation_depth': len(ancestry),
                'descendant_count': len(descendants),
                'is_root': len(ancestry) == 0,
                'is_leaf': len(descendants) == 0
            }
        
        return analysis
    
    def _analyze_family_context(self, bloom_id: str, tracer_type: str) -> Dict[str, Any]:
        """Analyze how the tracer type fits with the family context"""
        context = {
            'bloom_id': bloom_id,
            'tracer_type': tracer_type,
            'context_match_score': 0.0
        }
        
        # Get family data
        descendants = self.rebloom_tracker.get_descendants(bloom_id)
        ancestors = self.rebloom_tracker.get_ancestry_chain(bloom_id)
        
        if not descendants and not ancestors:
            context['context_type'] = 'isolated_bloom'
            context['context_match_score'] = 0.5
            return context
        
        # Analyze family structure
        family_size = len(set((descendants or []) + (ancestors or []) + [bloom_id]))
        generation_depth = len(ancestors or [])
        
        # Calculate context match based on tracer specialization
        if tracer_type == 'owl':
            # Owl prefers moderate-depth, well-structured families
            if 3 <= generation_depth <= 8 and family_size >= 5:
                context['context_match_score'] = 0.8
                context['context_type'] = 'deep_structured_family'
            else:
                context['context_match_score'] = 0.6
                context['context_type'] = 'standard_family'
                
        elif tracer_type == 'crow':
            # Crow prefers opportunities for weakness detection
            if family_size < 5 or generation_depth < 3:
                context['context_match_score'] = 0.7
                context['context_type'] = 'vulnerable_family'
            else:
                context['context_match_score'] = 0.4
                context['context_type'] = 'stable_family'
                
        elif tracer_type == 'spider':
            # Spider prefers interconnected families
            if family_size >= 8:
                context['context_match_score'] = 0.9
                context['context_type'] = 'highly_connected_family'
            else:
                context['context_match_score'] = 0.6
                context['context_type'] = 'connected_family'
                
        elif tracer_type == 'whale':
            # Whale prefers large, complex families
            if family_size >= 15 and generation_depth >= 5:
                context['context_match_score'] = 0.9
                context['context_type'] = 'massive_complex_family'
            else:
                context['context_match_score'] = 0.5
                context['context_type'] = 'moderate_family'
        
        context.update({
            'family_size': family_size,
            'generation_depth': generation_depth,
            'has_descendants': bool(descendants),
            'has_ancestors': bool(ancestors)
        })
        
        return context
    
    def _generate_cognitive_insights(self, tracer_route: RouteResult, 
                                   genealogy: Dict[str, Any], 
                                   family_context: Dict[str, Any]) -> List[str]:
        """Generate cognitive insights from the integrated analysis"""
        insights = []
        
        # Route quality insights
        if tracer_route.route_score > 0.8:
            insights.append(f"Excellent tracer-target match: {tracer_route.routing_reason}")
        elif tracer_route.route_score < 0.5:
            insights.append(f"Suboptimal routing detected: Consider alternative tracer for this target")
        
        # Genealogy insights
        if genealogy.get('has_genealogy_data'):
            depth = genealogy.get('depth', 0)
            if depth > 5:
                insights.append(f"Deep genealogical structure detected (depth {depth}): Ideal for pattern analysis")
            elif depth == 0:
                insights.append("Root bloom identified: Potential founding cognitive pattern")
            
            family_stats = genealogy.get('family_statistics', {})
            if family_stats.get('total_family_size', 0) > 10:
                insights.append("Large cognitive family detected: High potential for network effects")
        
        # Family context insights
        context_score = family_context.get('context_match_score', 0.0)
        if context_score > 0.8:
            insights.append(f"Optimal tracer-family alignment: {family_context.get('context_type')}")
        elif context_score < 0.4:
            insights.append("Poor tracer-family fit: Consider family-specialized routing")
        
        # Integration insights
        route_path_length = len(tracer_route.route_path)
        if route_path_length > 5 and genealogy.get('depth', 0) > 3:
            insights.append("Complex routing to deep genealogy: High cognitive processing potential")
        
        return insights
    
    def _generate_routing_recommendations(self, tracer_type: str, bloom_id: str,
                                        genealogy: Dict[str, Any],
                                        family_context: Dict[str, Any]) -> List[str]:
        """Generate recommendations for optimal routing"""
        recommendations = []
        
        # Context-based recommendations
        context_type = family_context.get('context_type', 'unknown')
        
        if context_type == 'isolated_bloom':
            recommendations.append("Consider Spider tracer for bridge-building to connect isolated bloom")
        elif context_type == 'vulnerable_family':
            recommendations.append("Crow tracer optimal for weakness analysis in small family structures")
        elif context_type == 'massive_complex_family':
            recommendations.append("Whale tracer recommended for comprehensive analysis of large family")
        
        # Genealogy-based recommendations
        if genealogy.get('has_genealogy_data'):
            family_stats = genealogy.get('family_statistics', {})
            
            if family_stats.get('is_root'):
                recommendations.append("Root bloom detected: Use Owl tracer for foundational pattern analysis")
            elif family_stats.get('is_leaf'):
                recommendations.append("Leaf bloom identified: Spider tracer effective for extension analysis")
            
            if family_stats.get('descendant_count', 0) > 8:
                recommendations.append("High descendant count: Consider Whale tracer for family cluster analysis")
        
        # Performance recommendations
        route_score = family_context.get('context_match_score', 0.0)
        if route_score < 0.6:
            recommendations.append(f"Low context match: Try alternative tracers for better family alignment")
        
        return recommendations
    
    def _calculate_family_match_score(self, tracer_type: str, depth: int, size: int, 
                                    avg_entropy: float, capabilities) -> float:
        """Calculate how well a tracer type matches a family structure"""
        score = 0.0
        
        # Depth matching
        min_depth, max_depth = capabilities.preferred_depth_range
        if min_depth <= depth <= max_depth:
            score += 0.3
        else:
            distance = min(abs(depth - min_depth), abs(depth - max_depth))
            score += max(0.0, 0.3 - (distance * 0.1))
        
        # Size/complexity matching
        if tracer_type == 'whale' and size > 10:
            score += 0.3
        elif tracer_type == 'spider' and size >= 5:
            score += 0.25
        elif tracer_type == 'owl' and 3 <= size <= 12:
            score += 0.25
        elif tracer_type == 'crow' and size < 8:
            score += 0.2
        
        # Entropy matching
        min_entropy, max_entropy = capabilities.entropy_affinity
        if min_entropy <= avg_entropy <= max_entropy:
            score += 0.4
        else:
            if avg_entropy < min_entropy:
                entropy_score = avg_entropy / min_entropy
            else:
                entropy_score = max_entropy / avg_entropy
            score += max(0.0, entropy_score * 0.4)
        
        return min(1.0, score)
    
    def _generate_family_suggestion_reason(self, tracer_type: str, depth: int, 
                                         size: int, avg_entropy: float) -> str:
        """Generate reasoning for family tracer suggestions"""
        if tracer_type == 'owl':
            return f"Deep pattern analysis ideal for family depth {depth} with moderate complexity"
        elif tracer_type == 'crow':
            if size < 5:
                return f"Small family structure ({size} members) suitable for vulnerability analysis"
            else:
                return f"Opportunistic analysis potential in {size}-member family"
        elif tracer_type == 'spider':
            return f"Bridge construction optimal for {size}-member interconnected family"
        elif tracer_type == 'whale':
            return f"High-capacity processing required for large family ({size} members, entropy {avg_entropy:.2f})"
        return f"Specialized analysis for family characteristics"
    
    def _calculate_rebloom_potential(self, route: Dict[str, Any], depth: int, 
                                   descendants: int, siblings: int) -> float:
        """Calculate the potential for optimal reblooming"""
        base_score = route['route_score']
        
        # Depth bonus (moderate depth is optimal for reblooming)
        if 2 <= depth <= 6:
            depth_bonus = 0.2
        else:
            depth_bonus = max(0.0, 0.2 - abs(depth - 4) * 0.05)
        
        # Family context bonus
        family_bonus = 0.0
        if descendants > 0:
            family_bonus += 0.1  # Has productive lineage
        if siblings > 2:
            family_bonus += 0.1  # Rich sibling context
        
        # Success probability bonus
        success_bonus = route.get('success_probability', 0.5) * 0.2
        
        potential = base_score + depth_bonus + family_bonus + success_bonus
        return min(1.0, potential)
    
    def _generate_rebloom_prediction_reason(self, tracer_type: str, bloom_id: str,
                                          route: Dict[str, Any], potential: float) -> str:
        """Generate reasoning for rebloom predictions"""
        return (f"{tracer_type.title()} tracer shows {potential:.1%} optimization potential "
                f"for {bloom_id} based on route score {route['route_score']:.2f} "
                f"and genealogical context")
    
    def _create_bloom_target_from_rebloom_data(self, bloom_id: str):
        """Create a bloom target in the router based on rebloom tracker data"""
        # Get rebloom data if available
        depth = self.rebloom_tracker.get_depth(bloom_id)
        
        # Use reasonable defaults based on depth
        entropy = min(0.9, 0.3 + (depth * 0.1))
        complexity = min(0.8, 0.4 + (depth * 0.08))
        
        scup_values = {
            'schema': random.uniform(0.3, 0.8),
            'coherence': random.uniform(0.4, 0.9),
            'utility': random.uniform(0.3, 0.8),
            'pressure': random.uniform(0.2, 0.7)
        }
        
        self.tracer_router.add_bloom_target(
            bloom_id=bloom_id,
            depth=depth,
            entropy=entropy,
            complexity=complexity,
            scup_values=scup_values,
            rebloom_status='stable'
        )
    
    def _update_integration_stats(self, success: bool, analysis_time: float):
        """Update integration statistics"""
        self.integration_stats['total_analyses'] += 1
        if success:
            self.integration_stats['successful_integrations'] += 1
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive integration statistics"""
        stats = self.integration_stats.copy()
        
        # Add system statistics
        stats['tracer_router_stats'] = self.tracer_router.get_routing_statistics()
        stats['rebloom_tracker_stats'] = self.rebloom_tracker.get_lineage_statistics()
        
        # Calculate integration efficiency
        if stats['total_analyses'] > 0:
            stats['integration_efficiency'] = stats['successful_integrations'] / stats['total_analyses']
        else:
            stats['integration_efficiency'] = 0.0
        
        return stats
    
    def export_integration_data(self, filename: str = None) -> str:
        """Export integration analysis data"""
        if filename is None:
            filename = f"integration_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'integration_statistics': self.get_integration_statistics(),
            'analysis_history': [result.to_dict() for result in self.analysis_history[-50:]],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"[TracerRebloomIntegration] 📁 Integration data exported to {filename}")
        return filename


# Example usage and demonstration
if __name__ == "__main__":
    print("🧠🕸️ DAWN Tracer-Rebloom Integration Test")
    print("=" * 50)
    
    # Create integrated system
    integration = TracerRebloomIntegration()
    
    # Add some rebloom data
    integration.rebloom_tracker.log_rebloom('bloom_001', None, 0.5)
    integration.rebloom_tracker.log_rebloom('bloom_002', 'bloom_001', 0.6)
    integration.rebloom_tracker.log_rebloom('bloom_003', 'bloom_001', 0.4)
    integration.rebloom_tracker.log_rebloom('bloom_004', 'bloom_002', 0.7)
    integration.rebloom_tracker.log_rebloom('bloom_005', 'bloom_002', 0.3)
    
    # Add corresponding bloom targets
    integration.tracer_router.add_bloom_target('bloom_001', depth=0, entropy=0.5, complexity=0.6)
    integration.tracer_router.add_bloom_target('bloom_002', depth=1, entropy=0.6, complexity=0.7)
    integration.tracer_router.add_bloom_target('bloom_003', depth=1, entropy=0.4, complexity=0.5)
    integration.tracer_router.add_bloom_target('bloom_004', depth=2, entropy=0.7, complexity=0.8)
    integration.tracer_router.add_bloom_target('bloom_005', depth=2, entropy=0.3, complexity=0.4)
    
    print("\n🎯 Testing Integrated Analysis:")
    print("-" * 40)
    
    # Test integrated analysis
    for tracer in ['owl', 'spider']:
        print(f"\n{tracer.upper()} Integrated Analysis:")
        result = integration.analyze_with_routing(tracer, 'bloom_004', include_family_analysis=True)
        
        if result:
            print(f"  ✅ Route Score: {result.tracer_route.route_score:.2f}")
            print(f"  🧬 Family Size: {result.family_context.get('family_size', 0)}")
            print(f"  💡 Insights: {len(result.cognitive_insights)}")
            for insight in result.cognitive_insights[:2]:
                print(f"     • {insight}")
    
    print(f"\n🔍 Family Tracer Suggestions:")
    suggestions = integration.suggest_optimal_tracers_for_family('bloom_001', max_suggestions=3)
    for suggestion in suggestions:
        print(f"  {suggestion['tracer_type']}: {suggestion['family_match_score']:.2f} - {suggestion['suggestion_reason']}")
    
    print(f"\n🔮 Rebloom Predictions:")
    predictions = integration.predict_optimal_rebloom_targets('owl', min_score=0.5)
    for pred in predictions[:3]:
        print(f"  {pred['target_bloom_id']}: {pred['optimization_score']:.2f} - {pred['prediction_reason']}")
    
    print(f"\n📊 Integration Statistics:")
    stats = integration.get_integration_statistics()
    print(f"  Total Analyses: {stats['total_analyses']}")
    print(f"  Integration Efficiency: {stats['integration_efficiency']:.1%}")
    print(f"  Tracer-Genealogy Matches: {stats['tracer_genealogy_matches']}")
    
    print(f"\n🧠🕸️ Integration test complete!") 