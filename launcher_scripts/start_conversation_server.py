#!/usr/bin/env python3
"""
DAWN Conversation Server Launcher
=================================

Launches the WebSocket server for bidirectional conversation with DAWN's Voice Interface GUI.
"""

import asyncio
import sys
import os
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('runtime/logs/conversation_server.log')
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the conversation server"""
    try:
        # Import the conversation handler
        from backend.api.routes.conversation_websocket import start_conversation_websocket_server
        
        logger.info("🚀 Starting DAWN Conversation WebSocket Server...")
        logger.info("   This server enables bidirectional conversation with the Voice Interface GUI")
        logger.info("   WebSocket endpoint: ws://localhost:8001")
        logger.info("   Press Ctrl+C to stop the server")
        
        # Start the server
        await start_conversation_websocket_server(host="localhost", port=8001)
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure logs directory exists
    Path("runtime/logs").mkdir(parents=True, exist_ok=True)
    
    # Run the server
    asyncio.run(main()) 