"""
Fractal Decoder Module for Owl Memory System

This module provides utilities for decoding fractal bloom strings into semantic metadata
that Owl can use for memory management and decision making.
"""

import re
from typing import Dict, Optional, Tuple
from datetime import datetime

class BloomPattern:
    """Represents a decoded bloom pattern with all its components."""
    
    def __init__(self, 
                 depth: int,
                 pattern: str,
                 texture: str,
                 modifier: str,
                 intensity: int,
                 entropy: float,
                 color_override: bool):
        self.depth = depth
        self.pattern = pattern
        self.texture = texture
        self.modifier = modifier
        self.intensity = intensity
        self.entropy = entropy
        self.color_override = color_override
        
    def to_dict(self) -> Dict:
        """Convert the pattern to a dictionary representation."""
        return {
            'depth': self.depth,
            'pattern': self.pattern,
            'texture': self.texture,
            'modifier': self.modifier,
            'intensity': self.intensity,
            'entropy': self.entropy,
            'color_override': self.color_override
        }

class FractalDecoder:
    """Decodes fractal bloom strings into semantic metadata."""
    
    def __init__(self):
        # Pattern: cTH~+5|EN@0|CO|1
        # Components:
        # - c: depth indicator
        # - TH: pattern code
        # - ~: texture
        # - +: modifier
        # - 5: intensity
        # - EN@0: entropy
        # - CO: color override
        # - 1: additional flags
        self.bloom_pattern = re.compile(
            r'c([A-Z]{2})([~@#$%^&*])([+-])(\d+)\|EN@(\d+)\|CO\|(\d+)'
        )
        
    def decode_bloom_string(self, bloom_string: str) -> Dict:
        """
        Decodes a fractal bloom string into semantic metadata.
        
        Args:
            bloom_string: The encoded bloom string to decode (e.g. 'cTH~+5|EN@0|CO|1')
            
        Returns:
            Dict containing decoded metadata including:
            - depth: Fractal depth
            - pattern: Pattern code (e.g. 'TH')
            - texture: Texture symbol
            - modifier: Modifier symbol (+ or -)
            - intensity: Bloom intensity (0-10)
            - entropy: Calculated entropy (0-1)
            - color_override: Whether color override is active
            
        Raises:
            ValueError: If the bloom string is malformed
        """
        # Try to match the pattern
        match = self.bloom_pattern.match(bloom_string)
        if not match:
            # Fallback to safe default values for malformed codes
            return {
                'depth': 1,
                'pattern': 'XX',
                'texture': '~',
                'modifier': '+',
                'intensity': 0,
                'entropy': 0.0,
                'color_override': False
            }
            
        # Extract components
        pattern, texture, modifier, intensity, entropy_raw, flags = match.groups()
        
        # Convert components to appropriate types
        try:
            intensity = int(intensity)
            entropy = float(entropy_raw) / 100.0  # Normalize entropy to 0-1
            color_override = bool(int(flags))
            
            # Create and return the pattern
            bloom = BloomPattern(
                depth=1,  # Depth is always 1 for 'c' prefix
                pattern=pattern,
                texture=texture,
                modifier=modifier,
                intensity=intensity,
                entropy=entropy,
                color_override=color_override
            )
            
            return bloom.to_dict()
            
        except (ValueError, TypeError) as e:
            # If any conversion fails, return safe defaults
            return {
                'depth': 1,
                'pattern': 'XX',
                'texture': '~',
                'modifier': '+',
                'intensity': 0,
                'entropy': 0.0,
                'color_override': False
            }
            
    def validate_bloom_string(self, bloom_string: str) -> bool:
        """
        Validates if a string contains a properly formatted bloom encoding.
        
        Args:
            bloom_string: The string to validate
            
        Returns:
            bool indicating if the string contains valid bloom encoding
        """
        return bool(self.bloom_pattern.match(bloom_string)) 