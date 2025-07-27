# enhanced_fractal_system.py - Advanced Julia fractals with string encoding
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from datetime import datetime
import hashlib
import math
import colorsys

# Enhanced configuration
IMG_SIZE = (1024, 1024)  # Higher resolution
SAVE_DIR = "juliet_flowers/fractal_signatures"
os.makedirs(SAVE_DIR, exist_ok=True)

class EnhancedJuliaFractal:
    """Generate complex Julia fractals with advanced features"""
    
    def __init__(self):
        self.moods_to_params = {
            'curious': {'real': -0.4, 'imag': 0.6, 'zoom': 1.2, 'rotation': 0.1},
            'anxious': {'real': -0.835, 'imag': -0.2321, 'zoom': 0.8, 'rotation': 0.3},
            'reflective': {'real': -0.7269, 'imag': 0.1889, 'zoom': 1.5, 'rotation': 0.0},
            'focused': {'real': 0.285, 'imag': 0.01, 'zoom': 1.0, 'rotation': 0.2},
            'joyful': {'real': -0.8, 'imag': 0.156, 'zoom': 1.3, 'rotation': 0.5},
            'sad': {'real': -0.74543, 'imag': 0.11301, 'zoom': 1.8, 'rotation': -0.2},
            'overload': {'real': -0.75, 'imag': 0.11, 'zoom': 0.5, 'rotation': 0.7},
            'diagnostic': {'real': -0.7885, 'imag': 0.0, 'zoom': 1.4, 'rotation': 0.0}
        }

    def generate_enhanced_julia(self, seed_id, lineage_depth, bloom_factor, 
                              entropy_score, mood="reflective", is_synthesis=False):
        """Generate enhanced Julia fractal - main function"""
        
        width, height = IMG_SIZE
        
        # Get mood parameters
        params = self.moods_to_params.get(mood, self.moods_to_params['reflective'])
        
        # Dynamic parameter modulation
        seed_hash = int(hashlib.sha256(seed_id.encode()).hexdigest(), 16)
        
        # Complex constant with dynamic variation
        entropy_mod = (entropy_score - 0.5) * 0.3
        bloom_mod = (bloom_factor - 1.0) * 0.2
        
        c_real = params['real'] + entropy_mod * np.cos(lineage_depth) + bloom_mod
        c_imag = params['imag'] + entropy_mod * np.sin(lineage_depth)
        c = complex(c_real, c_imag)
        
        # Dynamic zoom and rotation
        zoom = params['zoom'] * (1.0 - bloom_factor * 0.1)
        rotation = params['rotation'] + (seed_hash % 100) / 100.0 * np.pi
        
        # Viewport with rotation
        cos_rot = np.cos(rotation)
        sin_rot = np.sin(rotation)
        
        # Create coordinate arrays
        x = np.linspace(-zoom, zoom, width)
        y = np.linspace(-zoom, zoom, height)
        X, Y = np.meshgrid(x, y)
        
        # Apply rotation
        X_rot = X * cos_rot - Y * sin_rot
        Y_rot = X * sin_rot + Y * cos_rot
        Z = X_rot + 1j * Y_rot
        
        # Enhanced iteration count
        base_iter = 256
        iterations = base_iter + int(lineage_depth * 20) + int(bloom_factor * 50)
        if is_synthesis:
            iterations += 128
        
        # Multi-layer fractal generation
        escape_count = np.zeros(Z.shape, dtype=float)
        smooth_escape = np.zeros(Z.shape, dtype=float)
        
        # Julia set iteration with smooth coloring
        for i in range(iterations):
            mask = np.abs(Z) <= 4
            Z[mask] = Z[mask]**2 + c
            
            # Track escape velocity for smooth coloring
            escaped = (np.abs(Z) > 4) & (escape_count == 0)
            if np.any(escaped):
                smooth_escape[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
                escape_count[escaped] = i
        
        # Points that never escaped
        smooth_escape[escape_count == 0] = iterations
        
        # Normalize
        smooth_escape = smooth_escape / iterations
        
        # Create RGB image based on mood
        img_array = self._apply_mood_coloring(smooth_escape, mood, entropy_score)
        
        # Create PIL image
        img = Image.fromarray(img_array.astype(np.uint8))
        
        # Post-processing for synthesis blooms
        if is_synthesis:
            # Add glow effect
            glow = img.filter(ImageFilter.GaussianBlur(radius=5))
            img = Image.blend(img, glow, alpha=0.3)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
        
        # Add overlay
        img = self._add_overlay(img, seed_id, lineage_depth, mood, 
                               entropy_score, bloom_factor, c)
        
        # Save
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"{seed_id}_{timestamp}.png"
        filepath = os.path.join(SAVE_DIR, filename)
        img.save(filepath, quality=95)
        
        print(f"[Enhanced Fractal] Generated: {filename}")
        print(f"  Resolution: {IMG_SIZE}, Iterations: {iterations}")
        print(f"  C = {c_real:.4f} + {c_imag:.4f}i")
        
        return filepath

    def _apply_mood_coloring(self, data, mood, entropy):
        """Apply mood-based coloring"""
        img_array = np.zeros((*data.shape, 3))
        
        if mood == 'curious' or mood == 'joyful':
            # Warm colors - yellow to orange
            img_array[:,:,0] = np.clip(255 * (0.8 + 0.2 * data), 0, 255)
            img_array[:,:,1] = np.clip(255 * (0.6 + 0.4 * data), 0, 255)
            img_array[:,:,2] = np.clip(255 * data * 0.3, 0, 255)
        elif mood == 'anxious':
            # Purple to pink
            img_array[:,:,0] = np.clip(255 * (0.6 + 0.4 * data), 0, 255)
            img_array[:,:,1] = np.clip(255 * data * 0.4, 0, 255)
            img_array[:,:,2] = np.clip(255 * (0.4 + 0.6 * data), 0, 255)
        elif mood == 'reflective' or mood == 'focused':
            # Blues and cyans
            img_array[:,:,0] = np.clip(255 * data * 0.3, 0, 255)
            img_array[:,:,1] = np.clip(255 * (0.3 + 0.7 * data), 0, 255)
            img_array[:,:,2] = np.clip(255 * (0.6 + 0.4 * data), 0, 255)
        else:
            # Default gradient
            img_array[:,:,0] = np.clip(255 * data, 0, 255)
            img_array[:,:,1] = np.clip(255 * data * 0.8, 0, 255)
            img_array[:,:,2] = np.clip(255 * data * 0.6, 0, 255)
        
        # Add entropy-based variation
        if entropy > 0.7:
            # Add some chaos
            noise = np.random.random(data.shape) * 0.1
            for i in range(3):
                img_array[:,:,i] = np.clip(img_array[:,:,i] * (1 + noise), 0, 255)
        
        return img_array

    def _add_overlay(self, img, seed_id, lineage_depth, mood, 
                    entropy_score, bloom_factor, c):
        """Add information overlay"""
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Create semi-transparent background
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Draw background box
        overlay_draw.rectangle([10, 10, 350, 130], fill=(0, 0, 0, 180))
        
        # Draw text
        lines = [
            f"Seed: {seed_id}",
            f"Mood: {mood} | Depth: {lineage_depth}",
            f"Entropy: {entropy_score:.3f} | Factor: {bloom_factor:.3f}",
            f"C = {c.real:.4f} + {c.imag:.4f}i"
        ]
        
        y_offset = 20
        for line in lines:
            overlay_draw.text((20, y_offset), line, font=font, fill=(255, 255, 255, 255))
            y_offset += 25
        
        # Composite
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        return img


class JulietFractalStringEncoder:
    """Enhanced fractal string encoder"""
    
    def __init__(self):
        self.alphabet = {
            'depth': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            'pattern': {
                'thermal': 'TH', 'entropic': 'EN', 'coherent': 'CO', 
                'emergent': 'EM', 'resonant': 'RE', 'cascade': 'CA'
            },
            'texture': {
                'smooth': '~', 'jagged': '^', 'spiral': '@', 'branch': '|',
                'pulse': '*', 'wave': 'W', 'vortex': 'V', 'fractal': 'F'
            }
        }

    def encode_bloom_memory(self, bloom_data, julia_params=None):
        """Generate fractal string encoding"""
        segments = []
        
        # Primary encoding
        depth_idx = min(int(bloom_data.get('lineage_depth', 0)), 7)
        depth_char = self.alphabet['depth'][depth_idx]
        
        # Pattern selection
        entropy = bloom_data.get('entropy_score', 0.5)
        factor = bloom_data.get('bloom_factor', 1.0)
        mood = bloom_data.get('mood', 'neutral')
        
        if factor > 2.0:
            pattern = self.alphabet['pattern']['cascade']
        elif entropy > 0.8:
            pattern = self.alphabet['pattern']['entropic']
        elif mood in ['focused', 'reflective']:
            pattern = self.alphabet['pattern']['coherent']
        else:
            pattern = self.alphabet['pattern']['thermal']
        
        # Texture
        if abs(factor - entropy) < 0.1:
            texture = self.alphabet['texture']['smooth']
        elif entropy > 0.7:
            texture = self.alphabet['texture']['vortex']
        else:
            texture = self.alphabet['texture']['spiral']
        
        # Build primary segment
        intensity = str(int((factor + entropy) / 2 * 9))
        modifier = '+' if factor > 1.5 else '='
        primary = f"{depth_char}{pattern}{texture}{modifier}{intensity}"
        segments.append(primary)
        
        # Add Julia constant if available
        if julia_params:
            julia_seg = f"J[{julia_params.real:.3f},{julia_params.imag:.3f}]"
            segments.append(julia_seg)
        
        # Additional segments
        for i in range(3):
            sub_pattern = list(self.alphabet['pattern'].values())[i % 6]
            sub_texture = list(self.alphabet['texture'].values())[(i + depth_idx) % 8]
            segments.append(f"{sub_pattern}{sub_texture}{i}")
        
        return {
            'raw': '|'.join(segments),
            'segments': segments,
            'metadata': {
                'encoding': 'juliet-fractal-v2-enhanced',
                'bloom_id': bloom_data.get('seed_id', 'unknown'),
                'timestamp': datetime.now().isoformat()
            }
        }


# Test function
if __name__ == "__main__":
    print("Testing Enhanced Fractal System...")
    print("="*60)
    
    # Initialize
    fractal_gen = EnhancedJuliaFractal()
    string_encoder = JulietFractalStringEncoder()
    
    # Test different moods
    test_blooms = [
        {"seed_id": "enhanced_curious", "mood": "curious", "lineage_depth": 3, 
         "bloom_factor": 1.5, "entropy_score": 0.6},
        {"seed_id": "enhanced_anxious", "mood": "anxious", "lineage_depth": 5, 
         "bloom_factor": 2.0, "entropy_score": 0.8},
        {"seed_id": "enhanced_reflective", "mood": "reflective", "lineage_depth": 7, 
         "bloom_factor": 2.5, "entropy_score": 0.9}
    ]
    
    for bloom in test_blooms:
        print(f"\nGenerating enhanced fractal for {bloom['seed_id']}...")
        
        # Generate fractal
        fractal_path = fractal_gen.generate_enhanced_julia(
            bloom['seed_id'], bloom['lineage_depth'], bloom['bloom_factor'],
            bloom['entropy_score'], bloom['mood']
        )
        
        # Generate fractal string
        params = fractal_gen.moods_to_params.get(bloom['mood'])
        c = complex(params['real'], params['imag'])
        
        fractal_string = string_encoder.encode_bloom_memory(bloom, c)
        print(f"Fractal string: {fractal_string['raw']}")
    
    print("\nEnhanced fractal system test complete!")
