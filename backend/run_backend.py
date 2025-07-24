#!/usr/bin/env python3
"""
Wrapper script to run the DAWN backend with correct Python path
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import and run the main module
if __name__ == "__main__":
    from backend.main import dawn_central
    print("Backend initialized successfully!") 