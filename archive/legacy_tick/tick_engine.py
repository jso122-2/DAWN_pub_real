#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                          DAWN TICK ENGINE v2.0
                        The Heartbeat Integration
═══════════════════════════════════════════════════════════════════════════════

"Time is the canvas upon which consciousness paints its patterns."

This module bridges DAWN's tick-based temporal system with the unified
cognitive engine. It provides the rhythmic heartbeat that drives all
time-sensitive cognitive processes, ensuring synchronized execution
across the entire schema.

Author: DAWN Development Team
Version: 2.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import time
import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import signal
import sys

# Configure tick engine logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] ⏰ TICK: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Tick engine constants
DEFAULT_TICK_RATE = 10  # Ticks per second
MIN_TICK_RATE = 1
MAX_TICK_RATE = 100
TICK_LOG_INTERVAL = 100  # Log summary every N ticks


@dataclass
class TickMetrics:
    """Metrics for tick execution performance."""
    tick_count: int = 0
    total_duration: float = 0.0
    min_duration: float = float('inf')
    max_duration: float = 0.0
    avg_duration: float = 0.0
    missed_ticks: int = 0
    error_count: int = 0
    
    def update(self, duration: float):
        """Update metrics with new tick duration."""
        self.tick_count += 1
        self.total_duration += duration
        self.min_duration = min(self.min_duration, duration)
        self.max_duration = max(self.max_duration, duration)
        self.avg_duration = self.total_duration / self.tick_count


