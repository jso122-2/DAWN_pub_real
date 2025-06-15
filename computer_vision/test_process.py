#!/usr/bin/env python3
"""
Simple test script for DAWN process management
This script can be started/stopped via the process manager API
"""

import time
import sys
import argparse
import signal

def signal_handler(signum, frame):
    print(f"🛑 Test process received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def main():
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='DAWN Test Process')
    parser.add_argument('--duration', type=int, default=30, help='Run duration in seconds')
    parser.add_argument('--interval', type=float, default=1.0, help='Print interval in seconds')
    parser.add_argument('--mode', type=str, default='default', help='Processing mode')
    
    args = parser.parse_args()
    
    print(f"🚀 DAWN Test Process Started")
    print(f"   Duration: {args.duration} seconds")
    print(f"   Interval: {args.interval} seconds")
    print(f"   Mode: {args.mode}")
    print(f"   PID: {os.getpid()}")
    
    start_time = time.time()
    tick_count = 0
    
    try:
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            if elapsed >= args.duration:
                print(f"✅ Test completed after {elapsed:.1f} seconds ({tick_count} ticks)")
                break
            
            tick_count += 1
            cpu_sim = 10 + (tick_count % 20)  # Simulate varying CPU usage
            memory_sim = 50 + (tick_count % 30)  # Simulate varying memory usage
            
            print(f"🔄 Tick {tick_count}: {elapsed:.1f}s elapsed, simulated CPU: {cpu_sim}%, Memory: {memory_sim}MB")
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print(f"🛑 Test process interrupted by user")
    except Exception as e:
        print(f"❌ Test process error: {e}")
    finally:
        print(f"🏁 Test process finished. Total ticks: {tick_count}")

if __name__ == "__main__":
    import os
    main() 