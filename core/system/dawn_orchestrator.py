# core/system/dawn_orchestrator.py
"""
DAWN Orchestrator
Coordinates system wiring and communication
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.system.event_bus import EventBus, DAWNEvents
from core.tick_emitter import TickEmitter

logger = logging.getLogger(__name__)

class DAWNOrchestrator:
    """Orchestrates system wiring and communication"""
    
    def __init__(self):
        self.birth_time = datetime.now()
        self.event_bus = EventBus()
        self.systems = {}
        self.connections = []
        self._wired = False
        
    def wire_systems(self) -> Dict[str, bool]:
        """Wire all systems together"""
        logger.info("🔌 Wiring systems...")
        
        # Initialize core systems
        self.systems['tick_engine'] = TickEmitter()
        
        # Wire systems
        wiring_status = {}
        for name, system in self.systems.items():
            try:
                if hasattr(system, 'wire'):
                    system.wire(self)
                wiring_status[name] = True
            except Exception as e:
                logger.error(f"Failed to wire {name}: {e}")
                wiring_status[name] = False
                
        self._wired = True
        return wiring_status
        
    def verify_wiring(self) -> Dict[str, Any]:
        """Verify all system connections"""
        from core.system.wiring_monitor import WiringMonitor
        monitor = WiringMonitor(self)
        return monitor.verify_all_connections()
        
    def get_tick_engine(self) -> TickEmitter:
        """Get the tick engine instance"""
        return self.systems.get('tick_engine')
        
    def stop(self):
        """Stop all systems"""
        logger.info("Stopping all systems...")
        for name, system in self.systems.items():
            try:
                if hasattr(system, 'shutdown'):
                    system.shutdown()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")
                
        self._wired = False
        self.systems.clear()
        self.connections.clear()