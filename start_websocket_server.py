#!/usr/bin/env python3
"""
Launcher script for the Advanced Consciousness WebSocket Server
"""

import os
import sys
import asyncio
import uvicorn
from backend.main import app

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the server
if __name__ == "__main__":
    print("Starting Advanced Consciousness WebSocket Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 