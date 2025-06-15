# Tick_engine/visual/neural_network.py
"""
Neural Network Visualization Process for DAWN
============================================
Generates real-time neural network visualizations representing
consciousness patterns and information flow.
"""

import time
import math
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import deque
import threading
import json

from utils.logger_config import get_logger
from utils.metrics_collector import metrics
from schema.registry import registry

logger = get_logger(__name__)

@dataclass
class Neuron:
    """Represents a single neuron in the visualization"""
    id: str
    position: Tuple[float, float, float]  # 3D position
    activation: float = 0.0
    neuron_type: str = "excitatory"  # excitatory, inhibitory, modulatory
    connections: List[str] = field(default_factory=list)
    charge: float = 0.0
    refractory_period: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Synapse:
    """Represents a connection between neurons"""
    source_id: str
    target_id: str
    weight: float = 1.0
    plasticity: float = 0.5  # Learning rate
    signal_delay: float = 0.01
    neurotransmitter: str = "glutamate"
    recent_activity: deque = field(default_factory=lambda: deque(maxlen=100))

@dataclass
class NeuralLayer:
    """Represents a layer in the neural network"""
    name: str
    layer_type: str  # input, hidden, output, recurrent
    neurons: List[Neuron] = field(default_factory=list)
    position_offset: Tuple[float, float, float] = (0, 0, 0)
    activation_function: str = "sigmoid"

