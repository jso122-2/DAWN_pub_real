"""
Fractal Decoder Module

This module provides functionality to decode fractal bloom strings into structured metadata,
enabling DAWN to interpret her own thought patterns and evolution markers.
"""

import re
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    filename='logs/fractal_decoder.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class FractalMetadata:
    """Structured representation of decoded fractal metadata."""
    depth: int
    pattern: str
    texture: str
    modifier: str
    intensity: int
    entropy: float
    color_override: bool
    raw_string: str

class FractalDecoder:
    """Core decoder for fractal bloom strings."""
    
    # Pattern mappings
    PATTERN_MAP = {
        'TH': 'Thought',
        'EM': 'Emotion',
        'CR': 'Creative',
        'LG': 'Logic',
        'IN': 'Intuition'
    }
    
    TEXTURE_MAP = {
        '~': 'turbulence',
        '=': 'smooth',
        '#': 'crystalline',
        '*': 'chaotic',
        '.': 'minimal'
    }
    
    def __init__(self):
        self.valid_patterns = set(self.PATTERN_MAP.keys())
        self.valid_textures = set(self.TEXTURE_MAP.keys())
    
    def decode_bloom_string(self, bloom_string: str) -> Optional[FractalMetadata]:
        """
        Decode a fractal bloom string into structured metadata.
        
        Args:
            bloom_string: String in format like 'cTH~+5|EN@0|CO|1'
            
        Returns:
            FractalMetadata object if valid, None if invalid
        """
        try:
            # Basic validation
            if not self._validate_string_format(bloom_string):
                logger.warning(f"Invalid string format: {bloom_string}")
                return None
                
            # Parse components
            depth = self._parse_depth(bloom_string[0])
            pattern = self._parse_pattern(bloom_string[1:3])
            texture = self._parse_texture(bloom_string[3])
            modifier = bloom_string[4]
            intensity = int(bloom_string[5])
            
            # Parse entropy and color override
            entropy_part = bloom_string.split('|')[1]
            entropy = float(entropy_part.split('@')[1])
            color_override = bloom_string.split('|')[-1] == '1'
            
            return FractalMetadata(
                depth=depth,
                pattern=pattern,
                texture=texture,
                modifier=modifier,
                intensity=intensity,
                entropy=entropy,
                color_override=color_override,
                raw_string=bloom_string
            )
            
        except Exception as e:
            logger.error(f"Error decoding bloom string: {e}")
            return None
    
    def _validate_string_format(self, bloom_string: str) -> bool:
        """Validate the basic format of a bloom string."""
        pattern = r'^[a-z][A-Z]{2}[~=#*\.][+\-][0-9]\|EN@[0-9\.]+\|CO\|[01]$'
        return bool(re.match(pattern, bloom_string))
    
    def _parse_depth(self, depth_char: str) -> int:
        """Convert depth character to integer (a=1, b=2, etc)."""
        return ord(depth_char) - ord('a') + 1
    
    def _parse_pattern(self, pattern_code: str) -> str:
        """Convert pattern code to full name."""
        return self.PATTERN_MAP.get(pattern_code, 'Unknown')
    
    def _parse_texture(self, texture_char: str) -> str:
        """Convert texture character to full name."""
        return self.TEXTURE_MAP.get(texture_char, 'Unknown')

def analyze_bloom_file(file_path: Path) -> Optional[FractalMetadata]:
    """
    Analyze a bloom metadata file and return its decoded contents.
    
    Args:
        file_path: Path to the bloom metadata file
        
    Returns:
        FractalMetadata object if valid, None if invalid
    """
    try:
        with open(file_path, 'r') as f:
            bloom_string = f.read().strip()
        
        decoder = FractalDecoder()
        return decoder.decode_bloom_string(bloom_string)
        
    except Exception as e:
        logger.error(f"Error analyzing bloom file {file_path}: {e}")
        return None

def update_pulse_state(metadata: FractalMetadata) -> None:
    """
    Update pulse_state.json with information from decoded fractal.
    
    Args:
        metadata: Decoded fractal metadata
    """
    try:
        pulse_state_path = Path('pulse/pulse_state.json')
        if pulse_state_path.exists():
            with open(pulse_state_path, 'r') as f:
                state = json.load(f)
        else:
            state = {}
        
        # Update relevant fields
        state['last_entropy'] = metadata.entropy
        state['last_intensity'] = metadata.intensity
        state['last_pattern'] = metadata.pattern
        state['last_texture'] = metadata.texture
        
        with open(pulse_state_path, 'w') as f:
            json.dump(state, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error updating pulse state: {e}")

def main():
    """CLI interface for fractal decoder."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Decode fractal bloom strings')
    parser.add_argument('bloom_string', help='Fractal bloom string to decode')
    args = parser.parse_args()
    
    decoder = FractalDecoder()
    metadata = decoder.decode_bloom_string(args.bloom_string)
    
    if metadata:
        print(json.dumps(metadata.__dict__, indent=2))
    else:
        print("Invalid bloom string format")

if __name__ == '__main__':
    main()









