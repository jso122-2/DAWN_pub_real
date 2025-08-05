#!/usr/bin/env python3
"""
Fix Browser Cache Issues for DAWN Consolidated GUI
Helps resolve JavaScript errors caused by cached old GUI content
"""

import time
import webbrowser
from pathlib import Path

def main():
    """Main cache fixing function"""
    print("🧹 DAWN GUI Browser Cache Fix")
    print("=" * 50)
    
    print("🔍 Checking for consolidated GUI...")
    gui_file = Path('dawn_consolidated_gui.html')
    
    if gui_file.exists():
        print("✅ Consolidated GUI found")
    else:
        print("❌ Consolidated GUI missing!")
        print("💡 Run the GUI creation script first")
        return 1
    
    print()
    print("🧹 Browser Cache Clearing Instructions:")
    print("-" * 50)
    
    print("1. 🌐 Hard Refresh (Recommended):")
    print("   • Chrome/Edge: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)")
    print("   • Firefox: Ctrl+F5 (Windows) / Cmd+Shift+R (Mac)")
    print("   • Safari: Cmd+Option+R")
    print()
    
    print("2. 🧹 Clear Browser Cache (If hard refresh doesn't work):")
    print("   • Chrome: Settings → Privacy → Clear browsing data → Cached images and files")
    print("   • Firefox: Settings → Privacy → Clear Data → Cached Web Content")
    print("   • Edge: Settings → Privacy → Clear browsing data → Cached images and files")
    print()
    
    print("3. 🔄 Restart Web Server:")
    print("   • Stop current server (Ctrl+C)")
    print("   • Run: python launch_consolidated_web_gui.py --no-browser")
    print("   • Hard refresh browser after restart")
    print()
    
    print("4. 🚫 Disable Cache (For Development):")
    print("   • Open Browser Developer Tools (F12)")
    print("   • Go to Network tab")
    print("   • Check 'Disable cache' option")
    print("   • Keep Developer Tools open while using GUI")
    print()
    
    print("🔧 Expected Results After Cache Clear:")
    print("-" * 50)
    print("✅ No 'switchVisualization is not defined' errors")
    print("✅ No missing image 404 errors")
    print("✅ No 'Cannot set properties of undefined' errors")
    print("✅ Clean tab-based interface loads")
    print("✅ All buttons and controls work")
    print()
    
    print("📋 JavaScript Console Should Show:")
    print("   🔄 Loading DAWN Consolidated GUI v1.0.0")
    print("   🌅 DAWN Consolidated GUI initialized")
    print("   🔄 Connecting to real DAWN backend: http://localhost:8080")
    print()
    
    # Automatic browser opening with cache-busting URL
    print("🚀 Opening browser with cache-busting URL...")
    cache_bust = int(time.time())
    url = f"http://localhost:3000?v={cache_bust}&clear_cache=1"
    
    try:
        webbrowser.open(url)
        print(f"✅ Opened: {url}")
        print("💡 This URL includes cache-busting parameters")
    except Exception as e:
        print(f"⚠️ Could not auto-open browser: {e}")
        print(f"💡 Manually open: {url}")
    
    print()
    print("🔍 Troubleshooting Tips:")
    print("-" * 50)
    print("• If errors persist: Try incognito/private browsing mode")
    print("• If still broken: Check if server is running on port 3000")
    print("• For backend issues: Start real_dawn_backend.py on port 8080")
    print("• For testing: Run python test_consolidated_gui.py")
    print()
    
    print("✨ The consolidated GUI should now load properly!")
    return 0

if __name__ == "__main__":
    exit(main()) 