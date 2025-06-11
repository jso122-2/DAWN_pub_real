# core/dawn_central.py
"""
DAWN Central
The spine of the DAWN system - coordinates all major subsystems
"""

import logging
from datetime import datetime
from typing import Dict, Any

from core.system.dawn_orchestrator import DAWNOrchestrator
from core.system.event_bus import DAWNEvents

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DAWNCentral:
    """Central coordination point for all DAWN subsystems"""
    
    def __init__(self):
        logger.info("🌅 DAWN Central initializing...")
        
        # Use the production orchestrator and event bus
        self.orchestrator = DAWNOrchestrator()
        self.event_bus = self.orchestrator.event_bus  # Use orchestrator's bus
        
        # System state
        self.running = False
        self.tick_count = 0
        self.tick_engine = None  # Will be created by orchestrator
        
    def boot_sequence(self):
        """Initialize all subsystems in proper order"""
        logger.info("🔧 Starting DAWN boot sequence...")
        
        try:
            # Phase 1: Wire all systems using the orchestrator
            logger.info("Phase 1: System Wiring")
            wiring_status = self.orchestrator.wire_systems()
            
            # Check wiring status
            if not all(status for status in wiring_status.values() if isinstance(status, bool)):
                raise RuntimeError(f"System wiring failed: {wiring_status}")
            
            # Phase 2: Verify connections
            logger.info("Phase 2: Connection Verification")
            verification = self.orchestrator.verify_wiring()
            if not verification.get('overall_health', False):
                logger.warning("⚠️ Some connections may be unstable")
            
            # Phase 3: Subscribe to critical events
            logger.info("Phase 3: Event Subscriptions")
            self._setup_event_subscriptions()
            
            # Phase 4: Get tick engine from orchestrator
            logger.info("Phase 4: Initialize Tick Engine")
            self.tick_engine = self.orchestrator.get_tick_engine()
            
            logger.info("✅ DAWN boot sequence complete!")
            self.running = True
            
        except Exception as e:
            logger.error(f"❌ Boot sequence failed: {e}")
            raise
    
    def _setup_event_subscriptions(self):
        """Set up event subscriptions for system monitoring"""
        # Subscribe to critical system events
        self.event_bus.subscribe(DAWNEvents.SYSTEM_ERROR, self._on_system_error)
        self.event_bus.subscribe(DAWNEvents.BLOOM_SPAWNED, self._on_bloom_spawn)
        self.event_bus.subscribe(DAWNEvents.PULSE_CRITICAL, self._on_pulse_critical)
        self.event_bus.subscribe(DAWNEvents.OWL_INSIGHT, self._on_owl_insight)
        self.event_bus.subscribe(DAWNEvents.SIGIL_EMITTED, self._on_sigil_emit)
        
        # Subscribe to tick events for counting
        self.event_bus.subscribe(DAWNEvents.TICK_COMPLETE, self._on_tick_complete)
        
        logger.info("  ✓ Event subscriptions established")
        
    def _on_system_error(self, event):
        """Handle system errors"""
        logger.error(f"System error: {event.data}")
        
    def _on_bloom_spawn(self, event):
        """Handle bloom spawn events"""
        logger.debug(f"Bloom spawned: {event.data.get('seed_id', 'unknown')}")
        
    def _on_pulse_critical(self, event):
        """Handle critical pulse events"""
        logger.warning(f"Critical pulse event: {event.data}")
        
    def _on_owl_insight(self, event):
        """Handle owl insights"""
        logger.info(f"Owl insight: {event.data.get('insight', 'unknown')}")
        
    def _on_sigil_emit(self, event):
        """Handle sigil emissions"""
        logger.debug(f"Sigil emitted: {event.data.get('type', 'unknown')}")
        
    def _on_tick_complete(self, event):
        """Track tick completions"""
        self.tick_count = event.data.get('tick', self.tick_count + 1)
        
    def _should_shutdown(self) -> bool:
        """Check if system should shut down"""
        # Add shutdown conditions here
        return False
        
    def shutdown(self):
        """Graceful shutdown sequence"""
        logger.info("🌙 DAWN shutting down...")
        
        self.running = False
        
        # Use orchestrator's stop method
        self.orchestrator.stop()
        
        # Final event
        self.event_bus.publish(DAWNEvents.SYSTEM_SHUTDOWN, {
            'uptime': (datetime.now() - self.orchestrator.birth_time).total_seconds(),
            'total_ticks': self.tick_count,
            'timestamp': datetime.now()
        })
        
        logger.info("💤 DAWN shutdown complete. Sweet dreams...")
        
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        systems_status = {}
        
        # Get status of wired systems
        for name, system in self.orchestrator.systems.items():
            if hasattr(system, 'get_status'):
                systems_status[name] = system.get_status()
            elif hasattr(system, 'is_active'):
                systems_status[name] = system.is_active()
            else:
                systems_status[name] = system is not None
                
        return {
            "running": self.running,
            "tick_count": self.tick_count,
            "wired": self.orchestrator._wired,
            "birth_time": self.orchestrator.birth_time.isoformat(),
            "subsystems": systems_status,
            "event_bus_stats": self.event_bus.get_stats(),
            "connections": len(self.orchestrator.connections)
        }