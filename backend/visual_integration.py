"""
DAWN Visual Integration System
Integrates the run_visuals.sh script with the main DAWN engine
"""

import asyncio
import logging
import os
import subprocess
import signal
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class VisualMode(Enum):
    """Visual system operating modes"""
    DISABLED = "disabled"
    DEMO = "demo"
    STDIN = "stdin"
    AUTO = "auto"

@dataclass
class VisualConfig:
    """Configuration for visual system"""
    mode: VisualMode = VisualMode.STDIN
    interval_ms: int = 100
    buffer_size: int = 100
    log_dir: str = "visual/logs"
    output_dir: Optional[str] = None
    kill_existing: bool = True
    max_processes: int = 8

class VisualIntegrationManager:
    """
    Manages integration between the main DAWN engine and the visual system
    """
    
    def __init__(self, config: VisualConfig = None):
        self.config = config or VisualConfig()
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
        self.script_path = Path(__file__).parent.parent / "visual" / "run_visuals.sh"
        self.pid_file = "visualization_pids.txt"
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Handle Windows/WSL path conversion
        if os.name == 'nt':  # Windows
            # Convert to Windows path if needed
            if str(self.script_path).startswith('\\\\wsl$'):
                # Keep WSL path as is for subprocess
                pass
            else:
                # Convert to Windows path
                self.script_path = Path(str(self.script_path).replace('/', '\\'))
        
        # Validate script exists
        if not self.script_path.exists():
            raise FileNotFoundError(f"Visual script not found: {self.script_path}")
        
        # Make script executable (works on Unix-like systems)
        try:
            if os.name != 'nt':  # Not Windows
                self.script_path.chmod(0o755)
        except Exception as e:
            logger.warning(f"Could not make script executable: {e}")
        
        logger.info(f"Visual integration manager initialized with script: {self.script_path}")
    
    def start_visual_system(self) -> bool:
        """
        Start the visual system using the run_visuals.sh script
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_running:
            logger.warning("Visual system already running")
            return True
        
        try:
            # Build command arguments
            if os.name == 'nt':  # Windows
                # Use bash to run the script on Windows/WSL
                cmd = ["bash", str(self.script_path)]
            else:
                cmd = [str(self.script_path)]
            
            # Add configuration options
            if self.config.mode == VisualMode.DEMO:
                cmd.extend(["--source", "demo"])
            elif self.config.mode == VisualMode.STDIN:
                cmd.extend(["--source", "stdin"])
            
            cmd.extend(["--interval", str(self.config.interval_ms)])
            cmd.extend(["--buffer", str(self.config.buffer_size)])
            cmd.extend(["--log-dir", self.config.log_dir])
            
            if self.config.output_dir:
                cmd.extend(["--output-dir", self.config.output_dir])
            
            if self.config.kill_existing:
                cmd.append("--kill-existing")
            
            logger.info(f"Starting visual system with command: {' '.join(cmd)}")
            
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.is_running = True
            
            # Start monitoring thread
            self._start_monitor_thread()
            
            # Wait a moment to see if it starts successfully
            time.sleep(2)
            
            if self.process.poll() is None:
                logger.info(f"Visual system started successfully with PID: {self.process.pid}")
                return True
            else:
                stdout, stderr = self.process.communicate()
                logger.error(f"Visual system failed to start. stdout: {stdout}, stderr: {stderr}")
                self.is_running = False
                return False
                
        except Exception as e:
            logger.error(f"Error starting visual system: {e}")
            self.is_running = False
            return False
    
    def stop_visual_system(self) -> bool:
        """
        Stop the visual system gracefully
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        if not self.is_running:
            logger.info("Visual system not running")
            return True
        
        try:
            logger.info("Stopping visual system...")
            
            # Stop monitoring thread
            self._stop_event.set()
            if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=5)
            
            # Kill the main process
            if self.process:
                # Try graceful shutdown first
                self.process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning("Visual system did not terminate gracefully, forcing kill")
                    self.process.kill()
                    self.process.wait()
            
            # Clean up PID file
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            
            self.is_running = False
            logger.info("Visual system stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping visual system: {e}")
            return False
    
    def _start_monitor_thread(self):
        """Start the monitoring thread"""
        self._monitor_thread = threading.Thread(
            target=self._monitor_process,
            name="VisualMonitor",
            daemon=True
        )
        self._monitor_thread.start()
    
    def _monitor_process(self):
        """Monitor the visual system process"""
        logger.info("Visual system monitor started")
        
        while not self._stop_event.is_set() and self.process:
            try:
                # Check if process is still running
                if self.process.poll() is not None:
                    logger.warning("Visual system process has terminated")
                    self.is_running = False
                    break
                
                # Read output if available
                if self.process.stdout:
                    line = self.process.stdout.readline()
                    if line:
                        logger.debug(f"Visual system: {line.strip()}")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in visual system monitor: {e}")
                break
        
        logger.info("Visual system monitor stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the visual system
        
        Returns:
            Dict containing status information
        """
        status = {
            "is_running": self.is_running,
            "config": {
                "mode": self.config.mode.value,
                "interval_ms": self.config.interval_ms,
                "buffer_size": self.config.buffer_size,
                "log_dir": self.config.log_dir,
                "output_dir": self.config.output_dir
            },
            "process": {
                "pid": self.process.pid if self.process else None,
                "returncode": self.process.returncode if self.process else None
            }
        }
        
        # Check if PID file exists and read PIDs
        if os.path.exists(self.pid_file):
            try:
                with open(self.pid_file, 'r') as f:
                    pids = [int(line.strip()) for line in f if line.strip()]
                status["visual_processes"] = pids
            except Exception as e:
                logger.error(f"Error reading PID file: {e}")
                status["visual_processes"] = []
        else:
            status["visual_processes"] = []
        
        return status
    
    def update_config(self, **kwargs) -> bool:
        """
        Update the visual system configuration
        
        Args:
            **kwargs: Configuration parameters to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    if key == "mode" and isinstance(value, str):
                        value = VisualMode(value)
                    setattr(self.config, key, value)
                    logger.info(f"Updated visual config: {key} = {value}")
                else:
                    logger.warning(f"Unknown config parameter: {key}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating visual config: {e}")
            return False
    
    def restart_visual_system(self) -> bool:
        """
        Restart the visual system with current configuration
        
        Returns:
            bool: True if restarted successfully, False otherwise
        """
        logger.info("Restarting visual system...")
        
        if not self.stop_visual_system():
            logger.error("Failed to stop visual system for restart")
            return False
        
        time.sleep(2)  # Give time for cleanup
        
        return self.start_visual_system()

# Global instance
_visual_manager: Optional[VisualIntegrationManager] = None

def get_visual_manager(config: VisualConfig = None) -> VisualIntegrationManager:
    """
    Get or create the global visual integration manager
    
    Args:
        config: Optional configuration to use for initialization
        
    Returns:
        VisualIntegrationManager instance
    """
    global _visual_manager
    
    if _visual_manager is None:
        _visual_manager = VisualIntegrationManager(config)
    
    return _visual_manager

def start_visual_system(config: VisualConfig = None) -> bool:
    """
    Start the visual system
    
    Args:
        config: Optional configuration
        
    Returns:
        bool: True if started successfully
    """
    manager = get_visual_manager(config)
    return manager.start_visual_system()

def stop_visual_system() -> bool:
    """
    Stop the visual system
    
    Returns:
        bool: True if stopped successfully
    """
    if _visual_manager:
        return _visual_manager.stop_visual_system()
    return True

def get_visual_status() -> Dict[str, Any]:
    """
    Get visual system status
    
    Returns:
        Dict containing status information
    """
    if _visual_manager:
        return _visual_manager.get_status()
    return {"is_running": False, "error": "Visual manager not initialized"}

# Integration with main DAWN system
class DAWNVisualIntegration:
    """
    Integration class for use in the main DAWN system
    """
    
    def __init__(self, dawn_central):
        self.dawn_central = dawn_central
        self.visual_manager = get_visual_manager()
        
        # Configure visual system based on DAWN state
        self._configure_for_dawn()
    
    def _configure_for_dawn(self):
        """Configure visual system based on DAWN configuration"""
        # Set up output directory based on DAWN session
        output_dir = f"visual/outputs_{time.strftime('%Y-%m-%d')}"
        
        config = VisualConfig(
            mode=VisualMode.STDIN,
            interval_ms=100,
            buffer_size=100,
            log_dir="visual/logs",
            output_dir=output_dir,
            kill_existing=True
        )
        
        self.visual_manager.update_config(**config.__dict__)
    
    def start(self) -> bool:
        """Start visual integration"""
        logger.info("Starting DAWN visual integration...")
        return self.visual_manager.start_visual_system()
    
    def stop(self) -> bool:
        """Stop visual integration"""
        logger.info("Stopping DAWN visual integration...")
        return self.visual_manager.stop_visual_system()
    
    def get_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return self.visual_manager.get_status()
    
    def update_dawn_state(self, state_data: Dict[str, Any]):
        """
        Update visual system with DAWN state data
        This can be called from the main tick cycle
        """
        # The visual system reads from stdin, so we could potentially
        # pipe DAWN state data to the visual processes
        pass 