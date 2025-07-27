import signal
import sys
import asyncio
import logging
from typing import List, Callable, Optional

logger = logging.getLogger("DAWN.ShutdownManager")

class ShutdownManager:
    """
    Manages graceful shutdown of DAWN subsystems.
    Handles OS signals and coordinates cleanup across components.
    """
    
    def __init__(self):
        self.shutdown_requested = False
        self.cleanup_hooks: List[Callable] = []
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """Register OS signal handlers"""
        signal.signal(signal.SIGINT, self._handle_shutdown)   # Ctrl+C
        signal.signal(signal.SIGTERM, self._handle_shutdown)  # kill
        
    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals"""
        if not self.shutdown_requested:  # Prevent multiple shutdowns
            self.shutdown_requested = True
            print("\n🛑 Shutdown signal received")
            print("🧹 Initiating graceful shutdown...")
            
    def register_cleanup(self, hook: Callable):
        """Register a cleanup function to be called during shutdown"""
        self.cleanup_hooks.append(hook)
        
    async def shutdown(self, dawn=None):
        """Execute all registered cleanup hooks"""
        print("\n🌙 DAWN Shutdown Sequence Initiated...")
        
        # Trigger visual goodbye if available
        if dawn and hasattr(dawn, 'visualizer'):
            try:
                dawn.visualizer.say("System shutting down. Safe dreams.")
            except Exception as e:
                logger.error(f"Error during visual shutdown: {e}")
                
        # Execute cleanup hooks
        for hook in self.cleanup_hooks:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook()
                else:
                    hook()
            except Exception as e:
                logger.error(f"Error during cleanup hook: {e}")
                
        print("✅ DAWN Shutdown Complete")
        sys.exit(0)
        
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self.shutdown_requested 