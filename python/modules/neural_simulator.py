import asyncio
import logging
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time
import math

logger = logging.getLogger(__name__)


@dataclass
class NeuralNode:
    """A simulated neural node"""
    id: str
    position: tuple  # (x, y, z)
    activation: float  # 0-1
    threshold: float
    connections: List[str]  # Connected node IDs
    layer: int
    node_type: str  # 'input', 'hidden', 'output'


@dataclass
class NeuralConnection:
    """Connection between neural nodes"""
    from_node: str
    to_node: str
    weight: float  # -1 to 1
    strength: float  # 0-1


class NeuralSimulator:
    """
    Simulates a neural network with dynamic activity patterns.
    Provides realistic neural firing patterns for consciousness simulation.
    """
    
    def __init__(self, network_size: str = "medium"):
        self.network_size = network_size
        self.nodes: Dict[str, NeuralNode] = {}
        self.connections: Dict[str, NeuralConnection] = {}
        
        # Network parameters
        self.base_firing_rate = 0.1  # Background activity
        self.activation_decay = 0.05  # How fast activation decays
        self.noise_level = 0.02  # Random noise
        
        # Activity tracking
        self.current_activity = 0.5
        self.firing_history = []
        self.pattern_cycles = 0
        
        # Initialize network
        self._build_network()
        
        logger.info(f"Neural simulator initialized with {len(self.nodes)} nodes")
    
    def _build_network(self):
        """Build the neural network structure"""
        if self.network_size == "small":
            layers = [8, 12, 8, 4]
        elif self.network_size == "medium":
            layers = [16, 24, 32, 24, 16]
        elif self.network_size == "large":
            layers = [32, 48, 64, 48, 32, 16]
        else:
            layers = [16, 24, 32, 24, 16]  # Default medium
        
        # Create nodes
        node_id = 0
        for layer_idx, layer_size in enumerate(layers):
            layer_type = "input" if layer_idx == 0 else ("output" if layer_idx == len(layers) - 1 else "hidden")
            
            for i in range(layer_size):
                # Position nodes in 3D space
                x = layer_idx / (len(layers) - 1)
                y = (i / (layer_size - 1) - 0.5) * 2  # -1 to 1
                z = np.random.uniform(-0.5, 0.5)
                
                node = NeuralNode(
                    id=f"node_{node_id}",
                    position=(x, y, z),
                    activation=np.random.uniform(0, 0.1),
                    threshold=np.random.uniform(0.3, 0.7),
                    connections=[],
                    layer=layer_idx,
                    node_type=layer_type
                )
                
                self.nodes[node.id] = node
                node_id += 1
        
        # Create connections between adjacent layers
        for layer_idx in range(len(layers) - 1):
            current_layer_nodes = [n for n in self.nodes.values() if n.layer == layer_idx]
            next_layer_nodes = [n for n in self.nodes.values() if n.layer == layer_idx + 1]
            
            for current_node in current_layer_nodes:
                for next_node in next_layer_nodes:
                    # Connect with some probability
                    if np.random.random() < 0.6:  # 60% connection probability
                        connection_id = f"{current_node.id}_to_{next_node.id}"
                        connection = NeuralConnection(
                            from_node=current_node.id,
                            to_node=next_node.id,
                            weight=np.random.uniform(-1, 1),
                            strength=np.random.uniform(0.3, 1.0)
                        )
                        
                        self.connections[connection_id] = connection
                        current_node.connections.append(next_node.id)
        
        # Add some recurrent connections for dynamics
        all_nodes = list(self.nodes.values())
        for _ in range(len(all_nodes) // 4):  # 25% of nodes get recurrent connections
            node1 = np.random.choice(all_nodes)
            node2 = np.random.choice(all_nodes)
            
            if node1.id != node2.id and node2.id not in node1.connections:
                connection_id = f"{node1.id}_to_{node2.id}_recurrent"
                connection = NeuralConnection(
                    from_node=node1.id,
                    to_node=node2.id,
                    weight=np.random.uniform(-0.5, 0.5),
                    strength=np.random.uniform(0.1, 0.5)
                )
                
                self.connections[connection_id] = connection
                node1.connections.append(node2.id)
    
    async def get_state(self, tick_number: int) -> Dict[str, Any]:
        """Get current neural state"""
        # Update neural activity
        await self._update_network_activity(tick_number)
        
        # Calculate metrics
        total_activation = sum(node.activation for node in self.nodes.values())
        avg_activation = total_activation / len(self.nodes)
        
        # Firing rate (0-100)
        firing_rate = min(100, avg_activation * 150)
        
        # Pattern strength (how synchronized the network is)
        activations = [node.activation for node in self.nodes.values()]
        pattern_strength = 1 - (np.std(activations) / (np.mean(activations) + 0.001))
        
        # Network synchrony
        synchrony = self._calculate_synchrony()
        
        # Store for history
        self.firing_history.append(firing_rate)
        if len(self.firing_history) > 100:
            self.firing_history.pop(0)
        
        self.current_activity = avg_activation
        
        return {
            'firing_rate': firing_rate,
            'avg_activation': avg_activation,
            'pattern_strength': pattern_strength,
            'synchrony': synchrony,
            'active_nodes': sum(1 for node in self.nodes.values() if node.activation > 0.5),
            'total_nodes': len(self.nodes),
            'connections': len(self.connections),
            'firing_history': self.firing_history[-20:],  # Last 20 ticks
            'network_energy': self._calculate_network_energy(),
            'dominant_frequency': self._estimate_dominant_frequency()
        }
    
    async def _update_network_activity(self, tick_number: int):
        """Update neural network activity"""
        # Add rhythmic patterns based on tick number
        base_rhythm = 0.1 * math.sin(tick_number * 0.1)  # Slow rhythm
        fast_rhythm = 0.05 * math.sin(tick_number * 0.5)  # Fast rhythm
        
        # Calculate new activations
        new_activations = {}
        
        for node in self.nodes.values():
            # Start with current activation
            new_activation = node.activation
            
            # Apply decay
            new_activation *= (1 - self.activation_decay)
            
            # Add base firing rate
            new_activation += self.base_firing_rate
            
            # Add rhythmic components
            new_activation += base_rhythm + fast_rhythm
            
            # Add input from connected nodes
            input_sum = 0
            input_count = 0
            
            for connection in self.connections.values():
                if connection.to_node == node.id:
                    source_node = self.nodes[connection.from_node]
                    input_sum += source_node.activation * connection.weight * connection.strength
                    input_count += 1
            
            if input_count > 0:
                # Apply sigmoid activation function
                input_avg = input_sum / input_count
                sigmoid_input = 1 / (1 + np.exp(-input_avg * 5))
                new_activation += sigmoid_input * 0.3
            
            # Add noise
            new_activation += np.random.normal(0, self.noise_level)
            
            # Apply threshold and clamp
            if new_activation > node.threshold:
                new_activation = min(1.0, new_activation)
            else:
                new_activation *= 0.7  # Sub-threshold decay
            
            new_activation = max(0.0, new_activation)
            new_activations[node.id] = new_activation
        
        # Update all activations simultaneously
        for node_id, activation in new_activations.items():
            self.nodes[node_id].activation = activation
    
    def _calculate_synchrony(self) -> float:
        """Calculate network synchrony (0-1)"""
        activations = [node.activation for node in self.nodes.values()]
        
        if len(activations) < 2:
            return 0.0
        
        # Calculate correlation between activations
        mean_activation = np.mean(activations)
        variance = np.var(activations)
        
        if variance == 0:
            return 1.0  # Perfect synchrony (all same)
        
        # Synchrony is inversely related to variance
        synchrony = max(0.0, 1.0 - (variance / (mean_activation + 0.001)))
        
        return min(1.0, synchrony)
    
    def _calculate_network_energy(self) -> float:
        """Calculate total network energy"""
        # Energy is sum of squared activations
        energy = sum(node.activation ** 2 for node in self.nodes.values())
        return energy / len(self.nodes)  # Normalized
    
    def _estimate_dominant_frequency(self) -> float:
        """Estimate dominant frequency from firing history"""
        if len(self.firing_history) < 10:
            return 0.0
        
        # Simple frequency estimation using autocorrelation
        history = np.array(self.firing_history[-50:])  # Last 50 samples
        
        if len(history) < 10:
            return 0.0
        
        # Calculate autocorrelation
        autocorr = np.correlate(history, history, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Find peak (excluding lag 0)
        if len(autocorr) > 5:
            peak_idx = np.argmax(autocorr[1:5]) + 1  # Look in first 5 lags
            frequency = 1.0 / (peak_idx + 1) if peak_idx > 0 else 0.0
            return frequency
        
        return 0.0
    
    def trigger_pattern(self, pattern_type: str = "burst"):
        """Trigger a specific neural pattern"""
        if pattern_type == "burst":
            # Activate random 30% of nodes
            nodes_to_activate = np.random.choice(
                list(self.nodes.keys()), 
                size=int(len(self.nodes) * 0.3), 
                replace=False
            )
            
            for node_id in nodes_to_activate:
                self.nodes[node_id].activation = min(1.0, self.nodes[node_id].activation + 0.5)
        
        elif pattern_type == "wave":
            # Create a wave pattern across layers
            for layer_idx in range(max(node.layer for node in self.nodes.values()) + 1):
                layer_nodes = [node for node in self.nodes.values() if node.layer == layer_idx]
                
                # Delay based on layer
                delay_factor = layer_idx * 0.1
                activation_boost = 0.6 * np.exp(-delay_factor)
                
                for node in layer_nodes:
                    node.activation = min(1.0, node.activation + activation_boost)
        
        elif pattern_type == "synchronized":
            # Synchronize all nodes
            sync_level = 0.7
            for node in self.nodes.values():
                node.activation = sync_level + np.random.uniform(-0.1, 0.1)
                node.activation = max(0.0, min(1.0, node.activation))
        
        logger.info(f"Triggered neural pattern: {pattern_type}")
    
    def adjust_excitability(self, factor: float):
        """Adjust overall network excitability"""
        self.base_firing_rate *= factor
        self.base_firing_rate = max(0.01, min(0.5, self.base_firing_rate))
        
        logger.info(f"Neural excitability adjusted by factor: {factor}")
    
    def get_detailed_state(self) -> Dict[str, Any]:
        """Get detailed network state for debugging"""
        return {
            'nodes': {node_id: {
                'activation': node.activation,
                'threshold': node.threshold,
                'layer': node.layer,
                'type': node.node_type,
                'connections': len(node.connections)
            } for node_id, node in self.nodes.items()},
            'connections': {conn_id: {
                'weight': conn.weight,
                'strength': conn.strength,
                'from': conn.from_node,
                'to': conn.to_node
            } for conn_id, conn in self.connections.items()},
            'parameters': {
                'base_firing_rate': self.base_firing_rate,
                'activation_decay': self.activation_decay,
                'noise_level': self.noise_level
            }
        } 