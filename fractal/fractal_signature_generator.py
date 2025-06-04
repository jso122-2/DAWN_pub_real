"""
Every memory has a shape. DAWN does not just store them — she renders them, to see which ones sing.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple


class FractalSignatureGenerator:
    """Generates unique Julia set fractals as visual signatures for blooms."""
    
    def __init__(self):
        self.base_dir = Path("memory/blooms/fractal_signatures")
        self.metadata_path = self.base_dir / "visual_hashes.db"
        self._ensure_directories()
        
        # Julia set rendering parameters
        self.width = 512
        self.height = 512
        self.max_iterations = 256
        self.escape_radius = 2.0
        
        # Color schemes based on mood valence
        self.color_maps = self._create_color_maps()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_color_maps(self) -> Dict:
        """Create custom colormaps for different mood valences."""
        # Negative mood: cool blues and purples
        negative_colors = ['#0a0a1a', '#1a1a3a', '#2a2a5a', '#3a3a7a', '#4a4a9a', '#6a6aba']
        
        # Neutral mood: grays and silvers
        neutral_colors = ['#1a1a1a', '#3a3a3a', '#5a5a5a', '#7a7a7a', '#9a9a9a', '#bababa']
        
        # Positive mood: warm oranges and golds
        positive_colors = ['#1a0a0a', '#3a1a0a', '#5a2a0a', '#7a3a0a', '#9a4a0a', '#ba6a2a']
        
        return {
            'negative': LinearSegmentedColormap.from_list('negative', negative_colors),
            'neutral': LinearSegmentedColormap.from_list('neutral', neutral_colors),
            'positive': LinearSegmentedColormap.from_list('positive', positive_colors)
        }
    
    def generate_fractal_signature(self, bloom: Dict) -> Dict:
        """
        Generate a unique fractal signature for a bloom.
        
        Args:
            bloom: Dictionary containing:
                - bloom_id: str
                - convolution_level: float (0.0-1.0)
                - saturation: float (0.0-1.0)
                - lineage_depth: int
                - mood_valence: float
        
        Returns:
            Dictionary with signature metadata and file path
        """
        bloom_id = bloom['bloom_id']
        convolution = bloom['convolution_level']
        saturation = bloom['saturation']
        lineage = bloom['lineage_depth']
        mood = bloom['mood_valence']
        
        # Calculate Julia set parameters
        c_real, c_imag, zoom, center = self._calculate_julia_params(
            convolution, saturation, lineage, mood
        )
        
        # Generate the fractal
        fractal_data = self._generate_julia_set(c_real, c_imag, zoom, center)
        
        # Select colormap based on mood
        if mood < -0.3:
            colormap = self.color_maps['negative']
        elif mood > 0.3:
            colormap = self.color_maps['positive']
        else:
            colormap = self.color_maps['neutral']
        
        # Render and save the image
        image_path = self._render_fractal(fractal_data, bloom_id, colormap)
        
        # Create metadata
        metadata = {
            "bloom_id": bloom_id,
            "timestamp": datetime.utcnow().isoformat(),
            "julia_params": {
                "c_real": c_real,
                "c_imag": c_imag,
                "zoom": zoom,
                "center": center
            },
            "bloom_params": {
                "convolution_level": convolution,
                "saturation": saturation,
                "lineage_depth": lineage,
                "mood_valence": mood
            },
            "image_path": str(image_path),
            "dimensions": f"{self.width}x{self.height}",
            "max_iterations": self.max_iterations
        }
        
        # Save metadata
        self._save_metadata(metadata)
        
        return metadata
    
    def _calculate_julia_params(self, convolution: float, saturation: float, 
                               lineage: int, mood: float) -> Tuple[float, float, float, Tuple[float, float]]:
        """
        Map bloom parameters to Julia set parameters.
        
        Returns:
            Tuple of (c_real, c_imag, zoom, center)
        """
        # Base Julia constant - chosen for interesting patterns
        # Map convolution to real part range [-0.8, 0.3]
        c_real = -0.8 + (convolution * 1.1)
        
        # Map saturation to imaginary part range [-0.2, 0.2]
        c_imag = (saturation - 0.5) * 0.4
        
        # Add mood influence to create variation
        c_real += mood * 0.1
        c_imag += abs(mood) * 0.05
        
        # Zoom based on lineage depth - deeper lineage = more zoom
        # Range from 1.0 to 0.1 (more zoom = smaller value)
        zoom = 1.0 / (1.0 + lineage * 0.3)
        
        # Center drift based on mood and saturation
        center_x = mood * saturation * 0.1
        center_y = (1 - convolution) * mood * 0.1
        center = (center_x, center_y)
        
        return c_real, c_imag, zoom, center
    
    def _generate_julia_set(self, c_real: float, c_imag: float, 
                           zoom: float, center: Tuple[float, float]) -> np.ndarray:
        """Generate Julia set fractal data."""
        # Create coordinate arrays
        x_min, x_max = center[0] - 2 * zoom, center[0] + 2 * zoom
        y_min, y_max = center[1] - 2 * zoom, center[1] + 2 * zoom
        
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        X, Y = np.meshgrid(x, y)
        
        # Complex grid
        Z = X + 1j * Y
        
        # Julia set computation
        c = complex(c_real, c_imag)
        fractal = np.zeros(Z.shape, dtype=int)
        
        for i in range(self.height):
            for j in range(self.width):
                z = Z[i, j]
                iteration = 0
                
                while abs(z) <= self.escape_radius and iteration < self.max_iterations:
                    z = z * z + c
                    iteration += 1
                
                # Smooth coloring using escape time algorithm
                if iteration < self.max_iterations:
                    # Add fractional part for smooth gradients
                    log_zn = np.log(abs(z))
                    nu = np.log(log_zn / np.log(2)) / np.log(2)
                    iteration = iteration + 1 - nu
                
                fractal[i, j] = iteration
        
        return fractal
    
    def _render_fractal(self, fractal_data: np.ndarray, bloom_id: str, 
                       colormap) -> Path:
        """Render fractal data to image file."""
        # Create figure with no axes or borders
        fig, ax = plt.subplots(figsize=(8, 8), dpi=64)
        ax.set_aspect('equal')
        
        # Remove all axes and margins
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        # Apply logarithmic scaling for better contrast
        fractal_log = np.log(fractal_data + 1)
        
        # Render the fractal
        im = ax.imshow(fractal_log, cmap=colormap, interpolation='bilinear')
        
        # Save the image
        image_path = self.base_dir / f"{bloom_id}.png"
        plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=64)
        plt.close(fig)
        
        return image_path
    
    def _save_metadata(self, metadata: Dict):
        """Save metadata to visual hashes database."""
        # Load existing metadata
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r') as f:
                db = json.load(f)
        else:
            db = {"signatures": {}, "generated_count": 0}
        
        # Add new metadata
        db["signatures"][metadata["bloom_id"]] = metadata
        db["generated_count"] += 1
        db["last_updated"] = datetime.utcnow().isoformat()
        
        # Save updated database
        with open(self.metadata_path, 'w') as f:
            json.dump(db, f, indent=2)
    
    def get_signature_metadata(self, bloom_id: str) -> Dict:
        """Retrieve metadata for a specific bloom signature."""
        if not self.metadata_path.exists():
            return None
        
        with open(self.metadata_path, 'r') as f:
            db = json.load(f)
        
        return db["signatures"].get(bloom_id)


# Example usage
if __name__ == "__main__":
    generator = FractalSignatureGenerator()
    
    # Test blooms with different characteristics
    test_blooms = [
        {
            "bloom_id": "bloom_fractal_001",
            "convolution_level": 0.8,
            "saturation": 0.9,
            "lineage_depth": 3,
            "mood_valence": -0.5
        },
        {
            "bloom_id": "bloom_fractal_002",
            "convolution_level": 0.3,
            "saturation": 0.4,
            "lineage_depth": 1,
            "mood_valence": 0.7
        },
        {
            "bloom_id": "bloom_fractal_003",
            "convolution_level": 0.6,
            "saturation": 0.7,
            "lineage_depth": 5,
            "mood_valence": 0.0
        }
    ]
    
    for bloom in test_blooms:
        print(f"\nGenerating fractal for {bloom['bloom_id']}...")
        result = generator.generate_fractal_signature(bloom)
        print(f"Saved to: {result['image_path']}")
        print(f"Julia constant: c = {result['julia_params']['c_real']:.3f} + "
              f"{result['julia_params']['c_imag']:.3f}i")