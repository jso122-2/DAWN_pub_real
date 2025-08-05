#!/usr/bin/env python3
"""
Test what files the server can find
"""

from pathlib import Path

def main():
    print("🔍 TESTING SERVER FILE DETECTION")
    print("=" * 50)
    
    # This is the same logic as in real_aware_web_server.py
    gui_files = [
        'dawn_consolidated_gui.html',
        'dawn_ultimate_gui.html',
        'simple_gui.html', 
        'dawn_monitor.html',
        'dawn_local_gui.html'
    ]
    
    print(f"📁 Current directory: {Path.cwd()}")
    print(f"🔍 Script location: {Path(__file__).parent}")
    print()
    
    gui_file = None
    print("Looking for GUI files in order:")
    for filename in gui_files:
        file_path = Path(__file__).parent / filename
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        
        print(f"   {filename}")
        print(f"      Path: {file_path}")
        print(f"      Exists: {'✅ YES' if exists else '❌ NO'}")
        if exists:
            print(f"      Size: {size:,} bytes")
            if gui_file is None:
                gui_file = file_path
                print(f"      🎯 SELECTED!")
        print()
    
    if gui_file:
        print(f"🎉 Server would serve: {gui_file.name}")
        
        # Check content quickly
        try:
            with open(gui_file, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # First 1000 chars
            
            title_start = content.find('<title>') + 7
            title_end = content.find('</title>')
            title = content[title_start:title_end] if title_start > 6 and title_end > title_start else "No title"
            
            print(f"📝 Title: {title}")
            print(f"🔍 Contains 'Consolidated': {'✅ YES' if 'Consolidated' in content else '❌ NO'}")
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            
    else:
        print("❌ NO GUI FILES FOUND - Server will use minimal fallback")
        print("   This explains why you're seeing the basic JSON interface")
    
    # Check for backup files
    print()
    print("🔍 CHECKING FOR BACKUP FILES:")
    backup_files = list(Path(__file__).parent.glob("*.html.backup"))
    if backup_files:
        print("Found backup files:")
        for backup in backup_files:
            original = str(backup).replace('.backup', '')
            print(f"   {backup.name} -> {Path(original).name}")
    else:
        print("   No backup files found")

if __name__ == "__main__":
    main() 