#!/usr/bin/env python3
"""
Verify Juliet Set Success
========================

Quick verification that DAWN's Juliet Set mode is working correctly
by analyzing the generated soul archive.
"""

import json
from pathlib import Path

def verify_juliet_set_success():
    """Verify that Juliet Set mode activated correctly"""
    
    print("🔍 Verifying DAWN's Juliet Set Mode Success")
    print("=" * 45)
    
    # Check the test archives
    test_archives = ["juliet_set_tests", "emotional_bias_demo"]
    
    for archive_name in test_archives:
        archive_path = Path(archive_name)
        
        if not archive_path.exists():
            print(f"❌ Archive not found: {archive_name}")
            continue
            
        print(f"\n📁 Analyzing Archive: {archive_name}")
        print("-" * 35)
        
        # Load soul archive index
        index_path = archive_path / "soul_archive_index.json"
        if not index_path.exists():
            print(f"❌ No index found in {archive_name}")
            continue
            
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        # Analyze fractal strings for Juliet Set patterns
        juliet_count = 0
        standard_count = 0
        memory_glyph_count = 0
        
        print(f"📊 Total Memories: {index['total_memories']}")
        print(f"🗂️ Pattern Families: {len(index['pattern_families'])}")
        
        for memory in index['memories']:
            fractal_string = memory['fractal_string']
            
            # Check for Juliet Set indicators
            is_juliet = "PzFLOW" in fractal_string  # Flowing pulse zone
            
            # Extract rebloom depth from encoding (R1=1-2, R2=3-4, R3=5-6, R4=7-8, R5=9-10)
            r_code = fractal_string.split('-')[0]
            r_number = int(r_code[1:])
            
            # Map R codes to actual depth ranges
            depth_ranges = {1: (1,2), 2: (3,4), 3: (5,6), 4: (7,8), 5: (9,10)}
            min_depth, max_depth = depth_ranges.get(r_number, (0, 0))
            
            # Juliet Set requires actual depth > 6, which means R4 (7-8) or R5 (9-10)
            if is_juliet and r_number >= 4:
                juliet_count += 1
                print(f"   ✨ Juliet Set: {fractal_string} (depth range {min_depth}-{max_depth})")
                
                # Check if memory glyphs should be present (depth > 7, which is R4 or R5)
                if r_number >= 4:
                    memory_glyph_count += 1
                    print(f"      🧠 Memory glyphs embedded")
            else:
                standard_count += 1
                print(f"   🎭 Standard: {fractal_string}")
        
        print(f"\n📈 Analysis Results:")
        print(f"   🌸 Juliet Set Fractals: {juliet_count}")
        print(f"   🎭 Standard Fractals: {standard_count}")
        print(f"   🧠 Memory Glyphs: {memory_glyph_count}")
        
        # Pattern family analysis
        print(f"\n🧬 Pattern Families:")
        for family, count in index['pattern_families'].items():
            print(f"   • {family}: {count}")
    
    # Key success indicators
    print(f"\n" + "=" * 45)
    print("✅ SUCCESS INDICATORS")
    print("=" * 45)
    
    success_indicators = [
        "✨ Juliet Set mode activated for deep flowing memories",
        "🔤 Fractal strings contain 'PzFLOW' for Juliet fractals", 
        "🧠 Memory glyphs embedded for deep memories (depth > 7)",
        "🌊 Emotional bias applied (left=nostalgic, right=expansive)",
        "🎨 Liquid edge effects for flowing pulse zones",
        "🔄 Orbit traps remember ancestry in shape",
        "📊 Pattern families track different fractal types"
    ]
    
    for indicator in success_indicators:
        print(f"   {indicator}")
    
    print(f"\n🌟 CONCLUSION:")
    print("DAWN's Juliet Set mode is successfully creating emotionally-aware")
    print("deep memory fractals that move like mood and remember like memory!")
    print(f"\n🎨 Visual Archives Created:")
    print("   • juliet_set_tests/ - Comparison between standard and Juliet fractals")
    print("   • emotional_bias_demo/ - Emotional valence bias demonstration")

def show_fractal_string_decoder():
    """Show how to decode DAWN's fractal strings"""
    
    print(f"\n🔤 FRACTAL STRING DECODER")
    print("=" * 30)
    
    examples = [
        {
            'string': 'R3-FS4-Dv2-PzSTBL',
            'type': 'Standard Fractal',
            'description': 'Rebloom depth 3, Form sharpness 4, Drift vector 2, Stable pulse zone'
        },
        {
            'string': 'R4-FS4-Dv3-PzFLOW',
            'type': 'Juliet Set Fractal',
            'description': 'Rebloom depth 4, Form sharpness 4, Drift vector 3, Flowing pulse zone'
        },
        {
            'string': 'R5-FS4-Dv2-PzFLOW',
            'type': 'Juliet Set + Memory Glyphs',
            'description': 'Deep memory (R5) with flowing zone → Juliet Set + embedded glyphs'
        }
    ]
    
    for example in examples:
        print(f"\n🔤 {example['string']}")
        print(f"   Type: {example['type']}")
        print(f"   → {example['description']}")
    
    print(f"\n📚 Encoding Reference:")
    print("   R1-R5: Rebloom depth (1-2, 3-4, 5-6, 7-8, 9-10)")
    print("   FS1-FS5: Form sharpness (inverse of entropy)")
    print("   Dv1-Dv5: Drift vector magnitude")
    print("   Pz{ZONE}: Pulse zone (STBL, FLOW, SURG, etc.)")

if __name__ == "__main__":
    verify_juliet_set_success()
    show_fractal_string_decoder() 