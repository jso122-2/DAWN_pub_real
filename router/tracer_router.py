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
    thermal_tolerance: Tuple[float, float]    # Heat tolerance range
    specialization: str                       # Primary function
    efficiency_factors: Dict[str, float]      # Performance modifiers
    
    def calculate_compatibility(self, bloom: Dict[str, Any]) -> float:
        """Calculate how well this tracer matches a bloom's characteristics"""
        score = 0.0
        
        # Depth compatibility
        bloom_depth = bloom.get('depth', 0)
        depth_min, depth_max = self.preferred_depth_range
        if depth_min <= bloom_depth <= depth_max:
            score += 0.3
        else:
            # Penalty for being outside preferred range
            penalty = min(abs(bloom_depth - depth_min), abs(bloom_depth - depth_max)) * 0.05
            score += max(0, 0.3 - penalty)
        
        # Entropy compatibility
        bloom_entropy = bloom.get('entropy', 0.5)
        entropy_min, entropy_max = self.entropy_affinity
        if entropy_min <= bloom_entropy <= entropy_max:
            score += 0.3
        else:
            penalty = min(abs(bloom_entropy - entropy_min), abs(bloom_entropy - entropy_max)) * 0.5
            score += max(0, 0.3 - penalty)
        
        # Thermal compatibility
        bloom_heat = bloom.get('heat', 0.5)
        heat_min, heat_max = self.thermal_tolerance
        if heat_min <= bloom_heat <= heat_max:
            score += 0.2
        else:
            penalty = min(abs(bloom_heat - heat_min), abs(bloom_heat - heat_max)) * 0.4
            score += max(0, 0.2 - penalty)
        
        # Specialization bonus
        bloom_type = bloom.get('type', 'unknown')
        if bloom_type in self.efficiency_factors:
            score += self.efficiency_factors[bloom_type] * 0.2
        
        return min(1.0, max(0.0, score))


@dataclass
class BloomTarget:
    """Represents a bloom that needs tracer analysis"""
    bloom_id: str
    depth: int
    entropy: float
    heat: float
    bloom_type: str
    priority: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    assigned_tracers: List[str] = field(default_factory=list)
    analysis_history: List[Dict] = field(default_factory=list)
    
    def add_analysis_result(self, tracer_type: TracerType, result: Dict[str, Any]):
        """Add an analysis result to this bloom's history"""
        analysis_entry = {
            'timestamp': datetime.now().isoformat(),
            'tracer_type': tracer_type.value,
            'result': result
        }
        self.analysis_history.append(analysis_entry)
        
        # Keep history manageable
        if len(self.analysis_history) > 50:
            self.analysis_history = self.analysis_history[-25:]


@dataclass
class TracerInstance:
    """Represents an active tracer instance"""
    tracer_id: str
    tracer_type: TracerType
    capabilities: TracerCapabilities
    current_assignment: Optional[str] = None
    workload: int = 0
    efficiency: float = 1.0
    last_assignment_time: Optional[datetime] = None
    analysis_count: int = 0
    
    def is_available(self) -> bool:
        """Check if this tracer is available for new assignments"""
        return self.current_assignment is None and self.workload < 5
    
    def assign_to_bloom(self, bloom_id: str):
        """Assign this tracer to analyze a specific bloom"""
        self.current_assignment = bloom_id
        self.workload += 1
        self.last_assignment_time = datetime.now()
        self.analysis_count += 1
    
    def complete_assignment(self):
        """Mark the current assignment as complete"""
        self.current_assignment = None
        self.workload = max(0, self.workload - 1)


