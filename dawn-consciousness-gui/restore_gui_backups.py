#!/usr/bin/env python3
"""
Restore GUI Backups
Restore the backed up GUI files
"""

from pathlib import Path
import shutil

def main():
    print("🔄 RESTORING GUI BACKUPS")
    print("=" * 40)
    
    renamed_files = []
    
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
