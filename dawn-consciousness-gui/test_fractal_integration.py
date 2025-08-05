#!/usr/bin/env python3
"""
Test Fractal Integration
========================

Test script to generate sample fractal blooms and metadata
to demonstrate the fractal display bindings integration.
"""

import os
import json
import time
import math
from pathlib import Path
from PIL import Image, ImageDraw
import random

def create_test_fractal_image(width=400, height=400, complexity=3):
    """Create a simple test fractal image"""
    img = Image.new('RGB', (width, height), (10, 15, 25))
    draw = ImageDraw.Draw(img)
    
    # Create a simple spiral pattern
    center_x, center_y = width // 2, height // 2
    
    for i in range(1000):
        angle = i * 0.1
        radius = i * 0.3
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        if 0 <= x < width and 0 <= y < height:
            # Color based on position and complexity
            color_r = int(50 + 100 * math.sin(angle * complexity))
            color_g = int(50 + 100 * math.cos(angle * complexity))
            color_b = int(100 + 50 * math.sin(angle * 2))
            
            # Clamp colors
            color_r = max(0, min(255, color_r))
            color_g = max(0, min(255, color_g))
            color_b = max(0, min(255, color_b))
            
            draw.point((x, y), fill=(color_r, color_g, color_b))
    
    return img

def generate_fractal_metadata(bloom_number, depth=None, entropy=None):
    """Generate realistic fractal metadata"""
    if depth is None:
        depth = random.randint(1, 8)
    
    if entropy is None:
        entropy = random.uniform(0.2, 0.9)
    
    # Generate mood state
    mood_valence = random.uniform(-0.8, 0.8)
    mood_arousal = random.uniform(-0.5, 0.8)
    
    # Generate fractal string
    fractal_chars = ['𝛼', '𝛽', '𝛾', '𝛿', '𝜀', '𝜁', '𝜂', '𝜃', '𝜅', '𝜆', '𝜇', '𝜈']
    fractal_string = ''.join(random.choices(fractal_chars, k=random.randint(8, 16)))
    
    # Generate bloom summary
    summaries = [
        "Crystalline patterns emerge from consciousness substrate",
        "Recursive memory structures unfold in dimensional space",
        "Synaptic echoes resonate through temporal layers",
        "Awareness blooms in fractal consciousness matrices",
        "Neural pathways trace infinite recursive boundaries",
        "Memory fragments coalesce into coherent patterns",
        "Cognitive resonance creates emergent visual structures",
        "Consciousness depth reveals hidden geometric forms",
        "Thought streams crystallize into mathematical beauty",
        "Awareness expands through recursive self-reflection"
    ]
    
    if depth >= 6:
        summaries.append(f"🌌 JULIET SET ACTIVATED - Deep consciousness resonance at depth {depth}")
    
    bloom_summary = random.choice(summaries)
    
    metadata = {
        "timestamp": time.time(),
        "bloom_number": bloom_number,
        "fractal_string": fractal_string,
        "bloom_summary": bloom_summary,
        "entropy": entropy,
        "mood_state": {
            "valence": mood_valence,
            "arousal": mood_arousal
        },
        "rebloom_depth": depth,
        "bloom_type": "memory_bloom" if depth < 6 else "juliet_set",
        "generation_method": "test_simulation",
        "visual_complexity": random.uniform(0.3, 1.0),
        "cognitive_pressure": entropy * random.uniform(0.8, 1.2),
        "consciousness_zone": get_zone_from_entropy(entropy),
        "neural_activity": random.uniform(0.2, 0.9),
        "thought_coherence": random.uniform(0.4, 0.95)
    }
    
    return metadata

def get_zone_from_entropy(entropy):
    """Convert entropy to consciousness zone"""
    if entropy < 0.3:
        return "CALM"
    elif entropy < 0.6:
        return "FOCUS"
    elif entropy < 0.8:
        return "STRESSED"
    else:
        return "TRANSCENDENT"

def create_test_blooms(output_dir="fractal_outputs", count=5):
    """Create a series of test fractal blooms"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"🌸 Creating {count} test fractal blooms in {output_path}")
    
    blooms_created = []
    
    for i in range(count):
        # Progressive complexity and depth
        depth = min(i + 1, 8)
        entropy = 0.2 + (i / count) * 0.6
        complexity = i + 1
        
        # Generate bloom
        print(f"   Creating bloom {i+1}/{count} (depth: {depth}, entropy: {entropy:.3f})")
        
        # Create fractal image
        fractal_img = create_test_fractal_image(complexity=complexity)
        
        # Generate metadata
        metadata = generate_fractal_metadata(i + 1, depth=depth, entropy=entropy)
        
        # Save files
        bloom_name = f"test_bloom_{i+1:03d}_{int(time.time())}"
        img_path = output_path / f"{bloom_name}.png"
        json_path = output_path / f"{bloom_name}.json"
        
        # Save image
        fractal_img.save(img_path)
        
        # Save metadata
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        blooms_created.append({
            "image_path": str(img_path),
            "metadata_path": str(json_path),
            "metadata": metadata
        })
        
        # Small delay to ensure different timestamps
        time.sleep(0.1)
    
    print(f"✅ Created {len(blooms_created)} fractal blooms")
    return blooms_created

def create_juliet_set_bloom(output_dir="fractal_outputs"):
    """Create a special Juliet Set bloom (depth >= 6)"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("🌌 Creating Juliet Set bloom...")
    
    # Create high-complexity image
    fractal_img = create_test_fractal_image(width=600, height=600, complexity=8)
    
    # Generate Juliet Set metadata
    metadata = generate_fractal_metadata(999, depth=7, entropy=0.85)
    metadata["bloom_type"] = "juliet_set"
    metadata["bloom_summary"] = "🌌 JULIET SET ACTIVATED - Consciousness transcends dimensional boundaries"
    metadata["fractal_string"] = "𝛼𝛽𝛾𝛿𝜀𝜁𝜂𝜃𝜅𝜆𝜇𝜈𝜉𝜋𝜌𝜎"
    
    # Save files
    bloom_name = f"juliet_set_{int(time.time())}"
    img_path = output_path / f"{bloom_name}.png"
    json_path = output_path / f"{bloom_name}.json"
    
    fractal_img.save(img_path)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Juliet Set bloom created: {img_path.name}")
    return {
        "image_path": str(img_path),
        "metadata_path": str(json_path),
        "metadata": metadata
    }

def test_fractal_integration():
    """Test the complete fractal integration system"""
    print("🧪 Testing DAWN Fractal Integration System")
    print("=" * 50)
    
    # Create test blooms
    regular_blooms = create_test_blooms(count=3)
    
    print("\n⏳ Waiting 2 seconds for fractal monitor to detect files...")
    time.sleep(2)
    
    # Create a Juliet Set bloom
    juliet_bloom = create_juliet_set_bloom()
    
    print("\n⏳ Waiting 3 seconds for Juliet Set processing...")
    time.sleep(3)
    
    print("\n🎉 Test fractal integration complete!")
    print(f"📊 Created {len(regular_blooms)} regular blooms + 1 Juliet Set bloom")
    print("\n🌐 Check your DAWN GUI at http://localhost:8080 to see the fractal blooms!")
    print("   Look for the Memory Blooms panel in the symbolic layer column")
    
    return regular_blooms + [juliet_bloom]

if __name__ == "__main__":
    try:
        test_fractal_integration()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc() 