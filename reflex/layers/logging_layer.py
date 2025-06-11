import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from .base import LoggingLayer, ReflexState

class RebloomLogger(LoggingLayer):
    """Stores reflex outcomes for long-term pattern analysis"""
    
    def __init__(self, log_dir: str = "logs/rebloom"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "rebloom_history.jsonl"
    
    def _format_log_entry(self, state: ReflexState) -> Dict[str, Any]:
        """Format state into log entry"""
        decision = state.metadata.get("decision")
        if not decision:
            return {}
        
        return {
            "task_id": state.metadata.get("task_id", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "should_rebloom": decision.should_rebloom,
            "mode": decision.mode.value,
            "drift_score": decision.drift_score,
            "faltering": decision.faltering,
            "flags": decision.flags,
            "mood": state.mood,
            "heat": state.heat,
            "entropy": state.entropy,
            "sigil": state.sigil,
            "metadata": {
                k: v for k, v in state.metadata.items()
                if k not in ["decision", "task_id"]
            }
        }
    
    def process(self, state: ReflexState) -> ReflexState:
        """Process state and log outcome"""
        log_entry = self._format_log_entry(state)
        if not log_entry:
            return state
        
        # Append to log file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Update state with logging info
        state.metadata["logged"] = True
        state.metadata["log_entry"] = log_entry
        
        return state
    
    def validate(self, state: ReflexState) -> bool:
        """Validate logging results"""
        return state.metadata.get("logged", False) and "log_entry" in state.metadata 