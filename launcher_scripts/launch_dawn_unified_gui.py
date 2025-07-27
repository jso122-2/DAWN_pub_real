#!/usr/bin/env python3
"""
Quick Launcher for DAWN Unified GUI
Simple entry point for the unified launcher interface.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

if __name__ == "__main__":
    try:
        from dawn_core.unified_launcher_gui import main
        print("🌅 DAWN Unified Launcher")
        print("=" * 30)
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure all DAWN modules are available")
        print("\nAlternatively, try:")
        print("  python dawn_core/launch.py unified")
    except Exception as e:
        print(f"❌ Error: {e}") 