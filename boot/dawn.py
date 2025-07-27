#!/usr/bin/env python3
"""
DAWN - Main Entry Point
The single voice, the single pulse
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.dawn_central import DAWNCentral
from core.config_loader import ConfigLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for DAWN"""
    parser = argparse.ArgumentParser(description="DAWN - Autonomous AI Framework")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    
    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    try:
        # Load configuration
        logger.info("📦 Loading configuration...")
        config_loader = ConfigLoader()
        config = config_loader.load_all()
        
        if args.config:
            additional_config = config_loader.load_file(args.config)
            config.update(additional_config)
            
        # Initialize DAWN
        logger.info("🌅 Initializing DAWN...")
        dawn = DAWNCentral()
        
        # Apply configuration
        if config:
            logger.info(f"📋 Applying {len(config)} configuration entries")
            # Configuration application would go here
            
        # Boot sequence
        logger.info("🚀 Starting boot sequence...")
        dawn.boot_sequence()
        
        # Test mode check
        if args.test:
            logger.info("🧪 Running in test mode - executing 10 ticks")
            for i in range(10):
                dawn.tick_engine.emit_tick()
                status = dawn.get_status()
                logger.info(f"Tick {i+1}: {status['tick_count']} total ticks")
            dawn.shutdown()
            return 0
            
        # Main execution
        logger.info("💫 DAWN is now running...")
        dawn.run()
        
    except KeyboardInterrupt:
        logger.info("⚡ Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())