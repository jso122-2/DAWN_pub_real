#!/usr/bin/env python3
"""
DAWN Tick Engine Runner
======================
This script launches both the DAWN Tick Engine and its Streamlit interface.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import logging
import signal
import atexit
import re
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dawn_runner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('dawn_runner')

def get_local_ip():
    """Get the local IP address"""
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def setup_directories():
    """Ensure required directories exist"""
    directories = ['logs', 'data', 'cache', 'state']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

def run_engine():
    """Run the DAWN Tick Engine"""
    try:
        # Start the boot sequence
        boot_process = subprocess.Popen(
            [sys.executable, 'boot/boot_orchestrator.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for boot sequence to complete
        while True:
            output = boot_process.stdout.readline()
            if output == '' and boot_process.poll() is not None:
                break
            if output:
                logger.info(output.strip())
        
        if boot_process.returncode != 0:
            error = boot_process.stderr.read()
            logger.error(f"Boot sequence failed: {error}")
            return False
            
        logger.info("✅ Boot sequence completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to start engine: {str(e)}")
        return False

def run_streamlit():
    """Run the Streamlit interface"""
    try:
        # Start Streamlit
        streamlit_process = subprocess.Popen(
            ['streamlit', 'run', 'streamlit1.py', '--server.address', 'localhost'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait for Streamlit to start and capture the URL
        local_ip = get_local_ip()
        urls_printed = False
        
        while True:
            output = streamlit_process.stdout.readline()
            if output == '' and streamlit_process.poll() is not None:
                break
                
            if output:
                # Print all Streamlit output
                print(output.strip())
                
                # Look for URL patterns
                if not urls_printed:
                    if "Network URL" in output or "Local URL" in output:
                        print("\n" + "="*50)
                        print("🌐 STREAMLIT INTERFACE URLS:")
                        print("="*50)
                        print(f"Local URL: http://localhost:8501")
                        print(f"Network URL: http://{local_ip}:8501")
                        print("="*50 + "\n")
                        urls_printed = True
                
                # Check for errors
                if "Error" in output or "Exception" in output:
                    logger.error(f"Streamlit error: {output.strip()}")
                    return False
        
        if streamlit_process.poll() is not None:
            error = streamlit_process.stderr.read()
            logger.error(f"Streamlit failed to start: {error}")
            return False
            
        logger.info("✅ Streamlit interface started")
        return streamlit_process
        
    except Exception as e:
        logger.error(f"Failed to start Streamlit: {str(e)}")
        return False

def cleanup(processes):
    """Cleanup function to ensure proper shutdown"""
    logger.info("Shutting down DAWN...")
    for process in processes:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

def main():
    """Main entry point"""
    try:
        # Setup directories
        setup_directories()
        
        # Run the engine
        if not run_engine():
            logger.error("Failed to start DAWN Tick Engine")
            return 1
            
        # Run Streamlit
        streamlit_process = run_streamlit()
        if not streamlit_process:
            logger.error("Failed to start Streamlit interface")
            return 1
            
        # Register cleanup
        processes = [streamlit_process]
        atexit.register(cleanup, processes)
        
        # Keep the script running
        logger.info("DAWN is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 