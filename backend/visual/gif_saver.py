#!/usr/bin/env python3
"""
GIF Saver Utility for DAWN Visualizations
Handles saving matplotlib animations as GIF files with proper date formatting
"""

import os
import sys
from datetime import datetime
from typing import Optional, List
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
import logging

logger = logging.getLogger(__name__)

class GIFSaver:
    """Utility class for saving matplotlib animations as GIF files"""
    
    def __init__(self, output_dir: str, script_name: str):
        """
        Initialize GIF saver
        
        Args:
            output_dir: Base output directory
            script_name: Name of the visualization script (without .py)
        """
        self.output_dir = output_dir
        self.script_name = script_name
        self.date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Frame storage for GIF creation
        self.frames: List[Figure] = []
        self.save_interval = 10  # Save frame every N updates
        
    def get_gif_filename(self) -> str:
        """Generate GIF filename with date"""
        return f"{self.script_name}_{self.date_str}.gif"
    
    def get_gif_path(self) -> str:
        """Get full path for GIF file"""
        filename = self.get_gif_filename()
        return os.path.join(self.output_dir, filename)
    
    def save_frame(self, fig: Figure, frame_count: int) -> None:
        """
        Save current frame for GIF creation
        
        Args:
            fig: Matplotlib figure to save
            frame_count: Current frame number
        """
        if frame_count % self.save_interval == 0:
            # Create a copy of the figure to avoid modifying the original
            fig_copy = plt.figure(figsize=fig.get_size_inches())
            fig_copy.canvas.draw()
            
            # Copy the figure content
            for ax in fig.axes:
                ax_copy = fig_copy.add_subplot(ax.get_geometry()[0], ax.get_geometry()[1], ax.get_geometry()[2])
                ax_copy.set_xlim(ax.get_xlim())
                ax_copy.set_ylim(ax.get_ylim())
                ax_copy.set_title(ax.get_title())
                ax_copy.set_xlabel(ax.get_xlabel())
                ax_copy.set_ylabel(ax.get_ylabel())
                
                # Copy all artists (lines, patches, etc.)
                for artist in ax.get_children():
                    if hasattr(artist, 'get_data'):
                        # Handle lines
                        x_data, y_data = artist.get_data()
                        ax_copy.plot(x_data, y_data, color=artist.get_color(), 
                                   linewidth=artist.get_linewidth(), alpha=artist.get_alpha())
                    elif hasattr(artist, 'get_facecolor'):
                        # Handle patches
                        ax_copy.add_patch(artist)
            
            self.frames.append(fig_copy)
            
            # Keep only last 100 frames to manage memory
            if len(self.frames) > 100:
                self.frames.pop(0)
    
    def save_gif(self, fps: int = 10, dpi: int = 100) -> Optional[str]:
        """
        Save collected frames as GIF
        
        Args:
            fps: Frames per second for the GIF
            dpi: DPI for the output GIF
            
        Returns:
            Path to saved GIF file, or None if failed
        """
        if not self.frames:
            logger.warning("No frames to save as GIF")
            return None
        
        try:
            gif_path = self.get_gif_path()
            
            # Save the first frame as a test
            self.frames[0].savefig(gif_path, format='gif', dpi=dpi, 
                                 save_all=True, append_images=self.frames[1:],
                                 duration=1000//fps, loop=0)
            
            logger.info(f"GIF saved: {gif_path}")
            return gif_path
            
        except Exception as e:
            logger.error(f"Failed to save GIF: {e}")
            return None
    
    def save_animation_as_gif(self, anim: animation.FuncAnimation, 
                            fps: int = 10, dpi: int = 100) -> Optional[str]:
        """
        Save a matplotlib animation as GIF
        
        Args:
            anim: Matplotlib animation object
            fps: Frames per second for the GIF
            dpi: DPI for the output GIF
            
        Returns:
            Path to saved GIF file, or None if failed
        """
        try:
            gif_path = self.get_gif_path()
            
            # Save animation as GIF
            anim.save(gif_path, writer='pillow', fps=fps, dpi=dpi)
            
            logger.info(f"Animation GIF saved: {gif_path}")
            return gif_path
            
        except Exception as e:
            logger.error(f"Failed to save animation GIF: {e}")
            return None

def setup_gif_saver(script_name: str) -> GIFSaver:
    """
    Setup GIF saver using environment variables
    
    Args:
        script_name: Name of the script (without .py extension)
        
    Returns:
        Configured GIFSaver instance
    """
    # Get output directory from environment or use default
    output_dir = os.environ.get('DAWN_VISUAL_OUTPUT_DIR', 
                               f"backend/visual/outputs/{script_name}")
    
    return GIFSaver(output_dir, script_name)

def save_figure_as_gif(fig: Figure, script_name: str, 
                      output_dir: Optional[str] = None,
                      fps: int = 10, dpi: int = 100) -> Optional[str]:
    """
    Quick function to save a single figure as GIF
    
    Args:
        fig: Matplotlib figure
        script_name: Name of the script
        output_dir: Output directory (optional)
        fps: Frames per second
        dpi: DPI for output
        
    Returns:
        Path to saved GIF file, or None if failed
    """
    if output_dir is None:
        output_dir = os.environ.get('DAWN_VISUAL_OUTPUT_DIR', 
                                   f"backend/visual/outputs/{script_name}")
    
    saver = GIFSaver(output_dir, script_name)
    return saver.save_animation_as_gif(fig, fps, dpi) 