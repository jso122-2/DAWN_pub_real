#!/usr/bin/env python3
"""
Launcher script for the Advanced Consciousness WebSocket Server
"""

import os
import sys
import asyncio

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the server
from backend.advanced_consciousness_websocket import main

if __name__ == "__main__":
    print("Starting Advanced Consciousness WebSocket Server...")
    asyncio.run(main()) 