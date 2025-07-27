#!/usr/bin/env python3
"""
DAWN Rebloom Logger
Handles memory rebloom event logging for GUI visualization
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class RebloomEvent:
    """Represents a memory rebloom event"""
    source_id: str
    rebloom_id: str
    method: str
    topic: str
    reason: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

class RebloomLogger:
    """Logs memory rebloom events for GUI consumption"""
    
    def __init__(self, log_path: str = "runtime/memory/rebloom_log.jsonl"):
        self.log_path = Path(log_path)
        self.ensure_log_path()
        self.event_counter = 0
        
    def ensure_log_path(self):
        """Ensure log directory exists"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file if it doesn't exist
        if not self.log_path.exists():
            self.log_path.touch()
            print(f"🌸 Created rebloom log: {self.log_path}")
    
    def log_rebloom_event(
        self, 
        source_chunk: str, 
        rebloomed_chunk: str, 
        method: str = "semantic_resonance",
        topic: str = "unknown",
        reason: str = "Memory association triggered",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a memory rebloom event"""
        
        self.event_counter += 1
        
        event = RebloomEvent(
            source_id=source_chunk,
            rebloom_id=rebloomed_chunk, 
            method=method,
            topic=topic,
            reason=reason,
            metadata=metadata or {},
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S")
        )
        
        self._write_event(event)
        print(f"🌸 Rebloom event logged: {source_chunk} → {rebloomed_chunk}")
        
    def log_simulated_rebloom(self, tick_number: int):
        """Log a simulated rebloom event for testing"""
        
        # Create varied rebloom scenarios
        scenarios = [
            {
                "source": f"memory_chunk_{tick_number-5}",
                "target": f"rebloom_{tick_number}",
                "method": "semantic_resonance",
                "topic": "consciousness_reflection",
                "reason": "Recursive thought pattern detected"
            },
            {
                "source": f"journal_entry_{tick_number//10}",
                "target": f"meta_rebloom_{tick_number}",
                "method": "emotional_resonance", 
                "topic": "mood_association",
                "reason": "Emotional state triggered memory"
            },
            {
                "source": f"system_state_{tick_number-3}",
                "target": f"pattern_rebloom_{tick_number}",
                "method": "pattern_matching",
                "topic": "behavioral_analysis",
                "reason": "Behavioral pattern similarity"
            }
        ]
        
        scenario = scenarios[tick_number % len(scenarios)]
        
        self.log_rebloom_event(
            source_chunk=scenario["source"],
            rebloomed_chunk=scenario["target"],
            method=scenario["method"],
            topic=scenario["topic"],
            reason=scenario["reason"],
            metadata={
                "tick_number": tick_number,
                "simulated": True,
                "confidence": 0.7 + (tick_number % 3) * 0.1,
                "depth": (tick_number % 4) + 1
            }
        )
    
    def _write_event(self, event: RebloomEvent):
        """Write event to log file"""
        event_dict = {
            "timestamp": event.timestamp,
            "source_id": event.source_id,
            "rebloom_id": event.rebloom_id,
            "method": event.method,
            "topic": event.topic,
            "reason": event.reason,
            "metadata": event.metadata
        }
        
        try:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
                f.flush()  # Ensure immediate write
        except Exception as e:
            print(f"❌ Failed to write rebloom event: {e}")
    
    def read_recent_events(self, count: int = 10) -> list:
        """Read recent rebloom events"""
        if not self.log_path.exists():
            return []
        
        try:
            with open(self.log_path, 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-count:] if len(lines) > count else lines
                
                events = []
                for line in recent_lines:
                    try:
                        event = json.loads(line.strip())
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
                        
                return events
        except Exception as e:
            print(f"❌ Failed to read rebloom events: {e}")
            return []
    
    def get_event_count(self) -> int:
        """Get total number of logged events"""
        if not self.log_path.exists():
            return 0
            
        try:
            with open(self.log_path, 'r') as f:
                return sum(1 for line in f if line.strip())
        except Exception as e:
            print(f"❌ Failed to count events: {e}")
            return 0

# Global rebloom logger instance
_rebloom_logger = None

def get_rebloom_logger() -> RebloomLogger:
    """Get global rebloom logger instance"""
    global _rebloom_logger
    if _rebloom_logger is None:
        _rebloom_logger = RebloomLogger()
    return _rebloom_logger

def log_rebloom_event(source_chunk: str, rebloomed_chunk: str, **kwargs):
    """Convenient function to log rebloom event"""
    logger = get_rebloom_logger()
    logger.log_rebloom_event(source_chunk, rebloomed_chunk, **kwargs)

if __name__ == "__main__":
    # Test the rebloom logger
    import argparse
    
    parser = argparse.ArgumentParser(description="Test DAWN rebloom logger")
    parser.add_argument('--simulate', type=int, default=5, help='Number of simulated events')
    parser.add_argument('--read', action='store_true', help='Read recent events')
    
    args = parser.parse_args()
    
    logger = RebloomLogger()
    
    if args.read:
        events = logger.read_recent_events()
        print(f"📖 Recent rebloom events ({len(events)}):")
        for event in events:
            print(f"  🌸 {event['source_id']} → {event['rebloom_id']} ({event['method']})")
    else:
        print(f"🧪 Simulating {args.simulate} rebloom events...")
        for i in range(args.simulate):
            logger.log_simulated_rebloom(i + 1)
        
        print(f"✅ Total events logged: {logger.get_event_count()}") 