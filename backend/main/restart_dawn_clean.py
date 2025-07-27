#!/usr/bin/env python3
"""
DAWN Clean Restart Script
Stops all running servers and restarts with latest code
"""

import os
import sys
import subprocess
import time
import signal
import psutil
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.demo_advanced_consciousness import run_demo
from main.start_dawn_api import start_api
from main.run_kan_server import run_kan
from main.integrate_kan_cairrn import integrate
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def kill_process_by_port(port):
    """Kill any process using the specified port"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.info['connections'] or []:
                    if conn.laddr.port == port:
                        logger.info(f"🔪 Killing process {proc.info['name']} (PID: {proc.info['pid']}) using port {port}")
                        proc.kill()
                        proc.wait(timeout=3)
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
    except Exception as e:
        logger.error(f"Error killing process on port {port}: {e}")
    return False

def kill_dawn_processes():
    """Kill all DAWN-related processes"""
    processes_to_kill = [
        'simple_websocket_server.py',
        'python',
        'node',
        'vite'
    ]
    
    killed_any = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if any(target in cmdline.lower() for target in ['dawn', 'websocket', 'vite', 'localhost:8001', 'localhost:5173']):
                logger.info(f"🔪 Killing DAWN process: {proc.info['name']} (PID: {proc.info['pid']})")
                proc.kill()
                killed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if killed_any:
        time.sleep(2)  # Give processes time to cleanup
    
    return killed_any

def clear_caches():
    """Clear various caches"""
    logger.info("🧹 Clearing caches...")
    
    # Clear node_modules/.vite cache if it exists
    vite_cache_path = "node_modules/.vite"
    if os.path.exists(vite_cache_path):
        import shutil
        shutil.rmtree(vite_cache_path)
        logger.info("✅ Cleared Vite cache")
    
    # Clear browser cache (instructions)
    logger.info("🌐 Please clear your browser cache:")
    logger.info("   - Chrome/Edge: Ctrl+Shift+R (hard refresh)")
    logger.info("   - Firefox: Ctrl+F5")
    logger.info("   - Or open DevTools (F12) > Application > Storage > Clear Storage")

def start_websocket_server():
    """Start the WebSocket server"""
    logger.info("🚀 Starting WebSocket server...")
    
    # Kill any process using port 8001
    kill_process_by_port(8001)
    
    # Start the server
    try:
        proc = subprocess.Popen([
            sys.executable, 'simple_websocket_server.py'
        ], cwd=os.getcwd())
        
        logger.info(f"✅ WebSocket server started (PID: {proc.pid})")
        time.sleep(2)  # Give it time to start
        return proc
    except Exception as e:
        logger.error(f"❌ Failed to start WebSocket server: {e}")
        return None

def start_vite_server():
    """Start the Vite development server"""
    logger.info("🚀 Starting Vite dev server...")
    
    # Kill any process using port 5173
    kill_process_by_port(5173)
    
    # Check if we have package.json
    if not os.path.exists('package.json'):
        logger.error("❌ No package.json found. Make sure you're in the right directory.")
        return None
    
    try:
        proc = subprocess.Popen([
            'npm', 'run', 'dev'
        ], cwd=os.getcwd())
        
        logger.info(f"✅ Vite server started (PID: {proc.pid})")
        return proc
    except Exception as e:
        logger.error(f"❌ Failed to start Vite server: {e}")
        logger.info("💡 Try running: npm install")
        return None

def main():
    """Main restart process"""
    logger.info("🌟 DAWN Clean Restart Process Started")
    
    # Step 1: Kill existing processes
    logger.info("🛑 Stopping existing servers...")
    kill_dawn_processes()
    
    # Step 2: Clear caches
    clear_caches()
    
    # Step 3: Start WebSocket server
    ws_proc = start_websocket_server()
    if not ws_proc:
        logger.error("❌ Failed to start WebSocket server")
        return False
    
    # Step 4: Start Vite server
    vite_proc = start_vite_server()
    if not vite_proc:
        logger.error("❌ Failed to start Vite server")
        return False
    
    logger.info("🎉 All servers started successfully!")
    logger.info("📡 WebSocket: ws://localhost:8001")
    logger.info("🌐 Frontend: http://localhost:5173")
    logger.info("🔄 Press Ctrl+C to stop all servers")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping servers...")
        if ws_proc:
            ws_proc.terminate()
        if vite_proc:
            vite_proc.terminate()
        logger.info("✅ All servers stopped")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1) 