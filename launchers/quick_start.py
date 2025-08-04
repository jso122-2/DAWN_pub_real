# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
🧠⚡ DAWN Quick Start - Interactive Launcher
Simple interactive interface for launching DAWN's cognitive system
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print the DAWN quick start banner"""
    print("""
🧠⚡ DAWN QUICK START ⚡🧠
================================
Interactive Cognitive System Launcher
""")

def print_launch_options():
    """Display available launch options"""
    print("""
🚀 Launch Options:

1. 🎭 Full Demo        - Complete system with GUI, voice, tracers
2. 🖥️  Development     - GUI + tracers, no voice (quiet coding)
3. 🏭 Production       - Stable system, auto-snapshots
4. 🔇 Headless         - Server mode, no GUI or voice
5. 🧪 Testing          - Minimal components for testing
6. 🔬 Research         - Maximum data collection
7. 🎤 Voice Demo       - Focus on TTS and voice modulation
8. 🧬 Semantic         - Memory network and pattern analysis

9. 📊 System Status    - Check running processes
10. 🛑 Stop All        - Stop all DAWN processes
11. 🧹 Fresh Reset     - Clean state and restart

0. ❌ Exit
""")

def get_user_choice():
    """Get user's launch choice"""
    while True:
        try:
            choice = input("Select launch option (0-11): ").strip()
            if choice.isdigit() and 0 <= int(choice) <= 11:
                return int(choice)
            else:
                print("❌ Please enter a number between 0 and 11")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)

def launch_dawn(profile: str, extra_args: list = None):
    """Launch DAWN with the specified profile"""
    if extra_args is None:
        extra_args = []
    
    cmd = ["python", "dawn_launcher.py"] + extra_args
    
    print(f"🚀 Launching DAWN with {profile} profile...")
    print(f"📝 Command: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        # Run the launcher
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Launch interrupted by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Launch failed with exit code {e.returncode}")
    except FileNotFoundError:
        print("❌ dawn_launcher.py not found. Make sure you're in the correct directory.")

def check_prerequisites():
    """Check if required files exist"""
    required_files = [
        "dawn_launcher.py",
        "demo_reset.py",
        "voice_mood_modulation.py",
        "SymbolicTraceComposer.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("⚠️  Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all DAWN components are properly installed.")
        return False
    
    return True

def show_status():
    """Show current system status"""
    try:
        subprocess.run(["python", "dawn_launcher.py", "--status"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to get system status")
    except FileNotFoundError:
        print("❌ dawn_launcher.py not found")

def stop_all():
    """Stop all DAWN processes"""
    try:
        subprocess.run(["python", "dawn_launcher.py", "--stop"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to stop processes")

def fresh_reset():
    """Perform fresh reset and restart"""
    try:
        print("🧹 Performing fresh reset...")
        subprocess.run(["python", "demo_reset.py", "--silent"], check=True)
        print("✅ Fresh reset complete!")
        
        # Ask if user wants to launch after reset
        choice = input("\n🚀 Launch DAWN after reset? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            launch_dawn("Demo", ["--gui", "--voice", "--tracers", "--fresh"])
    except subprocess.CalledProcessError:
        print("❌ Fresh reset failed")

def main():
    """Main quick start interface"""
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install missing components.")
        return
    
    print("✅ All components found!")
    
    while True:
        print_launch_options()
        choice = get_user_choice()
        
        if choice == 0:
            print("👋 Goodbye!")
            break
        elif choice == 1:  # Full Demo
            launch_dawn("Demo", ["--gui", "--voice", "--tracers", "--log"])
        elif choice == 2:  # Development
            launch_dawn("Development", ["--gui", "--tracers", "--mute", "--verbose"])
        elif choice == 3:  # Production
            launch_dawn("Production", ["--voice", "--tracers", "--auto-snapshot"])
        elif choice == 4:  # Headless
            launch_dawn("Headless", ["--headless", "--mute", "--tracers", "--auto-snapshot"])
        elif choice == 5:  # Testing
            launch_dawn("Testing", ["--headless", "--mute", "--fresh"])
        elif choice == 6:  # Research
            launch_dawn("Research", ["--gui", "--voice", "--tracers", "--auto-snapshot", "--verbose", "--log"])
        elif choice == 7:  # Voice Demo
            launch_dawn("Voice Demo", ["--gui", "--voice", "--tracers"])
        elif choice == 8:  # Semantic
            launch_dawn("Semantic", ["--gui", "--mute", "--tracers", "--auto-snapshot"])
        elif choice == 9:  # Status
            show_status()
        elif choice == 10:  # Stop All
            stop_all()
        elif choice == 11:  # Fresh Reset
            fresh_reset()
        
        if choice in [1, 2, 3, 4, 5, 6, 7, 8]:
            # After launching, ask if user wants to do something else
            print("\n" + "=" * 50)
            continue_choice = input("Press Enter to return to menu, or 'q' to quit: ").strip().lower()
            if continue_choice == 'q':
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please check that all DAWN components are properly installed.") 