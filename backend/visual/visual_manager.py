import time
from typing import Dict, List, Optional, Type
from .base_visual import BaseVisualProcess
import importlib
import os
import logging
import signal
import atexit
import sys

# Import GIF saver
from .gif_saver import setup_gif_saver

logger = logging.getLogger(__name__)

class VisualManager:
    """Manages all visual processes in the DAWN system."""
    
    def __init__(self):
        self.processes: Dict[str, BaseVisualProcess] = {}
        self.last_update = 0
        self._process_classes: Dict[str, Type[BaseVisualProcess]] = {}
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("visualmanager")

        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def register_process(self, process: BaseVisualProcess) -> None:
        """Register a visual process.
        
        Args:
            process: Visual process instance to register
        """
        self.processes[process.name] = process
        logger.info(f"Registered visual process: {process.name}")
    
    def unregister_process(self, name: str) -> None:
        """Unregister a visual process.
        
        Args:
            name: Name of process to unregister
        """
        if name in self.processes:
            self.processes[name].stop()
            del self.processes[name]
            logger.info(f"Unregistered visual process: {name}")
    
    def get_process(self, name: str) -> Optional[BaseVisualProcess]:
        """Get a registered process by name.
        
        Args:
            name: Name of process to get
            
        Returns:
            Process instance if found, None otherwise
        """
        return self.processes.get(name)
    
    def list_processes(self) -> List[Dict]:
        """Get list of all registered processes with their metadata.
        
        Returns:
            List of process metadata dictionaries
        """
        return [p.get_metadata() for p in self.processes.values()]
    
    def update_all(self) -> None:
        """Update all active visual processes."""
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        for process in self.processes.values():
            if process.is_active:
                try:
                    process.update(dt)
                except Exception as e:
                    logger.error(f"Error updating process {process.name}: {e}")
    
    def capture_frame(self, process_name: str) -> Optional[str]:
        """Capture a frame from a specific process.
        
        Args:
            process_name: Name of process to capture from
            
        Returns:
            Base64 encoded PNG image if successful, None otherwise
        """
        process = self.get_process(process_name)
        if process and process.is_active:
            try:
                return process.capture_frame()
            except Exception as e:
                logger.error(f"Error capturing frame from {process_name}: {e}")
        return None
    
    def start_process(self, name: str) -> bool:
        """Start a visual process.
        
        Args:
            name: Name of process to start
            
        Returns:
            True if process was started, False otherwise
        """
        process = self.get_process(name)
        if process:
            process.start()
            logger.info(f"Started visual process: {name}")
            return True
        return False
    
    def stop_process(self, name: str) -> bool:
        """Stop a visual process.
        
        Args:
            name: Name of process to stop
            
        Returns:
            True if process was stopped, False otherwise
        """
        process = self.get_process(name)
        if process:
            process.stop()
            logger.info(f"Stopped visual process: {name}")
            return True
        return False
    
    def load_process_modules(self, directory: str = "visual/processes") -> None:
        """Load all visual process modules from a directory.
        
        Args:
            directory: Directory containing process modules
        """
        try:
            # Get absolute path to processes directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            processes_dir = os.path.join(base_dir, directory)
            
            # Import all .py files in the directory
            for filename in os.listdir(processes_dir):
                if filename.endswith('.py') and not filename.startswith('__'):
                    module_name = filename[:-3]
                    try:
                        module = importlib.import_module(f"{directory.replace('/', '.')}.", module_name)
                        if hasattr(module, 'VisualProcess'):
                            self._process_classes[module_name] = module.VisualProcess
                            logger.info(f"Loaded visual process module: {module_name}")
                    except Exception as e:
                        logger.error(f"Error loading module {module_name}: {e}")
        except Exception as e:
            logger.error(f"Error loading process modules: {e}")
    
    def create_process(self, name: str, **kwargs) -> Optional[BaseVisualProcess]:
        """Create a new process instance from a loaded module.
        
        Args:
            name: Name of process class to instantiate
            **kwargs: Arguments to pass to process constructor
            
        Returns:
            New process instance if successful, None otherwise
        """
        if name in self._process_classes:
            try:
                process = self._process_classes[name](**kwargs)
                self.register_process(process)
                return process
            except Exception as e:
                logger.error(f"Error creating process {name}: {e}")
        return None

    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'animation') and self.animation is not None:
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
        except Exception as e:
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)