#!/usr/bin/env python3
"""Check for null bytes in files"""

import os

files_to_check = [
    'mood/mood_engine.py',
    'backend/core/dawn_central.py', 
    'consciousness/dawn_tick_state_writer.py'
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            null_count = data.count(b'\x00')
            print(f"{file_path}: {null_count} null bytes")
            
            if null_count > 0:
                print(f"  First null byte at position: {data.find(b'\\x00')}")
                
        except Exception as e:
            print(f"{file_path}: Error - {e}")
    else:
        print(f"{file_path}: File not found") 