class NeuralNetworkVisualizer:
    """
    Generates and updates neural network visualizations based on
    consciousness state and tick data.
    """
    
    def __init__(self):
        # Network structure
        self.layers: List[NeuralLayer] = []
        self.neurons: Dict[str, Neuron] = {}
        self.synapses: Dict[Tuple[str, str], Synapse] = {}
        
        # Visualization parameters
        self.network_size = (100, 100, 50)  # 3D space dimensions
        self.layer_spacing = 20
        self.neuron_radius = 1.0
        
        # Animation state
        self.animation_speed = 1.0
        self.pulse_phase = 0.0
        self.wave_patterns = []
        
        # Activity tracking
        self.activity_history = deque(maxlen=1000)
        self.spike_trains = defaultdict(deque)
        self.max_spike_history = 100
        
        # Performance
        self.update_frequency = 30  # Hz
        self.last_update = time.time()
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Initialize network
        self._initialize_network()
        self._register_with_schema()
    
    def _initialize_network(self):
        """Initialize the neural network structure"""
        # Create layers
        self.layers = [
            NeuralLayer("sensory", "input", position_offset=(0, 0, 0)),
            NeuralLayer("processing_1", "hidden", position_offset=(0, 0, 20)),
            NeuralLayer("processing_2", "hidden", position_offset=(0, 0, 40)),
            NeuralLayer("integration", "hidden", position_offset=(0, 0, 60)),
            NeuralLayer("consciousness", "output", position_offset=(0, 0, 80))
        ]
        
        # Populate neurons
        neurons_per_layer = [20, 30, 30, 20, 10]
        
        for layer_idx, (layer, neuron_count) in enumerate(zip(self.layers, neurons_per_layer)):
            for i in range(neuron_count):
                # Arrange neurons in a circle
                angle = (i / neuron_count) * 2 * math.pi
                radius = 30
                
                x = radius * math.cos(angle) + layer.position_offset[0]
                y = radius * math.sin(angle) + layer.position_offset[1]
                z = layer.position_offset[2]
                
                neuron = Neuron(
                    id=f"{layer.name}_n{i}",
                    position=(x, y, z),
                    neuron_type="excitatory" if i % 5 != 0 else "inhibitory"
                )
                
                layer.neurons.append(neuron)
                self.neurons[neuron.id] = neuron
        
        # Create connections
        self._create_connections()
        
        logger.info(f"Initialized neural network with {len(self.neurons)} neurons")
    
    def _create_connections(self):
        """Create synaptic connections between neurons"""
        # Connect adjacent layers
        for i in range(len(self.layers) - 1):
            source_layer = self.layers[i]
            target_layer = self.layers[i + 1]
            
            # Create connections with small-world topology
            for source_neuron in source_layer.neurons:
                # Connect to subset of neurons in next layer
                connection_probability = 0.3
                
                for target_neuron in target_layer.neurons:
                    if np.random.random() < connection_probability:
                        # Calculate weight based on neuron types
                        if source_neuron.neuron_type == "excitatory":
                            weight = np.random.uniform(0.5, 1.5)
                        else:
                            weight = np.random.uniform(-1.5, -0.5)
                        
                        synapse = Synapse(
                            source_id=source_neuron.id,
                            target_id=target_neuron.id,
                            weight=weight,
                            plasticity=np.random.uniform(0.1, 0.9)
                        )
                        
                        self.synapses[(source_neuron.id, target_neuron.id)] = synapse
                        source_neuron.connections.append(target_neuron.id)
        
        # Add some recurrent connections within layers
        for layer in self.layers[1:-1]:  # Hidden layers only
            for i, neuron in enumerate(layer.neurons):
                # Connect to nearby neurons in same layer
                for j in range(max(0, i-2), min(len(layer.neurons), i+3)):
                    if i != j and np.random.random() < 0.2:
                        target = layer.neurons[j]
                        
                        synapse = Synapse(
                            source_id=neuron.id,
                            target_id=target.id,
                            weight=np.random.uniform(-0.5, 0.5),
                            neurotransmitter="gaba" if neuron.neuron_type == "inhibitory" else "glutamate"
                        )
                        
                        self.synapses[(neuron.id, target.id)] = synapse
                        neuron.connections.append(target.id)
        
        logger.info(f"Created {len(self.synapses)} synaptic connections")
    
    def _register_with_schema(self):
        """Register with schema registry"""
        registry.register(
            component_id="visual.neural_network",
            name="Neural Network Visualizer",
            component_type="VISUALIZER",
            instance=self,
            capabilities=["visualize_neural_activity", "track_information_flow"],
            version="2.0.0"
        )
    
    def update(self, tick_data: Dict[str, Any]):
        """Update visualization with new tick data"""
        with self.lock:
            current_time = time.time()
            
            # Rate limit updates
            if current_time - self.last_update < 1.0 / self.update_frequency:
                return
            
            self.last_update = current_time
            
            # Extract relevant data
            coherence = tick_data.get('activity', 0.5)
            pulse_sync = tick_data.get('pulse_sync', 0.5)
            nodes_data = tick_data.get('nodes', [])
            
            # Update network activity
            self._update_neural_activity(coherence, pulse_sync)
            
            # Process spike patterns
            self._process_spike_patterns(coherence)
            
            # Update synaptic plasticity
            self._update_plasticity()
            
            # Generate wave patterns
            self._generate_wave_patterns(pulse_sync)
            
            # Record activity
            self._record_activity()
            
            # Record metrics
            metrics.gauge("dawn.visual.neural.active_neurons", self._count_active_neurons())
            metrics.gauge("dawn.visual.neural.avg_activation", self._average_activation())
    
    def _update_neural_activity(self, coherence: float, pulse_sync: float):
        """Update neuron activations based on consciousness state"""
        # Update pulse phase
        self.pulse_phase += 0.1 * self.animation_speed
        
        # Propagate activity through layers
        for layer_idx, layer in enumerate(self.layers):
            for neuron in layer.neurons:
                # Base activation from position and phase
                x, y, z = neuron.position
                
                # Wave function for activation
                wave = math.sin(self.pulse_phase + z * 0.1) * pulse_sync
                
                # Layer-specific activation patterns
                if layer.layer_type == "input":
                    # Sensory layer responds to external stimuli
                    neuron.activation = coherence * (0.5 + 0.5 * wave)
                    
                elif layer.layer_type == "hidden":
                    # Hidden layers process information
                    input_sum = self._calculate_input(neuron)
                    neuron.activation = self._apply_activation_function(
                        input_sum + wave * 0.2,
                        layer.activation_function
                    )
                    
                elif layer.layer_type == "output":
                    # Output layer represents consciousness state
                    input_sum = self._calculate_input(neuron)
                    neuron.activation = self._apply_activation_function(
                        input_sum * coherence,
                        "tanh"
                    )
                
                # Apply refractory period
                if neuron.refractory_period > 0:
                    neuron.activation *= (1 - neuron.refractory_period)
                    neuron.refractory_period -= 0.1
                
                # Update charge
                neuron.charge += (neuron.activation - neuron.charge) * 0.1
                
                # Check for spike
                if neuron.activation > 0.8 and neuron.refractory_period <= 0:
                    self._fire_neuron(neuron)
    
    def _calculate_input(self, neuron: Neuron) -> float:
        """Calculate weighted input to a neuron"""
        total_input = 0.0
        
        # Sum inputs from all incoming connections
        for source_id, target_id in self.synapses:
            if target_id == neuron.id:
                synapse = self.synapses[(source_id, target_id)]
                source_neuron = self.neurons.get(source_id)
                
                if source_neuron:
                    # Apply synaptic weight and delay
                    delayed_activation = source_neuron.charge  # Use charge for delayed signal
                    total_input += delayed_activation * synapse.weight
        
        return total_input
    
    def _apply_activation_function(self, x: float, function: str) -> float:
        """Apply activation function"""
        if function == "sigmoid":
            return 1 / (1 + math.exp(-x))
        elif function == "tanh":
            return math.tanh(x)
        elif function == "relu":
            return max(0, x)
        elif function == "leaky_relu":
            return max(0.01 * x, x)
        else:
            return x
    
    def _fire_neuron(self, neuron: Neuron):
        """Handle neuron firing (spike)"""
        # Record spike
        self.spike_trains[neuron.id].append(time.time())
        
        # Limit spike history
        if len(self.spike_trains[neuron.id]) > self.max_spike_history:
            self.spike_trains[neuron.id].popleft()
        
        # Set refractory period
        neuron.refractory_period = 1.0
        
        # Propagate to connected neurons
        for target_id in neuron.connections:
            if (neuron.id, target_id) in self.synapses:
                synapse = self.synapses[(neuron.id, target_id)]
                synapse.recent_activity.append(time.time())
    
    def _process_spike_patterns(self, coherence: float):
        """Process and detect spike patterns"""
        # Detect synchronous firing
        current_time = time.time()
        recent_spikes = []
        
        for neuron_id, spike_times in self.spike_trains.items():
            # Count recent spikes
            recent = [t for t in spike_times if current_time - t < 0.5]
            if recent:
                recent_spikes.append((neuron_id, len(recent)))
        
        # Check for synchrony
        if len(recent_spikes) > 5:
            synchrony_score = len(recent_spikes) / len(self.neurons)
            
            if synchrony_score > 0.3:
                # High synchrony detected
                logger.debug(f"Neural synchrony detected: {synchrony_score:.2f}")
                
                # Boost coherence-based activity
                for neuron in self.neurons.values():
                    neuron.activation *= (1 + synchrony_score * coherence)
    
    def _update_plasticity(self):
        """Update synaptic plasticity based on activity"""
        for synapse_key, synapse in self.synapses.items():
            if len(synapse.recent_activity) >= 2:
                # Spike-timing dependent plasticity (STDP)
                time_diffs = np.diff(list(synapse.recent_activity))
                
                if len(time_diffs) > 0:
                    avg_interval = np.mean(time_diffs)
                    
                    # Strengthen frequently used connections
                    if avg_interval < 0.1:  # High frequency
                        synapse.weight *= 1.01
                    elif avg_interval > 1.0:  # Low frequency
                        synapse.weight *= 0.99
                    
                    # Bound weights
                    if synapse.weight > 0:
                        synapse.weight = min(2.0, max(0.1, synapse.weight))
                    else:
                        synapse.weight = max(-2.0, min(-0.1, synapse.weight))
    
    def _generate_wave_patterns(self, pulse_sync: float):
        """Generate wave patterns across the network"""
        self.wave_patterns.clear()
        
        # Create traveling waves
        wave_sources = [
            self.layers[0].neurons[0],  # Start from first sensory neuron
            self.layers[-1].neurons[0]  # And from first output neuron
        ]
        
        for source in wave_sources:
            wave = {
                'origin': source.position,
                'radius': 0,
                'speed': 10 * pulse_sync,
                'amplitude': source.activation,
                'decay': 0.95
            }
            self.wave_patterns.append(wave)
        
        # Update existing waves
        for wave in self.wave_patterns:
            wave['radius'] += wave['speed']
            wave['amplitude'] *= wave['decay']
            
            # Apply wave to neurons
            for neuron in self.neurons.values():
                distance = self._calculate_distance(wave['origin'], neuron.position)
                
                if abs(distance - wave['radius']) < 5:  # Wave thickness
                    wave_strength = wave['amplitude'] * math.exp(-0.1 * abs(distance - wave['radius']))
                    neuron.activation = max(neuron.activation, wave_strength)
    
    def _calculate_distance(self, pos1: Tuple[float, float, float], 
                          pos2: Tuple[float, float, float]) -> float:
        """Calculate 3D distance between positions"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    def _record_activity(self):
        """Record current activity state"""
        activity_snapshot = {
            'timestamp': time.time(),
            'active_neurons': self._count_active_neurons(),
            'avg_activation': self._average_activation(),
            'spike_rate': self._calculate_spike_rate(),
            'synchrony': self._calculate_synchrony()
        }
        
        self.activity_history.append(activity_snapshot)
    
    def _count_active_neurons(self) -> int:
        """Count neurons with significant activation"""
        return sum(1 for n in self.neurons.values() if n.activation > 0.5)
    
    def _average_activation(self) -> float:
        """Calculate average activation across network"""
        if not self.neurons:
            return 0.0
        
        return sum(n.activation for n in self.neurons.values()) / len(self.neurons)
    
    def _calculate_spike_rate(self) -> float:
        """Calculate network-wide spike rate"""
        current_time = time.time()
        recent_spike_count = 0
        
        for spike_times in self.spike_trains.values():
            recent_spike_count += sum(1 for t in spike_times if current_time - t < 1.0)
        
        return recent_spike_count / len(self.neurons) if self.neurons else 0.0
    
    def _calculate_synchrony(self) -> float:
        """Calculate network synchrony"""
        if not self.spike_trains:
            return 0.0
        
        # Simplified synchrony: variance of spike times
        all_recent_spikes = []
        current_time = time.time()
        
        for spike_times in self.spike_trains.values():
            recent = [t for t in spike_times if current_time - t < 0.5]
            all_recent_spikes.extend(recent)
        
        if len(all_recent_spikes) < 2:
            return 0.0
        
        # Low variance = high synchrony
        variance = np.var(all_recent_spikes)
        synchrony = 1.0 / (1.0 + variance)
        
        return synchrony
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get current visualization data for rendering"""
        with self.lock:
            # Prepare neuron data
            neurons_data = []
            for neuron in self.neurons.values():
                neurons_data.append({
                    'id': neuron.id,
                    'position': neuron.position,
                    'activation': neuron.activation,
                    'charge': neuron.charge,
                    'type': neuron.neuron_type,
                    'refractory': neuron.refractory_period > 0
                })
            
            # Prepare connection data
            connections_data = []
            for (source_id, target_id), synapse in self.synapses.items():
                connections_data.append({
                    'source': source_id,
                    'target': target_id,
                    'weight': synapse.weight,
                    'active': len(synapse.recent_activity) > 0
                })
            
            # Prepare layer data
            layers_data = []
            for layer in self.layers:
                layers_data.append({
                    'name': layer.name,
                    'type': layer.layer_type,
                    'neuron_count': len(layer.neurons),
                    'avg_activation': sum(n.activation for n in layer.neurons) / len(layer.neurons) if layer.neurons else 0
                })
            
            return {
                'neurons': neurons_data,
                'connections': connections_data,
                'layers': layers_data,
                'waves': self.wave_patterns.copy(),
                'metrics': {
                    'total_neurons': len(self.neurons),
                    'active_neurons': self._count_active_neurons(),
                    'total_synapses': len(self.synapses),
                    'avg_activation': self._average_activation(),
                    'spike_rate': self._calculate_spike_rate(),
                    'synchrony': self._calculate_synchrony()
                },
                'animation': {
                    'phase': self.pulse_phase,
                    'speed': self.animation_speed
                }
            }
    
    def reset(self):
        """Reset the neural network to initial state"""
        with self.lock:
            # Reset all neurons
            for neuron in self.neurons.values():
                neuron.activation = 0.0
                neuron.charge = 0.0
                neuron.refractory_period = 0.0
            
            # Reset synapses
            for synapse in self.synapses.values():
                synapse.recent_activity.clear()
            
            # Clear history
            self.activity_history.clear()
            self.spike_trains.clear()
            self.wave_patterns.clear()
            self.pulse_phase = 0.0
            
            logger.info("Neural network visualization reset")

# Global visualizer instance
visualizer = NeuralNetworkVisualizer()

# Module interface functions
def initialize():
    """Initialize the neural network visualizer"""
    global visualizer
    if visualizer is None:
        visualizer = NeuralNetworkVisualizer()
    logger.info("Neural network visualizer initialized")

def update(tick_data: Dict[str, Any]):
    """Update visualization with tick data"""
    if visualizer:
        visualizer.update(tick_data)

def get_data() -> Dict[str, Any]:
    """Get current visualization data"""
    if visualizer:
        return visualizer.get_visualization_data()
    return {}

def reset():
    """Reset the visualizer"""
    if visualizer:
        visualizer.reset()