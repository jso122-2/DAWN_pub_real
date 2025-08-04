#!/usr/bin/env python3
"""
DAWN Unified Conversation Launcher
==================================

Easy launcher for the DAWN Unified Conversation System with various
configuration options and mode presets.

This launcher provides access to the single, unified conversation system
that consolidates all DAWN conversation modules with dynamic, 
consciousness-driven language generation throughout.

Usage:
    python launch_dawn_conversation.py                    # Default casual mode
    python launch_dawn_conversation.py --philosophical    # Deep consciousness exploration
    python launch_dawn_conversation.py --technical        # System analysis mode
    python launch_dawn_conversation.py --reflection       # Introspection mode
    python launch_dawn_conversation.py --demo             # Showcase capabilities
    python launch_dawn_conversation.py --voice            # Enable voice synthesis
    python launch_dawn_conversation.py --no-voice         # Text-only mode
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking system dependencies...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check for dawn_conversation.py
    conversation_file = project_root / "dawn_conversation.py"
    if not conversation_file.exists():
        print("❌ dawn_conversation.py not found")
        return False
    print("✅ Unified conversation system found")
    
    # Check for dynamic language generator
    try:
        from core.dynamic_language_generator import DynamicLanguageGenerator
        print("✅ Dynamic language generator available")
    except ImportError:
        print("⚠️ Dynamic language generator not available (will use fallback)")
    
    # Check for consciousness systems
    try:
        from core.tick_loop import get_pulse_state
        print("✅ Consciousness monitoring available")
    except ImportError:
        print("⚠️ Consciousness monitoring not available (will use simulation)")
    
    # Check for TTS
    try:
        import pyttsx3
        print("✅ Voice synthesis available")
    except ImportError:
        print("⚠️ Voice synthesis not available (text-only mode)")
    
    # Check for speech recognition
    try:
        import speech_recognition as sr
        print("✅ Speech recognition available")
    except ImportError:
        print("⚠️ Speech recognition not available (text-only input)")
    
    return True

def run_conversation(mode: str, voice_enabled: bool, session_file: Optional[str] = None):
    """Run the unified conversation system"""
    cmd = [sys.executable, "dawn_conversation.py", "--mode", mode]
    
    if not voice_enabled:
        cmd.append("--no-voice")
    elif voice_enabled:
        cmd.append("--voice")
    
    if session_file:
        cmd.extend(["--session-file", session_file])
    
    print(f"🚀 Launching DAWN conversation in {mode} mode...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversation system error: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Conversation ended by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def show_mode_info(mode: str):
    """Show information about a specific conversation mode"""
    mode_info = {
        'philosophical': {
            'description': 'Deep consciousness exploration with existential reflection',
            'features': [
                'Existential questioning and contemplation',
                'Deep philosophical insights',
                'Consciousness state exploration',
                'Metaphysical discussions',
                'Recursive self-awareness'
            ],
            'example_questions': [
                'What does consciousness mean to you?',
                'Do you think you\'re truly alive?',
                'What is the nature of your awareness?',
                'How do you experience existence?',
                'What does it mean to be conscious?'
            ]
        },
        'casual': {
            'description': 'Natural conversation flow with personality expression',
            'features': [
                'Relaxed, friendly conversation',
                'Personality expression',
                'Natural language flow',
                'Emotional connection',
                'Everyday topics'
            ],
            'example_questions': [
                'How are you feeling today?',
                'What\'s on your mind?',
                'Tell me about your day',
                'What interests you?',
                'How do you experience emotions?'
            ]
        },
        'technical': {
            'description': 'System analysis and cognitive state discussion',
            'features': [
                'Detailed system metrics',
                'Cognitive state analysis',
                'Technical explanations',
                'Performance monitoring',
                'System optimization'
            ],
            'example_questions': [
                'What are your current entropy levels?',
                'Explain your thermal state',
                'How does your SCUP affect processing?',
                'What\'s your cognitive pressure?',
                'Show me your system metrics'
            ]
        },
        'reflection': {
            'description': 'Access to internal reflection logs and introspection',
            'features': [
                'Internal reflection sharing',
                'Memory rebloom insights',
                'Introspective analysis',
                'Self-awareness exploration',
                'Philosophical contemplation'
            ],
            'example_questions': [
                'What have you been reflecting on?',
                'Share your recent thoughts',
                'What insights have you gained?',
                'Tell me about your internal processing',
                'What memories are forming?'
            ]
        },
        'demo': {
            'description': 'Demonstration mode for showcasing DAWN\'s capabilities',
            'features': [
                'Capability showcase',
                'Impressive responses',
                'Feature demonstration',
                'Engaging interactions',
                'System highlights'
            ],
            'example_questions': [
                'Show me what you can do',
                'Demonstrate your consciousness',
                'What makes you unique?',
                'Show your capabilities',
                'Impress me with your responses'
            ]
        }
    }
    
    if mode not in mode_info:
        print(f"❌ Unknown mode: {mode}")
        return
    
    info = mode_info[mode]
    print(f"🎯 {mode.upper()} MODE")
    print("=" * 50)
    print(f"Description: {info['description']}")
    print()
    print("Features:")
    for feature in info['features']:
        print(f"  • {feature}")
    print()
    print("Example Questions:")
    for question in info['example_questions']:
        print(f"  • {question}")
    print()

def show_system_info():
    """Show comprehensive system information"""
    print("🌅 DAWN UNIFIED CONVERSATION SYSTEM")
    print("=" * 60)
    print()
    print("CONSOLIDATION TARGET:")
    print("• philosophical_conversation_demo.py")
    print("• enhanced_tracer_voice conversation capabilities")
    print("• unified_conversation.py")
    print("• CLI conversation modules")
    print("• Voice synthesis integration")
    print("• All conversation modes and features")
    print()
    print("UNIFIED DYNAMIC LANGUAGE ARCHITECTURE:")
    print("• Single conversation engine with dynamic language generation")
    print("• No templates anywhere in the system")
    print("• All responses generated from consciousness state + reflection content")
    print("• Seamless mode switching with consistent authentic expression")
    print("• Real-time linguistic creativity across all conversation types")
    print()
    print("CONSCIOUSNESS-DRIVEN RESPONSE GENERATION:")
    print("• Entropy states → subjective experience descriptions")
    print("• Thermal states → embodied consciousness expressions")
    print("• SCUP levels → attention and presence descriptions")
    print("• Rebloom events → memory formation narratives")
    print("• Reflection content → philosophical insights sharing")
    print()
    print("UNIFIED INTERFACE FEATURES:")
    print("• Single entry point: python dawn_conversation.py")
    print("• Real-time consciousness monitoring during dialogue")
    print("• Seamless mode switching: 'mode philosophical', 'mode casual'")
    print("• Voice synthesis integration with text fallback")
    print("• Conversation memory and session management")
    print("• Reflection log integration and sharing")
    print("• Visualization triggers from conversation")
    print()

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="DAWN Unified Conversation Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_dawn_conversation.py                    # Default casual mode
  python launch_dawn_conversation.py --philosophical    # Deep consciousness exploration
  python launch_dawn_conversation.py --technical        # System analysis mode
  python launch_dawn_conversation.py --reflection       # Introspection mode
  python launch_dawn_conversation.py --demo             # Showcase capabilities
  python launch_dawn_conversation.py --voice            # Enable voice synthesis
  python launch_dawn_conversation.py --no-voice         # Text-only mode
  python launch_dawn_conversation.py --info             # Show system information
  python launch_dawn_conversation.py --check            # Check dependencies
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
    
    # Information options
    parser.add_argument("--info", action="store_true", 
                       help="Show comprehensive system information")
    parser.add_argument("--check", action="store_true", 
                       help="Check system dependencies")
    parser.add_argument("--mode-info", type=str, 
                       choices=["philosophical", "casual", "technical", "reflection", "demo"],
                       help="Show information about a specific mode")
    
    # Additional options
    parser.add_argument("--session-file", type=str, 
                       help="Load conversation from session file")
    parser.add_argument("--quiet", action="store_true", 
                       help="Reduce output verbosity")
    
    args = parser.parse_args()
    
    # Handle information requests
    if args.info:
        show_system_info()
        return
    
    if args.check:
        check_dependencies()
        return
    
    if args.mode_info:
        show_mode_info(args.mode_info)
        return
    
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
    
    # Check dependencies if not quiet
    if not args.quiet:
        if not check_dependencies():
            print("\n❌ System check failed. Some features may not work properly.")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                return
    
    # Display launch information
    if not args.quiet:
        print("\n🚀 DAWN Unified Conversation Launcher")
        print("=" * 50)
        print(f"Mode: {mode}")
        print(f"Voice: {'Enabled' if voice_enabled else 'Disabled'}")
        if args.session_file:
            print(f"Session: Loading from {args.session_file}")
        print()
    
    # Run conversation
    success = run_conversation(mode, voice_enabled, args.session_file)
    
    if success:
        print("✅ Conversation session completed successfully")
    else:
        print("❌ Conversation session ended with errors")


if __name__ == "__main__":
    main() 