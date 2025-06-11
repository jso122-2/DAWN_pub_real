"""
Tick context for DAWN engine
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime

@dataclass
class TickContext:
    """Context object passed to subsystems during ticks"""
    
    tick_id: int
    uptime: float
    scup: float = 0.0
    mood: str = "neutral"
    entropy: float = 0.0
    errors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary"""
        return {
            "tick_id": self.tick_id,
            "uptime": self.uptime,
            "scup": self.scup,
            "mood": self.mood,
            "entropy": self.entropy,
            "errors": self.errors,
            "timestamp": self.timestamp.isoformat()
        }