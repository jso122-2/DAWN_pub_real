#!/usr/bin/env python3
"""
Script to copy the enhanced_spawn_bloom content to the proper location
Run this from the core directory
"""

import os
from pathlib import Path

# The enhanced spawn bloom content from the document
ENHANCED_BLOOM_CONTENT = '''# /bloom/enhanced_spawn_bloom.py
# Enhanced spawn_bloom with better SCUP handling and emergency recovery integration

import os
import json
from datetime import datetime
from typing import Dict, Optional

# Safe imports with fallback handling
def safe_import_fractal():
    try:
        from fractal.fractal_generator import generate_julia_image
        return generate_julia_image
    except ImportError:
        print("[SpawnBloom] ⚠️ Fractal generator not available")
        return lambda *args, **kwargs: "fractal_unavailable.png"

def safe_import_scup():
    try:
        from schema.scup_loop import calculate_SCUP
        return calculate_SCUP
    except ImportError:
        print("[SpawnBloom] ⚠️ SCUP calculator not available, using fallback")
        return lambda **kwargs: 0.5  # Neutral SCUP value

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
        from owl.owl_rebloom_router import route_rebloom
        components['route'] = route_rebloom
    except ImportError:
        components['route'] = lambda x: None
    
    return components

def safe_import_helix():
    """Safely import helix bridge for thermal coordination"""
    try:
        from helix_bridge import HELIX_BRIDGE
        return HELIX_BRIDGE
    except ImportError:
        print("[SpawnBloom] ⚠️ Helix bridge not available")
        return None

# Initialize safe imports
generate_julia_image = safe_import_fractal()
calculate_SCUP = safe_import_scup()
dawn_components = safe_import_components()
helix_bridge = safe_import_helix()

# Configuration
BLOOM_DIR = "juliet_flowers/bloom_metadata"
CSV_LOG = "juliet_flowers/bloom_log.csv"
SCUP_CSV = "juliet_flowers/scup_bloom_correlation.csv"
PRESSURE_PATH = "juliet_flowers/cluster_report/nutrient_pressure.json"

# Global tracking
_current_active_bloom = None
_bloom_counter = 0
_successful_blooms = 0
_failed_blooms = 0

def get_current_active_bloom():
    """Get currently active bloom"""
    return _current_active_bloom

def enhanced_spawn_bloom(bloom_data: Dict, pulse: Dict, bypass_scup: bool = False) -> Optional[str]:
    """
    Enhanced bloom spawning with better error handling and SCUP management
    
    Args:
        bloom_data: Bloom configuration data
        pulse: Pulse/heat system state
        bypass_scup: If True, skip SCUP gating (for debug/emergency blooms)
    
    Returns:
        Path to bloom metadata file or None if failed
    """
    global _current_active_bloom, _bloom_counter, _successful_blooms, _failed_blooms
    
    _bloom_counter += 1
    
    # Extract bloom parameters
    seed_id = bloom_data.get("seed_id", f"unnamed_bloom_{_bloom_counter}")
    depth = bloom_data.get("lineage_depth", 1)
    factor = bloom_data.get("bloom_factor", 1.0)
    entropy = bloom_data.get("entropy_score", 0.5)
    mood = bloom_data.get("mood", "reflective")
    trigger_type = bloom_data.get("trigger_type", "manual")
    
    print(f"[EnhancedBloom] 🌸 Attempting spawn: {seed_id}")
    print(f"  Trigger: {trigger_type} | Depth: {depth} | Factor: {factor:.3f} | Mood: {mood}")
    
    # Helix-aware thermal check
    if helix_bridge:
        thermal_state = helix_bridge.get_integration_status()
        if thermal_state.get("thermal_emergency", False):
            print(f"[EnhancedBloom] 🚨 Thermal emergency detected - reducing bloom factor")
            factor = min(factor * 0.5, 1.0)  # Reduce thermal contribution
            bloom_data["bloom_factor"] = factor
            bloom_data["thermal_adjusted"] = True
    
    # SCUP calculation and gating
    if not bypass_scup:
        pulse_pressure = min(factor / 5.0, 1.0)
        scup = calculate_SCUP(delta_vector=0.3, pulse_pressure=pulse_pressure, drift_variance=entropy)
        
        # Dynamic SCUP threshold based on trigger type
        scup_thresholds = {
            "emergency_bloom": 0.0,    # Always allow emergency blooms
            "debug_bloom": 0.0,        # Always allow debug blooms
            "curiosity_spike": 0.1,    # Low threshold for curiosity
            "memory_pressure": 0.2,    # Low threshold for memory
            "emotional_resonance": 0.3, # Medium threshold for emotions
            "semantic_drift": 0.4      # Higher threshold for drift
        }
        
        threshold = scup_thresholds.get(trigger_type, 0.2)  # Default lower threshold
        
        if scup < threshold:
            print(f"[EnhancedBloom] ❌ SCUP gating: {scup:.3f} < {threshold:.3f} (trigger: {trigger_type})")
            _failed_blooms += 1
            return f"[SCUP_BLOCKED] {seed_id} (scup:{scup:.3f} < {threshold:.3f})"
        
        print(f"[EnhancedBloom] ✅ SCUP passed: {scup:.3f} >= {threshold:.3f}")
        bloom_data["scup_at_spawn"] = scup
    else:
        print(f"[EnhancedBloom] 🔧 SCUP bypassed for {trigger_type}")
        bloom_data["scup_at_spawn"] = 0.0
    
    # Ensure directories exist
    os.makedirs(BLOOM_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(CSV_LOG), exist_ok=True)
    os.makedirs(os.path.dirname(SCUP_CSV), exist_ok=True)
    
    try:
        # Generate fractal visualization
        print(f"[EnhancedBloom] 🎨 Generating fractal for {seed_id}...")
        
        # Handle synthesis blooms differently
        is_synthesis = "synthesis" in trigger_type or factor > 2.0
        
        image_path = generate_julia_image(
            seed_id=seed_id,
            lineage_depth=depth,
            bloom_factor=factor,
            entropy_score=entropy,
            mood=mood,
            is_synthesis=is_synthesis
        )
        
        print(f"[EnhancedBloom] ✅ Fractal generated: {image_path}")
        bloom_data["image_path"] = image_path
        
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Fractal generation failed: {e}")
        bloom_data["image_path"] = "generation_failed.png"
    
    # Save bloom metadata
    timestamp_str = datetime.now().isoformat(timespec='seconds').replace(':', '-')
    metadata_filename = f"{seed_id}_{timestamp_str}.json"
    metadata_path = os.path.join(BLOOM_DIR, metadata_filename)
    
    # Add generation metadata
    bloom_data.update({
        "generated_at": datetime.now().isoformat(),
        "bloom_id": _bloom_counter,
        "generation_method": "enhanced_spawn_bloom",
        "scup_bypassed": bypass_scup
    })
    
    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(bloom_data, f, indent=2)
        print(f"[EnhancedBloom] 💾 Metadata saved: {metadata_path}")
    except Exception as e:
        print(f"[EnhancedBloom] ❌ Failed to save metadata: {e}")
        _failed_blooms += 1
        return None
    
    # Log to CSV files
    try:
        _log_bloom_to_csv(bloom_data, metadata_path)
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ CSV logging failed: {e}")
    
    # Handle nutrient logging
    try:
        dawn_components['nutrient_log'](bloom_data)
        dawn_components['nutrient_flow'](bloom=bloom_data, flow_strength=factor)
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Nutrient logging failed: {e}")
    
    # Handle mood pressure (with safeguards)
    try:
        _update_mood_pressure(bloom_data, pulse, mood, factor, entropy)
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Mood pressure update failed: {e}")
    
    # Optional components (owl, animation, routing)
    try:
        dawn_components['owl_log'](bloom_data)
        dawn_components['animate']()
        dawn_components['route'](bloom_data)
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Optional component failed: {e}")
    
    # Check for suppression
    try:
        should_suppress = _check_bloom_suppression(bloom_data)
        if should_suppress:
            return _handle_suppressed_bloom(bloom_data, metadata_path, pulse)
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Suppression check failed: {e}")
    
    # Success!
    _current_active_bloom = bloom_data
    _successful_blooms += 1
    
    print(f"[EnhancedBloom] 🎉 Bloom spawned successfully: {seed_id}")
    print(f"[EnhancedBloom] 📊 Success rate: {_successful_blooms}/{_bloom_counter} ({_successful_blooms/_bloom_counter*100:.1f}%)")
    
    return metadata_path

def _log_bloom_to_csv(bloom_data: Dict, metadata_path: str) -> None:
    """Log bloom to CSV files"""
    
    # Main bloom log
    if not os.path.exists(CSV_LOG) or os.stat(CSV_LOG).st_size == 0:
        with open(CSV_LOG, "w", encoding="utf-8") as f:
            f.write("timestamp,seed_id,lineage_depth,mood,entropy_score,bloom_factor,scup,trigger_type\\n")
    
    with open(CSV_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()},{bloom_data['seed_id']},{bloom_data['lineage_depth']},"
                f"{bloom_data['mood']},{bloom_data['entropy_score']:.3f},{bloom_data['bloom_factor']:.3f},"
                f"{bloom_data.get('scup_at_spawn', 0.0):.3f},{bloom_data.get('trigger_type', 'manual')}\\n")
    
    # SCUP correlation log
    if not os.path.exists(SCUP_CSV) or os.stat(SCUP_CSV).st_size == 0:
        with open(SCUP_CSV, "w", encoding="utf-8") as f:
            f.write("timestamp,seed_id,depth,entropy_score,bloom_factor,mood,scup,trigger_type,success\\n")
    
    with open(SCUP_CSV, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()},{bloom_data['seed_id']},{bloom_data['lineage_depth']},"
                f"{bloom_data['entropy_score']:.3f},{bloom_data['bloom_factor']:.3f},{bloom_data['mood']},"
                f"{bloom_data.get('scup_at_spawn', 0.0):.3f},{bloom_data.get('trigger_type', 'manual')},success\\n")

def _update_mood_pressure(bloom_data: Dict, pulse: Dict, mood: str, factor: float, entropy: float) -> None:
    """Update mood pressure with safeguards"""
    
    # Calculate mood pressure contribution (reduced to prevent heat explosions)
    mood_pressure_contribution = min(factor * entropy * 0.1, 0.3)  # Capped at 0.3
    
    # Initialize mood_pressure if it doesn't exist
    if not hasattr(pulse, 'mood_pressure'):
        pulse['mood_pressure'] = {}
    
    mood_pressure = pulse.get('mood_pressure', {})
    mood_pressure[mood] = mood_pressure.get(mood, 0.0) + mood_pressure_contribution
    
    # Cap total mood pressure to prevent thermal runaway
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
        
        os.makedirs(os.path.dirname(PRESSURE_PATH), exist_ok=True)
        with open(PRESSURE_PATH, "w", encoding="utf-8") as f:
            json.dump(pressure_data, f, indent=2)
            
        print(f"[EnhancedBloom] 📊 Mood pressure updated: {mood}={mood_pressure[mood]:.3f}")
        
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Pressure file update failed: {e}")

def _check_bloom_suppression(bloom_data: Dict) -> bool:
    """Check if bloom should be suppressed due to system conditions"""
    
    # Check helix thermal state
    if helix_bridge:
        thermal_state = helix_bridge.get_integration_status()
        
        # Suppress if emergency override is active
        if thermal_state.get("emergency_override", False):
            print(f"[EnhancedBloom] 🚨 Bloom suppression: Emergency override active")
            return True
            
        # Suppress if thermal heat is too high
        if thermal_state.get("thermal_heat", 0) >= 9.0:
            print(f"[EnhancedBloom] 🔥 Bloom suppression: Thermal heat too high ({thermal_state.get('thermal_heat', 0):.2f})")
            return True
    
    # Check bloom factor limits
    factor = bloom_data.get("bloom_factor", 1.0)
    if factor > 3.0:
        print(f"[EnhancedBloom] ⚠️ Bloom suppression: Factor too high ({factor:.2f})")
        return True
    
    # Check for rapid succession (bloom spam prevention)
    if _bloom_counter > _successful_blooms * 3:  # More than 2/3 failure rate
        print(f"[EnhancedBloom] 🛑 Bloom suppression: High failure rate ({_failed_blooms}/{_bloom_counter})")
        return True
    
    return False

def _handle_suppressed_bloom(bloom_data: Dict, metadata_path: str, pulse: Dict) -> str:
    """Handle a suppressed bloom gracefully"""
    
    # Mark as suppressed
    bloom_data["suppressed"] = True
    bloom_data["suppression_reason"] = "system_protection"
    bloom_data["suppressed_at"] = datetime.now().isoformat()
    
    # Save suppressed bloom metadata
    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(bloom_data, f, indent=2)
    except Exception as e:
        print(f"[EnhancedBloom] ❌ Failed to save suppressed bloom metadata: {e}")
    
    # Log suppression to CSV
    if not os.path.exists(SCUP_CSV) or os.stat(SCUP_CSV).st_size == 0:
        with open(SCUP_CSV, "w", encoding="utf-8") as f:
            f.write("timestamp,seed_id,depth,entropy_score,bloom_factor,mood,scup,trigger_type,success\\n")
    
    try:
        with open(SCUP_CSV, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()},{bloom_data['seed_id']},{bloom_data['lineage_depth']},"
                    f"{bloom_data['entropy_score']:.3f},{bloom_data['bloom_factor']:.3f},{bloom_data['mood']},"
                    f"{bloom_data.get('scup_at_spawn', 0.0):.3f},{bloom_data.get('trigger_type', 'manual')},suppressed\\n")
    except Exception as e:
        print(f"[EnhancedBloom] ⚠️ Suppression logging failed: {e}")
    
    _failed_blooms += 1
    
    print(f"[EnhancedBloom] 🛑 Bloom suppressed: {bloom_data['seed_id']}")
    return f"[SUPPRESSED] {bloom_data['seed_id']}"

def get_bloom_statistics() -> Dict:
    """Get current bloom spawning statistics"""
    return {
        "total_attempts": _bloom_counter,
        "successful_blooms": _successful_blooms,
        "failed_blooms": _failed_blooms,
        "success_rate": _successful_blooms / max(_bloom_counter, 1) * 100,
        "current_active_bloom": _current_active_bloom.get("seed_id") if _current_active_bloom else None
    }

def emergency_spawn_bloom(seed_id: str, mood: str = "emergency") -> Optional[str]:
    """Emergency bloom spawning with minimal gating"""
    
    emergency_bloom_data = {
        "seed_id": seed_id,
        "lineage_depth": 1,
        "bloom_factor": 0.5,  # Reduced for emergency
        "entropy_score": 0.3,
        "mood": mood,
        "trigger_type": "emergency_bloom"
    }
    
    # Minimal pulse state
    emergency_pulse = {"heat": 0.0, "mood_pressure": {}}
    
    print(f"[EnhancedBloom] 🚨 Emergency bloom spawn: {seed_id}")
    return enhanced_spawn_bloom(emergency_bloom_data, emergency_pulse, bypass_scup=True)

def debug_spawn_bloom(seed_id: str, **kwargs) -> Optional[str]:
    """Debug bloom spawning for testing"""
    
    debug_bloom_data = {
        "seed_id": seed_id,
        "lineage_depth": kwargs.get("depth", 1),
        "bloom_factor": kwargs.get("factor", 1.0),
        "entropy_score": kwargs.get("entropy", 0.5),
        "mood": kwargs.get("mood", "debug"),
        "trigger_type": "debug_bloom"
    }
    
    # Override with any provided kwargs
    debug_bloom_data.update(kwargs)
    
    debug_pulse = {"heat": 0.0, "mood_pressure": {}}
    
    print(f"[EnhancedBloom] 🔧 Debug bloom spawn: {seed_id}")
    return enhanced_spawn_bloom(debug_bloom_data, debug_pulse, bypass_scup=True)

# Integration hooks for helix bridge
def helix_bloom_coordination(thermal_state: Dict, coherence_state: Dict) -> Dict:
    """Coordinate bloom spawning with helix thermal and coherence states"""
    
    recommendations = {
        "allow_blooming": True,
        "suggested_factor_reduction": 1.0,
        "emergency_cooling_needed": False,
        "coherence_boost_recommended": False
    }
    
    # Thermal considerations
    thermal_heat = thermal_state.get("thermal_heat", 0.0)
    if thermal_heat >= 9.0:
        recommendations["allow_blooming"] = False
        recommendations["emergency_cooling_needed"] = True
    elif thermal_heat >= 8.0:
        recommendations["suggested_factor_reduction"] = 0.5
    
    # Coherence considerations
    scup_value = coherence_state.get("scup_value", 0.5)
    if scup_value <= 0.1:
        recommendations["coherence_boost_recommended"] = True
        recommendations["suggested_factor_reduction"] = 0.3
    
    return recommendations

if __name__ == "__main__":
    # Test the enhanced bloom system
    print("[EnhancedBloom] 🧪 Running tests...")
    
    test_bloom = {
        "seed_id": "test_bloom_001",
        "lineage_depth": 2,
        "bloom_factor": 1.5,
        "entropy_score": 0.7,
        "mood": "curious",
        "trigger_type": "curiosity_spike"
    }
    
    test_pulse = {"heat": 5.0, "mood_pressure": {}}
    
    result = enhanced_spawn_bloom(test_bloom, test_pulse)
    print(f"[EnhancedBloom] Test result: {result}")
    
    stats = get_bloom_statistics()
    print(f"[EnhancedBloom] Statistics: {stats}")
'''

def copy_enhanced_bloom():
    """Copy enhanced bloom content to proper location"""
    # Get the parent directory (should be Tick_engine)
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    
    # Create bloom directory
    bloom_dir = parent_dir / "bloom"
    bloom_dir.mkdir(exist_ok=True)
    
    # Write enhanced bloom file
    enhanced_file = bloom_dir / "enhanced_spawn_bloom.py"
    
    print(f"Writing enhanced bloom to: {enhanced_file}")
    
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        f.write(ENHANCED_BLOOM_CONTENT)
    
    print("✓ Enhanced bloom module created")
    
    # Create __init__.py
    init_file = bloom_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")
        print("✓ Created bloom/__init__.py")

if __name__ == "__main__":
    copy_enhanced_bloom()