# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Complete System Launcher

Launches DAWN with visual integration and API server for Tauri GUI.
"""

import sys
import os
import subprocess
import threading
import time
import signal
from pathlib import Path

def main():
    """Main launcher function"""
    print("🌅 DAWN Complete System Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("dawn_runner.py").exists():
        print("❌ Error: dawn_runner.py not found. Please run from the DAWN project root.")
        return
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    
    # Check visual integration
    try:
        from visual.visual_integration import get_visual_integration
        print("✅ Visual integration available")
    except ImportError as e:
        print(f"⚠️  Visual integration not available: {e}")
    
    # Check Flask for API server
    try:
        import flask
        print("✅ Flask available for API server")
    except ImportError:
        print("⚠️  Flask not available - install with: pip install flask flask-cors")
        print("   API server will not be available")
    
    print("\n🚀 Starting DAWN Complete System...")
    
    # Start processes
    dawn_process = None
    api_process = None
    
    try:
        # Start DAWN runner
        print("🧠 Starting DAWN Unified Runner...")
        dawn_process = subprocess.Popen(
            [sys.executable, "launch_dawn.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Give DAWN time to start
        time.sleep(3)
        
        # Start visual API server if Flask is available
        try:
            import flask
            print("📡 Starting Visual API Server...")
            api_process = subprocess.Popen(
                [sys.executable, "visual_api_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            time.sleep(2)
        except ImportError:
            print("⚠️  Skipping API server (Flask not available)")
        
        print("\n✅ DAWN Complete System is running!")
        print("   - DAWN Runner: PID", dawn_process.pid if dawn_process else "N/A")
        print("   - Visual API Server: PID", api_process.pid if api_process else "N/A")
        
        print("\n🌐 Visual API Server:")
        print("   - Status: http://localhost:5001/api/visual/status")
        print("   - Data: http://localhost:5001/api/visual/data")
        print("   - Modules: http://localhost:5001/api/visual/modules")
        
        print("\n🎨 Tauri GUI Integration:")
        print("   - Component: DAWNVisualProcesses.tsx")
        print("   - CSS: DAWNVisualProcesses.css")
        print("   - API Base URL: http://localhost:5001/api/visual")
        
        print("\n📋 To integrate with Tauri GUI:")
        print("   1. Copy DAWNVisualProcesses.tsx to your Tauri src/components/")
        print("   2. Copy DAWNVisualProcesses.css to your Tauri src/components/")
        print("   3. Import and use the component in your Tauri app")
        print("   4. The component will automatically connect to the API server")
        
        print("\n🔧 Manual Testing:")
        print("   - Test API: curl http://localhost:5001/api/visual/status")
        print("   - Test data: curl http://localhost:5001/api/visual/data")
        print("   - Test visualization: curl -X POST http://localhost:5001/api/visual/generate/tick_pulse")
        
        print("\nPress Ctrl+C to stop all processes...")
        
        # Monitor processes
        while True:
            if dawn_process and dawn_process.poll() is not None:
                print("❌ DAWN Runner stopped unexpectedly")
                break
            if api_process and api_process.poll() is not None:
                print("❌ Visual API Server stopped unexpectedly")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if dawn_process:
            print("🛑 Stopping DAWN Runner...")
            dawn_process.terminate()
            dawn_process.wait(timeout=5)
        
        if api_process:
            print("🛑 Stopping Visual API Server...")
            api_process.terminate()
            api_process.wait(timeout=5)
        
        print("✅ All processes stopped")

def test_api():
    """Test the API endpoints"""
    import requests
    import json
    
    base_url = "http://localhost:5001/api/visual"
    
    print("\n🧪 Testing Visual API...")
    
    try:
        # Test status
        response = requests.get(f"{base_url}/status")
        if response.ok:
            print("✅ Status endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Status endpoint failed")
        
        # Test data
        response = requests.get(f"{base_url}/data")
        if response.ok:
            print("✅ Data endpoint working")
            data = response.json()
            print(f"   Tick: {data.get('tick_number', 'N/A')}")
            print(f"   SCUP: {data.get('scup', 'N/A')}")
            print(f"   Heat: {data.get('heat', 'N/A')}")
        else:
            print("❌ Data endpoint failed")
        
        # Test modules
        response = requests.get(f"{base_url}/modules")
        if response.ok:
            print("✅ Modules endpoint working")
            modules = response.json()
            print(f"   Available modules: {len(modules)}")
            for module_id, module_info in modules.items():
                print(f"     - {module_id}: {module_info['name']}")
        else:
            print("❌ Modules endpoint failed")
        
        # Test visualization generation
        response = requests.post(f"{base_url}/generate/tick_pulse")
        if response.ok:
            print("✅ Visualization generation working")
            result = response.json()
            if result.get('success'):
                print("   Visualization generated successfully")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')}")
        else:
            print("❌ Visualization generation failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server - make sure it's running")
    except Exception as e:
        print(f"❌ API test error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_api()
    else:
        main() 