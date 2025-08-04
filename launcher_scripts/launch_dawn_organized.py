#!/usr/bin/env python3
"""
DAWN Organized Launcher
=======================

Main launcher for the organized DAWN system.
Works with the new directory structure after cleanup.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='Launch DAWN system components')
    parser.add_argument('--component', choices=['core', 'visual', 'conversation', 'beautiful'], 
                       default='core', help='Component to launch')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--list', action='store_true', help='List available components')
    
    args = parser.parse_args()
    
    if args.list:
        list_components()
        return
    
    if args.test:
        run_tests()
        return
    
    launch_component(args.component)

def list_components():
    """List available components"""
    print("🎯 Available DAWN Components:")
    print("=" * 40)
    
    components = {
        'core': {
            'description': 'Core DAWN system',
            'launcher': 'launchers/launch_dawn.py',
            'files': ['core/dawn_runner.py', 'core/dawn_constitution.py']
        },
        'visual': {
            'description': 'Visualization system',
            'launcher': 'launchers/launch_visual_gui.py',
            'files': ['visual/dawn_visual_gui.py', 'visual/visual_engine.py']
        },
        'conversation': {
            'description': 'Conversation system',
            'launcher': 'conversation/cli_dawn_conversation.py',
            'files': ['conversation/conversation_input_enhanced.py', 'conversation/conversation_response_enhanced.py']
        },
        'beautiful': {
            'description': 'Beautiful visualization system',
            'launcher': 'launchers/launch_dawn_beautiful.py',
            'files': ['visual/dawn_visual_beautiful.py']
        }
    }
    
    for name, info in components.items():
        print(f"\n🔧 {name.upper()}")
        print(f"   {info['description']}")
        print(f"   Launcher: {info['launcher']}")
        print(f"   Key files: {', '.join(info['files'])}")

def launch_component(component):
    """Launch a specific component"""
    launchers = {
        'core': 'launchers/launch_dawn.py',
        'visual': 'launchers/launch_visual_gui.py',
        'conversation': 'conversation/cli_dawn_conversation.py',
        'beautiful': 'launchers/launch_dawn_beautiful.py'
    }
    
    launcher = launchers.get(component)
    if not launcher or not Path(launcher).exists():
        print(f"❌ Launcher not found for component: {component}")
        return
    
    print(f"🚀 Launching {component} component...")
    print(f"   Using: {launcher}")
    
    try:
        subprocess.run([sys.executable, launcher], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch {component}: {e}")
    except KeyboardInterrupt:
        print(f"\n🛑 {component} component stopped")

def run_tests():
    """Run system tests"""
    print("🧪 Running DAWN system tests...")
    
    test_files = [
        'tests/test_conversation_system.py',
        'tests/test_enhanced_conversation_system.py',
        'integration/test_dawn_connection.py'
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"   Running {test_file}...")
            try:
                subprocess.run([sys.executable, test_file], check=True)
                print(f"   ✅ {test_file} passed")
            except subprocess.CalledProcessError:
                print(f"   ❌ {test_file} failed")
        else:
            print(f"   ⚠️  {test_file} not found")

if __name__ == "__main__":
    main() 