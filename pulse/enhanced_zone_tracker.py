"""
Enhanced Zone Tracker - Integrates with SCUP system for animation
"""

import logging
import time
import pandas as pd
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class ZoneState:
    """Represents a zone state with heat and metadata"""
    name: str
    heat: float
    timestamp: datetime
    scup_value: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "heat": self.heat,
            "timestamp": self.timestamp.isoformat(),
            "scup_value": self.scup_value
        }

class EnhancedZoneTracker:
    """Enhanced zone tracker that integrates with SCUP system"""
    
    def __init__(self, output_dir: str = "visual/outputs/scup_zone_animator"):
        self.active = False
        self.current_zone = "calm"
        self.zone_history: List[ZoneState] = []
        self.scup_history: List[float] = []
        self.output_dir = output_dir
        self.zone_labels = {"calm": "green", "active": "gold", "surge": "red"}
        self.zone_names = ["calm", "active", "surge"]
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("Enhanced Zone Tracker initialized")
        
    def wire(self, orchestrator):
        """Wire into the system"""
        self.event_bus = orchestrator.event_bus
        self.scup_tracker = orchestrator.scup_tracker
        self.active = True
        logger.info("Enhanced Zone tracker wired")
        
    def determine_zone(self, scup_value: float, heat: float = None) -> str:
        """Determine current zone based on SCUP value and heat"""
        if heat is None:
            heat = np.random.random()  # Fallback heat value
            
        # Zone determination logic
        if scup_value < 0.3:
            return "calm"
        elif scup_value < 0.7:
            return "active"
        else:
            return "surge"
            
    def update(self, scup_value: float, heat: float = None) -> None:
        """Update zone state with current SCUP and heat values"""
        if not self.active:
            return
            
        try:
            current_time = datetime.now()
            zone = self.determine_zone(scup_value, heat)
            
            # Create zone state
            zone_state = ZoneState(
                name=zone,
                heat=heat or np.random.random(),
                timestamp=current_time,
                scup_value=scup_value
            )
            
            # Update current state
            self.current_zone = zone
            self.zone_history.append(zone_state)
            self.scup_history.append(scup_value)
            
            # Keep history manageable (last 1000 entries)
            if len(self.zone_history) > 1000:
                self.zone_history = self.zone_history[-1000:]
                self.scup_history = self.scup_history[-1000:]
                
            logger.debug(f"Zone updated: {zone} (SCUP: {scup_value:.3f}, Heat: {heat:.3f})")
            
        except Exception as e:
            logger.error(f"Error updating zone: {e}")
            
    def export_data_for_animation(self) -> Dict[str, str]:
        """Export data in format expected by the animator"""
        try:
            if not self.zone_history:
                logger.warning("No zone history to export")
                return {}
                
            # Create SCUP log
            scup_data = []
            for i, (zone_state, scup_value) in enumerate(zip(self.zone_history, self.scup_history)):
                scup_data.append({
                    "timestamp": zone_state.timestamp,
                    "scup": scup_value
                })
            
            scup_df = pd.DataFrame(scup_data)
            scup_log_path = os.path.join(self.output_dir, "scup_bloom_correlation.csv")
            scup_df.to_csv(scup_log_path, index=False)
            
            # Create zone log
            zone_data = []
            for i, zone_state in enumerate(self.zone_history):
                zone_data.append({
                    "tick": i,
                    "zone": zone_state.name,
                    "heat": zone_state.heat
                })
            
            zone_df = pd.DataFrame(zone_data)
            zone_log_path = os.path.join(self.output_dir, "zone_overlay_log.csv")
            zone_df.to_csv(zone_log_path, index=False, header=False)
            
            logger.info(f"Exported animation data: {len(scup_data)} records")
            return {
                "scup_log": scup_log_path,
                "zone_log": zone_log_path
            }
            
        except Exception as e:
            logger.error(f"Error exporting animation data: {e}")
            return {}
            
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "active": self.active,
            "current_zone": self.current_zone,
            "history_size": len(self.zone_history),
            "scup_history_size": len(self.scup_history),
            "last_scup": self.scup_history[-1] if self.scup_history else None,
            "zone_labels": self.zone_labels
        }
        
    def get_recent_data(self, count: int = 50) -> Dict[str, Any]:
        """Get recent zone and SCUP data"""
        if not self.zone_history:
            return {"zones": [], "scup": []}
            
        recent_zones = self.zone_history[-count:]
        recent_scup = self.scup_history[-count:]
        
        return {
            "zones": [zone.to_dict() for zone in recent_zones],
            "scup": recent_scup
        }
        
    def shutdown(self):
        """Shutdown the tracker"""
        self.active = False
        self.zone_history.clear()
        self.scup_history.clear()
        logger.info("Enhanced Zone tracker shut down")

# Global instance
_enhanced_zone_tracker = EnhancedZoneTracker()

def get_enhanced_zone_tracker() -> EnhancedZoneTracker:
    """Get the global enhanced zone tracker instance"""
    return _enhanced_zone_tracker 