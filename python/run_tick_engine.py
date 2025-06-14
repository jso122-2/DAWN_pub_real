#!/usr/bin/env python3
"""
Run the DAWN Tick Engine with WebSocket API and Owl Integration
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('dawn_tick_engine.log')
        ]
    )

def main():
    """Main entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🦉 Starting DAWN Tick Engine with Owl Integration")
    logger.info("=" * 60)
    
    try:
        # Import and run the API server
        import uvicorn
        from api.websocket_server import app
        
        logger.info("🚀 Launching FastAPI server with WebSocket support")
        logger.info("📡 Main WebSocket: ws://localhost:8000/ws")
        logger.info("🦉 Owl WebSocket: ws://localhost:8000/owl")
        logger.info("🔗 API Docs: http://localhost:8000/docs")
        logger.info("💓 Health Check: http://localhost:8000/health")
        
        # Run the FastAPI app with Uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down DAWN Tick Engine")
    except Exception as e:
        logger.error(f"❌ Failed to start tick engine: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 