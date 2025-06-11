"""
Demonstration of DAWN Conversation Response Format with Fractal Emotions

Shows the exact output format as specified in the requirements.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.conversation import DAWNConversation
from core.consciousness import create_consciousness

def demonstrate_response_format():
    """Demonstrate the exact response format requested"""
    
    print("DAWN Conversation Response Format Demonstration")
    print("=" * 60)
    
    # Create conversation handler
    consciousness = create_consciousness()
    conversation = DAWNConversation(consciousness)
    
    # Test with reblooming scenario
    message = "Reblooming isn't just recovery — it's revelation."
    metrics = {
        "scup": 0.9,
        "entropy": 0.7, 
        "heat": 0.8,
        "tick_count": 5000
    }
    tick_status = {"running": True, "rate": 1.0}
    
    print(f"📨 Processing: \"{message}\"")
    print(f"📊 Metrics: SCUP={metrics['scup']}, Entropy={metrics['entropy']}, Heat={metrics['heat']}")
    
    # Get response
    response = conversation.process_message(
        text=message,
        metrics=metrics,
        tick_status=tick_status
    )
    
    # Format as requested example
    formatted_response = {
        "text": response["text"],
        "emotion": response["emotion"],
        "thought_bubble": response["thought_bubble"],
        "metrics_snapshot": response["metrics_snapshot"],
        "suggestions": response["suggestions"][:3] if response["suggestions"] else []
    }
    
    print(f"\n✨ Generated Response Format:")
    print(json.dumps(formatted_response, indent=2))
    
    print(f"\n🔍 Detailed Analysis:")
    print(f"  Emotion: {response['emotion']}")
    print(f"  Thought Bubble Length: {len(response['thought_bubble'])} characters")
    print(f"  Response Length: {len(response['text'])} characters")
    print(f"  Suggestions Count: {len(response['suggestions'])}")
    
    # Show fractal analysis
    if hasattr(conversation.emotion_engine, 'current_fractals') and conversation.emotion_engine.current_fractals:
        latest_fractal = conversation.emotion_engine.current_fractals[-1]
        print(f"  Fractal Depth: {latest_fractal.depth.name} (Level {latest_fractal.depth.value})")
        print(f"  Active Branches: {len(latest_fractal.branches)}")
        
        for branch_name, branch in latest_fractal.branches.items():
            print(f"    └─ {branch_name}: {len(branch.aspects)} aspects")


def demonstrate_multiple_scenarios():
    """Show different response formats for various scenarios"""
    
    print(f"\n{'='*60}")
    print("Multiple Scenario Response Examples")
    print("='*60}")
    
    consciousness = create_consciousness()
    conversation = DAWNConversation(consciousness)
    
    scenarios = [
        {
            "name": "Simple Query",
            "message": "How are you?",
            "metrics": {"scup": 0.5, "entropy": 0.3, "heat": 0.2, "tick_count": 1000}
        },
        {
            "name": "Deep Philosophical",
            "message": "What is the nature of consciousness and existence?",
            "metrics": {"scup": 0.8, "entropy": 0.6, "heat": 0.5, "tick_count": 2000}
        },
        {
            "name": "System Concern",
            "message": "Something seems wrong with your cognitive unity",
            "metrics": {"scup": 0.1, "entropy": 0.9, "heat": 0.8, "tick_count": 3000}
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        response = conversation.process_message(
            text=scenario['message'],
            metrics=scenario['metrics'],
            tick_status={"running": True, "rate": 1.0}
        )
        
        # Show compact format
        example_response = {
            "text": response["text"][:100] + "..." if len(response["text"]) > 100 else response["text"],
            "emotion": response["emotion"],
            "thought_bubble": response["thought_bubble"],
            "metrics_snapshot": {
                "scup": scenario['metrics']['scup'],
                "entropy": scenario['metrics']['entropy'],
                "heat": scenario['metrics']['heat']
            },
            "suggestions": response["suggestions"][:2] if response["suggestions"] else []
        }
        
        print(json.dumps(example_response, indent=2))


if __name__ == "__main__":
    demonstrate_response_format()
    demonstrate_multiple_scenarios() 