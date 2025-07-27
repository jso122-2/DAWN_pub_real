from bloom.recursive_synthesis import recursive_synthesis
from visual.synthesis_entropy_chart import plot_entropy_trend
from visual.synthesis_lineage_animator import animate_synthesis_lineage
import json
import os
from datetime import datetime

def read_pulse_state() -> dict:
    """
    Read the current pulse state from pulse_state.json.
    Returns a dictionary containing the pulse state data.
    """
    try:
        with open("pulse_state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ No pulse state file found. Defaulting to safe state.")
        return {"current_heat": 0.0, "current_zone": "🟢 calm"}

def evolve_recursive_generations(generations=3):
    """
    Evolve recursive generations of blooms while respecting system pressure constraints.
    
    This function implements a pressure-aware evolution system that:
    1. Checks the current pulse state before each generation
    2. Only proceeds with evolution if system pressure is below 0.7
    3. Logs skipped generations due to high pressure
    4. Updates visualization after successful evolution
    
    Args:
        generations (int): Number of generations to evolve (default: 3)
    
    The evolution process follows these steps:
    1. Read current pulse state
    2. For each generation:
       - Check if system pressure allows evolution
       - If pressure is too high, log and skip
       - If pressure is acceptable, perform recursive synthesis
    3. Update visualizations after all generations
    """
    print(f"🧪 Beginning recursive synthesis across {generations} generations...\n")
    
    for gen in range(generations):
        print(f"--- Generation {gen + 1} ---")
        
        # Check pulse state before evolution
        pulse_state = read_pulse_state()
        current_pressure = pulse_state.get("current_heat", 0.0)
        
        if current_pressure >= 0.7:
            print(f"⚠️ Skipping generation {gen + 1} - System pressure too high ({current_pressure:.2f})")
            print(f"Current zone: {pulse_state.get('current_zone', 'unknown')}")
            continue
            
        print(f"✅ System pressure acceptable ({current_pressure:.2f}) - proceeding with evolution")
        recursive_synthesis()
        
    print("\n✅ All generations synthesized.")
    print("📈 Updating charts and visuals...")
    plot_entropy_trend()
    animate_synthesis_lineage()

if __name__ == "__main__":
    evolve_recursive_generations()
