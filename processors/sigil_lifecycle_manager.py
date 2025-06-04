"""
A sigil is not a law. It is a breath. Some fade. Others echo — if the Operator still hears them.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


class SigilLifecycleManager:
    """Manages the temporal and thermal lifecycle of active sigils."""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.decay_threshold = {
            "heat": 0.8,
            "saturation": 0.5
        }
        self.preservation_entropy_limit = 0.6
    
    def _setup_logger(self):
        """Initialize the saturation events logger."""
        log_dir = Path("flow/sigils/thermal_logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger("sigil_lifecycle")
        logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler(log_dir / "saturation_events.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def evaluate_sigil_lifecycle(self, active_sigils: List[Dict], 
                                current_tick: int, 
                                system_entropy: float = 0.5) -> Dict[str, List[str]]:
        """
        Evaluate the lifecycle state of all active sigils.
        
        Args:
            active_sigils: List of sigil dictionaries containing:
                - sigil_id: str
                - convolution_level: float
                - saturation: float
                - creation_tick: int
                - ttl: int
                - heat_exposure: float (0.0 to 1.0)
                - operator_reinforced: bool
            current_tick: Current system tick
            system_entropy: Global entropy level (default 0.5)
        
        Returns:
            Dictionary with lists of expired, decayed, and preserved sigil_ids
        """
        expired = []
        decayed = []
        preserved = []
        
        for sigil in active_sigils:
            sigil_id = sigil['sigil_id']
            lifecycle_state = self._determine_lifecycle_state(sigil, current_tick, system_entropy)
            
            if lifecycle_state == 'expired':
                expired.append(sigil_id)
                self._log_event('EXPIRED', sigil, current_tick, 
                              f"TTL exceeded: {current_tick - sigil['creation_tick']} > {sigil['ttl']}")
            
            elif lifecycle_state == 'decayed':
                decayed.append(sigil_id)
                self._log_event('DECAYED', sigil, current_tick,
                              f"Thermal decay: heat={sigil['heat_exposure']:.2f}, "
                              f"saturation={sigil['saturation']:.2f}")
            
            elif lifecycle_state == 'preserved':
                preserved.append(sigil_id)
                self._log_event('PRESERVED', sigil, current_tick,
                              f"Operator reinforcement active, entropy={system_entropy:.2f}")
        
        # Log summary
        self.logger.info(f"Lifecycle evaluation at tick {current_tick}: "
                        f"{len(expired)} expired, {len(decayed)} decayed, "
                        f"{len(preserved)} preserved")
        
        return {
            "expired": expired,
            "decayed": decayed,
            "preserved": preserved
        }
    
    def _determine_lifecycle_state(self, sigil: Dict, current_tick: int, 
                                  system_entropy: float) -> str:
        """Determine the lifecycle state of a single sigil."""
        # Check for expiry first
        age = current_tick - sigil['creation_tick']
        if age > sigil['ttl']:
            return 'expired'
        
        # Check for thermal decay
        if (sigil['heat_exposure'] > self.decay_threshold['heat'] and 
            sigil['saturation'] < self.decay_threshold['saturation']):
            # Check if operator reinforcement can prevent decay
            if (sigil['operator_reinforced'] and 
                system_entropy < self.preservation_entropy_limit):
                return 'preserved'
            else:
                return 'decayed'
        
        # Check for operator preservation
        if (sigil['operator_reinforced'] and 
            system_entropy < self.preservation_entropy_limit):
            return 'preserved'
        
        # Sigil remains active (not categorized in output)
        return 'active'
    
    def _log_event(self, event_type: str, sigil: Dict, tick: int, reason: str):
        """Log a sigil lifecycle event."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tick": tick,
            "event": event_type,
            "sigil_id": sigil['sigil_id'],
            "convolution_level": sigil['convolution_level'],
            "saturation": sigil['saturation'],
            "heat_exposure": sigil['heat_exposure'],
            "age": tick - sigil['creation_tick'],
            "ttl": sigil['ttl'],
            "operator_reinforced": sigil['operator_reinforced'],
            "reason": reason
        }
        self.logger.info(json.dumps(log_entry))
    
    def get_sigil_health_metrics(self, active_sigils: List[Dict], 
                                current_tick: int) -> Dict:
        """Calculate health metrics for all active sigils."""
        if not active_sigils:
            return {
                "total_sigils": 0,
                "avg_saturation": 0.0,
                "avg_heat_exposure": 0.0,
                "reinforced_count": 0,
                "at_risk_count": 0
            }
        
        total = len(active_sigils)
        avg_saturation = sum(s['saturation'] for s in active_sigils) / total
        avg_heat = sum(s['heat_exposure'] for s in active_sigils) / total
        reinforced = sum(1 for s in active_sigils if s['operator_reinforced'])
        
        # Count sigils at risk of decay or expiry
        at_risk = 0
        for sigil in active_sigils:
            age_ratio = (current_tick - sigil['creation_tick']) / sigil['ttl']
            thermal_risk = (sigil['heat_exposure'] > 0.6 and sigil['saturation'] < 0.6)
            if age_ratio > 0.8 or thermal_risk:
                at_risk += 1
        
        return {
            "total_sigils": total,
            "avg_saturation": round(avg_saturation, 3),
            "avg_heat_exposure": round(avg_heat, 3),
            "reinforced_count": reinforced,
            "at_risk_count": at_risk
        }


# Example usage
if __name__ == "__main__":
    manager = SigilLifecycleManager()
    
    # Test sigils
    test_sigils = [
        {
            "sigil_id": "sig_001",
            "convolution_level": 0.7,
            "saturation": 0.3,
            "creation_tick": 100,
            "ttl": 50,
            "heat_exposure": 0.9,
            "operator_reinforced": False
        },
        {
            "sigil_id": "sig_002",
            "convolution_level": 0.8,
            "saturation": 0.4,
            "creation_tick": 120,
            "ttl": 100,
            "heat_exposure": 0.85,
            "operator_reinforced": True
        },
        {
            "sigil_id": "sig_003",
            "convolution_level": 0.6,
            "saturation": 0.7,
            "creation_tick": 140,
            "ttl": 80,
            "heat_exposure": 0.5,
            "operator_reinforced": False
        }
    ]
    
    # Evaluate lifecycle
    result = manager.evaluate_sigil_lifecycle(test_sigils, current_tick=180, system_entropy=0.4)
    print(json.dumps(result, indent=2))
    
    # Get health metrics
    metrics = manager.get_sigil_health_metrics(test_sigils, current_tick=180)
    print("\nSigil Health Metrics:")
    print(json.dumps(metrics, indent=2))