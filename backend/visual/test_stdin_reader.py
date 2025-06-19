#!/usr/bin/env python3
"""
Simple test script to verify stdin piping from backend
"""

import sys
import json
import time

def main():
    print("Test stdin reader started", file=sys.stderr)
    print("Waiting for JSON data from stdin...", file=sys.stderr)
    
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
                
            try:
                data = json.loads(line.strip())
                print(f"Received tick {data.get('tick', 'unknown')}: {json.dumps(data, indent=2)}", file=sys.stderr)
                
                # Save to a test file
                with open("test_output.json", "w") as f:
                    json.dump(data, f, indent=2)
                    
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error processing data: {e}", file=sys.stderr)
                
    except KeyboardInterrupt:
        print("Test stdin reader stopped", file=sys.stderr)

if __name__ == "__main__":
    main() 