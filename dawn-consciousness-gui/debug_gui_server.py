#!/usr/bin/env python3
"""
Debug GUI Server Issues
Check which GUI file is being served and why
"""

from pathlib import Path
import requests

def check_gui_files():
    """Check which GUI files exist and their content"""
    print("🔍 GUI FILES ANALYSIS")
    print("=" * 50)
    
    gui_files = [
        'dawn_consolidated_gui.html',
        'dawn_ultimate_gui.html',
        'simple_gui.html',
        'dawn_monitor.html',
        'dawn_local_gui.html'
    ]
    
    for filename in gui_files:
        file_path = Path(filename)
        if file_path.exists():
            content = file_path.read_text()
            title_start = content.find('<title>') + 7
            title_end = content.find('</title>')
            title = content[title_start:title_end] if title_start > 6 and title_end > title_start else "No title"
            
            has_consolidated = 'Consolidated' in content
            has_tabs = 'switchTab' in content
            
            print(f"✅ {filename}")
            print(f"   📊 Size: {len(content):,} characters")
            print(f"   📝 Title: {title}")
            print(f"   🎯 Consolidated: {'✅ YES' if has_consolidated else '❌ NO'}")
            print(f"   🏷️ Has Tabs: {'✅ YES' if has_tabs else '❌ NO'}")
            print()
        else:
            print(f"❌ {filename} - NOT FOUND")
            print()

def test_server_response():
    """Test what the server is actually serving"""
    print("🌐 SERVER RESPONSE TEST")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        
        if response.status_code == 200:
            content = response.text
            
            # Extract title
            title_start = content.find('<title>') + 7
            title_end = content.find('</title>')
            title = content[title_start:title_end] if title_start > 6 and title_end > title_start else "No title"
            
            print(f"✅ Server responding (status: {response.status_code})")
            print(f"📊 Content length: {len(content):,} characters")
            print(f"📝 Title: {title}")
            print(f"🎯 Contains 'Consolidated': {'✅ YES' if 'Consolidated' in content else '❌ NO'}")
            print(f"🏷️ Contains 'switchTab': {'✅ YES' if 'switchTab' in content else '❌ NO'}")
            print(f"🔧 Contains old 'switchView': {'⚠️ YES (OLD GUI!)' if 'switchView' in content and 'currentView' in content else '✅ NO'}")
            
            # Check for version info
            headers = response.headers
            if 'X-GUI-Version' in headers:
                print(f"🏷️ GUI Version Header: {headers['X-GUI-Version']}")
            else:
                print("⚠️ No GUI version header")
                
            print()
            
            if 'Consolidated Consciousness Interface' in content:
                print("🎉 SERVER IS SERVING THE NEW CONSOLIDATED GUI!")
            elif 'Ultimate Consciousness Monitor' in content:
                print("⚠️ SERVER IS SERVING THE OLD ULTIMATE GUI!")
                print("💡 This explains why you're seeing the old 3-column layout")
            else:
                print("❓ SERVER IS SERVING UNKNOWN GUI")
            
        else:
            print(f"❌ Server error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on localhost:3000")
        print("💡 Make sure the server is running:")
        print("   python launch_consolidated_web_gui.py")
        
    except Exception as e:
        print(f"❌ Error testing server: {e}")

def main():
    """Run all diagnostics"""
    print("🔧 DAWN GUI SERVER DIAGNOSTIC")
    print("=" * 70)
    print()
    
    check_gui_files()
    test_server_response()
    
    print()
    print("🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. If consolidated GUI exists but server serves old GUI:")
    print("   • Restart server: python launch_consolidated_web_gui.py")
    print("   • Check server debug output for which file it selects")
    print()
    print("2. If server serves consolidated GUI but browser shows old:")
    print("   • Clear browser cache completely")
    print("   • Try incognito/private mode")
    print("   • Hard refresh: Ctrl+Shift+R")
    print()
    print("3. If consolidated GUI file is wrong:")
    print("   • The GUI file needs to be recreated")

if __name__ == "__main__":
    main() 