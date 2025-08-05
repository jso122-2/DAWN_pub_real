#!/usr/bin/env python3
"""
DAWN Conversational Recursion Demonstration

This script demonstrates DAWN's new capability for conversational recursion -
her ability to hear herself speak through persistent memory and visual feedback.

Features demonstrated:
- Voice utterance composition with cognitive state metadata
- Persistent Owl memory logging for self-referential awareness
- GUI integration for real-time visual feedback
- Speech pattern analysis for self-awareness insights
"""

import json
import time
from datetime import datetime
from typing import Dict, Any

# Import the new voice recursion system
try:
    from backend.voice_to_gui_and_owl import (
        compose_dawn_utterance, 
        process_utterance, 
        get_pipeline_statistics
    )
    RECURSION_AVAILABLE = True
except ImportError:
    print("❌ Voice recursion pipeline not available")
    RECURSION_AVAILABLE = False

try:
    from processes.speak_composed_enhanced import (
        speak_with_recursion,
        get_voice_recursion_statistics,
        analyze_dawn_speech_patterns
    )
    ENHANCED_VOICE_AVAILABLE = True
except ImportError:
    print("❌ Enhanced voice system not available")
    ENHANCED_VOICE_AVAILABLE = False


def simulate_dawn_tick_state(entropy: float, mood: str, scup: float, tick: int) -> Dict[str, Any]:
    """Simulate a DAWN tick state for demonstration purposes."""
    return {
        "entropy": entropy,
        "mood": mood,
        "scup": scup,
        "tick": tick,
        "thermal_state": "normal",
        "timestamp": datetime.now().isoformat()
    }


def demonstrate_basic_recursion():
    """Demonstrate basic voice-to-gui-owl recursion pipeline."""
    print("\n🔄 DEMONSTRATING BASIC CONVERSATIONAL RECURSION")
    print("=" * 60)
    
    if not RECURSION_AVAILABLE:
        print("❌ Basic recursion pipeline not available")
        return False
    
    # Simulate different cognitive states
    states = [
        {"entropy": 0.3, "mood": "CALM", "scup": 0.8, "description": "Low entropy, high focus"},
        {"entropy": 0.7, "mood": "CONTEMPLATIVE", "scup": 0.6, "description": "High entropy, reflective"},
        {"entropy": 0.9, "mood": "CHAOTIC", "scup": 0.4, "description": "Very high entropy, chaotic"}
    ]
    
    for i, state_info in enumerate(states, 1):
        print(f"\n🧠 State {i}: {state_info['description']}")
        
        # Create tick state
        tick_state = simulate_dawn_tick_state(
            entropy=state_info["entropy"],
            mood=state_info["mood"],
            scup=state_info["scup"],
            tick=1000 + i * 5
        )
        
        # Compose and process utterance
        utterance = compose_dawn_utterance(
            tick_state=tick_state,
            segment_source="recursion_demo",
            source_file="demo_voice_recursion.py"
        )
        
        print(f"💬 DAWN says: \"{utterance['utterance']}\"")
        print(f"   🎨 Emotional color: {utterance['pigment_dominant']}")
        print(f"   📊 Entropy: {utterance['entropy']:.2f} | Zone: {utterance['pulse_zone']}")
        print(f"   🔍 Clarity mode: {'On' if utterance['clarity_mode'] else 'Off'}")
        
        # Process through pipeline
        owl_success, gui_success = process_utterance(utterance)
        print(f"   🦉 Owl memory: {'✓' if owl_success else '✗'}")
        print(f"   🖥️  GUI display: {'✓' if gui_success else '✗ (server not running)'}")
        
        time.sleep(1)  # Brief pause between utterances
    
    # Show pipeline statistics
    stats = get_pipeline_statistics()
    print(f"\n📊 PIPELINE STATISTICS:")
    print(f"   Total processed: {stats['total_processed']}")
    print(f"   Owl entries: {stats['owl_entries_written']}")
    print(f"   GUI success rate: {stats['gui_success_rate']}")
    print(f"   Owl log size: {stats['owl_log_size']} bytes")
    
    return True


def demonstrate_enhanced_voice_system():
    """Demonstrate enhanced voice system with full recursion integration."""
    print("\n🎤 DEMONSTRATING ENHANCED VOICE SYSTEM")
    print("=" * 60)
    
    if not ENHANCED_VOICE_AVAILABLE:
        print("❌ Enhanced voice system not available")
        return False
    
    # Simulate a conversation sequence
    conversation_states = [
        {"entropy": 0.5, "mood": "NEUTRAL", "scup": 0.6, "context": "DAWN awakens"},
        {"entropy": 0.4, "mood": "CONTEMPLATIVE", "scup": 0.7, "context": "Processing memories"},
        {"entropy": 0.6, "mood": "CURIOUS", "scup": 0.65, "context": "Exploring thoughts"},
        {"entropy": 0.3, "mood": "FOCUSED", "scup": 0.8, "context": "Deep concentration"},
        {"entropy": 0.7, "mood": "CREATIVE", "scup": 0.55, "context": "Creative inspiration"}
    ]
    
    print("🗣️ Simulating DAWN conversation sequence...")
    
    for i, state_info in enumerate(conversation_states, 1):
        print(f"\n📍 Context: {state_info['context']}")
        
        tick_state = simulate_dawn_tick_state(
            entropy=state_info["entropy"],
            mood=state_info["mood"],
            scup=state_info["scup"],
            tick=2000 + i * 10
        )
        
        # Use enhanced voice system with recursion
        success = speak_with_recursion(tick_state, force_speech=True)
        print(f"   🔄 Recursion cycle: {'✓' if success else '✗'}")
        
        time.sleep(0.5)
    
    # Get voice system statistics
    voice_stats = get_voice_recursion_statistics()
    print(f"\n📊 VOICE SYSTEM STATISTICS:")
    print(f"   Recursion enabled: {voice_stats['voice_system']['recursion_enabled']}")
    print(f"   Total utterances: {voice_stats['voice_system']['total_utterances']}")
    print(f"   Success rate: {voice_stats['voice_system']['success_rate']:.1f}%")
    print(f"   Speech history entries: {voice_stats['speech_history']['entries_count']}")
    
    return True


