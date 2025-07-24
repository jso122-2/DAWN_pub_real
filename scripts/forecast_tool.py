#!/usr/bin/env python3
"""
DAWN Forecast Tool Launcher
Simple launcher for the DAWN forecasting CLI tool.
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import and run the forecast tool
from cognitive.forecast_tool import main

if __name__ == "__main__":
    main() 