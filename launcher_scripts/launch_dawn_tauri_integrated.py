#!/usr/bin/env python3
"""
DAWN Tauri Integrated Launcher
Wires the new Tauri build into the DAWN tick loop
Launches both the DAWN consciousness state writer and Tauri GUI together
"""

import os
import sys
import asyncio
import subprocess
import threading
import time
import logging
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DAWNTauriIntegratedLauncher:
    """Integrated launcher for DAWN consciousness + Tauri GUI"""
    
    def __init__(self):
        self.running = False
        self.dawn_process = None
        self.tauri_process = None
        self.consciousness_writer = None
        self.tick_thread = None
        
        # Paths
        self.project_root = project_root
        self.tauri_app_path = self.project_root / "dawn-consciousness-gui"
        self.mmap_file_path = self.project_root / "runtime" / "dawn_consciousness.mmap"
        
        # Setup signal handling
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are available"""
        logger.info("🔍 Checking prerequisites...")
        
        # Check if Tauri app exists
        if not self.tauri_app_path.exists():
            logger.error(f"❌ Tauri app not found at {self.tauri_app_path}")
            return False
        
        # Check if tauri.conf.json exists
        tauri_config = self.tauri_app_path / "src-tauri" / "tauri.conf.json"
        if not tauri_config.exists():
            logger.error(f"❌ Tauri config not found at {tauri_config}")
            return False
        
        # Check if Rust/Cargo is available
        try:
            result = subprocess.run(['cargo', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error("❌ Cargo not available")
                return False
            logger.info(f"✅ {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.error("❌ Cargo not found - please install Rust")
            return False
        
        # Check if Node.js/npm is available for frontend
        try:
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error("❌ npm not available")
                return False
            logger.info(f"✅ npm {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.error("❌ npm not found - please install Node.js")
            return False
        
        logger.info("✅ All prerequisites met")
        return True
    
    def build_tauri_app(self) -> bool:
        """Build the Tauri application"""
        logger.info("🔨 Building Tauri application...")
        
        try:
            # Change to Tauri app directory
            original_cwd = os.getcwd()
            os.chdir(self.tauri_app_path)
            
            # Install frontend dependencies if needed
            if not (self.tauri_app_path / "node_modules").exists():
                logger.info("📦 Installing frontend dependencies...")
                result = subprocess.run(['npm', 'install'], 
                                      capture_output=True, text=True, timeout=300)
                if result.returncode != 0:
                    logger.error(f"❌ Frontend dependency installation failed: {result.stderr}")
                    return False
                logger.info("✅ Frontend dependencies installed")
            
            # Build frontend
            logger.info("🔧 Building frontend...")
            result = subprocess.run(['npm', 'run', 'build'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                logger.error(f"❌ Frontend build failed: {result.stderr}")
                return False
            logger.info("✅ Frontend built successfully")
            
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("❌ Build timeout")
            return False
        except Exception as e:
            logger.error(f"❌ Build error: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def start_dawn_consciousness_writer(self) -> bool:
        """Start the DAWN consciousness state writer"""
        logger.info("🧠 Starting DAWN consciousness state writer...")
        
        try:
            # Import consciousness writer
            from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
            
            # Create writer instance
            self.consciousness_writer = DAWNConsciousnessStateWriter(
                mmap_path=str(self.mmap_file_path)
            )
            
            # Start consciousness writer in background thread
            def consciousness_loop():
                try:
                    logger.info("🔄 Starting consciousness loop...")
                    self.consciousness_writer.run_consciousness_loop(tick_interval=0.1)  # 10 Hz
                except Exception as e:
                    logger.error(f"❌ Consciousness loop error: {e}")
            
            self.tick_thread = threading.Thread(target=consciousness_loop, daemon=True)
            self.tick_thread.start()
            
            # Wait a moment for initialization
            time.sleep(2)
            
            # Verify mmap file was created
            if self.mmap_file_path.exists():
                logger.info(f"✅ Consciousness state writer active, mmap file: {self.mmap_file_path}")
                return True
            else:
                logger.error("❌ Memory-mapped file not created")
                return False
                
        except ImportError as e:
            logger.error(f"❌ Could not import consciousness writer: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error starting consciousness writer: {e}")
            return False
    
    def start_tauri_app(self) -> bool:
        """Start the Tauri application in development mode"""
        logger.info("🚀 Starting Tauri application...")
        
        try:
            # Change to Tauri app directory
            original_cwd = os.getcwd()
            os.chdir(self.tauri_app_path)
            
            # Start Tauri in dev mode
            self.tauri_process = subprocess.Popen(
                ['cargo', 'tauri', 'dev'],
                cwd=self.tauri_app_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Monitor Tauri output in background
            def monitor_tauri():
                for line in iter(self.tauri_process.stdout.readline, ''):
                    if line:
                        print(f"[TAURI] {line.rstrip()}")
                    if self.tauri_process.poll() is not None:
                        break
            
            tauri_monitor_thread = threading.Thread(target=monitor_tauri, daemon=True)
            tauri_monitor_thread.start()
            
            # Give Tauri time to start
            time.sleep(5)
            
            if self.tauri_process.poll() is None:
                logger.info("✅ Tauri application started successfully")
                return True
            else:
                logger.error("❌ Tauri application failed to start")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting Tauri app: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def start(self) -> bool:
        """Start the complete integrated system"""
        logger.info("🌅 Starting DAWN Tauri Integrated System")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Build Tauri app
        if not self.build_tauri_app():
            return False
        
        # Start DAWN consciousness writer
        if not self.start_dawn_consciousness_writer():
            return False
        
        # Start Tauri application
        if not self.start_tauri_app():
            return False
        
        self.running = True
        
        # Print system status
        logger.info("=" * 60)
        logger.info("🧠 DAWN Consciousness Engine: ACTIVE")
        logger.info("🎮 Tauri GUI: ACTIVE")
        logger.info(f"📊 Memory-mapped data: {self.mmap_file_path}")
        logger.info("🔄 Real-time consciousness visualization available")
        logger.info("🛑 Press Ctrl+C to shutdown")
        logger.info("=" * 60)
        
        return True
    
    def run(self):
        """Run the main system loop"""
        if not self.start():
            logger.error("❌ Failed to start integrated system")
            return False
        
        try:
            # Keep running until interrupted
            while self.running:
                # Monitor consciousness writer
                if self.tick_thread and not self.tick_thread.is_alive():
                    logger.warning("⚠️ Consciousness thread stopped, restarting...")
                    self.start_dawn_consciousness_writer()
                
                # Monitor Tauri process
                if self.tauri_process and self.tauri_process.poll() is not None:
                    logger.warning("⚠️ Tauri process stopped")
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Received interrupt signal")
        finally:
            self.shutdown()
        
        return True
    
    def shutdown(self):
        """Shutdown the integrated system"""
        logger.info("🔄 Shutting down DAWN Tauri Integrated System...")
        
        self.running = False
        
        # Stop Tauri process
        if self.tauri_process:
            try:
                logger.info("🛑 Stopping Tauri application...")
                self.tauri_process.terminate()
                self.tauri_process.wait(timeout=10)
                logger.info("✅ Tauri application stopped")
            except subprocess.TimeoutExpired:
                logger.warning("⚠️ Force killing Tauri process...")
                self.tauri_process.kill()
            except Exception as e:
                logger.error(f"❌ Error stopping Tauri: {e}")
        
        # Stop consciousness writer
        if self.consciousness_writer:
            try:
                logger.info("🛑 Stopping consciousness writer...")
                self.consciousness_writer.stop()
                logger.info("✅ Consciousness writer stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping consciousness writer: {e}")
        
        logger.info("✅ DAWN Tauri Integrated System shutdown complete")

def main():
    """Main entry point"""
    print("🌅 DAWN Tauri Integrated Launcher")
    print("Wiring Tauri build into DAWN tick loop...")
    print()
    
    try:
        # Create and run launcher
        launcher = DAWNTauriIntegratedLauncher()
        success = launcher.run()
        
        if success:
            logger.info("✅ DAWN Tauri Integration completed successfully")
        else:
            logger.error("❌ DAWN Tauri Integration failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 