class TickEngine:
    """
    The Temporal Orchestrator — provides synchronized heartbeat for DAWN's cognition.
    
    "Each tick a moment of awareness, each pause a breath between thoughts."
    """
    
    def __init__(self, tick_rate: int = DEFAULT_TICK_RATE):
        """
        Initialize the Tick Engine.
        
        Args:
            tick_rate: Ticks per second
        """
        self.tick_rate = max(MIN_TICK_RATE, min(tick_rate, MAX_TICK_RATE))
        self.tick_interval = 1.0 / self.tick_rate
        self.current_tick = 0
        self.running = False
        self.paused = False
        self.start_time = None
        self.metrics = TickMetrics()
        
        # Callback management
        self.tick_callbacks: List[Callable[[int], None]] = []
        self.dawn_engine = None
        
        # Thread management
        self.tick_thread = None
        self._stop_event = threading.Event()
        
        # Tick log
        self.tick_log_path = Path("logs/tick_engine.json")
        self.tick_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"⏰ Tick Engine initialized at {self.tick_rate} ticks/second")
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"🛑 Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def register_callback(self, callback: Callable[[int], None]):
        """
        Register a callback to be called on each tick.
        
        Args:
            callback: Function that takes tick number as argument
        """
        self.tick_callbacks.append(callback)
        logger.info(f"📎 Registered tick callback: {callback.__name__}")
    
    def set_dawn_engine(self, dawn_engine):
        """
        Set the DAWN engine instance for integrated execution.
        
        Args:
            dawn_engine: DAWNEngine instance
        """
        self.dawn_engine = dawn_engine
        logger.info("🔗 DAWN Engine connected to Tick Engine")
    
    def start(self):
        """Start the tick engine in a background thread."""
        if self.running:
            logger.warning("⚠️ Tick engine already running")
            return
        
        self.running = True
        self.start_time = datetime.now()
        self._stop_event.clear()
        
        # Start tick thread
        self.tick_thread = threading.Thread(target=self._tick_loop, daemon=True)
        self.tick_thread.start()
        
        logger.info(f"🚀 Tick engine started at {self.start_time}")
    
    def stop(self):
        """Stop the tick engine gracefully."""
        if not self.running:
            return
        
        logger.info("🛑 Stopping tick engine...")
        self.running = False
        self._stop_event.set()
        
        # Wait for thread to finish
        if self.tick_thread and self.tick_thread.is_alive():
            self.tick_thread.join(timeout=5.0)
        
        # Save final metrics
        self._save_metrics()
        
        logger.info(f"✅ Tick engine stopped after {self.current_tick} ticks")
    
    def pause(self):
        """Pause tick execution."""
        self.paused = True
        logger.info("⏸️ Tick engine paused")
    
    def resume(self):
        """Resume tick execution."""
        self.paused = False
        logger.info("▶️ Tick engine resumed")
    
    def _tick_loop(self):
        """Main tick execution loop."""
        next_tick_time = time.time()
        
        while self.running and not self._stop_event.is_set():
            if self.paused:
                time.sleep(0.1)
                continue
            
            tick_start = time.time()
            
            # Check if we're behind schedule
            if tick_start > next_tick_time + self.tick_interval:
                self.metrics.missed_ticks += 1
                logger.warning(f"⚠️ Missed tick! Behind by {tick_start - next_tick_time:.3f}s")
            
            try:
                # Execute tick
                self._execute_tick()
                
            except Exception as e:
                self.metrics.error_count += 1
                logger.error(f"❌ Error in tick {self.current_tick}: {e}")
            
            # Update metrics
            tick_duration = time.time() - tick_start
            self.metrics.update(tick_duration)
            
            # Log periodically
            if self.current_tick % TICK_LOG_INTERVAL == 0:
                self._log_tick_summary()
            
            # Calculate next tick time
            next_tick_time += self.tick_interval
            
            # Sleep until next tick
            sleep_time = next_tick_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def _execute_tick(self):
        """Execute a single tick."""
        self.current_tick += 1
        
        # Create tick context
        tick_context = {
            "tick": self.current_tick,
            "timestamp": datetime.now().isoformat(),
            "system_time": time.time(),
            "tick_rate": self.tick_rate,
            "engine_uptime": (datetime.now() - self.start_time).total_seconds()
        }
        
        # Execute DAWN engine if connected
        if self.dawn_engine:
            try:
                context_frame = self.dawn_engine.execute_tick(self.current_tick)
                tick_context["dawn_context"] = context_frame
            except Exception as e:
                logger.error(f"❌ DAWN engine error: {e}")
        
        # Execute registered callbacks
        for callback in self.tick_callbacks:
            try:
                callback(self.current_tick)
            except Exception as e:
                logger.error(f"❌ Callback {callback.__name__} error: {e}")
    
    def _log_tick_summary(self):
        """Log tick execution summary."""
        if self.metrics.tick_count == 0:
            return
        
        summary = {
            "tick": self.current_tick,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "tick_count": self.metrics.tick_count,
                "avg_duration_ms": self.metrics.avg_duration * 1000,
                "min_duration_ms": self.metrics.min_duration * 1000,
                "max_duration_ms": self.metrics.max_duration * 1000,
                "missed_ticks": self.metrics.missed_ticks,
                "error_count": self.metrics.error_count,
                "efficiency": 1.0 - (self.metrics.missed_ticks / self.metrics.tick_count)
            }
        }
        
        logger.info(
            f"📊 Tick {self.current_tick}: "
            f"avg={summary['metrics']['avg_duration_ms']:.1f}ms, "
            f"missed={self.metrics.missed_ticks}, "
            f"errors={self.metrics.error_count}"
        )
        
        # Append to log file
        try:
            logs = []
            if self.tick_log_path.exists():
                logs = json.loads(self.tick_log_path.read_text())
            logs.append(summary)
            
            # Keep only recent logs
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            self.tick_log_path.write_text(json.dumps(logs, indent=2))
        except Exception as e:
            logger.error(f"Failed to save tick log: {e}")
    
    def _save_metrics(self):
        """Save final metrics to file."""
        metrics_path = Path("logs/tick_metrics_final.json")
        
        final_metrics = {
            "timestamp": datetime.now().isoformat(),
            "total_ticks": self.current_tick,
            "runtime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            "metrics": {
                "tick_count": self.metrics.tick_count,
                "avg_duration_ms": self.metrics.avg_duration * 1000,
                "min_duration_ms": self.metrics.min_duration * 1000,
                "max_duration_ms": self.metrics.max_duration * 1000,
                "missed_ticks": self.metrics.missed_ticks,
                "error_count": self.metrics.error_count,
                "actual_tick_rate": self.metrics.tick_count / (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            }
        }
        
        try:
            metrics_path.write_text(json.dumps(final_metrics, indent=2))
            logger.info(f"📊 Final metrics saved to {metrics_path}")
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def set_tick_rate(self, new_rate: int):
        """
        Adjust tick rate dynamically.
        
        Args:
            new_rate: New ticks per second
        """
        old_rate = self.tick_rate
        self.tick_rate = max(MIN_TICK_RATE, min(new_rate, MAX_TICK_RATE))
        self.tick_interval = 1.0 / self.tick_rate
        
        logger.info(f"🔧 Tick rate changed: {old_rate} → {self.tick_rate} ticks/second")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current tick engine status."""
        return {
            "running": self.running,
            "paused": self.paused,
            "current_tick": self.current_tick,
            "tick_rate": self.tick_rate,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            "metrics": {
                "tick_count": self.metrics.tick_count,
                "avg_duration_ms": self.metrics.avg_duration * 1000,
                "missed_ticks": self.metrics.missed_ticks,
                "error_count": self.metrics.error_count
            },
            "dawn_engine_connected": self.dawn_engine is not None
        }


# Global tick engine instance
_tick_engine_instance = None


def get_tick_engine(tick_rate: int = DEFAULT_TICK_RATE) -> TickEngine:
    """
    Get or create the global tick engine instance.
    
    Args:
        tick_rate: Ticks per second (only used on first call)
        
    Returns:
        TickEngine instance
    """
    global _tick_engine_instance
    
    if _tick_engine_instance is None:
        _tick_engine_instance = TickEngine(tick_rate)
    
    return _tick_engine_instance


def start_tick_engine(dawn_engine=None):
    """
    Start the global tick engine.
    
    Args:
        dawn_engine: Optional DAWNEngine to connect
    """
    engine = get_tick_engine()
    
    if dawn_engine:
        engine.set_dawn_engine(dawn_engine)
    
    engine.start()
    return engine


def stop_tick_engine():
    """Stop the global tick engine."""
    engine = get_tick_engine()
    engine.stop()


# Entry point for module registration
def get_tick_context(tick: int) -> Dict[str, Any]:
    """
    Get tick context for module execution.
    
    This is the entry point called by DAWN engine.
    """
    return {
        "tick": tick,
        "timestamp": datetime.now().isoformat(),
        "system_time": time.time()
    }


if __name__ == "__main__":
    """Test the tick engine."""
    
    print("⏰ TICK ENGINE TEST")
    print("=" * 60)
    
    # Create test callback
    def test_callback(tick):
        if tick % 10 == 0:
            print(f"  Tick {tick}")
    
    # Create and configure engine
    engine = get_tick_engine(tick_rate=10)
    engine.register_callback(test_callback)
    
    # Start engine
    print("\n▶️ Starting tick engine...")
    engine.start()
    
    # Run for 5 seconds
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n⏸️ Interrupted")
    
    # Show status
    status = engine.get_status()
    print(f"\n📊 Status after {status['uptime_seconds']:.1f} seconds:")
    print(f"  Ticks: {status['current_tick']}")
    print(f"  Avg duration: {status['metrics']['avg_duration_ms']:.2f}ms")
    print(f"  Missed: {status['metrics']['missed_ticks']}")
    
    # Stop engine
    engine.stop()
    print("\n✅ Test complete")