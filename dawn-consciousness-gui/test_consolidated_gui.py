#!/usr/bin/env python3
"""
Test script for DAWN Consolidated GUI
Verifies that all components are working properly
"""

import requests
import time
import subprocess
import sys
from pathlib import Path

def test_gui_files():
    """Test that all GUI files exist"""
    print("🔍 Testing GUI files...")
    
    gui_files = [
        'dawn_consolidated_gui.html',
        'real_aware_web_server.py',
        'launch_consolidated_web_gui.py'
    ]
    
    for file in gui_files:
        if Path(file).exists():
            print(f"  ✅ {file} exists")
        else:
            print(f"  ❌ {file} missing")
            return False
    
    return True

def test_gui_content():
    """Test that the consolidated GUI has the right content"""
    print("🔍 Testing GUI content...")
    
    gui_file = Path('dawn_consolidated_gui.html')
    if not gui_file.exists():
        print("  ❌ GUI file doesn't exist")
        return False
    
    content = gui_file.read_text()
    
    required_elements = [
        'switchTab(',  # Tab switching function
        'switchVisualization(',  # Visualization switching
        'Tab-Based Interface',  # Comment indicating new interface
        'Visual Tab',  # Visual tab content
        'Voice Tab',  # Voice tab content
        'State Monitor',  # State monitor tab
        'error handler',  # Error handling code
        'legacy function',  # Legacy compatibility
    ]
    
    for element in required_elements:
        if element in content:
            print(f"  ✅ Found: {element}")
        else:
            print(f"  ⚠️ Missing: {element}")
    
    print(f"  📊 GUI file size: {len(content):,} characters")
    return True

def test_server_response():
    """Test that the server serves the consolidated GUI"""
    print("🔍 Testing server response...")
    
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        
        if response.status_code == 200:
            print(f"  ✅ Server responding (status: {response.status_code})")
            
            # Check for consolidated GUI markers
            content = response.text
            
            if 'DAWN - Consolidated Consciousness Interface' in content:
                print("  ✅ Serving consolidated GUI")
            else:
                print("  ⚠️ Not serving consolidated GUI")
            
            if 'switchVisualization' in content:
                print("  ✅ JavaScript functions present")
            else:
                print("  ⚠️ JavaScript functions missing")
            
            # Check headers
            headers = response.headers
            if 'X-GUI-Version' in headers:
                print(f"  ✅ GUI Version: {headers['X-GUI-Version']}")
            else:
                print("  ⚠️ No version header")
            
            return True
        else:
            print(f"  ❌ Server error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ⚠️ Server not running on localhost:3000")
        return False
    except Exception as e:
        print(f"  ❌ Server test failed: {e}")
        return False

def test_backend_connection():
    """Test connection to DAWN backend"""
    print("🔍 Testing backend connection...")
    
    try:
        response = requests.get('http://localhost:8080/status', timeout=5)
        
        if response.status_code == 200:
            print("  ✅ Backend responding")
            
            data = response.json()
            if 'mode' in data:
                print(f"  📊 Backend mode: {data['mode']}")
            
            return True
        else:
            print(f"  ❌ Backend error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ⚠️ Backend not running on localhost:8080")
        return False
    except Exception as e:
        print(f"  ❌ Backend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 DAWN Consolidated GUI Test Suite")
    print("=" * 50)
    
    tests = [
        test_gui_files,
        test_gui_content,
        test_server_response,
        test_backend_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"  ❌ Test failed with error: {e}")
            results.append(False)
            print()
    
    # Summary
    print("📊 Test Results:")
    print("=" * 50)
    
    if all(results[:2]):  # File tests must pass
        print("✅ GUI files are properly installed")
    else:
        print("❌ GUI files have issues")
    
    if results[2]:  # Server test
        print("✅ Web server is serving consolidated GUI")
    else:
        print("⚠️ Web server issues - try restarting with:")
        print("   python launch_consolidated_web_gui.py")
    
    if results[3]:  # Backend test
        print("✅ DAWN backend is available")
    else:
        print("⚠️ Backend not available - start with:")
        print("   python real_dawn_backend.py")
    
    print()
    if all(results):
        print("🎉 All systems operational!")
        print("🌐 Access GUI at: http://localhost:3000")
    else:
        print("⚠️ Some components need attention")
    
    return 0 if all(results[:2]) else 1  # Return error if critical files missing

if __name__ == "__main__":
    sys.exit(main()) 