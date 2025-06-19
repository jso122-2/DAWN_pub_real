"""
SCUP Zone Animator Service - Backend integration for SCUP zone animations
"""

import logging
import asyncio
import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# Add project root to path for imports
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import with correct path
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from visual.scup_zone_animator import animate_scup_zone, generate_synthetic_logs
except ImportError:
    # Try alternative import paths
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from visual.scup_zone_animator import animate_scup_zone, generate_synthetic_logs
    except ImportError:
        # Fallback: create minimal functions
        def animate_scup_zone():
            return "visual/outputs/scup_zone_animator/scup_zone_overlay.gif"
        
        def generate_synthetic_logs():
            pass

from pulse.enhanced_zone_tracker import EnhancedZoneTracker
import signal
import atexit

# Import GIF saver
try:
    from .gif_saver import setup_gif_saver
except ImportError:
    from gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

class SCUPZoneAnimatorService:
    """Service for managing SCUP zone animations in the backend"""
    
    def __init__(self):
        self.active = False
        self.zone_tracker = EnhancedZoneTracker()
        self.animation_task = None
        self.last_animation_path = None
        self.auto_animate = False
        self.animation_interval = 60  # seconds
        
    def wire(self, orchestrator):
        """Wire into the DAWN system"""
        self.orchestrator = orchestrator
        self.zone_tracker.wire(orchestrator)
        self.active = True
        logger.info("SCUP Zone Animator Service wired")
        
    async def start_auto_animation(self, interval: int = 60):
        """Start automatic animation generation"""
        if self.auto_animate:
            logger.warning("Auto animation already running")
            return
            
        self.auto_animate = True
        self.animation_interval = interval
        
        async def auto_animate_loop():
            while self.auto_animate and self.active:
                try:
                    await self.generate_animation()
                    await asyncio.sleep(interval)
                except Exception as e:
                    logger.error(f"Error in auto animation loop: {e}")
                    await asyncio.sleep(10)  # Shorter sleep on error
                    
        self.animation_task = asyncio.create_task(auto_animate_loop())
        logger.info(f"Started auto animation with {interval}s interval")
        
    async def stop_auto_animation(self):
        """Stop automatic animation generation"""
        self.auto_animate = False
        if self.animation_task:
            self.animation_task.cancel()
            try:
                await self.animation_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped auto animation")
        
    async def generate_animation(self) -> Optional[str]:
        """Generate a new SCUP zone animation"""
        try:
            if not self.active:
                logger.warning("Service not active, cannot generate animation")
                return None
                
            # Update zone tracker with current SCUP value
            current_scup = self.orchestrator.scup_tracker.get_scup()
            self.zone_tracker.update(current_scup)
            
            # Export data for animation
            export_paths = self.zone_tracker.export_data_for_animation()
            
            if not export_paths:
                logger.warning("No data exported, generating synthetic data")
                generate_synthetic_logs()
            
            # Generate animation
            animation_path = animate_scup_zone()
            self.last_animation_path = animation_path
            
            logger.info(f"Generated SCUP zone animation: {animation_path}")
            return animation_path
            
        except Exception as e:
            logger.error(f"Error generating animation: {e}")
            return None
            
    def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "active": self.active,
            "auto_animate": self.auto_animate,
            "animation_interval": self.animation_interval,
            "last_animation_path": self.last_animation_path,
            "zone_tracker_status": self.zone_tracker.get_status()
        }
        
    def get_recent_data(self, count: int = 50) -> Dict[str, Any]:
        """Get recent zone and SCUP data"""
        return self.zone_tracker.get_recent_data(count)
        
    async def shutdown(self):
        """Shutdown the service"""
        await self.stop_auto_animation()
        self.active = False
        self.zone_tracker.shutdown()
        logger.info("SCUP Zone Animator Service shut down")

# Global instance
_scup_zone_animator_service = SCUPZoneAnimatorService()

def get_scup_zone_animator_service() -> SCUPZoneAnimatorService:
    """Get the global SCUP zone animator service instance"""
    return _scup_zone_animator_service