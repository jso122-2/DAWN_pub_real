"""
Memory Interface - Unified interface for memory management and tracing
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
import time
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MemoryState:
    """Current state of the memory system"""
    owl_active: bool = False
    rebloom_count: int = 0
    bloom_entropy: float = 0.0
    last_trace: float = 0.0
    trace_count: int = 0
    memory_usage: float = 0.0
    active_traces: List[str] = None
    
    def __post_init__(self):
        if self.active_traces is None:
            self.active_traces = []

class MemoryInterface:
    """Unified interface for memory management and tracing"""
    
    def __init__(self):
        """Initialize memory interface"""
        self._state = MemoryState()
        self._owl_active = False
        self._memory_dir = Path("memories")
        self._memory_dir.mkdir(exist_ok=True)
        self._initialize()
        logger.info("Initialized MemoryInterface")
        
    def _initialize(self) -> None:
        """Initialize memory components"""
        try:
            # Initialize with non-zero values
            self._state.owl_active = True
            self._state.rebloom_count = 0
            self._state.bloom_entropy = 0.1
            self._state.memory_usage = 0.1
            
            # Load existing traces
            self._load_traces()
            
        except Exception as e:
            logger.error(f"Error initializing memory components: {e}")
            
    def _load_traces(self) -> None:
        """Load existing memory traces"""
        try:
            trace_file = self._memory_dir / "active_traces.json"
            if trace_file.exists():
                with open(trace_file) as f:
                    data = json.load(f)
                    self._state.active_traces = data.get("traces", [])
                    self._state.trace_count = data.get("count", 0)
        except Exception as e:
            logger.error(f"Error loading traces: {e}")
            
    def _save_traces(self) -> None:
        """Save current memory traces"""
        try:
            trace_file = self._memory_dir / "active_traces.json"
            data = {
                "traces": self._state.active_traces,
                "count": self._state.trace_count,
                "timestamp": time.time()
            }
            with open(trace_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving traces: {e}")
            
    def recall(self, query: str) -> Optional[Dict[str, Any]]:
        """Recall memory based on query"""
        try:
            # Search active traces
            for trace in self._state.active_traces:
                if query.lower() in trace.lower():
                    return {
                        "trace": trace,
                        "timestamp": self._state.last_trace,
                        "entropy": self._state.bloom_entropy
                    }
            return None
        except Exception as e:
            logger.error(f"Error recalling memory: {e}")
            return None
            
    def store_trace(self, data: Dict[str, Any]) -> bool:
        """Store a new memory trace"""
        try:
            # Generate trace ID
            trace_id = f"trace_{self._state.trace_count}"
            self._state.trace_count += 1
            
            # Store trace
            trace_file = self._memory_dir / f"{trace_id}.json"
            with open(trace_file, "w") as f:
                json.dump({
                    "id": trace_id,
                    "data": data,
                    "timestamp": time.time(),
                    "entropy": self._state.bloom_entropy
                }, f, indent=2)
                
            # Update state
            self._state.active_traces.append(trace_id)
            self._state.last_trace = time.time()
            
            # Save updated traces
            self._save_traces()
            return True
            
        except Exception as e:
            logger.error(f"Error storing trace: {e}")
            return False
            
    def run_tick(self) -> None:
        """Run a memory tick (passive scan/log)"""
        try:
            # Update memory usage
            self._state.memory_usage = len(self._state.active_traces) / 100.0
            
            # Update bloom entropy
            self._state.bloom_entropy = min(1.0, self._state.memory_usage * 0.8)
            
            # Log memory state
            logger.debug(f"Memory tick: {len(self._state.active_traces)} active traces, "
                        f"entropy: {self._state.bloom_entropy:.3f}")
            
        except Exception as e:
            logger.error(f"Error in memory tick: {e}")

# Global instance
_memory_interface = MemoryInterface()

def recall(query: str) -> Optional[Dict[str, Any]]:
    """Recall memory from global interface"""
    return _memory_interface.recall(query)
    
def store_trace(data: Dict[str, Any]) -> bool:
    """Store trace on global interface"""
    return _memory_interface.store_trace(data)
    
def run_tick() -> None:
    """Run memory tick on global interface"""
    _memory_interface.run_tick()

# Export key functions
__all__ = [
    'MemoryInterface',
    'MemoryState',
    'recall',
    'store_trace',
    'run_tick'
] 