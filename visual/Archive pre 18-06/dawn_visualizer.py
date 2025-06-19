import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("visual.dawn_visualizer")

class DAWNVisualizer:
    """Visualizes DAWN system state"""
    
    def __init__(self):
        """Initialize the visualizer"""
        self.last_update = datetime.now(timezone.utc)
        self.state = {
            "scup": 0.5,
            "entropy": 0.5,
            "tension": 0.0,
            "drift": 0.0,
            "heat": 0.0,
            "stability": 1.0
        }
        logger.info("Initialized DAWNVisualizer")
        
    def update(self, metrics: Dict[str, float]) -> None:
        """Update visualization with new metrics"""
        try:
            current_time = datetime.now(timezone.utc)
            time_delta = (current_time - self.last_update).total_seconds()
            self.last_update = current_time
            
            # Update state with new metrics
            for key, value in metrics.items():
                if key in self.state:
                    self.state[key] = value
                    
            # Calculate visual indicators
            stability = 1.0 - abs(self.state["scup"] - 0.5) * 2
            self.state["stability"] = stability
            
            # Log state changes
            logger.debug(f"Updated visualization state: {self.state}")
            
            # Here you would typically update a visual display
            # For now, we'll just print a simple ASCII visualization
            self._print_ascii_state()
            
        except Exception as e:
            logger.error(f"Error updating visualization: {e}")
            
    def _print_ascii_state(self) -> None:
        """Print ASCII visualization of current state"""
        try:
            # Create simple ASCII visualization
            scup_bar = "█" * int(self.state["scup"] * 20) + "░" * (20 - int(self.state["scup"] * 20))
            entropy_bar = "█" * int(self.state["entropy"] * 20) + "░" * (20 - int(self.state["entropy"] * 20))
            tension_bar = "█" * int(self.state["tension"] * 20) + "░" * (20 - int(self.state["tension"] * 20))
            heat_bar = "█" * int(self.state["heat"] * 20) + "░" * (20 - int(self.state["heat"] * 20))
            
            print("\nDAWN System State:")
            print(f"SCUP:     [{scup_bar}] {self.state['scup']:.2f}")
            print(f"Entropy:  [{entropy_bar}] {self.state['entropy']:.2f}")
            print(f"Tension:  [{tension_bar}] {self.state['tension']:.2f}")
            print(f"Heat:     [{heat_bar}] {self.state['heat']:.2f}")
            print(f"Stability: {self.state['stability']:.2f}")
            print()
            
        except Exception as e:
            logger.error(f"Error printing ASCII state: {e}")
            
    def get_state(self) -> Dict[str, Any]:
        """Get current visualization state"""
        return {
            **self.state,
            "last_update": self.last_update.isoformat()
        } 