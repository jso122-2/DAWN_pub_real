#!/usr/bin/env python3
"""
Force Consolidated GUI Only
Temporarily rename other GUI files to ensure only consolidated GUI is served
"""

from pathlib import Path
import shutil

def main():
    """Force server to serve only consolidated GUI"""
    print("🔧 FORCE CONSOLIDATED GUI ONLY")
    print("=" * 50)
    
    # Check if consolidated GUI exists
    consolidated_gui = Path('dawn_consolidated_gui.html')
    if not consolidated_gui.exists():
        print("❌ dawn_consolidated_gui.html not found!")
        print("💡 You need to create it first")
        return 1
    
    print(f"✅ Found consolidated GUI: {consolidated_gui.name}")
    print(f"   📊 Size: {consolidated_gui.stat().st_size:,} bytes")
    
    # List of other GUI files to temporarily rename
    other_gui_files = [
        'dawn_ultimate_gui.html',
        'simple_gui.html',
        'dawn_monitor.html',
        'dawn_local_gui.html'
    ]
    
    print()
    print("🔄 Temporarily renaming other GUI files...")
    
    renamed_files = []
    for filename in other_gui_files:
        file_path = Path(filename)
        if file_path.exists():
            backup_name = f"{filename}.backup"
            backup_path = Path(backup_name)
            
            # If backup already exists, skip
            if backup_path.exists():
                print(f"   ⚠️ {filename} -> {backup_name} (backup already exists)")
            else:
                shutil.move(str(file_path), str(backup_path))
                renamed_files.append((filename, backup_name))
                print(f"   ✅ {filename} -> {backup_name}")
        else:
            print(f"   ➖ {filename} (not found)")
    
    print()
    print("🎯 RESULT:")
    print("   Only dawn_consolidated_gui.html will be served now")
    print("   Other GUI files are safely backed up with .backup extension")
    print()
    
    print("🚀 NOW RESTART YOUR SERVER:")
    print("   1. Stop current server (Ctrl+C)")
    print("   2. Run: python launch_consolidated_web_gui.py")
    print("   3. Open: http://localhost:3000")
    print()
    
    print("🔄 TO RESTORE OTHER GUI FILES LATER:")
    print("   Run: python restore_gui_backups.py")
    print()
    
    # Create restore script
    create_restore_script(renamed_files)
    
    return 0

def create_restore_script(renamed_files):
    """Create a script to restore the backed up files"""
    restore_script = '''#!/usr/bin/env python3
"""
Restore GUI Backups
Restore the backed up GUI files
"""

from pathlib import Path
import shutil

def main():
    print("🔄 RESTORING GUI BACKUPS")
    print("=" * 40)
    
    renamed_files = ''' + str(renamed_files) + '''
    
    for original, backup in renamed_files:
        backup_path = Path(backup)
        original_path = Path(original)
        
        if backup_path.exists():
            if original_path.exists():
                print(f"   ⚠️ {original} already exists, skipping")
            else:
                shutil.move(str(backup_path), str(original_path))
                print(f"   ✅ {backup} -> {original}")
        else:
            print(f"   ❌ {backup} not found")
    
    print()
    print("✅ GUI files restored!")

if __name__ == "__main__":
    main()
'''
    
    with open('restore_gui_backups.py', 'w') as f:
        f.write(restore_script)
    
    print("📝 Created restore_gui_backups.py for later use")

if __name__ == "__main__":
    exit(main()) 