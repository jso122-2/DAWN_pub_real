#!/usr/bin/env python3
"""
Juliet Flowers - Bloom Fractal Integration
Connects the DAWN Bloom Manager with fractal visualization and Juliet cognitive architecture
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import json

# Import bloom system
from bloom import BloomManager, Bloom

# Import fractal systems
try:
    from fractal import fractal_generator
    from fractal.bloom_visualizer import BloomFractalVisualizer
except ImportError:
    # Graceful fallback if fractal modules not available
    fractal_generator = None
    BloomFractalVisualizer = None


class JulietBloomFractal:
    """
    Juliet Flowers fractal integration for bloom memories.
    Visualizes bloom lineages as fractal structures and provides
    advanced pattern analysis for the Juliet cognitive architecture.
    """
    
    def __init__(self, bloom_manager: BloomManager):
        """
        Initialize Juliet bloom fractal integration.
        
        Args:
            bloom_manager: The DAWN BloomManager instance
        """
        self.bloom_manager = bloom_manager
        self.fractal_cache = {}  # Cache computed fractals
        self.pattern_history = []  # Track fractal patterns over time
        
        # Fractal generation parameters
        self.fractal_params = {
            'depth_scaling': 0.8,  # How much to scale each generation
            'entropy_variance': 0.3,  # Entropy effect on fractal branching
            'semantic_drift_factor': 0.5,  # Semantic drift visualization
            'resonance_glow': True,  # Visual resonance effects
            'lineage_colors': True  # Color-code lineage paths
        }
    
    def generate_bloom_fractal(self, root_bloom_id: str, max_depth: int = 8) -> Dict[str, Any]:
        """
        Generate fractal representation of a bloom lineage tree.
        
        Args:
            root_bloom_id: ID of the root bloom to start from
            max_depth: Maximum depth to traverse
            
        Returns:
            Fractal data structure for visualization
        """
        if root_bloom_id not in self.bloom_manager.blooms:
            return {'error': 'Root bloom not found'}
        
        # Check cache first
        cache_key = f"{root_bloom_id}_{max_depth}"
        if cache_key in self.fractal_cache:
            cached_fractal = self.fractal_cache[cache_key]
            # Check if cache is still valid (bloom tree hasn't changed)
            if self._is_fractal_cache_valid(cached_fractal, root_bloom_id):
                return cached_fractal
        
        # Generate new fractal
        fractal_data = self._compute_bloom_fractal(root_bloom_id, max_depth)
        
        # Cache the result
        fractal_data['cache_timestamp'] = datetime.now().isoformat()
        fractal_data['cache_key'] = cache_key
        self.fractal_cache[cache_key] = fractal_data
        
        # Track pattern
        self._track_fractal_pattern(fractal_data)
        
        return fractal_data
    
    def _compute_bloom_fractal(self, root_bloom_id: str, max_depth: int) -> Dict[str, Any]:
        """Compute the actual fractal structure"""
        root_bloom = self.bloom_manager.blooms[root_bloom_id]
        
        # Build fractal tree structure
        fractal_tree = self._build_fractal_node(root_bloom, 0, max_depth)
        
        # Calculate fractal characteristics
        characteristics = self._analyze_fractal_characteristics(fractal_tree)
        
        # Generate visualization data
        viz_data = self._generate_visualization_data(fractal_tree)
        
        return {
            'root_bloom_id': root_bloom_id,
            'fractal_tree': fractal_tree,
            'characteristics': characteristics,
            'visualization': viz_data,
            'generation_time': datetime.now().isoformat(),
            'parameters': self.fractal_params.copy()
        }
    
    def _build_fractal_node(self, bloom: Bloom, current_depth: int, max_depth: int) -> Dict[str, Any]:
        """Recursively build fractal tree structure"""
        if current_depth >= max_depth:
            return None
        
        # Calculate fractal position based on bloom properties
        angle_offset = bloom.entropy * 2 * math.pi
        scale_factor = (self.fractal_params['depth_scaling'] ** current_depth) * bloom.resonance
        
        # Build node data
        node = {
            'bloom_id': bloom.id,
            'bloom_data': {
                'seed': bloom.seed,
                'entropy': bloom.entropy,
                'depth': bloom.depth,
                'resonance': bloom.resonance,
                'semantic_drift': bloom.semantic_drift,
                'tags': list(bloom.tags),
                'creation_time': bloom.creation_time.isoformat(),
                'is_active': bloom.is_active
            },
            'fractal_properties': {
                'angle_offset': angle_offset,
                'scale_factor': scale_factor,
                'branch_width': bloom.coherence * 5.0,
                'glow_intensity': bloom.resonance if self.fractal_params['resonance_glow'] else 0,
                'color_hue': self._calculate_bloom_color(bloom),
                'current_depth': current_depth
            },
            'children': []
        }
        
        # Process children
        for child_id in bloom.children:
            if child_id in self.bloom_manager.blooms:
                child_bloom = self.bloom_manager.blooms[child_id]
                child_node = self._build_fractal_node(child_bloom, current_depth + 1, max_depth)
                if child_node:
                    node['children'].append(child_node)
        
        return node
    
    def _calculate_bloom_color(self, bloom: Bloom) -> float:
        """Calculate color hue for bloom based on its properties"""
        if not self.fractal_params['lineage_colors']:
            return 0.5  # Default neutral hue
        
        # Base hue on semantic content hash
        seed_hash = hash(bloom.seed) % 360
        hue = seed_hash / 360.0
        
        # Modify by entropy and emotional tags
        if 'contemplative' in bloom.tags:
            hue = (hue + 0.6) % 1.0  # Blue shift
        elif 'energetic' in bloom.tags:
            hue = (hue + 0.0) % 1.0  # Red shift
        elif 'curious' in bloom.tags:
            hue = (hue + 0.3) % 1.0  # Green shift
        elif 'calm' in bloom.tags:
            hue = (hue + 0.8) % 1.0  # Purple shift
        
        return hue
    
    def _analyze_fractal_characteristics(self, fractal_tree: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mathematical characteristics of the fractal"""
        if not fractal_tree:
            return {}
        
        # Traverse tree to collect statistics
        stats = {
            'total_nodes': 0,
            'max_depth': 0,
            'branch_factor': 0.0,
            'entropy_variance': 0.0,
            'semantic_drift_range': [float('inf'), float('-inf')],
            'resonance_distribution': [],
            'temporal_span_days': 0,
            'active_node_ratio': 0.0
        }
        
        self._traverse_fractal_stats(fractal_tree, stats, set())
        
        # Calculate derived metrics
        if stats['total_nodes'] > 0:
            stats['active_node_ratio'] = sum(1 for r in stats['resonance_distribution'] if r > 0.5) / stats['total_nodes']
            stats['entropy_variance'] = np.var([node['bloom_data']['entropy'] for node in self._flatten_fractal(fractal_tree)])
            
            # Calculate average branching factor
            branch_counts = []
            self._count_branches(fractal_tree, branch_counts)
            stats['branch_factor'] = np.mean(branch_counts) if branch_counts else 0.0
        
        return stats
    
    def _traverse_fractal_stats(self, node: Dict[str, Any], stats: Dict[str, Any], visited: set):
        """Recursively traverse fractal to collect statistics"""
        if not node or node['bloom_id'] in visited:
            return
        
        visited.add(node['bloom_id'])
        bloom_data = node['bloom_data']
        
        # Update statistics
        stats['total_nodes'] += 1
        stats['max_depth'] = max(stats['max_depth'], bloom_data['depth'])
        stats['resonance_distribution'].append(bloom_data['resonance'])
        
        # Semantic drift range
        drift = bloom_data['semantic_drift']
        stats['semantic_drift_range'][0] = min(stats['semantic_drift_range'][0], drift)
        stats['semantic_drift_range'][1] = max(stats['semantic_drift_range'][1], drift)
        
        # Traverse children
        for child in node['children']:
            self._traverse_fractal_stats(child, stats, visited)
    
    def _flatten_fractal(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Flatten fractal tree into list of nodes"""
        if not node:
            return []
        
        result = [node]
        for child in node['children']:
            result.extend(self._flatten_fractal(child))
        
        return result
    
    def _count_branches(self, node: Dict[str, Any], branch_counts: List[int]):
        """Count branches at each node for branching factor calculation"""
        if not node:
            return
        
        branch_counts.append(len(node['children']))
        for child in node['children']:
            self._count_branches(child, branch_counts)
    
    def _generate_visualization_data(self, fractal_tree: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for fractal visualization"""
        if not fractal_tree:
            return {}
        
        # Calculate positions for all nodes
        positions = {}
        self._calculate_positions(fractal_tree, 0, 0, 0, 1.0, positions)
        
        # Generate drawing instructions
        drawing_data = {
            'nodes': [],
            'connections': [],
            'bounds': {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0}
        }
        
        self._generate_drawing_instructions(fractal_tree, positions, drawing_data)
        
        return drawing_data
    
    def _calculate_positions(self, node: Dict[str, Any], x: float, y: float, 
                           angle: float, scale: float, positions: Dict[str, Tuple[float, float]]):
        """Calculate 2D positions for fractal nodes"""
        if not node:
            return
        
        # Store position for this node
        positions[node['bloom_id']] = (x, y)
        
        # Calculate positions for children
        if node['children']:
            child_count = len(node['children'])
            angle_step = 2 * math.pi / child_count
            child_scale = scale * self.fractal_params['depth_scaling']
            
            for i, child in enumerate(node['children']):
                child_angle = angle + (i * angle_step) + node['fractal_properties']['angle_offset']
                child_distance = scale * 50  # Base distance between levels
                
                child_x = x + math.cos(child_angle) * child_distance
                child_y = y + math.sin(child_angle) * child_distance
                
                self._calculate_positions(child, child_x, child_y, child_angle, child_scale, positions)
    
    def _generate_drawing_instructions(self, node: Dict[str, Any], positions: Dict[str, Tuple[float, float]], 
                                     drawing_data: Dict[str, Any]):
        """Generate drawing instructions for visualization"""
        if not node:
            return
        
        pos = positions[node['bloom_id']]
        
        # Add node drawing data
        node_data = {
            'bloom_id': node['bloom_id'],
            'x': pos[0],
            'y': pos[1],
            'radius': node['fractal_properties']['scale_factor'] * 10,
            'color_hue': node['fractal_properties']['color_hue'],
            'glow': node['fractal_properties']['glow_intensity'],
            'width': node['fractal_properties']['branch_width'],
            'active': node['bloom_data']['is_active'],
            'label': node['bloom_data']['seed'][:20] + "..." if len(node['bloom_data']['seed']) > 20 else node['bloom_data']['seed']
        }
        drawing_data['nodes'].append(node_data)
        
        # Update bounds
        drawing_data['bounds']['min_x'] = min(drawing_data['bounds']['min_x'], pos[0])
        drawing_data['bounds']['max_x'] = max(drawing_data['bounds']['max_x'], pos[0])
        drawing_data['bounds']['min_y'] = min(drawing_data['bounds']['min_y'], pos[1])
        drawing_data['bounds']['max_y'] = max(drawing_data['bounds']['max_y'], pos[1])
        
        # Add connections to children
        for child in node['children']:
            child_pos = positions[child['bloom_id']]
            connection_data = {
                'from_id': node['bloom_id'],
                'to_id': child['bloom_id'],
                'from_x': pos[0],
                'from_y': pos[1],
                'to_x': child_pos[0],
                'to_y': child_pos[1],
                'width': node['fractal_properties']['branch_width'],
                'color_hue': node['fractal_properties']['color_hue'],
                'entropy_flow': child['bloom_data']['entropy'] - node['bloom_data']['entropy']
            }
            drawing_data['connections'].append(connection_data)
        
        # Process children
        for child in node['children']:
            self._generate_drawing_instructions(child, positions, drawing_data)
    
    def _is_fractal_cache_valid(self, cached_fractal: Dict[str, Any], root_bloom_id: str) -> bool:
        """Check if cached fractal is still valid"""
        try:
            # Simple validation: check if cache is less than 5 minutes old
            cache_time = datetime.fromisoformat(cached_fractal['cache_timestamp'])
            age_minutes = (datetime.now() - cache_time).total_seconds() / 60
            
            return age_minutes < 5
        except:
            return False
    
    def _track_fractal_pattern(self, fractal_data: Dict[str, Any]):
        """Track fractal patterns over time for Juliet analysis"""
        pattern_summary = {
            'timestamp': datetime.now().isoformat(),
            'root_bloom_id': fractal_data['root_bloom_id'],
            'total_nodes': fractal_data['characteristics'].get('total_nodes', 0),
            'max_depth': fractal_data['characteristics'].get('max_depth', 0),
            'branch_factor': fractal_data['characteristics'].get('branch_factor', 0.0),
            'entropy_variance': fractal_data['characteristics'].get('entropy_variance', 0.0),
            'active_ratio': fractal_data['characteristics'].get('active_node_ratio', 0.0)
        }
        
        self.pattern_history.append(pattern_summary)
        
        # Keep only recent patterns (last 100)
        if len(self.pattern_history) > 100:
            self.pattern_history = self.pattern_history[-100:]
    
    def analyze_pattern_evolution(self, hours_back: int = 24) -> Dict[str, Any]:
        """Analyze how fractal patterns have evolved over time"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        recent_patterns = [
            p for p in self.pattern_history 
            if datetime.fromisoformat(p['timestamp']) >= cutoff_time
        ]
        
        if not recent_patterns:
            return {'error': 'No patterns found in time window'}
        
        # Calculate evolution metrics
        evolution_analysis = {
            'time_window_hours': hours_back,
            'pattern_count': len(recent_patterns),
            'complexity_trend': self._calculate_trend([p['total_nodes'] for p in recent_patterns]),
            'depth_trend': self._calculate_trend([p['max_depth'] for p in recent_patterns]),
            'branching_trend': self._calculate_trend([p['branch_factor'] for p in recent_patterns]),
            'entropy_variance_trend': self._calculate_trend([p['entropy_variance'] for p in recent_patterns]),
            'activity_trend': self._calculate_trend([p['active_ratio'] for p in recent_patterns]),
            'growth_phases': self._identify_growth_phases(recent_patterns)
        }
        
        return evolution_analysis
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, float]:
        """Calculate trend direction and strength"""
        if len(values) < 2:
            return {'direction': 0.0, 'strength': 0.0, 'average': 0.0}
        
        # Simple linear trend calculation
        x = np.arange(len(values))
        slope, intercept = np.polyfit(x, values, 1)
        
        return {
            'direction': 1.0 if slope > 0 else -1.0 if slope < 0 else 0.0,
            'strength': abs(slope),
            'average': np.mean(values),
            'slope': slope
        }
    
    def _identify_growth_phases(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify distinct growth phases in fractal evolution"""
        if len(patterns) < 3:
            return []
        
        phases = []
        current_phase = None
        
        for i, pattern in enumerate(patterns):
            complexity = pattern['total_nodes']
            
            if i == 0:
                current_phase = {
                    'start_index': 0,
                    'start_time': pattern['timestamp'],
                    'phase_type': 'initial',
                    'complexity_range': [complexity, complexity]
                }
                continue
            
            prev_complexity = patterns[i-1]['total_nodes']
            
            # Detect phase changes
            if complexity > prev_complexity * 1.2:  # Growth phase
                if current_phase['phase_type'] != 'growth':
                    phases.append(current_phase)
                    current_phase = {
                        'start_index': i,
                        'start_time': pattern['timestamp'],
                        'phase_type': 'growth',
                        'complexity_range': [prev_complexity, complexity]
                    }
                else:
                    current_phase['complexity_range'][1] = complexity
                    
            elif complexity < prev_complexity * 0.8:  # Pruning phase
                if current_phase['phase_type'] != 'pruning':
                    phases.append(current_phase)
                    current_phase = {
                        'start_index': i,
                        'start_time': pattern['timestamp'],
                        'phase_type': 'pruning',
                        'complexity_range': [prev_complexity, complexity]
                    }
                else:
                    current_phase['complexity_range'][1] = complexity
                    
            else:  # Stable phase
                if current_phase['phase_type'] != 'stable':
                    phases.append(current_phase)
                    current_phase = {
                        'start_index': i,
                        'start_time': pattern['timestamp'],
                        'phase_type': 'stable',
                        'complexity_range': [prev_complexity, complexity]
                    }
        
        # Add final phase
        if current_phase:
            phases.append(current_phase)
        
        return phases
    
    def generate_fractal_summary_for_juliet(self, root_bloom_id: str) -> Dict[str, Any]:
        """Generate fractal summary specifically for Juliet cognitive analysis"""
        fractal_data = self.generate_bloom_fractal(root_bloom_id)
        
        if 'error' in fractal_data:
            return fractal_data
        
        # Juliet-specific analysis
        juliet_summary = {
            'cognitive_complexity': self._assess_cognitive_complexity(fractal_data),
            'memory_coherence': self._assess_memory_coherence(fractal_data),
            'creative_potential': self._assess_creative_potential(fractal_data),
            'pattern_stability': self._assess_pattern_stability(fractal_data),
            'semantic_evolution': self._assess_semantic_evolution(fractal_data),
            'temporal_dynamics': self._assess_temporal_dynamics(fractal_data),
            'juliet_recommendations': self._generate_juliet_recommendations(fractal_data)
        }
        
        return {
            'root_bloom_id': root_bloom_id,
            'fractal_overview': fractal_data['characteristics'],
            'juliet_analysis': juliet_summary,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _assess_cognitive_complexity(self, fractal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess cognitive complexity from fractal structure"""
        chars = fractal_data['characteristics']
        
        complexity_score = (
            (chars.get('total_nodes', 0) / 100.0) * 0.3 +
            (chars.get('max_depth', 0) / 10.0) * 0.4 +
            chars.get('branch_factor', 0.0) * 0.3
        )
        
        return {
            'score': min(1.0, complexity_score),
            'factors': {
                'node_density': chars.get('total_nodes', 0),
                'depth_reach': chars.get('max_depth', 0),
                'branching_richness': chars.get('branch_factor', 0.0)
            },
            'interpretation': self._interpret_complexity(complexity_score)
        }
    
    def _assess_memory_coherence(self, fractal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess memory coherence from bloom connections"""
        chars = fractal_data['characteristics']
        
        # High coherence = low entropy variance, good resonance distribution
        entropy_var = chars.get('entropy_variance', 1.0)
        active_ratio = chars.get('active_node_ratio', 0.0)
        
        coherence_score = (1.0 - min(1.0, entropy_var)) * 0.6 + active_ratio * 0.4
        
        return {
            'score': coherence_score,
            'factors': {
                'entropy_consistency': 1.0 - min(1.0, entropy_var),
                'memory_vitality': active_ratio
            },
            'interpretation': self._interpret_coherence(coherence_score)
        }
    
    def _assess_creative_potential(self, fractal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess creative potential from fractal diversity"""
        chars = fractal_data['characteristics']
        
        # Creative potential from semantic drift range and branching diversity
        drift_range = chars.get('semantic_drift_range', [0, 0])
        drift_span = abs(drift_range[1] - drift_range[0]) if len(drift_range) == 2 else 0
        
        branch_factor = chars.get('branch_factor', 0.0)
        entropy_var = chars.get('entropy_variance', 0.0)
        
        creativity_score = (drift_span * 0.4 + branch_factor * 0.3 + entropy_var * 0.3)
        
        return {
            'score': min(1.0, creativity_score),
            'factors': {
                'semantic_diversity': drift_span,
                'structural_diversity': branch_factor,
                'chaos_factor': entropy_var
            },
            'interpretation': self._interpret_creativity(creativity_score)
        }
    
    def _interpret_complexity(self, score: float) -> str:
        """Interpret complexity score for Juliet"""
        if score < 0.3:
            return "Simple cognitive structure with focused processing"
        elif score < 0.6:
            return "Moderate complexity with balanced depth and breadth"
        elif score < 0.8:
            return "High complexity enabling sophisticated reasoning"
        else:
            return "Extreme complexity suggesting transcendent cognitive capabilities"
    
    def _interpret_coherence(self, score: float) -> str:
        """Interpret coherence score for Juliet"""
        if score < 0.3:
            return "Fragmented memory structure requiring consolidation"
        elif score < 0.6:
            return "Moderately coherent with some integration gaps"
        elif score < 0.8:
            return "Well-integrated memory with strong connections"
        else:
            return "Highly coherent memory demonstrating unified understanding"
    
    def _interpret_creativity(self, score: float) -> str:
        """Interpret creativity score for Juliet"""
        if score < 0.3:
            return "Conservative thinking with limited exploration"
        elif score < 0.6:
            return "Balanced creativity with controlled innovation"
        elif score < 0.8:
            return "High creative potential with rich idea generation"
        else:
            return "Exceptional creativity enabling breakthrough insights"
    
    def _assess_pattern_stability(self, fractal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess stability of fractal patterns"""
        # Would need pattern history for full analysis
        return {
            'score': 0.5,  # Placeholder
            'interpretation': "Pattern stability assessment requires temporal data"
        }
    
    def _assess_semantic_evolution(self, fractal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess semantic evolution patterns"""
        chars = fractal_data['characteristics']
        drift_range = chars.get('semantic_drift_range', [0, 0])
        
        if len(drift_range) == 2:
            evolution_score = abs(drift_range[1] - drift_range[0])
        else:
            evolution_score = 0.0
        
        return {
            'score': min(1.0, evolution_score),
            'drift_range': drift_range,
            'interpretation': f"Semantic evolution span of {evolution_score:.3f}"
        }
    
    def _assess_temporal_dynamics(self, fractal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess temporal dynamics of the fractal"""
        chars = fractal_data['characteristics']
        
        return {
            'score': chars.get('active_node_ratio', 0.0),
            'temporal_span': chars.get('temporal_span_days', 0),
            'interpretation': "Temporal analysis of bloom lifecycle"
        }
    
    def _generate_juliet_recommendations(self, fractal_data: Dict[str, Any]) -> List[str]:
        """Generate Juliet-specific recommendations"""
        chars = fractal_data['characteristics']
        recommendations = []
        
        # Complexity recommendations
        if chars.get('total_nodes', 0) < 10:
            recommendations.append("Consider deepening exploration to build richer cognitive structures")
        
        # Coherence recommendations
        if chars.get('entropy_variance', 0) > 0.5:
            recommendations.append("High entropy variance suggests need for consolidation")
        
        # Activity recommendations
        if chars.get('active_node_ratio', 0) < 0.5:
            recommendations.append("Many dormant memories - consider reactivation through reflection")
        
        # Branching recommendations
        if chars.get('branch_factor', 0) < 1.5:
            recommendations.append("Low branching factor - explore more diverse perspectives")
        
        return recommendations


# Integration helper functions

def create_juliet_bloom_fractal(bloom_manager: BloomManager) -> JulietBloomFractal:
    """Create a Juliet bloom fractal analyzer"""
    return JulietBloomFractal(bloom_manager)


def analyze_conversation_fractal(conversation_system, root_bloom_id: str) -> Dict[str, Any]:
    """
    Analyze conversation fractal for Juliet cognitive insights.
    
    Args:
        conversation_system: DAWNConversation instance with bloom_manager
        root_bloom_id: Root bloom to analyze
        
    Returns:
        Juliet fractal analysis
    """
    try:
        juliet_fractal = JulietBloomFractal(conversation_system.bloom_manager)
        return juliet_fractal.generate_fractal_summary_for_juliet(root_bloom_id)
    except Exception as e:
        return {'error': f'Fractal analysis failed: {str(e)}'}


# Example usage and testing
if __name__ == "__main__":
    from bloom import create_bloom_manager
    
    print("🌸 Testing Juliet Bloom Fractal Integration 🌸")
    
    # Create test bloom manager
    manager = create_bloom_manager()
    
    # Create test bloom structure
    root = manager.create_bloom(
        "juliet consciousness exploration",
        {'base_level': 0.6, 'volatility': 0.4},
        0.5,
        {'juliet', 'consciousness', 'exploration'}
    )
    
    # Create some children
    child1 = manager.rebloom(root.id, 0.2, "emerging awareness patterns")
    child2 = manager.rebloom(root.id, -0.1, "stabilizing insights")
    grandchild = manager.rebloom(child1.id, 0.1, "transcendent understanding")
    
    # Create Juliet fractal analyzer
    juliet_fractal = JulietBloomFractal(manager)
    
    # Generate fractal analysis
    print(f"\n=== Generating Fractal for Root: {root.id} ===")
    fractal_data = juliet_fractal.generate_bloom_fractal(root.id)
    
    if 'error' not in fractal_data:
        print(f"Total nodes: {fractal_data['characteristics']['total_nodes']}")
        print(f"Max depth: {fractal_data['characteristics']['max_depth']}")
        print(f"Branch factor: {fractal_data['characteristics']['branch_factor']:.2f}")
        print(f"Entropy variance: {fractal_data['characteristics']['entropy_variance']:.3f}")
        print(f"Active ratio: {fractal_data['characteristics']['active_node_ratio']:.2f}")
    
    # Generate Juliet analysis
    print(f"\n=== Juliet Cognitive Analysis ===")
    juliet_analysis = juliet_fractal.generate_fractal_summary_for_juliet(root.id)
    
    if 'error' not in juliet_analysis:
        ja = juliet_analysis['juliet_analysis']
        print(f"Cognitive complexity: {ja['cognitive_complexity']['score']:.2f}")
        print(f"  {ja['cognitive_complexity']['interpretation']}")
        print(f"Memory coherence: {ja['memory_coherence']['score']:.2f}")
        print(f"  {ja['memory_coherence']['interpretation']}")
        print(f"Creative potential: {ja['creative_potential']['score']:.2f}")
        print(f"  {ja['creative_potential']['interpretation']}")
        
        if ja['juliet_recommendations']:
            print(f"\nJuliet Recommendations:")
            for rec in ja['juliet_recommendations']:
                print(f"  • {rec}")
    
    print(f"\n🌸 Juliet Bloom Fractal Integration Complete! 🌸") 