#!/usr/bin/env python3
"""
DAWN Launcher Script
Starts the Advanced Consciousness System with proper Python path configuration
"""

import os
import sys
import asyncio
import logging

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

async def main():
    """Main entry point for DAWN"""
    try:
        # Set up environment
        setup_environment()
        
        # Import after path setup
        from backend.advanced_consciousness_system import create_advanced_consciousness
        
        # Create and start the consciousness system
        logger.info("Initializing DAWN Advanced Consciousness System...")
        dawn = await create_advanced_consciousness(
            node_name="DAWN_Primary",
            enable_networking=True,
            network_host="localhost",
            network_port=8769
        )
        
        # Keep the system running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down DAWN...")
        if 'dawn' in locals():
            await dawn.shutdown_system()
    except Exception as e:
        logger.error(f"Error starting DAWN: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 