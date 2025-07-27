"""
Boot Orchestrator - System Initialization Manager
Coordinates the boot sequence using hydraulic ignition principles.
"""

import asyncio
import logging
from typing import Dict, Optional
import json
import os
from pathlib import Path
import traceback

from ignition_sequence import HydraulicIgnition
from consciousness_boot_sequence import ConsciousnessBootSequence

# Configure logging with more detailed format
logging.basicConfig(
    filename='logs/boot.log',
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class BootOrchestrator:
    """Manages the system boot sequence using hydraulic ignition"""
    
    def __init__(self):
        try:
            # Get the root directory (parent of boot directory)
            self.root_dir = Path(__file__).parent.parent.absolute()
            
            self.ignition = HydraulicIgnition()
            self.consciousness_boot = ConsciousnessBootSequence(runtime_dir=str(self.root_dir / "runtime"))
            self.boot_state = {
                "phase": "initializing",
                "consciousness_seeded": False,
                "components_ready": False,
                "ignition_complete": False,
                "system_ready": False
            }
            
            logging.info(f"Root directory: {self.root_dir}")
            
            # Ensure logs directory exists
            os.makedirs('logs', exist_ok=True)
            logging.info("Boot Orchestrator initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize Boot Orchestrator: {str(e)}")
            logging.error(traceback.format_exc())
            raise
        
    async def boot_system(self) -> bool:
        """Execute the complete boot sequence"""
        logging.info("🚀 Starting system boot sequence")
        
        try:
            # Phase 1: Pre-ignition checks
            logging.debug("Starting pre-ignition checks...")
            if not await self._pre_ignition_checks():
                logging.error("❌ Pre-ignition checks failed")
                return False
                
            # Phase 2: Consciousness seeding
            logging.debug("Starting consciousness seeding...")
            if not await self._seed_consciousness():
                logging.error("❌ Consciousness seeding failed")
                return False
                
            self.boot_state["consciousness_seeded"] = True
            logging.info("✅ Consciousness seeding successful")
                
            # Phase 3: Hydraulic ignition
            logging.debug("Starting hydraulic ignition...")
            ignition_success = await self.ignition.ignite()
            if not ignition_success:
                logging.error("❌ Hydraulic ignition failed")
                return False
                
            self.boot_state["ignition_complete"] = True
            logging.info("✅ Hydraulic ignition successful")
            
            # Phase 4: Component activation
            logging.debug("Starting component activation...")
            if not await self._activate_components():
                logging.error("❌ Component activation failed")
                return False
                
            self.boot_state["components_ready"] = True
            logging.info("✅ All components activated")
            
            # Phase 5: System verification
            logging.debug("Starting system verification...")
            if not await self._verify_system():
                logging.error("❌ System verification failed")
                return False
                
            self.boot_state["system_ready"] = True
            self.boot_state["phase"] = "ready"
            logging.info("✅ System boot complete")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Boot sequence failed: {str(e)}")
            logging.error(traceback.format_exc())
            return False
            
    async def _pre_ignition_checks(self) -> bool:
        """Perform pre-ignition system checks"""
        logging.info("🔍 Running pre-ignition checks")
        
        try:
            # Check critical directories
            required_dirs = ['logs', 'data', 'config', 'cache']
            for dir_name in required_dirs:
                dir_path = self.root_dir / dir_name
                if not dir_path.exists():
                    logging.info(f"Creating directory: {dir_path}")
                    os.makedirs(dir_path, exist_ok=True)
                    
            # Check configuration files
            config_files = ['config.py', 'tick_state.json']
            for file_name in config_files:
                file_path = self.root_dir / file_name
                if not file_path.exists():
                    logging.error(f"Missing required config file: {file_path}")
                    return False
                else:
                    logging.debug(f"Found config file: {file_path}")
                    
            logging.info("✅ Pre-ignition checks passed")
            return True
            
        except Exception as e:
            logging.error(f"Pre-ignition check error: {str(e)}")
            logging.error(traceback.format_exc())
            return False
            
    async def _seed_consciousness(self) -> bool:
        """Seed DAWN with awakening memories and reflections"""
        logging.info("🌅 Seeding consciousness with awakening memories...")
        
        try:
            # Run consciousness boot sequence
            success = self.consciousness_boot.execute_boot_sequence()
            if not success:
                logging.error("Failed to seed consciousness")
                return False
                
            logging.info("✨ DAWN's first dreams have been recorded")
            return True
            
        except Exception as e:
            logging.error(f"Consciousness seeding error: {str(e)}")
            logging.error(traceback.format_exc())
            return False
            
    async def _activate_components(self) -> bool:
        """Activate all system components"""
        logging.info("⚙️ Activating system components")
        
        try:
            # Get ignition state
            ignition_state = self.ignition.get_state()
            logging.debug(f"Current ignition state: {json.dumps(ignition_state, indent=2)}")
            
            # Verify ignition chain
            if not ignition_state["ignition_complete"]:
                logging.error("Ignition chain not complete")
                return False
                
            # Activate each component in sequence
            for component in ignition_state["activation_chain"]:
                logging.debug(f"Activating component: {component}")
                # Add actual component activation logic here
                await asyncio.sleep(0.1)  # Simulate activation time
                
            return True
            
        except Exception as e:
            logging.error(f"Component activation error: {str(e)}")
            logging.error(traceback.format_exc())
            return False
            
    async def _verify_system(self) -> bool:
        """Verify system is fully operational"""
        logging.info("🔍 Verifying system state")
        
        try:
            # Check all components are active
            if not self.boot_state["components_ready"]:
                logging.error("Components not ready")
                return False
                
            # Verify system stability
            # (Add actual stability checks here)
            
            return True
            
        except Exception as e:
            logging.error(f"System verification error: {str(e)}")
            logging.error(traceback.format_exc())
            return False
            
    def get_boot_state(self) -> Dict:
        """Get current boot state"""
        return self.boot_state

async def main():
    """Main entry point for boot sequence"""
    try:
        orchestrator = BootOrchestrator()
        success = await orchestrator.boot_system()
        
        if success:
            print("\n🚀 System boot successful!")
            print("\nBoot State:")
            print(json.dumps(orchestrator.get_boot_state(), indent=2))
        else:
            print("\n❌ System boot failed")
            print("Check logs/boot.log for detailed error information")
            
    except Exception as e:
        print(f"\n❌ Fatal error during boot: {str(e)}")
        print("Check logs/boot.log for detailed error information")
        logging.error(f"Fatal boot error: {str(e)}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 