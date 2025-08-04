"""
Pulse System Loader
Handles loading and initialization of the pulse system components
"""

import os
import yaml
import logging
from typing import Tuple, Optional, Dict, Any
from pathlib import Path

from ...pulse_layer import UnifiedPulseHeat
from ...scup_tracker import SCUPTracker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pulse.pulse_loader")

def load_pulse_config() -> Dict[str, Any]:
    """Load pulse configuration from YAML file"""
    config_path = Path(__file__).parent.parent / 'config' / 'pulse_config.yaml'
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info("Successfully loaded pulse configuration")
        return config
    except Exception as e:
        logger.error(f"Failed to load pulse configuration: {e}")
        return {}

def initialize_pulse_system(config: Dict[str, Any]) -> Tuple[Optional[UnifiedPulseHeat], Optional[SCUPTracker]]:
    """Initialize pulse system components with configuration"""
    try:
        # Initialize SCUP tracker
        scup_tracker = SCUPTracker(
            threshold=config.get('scup_threshold', 0.5),
            cooldown=config.get('emergency', {}).get('recovery_cooldown', 300)
        )
        
        # Initialize pulse heat system
        pulse = UnifiedPulseHeat(
            decay_rate=config.get('thermal_decay_rate', 0.02),
            memory_window=config.get('thermal_memory_window', 100),
            max_heat=config.get('heat_capacity', 10.0)
        )
        pulse.baseline_heat = config.get('thermal_baseline', 0.0)
        pulse.conductivity = config.get('thermal_conductivity', 0.1)
        pulse.cooling_rate = config.get('thermal_cooling_rate', 0.05)
        
        # Configure mood weights
        pulse.mood_weights = config.get('mood_weights', {})
        
        # Configure zone thresholds
        pulse.zone_thresholds = config.get('zone_thresholds', {
            'calm': 0.3,
            'active': 0.7,
            'surge': 0.9
        })
        
        logger.info("Successfully initialized pulse system components")
        return pulse, scup_tracker
        
    except Exception as e:
        logger.error(f"Failed to initialize pulse system: {e}")
        return None, None

async def load_pulse_system() -> Tuple[Optional[UnifiedPulseHeat], callable, callable, Optional[SCUPTracker]]:
    """Load and initialize the pulse system components"""
    try:
        # Initialize SCUP tracker
        scup_tracker = SCUPTracker()
        logger.info("Initialized SCUPTracker")
        
        # Initialize pulse heat system
        pulse = UnifiedPulseHeat()
        logger.info("Initialized UnifiedPulseHeat")
        
        # Define thermal update function
        def tick_thermal_update(scup: float):
            """Update thermal state based on SCUP"""
            try:
                pulse.update(scup)
                scup_tracker.update(scup)
            except Exception as e:
                logger.error(f"Error in thermal update: {e}")
                
        # Define heat addition function
        def add_heat(amount: float):
            """Add heat to the system"""
            try:
                current_heat = pulse.get_heat()
                new_heat = min(1.0, current_heat + amount)
                pulse.heat = new_heat
                logger.debug(f"Added heat: {amount:.2f}, new heat: {new_heat:.2f}")
            except Exception as e:
                logger.error(f"Error adding heat: {e}")
                
        logger.info("Successfully loaded pulse configuration")
        logger.info("Successfully initialized pulse system components")
        logger.info("Pulse system loaded successfully")
        
        return pulse, tick_thermal_update, add_heat, scup_tracker
        
    except Exception as e:
        logger.error(f"Failed to load pulse system: {e}")
        return None, None, None, None

if __name__ == "__main__":
    # Test pulse system loading
    async def test():
        pulse, tick_update, add_heat, scup_tracker = await load_pulse_system()
        print("\nTesting pulse system:")
        print(f"Initial heat: {pulse._state.heat}")
        add_heat(0.5)
        print(f"After adding heat: {pulse._state.heat}")
        tick_update(0.1)
        print(f"After tick update: {pulse._state.heat}")
        print(f"Thermal profile: {pulse.get_state()}")
    
    asyncio.run(test()) 