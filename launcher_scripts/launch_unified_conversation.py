#!/usr/bin/env python3
"""
DAWN Unified Conversation Launcher
==================================

Easy launcher for the DAWN Unified Conversation Interface with various
configuration options and mode presets.
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Launch the unified conversation interface"""
    
    parser = argparse.ArgumentParser(
        description="DAWN Unified Conversation Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_unified_conversation.py                    # Default casual mode
  python launch_unified_conversation.py --philosophical    # Deep consciousness exploration
  python launch_unified_conversation.py --technical        # System analysis mode
  python launch_unified_conversation.py --demo             # Showcase DAWN's capabilities
  python launch_unified_conversation.py --voice            # Enable voice synthesis
  python launch_unified_conversation.py --no-voice         # Text-only mode
        """
    )
    
    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--philosophical", action="store_true", 
                           help="Start in philosophical mode for deep consciousness exploration")
    mode_group.add_argument("--casual", action="store_true", 
                           help="Start in casual mode for natural conversation (default)")
    mode_group.add_argument("--technical", action="store_true", 
                           help="Start in technical mode for system analysis")
    mode_group.add_argument("--reflection", action="store_true", 
                           help="Start in reflection mode for introspection")
    mode_group.add_argument("--demo", action="store_true", 
                           help="Start in demo mode to showcase DAWN's capabilities")
    
    # Voice options
    voice_group = parser.add_mutually_exclusive_group()
    voice_group.add_argument("--voice", action="store_true", 
                            help="Enable voice synthesis")
    voice_group.add_argument("--no-voice", action="store_true", 
                            help="Disable voice synthesis (text-only)")
    
    # Additional options
    parser.add_argument("--session-file", type=str, 
                       help="Load conversation from session file")
    parser.add_argument("--auto-save", action="store_true", 
                       help="Automatically save session on exit")
    parser.add_argument("--quiet", action="store_true", 
                       help="Reduce output verbosity")
    
    args = parser.parse_args()
    
    # Determine mode
    mode = "casual"  # default
    if args.philosophical:
        mode = "philosophical"
    elif args.technical:
        mode = "technical"
    elif args.reflection:
        mode = "reflection"
    elif args.demo:
        mode = "demo"
    
    # Determine voice setting
    voice_enabled = True  # default
    if args.no_voice:
        voice_enabled = False
    elif args.voice:
        voice_enabled = True
    
    # Build command
    cmd = [sys.executable, "unified_conversation.py", "--mode", mode]
    
    if not voice_enabled:
        cmd.append("--no-voice")
    elif args.voice:
        cmd.append("--voice")
    
    # Display launch information
    print("🚀 DAWN Unified Conversation Launcher")
    print("=" * 50)
    print(f"Mode: {mode}")
    print(f"Voice: {'Enabled' if voice_enabled else 'Disabled'}")
    if args.session_file:
        print(f"Session: Loading from {args.session_file}")
    print()
    
    # Launch the unified conversation interface
    try:
        import subprocess
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Launch interrupted by user")
    except Exception as e:
        print(f"❌ Launch error: {e}")
        print("Try running: python unified_conversation.py --help")

if __name__ == "__main__":
    main() 