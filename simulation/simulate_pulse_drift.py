"""
Pulse Drift Simulator
Simulates system pressure drift over time with controlled random variations.
Maintains pressure between 0.0 and 1.0 while logging all changes.
"""

import json
import os
import random
from datetime import datetime
import logging
from typing import Dict, Optional

# Constants
MAX_TICKS = 50
PRESSURE_DELTA = 0.03
MIN_PRESSURE = 0.0
MAX_PRESSURE = 1.0
PULSE_STATE_FILE = "pulse_state.json"
LOG_FILE = "logs/pressure_drift.log"

class PulseDriftSimulator:
    """Simulates system pressure drift with controlled random variations."""
    
    def __init__(self):
        """Initialize the simulator with proper logging and state management."""
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Initialize state
        self.current_pressure = self._load_initial_pressure()
        self.tick_count = 0
        
    def _load_initial_pressure(self) -> float:
        """Load initial pressure from pulse_state.json or create new state."""
        try:
            if os.path.exists(PULSE_STATE_FILE):
                with open(PULSE_STATE_FILE, 'r') as f:
                    state = json.load(f)
                    pressure = state.get('pressure', 0.5)
                    logging.info(f"Loaded initial pressure: {pressure:.3f}")
                    return pressure
            else:
                # Create new state with default pressure
                initial_pressure = 0.5
                self._save_pulse_state(initial_pressure)
                logging.info(f"Created new pulse state with pressure: {initial_pressure:.3f}")
                return initial_pressure
        except Exception as e:
            logging.error(f"Error loading pulse state: {str(e)}")
            return 0.5  # Default to middle pressure on error
            
    def _save_pulse_state(self, pressure: float) -> None:
        """Save current pressure to pulse_state.json."""
        try:
            state = {
                'pressure': pressure,
                'last_updated': datetime.now().isoformat(),
                'tick_count': self.tick_count
            }
            with open(PULSE_STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
            logging.info(f"Saved pulse state with pressure: {pressure:.3f}")
        except Exception as e:
            logging.error(f"Error saving pulse state: {str(e)}")
            
    def _calculate_pressure_drift(self) -> float:
        """Calculate random pressure drift within bounds."""
        # Generate random drift
        drift = random.uniform(-PRESSURE_DELTA, PRESSURE_DELTA)
        
        # Calculate new pressure
        new_pressure = self.current_pressure + drift
        
        # Clamp to valid range
        return max(MIN_PRESSURE, min(MAX_PRESSURE, new_pressure))
        
    def run_simulation(self) -> None:
        """Run the pressure drift simulation for MAX_TICKS."""
        logging.info("Starting pulse drift simulation")
        
        for tick in range(MAX_TICKS):
            self.tick_count = tick + 1
            
            # Calculate new pressure
            new_pressure = self._calculate_pressure_drift()
            pressure_change = new_pressure - self.current_pressure
            
            # Update current pressure
            self.current_pressure = new_pressure
            
            # Log the tick
            logging.info(
                f"Tick {self.tick_count:02d} - "
                f"Pressure: {self.current_pressure:.3f} "
                f"(Δ: {pressure_change:+.3f})"
            )
            
        # Save final state
        self._save_pulse_state(self.current_pressure)
        logging.info("Simulation complete")

def main():
    """Main entry point for the pulse drift simulator."""
    try:
        simulator = PulseDriftSimulator()
        simulator.run_simulation()
        print(f"Simulation complete. Check {LOG_FILE} for details.")
    except Exception as e:
        print(f"Error running simulation: {str(e)}")
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main() 