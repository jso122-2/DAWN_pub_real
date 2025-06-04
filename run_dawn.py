#!/usr/bin/env python3
"""
🌅 DAWN Launcher Script
Quick launcher for the interactive DAWN testing environment
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dawn_interactive_runner import run_interactive_dawn
    
    # Run DAWN with interactive commands
    run_interactive_dawn()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure these files are in the same directory:")
    print("  - main.py (with DAWNGenomeConsciousnessWrapper)")
    print("  - dawn_command_interface.py")
    print("  - dawn_interactive_runner.py")
    print("  - run_dawn.py (this file)")
    print("\nNote: Your DAWN uses DAWNGenomeConsciousnessWrapper, not DawnSchema")
except KeyboardInterrupt:
    print("\n👋 Goodbye!")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()