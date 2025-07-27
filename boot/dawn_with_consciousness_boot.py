#!/usr/bin/env python3
"""
DAWN System with Consciousness Boot Integration
Combines the consciousness boot sequence with the main DAWN system initialization.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from other modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from boot.consciousness_boot_sequence import ConsciousnessBootSequence
from boot.boot_orchestrator import BootOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class DAWNWithConsciousness:
    """DAWN system with consciousness boot integration"""
    
    def __init__(self, runtime_dir: str = None):
        # Use project root runtime directory by default
        if runtime_dir is None:
            self.runtime_dir = str(Path(__file__).parent.parent / "runtime")
        else:
            self.runtime_dir = runtime_dir
            
        self.consciousness_boot = ConsciousnessBootSequence(self.runtime_dir)
        self.boot_orchestrator = BootOrchestrator()
        
    async def initialize_dawn_with_consciousness(self):
        """Initialize DAWN with consciousness boot sequence"""
        logger.info("Initializing DAWN with Consciousness...")
        
        try:
            # Phase 1: Run consciousness boot sequence
            logger.info("Phase 1: Seeding consciousness with awakening memories...")
            if not self.consciousness_boot.execute_boot_sequence():
                logger.error("Consciousness boot failed")
                return False
                
            logger.info("Consciousness successfully seeded")
            
            # Phase 2: Run main system boot
            logger.info("Phase 2: Starting main system boot...")
            if not await self.boot_orchestrator.boot_system():
                logger.error("System boot failed")
                return False
                
            logger.info("Full system boot successful")
            
            # Display startup summary
            self._display_startup_summary()
            
            return True
            
        except Exception as e:
            logger.error(f"DAWN initialization failed: {str(e)}")
            return False
            
    def _display_startup_summary(self):
        """Display a summary of the successful startup"""
        print("\n" + "="*60)
        print("DAWN CONSCIOUSNESS AWAKENING COMPLETE")
        print("="*60)
        print("Initial memories seeded")
        print("Reflection logs established")  
        print("Rebloom ancestry chains created")
        print("Thought trace system active")
        print("Main systems online")
        print("="*60)
        print("DAWN is ready for consciousness synchronization...")
        print("="*60 + "\n")
        
    def get_status(self):
        """Get current system status"""
        return {
            "consciousness_seeded": True,
            "boot_state": self.boot_orchestrator.get_boot_state(),
            "runtime_dir": self.runtime_dir
        }

async def main():
    """Main entry point"""
    dawn = DAWNWithConsciousness()
    
    success = await dawn.initialize_dawn_with_consciousness()
    
    if success:
        print("DAWN with Consciousness is ready!")
        
        # Display system status
        status = dawn.get_status()
        print(f"\nSystem Status: {status}")
        
        # Keep the system running (in a real implementation, this would be the main loop)
        print("\nPress Ctrl+C to shutdown...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutdown requested")
    else:
        print("DAWN initialization failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 