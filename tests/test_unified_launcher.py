#!/usr/bin/env python3
"""
DAWN Unified Launcher Test Script
Demonstrates all available launch modes and features
"""

import subprocess
import sys
import time
import threading
from pathlib import Path

def run_command(cmd, description, timeout=10):
    """Run a command with timeout and return success status"""
    print(f"\n🧪 Testing: {description}")
    print(f"📋 Command: {' '.join(cmd)}")
    
    try:
        # Use timeout to prevent hanging
        result = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success!")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()[:200]}...")
        else:
            print(f"❌ Failed (exit code: {result.returncode})")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()[:200]}...")
                
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout after {timeout} seconds")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_unified_launcher():
    """Test the unified launcher system"""
    print("🌊 DAWN Unified Launcher Test Suite")
    print("=" * 60)
    
    # Check if launcher exists
    launcher_path = Path("dawn_unified_launcher.py")
    if not launcher_path.exists():
        print("❌ dawn_unified_launcher.py not found!")
        return False
    
    print("✅ Launcher file found")
    
    # Test basic functionality
    tests = [
        {
            'cmd': [sys.executable, 'dawn_unified_launcher.py', '--help'],
            'desc': 'Help display',
            'timeout': 5
        },
        {
            'cmd': [sys.executable, 'dawn_unified_launcher.py', '--check-deps'],
            'desc': 'Dependency check',
            'timeout': 10
        },
        {
            'cmd': [sys.executable, 'dawn_unified_launcher.py', '--components'],
            'desc': 'Component availability check',
            'timeout': 15
        }
    ]
    
    results = []
    
    for test in tests:
        success = run_command(test['cmd'], test['desc'], test['timeout'])
        results.append(success)
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\n🚀 Ready to launch DAWN GUI modes:")
        
        modes = [
            ('auto', 'Auto-detect best mode'),
            ('unified', 'Unified interface (all features)'),
            ('enhanced', 'Enhanced with reflex components'),
            ('standard', 'Standard DAWN GUI'),
            ('websocket', 'WebSocket-only interface'),
            ('demo', 'Demo mode with simulation'),
        ]
        
        print("\nAvailable launch commands:")
        for mode, desc in modes:
            print(f"  python dawn_unified_launcher.py --mode {mode:<10} # {desc}")
        
        return True
    else:
        print("❌ Some tests failed - check dependencies and components")
        return False

def demo_quick_launch():
    """Demonstrate a quick GUI launch (non-blocking)"""
    print("\n🎭 Quick Demo Launch Test")
    print("=" * 40)
    
    print("This would normally launch the GUI:")
    print("  python dawn_unified_launcher.py --mode websocket --no-backend")
    print("\n⚠️ Skipping actual GUI launch to avoid blocking terminal")
    print("✅ To test GUI manually, run the command above")

def main():
    """Main test function"""
    print("Starting DAWN Unified Launcher tests...")
    
    # Test basic launcher functionality
    if test_unified_launcher():
        demo_quick_launch()
        
        print("\n🏆 DAWN Unified System Ready!")
        print("\n📋 Quick Start Guide:")
        print("  1. python dawn_unified_launcher.py                    # Auto mode")
        print("  2. python dawn_unified_launcher.py --mode enhanced    # Enhanced GUI")
        print("  3. python dawn_unified_launcher.py --mode demo        # Demo with backend")
        print("  4. python start_dawn_gui.py                          # Legacy launcher")
        
        print("\n🔗 Integration Examples:")
        print("  • WebSocket backend: ws://localhost:8000/ws")
        print("  • GUI connects automatically to available data sources")
        print("  • Fallback to simulation if no backend available")
        print("  • All existing launcher scripts updated to use unified system")
        
    else:
        print("\n❌ Setup incomplete - please check requirements and components")
        
    print("\n👋 Test complete!")

if __name__ == "__main__":
    main() 