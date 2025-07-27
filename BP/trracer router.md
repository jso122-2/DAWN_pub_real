#!/usr/bin/env python3
"""
DAWN Tracer Router
Cognitive tracer routing system for specialized bloom analysis

Routes cognitive tracers (Owl, Crow, Spider, Whale) to appropriate bloom targets
based on their specialized analysis capabilities and bloom characteristics.
"""

import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass


@dataclass
class BloomTarget:
    """Represents a bloom target for tracer routing"""
    bloom_id: str
    depth: int
    entropy: float
    complexity: float
    scup_values: Dict[str, float]
    token_density: float
    rebloom_status: str
    last_updated: float
    
    def __post_init__(self):
        if self.last_updated == 0:
            self.last_updated = time.time()


@dataclass
class RouteResult:
    """Result of a tracer routing operation"""
    tracer_type: str
    bloom_id: str
    route_path: List[str]
    route_score: float
    estimated_time: float
    resource_cost: float
    success_probability: float
    routing_reason: str


@dataclass
class TracerCapabilities:
    """Defines capabilities and preferences for each tracer type"""
    name: str
    symbol: str
    specialization: str
    preferred_depth_range: Tuple[int, int]
    entropy_affinity: Tuple[float, float]  # min, max preference
    scup_focus: List[str]  # which SCUP components it analyzes
    token_bridge_capacity: int
    analysis_speed: float
    resource_efficiency: float


