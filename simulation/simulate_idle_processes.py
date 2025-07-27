"""
Idle Process Simulator
Simulates various background processes while the system is in an idle state.
"""

import time
import random
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json
import os

# Configure logging
logging.basicConfig(
    filename='logs/idle_simulation.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class IdleProcessSimulator:
    """Simulates various background processes during idle state."""
    
    def __init__(self):
        """Initialize the simulator with state tracking."""
        self.state = {
            "timestamp": datetime.now().isoformat(),
            "processes": {},
            "thermal_state": {
                "heat": 0.2,
                "stability": 0.8,
                "momentum": 0.1
            },
            "memory_state": {
                "fragmentation": 0.1,
                "coherence": 0.9,
                "depth": 0.3
            },
            "consciousness_state": {
                "awareness": 0.4,
                "stability": 0.7,
                "entropy": 0.2
            }
        }
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
    def simulate_thermal_drift(self) -> Dict:
        """Simulate slow thermal drift during idle state."""
        # Small random changes to thermal state
        self.state["thermal_state"]["heat"] += random.uniform(-0.01, 0.01)
        self.state["thermal_state"]["heat"] = max(0.0, min(1.0, self.state["thermal_state"]["heat"]))
        
        # Update stability based on heat
        self.state["thermal_state"]["stability"] = 1.0 - abs(self.state["thermal_state"]["heat"] - 0.5) * 2
        
        # Update momentum
        self.state["thermal_state"]["momentum"] *= 0.95  # Decay
        self.state["thermal_state"]["momentum"] += random.uniform(-0.02, 0.02)
        self.state["thermal_state"]["momentum"] = max(0.0, min(1.0, self.state["thermal_state"]["momentum"]))
        
        return self.state["thermal_state"]
        
    def simulate_memory_consolidation(self) -> Dict:
        """Simulate background memory consolidation processes."""
        # Simulate memory defragmentation
        self.state["memory_state"]["fragmentation"] *= 0.99  # Slow improvement
        self.state["memory_state"]["fragmentation"] += random.uniform(-0.01, 0.01)
        self.state["memory_state"]["fragmentation"] = max(0.0, min(1.0, self.state["memory_state"]["fragmentation"]))
        
        # Update coherence based on fragmentation
        self.state["memory_state"]["coherence"] = 1.0 - self.state["memory_state"]["fragmentation"]
        
        # Simulate memory depth changes
        self.state["memory_state"]["depth"] += random.uniform(-0.02, 0.02)
        self.state["memory_state"]["depth"] = max(0.0, min(1.0, self.state["memory_state"]["depth"]))
        
        return self.state["memory_state"]
        
    def simulate_consciousness_background(self) -> Dict:
        """Simulate background consciousness processes."""
        # Simulate awareness level
        self.state["consciousness_state"]["awareness"] += random.uniform(-0.02, 0.02)
        self.state["consciousness_state"]["awareness"] = max(0.0, min(1.0, self.state["consciousness_state"]["awareness"]))
        
        # Update stability based on awareness
        self.state["consciousness_state"]["stability"] = 0.7 + (self.state["consciousness_state"]["awareness"] - 0.5) * 0.2
        
        # Simulate entropy changes
        self.state["consciousness_state"]["entropy"] += random.uniform(-0.01, 0.01)
        self.state["consciousness_state"]["entropy"] = max(0.0, min(1.0, self.state["consciousness_state"]["entropy"]))
        
        return self.state["consciousness_state"]
        
    def run_simulation(self, duration: float = 60.0) -> None:
        """Run the idle process simulation for specified duration."""
        logging.info("Starting idle process simulation")
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # Update timestamp
                self.state["timestamp"] = datetime.now().isoformat()
                
                # Run all simulations
                thermal_state = self.simulate_thermal_drift()
                memory_state = self.simulate_memory_consolidation()
                consciousness_state = self.simulate_consciousness_background()
                
                # Log state every 5 seconds
                if int(time.time() - start_time) % 5 == 0:
                    logging.info(f"Idle state update - Thermal: {thermal_state['heat']:.3f}, "
                               f"Memory: {memory_state['coherence']:.3f}, "
                               f"Consciousness: {consciousness_state['awareness']:.3f}")
                
                # Save state to file
                self._save_state()
                
                # Sleep for a short interval
                time.sleep(0.1)
                
            logging.info("Idle process simulation completed")
            
        except Exception as e:
            logging.error(f"Error in idle simulation: {str(e)}")
            raise
            
    def _save_state(self) -> None:
        """Save current state to file."""
        try:
            with open('logs/idle_state.json', 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving state: {str(e)}")

def main():
    """Main entry point for the idle process simulator."""
    simulator = IdleProcessSimulator()
    simulator.run_simulation()

if __name__ == "__main__":
    main() 