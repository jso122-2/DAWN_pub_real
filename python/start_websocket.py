#!/usr/bin/env python3
"""
Simple WebSocket server startup script for DAWN consciousness data
"""

import asyncio
import logging
from websocket_consciousness_server import ConsciousnessWebSocketServer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """Start the WebSocket server"""
    print("🧠 Starting DAWN Consciousness WebSocket Server...")
    print("   Server will run on: ws://localhost:8001")
    print("   Press Ctrl+C to stop\n")
    
    server = ConsciousnessWebSocketServer(host='localhost', port=8001)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        logger.error(f"Server error: {e}")

if __name__ == '__main__':
    asyncio.run(main()) 