#!/usr/bin/env python3
"""
GIF Saver for DAWN Visualizations
Handles saving matplotlib animations as GIF files
"""

import os
import logging
from typing import Optional, List
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GIFSaver:
    """Handles saving matplotlib figures and animations as GIF files"""
    
    def __init__(self, output_dir: str, script_name: str):
        """
        Initialize GIF saver
        
        Args:
            output_dir: Directory to save GIF files
            script_name: Name of the script (for filename)
        """
        self.output_dir = output_dir
        self.script_name = script_name
        self.frames: List[Figure] = []
        self.save_interval = 5  # Save every 5 frames
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def get_gif_filename(self) -> str:
        """Generate GIF filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.script_name}_{timestamp}.gif"
    
    def get_gif_path(self) -> str:
        """Get full path for GIF file"""
        filename = self.get_gif_filename()
        return os.path.join(self.output_dir, filename)
    
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
        if anim is None:
            logger.error("No animation object provided to save_animation_as_gif.")
            return None
        
        try:
            gif_path = self.get_gif_path()
            
            # Try different writers in order of preference
            writers_to_try = ['pillow', 'imagemagick']
            
            for writer_name in writers_to_try:
                try:
                    logger.info(f"Trying to save with writer: {writer_name}")
                    
                    if writer_name == 'pillow':
                        # For pillow, we need to use a different approach
                        anim.save(gif_path, writer='pillow', fps=fps, dpi=dpi)
                    elif writer_name == 'imagemagick':
                        anim.save(gif_path, writer='imagemagick', fps=fps, dpi=dpi)
                    
                    logger.info(f"Animation saved with {writer_name}: {gif_path}")
                    return gif_path
                except Exception as e:
                    logger.warning(f"Failed to save with {writer_name}: {e}")
                    continue
            
            # If all writers fail, try saving as MP4 with ffmpeg
            try:
                mp4_path = gif_path.replace('.gif', '.mp4')
                anim.save(mp4_path, writer='ffmpeg', fps=fps, dpi=dpi)
                logger.info(f"Saved as MP4 instead: {mp4_path}")
                return mp4_path
            except Exception as e:
                logger.warning(f"Failed to save as MP4: {e}")
            
            # Final fallback: save as individual PNG frames
            logger.warning("All video writers failed, saving as PNG frames")
            return self.save_as_png_frames(anim, fps, dpi)
            
        except Exception as e:
            logger.error(f"Failed to save animation GIF: {e}")
            return None
    
    def save_as_png_frames(self, anim: animation.FuncAnimation, 
                          fps: int = 10, dpi: int = 100) -> Optional[str]:
        """
        Save animation as individual PNG frames as fallback
        
        Args:
            anim: Matplotlib animation object
            fps: Frames per second for the GIF
            dpi: DPI for the output GIF
            
        Returns:
            Path to saved frames directory, or None if failed
        """
        try:
            frames_dir = self.get_gif_path().replace('.gif', '_frames')
            os.makedirs(frames_dir, exist_ok=True)
            
            # Save a few key frames
            frame_count = 0
            for i in range(0, 100, 5):  # Save every 5th frame up to 100
                try:
                    # Update animation to frame i
                    anim._func(i)
                    
                    # Save frame
                    frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
                    anim._fig.savefig(frame_path, dpi=dpi, bbox_inches='tight')
                    frame_count += 1
                    
                    if frame_count >= 20:  # Limit to 20 frames
                        break
                        
                except Exception as e:
                    logger.warning(f"Failed to save frame {i}: {e}")
                    continue
            
            logger.info(f"Saved {frame_count} PNG frames to: {frames_dir}")
            return frames_dir
            
        except Exception as e:
            logger.error(f"Failed to save PNG frames: {e}")
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