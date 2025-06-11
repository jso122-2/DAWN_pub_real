# encode_script_as_fractal.py
# Encodes a text/script into a Julia set fractal key.

from fractal.fractal_key_generator import generate_complex_seed
from fractal.fractal_token_mapper import map_tokens_to_depths
from fractal.fractal_key_visualizer import render_julia

def encode_script_as_fractal(text: str, save_path: str = None, resolution: int = 512):
    """
    Encode the given text into a Julia fractal and optionally save the image.
    Returns the complex seed and matplotlib Figure.
    """
    # Split text into tokens
    words = text.split()
    # Map tokens to recursion depths
    depths = map_tokens_to_depths(words)
    # Generate complex seed based on words and depths
    c = generate_complex_seed(words, depths)
    # Render the Julia set
    fig = render_julia(c, resolution=resolution)
    # Save if requested
    if save_path:
        fig.savefig(save_path)
    return c, fig
