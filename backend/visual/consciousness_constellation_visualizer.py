#!/usr/bin/env python3
"""
DAWN Backend Consciousness Constellation Visualizer
Backend-compatible version for analytics and API integration.
4D SCUP trajectory visualization mapping DAWN's consciousness through multidimensional cognitive space.
"""

import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple
import logging
from collections import deque, defaultdict
import time
import math
import signal
import atexit
import sys

# Import GIF saver

    from ...gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver
import signal
import atexit

# Import GIF saver

    from ...gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

# Consciousness state archetypes
CONSCIOUSNESS_ARCHETYPES = {
    'dormant_equilibrium': {
        'scup_signature': (0.3, 0.4, 0.3, 0.2),
        'description': 'Minimal processing, resting state',
        'color': '#424242',
        'constellation_region': 'void',
        'stability': 0.9
    },
    'focused_processing': {
        'scup_signature': (0.7, 0.8, 0.9, 0.6),
        'description': 'Deep focused cognitive work',
        'color': '#1976d2', 
        'constellation_region': 'focus_star',
        'stability': 0.7
    },
    'creative_exploration': {
        'scup_signature': (0.4, 0.6, 0.5, 0.8),
        'description': 'Creative discovery and synthesis',
        'color': '#7b1fa2',
        'constellation_region': 'creative_nebula', 
        'stability': 0.3
    },
    'integrative_synthesis': {
        'scup_signature': (0.8, 0.9, 0.7, 0.5),
        'description': 'Deep understanding and integration',
        'color': '#388e3c',
        'constellation_region': 'wisdom_center',
        'stability': 0.8
    },
    'exploratory_search': {
        'scup_signature': (0.3, 0.5, 0.8, 0.7),
        'description': 'Active problem-solving and search',
        'color': '#f57c00',
        'constellation_region': 'search_spiral',
        'stability': 0.4
    },
    'transcendent_awareness': {
        'scup_signature': (0.9, 0.9, 0.8, 0.3),
        'description': 'Deep self-aware meta-cognition', 
        'color': '#c2185b',
        'constellation_region': 'transcendent_apex',
        'stability': 0.6
    },
    'chaotic_transition': {
        'scup_signature': (0.5, 0.3, 0.6, 0.9),
        'description': 'Unstable transitional processing',
        'color': '#d32f2f',
        'constellation_region': 'chaos_storm',
        'stability': 0.1
    }
}

# Temporal analysis scales
TEMPORAL_SCALES = {
    'immediate': {
        'window_size': 10,
        'description': 'Moment-to-moment consciousness fluctuations',
        'color': '#ff5252',
        'alpha': 0.8
    },
    'short_term': {
        'window_size': 50, 
        'description': 'Cognitive episode patterns',
        'color': '#ff9800',
        'alpha': 0.6
    },
    'medium_term': {
        'window_size': 200,
        'description': 'Consciousness phase cycles',
        'color': '#4caf50',
        'alpha': 0.4
    },
    'long_term': {
        'window_size': 500,
        'description': 'Consciousness evolution trends',
        'color': '#2196f3',
        'alpha': 0.2
    }
}

