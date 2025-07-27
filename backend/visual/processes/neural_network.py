import numpy as np
import cv2
from ..base_visual import BaseVisualProcess

class VisualProcess(BaseVisualProcess):
    """Neural network visualization process."""
    
    def __init__(self, name: str = "neural_network", width: int = 800, height: int = 600):
        super().__init__(name, width, height)
        self.num_neurons = 50
        self.neurons = self._initialize_neurons()
        self.connections = self._initialize_connections()
        self.time = 0
        
    def _initialize_neurons(self) -> np.ndarray:
        """Initialize neuron positions and states."""
        neurons = np.zeros((self.num_neurons, 4))  # x, y, activation, phase
        for i in range(self.num_neurons):
            # Random position within frame
            neurons[i, 0] = np.random.uniform(0, self.width)
            neurons[i, 1] = np.random.uniform(0, self.height)
            # Random initial activation and phase
            neurons[i, 2] = np.random.uniform(0, 1)
            neurons[i, 3] = np.random.uniform(0, 2 * np.pi)
        return neurons
    
    def _initialize_connections(self) -> np.ndarray:
        """Initialize connections between neurons."""
        connections = []
        for i in range(self.num_neurons):
            # Connect to 3-5 random other neurons
            num_connections = np.random.randint(3, 6)
            for _ in range(num_connections):
                j = np.random.randint(0, self.num_neurons)
                if i != j:
                    connections.append((i, j))
        return np.array(connections)
    
    def _update_impl(self, dt: float) -> None:
        """Update neural network state."""
        self.time += dt
        
        # Update neuron activations
        for i in range(self.num_neurons):
            # Oscillate activation based on time and phase
            self.neurons[i, 2] = 0.5 + 0.5 * np.sin(self.time * 2 + self.neurons[i, 3])
            
            # Add some random noise
            self.neurons[i, 2] += np.random.normal(0, 0.1)
            self.neurons[i, 2] = np.clip(self.neurons[i, 2], 0, 1)
        
        # Create new frame
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Draw connections
        for i, j in self.connections:
            # Get neuron positions
            x1, y1 = int(self.neurons[i, 0]), int(self.neurons[i, 1])
            x2, y2 = int(self.neurons[j, 0]), int(self.neurons[j, 1])
            
            # Calculate connection strength based on neuron activations
            strength = (self.neurons[i, 2] + self.neurons[j, 2]) / 2
            
            # Draw line with varying color based on strength
            color = (
                int(255 * (1 - strength)),  # Red
                int(255 * strength),        # Green
                255                         # Blue
            )
            cv2.line(frame, (x1, y1), (x2, y2), color, 1)
        
        # Draw neurons
        for i in range(self.num_neurons):
            x, y = int(self.neurons[i, 0]), int(self.neurons[i, 1])
            activation = self.neurons[i, 2]
            
            # Draw neuron circle
            radius = int(3 + 2 * activation)
            color = (
                int(255 * (1 - activation)),  # Red
                int(255 * activation),        # Green
                255                           # Blue
            )
            cv2.circle(frame, (x, y), radius, color, -1)
            
            # Add glow effect
            cv2.circle(frame, (x, y), radius + 2, color, 1)
        
        # Add some text
        cv2.putText(
            frame,
            f"Neural Network - {self.num_neurons} Neurons",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )
        
        # Update frame
        self._frame = frame
        
        # Update metadata
        self._metadata = {
            "num_neurons": self.num_neurons,
            "num_connections": len(self.connections),
            "avg_activation": float(np.mean(self.neurons[:, 2])),
            "time": self.time
        } 