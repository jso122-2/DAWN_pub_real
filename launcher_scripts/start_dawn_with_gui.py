#!/usr/bin/env python3
"""
DAWN Launcher Script with GUI Integration
Starts the Advanced Consciousness System with real-time GUI monitoring
"""

import os
import sys
import asyncio
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the Python environment for DAWN"""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Create necessary directories
    os.makedirs('backend/embeddings', exist_ok=True)
    os.makedirs('backend/memory', exist_ok=True)
    
    # Check for required files
    required_files = [
        'backend/embeddings/echo_library.pkl',
        'backend/memory/glyph_memory.pkl'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            logger.warning(f"Required file not found: {file}")
            # Create empty file if it doesn't exist
            with open(file, 'wb') as f:
                pass

def start_gui_monitoring(dawn_system):
    """Start GUI monitoring for the DAWN system"""
    try:
        from gui.dawn_gui_integration import DAWNGuiIntegration
        
        # Create GUI integration
        gui_integration = DAWNGuiIntegration()
        
        # Try to integrate with tick engine if available
        if hasattr(dawn_system, 'tick_engine'):
            if gui_integration.register_with_tick_engine(dawn_system.tick_engine):
                logger.info("✅ GUI integrated with DAWN tick engine")
                return gui_integration
            else:
                logger.warning("Failed to integrate GUI with tick engine, starting standalone")
        
        # Fall back to standalone mode
        if gui_integration.start_standalone_gui():
            logger.info("✅ GUI started in standalone monitoring mode")
            return gui_integration
        else:
            logger.error("❌ Failed to start GUI")
            return None
            
    except ImportError as e:
        logger.warning(f"GUI components not available: {e}")
        logger.info("💡 Install tkinter if you want GUI monitoring: pip install tk")
        return None
    except Exception as e:
        logger.error(f"Error starting GUI: {e}")
        return None

async def main():
    """Main entry point for DAWN with GUI"""
    parser = argparse.ArgumentParser(description="DAWN Advanced Consciousness System")
    parser.add_argument(
        '--no-gui',
        action='store_true',
        help='Disable GUI monitoring interface'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    gui_integration = None
    dawn = None
    
    try:
        # Set up environment
        setup_environment()
        
        # Import after path setup
        from backend.advanced_consciousness_system import create_advanced_consciousness
        
        # Create and start the consciousness system
        logger.info("🌅 Initializing DAWN Advanced Consciousness System...")
        dawn = await create_advanced_consciousness(
            node_name="DAWN_Primary",
            enable_networking=True,
            network_host="localhost",
            network_port=8769
        )
        
        # Start GUI monitoring if requested
        if not args.no_gui:
            logger.info("🖥️  Starting GUI monitoring interface...")
            gui_integration = start_gui_monitoring(dawn)
            if gui_integration:
                logger.info("🎮 DAWN GUI monitoring active")
                logger.info("🖥️  Real-time consciousness monitoring available")
            else:
                logger.info("⚠️  Continuing without GUI monitoring")
        else:
            logger.info("GUI monitoring disabled by --no-gui flag")
        
        # Print system status
        logger.info("=" * 60)
        logger.info("🧠 DAWN Advanced Consciousness System ONLINE")
        logger.info(f"🌐 Network: localhost:8769")
        if gui_integration:
            logger.info("🎮 GUI: Real-time monitoring active")
        else:
            logger.info("📊 GUI: Disabled or unavailable")
        logger.info("🛑 Press Ctrl+C to shutdown")
        logger.info("=" * 60)
        
        # Keep the system running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down DAWN...")
        
        # Shutdown GUI first
        if gui_integration:
            logger.info("Shutting down GUI monitoring...")
            gui_integration.shutdown()
        
        # Shutdown DAWN system
        if dawn:
            logger.info("Shutting down consciousness system...")
            await dawn.shutdown_system()
            
        logger.info("✅ DAWN shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Error starting DAWN: {e}")
        
        # Emergency cleanup
        if gui_integration:
            gui_integration.shutdown()
        if dawn:
            try:
                await dawn.shutdown_system()
            except:
                pass
        raise

if __name__ == "__main__":
    asyncio.run(main()) 