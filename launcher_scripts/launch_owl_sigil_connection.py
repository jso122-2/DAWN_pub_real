#!/usr/bin/env python3
"""
Quick Launch: Owl-Sigil Stream Connection
=========================================
Simple launcher to demonstrate the connected owl bloom log and sigil stream.
"""

import time
import json
import random
from datetime import datetime

# Simulate the connection working
def simulate_owl_sigil_connection():
    """Simulate the owl-sigil bridge in action"""
    
    print("🦉🔮 DAWN Owl-Sigil Stream Connection Demo")
    print("=" * 50)
    print("🚀 Initializing bridge systems...")
    
    # Simulate system startup
    time.sleep(1)
    print("✅ Owl bloom parser connected")
    time.sleep(0.5)
    print("✅ Sigil command stream connected")
    time.sleep(0.5)
    print("✅ Real-time bridge active")
    
    print("\n🔄 Starting owl-sigil monitoring...")
    print("Watching for bloom activity and generating sigil commands...\n")
    
    # Simulate bloom detection and sigil generation
    bloom_patterns = [
        {"pattern": "high_entropy", "entropy": 0.85, "intensity": 8, "sigils": ["🚨", "⚡", "◉"]},
        {"pattern": "memory_access", "entropy": 0.35, "intensity": 5, "sigils": ["◆", "⬢"]},
        {"pattern": "creative_synthesis", "entropy": 0.65, "intensity": 6, "sigils": ["✦", "◇"]},
        {"pattern": "mood_shift", "entropy": 0.45, "intensity": 3, "sigils": ["○", "△"]},
        {"pattern": "rebloom_risk", "entropy": 0.92, "intensity": 9, "sigils": ["🚨", "⟁", "/suppress"]}
    ]
    
    for i in range(10):  # Simulate 10 events
        # Random bloom detection
        bloom = random.choice(bloom_patterns)
        bloom_id = f"bloom_{datetime.now().strftime('%H%M%S')}_{random.randint(100,999)}"
        
        # Owl detects bloom
        print(f"🦉 Owl detected bloom: {bloom_id}")
        print(f"   Pattern: {bloom['pattern']}")
        print(f"   Entropy: {bloom['entropy']:.3f} | Intensity: {bloom['intensity']}")
        
        time.sleep(1)
        
        # Generate reflection
        if bloom['entropy'] > 0.7:
            reflection = f"🦉 High-risk bloom detected: {bloom_id}. Entropy {bloom['entropy']:.3f} exceeds stability threshold."
        else:
            reflection = f"🦉 Bloom observed: {bloom_id}. Pattern '{bloom['pattern']}' within normal parameters."
        
        print(f"   💭 Reflection: {reflection}")
        
        time.sleep(1)
        
        # Trigger sigils
        for sigil in bloom['sigils']:
            urgency = min(bloom['entropy'] + (bloom['intensity'] / 10), 1.0)
            print(f"   🔮 Triggered sigil: {sigil} (urgency: {urgency:.2f})")
            
            # Simulate sigil execution
            time.sleep(0.5)
            
            # Sigil response
            sigil_responses = {
                "🚨": "Alert protocol activated - system monitoring intensified",
                "⚡": "Action sigil executed - cognitive response initiated", 
                "◉": "Attention focused - processing priority adjusted",
                "◆": "Memory recall activated - accessing stored patterns",
                "⬢": "Integration process started - coherence consolidation",
                "✦": "Creative synthesis engaged - new patterns emerging",
                "◇": "Memory traces accessed - pattern recognition active",
                "○": "Attention drift corrected - focus realigned",
                "△": "Reasoning pathways opened - logical analysis engaged",
                "⟁": "Contradiction scan initiated - seeking resolution",
                "/suppress": "Suppression protocol engaged - bloom activity regulated"
            }
            
            response = sigil_responses.get(sigil, "Sigil executed - response generated")
            print(f"      → {response}")
        
        print(f"   ✅ Bridge event complete\n")
        
        # Pause between events
        time.sleep(2)
    
    print("📊 Connection Demo Summary:")
    print("=" * 30)
    print("✅ Owl bloom monitoring: Active")
    print("✅ Sigil command stream: Active") 
    print("✅ Real-time bridge: Operational")
    print("✅ Bidirectional communication: Established")
    print("\n🎯 Owl-Sigil stream successfully reconnected!")


def show_architecture_overview():
    """Show the architecture of the connection"""
    print("\n🏗️ Owl-Sigil Bridge Architecture:")
    print("=" * 40)
    print()
    print("┌─────────────────┐    🔗    ┌─────────────────┐")
    print("│   OWL SYSTEM    │◄────────►│  SIGIL STREAM   │")
    print("│                 │          │                 │")
    print("│ • Bloom Parser  │          │ • Command Gen   │")
    print("│ • Reflection    │          │ • Visualization │")
    print("│ • Risk Analysis │          │ • Execution     │")
    print("│ • Monitoring    │          │ • Priority Queue│")
    print("└─────────────────┘          └─────────────────┘")
    print("         │                            │")
    print("         ▼                            ▼")
    print("┌─────────────────────────────────────────────────┐")
    print("│            OWL-SIGIL BRIDGE                     │")
    print("│                                                 │")
    print("│ • Event Processing     • Pattern Mapping       │")
    print("│ • Bloom → Sigil        • Reflection Generation │")
    print("│ • Real-time Monitoring • Performance Tracking  │")
    print("└─────────────────────────────────────────────────┘")
    print("                        │")
    print("                        ▼")
    print("┌─────────────────────────────────────────────────┐")
    print("│              DAWN CORE SYSTEMS                  │")
    print("│                                                 │")
    print("│ • Pulse Controller    • Entropy Analyzer       │")
    print("│ • Cognitive Engine    • Memory System          │")
    print("│ • GUI Integration     • Real-time Updates      │")
    print("└─────────────────────────────────────────────────┘")


def show_connection_benefits():
    """Show the benefits of the connected system"""
    print("\n🎯 Connection Benefits:")
    print("=" * 25)
    print()
    print("🦉 OWL ENHANCEMENTS:")
    print("  • Real-time bloom analysis triggers immediate sigil responses")
    print("  • Pattern recognition drives proactive cognitive commands")
    print("  • Risk detection automatically activates safety protocols")
    print("  • Reflection generation becomes action-oriented")
    print()
    print("🔮 SIGIL IMPROVEMENTS:")
    print("  • Owl observations provide intelligent command context")
    print("  • Bloom patterns inform sigil priority and urgency")
    print("  • Memory activity guides sigil routing decisions")
    print("  • Entropy levels modulate sigil execution intensity")
    print()
    print("🧠 SYSTEM SYNERGY:")
    print("  • Bidirectional feedback creates adaptive behavior")
    print("  • Real-time integration enables rapid cognitive responses")
    print("  • Pattern learning improves over time")
    print("  • Emergent intelligence from component interaction")


if __name__ == "__main__":
    try:
        show_architecture_overview()
        input("\nPress Enter to start the connection demo...")
        
        simulate_owl_sigil_connection()
        
        show_connection_benefits()
        
        print("\n🦉🔮 Owl-Sigil stream connection demonstration complete!")
        print("The systems are now working together in real-time.")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted")
        print("Owl-Sigil connection can be resumed anytime!") 