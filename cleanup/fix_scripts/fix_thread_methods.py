#!/usr/bin/env python3
"""
Fix thread method names and ensure proper data reading
"""

import os
import re
import glob

def fix_thread_methods():
    """Fix thread method names and data reading"""
    
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
        # Fix thread target method name
        (
            r'threading\.Thread\(target=self\.read_stdin_data, daemon=True\)',
            'threading.Thread(target=self.read_json_data, daemon=True)'
        ),
        
        # Fix thread target method name (alternative pattern)
        (
            r'Thread\(target=self\.read_stdin_data',
            'Thread(target=self.read_json_data'
        ),
        
        # Add proper data reading in update_visualization
        (
            r'def update_visualization\(self, frame\):',
            '''def update_visualization(self, frame):
        """Animation update function"""
        try:
            # Read data from JSON file
            data = self.read_latest_json_data()
            
            if data is None:
                # Use simulated data if no real data available
                data = {
                    'tick': frame,
                    'mood': {'valence': 0.5 + 0.2 * np.sin(frame * 0.05)},
                    'entropy': {'total_entropy': 0.5 + 0.2 * np.sin(frame * 0.03)},
                    'thermal_state': {'heat_level': 0.3 + 0.1 * np.cos(frame * 0.04)},
                    'scup': {'schema': 0.5, 'coherence': 0.5, 'utility': 0.5, 'pressure': 0.5}
                }'''
        ),
        
        # Add read_latest_json_data method
        (
            r'def update_visualization\(self, frame\):',
            '''def read_latest_json_data(self):
        """Read the latest data from JSON file"""
        json_file = "/tmp/dawn_tick_data.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line:
                            return json.loads(last_line)
            except Exception as e:
                print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

    def update_visualization(self, frame):'''
        ),
        
        # Fix data reading in run method
        (
            r'while not self\.data_queue\.empty\(\):\s+data = self\.data_queue\.get\(\)',
            '''# Read from JSON file
                data = self.read_latest_json_data()
                if data is None:
                    time.sleep(0.1)
                    continue'''
        ),
        
        # Add proper imports if missing
        (
            r'import json',
            '''import json
import os'''
        ),
        
        # Fix data reading in main loop
        (
            r'data = self\.data_queue\.get\(\)',
            '''data = self.read_latest_json_data()
                if data is None:
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
    fix_thread_methods() 