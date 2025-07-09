#!/usr/bin/env python3
"""
DAWN Queue Communication Demo
Demonstrates the queue.Queue() bridge between tick engine and GUI
"""

import sys
import os
import time
import queue
import threading
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from tick_engine.core_tick import CoreTickManager

def demonstrate_queue_injection():
    """Demonstrate queue-based data injection"""
    print("🧪 DAWN Queue Communication Demonstration")
    print("=" * 50)
    print("This demo shows how the tick engine pushes data to a queue")
    print("and how the GUI polls the queue for real-time updates.")
    print()
    
    # Create shared queue
    data_queue = queue.Queue(maxsize=50)
    
    # Create tick manager
    print("🔧 Creating CoreTickManager...")
    tick_manager = CoreTickManager(tick_interval=0.3, queue_maxsize=50)
    tick_manager.data_queue = data_queue
    tick_manager.tick_engine.data_queue = data_queue
    
    # Start tick engine
    print("🚀 Starting tick engine...")
    tick_manager.start()
    
    # Simulate GUI polling behavior
    print("🖥️  Simulating GUI queue polling...")
    print("📊 Monitoring queue for 10 seconds...")
    print()
    
    start_time = time.time()
    tick_count = 0
    
    try:
        while time.time() - start_time < 10.0:
            try:
                # Poll queue like GUI does
                data = data_queue.get_nowait()
                tick_count += 1
                
                # Display key data like GUI would
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] 📨 GUI received:")
                print(f"   Heat: {data['heat']}% | Zone: {data['zone']} | Mood: {data['mood']}")
                print(f"   SCUP: {data['scup']:.3f} | Entropy: {data['entropy']:.3f}")
                print(f"   Tick: {data['tick']}")
                print(f"   Sigils: {len(data['sigils'])} active")
                print()
                
                # Simulate GUI processing time
                time.sleep(0.1)
                
            except queue.Empty:
                # No data available - continue polling
                time.sleep(0.05)
    
    except KeyboardInterrupt:
        print("🛑 Demo interrupted")
    
    finally:
        print(f"✅ Demo complete - processed {tick_count} ticks")
        print(f"📊 Average rate: {tick_count/10.0:.1f} ticks/second")
        tick_manager.stop()
        print("🛑 Tick engine stopped")

def main():
    """Main demonstration"""
    print("🌅 DAWN Queue Communication System Demo")
    print("Demonstrating thread-safe data transfer between tick engine and GUI")
    print()
    
    try:
        # Demo: Live queue communication
        demonstrate_queue_injection()
        
        print("\n" + "=" * 50)
        print("🎯 Key Features Demonstrated:")
        print("✅ Thread-safe queue.Queue() communication")
        print("✅ Tick engine pushes data every ~0.5s")
        print("✅ GUI polls queue every 100ms")
        print("✅ Non-blocking queue.get_nowait() with error handling")
        print("✅ Real-time cognitive data streaming")
        print("✅ Complete separation of tick and GUI threads")
        print("\n🚀 Ready to run: python launch_dawn_gui.py")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main() 