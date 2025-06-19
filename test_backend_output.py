#!/usr/bin/env python3
"""
Simple test to check if backend outputs JSON data in CLI mode
"""

import subprocess
import sys
import time

def test_backend_output():
    print("Testing backend CLI mode output...")
    
    # Start backend in CLI mode
    cmd = [
        "/root/miniconda3/envs/dawn/bin/python", 
        "backend/local_main.py", 
        "--stdout-ticks", 
        "--interval", "0.1"
    ]
    
    try:
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        print(f"Backend started with PID: {process.pid}")
        
        # Wait a bit for initialization
        time.sleep(3)
        
        # Try to read output for 10 seconds
        start_time = time.time()
        lines_read = 0
        
        while time.time() - start_time < 10:
            if process.poll() is not None:
                print(f"Backend process exited with code: {process.returncode}")
                break
                
            # Try to read a line
            try:
                line = process.stdout.readline()
                if line:
                    lines_read += 1
                    print(f"Line {lines_read}: {line.strip()}")
                    
                    # Try to parse as JSON
                    try:
                        import json
                        data = json.loads(line.strip())
                        print(f"✅ Valid JSON: {type(data)}")
                    except json.JSONDecodeError:
                        print(f"❌ Not valid JSON: {line.strip()}")
                        
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error reading output: {e}")
                break
        
        if lines_read == 0:
            print("❌ No output received from backend")
            
        # Check stderr for any errors
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Stderr output: {stderr_output}")
            
    except Exception as e:
        print(f"Error starting backend: {e}")
    finally:
        # Clean up
        if process.poll() is None:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    test_backend_output() 