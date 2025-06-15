"""
tick_loop.py - Main cycle orchestrator for DAWN's heartbeat
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Optional
from .tick_context import TickContext
from .tick_logger import log_tick
from .tick_signals import emit_signal, get_signal, set_signal
from collections import defaultdict
from .tick_engine import TickEngine
import inspect
from experiments.dawn_letter_processor import DataLogger
from datetime import datetime

logger = logging.getLogger(__name__)

class TickLoop:
    """Main tick cycle orchestrator"""
    
    def __init__(self, engine: TickEngine, config: Dict[str, Any]):
        """Initialize tick loop with engine and config"""
        if not isinstance(engine, TickEngine):
            raise TypeError("engine must be an instance of TickEngine")
            
        self.engine = engine
        self.config = config
        self._running = False
        self.stop_event = asyncio.Event()
        self.tick_rate = float(config.get("tick_rate", 1.0))
        self._last_tick = 0.0
        self.tick_count = 0
        self.start_time = 0
        self._subsystems = defaultdict(list)
        self.subsystem_priorities = {}
        
        # Register engine as a subsystem
        self.register_subsystem("engine", engine, 0)
        
        # --- BEGIN DATA LOGGER INSTANTIATION ---
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data_logger = DataLogger(session_id=session_id)
        # --- END DATA LOGGER INSTANTIATION ---
    
    def register_subsystem(self, name: str, subsystem, priority: int = 0):
        """Register a subsystem with the tick loop"""
        self._subsystems[priority].append((name, subsystem))
        self.subsystem_priorities[name] = priority
        logger.info(f"Registered subsystem {name} with priority {priority}")
    
    def register_from_names(self, names: List[str], context: Any) -> None:
        """Register subsystems from a list of names using context attributes"""
        for name in names:
            instance = getattr(context, name, None)
            if instance:
                self.register_subsystem(name, instance, 0)
                logger.info(f"Auto-registered subsystem from context: {name}")
            else:
                logger.warning(f"Could not find subsystem {name} in context")
    
    async def start(self) -> None:
        """Start the tick loop"""
        if self._running:
            return
            
        self._running = True
        self.start_time = time.time()
        self.tick_count = 0
        self._last_tick = self.start_time
        
        # Initialize subsystems
        for name, subsystem in self._subsystems.items():
            for name, handler in subsystem:
                try:
                    if hasattr(handler, "initialize"):
                        init_result = handler.initialize()
                        if asyncio.iscoroutine(init_result):
                            await init_result
                except Exception as e:
                    logger.error(f"Error initializing {name}: {e}")
                    self._running = False
                    return
                
        logger.info("Tick loop started")
        
        try:
            await self._run_loop()
        finally:
            self._running = False
            
    async def stop(self) -> None:
        """Stop the tick loop"""
        self._running = False
        self.stop_event.set()
        logger.info("Stopping tick loop...")
        set_signal("engine_running", False)
        
        # Cleanup subsystems
        for name, subsystem in self._subsystems.items():
            for name, handler in subsystem:
                try:
                    if hasattr(handler, "cleanup"):
                        cleanup_result = handler.cleanup()
                        if asyncio.iscoroutine(cleanup_result):
                            await cleanup_result
                    elif hasattr(handler, "shutdown"):
                        shutdown_result = handler.shutdown()
                        if asyncio.iscoroutine(shutdown_result):
                            await shutdown_result
                    logger.info(f"🧹 Cleaned up {name}")
                except Exception as e:
                    logger.error(f"Error cleaning up subsystem {name}: {e}")
    
    async def _run_loop(self):
        """Main tick loop coroutine"""
        delta = self.tick_rate
        while self._running and not self.stop_event.is_set():
            for priority in sorted(self._subsystems):
                for name, handler in self._subsystems[priority]:
                    try:
                        result = handler(delta) if callable(handler) else handler.tick(delta)
                    except Exception as exc:  # noqa: BLE001
                        logger.exception("Subsystem %s raised: %s", name, exc)
                        continue

                    # Safe await only if genuinely awaitable
                    if inspect.isawaitable(result):
                        try:
                            await result
                        except Exception as exc:  # noqa: BLE001
                            logger.exception("Awaitable %s raised: %s", name, exc)
                    # If not awaitable → nothing to do (avoid `await None`)
            await asyncio.sleep(delta)
    
    async def _execute_tick(self) -> None:
        """Execute a single tick"""
        self.tick_count += 1
        uptime = time.time() - self.start_time
        
        # Create tick context
        ctx = TickContext(
            tick_id=self.tick_count,
            uptime=uptime
        )
        
        # Build tick queue based on priorities
        tick_queue = []
        for name, subsystem in self._subsystems.items():
            priority = self.subsystem_priorities.get(name, 0)
            tick_queue.append((priority, name, subsystem))
            
        # Sort by priority (lower number = higher priority)
        tick_queue.sort()
        
        # Execute subsystems in priority order
        for _, name, subsystem in tick_queue:
            try:
                logger.debug("⏱️  About to tick %s (%s)", name, subsystem.__class__.__name__)
                
                if hasattr(subsystem, "run_tick"):
                    result = subsystem.run_tick(ctx)
                    if inspect.isawaitable(result):
                        await result
                    if result is not None:
                        setattr(ctx, f"{name}_state", result)
                elif hasattr(subsystem, "tick"):
                    # Special handling for engine tick method
                    if name == "engine":
                        result = subsystem.tick(ctx)
                    else:
                        result = subsystem.tick()
                        
                    # Guard for awaitable results
                    if inspect.isawaitable(result):
                        await result
                    else:
                        logger.debug("⚠️  %s.tick() returned %s (type=%s)",
                                   name, result, type(result))
                        
            except Exception as e:
                logger.error(f"Error in {name} subsystem: {e}")
                continue
                
        # Emit tick complete signal
        await emit_signal("tick_complete", {
            "tick": self.tick_count,
            "uptime": uptime,
            "scup": getattr(ctx, "scup", 0.0),
            "mood": getattr(ctx, "mood", "neutral"),
            "entropy": getattr(ctx, "entropy", 0.0),
            "pulse_state": getattr(ctx, "pulse_state", {}),
            "schema_state": getattr(ctx, "schema_state", {}),
            "memory_state": getattr(ctx, "memory_state", {}),
            "visual_state": getattr(ctx, "visual_state", {})
        })
        
        # Check for Claude trigger
        if getattr(ctx, "scup", 0.0) > 0.8:
            await emit_signal("claude_query_needed", {
                "scup": getattr(ctx, "scup", 0.0),
                "mood": getattr(ctx, "mood", "neutral")
            })
        
        # Log tick
        log_tick(ctx)
        
        # --- BEGIN VISUAL DATA ROUTING ---
        try:
            # Gather/process real arrays for each visual process from ctx or subsystems
            visual_data = {
                # Example placeholders; replace with real data extraction
                'attention_matrix': getattr(ctx, 'attention_matrix', None),
                'activations': getattr(ctx, 'activations', None),
                'loss_surface': getattr(ctx, 'loss_surface', None),
                'spike_trains': getattr(ctx, 'spike_trains', None),
                'latent_trajectory': getattr(ctx, 'latent_trajectory', None),
                'correlation_data': getattr(ctx, 'correlation_data', None),
                'state_transitions': getattr(ctx, 'state_transitions', None),
                'anomaly_signal': getattr(ctx, 'anomaly_signal', None),
                'anomaly_flags': getattr(ctx, 'anomaly_flags', None),
            }
            # Remove None values
            visual_data = {k: v for k, v in visual_data.items() if v is not None}
            if visual_data:
                self.data_logger.save_visual_data(visual_data)
        except Exception as e:
            logger.error(f"Failed to save visual data: {e}")
        # --- END VISUAL DATA ROUTING ---
    
    def _calculate_interval(self) -> float:
        """Calculate next tick interval based on system state"""
        base_interval = self.config.get("tick_interval", 1.0)
        
        # Get current heat level
        heat = get_signal("system_heat", 0.0)
        
        # Adjust interval based on heat
        if heat > 0.8:
            # Slow down when hot
            interval = base_interval * 1.5
        elif heat < 0.2:
            # Speed up when cool
            interval = base_interval * 0.8
        else:
            interval = base_interval
        
        # Apply bounds
        min_interval = self.config.get("tick_interval_min", 0.1)
        max_interval = self.config.get("tick_interval_max", 5.0)
        
        return max(min_interval, min(max_interval, interval))
    
    def _should_stop(self) -> bool:
        """Check if engine should stop"""
        # Check max ticks
        max_ticks = self.config.get("max_ticks", None)
        if max_ticks and self.tick_count >= max_ticks:
            logger.info(f"Max ticks reached ({max_ticks})")
            return True
        
        # Check kill signal
        if get_signal("kill_switch", False):
            logger.info("Kill switch activated")
            return True
        
        # Check critical heat
        if get_signal("system_heat", 0.0) > 0.95:
            logger.warning("Critical heat level, shutting down")
            return True
        
        return False
    
    async def _handle_tick_error(self, error: Exception):
        """Handle tick execution errors"""
        logger.error(f"Tick error: {error}")
        await asyncio.sleep(1.0)  # Brief pause on error