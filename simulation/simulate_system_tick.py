"""
System Tick Simulator (Master Integrator)
Orchestrates all simulation components and generates system state summary.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

# Import simulation modules
from simulate_pulse_drift import simulate_pulse_drift
from simulate_claude_burst import ClaudeBurstSimulator
from simulate_owl_read import OwlReadSimulator
from simulate_bloom_cycle import BloomCycleSimulator
from .simulate_tracer_tick import simulate_tracer_tick

# Constants
LOGS_DIR = "logs"
SUMMARY_LOG = "logs/system_simulation_summary.json"
SYSTEM_LOG = "logs/system_tick.log"

class SystemTickSimulator:
    """Orchestrates all simulation components and tracks system state."""
    
    def __init__(self):
        """Initialize the simulator with proper logging and state tracking."""
        # Ensure logs directory exists
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=SYSTEM_LOG,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Initialize simulation components
        self.claude_sim = ClaudeBurstSimulator()
        self.owl_sim = OwlReadSimulator()
        self.bloom_sim = BloomCycleSimulator()
        
        # Initialize state tracking
        self.system_state = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "warnings": [],
            "errors": []
        }
        
    def _update_component_state(self, component: str, state: Dict) -> None:
        """Update state for a specific component."""
        self.system_state["components"][component] = {
            "state": state,
            "last_updated": datetime.now().isoformat()
        }
        
    def _add_warning(self, component: str, message: str) -> None:
        """Add a warning to the system state."""
        self.system_state["warnings"].append({
            "component": component,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        logging.warning(f"{component}: {message}")
        
    def _add_error(self, component: str, message: str) -> None:
        """Add an error to the system state."""
        self.system_state["errors"].append({
            "component": component,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        logging.error(f"{component}: {message}")
        
    def _save_summary(self) -> None:
        """Save system state summary to JSON file."""
        try:
            with open(SUMMARY_LOG, 'w') as f:
                json.dump(self.system_state, f, indent=2)
            logging.info(f"System state summary saved to {SUMMARY_LOG}")
        except Exception as e:
            self._add_error("summary", f"Failed to save summary: {str(e)}")
            
    def run_simulation(self) -> None:
        """Run all simulation components in sequence."""
        logging.info("Starting system tick simulation")
        
        try:
            # 1. Simulate pulse drift
            logging.info("Running pulse drift simulation")
            pulse_state = simulate_pulse_drift()
            self._update_component_state("pulse", pulse_state)
            
            # 2. Simulate Claude burst
            logging.info("Running Claude burst simulation")
            self.claude_sim.simulate_burst()
            self._update_component_state("claude", {
                "status": "completed",
                "burst_count": 3
            })
            
            # 3. Simulate owl read
            logging.info("Running owl read simulation")
            self.owl_sim.run_owl_read()
            self._update_component_state("owl", {
                "status": "completed",
                "blooms_processed": 3
            })
            
            # 4. Simulate bloom cycle
            logging.info("Running bloom cycle simulation")
            self.bloom_sim.simulate_bloom_cycle()
            self._update_component_state("bloom", {
                "status": "completed",
                "cycles_completed": 1
            })
            
            # 5. Simulate tracer tick
            logging.info("Running tracer tick simulation")
            simulate_tracer_tick()
            self._update_component_state("tracer", {
                "status": "completed",
                "routes_evaluated": 3
            })
            
            # Update final timestamp
            self.system_state["timestamp"] = datetime.now().isoformat()
            
            # Save summary
            self._save_summary()
            
            logging.info("System tick simulation completed successfully")
            
        except Exception as e:
            self._add_error("system", f"Simulation failed: {str(e)}")
            self._save_summary()
            raise
            
    def print_summary(self) -> None:
        """Print a human-readable summary of the simulation results."""
        print("\nSystem Tick Simulation Summary")
        print("=" * 40)
        
        # Print component states
        print("\nComponent States:")
        for component, data in self.system_state["components"].items():
            print(f"\n{component.upper()}:")
            for key, value in data["state"].items():
                print(f"  {key}: {value}")
                
        # Print warnings
        if self.system_state["warnings"]:
            print("\nWarnings:")
            for warning in self.system_state["warnings"]:
                print(f"  {warning['component']}: {warning['message']}")
                
        # Print errors
        if self.system_state["errors"]:
            print("\nErrors:")
            for error in self.system_state["errors"]:
                print(f"  {error['component']}: {error['message']}")
                
        print(f"\nFull summary saved to: {SUMMARY_LOG}")

def main():
    """Main entry point for the system tick simulator."""
    try:
        simulator = SystemTickSimulator()
        simulator.run_simulation()
        simulator.print_summary()
    except Exception as e:
        print(f"Error running system simulation: {str(e)}")
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main() 