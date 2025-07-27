# pulse/zone_tracker.py
"""
Pulse Zone Tracker
Tracks pulse zones and transitions
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PulseZone:
    """Represents a pulse zone"""
    name: str
    temperature_range: tuple
    sigil_burn_rate: float
    
    def get_color_code(self) -> str:
        """Get ANSI color code for zone"""
        colors = {
            'DAWN': '\033[94m',  # Blue
            'PULSE': '\033[92m',  # Green
            'BLOOM': '\033[95m',  # Magenta
            'OWL': '\033[93m',    # Yellow
            'MOOD': '\033[91m'    # Red
        }
        return colors.get(self.name, '\033[0m')

class PulseZoneTracker:
    """Tracks pulse zones and transitions"""
    
    def __init__(self):
        self.active = False
        self.current_zone = None
        self.zone_history = []
        
    def wire(self, orchestrator):
        """Wire into the system"""
        self.event_bus = orchestrator.event_bus
        self.active = True
        logger.info("Zone tracker wired")
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "active": self.active,
            "current_zone": self.current_zone.name if self.current_zone else None,
            "history_size": len(self.zone_history)
        }
        
    def shutdown(self):
        """Shutdown the tracker"""
        self.active = False
        self.current_zone = None
        self.zone_history.clear()
        logger.info("Zone tracker shut down")
