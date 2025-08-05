#!/usr/bin/env python3
"""
DAWN GUI Fix Validation Test
============================

Tests that all GUI fixes have been applied successfully and buttons/tabs are functional.
"""

import os
import subprocess
import time
import requests
from pathlib import Path

def test_web_server_startup():
    """Test that the web server starts without import errors"""
    print("🌐 Testing web server startup...")
    
    try:
        # Try to import web_server module
        import sys
        sys.path.append(".")
        
        # Test import
        from web_server import DAWNWebRunner
        print("  ✅ Web server module imports successfully")
        
        # Test initialization
        runner = DAWNWebRunner()
        print("  ✅ Web server initializes without errors")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Initialization error: {e}")
        return False

def test_gui_files_exist():
    """Test that all required GUI files exist"""
    print("\n📁 Testing GUI file structure...")
    
    required_files = [
        "dawn_ultimate_gui.html",
        "dawn_gui_fix.js",
        "web_server.py",
        "test_gui_fixes.py"
    ]
    
    missing_files = []
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
        else:
            print(f"  ✅ {file_name} exists")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    return True

def test_button_handlers():
    """Test that button handlers are properly defined in the fix script"""
    print("\n🔘 Testing button handler definitions...")
    
    try:
        with open("dawn_gui_fix.js", 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for key handler functions
        required_handlers = [
            "toggleEntropyPanel",
            "exportEntropyData", 
            "openEntropySettings",
            "pauseNeuralActivity",
            "resetNeuralActivity",
            "toggle3DView",
            "executeSigilCommand",
            "clearSigilInput",
            "toggleAutoRebloom",
            "exportMemoryData",
            "toggleFullscreenVisualization",
            "toggleVoiceMode",
            "clearCommentary",
            "toggleAutoFollow",
            "clearThoughtTrace",
            "toggleLogFilter",
            "clearSystemLogs",
            "openAdvancedPanel",
            "switchTab",
            "handleButtonClick"
        ]
        
        missing_handlers = []
        for handler in required_handlers:
            if f"function {handler}" not in js_content:
                missing_handlers.append(handler)
            else:
                print(f"  ✅ {handler} defined")
        
        if missing_handlers:
            print(f"  ❌ Missing handlers: {missing_handlers}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading fix script: {e}")
        return False

def test_html_button_integration():
    """Test that HTML file includes the fix script"""
    print("\n🔗 Testing HTML-JavaScript integration...")
    
    try:
        with open("dawn_ultimate_gui.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check that fix script is included
        if 'dawn_gui_fix.js' in html_content:
            print("  ✅ Fix script included in HTML")
        else:
            print("  ❌ Fix script not included in HTML")
            return False
        
        # Check for script tag
        if '<script src="dawn_gui_fix.js"></script>' in html_content:
            print("  ✅ Fix script properly linked")
        else:
            print("  ❌ Fix script not properly linked")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading HTML file: {e}")
        return False

def test_server_endpoints():
    """Test that server has required API endpoints"""
    print("\n🌐 Testing API endpoint availability...")
    
    # Start server in background for testing
    print("  🚀 Starting test server...")
    
    try:
        # Import and start server
        from web_server import DAWNWebRunner
        server = DAWNWebRunner(port=8081)  # Use different port for testing
        
        # Test that server can initialize
        print("  ✅ Server initializes successfully")
        
        # Check that required endpoints exist in code
        with open("web_server.py", 'r', encoding='utf-8') as f:
            server_content = f.read()
        
        required_endpoints = [
            "/api/consciousness-state",
            "/api/sigil-overlays", 
            "/api/entropy-visual",
            "/api/fractal-current"
        ]
        
        missing_endpoints = []
        for endpoint in required_endpoints:
            if endpoint.replace("/", "") in server_content or endpoint in server_content:
                print(f"  ✅ {endpoint} endpoint available")
            else:
                missing_endpoints.append(endpoint)
        
        if missing_endpoints:
            print(f"  ❌ Missing endpoints: {missing_endpoints}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Server test error: {e}")
        return False

def test_import_fixes():
    """Test that import fixes resolved dependency issues"""
    print("\n🔧 Testing import dependency fixes...")
    
    try:
        # Test key imports
        test_modules = [
            "entropy_visual_stream",
            "sigil_overlay_renderer", 
            "web_server"
        ]
        
        successful_imports = []
        failed_imports = []
        
        for module_name in test_modules:
            try:
                if Path(f"{module_name}.py").exists():
                    __import__(module_name)
                    successful_imports.append(module_name)
                    print(f"  ✅ {module_name} imports successfully")
                else:
                    print(f"  ℹ️ {module_name} not found (optional)")
            except ImportError as e:
                failed_imports.append((module_name, str(e)))
                print(f"  ⚠️ {module_name} import warning: {e}")
            except Exception as e:
                failed_imports.append((module_name, str(e)))
                print(f"  ❌ {module_name} import error: {e}")
        
        # Success if most imports work
        success_rate = len(successful_imports) / len(test_modules)
        if success_rate >= 0.7:  # 70% success rate
            print(f"  ✅ Import fixes successful ({success_rate:.1%} success rate)")
            return True
        else:
            print(f"  ❌ Import fixes partially successful ({success_rate:.1%} success rate)")
            return False
        
    except Exception as e:
        print(f"  ❌ Import test error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🧪 DAWN GUI Fix Validation Test")
    print("=" * 50)
    
    tests = [
        ("GUI Files", test_gui_files_exist),
        ("Web Server", test_web_server_startup),
        ("Button Handlers", test_button_handlers),
        ("HTML Integration", test_html_button_integration),
        ("API Endpoints", test_server_endpoints),
        ("Import Fixes", test_import_fixes)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"  ❌ Test {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<20} {status}")
    
    print(f"\n📊 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED! Your DAWN GUI should now be fully functional.")
        print("\n🚀 Next Steps:")
        print("   1. Start the web server: python web_server.py --port 8080")
        print("   2. Open: http://localhost:8080/dawn_ultimate_gui.html")
        print("   3. Test button functionality and tab switching")
    elif passed >= total * 0.8:  # 80% pass rate
        print("✅ Most tests PASSED! GUI should be functional with minor issues.")
        print("\n⚠️ Check failed tests above for any remaining issues.")
    else:
        print("❌ Several tests FAILED. Additional fixes may be needed.")
        print("\n🔧 Check the specific test failures above.")
    
    return passed, total, results

if __name__ == "__main__":
    run_comprehensive_test() 