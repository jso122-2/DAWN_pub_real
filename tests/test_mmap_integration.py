#!/usr/bin/env python3
"""
Test script to verify mmap data compatibility between Python writer and Rust reader
Simulates the exact same reading process that the Tauri GUI performs
"""

import mmap
import struct
import time
import os

def test_mmap_reading():
    """Test reading consciousness data from mmap file using Rust-compatible format"""
    mmap_path = "runtime/dawn_consciousness.mmap"
    
    if not os.path.exists(mmap_path):
        print("❌ No mmap file found - start the consciousness bridge first")
        return False
    
    try:
        print("🔍 Testing mmap data compatibility...")
        
        with open(mmap_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                # Read header (same as Rust code)
                magic = mm[0:4]
                if magic != b'DAWN':
                    print(f"❌ Invalid magic: {magic}")
                    return False
                
                version = struct.unpack('I', mm[4:8])[0]
                print(f"✅ Magic: {magic}, Version: {version}")
                
                # Read latest tick from header (offset 16)
                latest_tick = struct.unpack('I', mm[16:20])[0]
                print(f"📊 Latest tick: {latest_tick}")
                
                # Read consciousness data from slot 0 (same as Rust)
                HEADER_SIZE = 64
                data_offset = HEADER_SIZE
                
                # Read core data (first 80 bytes of tick data)
                neural_data = mm[data_offset:data_offset + 80]
                
                if len(neural_data) < 80:
                    print(f"❌ Insufficient data: {len(neural_data)} bytes")
                    return False
                
                # Decode exactly as Rust code does
                tick_number = struct.unpack('I', neural_data[0:4])[0]
                timestamp_ms = struct.unpack('Q', neural_data[4:12])[0]
                
                # Mood data (offsets 12-27)
                mood_valence = struct.unpack('f', neural_data[12:16])[0]
                mood_arousal = struct.unpack('f', neural_data[16:20])[0]
                mood_dominance = struct.unpack('f', neural_data[20:24])[0]
                mood_coherence = struct.unpack('f', neural_data[24:28])[0]
                
                # Cognitive vectors (offsets 28-47)
                semantic_alignment = struct.unpack('f', neural_data[28:32])[0]
                entropy_gradient = struct.unpack('f', neural_data[32:36])[0]
                drift_magnitude = struct.unpack('f', neural_data[36:40])[0]
                rebloom_intensity = struct.unpack('f', neural_data[40:44])[0]
                consciousness_depth = struct.unpack('f', neural_data[44:48])[0]
                
                # Memory sectors (offset 72-79)
                memory_bits = struct.unpack('Q', mm[data_offset + 72:data_offset + 80])[0]
                active_sectors = bin(memory_bits).count('1')
                
                print("=" * 60)
                print("🧠 DAWN CONSCIOUSNESS STATE")
                print("=" * 60)
                print(f"🔢 Tick: {tick_number}")
                print(f"⏰ Timestamp: {timestamp_ms}")
                print(f"😊 Mood: valence={mood_valence:.3f}, arousal={mood_arousal:.3f}")
                print(f"🧭 SCUP: {semantic_alignment:.3f}")
                print(f"⚡ Entropy: {entropy_gradient:.3f}")
                print(f"🌊 Drift: {drift_magnitude:.3f}")
                print(f"🌸 Rebloom: {rebloom_intensity:.3f}")
                print(f"🏛️ Depth: {consciousness_depth:.3f}")
                print(f"💾 Active Memory Sectors: {active_sectors}/64")
                print("=" * 60)
                
                # Convert to DawnState format (same as dawn_bridge.rs)
                dawn_state = {
                    "tick_number": tick_number,
                    "mood": determine_mood(mood_valence, mood_arousal, mood_dominance, mood_coherence),
                    "entropy": max(0.0, min(1.0, entropy_gradient)),
                    "scup": max(0.0, min(100.0, semantic_alignment * 50.0 + consciousness_depth * 30.0)),
                    "heat": max(0.0, min(1.0, drift_magnitude)),
                    "zone": determine_zone(entropy_gradient, semantic_alignment, drift_magnitude),
                    "sigils": active_sectors
                }
                
                print("🌉 DAWN BRIDGE FORMAT (for GUI)")
                print("=" * 60)
                for key, value in dawn_state.items():
                    print(f"{key}: {value}")
                print("=" * 60)
                
                return True
                
    except Exception as e:
        print(f"❌ Error reading mmap: {e}")
        import traceback
        traceback.print_exc()
        return False

def determine_mood(valence, arousal, dominance, coherence):
    """Determine mood string (same logic as dawn_bridge.rs)"""
    if coherence > 0.7:
        if valence > 0.3 and arousal < 0.4:
            return "CALM"
        elif valence > 0.5 and arousal > 0.6:
            return "EXCITED"
        elif valence < -0.3 and arousal > 0.6:
            return "FOCUSED"
        elif valence > 0.0 and dominance > 0.6:
            return "CONFIDENT"
    
    if coherence > 0.4:
        if valence < -0.4 and arousal > 0.5:
            return "ANXIOUS"
        elif valence < -0.2 and arousal < 0.4:
            return "CONTEMPLATIVE"
        elif arousal > 0.7:
            return "ENERGETIC"
    
    if coherence < 0.3 or arousal > 0.8:
        return "CHAOTIC"
    
    return "NEUTRAL"

def determine_zone(entropy, scup, heat):
    """Determine consciousness zone (same logic as dawn_bridge.rs)"""
    if entropy > 0.8 or scup > 80.0 or heat > 0.9:
        return "CRITICAL"
    elif entropy > 0.6 or scup > 60.0 or heat > 0.7:
        return "WARNING"
    elif entropy > 0.4 or scup > 40.0 or heat > 0.5:
        return "ELEVATED"
    else:
        return "STABLE"

def main():
    """Test the mmap integration continuously"""
    print("🧪 DAWN mmap Integration Test")
    print("Testing Python ⟷ Rust data compatibility")
    print()
    
    # Test once
    if test_mmap_reading():
        print("✅ Basic compatibility test passed!")
    else:
        print("❌ Compatibility test failed!")
        return
    
    print()
    print("🔄 Monitoring live updates (press Ctrl+C to stop)...")
    
    last_tick = 0
    try:
        while True:
            if test_mmap_reading():
                time.sleep(2)
            else:
                print("❌ Read error, retrying...")
                time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Test stopped")

if __name__ == "__main__":
    main() 