#!/usr/bin/env python3
"""
tracer_router.py - DAWN Cognitive Tracer Routing System
Intelligently routes specialized tracers (Owl, Crow, Spider, Whale) to optimal bloom targets
based on their unique capabilities and analysis specializations.
"""

import time
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum


class TracerType(Enum):
    """Specialized tracer types with unique capabilities"""
    OWL = "owl"           # 🦉 Deep Pattern Analysis
    CROW = "crow"         # 🐦‍⬛ SCUP Weakness Detection  
    SPIDER = "spider"     # 🕷️ Token Bridge Construction
    WHALE = "whale"       # 🐋 High-Density Processing


@dataclass
class TracerCapabilities:
    """Defines the capabilities and preferences of a tracer type"""
    preferred_depth_range: Tuple[int, int]    # Optimal working depth
    entropy_affinity: Tuple[float, float]     # Entropy preference range
    token_bridge_capacity: int                # Max simultaneous connections
    analysis_speed: float                     # Processing speed multiplier
    resource_efficiency: float               # Resource usage efficiency
    scup_focus: List[str]                    # Preferred SCUP components
    specialization_bonus: float             # Bonus for specialized tasks


@dataclass
class BloomTarget:
    """Represents a bloom target for tracer routing"""
    bloom_id: str
    depth: int = 0
    entropy: float = 0.5
    complexity: float = 0.5
    scup_values: Dict[str, float] = field(default_factory=dict)
    token_density: float = 0.5
    rebloom_status: str = "stable"
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'bloom_id': self.bloom_id,
            'depth': self.depth,
            'entropy': self.entropy,
            'complexity': self.complexity,
            'scup_values': self.scup_values,
            'token_density': self.token_density,
            'rebloom_status': self.rebloom_status,
            'last_updated': self.last_updated.isoformat()
        }


@dataclass
class RouteResult:
    """Result of a tracer routing operation"""
    tracer_type: str
    target_bloom_id: str
    route_path: List[str]
    route_score: float
    estimated_time: float
    resource_cost: float
    success_probability: float
    routing_reason: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        tracer_emoji = {'owl': '🦉', 'crow': '🐦‍⬛', 'spider': '🕷️', 'whale': '🐋'}
        emoji = tracer_emoji.get(self.tracer_type, '🔍')
        
        return (f"✅ {emoji} {self.tracer_type.title()} routed to {self.target_bloom_id}\n"
                f"Path: {' → '.join(self.route_path)}\n"
                f"Score: {self.route_score:.2f} | Time: {self.estimated_time:.1f}s")