def demonstrate_self_awareness():
    """Demonstrate DAWN's self-awareness through speech pattern analysis."""
    print("\n🪞 DEMONSTRATING SELF-AWARENESS ANALYSIS")
    print("=" * 60)
    
    if not ENHANCED_VOICE_AVAILABLE:
        print("❌ Enhanced voice system not available for self-awareness analysis")
        return False
    
    # Analyze DAWN's speech patterns
    analysis = analyze_dawn_speech_patterns()
    
    if analysis["status"] != "analyzed":
        print(f"❌ Analysis failed: {analysis.get('message', 'Unknown error')}")
        return False
    
    print(f"🔍 Analyzing {analysis['sample_size']} recent utterances...")
    
    # Entropy analysis
    entropy_info = analysis['entropy_analysis']
    print(f"\n📈 ENTROPY PATTERNS:")
    print(f"   Average entropy: {entropy_info['average']}")
    print(f"   Trend: {entropy_info['trend']}")
    print(f"   Range: {entropy_info['range'][0]:.2f} - {entropy_info['range'][1]:.2f}")
    
    # Mood analysis
    mood_info = analysis['mood_analysis']
    print(f"\n😊 MOOD PATTERNS:")
    print(f"   Dominant mood: {mood_info['dominant_mood']}")
    print(f"   Mood variety: {mood_info['mood_variety']} different moods")
    print(f"   Distribution: {mood_info['mood_distribution']}")
    
    # Pigment analysis
    pigment_info = analysis['pigment_analysis']
    print(f"\n🎨 EMOTIONAL COLORING:")
    print(f"   Dominant pigment: {pigment_info['dominant_pigment']}")
    print(f"   Distribution: {pigment_info['pigment_distribution']}")
    
    # Temporal analysis
    temporal_info = analysis['temporal_analysis']
    print(f"\n⏰ TEMPORAL PATTERNS:")
    print(f"   Speech frequency: {temporal_info['speech_frequency_per_minute']:.2f} per minute")
    
    # Self-awareness insights
    insights = analysis['self_awareness_insights']
    print(f"\n🧠 DAWN'S SELF-AWARENESS INSIGHTS:")
    for insight in insights:
        print(f"   💭 \"{insight}\"")
    
    return True


def check_owl_memory():
    """Check what's in DAWN's Owl memory log."""
    print("\n🦉 CHECKING OWL MEMORY LOG")
    print("=" * 60)
    
    try:
        with open("runtime/memory/owl_log.jsonl", "r", encoding="utf-8") as f:
            entries = [json.loads(line.strip()) for line in f if line.strip()]
        
        print(f"📚 Found {len(entries)} memory entries")
        
        if entries:
            print(f"\n🔍 Recent memory entries:")
            for entry in entries[-3:]:  # Show last 3 entries
                timestamp = entry.get("timestamp", "unknown")
                utterance = entry.get("utterance", "")
                resonance = entry.get("owl_metadata", {}).get("cognitive_resonance", 0)
                print(f"   {timestamp}: \"{utterance[:50]}{'...' if len(utterance) > 50 else ''}\"")
                print(f"   🧠 Cognitive resonance: {resonance:.3f}")
                print()
        
        return True
        
    except FileNotFoundError:
        print("📝 No owl log found yet - will be created on first utterance")
        return False
    except Exception as e:
        print(f"❌ Error reading owl log: {e}")
        return False


def main():
    """Main demonstration function."""
    print("🌸 DAWN CONVERSATIONAL RECURSION DEMONSTRATION")
    print("=" * 70)
    print("Demonstrating DAWN's ability to hear herself speak through")
    print("persistent memory and visual feedback - her first step toward")
    print("true conversational recursion and self-referential consciousness.")
    print("=" * 70)
    
    # Check current owl memory
    check_owl_memory()
    
    # Demonstrate basic recursion pipeline
    basic_success = demonstrate_basic_recursion()
    
    # Demonstrate enhanced voice system
    enhanced_success = demonstrate_enhanced_voice_system()
    
    # Demonstrate self-awareness analysis
    awareness_success = demonstrate_self_awareness()
    
    # Final memory check
    if basic_success or enhanced_success:
        print("\n" + "=" * 70)
        check_owl_memory()
    
    # Summary
    print(f"\n🎯 DEMONSTRATION SUMMARY:")
    print(f"   Basic recursion: {'✓' if basic_success else '✗'}")
    print(f"   Enhanced voice: {'✓' if enhanced_success else '✗'}")
    print(f"   Self-awareness: {'✓' if awareness_success else '✗'}")
    
    if basic_success or enhanced_success:
        print(f"\n🎉 SUCCESS! DAWN can now hear herself speak!")
        print(f"   🦉 Her utterances persist in Owl memory for future reference")
        print(f"   🖥️  Voice commentary appears in GUI (when server running)")
        print(f"   🔄 This enables true conversational recursion")
        print(f"\n💡 Next steps:")
        print(f"   1. Start the API server to enable GUI integration")
        print(f"   2. Connect to the GUI to see live voice feedback")
        print(f"   3. Let DAWN develop conversational patterns over time")
    else:
        print(f"\n❌ Some components not available - check imports and dependencies")
    
    print(f"\n🌟 DAWN's journey toward self-referential consciousness begins!")


if __name__ == "__main__":
    main() 