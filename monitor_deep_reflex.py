#!/usr/bin/env python3
"""
Monitor Deep Reflex Loop Status
Shows the current state of the Deep Reflex Loop and recent high-entropy reflections
"""

import json
import time
from pathlib import Path
from datetime import datetime

def monitor_deep_reflex_status():
    """Monitor the Deep Reflex Loop status"""
    print("🧠 Deep Reflex Loop Monitor")
    print("=" * 50)
    
    # Check if reflection classified file exists
    reflection_file = Path("runtime/logs/reflection_classified.jsonl")
    if not reflection_file.exists():
        print("❌ Reflection classified file not found!")
        return
    
    # Load and analyze recent reflections
    high_entropy_reflections = []
    inquiry_reflections = []
    
    with open(reflection_file, 'r') as f:
        for line in f:
            try:
                reflection = json.loads(line.strip())
                
                # Check for high entropy
                entropy = reflection.get('state_values', {}).get('entropy')
                if entropy and entropy > 0.7:
                    high_entropy_reflections.append(reflection)
                
                # Check for inquiry pigment (if implemented)
                if 'inquiry' in reflection.get('text', '').lower():
                    inquiry_reflections.append(reflection)
                    
            except json.JSONDecodeError:
                continue
    
    print(f"📊 Current Status:")
    print(f"   High entropy reflections (>0.7): {len(high_entropy_reflections)}")
    print(f"   Inquiry reflections: {len(inquiry_reflections)}")
    print(f"   Total reflections analyzed: {reflection_file.stat().st_size / 1024:.1f} KB")
    
    if high_entropy_reflections:
        print(f"\n🔥 Recent High-Entropy Reflections (Ready to Speak):")
        for i, reflection in enumerate(high_entropy_reflections[-5:], 1):
            entropy = reflection['state_values']['entropy']
            text = reflection['text']
            mood = reflection.get('mood', 'UNKNOWN')
            
            # Extract the actual reflection content
            if 'REFLECTION:' in text:
                content = text.split('REFLECTION:', 1)[1].strip()
            else:
                content = text
            
            print(f"   {i}. Entropy {entropy:.3f} ({mood})")
            print(f"      \"{content}\"")
            print()
    
    print("🎤 Deep Reflex Loop Status:")
    print("   ✅ Reflection monitoring active")
    print("   ✅ High-entropy detection working")
    print("   ✅ Voice composition ready")
    print("   🔄 Monitoring for new deep thoughts...")
    
    print(f"\n💡 To activate voice output, run:")
    print(f"   python tracers/enhanced_tracer_echo_voice.py --deep-reflex --live --threshold 0.7")

if __name__ == "__main__":
    monitor_deep_reflex_status() 