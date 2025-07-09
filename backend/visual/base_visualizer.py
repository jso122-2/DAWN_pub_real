"""
Base Visualizer class for DAWN visualization components
"""

import base64
import io
import json
import os
import os
import os
import os
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

logger = logging.getLogger(__name__)

class BaseVisualizer(ABC):
    """Base class for all DAWN visualizers"""
    
    def __init__(self, name: str = "BaseVisualizer"):
        self.name = name
        self.is_active = False
        self.data_source: Optional[Callable[[], Dict[str, Any]]] = None
        self.update_interval = 1.0  # seconds
        self.last_update = 0.0
        self.colors = {
            'bg': '#000000',
            'fg': '#00ff41',
            'grid': '#1a1a1a',
            'accent': '#00cc33',
            'warning': '#ffb000',
            'error': '#ff0040',
            'text': '#f0f0f0'
        }
        self.fig_size = (8, 6)
        self.dpi = 100
        self.frame_count = 0
        self.start_time = time.time()
        self.is_running = True
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    def update(self, data: Dict[str, Any]) -> None:
        """Update the visualization with new data"""
        pass
    
    @abstractmethod
    def render(self) -> None:
        """Render the current visualization state"""
        pass
    
    def start(self) -> None:
        """Start the visualization"""
        self.is_active = True
        logger.info(f"{self.name} started")
    
    def stop(self) -> None:
        """Stop the visualization"""
        self.is_active = False
        logger.info(f"{self.name} stopped")
    
    def set_data_source(self, data_source: Callable[[], Dict[str, Any]]) -> None:
        """Set the data source function for this visualizer"""
        self.data_source = data_source
    
    def set_update_interval(self, interval: float) -> None:
        """Set the update interval in seconds"""
        self.update_interval = interval
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the visualizer"""
        return {
            "name": self.name,
            "is_active": self.is_active,
            "update_interval": self.update_interval,
            "last_update": self.last_update
        }
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.stop()
        logger.info(f"{self.name} cleaned up")

    def setup_plot(self, fig=None, ax=None):
        if fig is None or ax is None:
            fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        fig.patch.set_facecolor(self.colors['bg'])
        ax.set_facecolor(self.colors['bg'])
        ax.spines['bottom'].set_color(self.colors['fg'])
        ax.spines['top'].set_color(self.colors['fg'])
        ax.spines['left'].set_color(self.colors['fg'])
        ax.spines['right'].set_color(self.colors['fg'])
        ax.tick_params(colors=self.colors['text'])
        ax.xaxis.label.set_color(self.colors['text'])
        ax.yaxis.label.set_color(self.colors['text'])
        ax.title.set_color(self.colors['text'])
        ax.grid(True, color=self.colors['grid'], linestyle='--', alpha=0.3)
        return fig, ax

    def to_base64(self, fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', facecolor=self.colors['bg'], edgecolor='none', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"

    @abstractmethod
    def generate(self, data):
        pass

    def _encode_frame(self, image: Image.Image) -> str:
        """Encode an image to base64 string."""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def _create_frame_data(self, image: Image.Image, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a frame data dictionary and encode it as JSON."""
        frame_data = {
            "frame": self._encode_frame(image),
            "timestamp": time.time(),
            "frame_count": self.frame_count,
            "metadata": metadata or {}
        }
        return json.dumps(frame_data)

    def run(self):
        """Main loop for the visualizer."""
        try:
            while self.is_running:
                self.generate()
                frame = self.render()
                frame_data = self._create_frame_data(frame)
                print(frame_data, flush=True)  # Print to stdout for the server to capture
                self.frame_count += 1
                time.sleep(1/30)  # Target 30 FPS
        except KeyboardInterrupt:
            logger.info("Visualizer stopped by user")
        except Exception as e:
            logger.error(f"Error in visualizer: {str(e)}")
        finally:
            self.cleanup()

    @staticmethod
    def create_gradient_background(width: int, height: int, color1: tuple, color2: tuple) -> Image.Image:
        """Create a gradient background."""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        for y in range(height):
            for x in range(width):
                # Calculate gradient
                r = int(color1[0] * (1 - y/height) + color2[0] * (y/height))
                g = int(color1[1] * (1 - y/height) + color2[1] * (y/height))
                b = int(color1[2] * (1 - y/height) + color2[2] * (y/height))
                pixels[x, y] = (r, g, b)
        
        return image

    @staticmethod
    def draw_text(image: Image.Image, text: str, position: tuple, color: tuple = (255, 255, 255), 
                 font_size: int = 12) -> Image.Image:
        """Draw text on the image."""
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("JetBrainsMono-Regular.ttf", font_size)
        except:
            font = ImageFont.load_default()
        draw.text(position, text, fill=color, font=font)
        return image

    @staticmethod
    def create_heatmap(data: np.ndarray, width: int, height: int, 
                      min_val: float = 0, max_val: float = 1) -> Image.Image:
        """Create a heatmap from 2D data."""
        # Normalize data
        data = (data - min_val) / (max_val - min_val)
        data = np.clip(data, 0, 1)
        
        # Create RGB image
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Color mapping (blue to red)
        image[..., 0] = (data * 255).astype(np.uint8)  # Red
        image[..., 1] = 0  # Green
        image[..., 2] = ((1 - data) * 255).astype(np.uint8)  # Blue
        
        return Image.fromarray(image)

    @staticmethod
    def create_vector_field(vectors: np.ndarray, width: int, height: int, 
                          scale: float = 1.0, color: tuple = (0, 255, 136)) -> Image.Image:
        """Create a vector field visualization."""
        image = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw vectors
        for y in range(0, height, 20):
            for x in range(0, width, 20):
                if y < vectors.shape[0] and x < vectors.shape[1]:
                    vx, vy = vectors[y, x]
                    end_x = int(x + vx * scale)
                    end_y = int(y + vy * scale)
                    draw.line([(x, y), (end_x, end_y)], fill=color, width=1)
        
        return image 