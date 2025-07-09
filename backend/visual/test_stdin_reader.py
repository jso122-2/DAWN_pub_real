#!/usr/bin/env python3
"""
Simple test script to verify stdin piping from backend
"""

import sys
import json
import os
import os
import os
import os
import time

def main():
    print("Test stdin reader started", file=sys.stderr)
    print("Waiting for JSON data from stdin...", file=sys.stderr)

        while True:
            # Read from JSON file instead of stdin
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
                        line = lines[-1].strip()
            if not line:
                break

                data = json.loads(line.strip())
                print(f"Received tick {data.get('tick', 'unknown')}: {json.dumps(data, indent=2)}", file=sys.stderr)
                
                # Save to a test file
                with open("test_output.json", "w") as f:
                    json.dump(data, f, indent=2)
                    
                print(f"Invalid JSON: {e}", file=sys.stderr)
                print(f"Error processing data: {e}", file=sys.stderr)
                
        print("Test stdin reader stopped", file=sys.stderr)

if __name__ == "__main__":
    main() 