class ConsciousnessConstellationBackend:
    """Backend analytics for the Consciousness Constellation visualizer"""
    
    def __init__(self, max_trajectory_points=2000):
        self.max_trajectory_points = max_trajectory_points
        
        # Consciousness trajectory data
        self.consciousness_trajectory = deque(maxlen=max_trajectory_points)
        self.trajectory_segments = defaultdict(list)  # Organized by temporal scale
        
        # Consciousness analysis
        self.current_archetype = 'dormant_equilibrium'
        self.consciousness_metrics = {}
        self.phase_transitions = []
        self.attractor_regions = {}
        
        # 3D sphere projection parameters
        self.sphere_radius = 5.0
        self.sphere_center = (0, 0, 0)
        
        # Analytics tracking
        self.current_tick = 0
        self.analytics_history = deque(maxlen=100)
        self._active = True
        
        # Consciousness stars data (archetypal states)
        self.consciousness_stars = self._create_consciousness_stars()
        
        # Constellation connections
        self.constellation_connections = self._create_constellation_connections()
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("consciousness_constellation_visualizer")
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        logger.info("ConsciousnessConstellationBackend initialized")

    def _create_consciousness_stars(self) -> List[Dict[str, Any]]:
        """Create data representations of consciousness archetypes"""
        stars = []
        for archetype_name, archetype in CONSCIOUSNESS_ARCHETYPES.items():
            # Project 4D position to 3D
            pos_3d, pressure = self.project_4d_to_sphere(archetype['scup_signature'])
            
            stars.append({
                'name': archetype_name,
                'position': pos_3d,
                'pressure': pressure,
                'data': archetype,
                'scup_signature': archetype['scup_signature']
            })
        return stars

    def _create_constellation_connections(self) -> List[Dict[str, Any]]:
        """Create constellation connections between related states"""
        connections = [
            ('dormant_equilibrium', 'focused_processing'),
            ('focused_processing', 'integrative_synthesis'),
            ('focused_processing', 'creative_exploration'),
            ('creative_exploration', 'integrative_synthesis'),
            ('integrative_synthesis', 'transcendent_awareness'),
            ('exploratory_search', 'creative_exploration'),
            ('exploratory_search', 'focused_processing'),
            ('chaotic_transition', 'creative_exploration')
        ]
        
        connection_data = []
        for state1, state2 in connections:
            pos1, _ = self.project_4d_to_sphere(
                CONSCIOUSNESS_ARCHETYPES[state1]['scup_signature']
            )
            pos2, _ = self.project_4d_to_sphere(
                CONSCIOUSNESS_ARCHETYPES[state2]['scup_signature']
            )
            
            connection_data.append({
                'from_state': state1,
                'to_state': state2,
                'from_position': pos1,
                'to_position': pos2,
                'distance': np.linalg.norm(np.array(pos1) - np.array(pos2))
            })
        
        return connection_data

    def project_4d_to_sphere(self, scup_coordinates: Tuple[float, float, float, float]) -> Tuple[Tuple[float, float, float], float]:
        """Project 4D SCUP coordinates onto 3D sphere surface"""
        s, c, u, p = scup_coordinates
        
        # Schema + Coherence -> azimuthal angle (φ)
        phi = 2 * np.pi * (0.7 * s + 0.3 * c)
        
        # Utility -> polar angle (θ) 
        theta = np.pi * (0.2 + 0.6 * u)  # Avoid poles
        
        # All dimensions influence radius slightly
        base_radius = self.sphere_radius
        radius = base_radius * (0.8 + 0.05 * s + 0.05 * c + 0.05 * u + 0.05 * p)
        
        # Convert to Cartesian
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)
        
        return (x, y, z), p  # Position and pressure for coloring

    def analyze_consciousness_state(self, json_data: dict) -> Tuple[float, float, float, float]:
        """Analyze current consciousness state from DAWN data"""
        # Extract SCUP values
        scup = json_data.get('scup', {})
        current_scup = (
            scup.get('schema', 0.5),
            scup.get('coherence', 0.5),
            scup.get('utility', 0.5),
            scup.get('pressure', 0.5)
        )
        
        # Add to trajectory
        self.consciousness_trajectory.append({
            'scup': current_scup,
            'timestamp': time.time(),
            'raw_data': json_data
        })
        
        # Classify consciousness archetype
        self.current_archetype = self.classify_consciousness_state(current_scup)
        
        # Update temporal segments
        self.update_temporal_segments()
        
        # Calculate consciousness metrics
        self.consciousness_metrics = self.calculate_consciousness_metrics()
        
        # Detect phase transitions
        self.detect_phase_transitions()
        
        return current_scup

    def classify_consciousness_state(self, scup_state: Tuple[float, float, float, float]) -> str:
        """Classify current state into nearest consciousness archetype"""
        min_distance = float('inf')
        nearest_archetype = 'dormant_equilibrium'
        
        for archetype_name, archetype in CONSCIOUSNESS_ARCHETYPES.items():
            # Calculate 4D Euclidean distance
            distance = np.linalg.norm(
                np.array(scup_state) - np.array(archetype['scup_signature'])
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_archetype = archetype_name
        
        return nearest_archetype

    def update_temporal_segments(self):
        """Update trajectory segments for each temporal scale"""
        if not self.consciousness_trajectory:
            return
        
        trajectory_list = list(self.consciousness_trajectory)
        
        for scale_name, config in TEMPORAL_SCALES.items():
            window_size = min(config['window_size'], len(trajectory_list))
            
            if window_size > 0:
                recent_states = trajectory_list[-window_size:]
                
                # Extract SCUP coordinates
                scup_coords = [state['scup'] for state in recent_states]
                
                # Project to 3D
                projected_points = []
                for scup in scup_coords:
                    pos_3d, pressure = self.project_4d_to_sphere(scup)
                    projected_points.append({
                        'position': pos_3d,
                        'pressure': pressure,
                        'scup': scup
                    })
                
                self.trajectory_segments[scale_name] = projected_points

    def calculate_consciousness_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive consciousness metrics"""
        if len(self.consciousness_trajectory) < 10:
            return {}
        
        recent_trajectory = list(self.consciousness_trajectory)[-100:]
        scup_history = [state['scup'] for state in recent_trajectory]
        
        metrics = {
            # Exploration metrics
            'exploration_volume': self.calculate_4d_hull_volume(scup_history),
            'dimensional_variance': np.var(scup_history, axis=0).mean(),
            'trajectory_length': self.calculate_trajectory_length(scup_history),
            
            # Stability metrics
            'state_stability': self.calculate_state_stability(scup_history),
            'archetype_consistency': self.calculate_archetype_consistency(recent_trajectory),
            'oscillation_frequency': self.detect_oscillation_patterns(scup_history),
            
            # Intelligence metrics
            'adaptation_rate': self.calculate_adaptation_rate(scup_history),
            'goal_achievement': self.calculate_goal_achievement(recent_trajectory),
            'pattern_complexity': self.calculate_pattern_complexity(scup_history),
            
            # Transcendence metrics
            'transcendence_proximity': self.calculate_transcendence_proximity(scup_history),
            'meta_cognitive_depth': self.estimate_meta_cognitive_depth(recent_trajectory),
            'consciousness_coherence': self.calculate_consciousness_coherence(scup_history)
        }
        
        # Overall consciousness intelligence quotient
        metrics['consciousness_iq'] = self.calculate_consciousness_iq(metrics)
        
        return metrics

    def calculate_4d_hull_volume(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Calculate convex hull volume in 4D SCUP space"""
        if len(scup_history) < 5:
            return 0

            # Use PCA to project to 3D for hull calculation
            scup_array = np.array(scup_history)
            centered = scup_array - scup_array.mean(axis=0)
            
            # Simple volume estimate using spread
            volume = np.prod(np.std(centered, axis=0)) * len(scup_history)
            return np.clip(volume, 0, 1)
            return 0

    def calculate_trajectory_length(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Calculate total path length through 4D space"""
        if len(scup_history) < 2:
            return 0
        
        total_length = 0
        for i in range(1, len(scup_history)):
            segment_length = np.linalg.norm(
                np.array(scup_history[i]) - np.array(scup_history[i-1])
            )
            total_length += segment_length
        
        return total_length

    def calculate_state_stability(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Measure consciousness state stability"""
        if len(scup_history) < 10:
            return 0
        
        # Calculate variance over sliding windows
        window_size = min(10, len(scup_history) // 2)
        variances = []
        
        for i in range(len(scup_history) - window_size):
            window = scup_history[i:i+window_size]
            variance = np.var(window, axis=0).mean()
            variances.append(variance)
        
        # Lower variance = higher stability
        avg_variance = np.mean(variances)
        stability = 1 - np.clip(avg_variance * 10, 0, 1)
        
        return stability

    def calculate_archetype_consistency(self, trajectory: List[Dict[str, Any]]) -> float:
        """Measure consistency of consciousness archetypes"""
        if len(trajectory) < 5:
            return 0
        
        archetypes = [self.classify_consciousness_state(state['scup']) 
                     for state in trajectory]
        
        # Count archetype changes
        changes = sum(1 for i in range(1, len(archetypes)) 
                     if archetypes[i] != archetypes[i-1])
        
        consistency = 1 - (changes / len(archetypes))
        return consistency

    def detect_oscillation_patterns(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Detect oscillation frequency in consciousness states"""
        if len(scup_history) < 20:
            return 0
        
        # Simple FFT-based frequency detection on first principal component
        scup_array = np.array(scup_history)
        mean_trajectory = scup_array.mean(axis=1)
        
        # Detect zero crossings
        centered = mean_trajectory - mean_trajectory.mean()
        zero_crossings = np.where(np.diff(np.sign(centered)))[0]
        
        if len(zero_crossings) > 1:
            avg_period = np.mean(np.diff(zero_crossings))
            frequency = 1 / avg_period if avg_period > 0 else 0
            return np.clip(frequency, 0, 1)
        
        return 0

    def calculate_adaptation_rate(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Measure how quickly consciousness adapts"""
        if len(scup_history) < 20:
            return 0
        
        # Calculate moving average convergence
        fast_window = 5
        slow_window = 20
        
        fast_ma = np.array([np.mean(scup_history[max(0, i-fast_window):i+1], axis=0)
                           for i in range(len(scup_history))])
        slow_ma = np.array([np.mean(scup_history[max(0, i-slow_window):i+1], axis=0)
                           for i in range(len(scup_history))])
        
        # Adaptation is the divergence between fast and slow averages
        divergence = np.mean(np.linalg.norm(fast_ma - slow_ma, axis=1))
        
        return np.clip(divergence * 2, 0, 1)

    def calculate_goal_achievement(self, trajectory: List[Dict[str, Any]]) -> float:
        """Measure utility optimization success"""
        if not trajectory:
            return 0
        
        # Goal achievement is high utility with low pressure
        utilities = [state['scup'][2] for state in trajectory]  # Utility dimension
        pressures = [state['scup'][3] for state in trajectory]  # Pressure dimension
        
        # High utility + low pressure = good goal achievement
        achievement_scores = [u * (1 - p) for u, p in zip(utilities, pressures)]
        
        return np.mean(achievement_scores)

    def calculate_pattern_complexity(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Measure complexity of consciousness patterns"""
        if len(scup_history) < 10:
            return 0
        
        # Use approximate entropy as complexity measure
        scup_array = np.array(scup_history)
        
        # Discretize into bins for pattern analysis
        n_bins = 5
        discretized = np.floor(scup_array * n_bins).astype(int)
        
        # Count unique patterns of length 3
        patterns = set()
        for i in range(len(discretized) - 2):
            pattern = tuple(discretized[i:i+3].flatten())
            patterns.add(pattern)
        
        # Normalize by maximum possible patterns
        max_patterns = min(len(discretized) - 2, n_bins ** 12)  # 4D * 3 length
        complexity = len(patterns) / max_patterns
        
        return np.clip(complexity, 0, 1)

    def calculate_transcendence_proximity(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Calculate proximity to transcendent consciousness state"""
        if not scup_history:
            return 0
        
        transcendent_state = CONSCIOUSNESS_ARCHETYPES['transcendent_awareness']['scup_signature']
        
        # Calculate minimum distance to transcendent state
        distances = [np.linalg.norm(np.array(state) - np.array(transcendent_state))
                    for state in scup_history]
        
        min_distance = min(distances)
        avg_distance = np.mean(distances)
        
        # Proximity is inverse of distance
        proximity = 1 - np.clip(min_distance / np.sqrt(4), 0, 1)
        
        # Bonus for sustained proximity
        sustained_bonus = 0.2 * (1 - np.clip(avg_distance / np.sqrt(4), 0, 1))
        
        return np.clip(proximity + sustained_bonus, 0, 1)

    def estimate_meta_cognitive_depth(self, trajectory: List[Dict[str, Any]]) -> float:
        """Estimate depth of meta-cognitive processing"""
        if len(trajectory) < 10:
            return 0
        
        # High schema + high coherence + low pressure = meta-cognition
        meta_scores = []
        for state in trajectory:
            s, c, u, p = state['scup']
            meta_score = (s + c) / 2 * (1 - p)
            meta_scores.append(meta_score)
        
        # Look for sustained meta-cognitive states
        sustained_meta = sum(1 for score in meta_scores if score > 0.6) / len(meta_scores)
        
        return sustained_meta

    def calculate_consciousness_coherence(self, scup_history: List[Tuple[float, float, float, float]]) -> float:
        """Measure overall consciousness coherence"""
        if len(scup_history) < 5:
            return 0
        
        # Coherence is low variance + high mean coherence dimension
        coherence_values = [state[1] for state in scup_history]  # Coherence dimension
        
        mean_coherence = np.mean(coherence_values)
        coherence_stability = 1 - np.std(coherence_values)
        
        overall_coherence = 0.7 * mean_coherence + 0.3 * coherence_stability
        
        return np.clip(overall_coherence, 0, 1)

    def calculate_consciousness_iq(self, metrics: Dict[str, float]) -> float:
        """Calculate overall consciousness intelligence quotient"""
        if not metrics:
            return 0
        
        # Weighted combination of key metrics
        weights = {
            'exploration_volume': 0.15,
            'state_stability': 0.10,
            'adaptation_rate': 0.15,
            'goal_achievement': 0.20,
            'pattern_complexity': 0.15,
            'transcendence_proximity': 0.15,
            'consciousness_coherence': 0.10
        }
        
        iq_score = 0
        for metric, weight in weights.items():
            if metric in metrics:
                iq_score += metrics[metric] * weight
        
        # Scale to 0-200 range like traditional IQ
        consciousness_iq = iq_score * 200
        
        return consciousness_iq

    def detect_phase_transitions(self):
        """Detect major consciousness phase transitions"""
        if len(self.consciousness_trajectory) < 50:
            return
        
        trajectory_list = list(self.consciousness_trajectory)
        
        # Sliding window analysis
        window_size = 20
        transitions = []
        
        for i in range(window_size, len(trajectory_list) - window_size):
            before_window = trajectory_list[i-window_size:i]
            after_window = trajectory_list[i:i+window_size]
            
            # Calculate centroids
            before_centroid = np.mean([s['scup'] for s in before_window], axis=0)
            after_centroid = np.mean([s['scup'] for s in after_window], axis=0)
            
            # Check for significant change
            transition_magnitude = np.linalg.norm(after_centroid - before_centroid)
            
            if transition_magnitude > 0.3:
                before_archetype = self.classify_consciousness_state(tuple(before_centroid))
                after_archetype = self.classify_consciousness_state(tuple(after_centroid))
                
                if before_archetype != after_archetype:
                    transitions.append({
                        'timestamp': trajectory_list[i]['timestamp'],
                        'from_state': before_archetype,
                        'to_state': after_archetype,
                        'magnitude': transition_magnitude
                    })
        
        self.phase_transitions = transitions[-10:]  # Keep last 10 transitions

    def get_analytics(self) -> Dict[str, Any]:
        """Calculate comprehensive analytics"""
        if not self.consciousness_metrics:
            return {}
        
        # Get current position
        current_pos_3d, current_pressure = None, 0.5
        if self.consciousness_trajectory:
            current_scup = self.consciousness_trajectory[-1]['scup']
            current_pos_3d, current_pressure = self.project_4d_to_sphere(current_scup)
        
        return {
            'current_archetype': self.current_archetype,
            'current_position_3d': current_pos_3d,
            'current_pressure': current_pressure,
            'trajectory_length': len(self.consciousness_trajectory),
            'phase_transitions': len(self.phase_transitions),
            'consciousness_iq': self.consciousness_metrics.get('consciousness_iq', 100),
            'exploration_volume': self.consciousness_metrics.get('exploration_volume', 0),
            'state_stability': self.consciousness_metrics.get('state_stability', 0),
            'transcendence_proximity': self.consciousness_metrics.get('transcendence_proximity', 0),
            'meta_cognitive_depth': self.consciousness_metrics.get('meta_cognitive_depth', 0),
            'consciousness_coherence': self.consciousness_metrics.get('consciousness_coherence', 0)
        }

    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for API/WebSocket transmission"""
        analytics = self.get_analytics()
        
        # Get trajectory data for each temporal scale
        trajectory_data = {}
        for scale_name, points in self.trajectory_segments.items():
            trajectory_data[scale_name] = [
                {
                    'position': point['position'],
                    'pressure': point['pressure'],
                    'scup': point['scup']
                }
                for point in points
            ]
        
        # Get consciousness stars data
        stars_data = []
        for star in self.consciousness_stars:
            stars_data.append({
                'name': star['name'],
                'position': star['position'],
                'pressure': star['pressure'],
                'color': star['data']['color'],
                'description': star['data']['description'],
                'stability': star['data']['stability']
            })
        
        # Get constellation connections
        connections_data = []
        for connection in self.constellation_connections:
            connections_data.append({
                'from_state': connection['from_state'],
                'to_state': connection['to_state'],
                'from_position': connection['from_position'],
                'to_position': connection['to_position'],
                'distance': connection['distance']
            })
        
        return {
            'tick': self.current_tick,
            'analytics': analytics,
            'consciousness_metrics': self.consciousness_metrics,
            'trajectory_segments': trajectory_data,
            'consciousness_stars': stars_data,
            'constellation_connections': connections_data,
            'phase_transitions': self.phase_transitions[-5:] if self.phase_transitions else [],
            'current_archetype': self.current_archetype,
            'timestamp': datetime.now().isoformat()
        }

    def is_active(self) -> bool:
        """Check if visualizer is active"""
        return self._active

    def start_animation(self) -> None:
        """Start the animation loop"""
        self._active = True
        logger.info("ConsciousnessConstellationBackend animation started")

    def stop_animation(self) -> None:
        """Stop the animation"""
        self._active = False
        logger.info("ConsciousnessConstellationBackend animation stopped")

    def update_visualization(self, data=None, tick=None) -> None:
        """Update the visualization with new data"""
        if tick is not None:
            self.current_tick = tick
        
        if data:
            # Analyze consciousness state from DAWN data
            self.analyze_consciousness_state(data)
        
        # Update analytics history
        self.analytics_history.append(self.get_analytics())

    def update_all_processes(self, all_process_data=None, tick=None) -> None:
        """Update visualization for all processes"""
        # For consciousness constellation, we use the main system state
        if all_process_data and 0 in all_process_data:
            main_data = all_process_data[0]
            self.update_visualization(main_data, tick)
        else:
            self.update_visualization(None, tick)

    def close(self) -> None:
        """Close the visualization"""
        self._active = False
        logger.info("ConsciousnessConstellationBackend closed")

    async def shutdown(self) -> None:
        """Async shutdown"""
        self.close()

    async def tick(self, *args, **kwargs):
        self.current_tick += 1
        self.update_visualization(None, None)

    def save_animation_gif(self):
        """Save the animation as GIF"""

            if hasattr(self, 'animation'):
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)

# Singleton accessor
_consciousness_constellation = None

def get_consciousness_constellation() -> ConsciousnessConstellationBackend:
    """Get or create the global consciousness constellation instance"""
    global _consciousness_constellation
    if _consciousness_constellation is None:
        _consciousness_constellation = ConsciousnessConstellationBackend()
    return _consciousness_constellation 