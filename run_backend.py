#!/usr/bin/env python3
"""
Wrapper script to run the DAWN backend with correct Python path
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the main module
if __name__ == "__main__":
    from backend.main import dawn_central
    print("Backend initialized successfully!") 