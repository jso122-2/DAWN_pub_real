"""
Simple JSON Fixer - Find and fix corrupted JSON logs
No emojis, just pure functionality
"""

import json
import os
from pathlib import Path

def fix_json_logs():
    """Find and fix corrupted JSON logs"""
    
    print("Searching for JSON log files...")
    
    # Find all JSON files
    json_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    
    print(f"Found {len(json_files)} JSON files")
    
    fixed_count = 0
    
    for json_file in json_files:
        try:
            # Try to load the file
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"OK: {json_file}")
            
        except Exception as e:
            print(f"CORRUPTED: {json_file} - {e}")
            
            # Back up the corrupted file
            backup_path = json_file + ".backup"
            try:
                os.rename(json_file, backup_path)
                print(f"  Backed up to: {backup_path}")
            except:
                pass
            
            # Create fresh file
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                print(f"  FIXED: {json_file}")
                fixed_count += 1
            except Exception as e:
                print(f"  Could not fix: {e}")
    
    print(f"Fixed {fixed_count} corrupted files")
    return fixed_count

def create_missing_logs():
    """Create missing log files that DAWN needs"""
    
    required_logs = [
        "owl/owl_tracer_log.json",
        "logs/owl_tracer_log.json", 
        "schema/logs/schema_log.json"
    ]
    
    for log_path in required_logs:
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            
            # Create file if missing
            if not os.path.exists(log_path):
                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                print(f"Created: {log_path}")
        except Exception as e:
            print(f"Could not create {log_path}: {e}")

def main():
    print("DAWN JSON Log Repair")
    print("=" * 30)
    
    # Create missing logs first
    create_missing_logs()
    
    # Fix corrupted logs
    fixed = fix_json_logs()
    
    print("=" * 30)
    print("Repair complete!")
    print(f"Fixed {fixed} files")
    print("Try running: python main.py")

if __name__ == "__main__":
    main()