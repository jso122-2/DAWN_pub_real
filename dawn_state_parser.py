#!/usr/bin/env python3
"""
DAWN State Parser - Consciousness Metadata Processing
=====================================================

Reads JSON metadata from DAWN memory files and extracts validated
consciousness parameters for fractal generation and analysis.

Handles:
- Memory metadata parsing
- Parameter validation and range checking
- Error handling for malformed inputs
- Structured config object generation
- Consciousness state validation
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("dawn_state_parser")

@dataclass
class DAWNConsciousnessConfig:
    """Validated consciousness configuration for fractal generation"""
    
    # Primary consciousness parameters
    bloom_entropy: float
    mood_valence: float
    drift_vector: float
    rebloom_depth: int
    sigil_saturation: float
    pulse_zone: str
    
    # Optional metadata
    timestamp: Optional[str] = None
    memory_id: Optional[str] = None
    archetype: Optional[str] = None
    fractal_string: Optional[str] = None
    
    # Validation metadata
    validation_passed: bool = True
    validation_warnings: List[str] = field(default_factory=list)
    source_file: Optional[str] = None
    
    def to_fractal_params(self) -> Dict[str, Any]:
        """Convert to fractal generation parameters"""
        return {
            'bloom_entropy': self.bloom_entropy,
            'mood_valence': self.mood_valence,
            'drift_vector': self.drift_vector,
            'rebloom_depth': self.rebloom_depth,
            'sigil_saturation': self.sigil_saturation,
            'pulse_zone': self.pulse_zone
        }
    
    def to_voice_params(self) -> Dict[str, Any]:
        """Convert to voice generation parameters"""
        # Create mood pigment from consciousness state
        mood_pigment = self._derive_mood_pigment()
        sigil_heat = self._derive_sigil_heat()
        
        return {
            'pigment_dict': mood_pigment,
            'sigil_state': sigil_heat,
            'entropy': self.bloom_entropy,
            'drift': self.drift_vector
        }
    
    def _derive_mood_pigment(self) -> Dict[str, float]:
        """Derive mood pigment from consciousness parameters"""
        # Map consciousness parameters to pigment channels
        pigment = {
            'red': max(0.0, self.bloom_entropy * 0.7),  # Entropy → red (chaos/energy)
            'blue': max(0.0, -self.mood_valence * 0.8) if self.mood_valence < 0 else 0.0,  # Negative valence → blue
            'yellow': max(0.0, self.mood_valence * 0.6) if self.mood_valence > 0 else 0.0,  # Positive valence → yellow
            'green': max(0.0, (1.0 - abs(self.mood_valence)) * 0.5),  # Neutral valence → green
            'violet': max(0.0, (1.0 - self.bloom_entropy) * 0.4),  # Low entropy → violet (structure)
            'orange': max(0.0, abs(self.drift_vector) * 0.5)  # Drift → orange (movement)
        }
        
        # Normalize to sum to 1.0
        total = sum(pigment.values())
        if total > 0:
            pigment = {color: value / total for color, value in pigment.items()}
        else:
            # Fallback neutral state
            pigment = {'blue': 0.4, 'green': 0.3, 'violet': 0.3}
        
        return pigment
    
    def _derive_sigil_heat(self) -> Dict[str, float]:
        """Derive sigil heat from consciousness parameters"""
        return {
            'heat': self.sigil_saturation * 0.8,  # Saturation → heat
            'friction': abs(self.drift_vector) * 0.6,  # Drift → friction
            'recasion': (self.rebloom_depth / 10.0) * 0.7  # Depth → recasion (memory cycling)
        }

class DAWNStateParser:
    """
    Parses and validates DAWN consciousness states from JSON metadata
    
    Handles memory files, consciousness logs, and state snapshots.
    Validates parameter ranges and ensures data integrity.
    """
    
    def __init__(self, strict_validation: bool = True):
        """
        Initialize parser
        
        Args:
            strict_validation: If True, invalid parameters cause errors.
                              If False, invalid parameters are clamped and warnings issued.
        """
        self.strict_validation = strict_validation
        
        # Parameter validation ranges
        self.parameter_ranges = {
            'bloom_entropy': (0.0, 1.0),
            'mood_valence': (-1.0, 1.0),
            'drift_vector': (-1.0, 1.0),
            'rebloom_depth': (1, 20),
            'sigil_saturation': (0.0, 1.0)
        }
        
        # Valid pulse zones
        self.valid_pulse_zones = {
            'calm', 'fragile', 'stable', 'surge', 'volatile', 
            'crystalline', 'flowing', 'transcendent'
        }
        
        # Parameter aliases (for different naming conventions)
        self.parameter_aliases = {
            'entropy': 'bloom_entropy',
            'valence': 'mood_valence',
            'drift': 'drift_vector',
            'depth': 'rebloom_depth',
            'saturation': 'sigil_saturation',
            'zone': 'pulse_zone',
            'pulse': 'pulse_zone'
        }
    
    def parse_file(self, file_path: Union[str, Path]) -> DAWNConsciousnessConfig:
        """
        Parse consciousness state from JSON file
        
        Args:
            file_path: Path to JSON metadata file
            
        Returns:
            Validated consciousness configuration
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains invalid data (in strict mode)
            json.JSONDecodeError: If file contains invalid JSON
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Consciousness metadata file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {e}", e.doc, e.pos)
        
        # Parse with source file information
        config = self.parse_data(data)
        config.source_file = str(file_path)
        
        return config
    
    def parse_data(self, data: Dict[str, Any]) -> DAWNConsciousnessConfig:
        """
        Parse consciousness state from dictionary data
        
        Args:
            data: Dictionary containing consciousness parameters
            
        Returns:
            Validated consciousness configuration
            
        Raises:
            ValueError: If required parameters missing or invalid (in strict mode)
        """
        warnings = []
        
        # Extract parameters with fallbacks
        extracted = self._extract_parameters(data, warnings)
        
        # Validate parameters
        validated = self._validate_parameters(extracted, warnings)
        
        # Extract metadata
        metadata = self._extract_metadata(data)
        
        # Create configuration object
        config = DAWNConsciousnessConfig(
            bloom_entropy=validated['bloom_entropy'],
            mood_valence=validated['mood_valence'],
            drift_vector=validated['drift_vector'],
            rebloom_depth=validated['rebloom_depth'],
            sigil_saturation=validated['sigil_saturation'],
            pulse_zone=validated['pulse_zone'],
            **metadata,
            validation_warnings=warnings,
            validation_passed=len(warnings) == 0
        )
        
        if self.strict_validation and warnings:
            error_msg = f"Validation failed with {len(warnings)} issues: {'; '.join(warnings)}"
            raise ValueError(error_msg)
        
        return config
    
    def parse_multiple_files(self, directory: Union[str, Path], 
                           pattern: str = "*.json") -> List[DAWNConsciousnessConfig]:
        """
        Parse multiple consciousness state files from directory
        
        Args:
            directory: Directory containing metadata files
            pattern: File pattern to match (default: "*.json")
            
        Returns:
            List of validated consciousness configurations
        """
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        configs = []
        errors = []
        
        for file_path in directory.glob(pattern):
            try:
                config = self.parse_file(file_path)
                configs.append(config)
            except Exception as e:
                errors.append(f"Error parsing {file_path}: {e}")
                logger.warning(f"Failed to parse {file_path}: {e}")
        
        if errors:
            logger.warning(f"Encountered {len(errors)} errors while parsing directory")
            for error in errors[:5]:  # Log first 5 errors
                logger.warning(f"  {error}")
        
        logger.info(f"Successfully parsed {len(configs)} consciousness states from {directory}")
        
        return configs
    
    def _extract_parameters(self, data: Dict[str, Any], warnings: List[str]) -> Dict[str, Any]:
        """Extract consciousness parameters from data with alias handling"""
        
        extracted = {}
        required_params = [
            'bloom_entropy', 'mood_valence', 'drift_vector', 
            'rebloom_depth', 'sigil_saturation', 'pulse_zone'
        ]
        
        # Look for parameters in various locations
        search_locations = [
            data,  # Root level
            data.get('parameters', {}),  # Parameters section
            data.get('consciousness_state', {}),  # Consciousness state section
            data.get('fractal_params', {}),  # Fractal parameters section
            data.get('voice_params', {})  # Voice parameters section
        ]
        
        for param in required_params:
            value = None
            
            # Search all locations for parameter
            for location in search_locations:
                if not isinstance(location, dict):
                    continue
                
                # Try direct parameter name
                if param in location:
                    value = location[param]
                    break
                
                # Try aliases
                for alias, canonical in self.parameter_aliases.items():
                    if canonical == param and alias in location:
                        value = location[alias]
                        break
                
                if value is not None:
                    break
            
            if value is None:
                # Try to derive from other parameters
                if param == 'bloom_entropy' and 'entropy' in data:
                    value = data['entropy']
                elif param == 'mood_valence' and 'valence' in data:
                    value = data['valence']
                elif param == 'pulse_zone':
                    # Default pulse zone
                    value = 'stable'
                    warnings.append(f"Missing {param}, using default: {value}")
            
            if value is None:
                if self.strict_validation:
                    warnings.append(f"Required parameter '{param}' not found")
                else:
                    # Provide sensible defaults
                    defaults = {
                        'bloom_entropy': 0.5,
                        'mood_valence': 0.0,
                        'drift_vector': 0.0,
                        'rebloom_depth': 5,
                        'sigil_saturation': 0.5,
                        'pulse_zone': 'stable'
                    }
                    value = defaults[param]
                    warnings.append(f"Missing {param}, using default: {value}")
            
            extracted[param] = value
        
        return extracted
    
    def _validate_parameters(self, extracted: Dict[str, Any], warnings: List[str]) -> Dict[str, Any]:
        """Validate and clamp parameters to valid ranges"""
        
        validated = {}
        
        for param, value in extracted.items():
            if value is None:
                warnings.append(f"Parameter {param} is None")
                continue
            
            if param == 'pulse_zone':
                # Validate pulse zone
                if isinstance(value, str) and value.lower() in self.valid_pulse_zones:
                    validated[param] = value.lower()
                else:
                    warnings.append(f"Invalid pulse_zone '{value}', using 'stable'")
                    validated[param] = 'stable'
            
            elif param in self.parameter_ranges:
                # Validate numeric parameters
                min_val, max_val = self.parameter_ranges[param]
                
                try:
                    # Convert to appropriate type
                    if param == 'rebloom_depth':
                        numeric_value = int(value)
                    else:
                        numeric_value = float(value)
                    
                    # Check range
                    if min_val <= numeric_value <= max_val:
                        validated[param] = numeric_value
                    else:
                        # Clamp to valid range
                        clamped_value = max(min_val, min(max_val, numeric_value))
                        if param == 'rebloom_depth':
                            clamped_value = int(clamped_value)
                        
                        warnings.append(
                            f"Parameter {param} value {numeric_value} out of range "
                            f"[{min_val}, {max_val}], clamped to {clamped_value}"
                        )
                        validated[param] = clamped_value
                
                except (ValueError, TypeError) as e:
                    warnings.append(f"Invalid {param} value '{value}': {e}")
                    # Use midpoint of range as default
                    if param == 'rebloom_depth':
                        default_value = int((min_val + max_val) / 2)
                    else:
                        default_value = (min_val + max_val) / 2.0
                    validated[param] = default_value
            else:
                # Unknown parameter, pass through
                validated[param] = value
        
        return validated
    
    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract optional metadata from data"""
        
        metadata = {}
        
        # Common metadata fields
        metadata_fields = {
            'timestamp': ['timestamp', 'created_at', 'time'],
            'memory_id': ['memory_id', 'id', 'identifier'],
            'archetype': ['archetype', 'consciousness_archetype', 'type'],
            'fractal_string': ['fractal_string', 'pattern_string', 'encoding']
        }
        
        for field, aliases in metadata_fields.items():
            value = None
            
            # Search for field in various locations
            search_locations = [
                data,
                data.get('visual_characteristics', {}),
                data.get('soul_archive_data', {}),
                data.get('metadata', {})
            ]
            
            for location in search_locations:
                if not isinstance(location, dict):
                    continue
                
                for alias in aliases:
                    if alias in location:
                        value = location[alias]
                        break
                
                if value is not None:
                    break
            
            if value is not None:
                metadata[field] = value
        
        return metadata
    
    def validate_consciousness_state(self, config: DAWNConsciousnessConfig) -> bool:
        """
        Perform additional validation on consciousness state coherence
        
        Args:
            config: Consciousness configuration to validate
            
        Returns:
            True if state is coherent, False otherwise
        """
        
        # Check for impossible combinations
        warnings = []
        
        # Very high entropy with very low drift is unusual
        if config.bloom_entropy > 0.8 and abs(config.drift_vector) < 0.1:
            warnings.append("High entropy with low drift may indicate unstable state")
        
        # Very negative valence with high saturation is concerning
        if config.mood_valence < -0.7 and config.sigil_saturation > 0.8:
            warnings.append("Very negative valence with high saturation may indicate distress")
        
        # Very deep rebloom with crystalline zone is unusual
        if config.rebloom_depth > 15 and config.pulse_zone == 'crystalline':
            warnings.append("Deep rebloom with crystalline zone may be contradictory")
        
        if warnings:
            logger.warning(f"Consciousness state coherence warnings: {'; '.join(warnings)}")
            return False
        
        return True


def test_dawn_state_parser():
    """Test the DAWN state parser with various input scenarios"""
    
    print("🧠 Testing DAWN State Parser")
    print("=" * 30)
    
    parser = DAWNStateParser(strict_validation=False)
    
    # Test 1: Valid complete data
    print("\n✅ Test 1: Valid Complete Data")
    valid_data = {
        "parameters": {
            "bloom_entropy": 0.7,
            "mood_valence": -0.3,
            "drift_vector": 0.4,
            "rebloom_depth": 8,
            "sigil_saturation": 0.6,
            "pulse_zone": "flowing"
        },
        "timestamp": "2025-08-04T19:30:00",
        "memory_id": "test_memory_001"
    }
    
    config = parser.parse_data(valid_data)
    print(f"   Parsed successfully: {config.validation_passed}")
    print(f"   Fractal params: {config.to_fractal_params()}")
    
    # Test 2: Data with aliases
    print("\n🔄 Test 2: Data with Aliases")
    alias_data = {
        "entropy": 0.5,
        "valence": 0.8,
        "drift": -0.2,
        "depth": 12,
        "saturation": 0.9,
        "zone": "surge"
    }
    
    config = parser.parse_data(alias_data)
    print(f"   Parsed successfully: {config.validation_passed}")
    print(f"   Warnings: {len(config.validation_warnings)}")
    
    # Test 3: Out of range values
    print("\n⚠️  Test 3: Out of Range Values")
    invalid_data = {
        "parameters": {
            "bloom_entropy": 1.5,  # Too high
            "mood_valence": -2.0,  # Too low
            "drift_vector": 0.3,
            "rebloom_depth": 25,   # Too high
            "sigil_saturation": -0.1,  # Too low
            "pulse_zone": "invalid_zone"
        }
    }
    
    config = parser.parse_data(invalid_data)
    print(f"   Parsed with clamping: {config.validation_passed}")
    print(f"   Warnings: {len(config.validation_warnings)}")
    for warning in config.validation_warnings[:3]:
        print(f"     • {warning}")
    
    # Test 4: Missing parameters
    print("\n❌ Test 4: Missing Parameters")
    incomplete_data = {
        "bloom_entropy": 0.4,
        "mood_valence": 0.1
        # Missing other required parameters
    }
    
    config = parser.parse_data(incomplete_data)
    print(f"   Parsed with defaults: {config.validation_passed}")
    print(f"   Warnings: {len(config.validation_warnings)}")
    
    # Test 5: Voice parameter conversion
    print("\n🗣️  Test 5: Voice Parameter Conversion")
    config = parser.parse_data(valid_data)
    voice_params = config.to_voice_params()
    print(f"   Mood pigment: {voice_params['pigment_dict']}")
    print(f"   Sigil heat: {voice_params['sigil_state']}")
    
    # Test 6: Consciousness coherence validation
    print("\n🧠 Test 6: Consciousness Coherence")
    coherent = parser.validate_consciousness_state(config)
    print(f"   State is coherent: {coherent}")
    
    print(f"\n✨ DAWN State Parser testing complete!")


if __name__ == "__main__":
    test_dawn_state_parser() 