class TracerRouter:
    """Advanced routing system for DAWN cognitive tracers"""
    
    def __init__(self):
        """Initialize the tracer router with default configurations"""
        self.tracer_configurations = self._initialize_tracer_configs()
        self.active_tracers: Dict[str, TracerInstance] = {}
        self.bloom_queue: List[BloomTarget] = []
        self.routing_history: List[Dict] = []
        self.performance_metrics = {
            'total_assignments': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'avg_analysis_time': 0.0
        }
        
    def _initialize_tracer_configs(self) -> Dict[TracerType, TracerCapabilities]:
        """Initialize the capabilities for each tracer type"""
        return {
            TracerType.OWL: TracerCapabilities(
                preferred_depth_range=(5, 15),
                entropy_affinity=(0.3, 0.7),
                thermal_tolerance=(0.2, 0.8),
                specialization="pattern_analysis",
                efficiency_factors={
                    'cognitive': 1.2,
                    'memory': 1.1,
                    'symbolic': 1.3,
                    'abstract': 1.0
                }
            ),
            TracerType.CROW: TracerCapabilities(
                preferred_depth_range=(2, 8),
                entropy_affinity=(0.5, 0.9),
                thermal_tolerance=(0.4, 1.0),
                specialization="weakness_detection",
                efficiency_factors={
                    'scup': 1.5,
                    'coherence': 1.2,
                    'stability': 1.1,
                    'error': 1.4
                }
            ),
            TracerType.SPIDER: TracerCapabilities(
                preferred_depth_range=(3, 12),
                entropy_affinity=(0.2, 0.6),
                thermal_tolerance=(0.1, 0.7),
                specialization="bridge_construction",
                efficiency_factors={
                    'connection': 1.4,
                    'network': 1.3,
                    'bridge': 1.5,
                    'link': 1.2
                }
            ),
            TracerType.WHALE: TracerCapabilities(
                preferred_depth_range=(8, 20),
                entropy_affinity=(0.6, 1.0),
                thermal_tolerance=(0.5, 1.0),
                specialization="high_density_processing",
                efficiency_factors={
                    'complex': 1.3,
                    'dense': 1.4,
                    'heavy': 1.2,
                    'bulk': 1.5
                }
            )
        }
    
    def create_tracer(self, tracer_type: TracerType, tracer_id: Optional[str] = None) -> str:
        """Create a new tracer instance of the specified type"""
        if tracer_id is None:
            tracer_id = f"{tracer_type.value}_{len(self.active_tracers):03d}"
        
        capabilities = self.tracer_configurations[tracer_type]
        tracer = TracerInstance(
            tracer_id=tracer_id,
            tracer_type=tracer_type,
            capabilities=capabilities
        )
        
        self.active_tracers[tracer_id] = tracer
        return tracer_id
    
    def add_bloom_target(self, bloom_id: str, depth: int, entropy: float, 
                        heat: float, bloom_type: str, priority: float = 0.5,
                        metadata: Optional[Dict] = None) -> BloomTarget:
        """Add a new bloom target to the analysis queue"""
        bloom = BloomTarget(
            bloom_id=bloom_id,
            depth=depth,
            entropy=entropy,
            heat=heat,
            bloom_type=bloom_type,
            priority=priority,
            metadata=metadata or {}
        )
        
        self.bloom_queue.append(bloom)
        # Sort queue by priority (higher priority first)
        self.bloom_queue.sort(key=lambda b: b.priority, reverse=True)
        
        return bloom
    
    def find_optimal_tracer(self, bloom: BloomTarget) -> Optional[TracerInstance]:
        """Find the most suitable available tracer for a bloom"""
        available_tracers = [t for t in self.active_tracers.values() if t.is_available()]
        
        if not available_tracers:
            return None
        
        # Calculate compatibility scores
        scored_tracers = []
        for tracer in available_tracers:
            bloom_dict = {
                'depth': bloom.depth,
                'entropy': bloom.entropy,
                'heat': bloom.heat,
                'type': bloom.bloom_type
            }
            compatibility = tracer.capabilities.calculate_compatibility(bloom_dict)
            # Factor in tracer efficiency
            total_score = compatibility * tracer.efficiency
            scored_tracers.append((total_score, tracer))
        
        # Return the best match
        scored_tracers.sort(key=lambda x: x[0], reverse=True)
        return scored_tracers[0][1] if scored_tracers else None
    
    def route_tracers(self) -> Dict[str, List[str]]:
        """Perform intelligent routing of available tracers to bloom targets"""
        routing_results = {
            'successful_assignments': [],
            'failed_assignments': [],
            'queue_remaining': []
        }
        
        assignments_made = 0
        
        # Process bloom queue
        remaining_blooms = []
        for bloom in self.bloom_queue:
            optimal_tracer = self.find_optimal_tracer(bloom)
            
            if optimal_tracer:
                # Make the assignment
                optimal_tracer.assign_to_bloom(bloom.bloom_id)
                bloom.assigned_tracers.append(optimal_tracer.tracer_id)
                
                # Record the routing decision
                routing_record = {
                    'timestamp': datetime.now().isoformat(),
                    'bloom_id': bloom.bloom_id,
                    'tracer_id': optimal_tracer.tracer_id,
                    'tracer_type': optimal_tracer.tracer_type.value,
                    'compatibility_score': optimal_tracer.capabilities.calculate_compatibility({
                        'depth': bloom.depth,
                        'entropy': bloom.entropy,
                        'heat': bloom.heat,
                        'type': bloom.bloom_type
                    })
                }
                self.routing_history.append(routing_record)
                
                routing_results['successful_assignments'].append(
                    f"{bloom.bloom_id} → {optimal_tracer.tracer_id}"
                )
                assignments_made += 1
                
                # Update performance metrics
                self.performance_metrics['total_assignments'] += 1
                
            else:
                # No available tracer found
                remaining_blooms.append(bloom)
                routing_results['failed_assignments'].append(bloom.bloom_id)
        
        # Update bloom queue with unassigned blooms
        self.bloom_queue = remaining_blooms
        routing_results['queue_remaining'] = [b.bloom_id for b in remaining_blooms]
        
        return routing_results
    
    def complete_analysis(self, tracer_id: str, bloom_id: str, 
                         analysis_result: Dict[str, Any]) -> bool:
        """Mark an analysis as complete and free up the tracer"""
        if tracer_id not in self.active_tracers:
            return False
        
        tracer = self.active_tracers[tracer_id]
        if tracer.current_assignment != bloom_id:
            return False
        
        # Find the bloom and add the analysis result
        for bloom in self.bloom_queue + [b for b in self.bloom_queue]:
            if bloom.bloom_id == bloom_id:
                bloom.add_analysis_result(tracer.tracer_type, analysis_result)
                break
        
        # Free up the tracer
        tracer.complete_assignment()
        
        # Update performance metrics
        if analysis_result.get('success', False):
            self.performance_metrics['successful_analyses'] += 1
        else:
            self.performance_metrics['failed_analyses'] += 1
        
        return True
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about routing performance"""
        total_tracers = len(self.active_tracers)
        available_tracers = len([t for t in self.active_tracers.values() if t.is_available()])
        
        # Tracer type distribution
        type_counts = {}
        for tracer in self.active_tracers.values():
            tracer_type = tracer.tracer_type.value
            type_counts[tracer_type] = type_counts.get(tracer_type, 0) + 1
        
        # Recent routing success rate
        recent_history = self.routing_history[-100:] if self.routing_history else []
        
        stats = {
            'total_tracers': total_tracers,
            'available_tracers': available_tracers,
            'utilization_rate': (total_tracers - available_tracers) / total_tracers if total_tracers > 0 else 0,
            'queue_size': len(self.bloom_queue),
            'tracer_type_distribution': type_counts,
            'recent_routing_decisions': len(recent_history),
            'performance_metrics': self.performance_metrics.copy()
        }
        
        if self.performance_metrics['total_assignments'] > 0:
            success_rate = (self.performance_metrics['successful_analyses'] / 
                          self.performance_metrics['total_assignments'])
            stats['success_rate'] = success_rate
        
        return stats
    
    def optimize_tracer_fleet(self):
        """Analyze performance and suggest tracer fleet optimizations"""
        stats = self.get_routing_statistics()
        suggestions = []
        
        # Check utilization
        if stats['utilization_rate'] > 0.9:
            suggestions.append("High utilization detected - consider adding more tracers")
        elif stats['utilization_rate'] < 0.3:
            suggestions.append("Low utilization detected - consider reducing tracer count")
        
        # Check queue buildup
        if stats['queue_size'] > 20:
            suggestions.append("Large queue detected - increase tracer capacity or optimize routing")
        
        # Check type balance
        type_dist = stats['tracer_type_distribution']
        if type_dist:
            most_common = max(type_dist, key=type_dist.get)
            least_common = min(type_dist, key=type_dist.get)
            
            if type_dist[most_common] > type_dist[least_common] * 3:
                suggestions.append(f"Imbalanced fleet - too many {most_common}, too few {least_common}")
        
        return suggestions


# Example usage and testing
if __name__ == "__main__":
    print("🧠 DAWN Tracer Router - Cognitive Assignment System")
    print("=" * 60)
    
    # Create router
    router = TracerRouter()
    
    # Create a diverse fleet of tracers
    print("\n🚀 Creating tracer fleet...")
    tracer_fleet = [
        (TracerType.OWL, 3),
        (TracerType.CROW, 2),
        (TracerType.SPIDER, 2),
        (TracerType.WHALE, 1)
    ]
    
    for tracer_type, count in tracer_fleet:
        for i in range(count):
            tracer_id = router.create_tracer(tracer_type)
            print(f"  Created {tracer_type.value} tracer: {tracer_id}")
    
    # Add various bloom targets
    print("\n🎯 Adding bloom targets...")
    bloom_scenarios = [
        ("cognitive_bloom_001", 7, 0.4, 0.3, "cognitive", 0.8),
        ("memory_bloom_002", 12, 0.6, 0.7, "memory", 0.6),
        ("scup_weakness_003", 4, 0.8, 0.9, "scup", 0.9),
        ("bridge_bloom_004", 6, 0.3, 0.4, "connection", 0.7),
        ("dense_bloom_005", 15, 0.9, 0.8, "complex", 0.5)
    ]
    
    for bloom_id, depth, entropy, heat, bloom_type, priority in bloom_scenarios:
        router.add_bloom_target(bloom_id, depth, entropy, heat, bloom_type, priority)
        print(f"  Added bloom: {bloom_id} (type: {bloom_type}, priority: {priority})")
    
    # Perform routing
    print("\n🎯 Performing intelligent routing...")
    routing_results = router.route_tracers()
    
    print("  Successful assignments:")
    for assignment in routing_results['successful_assignments']:
        print(f"    {assignment}")
    
    if routing_results['failed_assignments']:
        print("  Failed assignments:")
        for failed in routing_results['failed_assignments']:
            print(f"    {failed} (no suitable tracer available)")
    
    # Show statistics
    print("\n📊 Routing Statistics:")
    stats = router.get_routing_statistics()
    print(f"  Total tracers: {stats['total_tracers']}")
    print(f"  Available tracers: {stats['available_tracers']}")
    print(f"  Utilization rate: {stats['utilization_rate']:.1%}")
    print(f"  Queue size: {stats['queue_size']}")
    print(f"  Tracer distribution: {stats['tracer_type_distribution']}")
    
    # Get optimization suggestions
    print("\n💡 Fleet Optimization Suggestions:")
    suggestions = router.optimize_tracer_fleet()
    if suggestions:
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    else:
        print("  • Fleet appears well-optimized")
    
    print("\n🎉 Tracer routing demonstration complete!") 