class TracerRouter:
    """
    Sophisticated cognitive tracer routing system that intelligently routes
    specialized tracers to optimal bloom targets based on capabilities and analysis needs.
    """
    
    def __init__(self):
        """Initialize the tracer router"""
        # Bloom targets registry
        self.bloom_targets: Dict[str, BloomTarget] = {}
        
        # Route cache for performance optimization
        self.route_cache: Dict[str, Tuple[RouteResult, datetime]] = {}
        self.cache_ttl = timedelta(minutes=5)
        
        # Route history and statistics
        self.route_history: List[RouteResult] = []
        self.active_routes: Dict[str, RouteResult] = {}
        
        # Performance tracking
        self.routing_stats = {
            'total_routes': 0,
            'successful_routes': 0,
            'cache_hits': 0,
            'tracer_usage': defaultdict(int),
            'average_routing_time': 0.0
        }
        
        # Initialize tracer capabilities
        self.tracer_capabilities = self._initialize_tracer_capabilities()
        
        # Cognitive pathway network
        self.cognitive_pathways = self._initialize_cognitive_pathways()
        
        print("[TracerRouter] 🕸️ Cognitive tracer routing system initialized")
    
    def _initialize_tracer_capabilities(self) -> Dict[TracerType, TracerCapabilities]:
        """Initialize the capabilities for each tracer type"""
        return {
            TracerType.OWL: TracerCapabilities(
                preferred_depth_range=(3, 8),
                entropy_affinity=(0.3, 0.8),
                token_bridge_capacity=6,
                analysis_speed=0.7,
                resource_efficiency=0.8,
                scup_focus=['schema', 'coherence'],
                specialization_bonus=0.3
            ),
            TracerType.CROW: TracerCapabilities(
                preferred_depth_range=(1, 5),
                entropy_affinity=(0.6, 1.0),
                token_bridge_capacity=3,
                analysis_speed=0.9,
                resource_efficiency=0.6,
                scup_focus=['utility', 'pressure'],
                specialization_bonus=0.4
            ),
            TracerType.SPIDER: TracerCapabilities(
                preferred_depth_range=(2, 6),
                entropy_affinity=(0.4, 0.7),
                token_bridge_capacity=12,
                analysis_speed=0.8,
                resource_efficiency=0.9,
                scup_focus=['coherence', 'utility'],
                specialization_bonus=0.35
            ),
            TracerType.WHALE: TracerCapabilities(
                preferred_depth_range=(4, 10),
                entropy_affinity=(0.6, 1.0),
                token_bridge_capacity=8,
                analysis_speed=0.5,
                resource_efficiency=0.7,
                scup_focus=['schema', 'pressure'],
                specialization_bonus=0.5
            )
        }
    
    def _initialize_cognitive_pathways(self) -> Dict[str, List[str]]:
        """Initialize the cognitive pathway network"""
        return {
            'memory_banks': ['recall_system', 'consolidation_core', 'pattern_library'],
            'analysis_core': ['deep_processor', 'pattern_analyzer', 'logic_engine'],
            'synthesis_chamber': ['creative_engine', 'integration_hub', 'ideation_core'],
            'attention_nexus': ['focus_director', 'priority_filter', 'awareness_monitor'],
            'meta_layer': ['self_observer', 'cognitive_tracker', 'reflection_engine']
        }
    
    def add_bloom_target(self, bloom_id: str, depth: int = 0, entropy: float = 0.5,
                        complexity: float = 0.5, scup_values: Optional[Dict[str, float]] = None,
                        token_density: float = 0.5, rebloom_status: str = "stable") -> bool:
        """
        Add or update a bloom target for routing
        
        Args:
            bloom_id: Unique identifier for the bloom
            depth: Cognitive depth level
            entropy: Information chaos level (0-1)
            complexity: Processing complexity (0-1)
            scup_values: Schema, Coherence, Utility, Pressure values
            token_density: Information token density
            rebloom_status: Current rebloom status
            
        Returns:
            True if successfully added/updated
        """
        if scup_values is None:
            scup_values = {
                'schema': random.uniform(0.2, 0.8),
                'coherence': random.uniform(0.3, 0.9),
                'utility': random.uniform(0.2, 0.8),
                'pressure': random.uniform(0.1, 0.7)
            }
        
        target = BloomTarget(
            bloom_id=bloom_id,
            depth=depth,
            entropy=entropy,
            complexity=complexity,
            scup_values=scup_values,
            token_density=token_density,
            rebloom_status=rebloom_status
        )
        
        self.bloom_targets[bloom_id] = target
        
        # Invalidate related cache entries
        self._invalidate_cache_for_bloom(bloom_id)
        
        print(f"[TracerRouter] 📍 Added bloom target: {bloom_id} (depth={depth}, entropy={entropy:.2f})")
        return True
    
    def route(self, tracer_type: str, target_bloom_id: str) -> Optional[RouteResult]:
        """
        Route a tracer to a specific bloom target
        
        Args:
            tracer_type: Type of tracer ('owl', 'crow', 'spider', 'whale')
            target_bloom_id: ID of the target bloom
            
        Returns:
            RouteResult if successful, None if routing failed
        """
        start_time = time.time()
        
        # Validate inputs
        try:
            tracer_enum = TracerType(tracer_type.lower())
        except ValueError:
            print(f"[TracerRouter] ❌ Invalid tracer type: {tracer_type}")
            return None
        
        if target_bloom_id not in self.bloom_targets:
            print(f"[TracerRouter] ❌ Bloom target not found: {target_bloom_id}")
            return None
        
        # Check cache first
        cache_key = f"{tracer_type}:{target_bloom_id}"
        cached_result = self._get_cached_route(cache_key)
        if cached_result:
            self.routing_stats['cache_hits'] += 1
            return cached_result
        
        # Get target and capabilities
        target = self.bloom_targets[target_bloom_id]
        capabilities = self.tracer_capabilities[tracer_enum]
        
        # Calculate routing score
        route_score = self._calculate_route_score(tracer_enum, target)
        
        # Check if route is viable (minimum 30% success probability)
        if route_score < 0.3:
            print(f"[TracerRouter] ⚠️ Route score too low: {route_score:.2f} for {tracer_type} → {target_bloom_id}")
            return None
        
        # Generate optimal route path
        route_path = self._generate_route_path(tracer_enum, target)
        
        # Calculate estimates
        estimated_time = self._estimate_routing_time(capabilities, target, len(route_path))
        resource_cost = self._calculate_resource_cost(capabilities, target)
        success_probability = min(route_score * 1.2, 1.0)
        routing_reason = self._generate_routing_reason(tracer_enum, target, route_score)
        
        # Create route result
        result = RouteResult(
            tracer_type=tracer_type,
            target_bloom_id=target_bloom_id,
            route_path=route_path,
            route_score=route_score,
            estimated_time=estimated_time,
            resource_cost=resource_cost,
            success_probability=success_probability,
            routing_reason=routing_reason
        )
        
        # Cache and log the route
        self._cache_route(cache_key, result)
        self.log_route(tracer_type, target_bloom_id)
        
        # Update statistics
        routing_time = time.time() - start_time
        self._update_routing_stats(True, routing_time, tracer_type)
        
        # Store active route
        self.active_routes[f"{tracer_type}:{target_bloom_id}"] = result
        
        print(f"[TracerRouter] {result}")
        
        return result
    
    def get_available_routes(self, tracer_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get available route options for a tracer type
        
        Args:
            tracer_type: Type of tracer
            limit: Maximum number of routes to return
            
        Returns:
            List of route options with scores and reasons
        """
        try:
            tracer_enum = TracerType(tracer_type.lower())
        except ValueError:
            return []
        
        capabilities = self.tracer_capabilities[tracer_enum]
        route_options = []
        
        for bloom_id, target in self.bloom_targets.items():
            route_score = self._calculate_route_score(tracer_enum, target)
            
            # Only include viable routes (>30% success probability)
            if route_score >= 0.3:
                routing_reason = self._generate_routing_reason(tracer_enum, target, route_score)
                
                route_options.append({
                    'bloom_id': bloom_id,
                    'route_score': route_score,
                    'routing_reason': routing_reason,
                    'estimated_time': self._estimate_routing_time(capabilities, target, 4),
                    'success_probability': min(route_score * 1.2, 1.0),
                    'target_depth': target.depth,
                    'target_entropy': target.entropy
                })
        
        # Sort by route score (best first)
        route_options.sort(key=lambda x: x['route_score'], reverse=True)
        
        print(f"[TracerRouter] 📋 Found {len(route_options)} available routes for {tracer_type}")
        
        return route_options[:limit]
    
    def log_route(self, tracer_type: str, bloom_id: str) -> None:
        """
        Log a route for tracking and analytics
        
        Args:
            tracer_type: Type of tracer
            bloom_id: Target bloom ID
        """
        tracer_emoji = {'owl': '🦉', 'crow': '🐦‍⬛', 'spider': '🕷️', 'whale': '🐋'}
        emoji = tracer_emoji.get(tracer_type, '🔍')
        
        print(f"[TracerRouter] 📝 Logged route: {emoji}{tracer_type.title()} → {bloom_id}")
        
        # Add to route history if we have the full result
        route_key = f"{tracer_type}:{bloom_id}"
        if route_key in self.active_routes:
            self.route_history.append(self.active_routes[route_key])
    
    def _calculate_route_score(self, tracer_type: TracerType, target: BloomTarget) -> float:
        """Calculate routing score based on tracer capabilities and target properties"""
        capabilities = self.tracer_capabilities[tracer_type]
        
        # Depth score
        min_depth, max_depth = capabilities.preferred_depth_range
        if min_depth <= target.depth <= max_depth:
            depth_score = 1.0
        else:
            # Penalty for being outside preferred range
            distance = min(abs(target.depth - min_depth), abs(target.depth - max_depth))
            depth_score = max(0.0, 1.0 - (distance * 0.2))
        
        # Entropy score
        min_entropy, max_entropy = capabilities.entropy_affinity
        if min_entropy <= target.entropy <= max_entropy:
            entropy_score = 1.0
        else:
            # Penalty for entropy mismatch
            if target.entropy < min_entropy:
                entropy_score = target.entropy / min_entropy
            else:
                entropy_score = max_entropy / target.entropy
            entropy_score = max(0.0, entropy_score)
        
        # SCUP score (focus areas)
        scup_score = 0.0
        if target.scup_values:
            focus_values = [target.scup_values.get(component, 0.5) 
                          for component in capabilities.scup_focus]
            scup_score = sum(focus_values) / len(focus_values) if focus_values else 0.5
        
        # Specialization bonus based on tracer type
        specialization_bonus = 0.0
        
        if tracer_type == TracerType.OWL:
            # Owl bonus for reblooming structures and moderate entropy
            if target.rebloom_status in ['reblooming', 'evolving']:
                specialization_bonus += 0.2
            if 0.4 <= target.entropy <= 0.7:
                specialization_bonus += 0.1
                
        elif tracer_type == TracerType.CROW:
            # Crow bonus for weakness detection
            utility = target.scup_values.get('utility', 0.5)
            pressure = target.scup_values.get('pressure', 0.5)
            if utility < 0.3 and pressure > 0.8:
                specialization_bonus += 0.3
            elif target.rebloom_status == 'fragmenting':
                specialization_bonus += 0.2
                
        elif tracer_type == TracerType.SPIDER:
            # Spider bonus for token bridging opportunities
            if target.token_density > 0.6:
                specialization_bonus += 0.25
            if target.complexity > 0.5:
                specialization_bonus += 0.1
                
        elif tracer_type == TracerType.WHALE:
            # Whale bonus for high-density processing
            if target.entropy > 0.6 and target.complexity > 0.7:
                specialization_bonus += 0.4
            if target.token_density > 0.8:
                specialization_bonus += 0.1
        
        # Combine scores with weights
        final_score = (
            depth_score * 0.3 +
            entropy_score * 0.3 +
            scup_score * 0.2 +
            specialization_bonus * 0.2
        )
        
        return min(1.0, final_score)
    
    def _generate_route_path(self, tracer_type: TracerType, target: BloomTarget) -> List[str]:
        """Generate optimal cognitive pathway for the route"""
        
        # Select starting pathway based on tracer type
        if tracer_type == TracerType.OWL:
            start_pathway = 'analysis_core'
        elif tracer_type == TracerType.CROW:
            start_pathway = 'attention_nexus'
        elif tracer_type == TracerType.SPIDER:
            start_pathway = 'synthesis_chamber'
        elif tracer_type == TracerType.WHALE:
            start_pathway = 'memory_banks'
        else:
            start_pathway = 'analysis_core'
        
        # Build route path
        route_path = [start_pathway]
        
        # Add intermediate steps based on complexity
        if target.complexity > 0.7:
            # High complexity routes need more processing steps
            if start_pathway in self.cognitive_pathways:
                route_path.extend(self.cognitive_pathways[start_pathway])
        else:
            # Simpler routes can be more direct
            if start_pathway in self.cognitive_pathways:
                route_path.extend(self.cognitive_pathways[start_pathway][:2])
        
        # Add meta layer for deep analysis
        if target.depth > 5:
            route_path.append('meta_layer')
        
        # Final destination
        route_path.append(target.bloom_id)
        
        # Limit route length to prevent excessive hops
        if len(route_path) > 6:
            route_path = route_path[:3] + route_path[-2:]
        
        return route_path
    
    def _estimate_routing_time(self, capabilities: TracerCapabilities, 
                             target: BloomTarget, path_length: int) -> float:
        """Estimate routing time based on capabilities and target complexity"""
        base_time = path_length * 2.0  # 2 seconds per hop
        complexity_factor = 1.0 + target.complexity
        speed_factor = capabilities.analysis_speed
        
        estimated_time = (base_time * complexity_factor) / speed_factor
        
        # Add randomness to simulate real-world variance
        variance = random.uniform(0.8, 1.2)
        return estimated_time * variance
    
    def _calculate_resource_cost(self, capabilities: TracerCapabilities, 
                                target: BloomTarget) -> float:
        """Calculate computational resource cost"""
        base_cost = target.complexity * 0.5
        efficiency_factor = capabilities.resource_efficiency
        entropy_penalty = target.entropy * 0.3
        
        resource_cost = (base_cost + entropy_penalty) / efficiency_factor
        return min(1.0, resource_cost)
    
    def _generate_routing_reason(self, tracer_type: TracerType, target: BloomTarget, 
                                score: float) -> str:
        """Generate human-readable explanation for the routing decision"""
        
        if tracer_type == TracerType.OWL:
            if target.rebloom_status == 'reblooming':
                return f"Pattern analysis of reblooming structure (depth {target.depth}, entropy {target.entropy:.2f})"
            else:
                return f"Deep cognitive pattern recognition in {target.rebloom_status} bloom"
                
        elif tracer_type == TracerType.CROW:
            utility = target.scup_values.get('utility', 0.5)
            pressure = target.scup_values.get('pressure', 0.5)
            if utility < 0.4:
                return f"SCUP weakness detected - low utility ({utility:.2f}), high pressure ({pressure:.2f})"
            else:
                return f"Opportunistic analysis of cognitive vulnerabilities"
                
        elif tracer_type == TracerType.SPIDER:
            if target.token_density > 0.6:
                return f"Token bridging opportunity - high density ({target.token_density:.2f}), {target.complexity:.1f} complexity"
            else:
                return f"Information interconnection and synthesis pathway construction"
                
        elif tracer_type == TracerType.WHALE:
            if target.entropy > 0.6:
                return f"High-density processing required - entropy {target.entropy:.2f}, complexity {target.complexity:.2f}"
            else:
                return f"Massive information consolidation and pattern extraction"
        
        return f"Specialized cognitive analysis (score: {score:.2f})"
    
    def _get_cached_route(self, cache_key: str) -> Optional[RouteResult]:
        """Get cached route if still valid"""
        if cache_key in self.route_cache:
            route, timestamp = self.route_cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                return route
            else:
                # Remove expired cache entry
                del self.route_cache[cache_key]
        return None
    
    def _cache_route(self, cache_key: str, route: RouteResult):
        """Cache a route result"""
        self.route_cache[cache_key] = (route, datetime.now())
        
        # Clean up old cache entries periodically
        if len(self.route_cache) > 100:
            self._cleanup_cache()
    
    def _cleanup_cache(self):
        """Remove expired cache entries"""
        current_time = datetime.now()
        expired_keys = [
            key for key, (_, timestamp) in self.route_cache.items()
            if current_time - timestamp >= self.cache_ttl
        ]
        
        for key in expired_keys:
            del self.route_cache[key]
    
    def _invalidate_cache_for_bloom(self, bloom_id: str):
        """Invalidate cache entries related to a specific bloom"""
        keys_to_remove = [
            key for key in self.route_cache.keys()
            if bloom_id in key
        ]
        
        for key in keys_to_remove:
            del self.route_cache[key]
    
    def _update_routing_stats(self, success: bool, routing_time: float, tracer_type: str):
        """Update routing statistics"""
        self.routing_stats['total_routes'] += 1
        if success:
            self.routing_stats['successful_routes'] += 1
        
        self.routing_stats['tracer_usage'][tracer_type] += 1
        
        # Update average routing time
        current_avg = self.routing_stats['average_routing_time']
        total_routes = self.routing_stats['total_routes']
        self.routing_stats['average_routing_time'] = (
            (current_avg * (total_routes - 1) + routing_time) / total_routes
        )
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive routing statistics"""
        stats = self.routing_stats.copy()
        
        # Calculate success rate
        if stats['total_routes'] > 0:
            stats['success_rate'] = stats['successful_routes'] / stats['total_routes']
        else:
            stats['success_rate'] = 0.0
        
        # Add current state
        stats['active_routes'] = len(self.active_routes)
        stats['cached_routes'] = len(self.route_cache)
        stats['bloom_targets'] = len(self.bloom_targets)
        
        return stats
    
    def get_route_history(self, tracer_type: Optional[str] = None, 
                         limit: int = 20) -> List[Dict[str, Any]]:
        """Get route history with optional filtering"""
        history = self.route_history
        
        if tracer_type:
            history = [r for r in history if r.tracer_type == tracer_type]
        
        # Convert to dict format and limit results
        return [
            {
                'tracer_type': r.tracer_type,
                'target_bloom_id': r.target_bloom_id,
                'route_score': r.route_score,
                'estimated_time': r.estimated_time,
                'success_probability': r.success_probability,
                'timestamp': r.timestamp.isoformat(),
                'routing_reason': r.routing_reason
            }
            for r in history[-limit:]
        ]
    
    def clear_active_routes(self):
        """Clear all active routes"""
        self.active_routes.clear()
        print("[TracerRouter] 🧹 Cleared all active routes")
    
    def remove_bloom_target(self, bloom_id: str) -> bool:
        """Remove a bloom target from the routing system"""
        if bloom_id in self.bloom_targets:
            del self.bloom_targets[bloom_id]
            self._invalidate_cache_for_bloom(bloom_id)
            print(f"[TracerRouter] 🗑️ Removed bloom target: {bloom_id}")
            return True
        return False


# Example usage and testing
if __name__ == "__main__":
    print("🕸️ DAWN Tracer Router System Test")
    print("=" * 50)
    
    # Create router
    router = TracerRouter()
    
    # Add some bloom targets
    router.add_bloom_target('bloom_001', depth=5, entropy=0.7, complexity=0.8,
                           scup_values={'schema': 0.6, 'coherence': 0.9, 'utility': 0.7, 'pressure': 0.4})
    
    router.add_bloom_target('bloom_002', depth=2, entropy=0.9, complexity=0.3,
                           scup_values={'schema': 0.3, 'coherence': 0.4, 'utility': 0.2, 'pressure': 0.9})
    
    router.add_bloom_target('bloom_003', depth=7, entropy=0.5, complexity=0.9,
                           scup_values={'schema': 0.8, 'coherence': 0.8, 'utility': 0.6, 'pressure': 0.5},
                           token_density=0.8, rebloom_status='reblooming')
    
    router.add_bloom_target('bloom_004', depth=6, entropy=0.85, complexity=0.95,
                           scup_values={'schema': 0.9, 'coherence': 0.7, 'utility': 0.8, 'pressure': 0.7},
                           token_density=0.9, rebloom_status='stable')
    
    print("\n🎯 Testing Specialized Tracer Routing:")
    print("-" * 40)
    
    # Test each tracer type
    tracers = ['owl', 'crow', 'spider', 'whale']
    targets = ['bloom_001', 'bloom_002', 'bloom_003', 'bloom_004']
    
    for tracer in tracers:
        print(f"\n{tracer.upper()} Tracer Routes:")
        
        # Get available routes
        available = router.get_available_routes(tracer, limit=3)
        print(f"  📋 Top {len(available)} routes available")
        
        # Route to best target
        if available:
            best_target = available[0]['bloom_id']
            result = router.route(tracer, best_target)
            
            if result:
                print(f"  ✅ Successfully routed to {best_target}")
                print(f"     Reason: {result.routing_reason}")
            else:
                print(f"  ❌ Failed to route to {best_target}")
    
    print(f"\n📊 Routing Statistics:")
    stats = router.get_routing_statistics()
    for key, value in stats.items():
        if key != 'tracer_usage':
            print(f"  {key}: {value}")
    
    print(f"\n🔍 Tracer Usage:")
    for tracer, count in stats['tracer_usage'].items():
        print(f"  {tracer}: {count}")
    
    print(f"\n📝 Recent Route History:")
    history = router.get_route_history(limit=5)
    for route in history:
        print(f"  {route['tracer_type']} → {route['target_bloom_id']} (score: {route['route_score']:.2f})")
    
    print(f"\n🕸️ Tracer Router test complete!") 