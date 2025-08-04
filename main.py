#!/usr/bin/env python3
"""
DAWN - Deep Learning Research
Main Entry Point

This is the primary entry point for the DAWN consciousness system.
It provides a unified interface to launch all components and subsystems.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for DAWN system"""
    parser = argparse.ArgumentParser(
        description="DAWN - Deep Learning Research Consciousness System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch default GUI mode
  python main.py --mode console     # Launch console mode
  python main.py --mode conversation # Launch conversation interface
  python main.py --mode visual      # Launch visual interface
  python main.py --mode demo        # Run demonstration mode
  python main.py --mode test        # Run system tests
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['gui', 'console', 'conversation', 'visual', 'demo', 'test'],
        default='gui',
        help='Launch mode (default: gui)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    print("🌅 DAWN - Deep Learning Research")
    print("=" * 50)
    print(f"🚀 Launching in {args.mode} mode...")
    
    try:
        if args.mode == 'gui':
            # Try the unified launcher first
            try:
                from launcher_scripts.launch_dawn_unified import main as launch_unified
                print("🎯 Using unified launcher...")
                launch_unified()
            except ImportError as e:
                print(f"⚠️ Unified launcher not available: {e}")
                # Fallback to other GUI options
                try:
                    from launcher_scripts.launch_dawn_gui import main as launch_gui
                    print("🎯 Using DAWN GUI launcher...")
                    launch_gui()
                except ImportError:
                    try:
                        from launcher_scripts.launch_local_gui import main as launch_local_gui
                        print("🎯 Using local GUI launcher...")
                        launch_local_gui()
                    except ImportError:
                        print("❌ No GUI launcher available, falling back to console mode")
                        from launcher_scripts.launch_dawn_unified import main as launch_console
                        launch_console()
                        
        elif args.mode == 'console':
            # Use the unified launcher for console mode
            try:
                from launcher_scripts.launch_dawn_unified import main as launch_console
                launch_console()
            except ImportError:
                try:
                    from launcher_scripts.start_dawn import main as start_dawn
                    start_dawn()
                except ImportError:
                    print("❌ No console launcher available")
                    sys.exit(1)
                    
        elif args.mode == 'conversation':
            # Try conversation interfaces
            try:
                from conversation.cli_dawn_conversation import main as launch_conversation
                # Clear sys.argv to avoid passing --mode to the conversation script
                original_argv = sys.argv.copy()
                sys.argv = [sys.argv[0]]  # Keep only the script name
                try:
                    launch_conversation()
                finally:
                    sys.argv = original_argv  # Restore original argv
            except ImportError:
                try:
                    from launcher_scripts.launch_dawn_conversation import main as launch_conv
                    launch_conv()
                except ImportError:
                    try:
                        from launcher_scripts.activate_enhanced_conversation import main as activate_conv
                        activate_conv()
                    except ImportError:
                        print("❌ No conversation interface available")
                        sys.exit(1)
                        
        elif args.mode == 'visual':
            # Try visual interfaces
            try:
                from visual.dawn_visual_gui import main as launch_visual
                launch_visual()
            except ImportError:
                try:
                    from launcher_scripts.launch_dawn_visual_journal import main as launch_visual_journal
                    launch_visual_journal()
                except ImportError:
                    try:
                        from launcher_scripts.launch_enhanced_dawn_gui import main as launch_enhanced_gui
                        launch_enhanced_gui()
                    except ImportError:
                        print("❌ No visual interface available")
                        sys.exit(1)
                        
        elif args.mode == 'demo':
            # Try demo scripts
            try:
                from demos.complete_integration_demo import main as run_demo
                run_demo()
            except ImportError:
                try:
                    from demos.demo_unified_conversation import main as run_unified_demo
                    run_unified_demo()
                except ImportError:
                    try:
                        from launcher_scripts.launch_dynamic_language_demo import main as run_lang_demo
                        run_lang_demo()
                    except ImportError:
                        print("❌ No demo available")
                        sys.exit(1)
                        
        elif args.mode == 'test':
            # Try test suites
            try:
                # Check if there's a test system module
                test_modules = [
                    'tests.test_system',
                    'tests.test_conversation_system',
                    'tests.test_enhanced_conversation_system'
                ]
                
                for test_module in test_modules:
                    try:
                        module = __import__(test_module, fromlist=['main'])
                        if hasattr(module, 'main'):
                            module.main()
                            break
                    except ImportError:
                        continue
                else:
                    print("❌ No test suite available")
                    sys.exit(1)
                    
            except Exception as e:
                print(f"❌ Test execution failed: {e}")
                sys.exit(1)
        else:
            print(f"❌ Unknown mode: {args.mode}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed and modules are available")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Launch error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 