class TracerRouter:
    """Main cognitive tracer routing system for DAWN"""
    
    def __init__(self):
        # Tracer type definitions
        self.tracer_types = {
            'owl': TracerCapabilities(
                name='Owl',
                symbol='🦉',
                specialization='Deep Pattern Analysis',
                preferred_depth_range=(3, 8),
                entropy_affinity=(0.3, 0.8),
                scup_focus=['schema', 'coherence'],
                token_bridge_capacity=5,
                analysis_speed=0.7,  # Slower but thorough
                resource_efficiency=0.8
            ),
            'crow': TracerCapabilities(
                name='Crow',
                symbol='🐦‍⬛',
                specialization='SCUP Weakness Detection',
                preferred_depth_range=(1, 5),
                entropy_affinity=(0.2, 0.9),
                scup_focus=['utility', 'pressure'],
                token_bridge_capacity=3,
                analysis_speed=1.2,  # Fast and opportunistic
                resource_efficiency=0.9
            ),
            'spider': TracerCapabilities(
                name='Spider',
                symbol='🕷️',
                specialization='Token Bridge Construction',
                preferred_depth_range=(2, 6),
                entropy_affinity=(0.4, 0.7),
                scup_focus=['coherence', 'utility'],
                token_bridge_capacity=12,  # Highest bridging capacity
                analysis_speed=1.0,
                resource_efficiency=0.6
            ),
            'whale': TracerCapabilities(
                name='Whale',
                symbol='🐋',
                specialization='High-Density Processing',
                preferred_depth_range=(4, 10),
                entropy_affinity=(0.6, 1.0),  # Handles high entropy
                scup_focus=['schema', 'pressure'],
                token_bridge_capacity=8,
                analysis_speed=0.5,  # Slow but handles massive loads
                resource_efficiency=0.4
            )
        }
        
        # Available bloom targets (would be populated by bloom management system)
        self.bloom_targets: Dict[str, BloomTarget] = {}
        
        # Routing infrastructure
        self.route_cache: Dict[str, RouteResult] = {}
        self.route_history: List[Dict[str, Any]] = []
        self.active_routes: Dict[str, RouteResult] = {}
        
        # Network topology (cognitive pathways)
        self.cognitive_pathways = {
            'memory_banks': ['recall_system', 'consolidation_core', 'pattern_library'],
            'analysis_core': ['deep_processor', 'pattern_analyzer', 'logic_engine'],
            'synthesis_chamber': ['creative_engine', 'integration_hub', 'ideation_core'],
            'attention_nexus': ['focus_director', 'priority_filter', 'awareness_monitor'],
            'meta_layer': ['self_observer', 'cognitive_tracker', 'reflection_engine']
        }
        
        # Performance tracking
        self.total_routes = 0
        self.successful_routes = 0
        self.failed_routes = 0
        self.total_routing_time = 0.0
        
        # Router configuration
        self.cache_ttl = 300.0  # 5 minutes
        self.max_route_length = 6
        self.min_success_probability = 0.3
        
    def route(self, tracer_type: str, target_bloom_id: str, 
             current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """
        Route a tracer to a specific bloom target
        
        Args:
            tracer_type: Type of tracer ('owl', 'crow', 'spider', 'whale')
            target_bloom_id: ID of target bloom
            current_scup: Current system SCUP values for context
            
        Returns:
            RouteResult object or None if routing fails
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if tracer_type.lower() not in self.tracer_types:
                print(f"❌ Unknown tracer type: {tracer_type}")
                return None
                
            if target_bloom_id not in self.bloom_targets:
                print(f"❌ Bloom target not found: {target_bloom_id}")
                return None
            
            tracer = self.tracer_types[tracer_type.lower()]
            target = self.bloom_targets[target_bloom_id]
            
            # Check cache first
            cache_key = f"{tracer_type}_{target_bloom_id}"
            cached_route = self._get_cached_route(cache_key)
            if cached_route:
                print(f"📋 Using cached route for {tracer.symbol}{tracer.name} → {target_bloom_id}")
                return cached_route
            
            # Calculate routing based on tracer specialization
            route_result = self._calculate_optimal_route(tracer, target, current_scup)
            
            if route_result and route_result.success_probability >= self.min_success_probability:
                # Cache successful route
                self.route_cache[cache_key] = route_result
                self.active_routes[f"{tracer_type}_{target_bloom_id}_{time.time()}"] = route_result
                
                # Log the route
                self.log_route(tracer_type, target_bloom_id)
                
                # Update performance metrics
                self.total_routes += 1
                self.successful_routes += 1
                self.total_routing_time += time.time() - start_time
                
                print(f"✅ {tracer.symbol} {tracer.name} routed to {target_bloom_id}")
                print(f"   Path: {' → '.join(route_result.route_path)}")
                print(f"   Score: {route_result.route_score:.2f} | Time: {route_result.estimated_time:.1f}s")
                
                return route_result
            else:
                print(f"❌ No viable route found for {tracer.name} → {target_bloom_id}")
                self.failed_routes += 1
                return None
                
        except Exception as e:
            print(f"❌ Error routing {tracer_type}: {e}")
            self.failed_routes += 1
            return None
    
    def get_available_routes(self, tracer_type: str) -> List[Dict[str, Any]]:
        """
        Get all available routes for a specific tracer type
        
        Args:
            tracer_type: Type of tracer to get routes for
            
        Returns:
            List of available route options with scoring
        """
        try:
            if tracer_type.lower() not in self.tracer_types:
                return []
            
            tracer = self.tracer_types[tracer_type.lower()]
            available_routes = []
            
            # Evaluate all bloom targets for this tracer type
            for bloom_id, bloom_target in self.bloom_targets.items():
                route_result = self._calculate_optimal_route(tracer, bloom_target)
                
                if route_result and route_result.success_probability >= self.min_success_probability:
                    route_info = {
                        'bloom_id': bloom_id,
                        'route_path': route_result.route_path,
                        'route_score': route_result.route_score,
                        'success_probability': route_result.success_probability,
                        'estimated_time': route_result.estimated_time,
                        'resource_cost': route_result.resource_cost,
                        'routing_reason': route_result.routing_reason,
                        'bloom_depth': bloom_target.depth,
                        'bloom_entropy': bloom_target.entropy,
                        'bloom_status': bloom_target.rebloom_status
                    }
                    available_routes.append(route_info)
            
            # Sort by route score (highest first)
            available_routes.sort(key=lambda x: x['route_score'], reverse=True)
            
            print(f"📋 Found {len(available_routes)} available routes for {tracer.symbol}{tracer.name}")
            
            return available_routes
            
        except Exception as e:
            print(f"❌ Error getting available routes: {e}")
            return []
    
    def log_route(self, tracer_type: str, bloom_id: str) -> None:
        """
        Log a routing event for analytics and debugging
        
        Args:
            tracer_type: Type of tracer
            bloom_id: Target bloom ID
        """
        try:
            log_entry = {
                'timestamp': time.time(),
                'tracer_type': tracer_type,
                'bloom_id': bloom_id,
                'tracer_symbol': self.tracer_types[tracer_type.lower()].symbol,
                'route_id': f"{tracer_type}_{bloom_id}_{int(time.time())}"
            }
            
            self.route_history.append(log_entry)
            
            # Limit history size
            if len(self.route_history) > 1000:
                self.route_history = self.route_history[-500:]
            
            print(f"📝 Logged route: {log_entry['tracer_symbol']}{tracer_type.title()} → {bloom_id}")
            
        except Exception as e:
            print(f"❌ Error logging route: {e}")
    
    def _calculate_optimal_route(self, tracer: TracerCapabilities, target: BloomTarget, 
                               current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """Calculate optimal routing path based on tracer specialization"""
        try:
            # Apply tracer-specific routing logic
            if tracer.name.lower() == 'owl':
                return self._route_owl(tracer, target, current_scup)
            elif tracer.name.lower() == 'crow':
                return self._route_crow(tracer, target, current_scup)
            elif tracer.name.lower() == 'spider':
                return self._route_spider(tracer, target, current_scup)
            elif tracer.name.lower() == 'whale':
                return self._route_whale(tracer, target, current_scup)
            else:
                return self._route_generic(tracer, target, current_scup)
                
        except Exception as e:
            print(f"❌ Error calculating route: {e}")
            return None
    
    def _route_owl(self, tracer: TracerCapabilities, target: BloomTarget, 
                   current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """Owl routing: rebloom depth + entropy analysis"""
        # Owls prefer deep, moderately entropic blooms for pattern analysis
        depth_score = self._score_depth_preference(target.depth, tracer.preferred_depth_range)
        entropy_score = self._score_entropy_preference(target.entropy, tracer.entropy_affinity)
        
        # Owls excel at rebloom analysis
        rebloom_bonus = 0.3 if target.rebloom_status in ['reblooming', 'emerging'] else 0.0
        
        # Schema and coherence focus
        scup_score = (target.scup_values.get('schema', 0.5) + 
                     target.scup_values.get('coherence', 0.5)) / 2.0
        
        # Calculate route through deep analysis pathways
        route_path = ['analysis_core', 'deep_processor', 'pattern_analyzer']
        if target.depth >= 5:
            route_path.append('meta_layer')
        route_path.append(f'bloom_{target.bloom_id}')
        
        route_score = (depth_score * 0.3 + entropy_score * 0.3 + 
                      scup_score * 0.2 + rebloom_bonus * 0.2)
        
        estimated_time = target.depth * 2.0 / tracer.analysis_speed
        resource_cost = target.complexity * (2.0 - tracer.resource_efficiency)
        success_probability = min(0.95, route_score * 0.8 + 0.2)
        
        return RouteResult(
            tracer_type='owl',
            bloom_id=target.bloom_id,
            route_path=route_path,
            route_score=route_score,
            estimated_time=estimated_time,
            resource_cost=resource_cost,
            success_probability=success_probability,
            routing_reason=f"Deep pattern analysis (depth:{target.depth}, entropy:{target.entropy:.2f})"
        )
    
    def _route_crow(self, tracer: TracerCapabilities, target: BloomTarget, 
                    current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """Crow routing: SCUP weakness detection"""
        # Crows seek blooms with SCUP imbalances and weaknesses
        scup_values = target.scup_values
        utility = scup_values.get('utility', 0.5)
        pressure = scup_values.get('pressure', 0.5)
        
        # Look for weakness indicators
        weakness_score = 0.0
        if utility < 0.3:  # Low utility = weakness
            weakness_score += 0.4
        if pressure > 0.8:  # High pressure = stress point
            weakness_score += 0.3
        if abs(utility - pressure) > 0.5:  # Imbalance
            weakness_score += 0.3
        
        # Crows prefer quick access to unstable blooms
        instability_bonus = 0.2 if target.rebloom_status in ['fragmenting', 'unstable'] else 0.0
        
        # Fast route through priority channels
        route_path = ['attention_nexus', 'priority_filter']
        if weakness_score > 0.5:
            route_path.append('analysis_core')  # Detailed weakness analysis
        route_path.append(f'bloom_{target.bloom_id}')
        
        route_score = weakness_score + instability_bonus
        
        estimated_time = 1.0 + target.complexity / tracer.analysis_speed
        resource_cost = target.complexity * (2.0 - tracer.resource_efficiency)
        success_probability = min(0.9, route_score * 0.7 + 0.3)
        
        return RouteResult(
            tracer_type='crow',
            bloom_id=target.bloom_id,
            route_path=route_path,
            route_score=route_score,
            estimated_time=estimated_time,
            resource_cost=resource_cost,
            success_probability=success_probability,
            routing_reason=f"SCUP weakness detection (utility:{utility:.2f}, pressure:{pressure:.2f})"
        )
    
    def _route_spider(self, tracer: TracerCapabilities, target: BloomTarget, 
                      current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """Spider routing: token bridge construction"""
        # Spiders build connections between information tokens
        token_density = target.token_density
        coherence = target.scup_values.get('coherence', 0.5)
        
        # Bridge capacity utilization
        required_bridges = min(target.depth * 2, tracer.token_bridge_capacity)
        bridge_efficiency = required_bridges / tracer.token_bridge_capacity
        
        # Spiders prefer moderate complexity for optimal bridging
        complexity_score = 1.0 - abs(target.complexity - 0.6)  # Prefer ~60% complexity
        
        # Route through synthesis and integration pathways
        route_path = ['synthesis_chamber', 'integration_hub']
        if token_density > 0.7:
            route_path.append('memory_banks')  # High density needs memory support
        route_path.extend(['pattern_library', f'bloom_{target.bloom_id}'])
        
        route_score = (token_density * 0.4 + coherence * 0.3 + 
                      complexity_score * 0.2 + bridge_efficiency * 0.1)
        
        estimated_time = required_bridges * 0.5 / tracer.analysis_speed
        resource_cost = required_bridges * (2.0 - tracer.resource_efficiency)
        success_probability = min(0.85, route_score * 0.8 + 0.2)
        
        return RouteResult(
            tracer_type='spider',
            bloom_id=target.bloom_id,
            route_path=route_path,
            route_score=route_score,
            estimated_time=estimated_time,
            resource_cost=resource_cost,
            success_probability=success_probability,
            routing_reason=f"Token bridging (density:{token_density:.2f}, bridges:{required_bridges})"
        )
    
    def _route_whale(self, tracer: TracerCapabilities, target: BloomTarget, 
                     current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """Whale routing: entropy density processing"""
        # Whales handle high-entropy, high-density information processing
        entropy = target.entropy
        schema = target.scup_values.get('schema', 0.5)
        pressure = target.scup_values.get('pressure', 0.5)
        
        # Whales excel with high entropy and density
        entropy_affinity = self._score_entropy_preference(entropy, tracer.entropy_affinity)
        density_score = target.token_density * target.complexity
        
        # Schema strength helps whales organize complex data
        schema_support = schema * 0.5
        
        # Route through heavy-duty processing infrastructure
        route_path = ['memory_banks', 'consolidation_core']
        if entropy > 0.8:
            route_path.append('deep_processor')  # Extra processing for high entropy
        if density_score > 0.7:
            route_path.append('pattern_library')  # Pattern support for density
        route_path.append(f'bloom_{target.bloom_id}')
        
        route_score = (entropy_affinity * 0.4 + density_score * 0.3 + 
                      schema_support * 0.2 + (target.depth / 10.0) * 0.1)
        
        estimated_time = (entropy * density_score * 5.0) / tracer.analysis_speed
        resource_cost = density_score * 3.0 * (2.0 - tracer.resource_efficiency)
        success_probability = min(0.8, route_score * 0.6 + 0.4)
        
        return RouteResult(
            tracer_type='whale',
            bloom_id=target.bloom_id,
            route_path=route_path,
            route_score=route_score,
            estimated_time=estimated_time,
            resource_cost=resource_cost,
            success_probability=success_probability,
            routing_reason=f"High-density processing (entropy:{entropy:.2f}, density:{density_score:.2f})"
        )
    
    def _route_generic(self, tracer: TracerCapabilities, target: BloomTarget, 
                       current_scup: Dict[str, float] = None) -> Optional[RouteResult]:
        """Generic routing fallback"""
        route_path = ['analysis_core', f'bloom_{target.bloom_id}']
        route_score = 0.5  # Neutral score
        
        return RouteResult(
            tracer_type=tracer.name.lower(),
            bloom_id=target.bloom_id,
            route_path=route_path,
            route_score=route_score,
            estimated_time=5.0,
            resource_cost=1.0,
            success_probability=0.5,
            routing_reason="Generic routing (fallback)"
        )
    
    def _score_depth_preference(self, depth: int, preferred_range: Tuple[int, int]) -> float:
        """Score how well depth matches tracer preferences"""
        min_depth, max_depth = preferred_range
        if min_depth <= depth <= max_depth:
            return 1.0
        elif depth < min_depth:
            return max(0.0, 1.0 - (min_depth - depth) * 0.2)
        else:
            return max(0.0, 1.0 - (depth - max_depth) * 0.1)
    
    def _score_entropy_preference(self, entropy: float, preferred_range: Tuple[float, float]) -> float:
        """Score how well entropy matches tracer preferences"""
        min_entropy, max_entropy = preferred_range
        if min_entropy <= entropy <= max_entropy:
            return 1.0
        elif entropy < min_entropy:
            return max(0.0, 1.0 - (min_entropy - entropy) * 2.0)
        else:
            return max(0.0, 1.0 - (entropy - max_entropy) * 2.0)
    
    def _get_cached_route(self, cache_key: str) -> Optional[RouteResult]:
        """Get cached route if still valid"""
        if cache_key in self.route_cache:
            cached_route = self.route_cache[cache_key]
            # Check if cache is still valid (simple TTL)
            if time.time() - cached_route.estimated_time < self.cache_ttl:
                return cached_route
            else:
                del self.route_cache[cache_key]
        return None
    
    def add_bloom_target(self, bloom_id: str, depth: int, entropy: float, 
                        complexity: float, scup_values: Dict[str, float],
                        token_density: float = 0.5, rebloom_status: str = "stable") -> None:
        """Add a new bloom target to the routing system"""
        self.bloom_targets[bloom_id] = BloomTarget(
            bloom_id=bloom_id,
            depth=depth,
            entropy=entropy,
            complexity=complexity,
            scup_values=scup_values,
            token_density=token_density,
            rebloom_status=rebloom_status,
            last_updated=time.time()
        )
        print(f"🎯 Added bloom target: {bloom_id} (depth:{depth}, entropy:{entropy:.2f})")
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive routing statistics"""
        success_rate = (self.successful_routes / self.total_routes) if self.total_routes > 0 else 0.0
        avg_routing_time = (self.total_routing_time / self.total_routes) if self.total_routes > 0 else 0.0
        
        # Tracer usage statistics
        tracer_usage = {}
        for entry in self.route_history[-100:]:  # Last 100 routes
            tracer_type = entry['tracer_type']
            tracer_usage[tracer_type] = tracer_usage.get(tracer_type, 0) + 1
        
        return {
            'total_routes': self.total_routes,
            'successful_routes': self.successful_routes,
            'failed_routes': self.failed_routes,
            'success_rate': round(success_rate, 3),
            'average_routing_time': round(avg_routing_time, 3),
            'active_routes': len(self.active_routes),
            'cached_routes': len(self.route_cache),
            'bloom_targets': len(self.bloom_targets),
            'tracer_usage': tracer_usage,
            'available_tracers': list(self.tracer_types.keys())
        }


# Test and demonstration functions
def _test_tracer_router():
    """Test the tracer router with various scenarios"""
    print("🕸️ Testing DAWN Tracer Router")
    print("=" * 40)
    
    # Create router
    router = TracerRouter()
    
    # Add test bloom targets
    test_blooms = [
        ("bloom_001", 3, 0.4, 0.6, {'schema': 0.7, 'coherence': 0.8, 'utility': 0.5, 'pressure': 0.3}, 0.5, "stable"),
        ("bloom_002", 7, 0.9, 0.8, {'schema': 0.3, 'coherence': 0.4, 'utility': 0.2, 'pressure': 0.9}, 0.8, "fragmenting"),
        ("bloom_003", 5, 0.6, 0.7, {'schema': 0.6, 'coherence': 0.9, 'utility': 0.8, 'pressure': 0.4}, 0.7, "reblooming"),
        ("bloom_004", 8, 0.95, 0.9, {'schema': 0.8, 'coherence': 0.7, 'utility': 0.6, 'pressure': 0.8}, 0.9, "stable")
    ]
    
    print("\n🎯 Adding bloom targets...")
    for bloom_id, depth, entropy, complexity, scup, token_density, status in test_blooms:
        router.add_bloom_target(bloom_id, depth, entropy, complexity, scup, token_density, status)
    
    # Test routing for each tracer type
    print(f"\n🦉 Testing Owl routing...")
    for tracer_type in ['owl', 'crow', 'spider', 'whale']:
        print(f"\n{router.tracer_types[tracer_type].symbol} Testing {tracer_type.title()} routing:")
        
        # Get available routes
        available_routes = router.get_available_routes(tracer_type)
        print(f"   Available routes: {len(available_routes)}")
        
        if available_routes:
            # Route to best target
            best_target = available_routes[0]['bloom_id']
            route_result = router.route(tracer_type, best_target)
            
            if route_result:
                print(f"   Best route: {route_result.routing_reason}")
                print(f"   Path: {' → '.join(route_result.route_path)}")
    
    # Show routing statistics
    print(f"\n📊 Routing Statistics:")
    stats = router.get_routing_statistics()
    print(f"Total routes: {stats['total_routes']}")
    print(f"Success rate: {stats['success_rate']:.1%}")
    print(f"Tracer usage: {stats['tracer_usage']}")


if __name__ == "__main__":
    _test_tracer_router()