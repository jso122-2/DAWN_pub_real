#!/usr/bin/env python3
"""
DAWN Backend with Integrated Visualizations
Run script for the complete DAWN system with all visualizers
"""

import asyncio
import sys
import os
import signal
import logging
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from main import dawn_central, app
from fastapi import FastAPI
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point for DAWN with visualizations"""
    print("🌅 DAWN Backend with Integrated Visualizations")
    print("=" * 50)
    print("Starting integrated visualizations:")
    print("  • Mood State Visualizer (Emotional landscape heatmap)")
    print("  • Heat Monitor Visualizer (12-process radial gauges)")
    print("  • Entropy Flow Visualizer (12-process vector fields)")
    print("  • SCUP Pressure Grid Visualizer (4x4 cognitive pressure matrix)")
    print("  • Mood Entropy Phase Visualizer (3D phase space)")
    print("  • Drift State Transitions Visualizer (State evolution)")
    print("  • Bloom Genealogy Network Visualizer (Bloom relationship mapping)")
    print("  • Recursive Depth Explorer Visualizer (Cognitive depth analysis)")
    print("  • Semantic Flow Graph Visualizer (Semantic concept network)")
    print("  • Consciousness Constellation Visualizer (4D SCUP trajectory)")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
        server = uvicorn.Server(config)
        
        # Run the server
        await server.serve()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down DAWN...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        # Ensure clean shutdown
        if dawn_central:
            await dawn_central.shutdown()

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n🛑 Received shutdown signal...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the main async function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1) 