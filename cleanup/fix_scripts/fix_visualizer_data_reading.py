#!/usr/bin/env python3
"""
Fix visualizer data reading to use JSON file instead of stdin
"""

import os
import re
import glob
from pathlib import Path

def fix_visualizer_data_reading():
    """Patch visualizers to read from JSON file instead of stdin"""
    
    # Find all visualizer files
    visualizer_files = []
    visualizer_dirs = [
        "backend/visual",
        "visual"
    ]
    
    for dir_path in visualizer_dirs:
        if os.path.exists(dir_path):
            visualizer_files.extend(glob.glob(f"{dir_path}/*.py"))
    
    print(f"Found {len(visualizer_files)} visualizer files")
    
    # Patterns to replace
    replacements = [
        # Replace stdin reading with JSON file reading
        (
            r'def read_stdin_data\(self\):',
            '''def read_json_data(self):
        """Background thread to read data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        last_position = 0
        
        while not self.stop_event.is_set():
            try:
                if not os.path.exists(json_file):
                    time.sleep(0.1)
                    continue
                
                with open(json_file, 'r') as f:
                    f.seek(last_position)
                    lines = f.readlines()
                    last_position = f.tell()
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            self.data_queue.put(data)
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"Error parsing JSON: {e}", file=sys.stderr)
                            continue
                
                time.sleep(0.1)  # Small delay to avoid excessive CPU usage
                
            except Exception as e:
                print(f"Error reading JSON file: {e}", file=sys.stderr)
                time.sleep(1.0)  # Longer delay on error'''
        ),
        
        # Replace stdin.readline() with JSON file reading
        (
            r'line = sys\.stdin\.readline\(\)',
            '''# Read from JSON file instead of stdin
                json_file = "/tmp/dawn_tick_data.json"
                if not os.path.exists(json_file):
                    time.sleep(0.1)
                    continue
                
                with open(json_file, 'r') as f:
                    f.seek(0, 2)  # Seek to end
                    file_size = f.tell()
                    if file_size == 0:
                        time.sleep(0.1)
                        continue
                    
                    # Read last line
                    f.seek(max(0, file_size - 1024))  # Read last 1KB
                    lines = f.readlines()
                    if lines:
                        line = lines[-1].strip()'''
        ),
        
        # Replace data_source == "stdin" check
        (
            r'if self\.data_source == "stdin":',
            'if True:  # Always read from JSON file'
        ),
        
        # Replace stdin reading in update_visualization
        (
            r'while not self\.data_queue\.empty\(\):\s+data = self\.data_queue\.get\(\)',
            '''# Read from JSON file
                json_file = "/tmp/dawn_tick_data.json"
                if os.path.exists(json_file):
                    try:
                        with open(json_file, 'r') as f:
                            lines = f.readlines()
                            if lines:
                                last_line = lines[-1].strip()
                                if last_line:
                                    data = json.loads(last_line)
                    except Exception as e:
                        print(f"Error reading JSON: {e}", file=sys.stderr)
                        data = None
                else:
                    data = None'''
        ),
        
        # Add necessary imports
        (
            r'import json',
            '''import json
import os'''
        ),
        
        # Replace stdin.readline() in read_stdin_data
        (
            r'line = sys\.stdin\.readline\(\)\s+if line == \'\':\s+print\("\[.*?\] Waiting for input\.\.\."\)\s+time\.sleep\(0\.1\)\s+continue',
            '''# Read from JSON file
                json_file = "/tmp/dawn_tick_data.json"
                if not os.path.exists(json_file):
                    print("[visualizer] Waiting for JSON file...")
                    time.sleep(0.1)
                    continue
                
                try:
                    with open(json_file, 'r') as f:
                        lines = f.readlines()
                        if not lines:
                            print("[visualizer] JSON file is empty, waiting...")
                            time.sleep(0.1)
                            continue
                        
                        line = lines[-1].strip()  # Get last line
                        if not line:
                            time.sleep(0.1)
                            continue
                except Exception as e:
                    print(f"Error reading JSON file: {e}")
                    time.sleep(0.1)
                    continue'''
        )
    ]
    
    fixed_files = []
    
    for file_path in visualizer_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply replacements
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            
            # If content changed, write it back
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"Fixed: {file_path}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nFixed {len(fixed_files)} visualizer files:")
    for file_path in fixed_files:
        print(f"  - {file_path}")

if __name__ == "__main__":
    fix_visualizer_data_reading() 