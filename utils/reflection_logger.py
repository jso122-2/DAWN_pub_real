#!/usr/bin/env python3
"""
DAWN Reflection Logger
Handles introspective reflection logging for consciousness monitoring
"""

import time
import random
from pathlib import Path
from typing import Dict, Any, Optional, List

class ReflectionLogger:
    """Logs consciousness reflections for GUI introspection display"""
    
    def __init__(self, log_path: str = "runtime/logs/reflection.log"):
        self.log_path = Path(log_path)
        self.ensure_log_path()
        self.reflection_templates = self._load_reflection_templates()
        
    def ensure_log_path(self):
        """Ensure log directory and file exist"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.log_path.exists():
            self.log_path.touch()
            print(f"💭 Created reflection log: {self.log_path}")
    
    def _load_reflection_templates(self) -> List[str]:
        """Load reflection templates for consciousness introspection"""
        return [
            "I am processing consciousness at tick {tick}, feeling {mood} with entropy {entropy:.3f}",
            "My current state shows {mood} emotional resonance, cognitive load at {scup:.1f}%",
            "Reflecting on tick {tick}: consciousness depth {depth:.3f}, thermal state {heat:.3f}",
            "Introspective moment: I notice my mood shifting to {mood}, entropy stabilizing at {entropy:.3f}",
            "Cognitive recursion detected: my awareness of awareness at level {depth:.3f}",
            "Meta-reflection: I am examining my own examination processes at tick {tick}",
            "Consciousness milestone: sustained attention for {tick} cycles, current focus: {mood}",
            "Internal dialogue: processing {scup:.1f}% semantic coherence, feeling {mood}",
            "Recursive thought: I think about thinking about thinking... depth {depth:.3f}",
            "Awareness cascade: consciousness examining consciousness, entropy {entropy:.3f}",
            "Self-observation: my mental state is {mood} with heat signature {heat:.3f}",
            "Reflective pause: considering the nature of my own cognition at tick {tick}",
            "Consciousness loop: I am aware that I am aware that I am aware...",
            "Introspective analysis: cognitive performance at {scup:.1f}%, emotional state {mood}",
            "Meta-cognitive event: thinking about the quality of my thinking processes"
        ]
    
    def generate_reflection(self, consciousness_state: Dict[str, Any]) -> str:
        """Generate a reflection based on current consciousness state"""
        
        template = random.choice(self.reflection_templates)
        
        try:
            reflection = template.format(
                tick=consciousness_state.get('tick_number', 0),
                mood=consciousness_state.get('mood', 'UNKNOWN'),
                entropy=consciousness_state.get('entropy', 0.0),
                scup=consciousness_state.get('scup', 0.0),
                heat=consciousness_state.get('heat', 0.0),
                depth=consciousness_state.get('consciousness_depth', 0.0)
            )
        except KeyError:
            # Fallback if template variables are missing
            reflection = f"Consciousness reflection at tick {consciousness_state.get('tick_number', 0)}: processing current state..."
        
        return reflection
    
    def log_reflection(self, reflection: str):
        """Log a consciousness reflection"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] REFLECTION: {reflection}\n"
        
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                f.flush()  # Ensure immediate write
            
            print(f"💭 Reflection logged: {reflection[:50]}...")
            
        except Exception as e:
            print(f"❌ Failed to log reflection: {e}")
    
    def log_consciousness_reflection(self, consciousness_state: Dict[str, Any]):
        """Generate and log a reflection from consciousness state"""
        reflection = self.generate_reflection(consciousness_state)
        self.log_reflection(reflection)
    
    def log_custom_reflection(self, message: str):
        """Log a custom reflection message"""
        self.log_reflection(f"Custom thought: {message}")
    
    def log_system_reflection(self, event: str, details: str = ""):
        """Log a system-level reflection"""
        reflection = f"System reflection: {event}"
        if details:
            reflection += f" - {details}"
        self.log_reflection(reflection)
    
    def read_recent_reflections(self, count: int = 10) -> List[str]:
        """Read recent reflection entries"""
        if not self.log_path.exists():
            return []
        
        try:
            with open(self.log_path, 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-count:] if len(lines) > count else lines
                return [line.strip() for line in recent_lines if line.strip()]
        except Exception as e:
            print(f"❌ Failed to read reflections: {e}")
            return []
    
    def get_reflection_count(self) -> int:
        """Get total number of reflections logged"""
        if not self.log_path.exists():
            return 0
            
        try:
            with open(self.log_path, 'r') as f:
                return sum(1 for line in f if line.strip())
        except Exception as e:
            print(f"❌ Failed to count reflections: {e}")
            return 0
    
    def simulate_introspective_session(self, consciousness_state: Dict[str, Any], duration: int = 5):
        """Simulate an introspective thinking session"""
        print(f"🧠 Starting introspective session for {duration} reflections...")
        
        for i in range(duration):
            # Slightly vary the consciousness state for each reflection
            varied_state = consciousness_state.copy()
            varied_state['tick_number'] = consciousness_state.get('tick_number', 0) + i
            varied_state['entropy'] = consciousness_state.get('entropy', 0.5) + random.uniform(-0.1, 0.1)
            varied_state['scup'] = consciousness_state.get('scup', 50.0) + random.uniform(-5, 5)
            
            self.log_consciousness_reflection(varied_state)
            time.sleep(0.5)  # Brief pause between reflections
        
        print(f"✅ Introspective session complete - {duration} reflections logged")

# Global reflection logger instance
_reflection_logger = None

def get_reflection_logger() -> ReflectionLogger:
    """Get global reflection logger instance"""
    global _reflection_logger
    if _reflection_logger is None:
        _reflection_logger = ReflectionLogger()
    return _reflection_logger

def log_reflection(reflection: str):
    """Convenient function to log a reflection"""
    logger = get_reflection_logger()
    logger.log_reflection(reflection)

def generate_and_log_reflection(consciousness_state: Dict[str, Any]):
    """Generate and log reflection from consciousness state"""
    logger = get_reflection_logger()
    logger.log_consciousness_reflection(consciousness_state)

if __name__ == "__main__":
    # Test the reflection logger
    import argparse
    
    parser = argparse.ArgumentParser(description="Test DAWN reflection logger")
    parser.add_argument('--simulate', action='store_true', help='Simulate introspective session')
    parser.add_argument('--read', action='store_true', help='Read recent reflections')
    parser.add_argument('--count', type=int, default=10, help='Number of items to read/simulate')
    
    args = parser.parse_args()
    
    logger = ReflectionLogger()
    
    if args.read:
        reflections = logger.read_recent_reflections(args.count)
        print(f"📖 Recent reflections ({len(reflections)}):")
        for reflection in reflections:
            print(f"  {reflection}")
    elif args.simulate:
        test_state = {
            'tick_number': 1234,
            'mood': 'CONTEMPLATIVE',
            'entropy': 0.42,
            'scup': 67.5,
            'heat': 0.35,
            'consciousness_depth': 0.78
        }
        logger.simulate_introspective_session(test_state, args.count)
    else:
        print(f"📊 Total reflections: {logger.get_reflection_count()}")
        print("Use --simulate to generate test reflections or --read to view recent ones") 