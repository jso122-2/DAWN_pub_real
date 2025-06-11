"""
Unified Bloom Spawning System
Consolidates all spawn functionality with enhanced features
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, Optional, List, Any, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import hashlib
import math
import colorsys

# ============== Configuration ==============

BLOOM_DIR = "juliet_flowers/bloom_metadata"
CSV_LOG = "juliet_flowers/bloom_log.csv"
SCUP_CSV = "juliet_flowers/scup_bloom_correlation.csv"
PRESSURE_PATH = "juliet_flowers/cluster_report/nutrient_pressure.json"
FRACTAL_DIR = "juliet_flowers/fractal_signatures"
IMG_SIZE = (1024, 1024)

# Ensure directories exist
for directory in [BLOOM_DIR, FRACTAL_DIR, os.path.dirname(CSV_LOG), os.path.dirname(PRESSURE_PATH)]:
    os.makedirs(directory, exist_ok=True)


# ============== Safe Imports ==============

def safe_import_scup():
    """Safely import SCUP calculator"""
    try:
        from schema.scup_loop import calculate_SCUP
        return calculate_SCUP
    except ImportError:
        print("[SpawnBloom] ⚠️ SCUP calculator not available, using fallback")
        return lambda **kwargs: 0.5

def safe_import_components():
    """Safely import optional DAWN components"""
    components = {}
    
    try:
        from visual.rebloom_lineage_animator import animate_rebloom_lineage
        components['animate'] = animate_rebloom_lineage
    except ImportError:
        components['animate'] = lambda: None
    
    try:
        from owl.owl_rebloom_log import owl_log_rebloom
        components['owl_log'] = owl_log_rebloom
    except ImportError:
        components['owl_log'] = lambda x: None
    
    try:
        from mycelium.nutrient_logger import log_bloom_to_nutrient, log_nutrient_flow
        components['nutrient_log'] = log_bloom_to_nutrient
        components['nutrient_flow'] = log_nutrient_flow
    except ImportError:
        components['nutrient_log'] = lambda x: None
        components['nutrient_flow'] = lambda **kwargs: None
    
    try:
        from bloom_memory_system import write_bloom_json
        components['write_memory'] = write_bloom_json
    except ImportError:
        components['write_memory'] = lambda *args: None
    
    return components

def safe_import_helix():
    """Safely import helix bridge"""
    try:
        from helix_bridge import HELIX_BRIDGE
        return HELIX_BRIDGE
    except ImportError:
        print("[SpawnBloom] ⚠️ Helix bridge not available")
        return None

# Initialize imports
calculate_SCUP = safe_import_scup()
dawn_components = safe_import_components()
helix_bridge = safe_import_helix()


# ============== Enhanced Fractal Generator ==============

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
            'diagnostic': {'real': -0.7885, 'imag': 0.0, 'zoom': 1.4, 'rotation': 0.0},
            'emergency': {'real': -0.8, 'imag': 0.0, 'zoom': 0.7, 'rotation': 0.0},
            'debug': {'real': -0.7, 'imag': 0.27015, 'zoom': 1.0, 'rotation': 0.0}
        }

    def generate_enhanced_julia(self, seed_id: str, lineage_depth: int, bloom_factor: float, 
                              entropy_score: float, mood: str = "reflective", 
                              is_synthesis: bool = False) -> str:
        """Generate enhanced Julia fractal"""
        
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
        
        # Generate fractal data
        escape_data = self._generate_julia_set(width, height, c, zoom, rotation, 
                                               lineage_depth, bloom_factor, is_synthesis)
        
        # Apply coloring
        img_array = self._apply_mood_coloring(escape_data, mood, entropy_score)
        
        # Create PIL image
        img = Image.fromarray(img_array.astype(np.uint8))
        
        # Post-processing for synthesis blooms
        if is_synthesis:
            img = self._apply_synthesis_effects(img)
        
        # Add overlay
        img = self._add_overlay(img, seed_id, lineage_depth, mood, 
                               entropy_score, bloom_factor, c)
        
        # Save
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"{seed_id}_{timestamp}.png"
        filepath = os.path.join(FRACTAL_DIR, filename)
        img.save(filepath, quality=95)
        
        print(f"[Fractal] Generated: {filename} (C = {c_real:.4f} + {c_imag:.4f}i)")
        
        return filepath

    def _generate_julia_set(self, width: int, height: int, c: complex, 
                           zoom: float, rotation: float, lineage_depth: int, 
                           bloom_factor: float, is_synthesis: bool) -> np.ndarray:
        """Generate Julia set data"""
        # Coordinate arrays with rotation
        cos_rot = np.cos(rotation)
        sin_rot = np.sin(rotation)
        
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
        
        # Julia set iteration with smooth coloring
        escape_count = np.zeros(Z.shape, dtype=float)
        smooth_escape = np.zeros(Z.shape, dtype=float)
        
        for i in range(iterations):
            mask = np.abs(Z) <= 4
            Z[mask] = Z[mask]**2 + c
            
            # Track escape velocity
            escaped = (np.abs(Z) > 4) & (escape_count == 0)
            if np.any(escaped):
                smooth_escape[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
                escape_count[escaped] = i
        
        # Points that never escaped
        smooth_escape[escape_count == 0] = iterations
        
        # Normalize
        return smooth_escape / iterations

    def _apply_mood_coloring(self, data: np.ndarray, mood: str, entropy: float) -> np.ndarray:
        """Apply mood-based coloring to fractal data"""
        img_array = np.zeros((*data.shape, 3))
        
        if mood in ['curious', 'joyful']:
            # Warm colors - yellow to orange
            img_array[:,:,0] = np.clip(255 * (0.8 + 0.2 * data), 0, 255)
            img_array[:,:,1] = np.clip(255 * (0.6 + 0.4 * data), 0, 255)
            img_array[:,:,2] = np.clip(255 * data * 0.3, 0, 255)
        elif mood == 'anxious':
            # Purple to pink
            img_array[:,:,0] = np.clip(255 * (0.6 + 0.4 * data), 0, 255)
            img_array[:,:,1] = np.clip(255 * data * 0.4, 0, 255)
            img_array[:,:,2] = np.clip(255 * (0.4 + 0.6 * data), 0, 255)
        elif mood in ['reflective', 'focused']:
            # Blues and cyans
            img_array[:,:,0] = np.clip(255 * data * 0.3, 0, 255)
            img_array[:,:,1] = np.clip(255 * (0.3 + 0.7 * data), 0, 255)
            img_array[:,:,2] = np.clip(255 * (0.6 + 0.4 * data), 0, 255)
        elif mood == 'emergency':
            # Red alert
            img_array[:,:,0] = np.clip(255 * (0.7 + 0.3 * data), 0, 255)
            img_array[:,:,1] = np.clip(255 * data * 0.2, 0, 255)
            img_array[:,:,2] = np.clip(255 * data * 0.1, 0, 255)
        else:
            # Default gradient
            img_array[:,:,0] = np.clip(255 * data, 0, 255)
            img_array[:,:,1] = np.clip(255 * data * 0.8, 0, 255)
            img_array[:,:,2] = np.clip(255 * data * 0.6, 0, 255)
        
        # Add entropy-based variation
        if entropy > 0.7:
            noise = np.random.random(data.shape) * 0.1
            for i in range(3):
                img_array[:,:,i] = np.clip(img_array[:,:,i] * (1 + noise), 0, 255)
        
        return img_array

    def _apply_synthesis_effects(self, img: Image.Image) -> Image.Image:
        """Apply special effects for synthesis blooms"""
        # Add glow effect
        glow = img.filter(ImageFilter.GaussianBlur(radius=5))
        img = Image.blend(img, glow, alpha=0.3)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Add brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        return img

    def _add_overlay(self, img: Image.Image, seed_id: str, lineage_depth: int, 
                    mood: str, entropy_score: float, bloom_factor: float, 
                    c: complex) -> Image.Image:
        """Add information overlay to fractal"""
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Create semi-transparent overlay
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
        return img.convert('RGB')


# ============== Bloom Spawner ==============

class BloomSpawner:
    """Unified bloom spawning system"""
    
    def __init__(self):
        self.fractal_generator = EnhancedJuliaFractal()
        self._bloom_counter = 0
        self._successful_blooms = 0
        self._failed_blooms = 0
        self._current_active_bloom = None
        
    def spawn_bloom(self, bloom_data: Dict, pulse: Optional[Dict] = None, 
                   bypass_scup: bool = False) -> Optional[str]:
        """
        Main bloom spawning function
        """
        self._bloom_counter += 1
        
        # Extract parameters
        seed_id = bloom_data.get("seed_id", f"unnamed_bloom_{self._bloom_counter}")
        depth = bloom_data.get("lineage_depth", 1)
        factor = bloom_data.get("bloom_factor", 1.0)
        entropy = bloom_data.get("entropy_score", 0.5)
        mood = bloom_data.get("mood", "reflective")
        trigger_type = bloom_data.get("trigger_type", "manual")
        
        print(f"[Bloom] 🌸 Spawning: {seed_id} (trigger: {trigger_type})")
        
        # Get pulse state
        if pulse is None:
            pulse = self._get_default_pulse()
        
        # Thermal check with helix integration
        if helix_bridge:
            factor = self._apply_thermal_modulation(factor, bloom_data)
        
        # SCUP gating
        if not bypass_scup:
            scup_result = self._check_scup_gating(bloom_data, factor, entropy, trigger_type)
            if scup_result is not None:
                return scup_result
        
        # Generate fractal
        try:
            is_synthesis = "synthesis" in trigger_type or factor > 2.0
            
            image_path = self.fractal_generator.generate_enhanced_julia(
                seed_id=seed_id,
                lineage_depth=depth,
                bloom_factor=factor,
                entropy_score=entropy,
                mood=mood,
                is_synthesis=is_synthesis
            )
            
            bloom_data["image_path"] = image_path
            
        except Exception as e:
            print(f"[Bloom] ⚠️ Fractal generation failed: {e}")
            bloom_data["image_path"] = "generation_failed.png"
        
        # Save metadata
        metadata_path = self._save_bloom_metadata(bloom_data, bypass_scup)
        if not metadata_path:
            return None
        
        # Log to CSV
        self._log_bloom_to_csv(bloom_data)
        
        # Update mood pressure
        self._update_mood_pressure(bloom_data, pulse, mood, factor, entropy)
        
        # Handle components
        self._handle_bloom_components(bloom_data, factor)
        
        # Check suppression
        if self._check_bloom_suppression(bloom_data):
            return self._handle_suppressed_bloom(bloom_data, metadata_path, pulse)
        
        # Success!
        self._current_active_bloom = bloom_data
        self._successful_blooms += 1
        
        success_rate = self._successful_blooms / self._bloom_counter * 100
        print(f"[Bloom] 🎉 Success! Rate: {success_rate:.1f}%")
        
        return metadata_path

    def _get_default_pulse(self) -> Dict:
        """Get default pulse state"""
        try:
            import builtins
            pulse = getattr(builtins, 'pulse', None)
            if pulse:
                return {
                    "heat": pulse.get_heat() if hasattr(pulse, 'get_heat') else 0.0,
                    "mood_pressure": getattr(pulse, 'mood_pressure', {})
                }
        except:
            pass
        return {"heat": 0.0, "mood_pressure": {}}

    def _apply_thermal_modulation(self, factor: float, bloom_data: Dict) -> float:
        """Apply thermal modulation from helix bridge"""
        thermal_state = helix_bridge.get_integration_status()
        if thermal_state.get("thermal_emergency", False):
            print(f"[Bloom] 🚨 Thermal emergency - reducing bloom factor")
            factor = min(factor * 0.5, 1.0)
            bloom_data["thermal_adjusted"] = True
        return factor

    def _check_scup_gating(self, bloom_data: Dict, factor: float, 
                          entropy: float, trigger_type: str) -> Optional[str]:
        """Check SCUP gating conditions"""
        pulse_pressure = min(factor / 5.0, 1.0)
        scup = calculate_SCUP(delta_vector=0.3, pulse_pressure=pulse_pressure, 
                             drift_variance=entropy)
        
        # Dynamic thresholds
        scup_thresholds = {
            "emergency_bloom": 0.0,
            "debug_bloom": 0.0,
            "curiosity_spike": 0.1,
            "memory_pressure": 0.2,
            "emotional_resonance": 0.3,
            "semantic_drift": 0.4
        }
        
        threshold = scup_thresholds.get(trigger_type, 0.2)
        
        if scup < threshold:
            print(f"[Bloom] ❌ SCUP blocked: {scup:.3f} < {threshold:.3f}")
            self._failed_blooms += 1
            return f"[SCUP_BLOCKED] {bloom_data['seed_id']}"
        
        print(f"[Bloom] ✅ SCUP passed: {scup:.3f}")
        bloom_data["scup_at_spawn"] = scup
        return None

    def _save_bloom_metadata(self, bloom_data: Dict, bypass_scup: bool) -> Optional[str]:
        """Save bloom metadata to file"""
        timestamp_str = datetime.now().isoformat(timespec='seconds').replace(':', '-')
        metadata_filename = f"{bloom_data['seed_id']}_{timestamp_str}.json"
        metadata_path = os.path.join(BLOOM_DIR, metadata_filename)
        
        # Add generation metadata
        bloom_data.update({
            "generated_at": datetime.now().isoformat(),
            "bloom_id": self._bloom_counter,
            "generation_method": "unified_spawn_bloom",
            "scup_bypassed": bypass_scup
        })
        
        try:
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(bloom_data, f, indent=2)
            print(f"[Bloom] 💾 Metadata saved: {metadata_path}")
            return metadata_path
        except Exception as e:
            print(f"[Bloom] ❌ Failed to save metadata: {e}")
            self._failed_blooms += 1
            return None

    def _log_bloom_to_csv(self, bloom_data: Dict):
        """Log bloom to CSV files"""
        # Main bloom log
        if not os.path.exists(CSV_LOG) or os.stat(CSV_LOG).st_size == 0:
            with open(CSV_LOG, "w", encoding="utf-8") as f:
                f.write("timestamp,seed_id,lineage_depth,mood,entropy_score,bloom_factor,scup,trigger_type\n")
        
        with open(CSV_LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()},{bloom_data['seed_id']},"
                   f"{bloom_data['lineage_depth']},{bloom_data['mood']},"
                   f"{bloom_data['entropy_score']:.3f},{bloom_data['bloom_factor']:.3f},"
                   f"{bloom_data.get('scup_at_spawn', 0.0):.3f},"
                   f"{bloom_data.get('trigger_type', 'manual')}\n")

    def _update_mood_pressure(self, bloom_data: Dict, pulse: Dict, 
                             mood: str, factor: float, entropy: float):
        """Update mood pressure system"""
        # Calculate contribution (capped to prevent runaway)
        mood_pressure_contribution = min(factor * entropy * 0.1, 0.3)
        
        mood_pressure = pulse.get('mood_pressure', {})
        mood_pressure[mood] = mood_pressure.get(mood, 0.0) + mood_pressure_contribution
        
        # Cap total pressure
        for mood_key in mood_pressure:
            mood_pressure[mood_key] = min(mood_pressure[mood_key], 2.0)
        
        pulse['mood_pressure'] = mood_pressure
        
        # Update pressure file
        try:
            pressure_data = {
                "timestamp": datetime.now().isoformat(),
                "mood_pressures": mood_pressure,
                "total_pressure": sum(mood_pressure.values()),
                "last_bloom_contribution": mood_pressure_contribution,
                "bloom_id": bloom_data.get("seed_id", "unknown")
            }
            
            with open(PRESSURE_PATH, "w", encoding="utf-8") as f:
                json.dump(pressure_data, f, indent=2)
                
        except Exception as e:
            print(f"[Bloom] ⚠️ Pressure update failed: {e}")

    def _handle_bloom_components(self, bloom_data: Dict, factor: float):
        """Handle optional bloom components"""
        try:
            # Write memory
            if 'write_memory' in dawn_components:
                dawn_components['write_memory'](bloom_data, bloom_data.get('image_path', ''))
            
            # Nutrient logging
            dawn_components['nutrient_log'](bloom_data)
            dawn_components['nutrient_flow'](bloom=bloom_data, flow_strength=factor)
            
            # Other components
            dawn_components['owl_log'](bloom_data)
            dawn_components['animate']()
            
        except Exception as e:
            print(f"[Bloom] ⚠️ Component handling failed: {e}")

    def _check_bloom_suppression(self, bloom_data: Dict) -> bool:
        """Check if bloom should be suppressed"""
        # Helix thermal check
        if helix_bridge:
            thermal_state = helix_bridge.get_integration_status()
            if thermal_state.get("emergency_override", False):
                return True
            if thermal_state.get("thermal_heat", 0) >= 9.0:
                return True
        
        # Factor limit check
        if bloom_data.get("bloom_factor", 1.0) > 3.0:
            return True
        
        # Failure rate check
        if self._bloom_counter > self._successful_blooms * 3:
            return True
        
        return False

    def _handle_suppressed_bloom(self, bloom_data: Dict, metadata_path: str, 
                                pulse: Dict) -> str:
        """Handle suppressed bloom"""
        bloom_data["suppressed"] = True
        bloom_data["suppression_reason"] = "system_protection"
        bloom_data["suppressed_at"] = datetime.now().isoformat()
        
        # Save updated metadata
        try:
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(bloom_data, f, indent=2)
        except:
            pass
        
        self._failed_blooms += 1
        print(f"[Bloom] 🛑 Bloom suppressed: {bloom_data['seed_id']}")
        return f"[SUPPRESSED] {bloom_data['seed_id']}"

    def get_statistics(self) -> Dict:
        """Get bloom spawning statistics"""
        return {
            "total_attempts": self._bloom_counter,
            "successful_blooms": self._successful_blooms,
            "failed_blooms": self._failed_blooms,
            "success_rate": self._successful_blooms / max(self._bloom_counter, 1) * 100,
            "current_active_bloom": self._current_active_bloom.get("seed_id") if self._current_active_bloom else None
        }


# ============== Global Instance & Functions ==============

# Create global spawner
bloom_spawner = BloomSpawner()

# Main spawn function
def spawn_bloom(bloom_data: Dict, pulse: Optional[Dict] = None) -> Optional[str]:
    """Standard spawn bloom function"""
    return bloom_spawner.spawn_bloom(bloom_data, pulse, bypass_scup=False)

# Enhanced spawn function (explicit)
def enhanced_spawn_bloom(bloom_data: Dict, pulse: Dict, bypass_scup: bool = False) -> Optional[str]:
    """Enhanced spawn bloom with full control"""
    return bloom_spawner.spawn_bloom(bloom_data, pulse, bypass_scup)

# Emergency spawn
def emergency_spawn_bloom(seed_id: str, mood: str = "emergency") -> Optional[str]:
    """Emergency bloom spawning"""
    emergency_bloom_data = {
        "seed_id": seed_id,
        "lineage_depth": 1,
        "bloom_factor": 0.5,
        "entropy_score": 0.3,
        "mood": mood,
        "trigger_type": "emergency_bloom"
    }
    return bloom_spawner.spawn_bloom(emergency_bloom_data, None, bypass_scup=True)

# Debug spawn
def debug_spawn_bloom(seed_id: str, **kwargs) -> Optional[str]:
    """Debug bloom spawning"""
    debug_bloom_data = {
        "seed_id": seed_id,
        "lineage_depth": kwargs.get("depth", 1),
        "bloom_factor": kwargs.get("factor", 1.0),
        "entropy_score": kwargs.get("entropy", 0.5),
        "mood": kwargs.get("mood", "debug"),
        "trigger_type": "debug_bloom",
        **kwargs
    }
    return bloom_spawner.spawn_bloom(debug_bloom_data, None, bypass_scup=True)

# Statistics functions
def get_bloom_statistics() -> Dict:
    """Get bloom statistics"""
    return bloom_spawner.get_statistics()

def get_bloom_stats():
    """Alias for statistics"""
    return get_bloom_statistics()

def print_bloom_statistics():
    """Print statistics"""
    stats = get_bloom_statistics()
    print("\n🌸 BLOOM STATISTICS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

def print_bloom_status(heat: float, scup: float, entropy: float, mood: str):
    """Print bloom system status"""
    print(f"\n🌸 BLOOM STATUS:")
    print(f"  Heat: {heat:.2f}")
    print(f"  SCUP: {scup:.3f}")
    print(f"  Entropy: {entropy:.3f}")
    print(f"  Mood: {mood}")
    stats = get_bloom_statistics()
    print(f"  Success Rate: {stats['success_rate']:.1f}%")
    print(f"  Active Bloom: {stats['current_active_bloom']}")

# Compatibility functions
def force_spawn_bloom(seed_id: str = "forced_bloom", **kwargs) -> str:
    """Force spawn a bloom"""
    return debug_spawn_bloom(seed_id, **kwargs) or f"[FAILED] {seed_id}"

def check_bloom_conditions(*args, **kwargs):
    """Placeholder for condition checking"""
    return None

def enable_bloom_debug(enabled: bool = True):
    """Enable/disable debug mode"""
    global BLOOM_DEBUG
    BLOOM_DEBUG = enabled
    print(f"[Bloom] Debug mode: {'enabled' if enabled else 'disabled'}")

def get_current_active_bloom():
    """Get current active bloom"""
    return bloom_spawner._current_active_bloom


# ============== Test Functions ==============

if __name__ == "__main__":
    print("🌸 Unified Bloom Spawner Test")
    print("=" * 50)
    
    # Test different bloom types
    test_blooms = [
        {
            "name": "Curious Bloom",
            "data": {
                "seed_id": "test_curious_001",
                "lineage_depth": 2,
                "bloom_factor": 1.5,
                "entropy_score": 0.7,
                "mood": "curious",
                "trigger_type": "curiosity_spike"
            }
        },
        {
            "name": "Emergency Bloom",
            "data": {
                "seed_id": "test_emergency_001",
                "lineage_depth": 1,
                "bloom_factor": 0.5,
                "entropy_score": 0.3,
                "mood": "emergency",
                "trigger_type": "emergency_bloom"
            }
        },
        {
            "name": "Synthesis Bloom",
            "data": {
                "seed_id": "test_synthesis_001",
                "lineage_depth": 5,
                "bloom_factor": 2.5,
                "entropy_score": 0.9,
                "mood": "reflective",
                "trigger_type": "synthesis"
            }
        }
    ]
    
    for test in test_blooms:
        print(f"\n{'='*30}")
        print(f"Testing: {test['name']}")
        print(f"{'='*30}")
        
        result = spawn_bloom(test['data'])
        print(f"Result: {result}")
    
    # Print final statistics
    print("\n" + "="*50)
    print_bloom_statistics()
    
    print("\n✅ Bloom spawner test complete!")