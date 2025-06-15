import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from typing import Optional, Dict, Any
import time

class BaseVisualProcess:
    """Base class for all visual processes in the DAWN system."""
    
    def __init__(self, name: str, width: int = 800, height: int = 600):
        self.name = name
        self.width = width
        self.height = height
        self.is_active = False
        self.last_update = 0
        self.frame_count = 0
        self.fps = 0
        self._frame = np.zeros((height, width, 3), dtype=np.uint8)
        self._metadata: Dict[str, Any] = {}
    
    def update(self, dt: float) -> None:
        """Update the visual process state.
        
        Args:
            dt: Time delta since last update in seconds
        """
        self.last_update = time.time()
        self.frame_count += 1
        self._update_impl(dt)
    
    def _update_impl(self, dt: float) -> None:
        """Implementation of update logic. Override this in subclasses."""
        pass
    
    def capture_frame(self) -> str:
        """Capture the current frame and return as base64 encoded PNG.
        
        Returns:
            str: Base64 encoded PNG image
        """
        # Convert frame to PIL Image
        image = Image.fromarray(cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB))
        
        # Save to BytesIO buffer
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        
        # Convert to base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get current process metadata.
        
        Returns:
            Dict containing process metadata
        """
        return {
            'name': self.name,
            'is_active': self.is_active,
            'fps': self.fps,
            'frame_count': self.frame_count,
            'last_update': self.last_update,
            **self._metadata
        }
    
    def start(self) -> None:
        """Start the visual process."""
        self.is_active = True
        self.frame_count = 0
        self.last_update = time.time()
    
    def stop(self) -> None:
        """Stop the visual process."""
        self.is_active = False
    
    def reset(self) -> None:
        """Reset the visual process state."""
        self._frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.frame_count = 0
        self.fps = 0
        self._metadata = {}
    
    def set_size(self, width: int, height: int) -> None:
        """Set the output frame size.
        
        Args:
            width: New width in pixels
            height: New height in pixels
        """
        self.width = width
        self.height = height
        self._frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    def _update_fps(self, dt: float) -> None:
        """Update FPS calculation.
        
        Args:
            dt: Time delta since last update in seconds
        """
        if dt > 0:
            self.fps = 1.0 / dt 