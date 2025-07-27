#!/usr/bin/env python3
"""
DAWN System Launcher - Unified Entry Point
Launch DAWN cognitive engine or GUI dashboard with simple commands.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def launch_core_engine():
    """Launch the DAWN core cognitive engine."""
    print("🧠 Launching DAWN Core Engine...")
    
    try:
        from dawn_core.main import create_dawn_engine
        engine = create_dawn_engine()
        engine.run()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure all DAWN modules are properly installed")
    except KeyboardInterrupt:
        print("\n⚠️ Engine shutdown requested")
    except Exception as e:
        print(f"❌ Engine error: {e}")


def launch_gui_dashboard():
    """Launch the DAWN GUI dashboard."""
    print("🖥️ Launching DAWN GUI Dashboard...")
    
    try:
        from dawn_core.gui.forecast_dashboard import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure tkinter and all DAWN modules are available")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")


def launch_unified_dashboard():
    """Launch the DAWN Unified Dashboard."""
    print("🌟 Launching DAWN Unified Dashboard...")
    
    try:
        from dawn_core.gui.dawn_gui_dashboard import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure tkinter and all DAWN modules are available")
    except Exception as e:
        print(f"❌ Unified Dashboard error: {e}")


def launch_unified_gui():
    """Launch the unified launcher GUI."""
    print("🌅 Launching DAWN Unified Launcher GUI...")
    
    try:
        from dawn_core.unified_launcher_gui import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure tkinter and all DAWN modules are available")
    except Exception as e:
        print(f"❌ Unified GUI error: {e}")


def launch_snapshot_tool():
    """Launch the snapshot creation tool."""
    print("📦 Launching DAWN Snapshot Tool...")
    
    try:
        from dawn_core.snapshot_exporter import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure all DAWN modules are available")
    except Exception as e:
        print(f"❌ Snapshot tool error: {e}")


def main():
    """Main launcher with command-line interface."""
    parser = argparse.ArgumentParser(
        description="DAWN System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py engine     # Start cognitive engine
  python launch.py gui        # Start GUI dashboard
  python launch.py dashboard  # Start unified dashboard (NEW!)
  python launch.py unified    # Start unified launcher GUI
  python launch.py snapshot   # Create system snapshot
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['engine', 'gui', 'dashboard', 'unified', 'snapshot'],
        help='Launch mode selection'
    )
    
    args = parser.parse_args()
    
    print("🌟 DAWN System Launcher")
    print("=" * 30)
    
    if args.mode == 'engine':
        launch_core_engine()
    elif args.mode == 'gui':
        launch_gui_dashboard()
    elif args.mode == 'dashboard':
        launch_unified_dashboard()
    elif args.mode == 'unified':
        launch_unified_gui()
    elif args.mode == 'snapshot':
        launch_snapshot_tool()
    
    print("\n🎯 DAWN System Launcher complete")


if __name__ == "__main__":
    main() 