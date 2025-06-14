#!/usr/bin/env python3
"""
Dependency installation script with verification
"""
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install all requirements with error handling"""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    print("🔧 Installing DAWN dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def verify_imports():
    """Verify critical imports work"""
    critical_imports = [
        "numpy",
        "matplotlib",
        "websocket",
        "requests",
        "fastapi",
        "asyncio"
    ]
    
    failed = []
    for module in critical_imports:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            failed.append(module)
            print(f"❌ Failed to import {module}")
    
    if failed:
        print(f"\n❌ Failed imports: {', '.join(failed)}")
        print("Please install missing dependencies manually")
        sys.exit(1)
    else:
        print("\n✅ All critical imports verified!")

if __name__ == "__main__":
    install_requirements()
    verify_imports() 