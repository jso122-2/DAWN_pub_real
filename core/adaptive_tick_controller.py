#!/usr/bin/env python3
"""
DAWN Adaptive Tick Controller
Self-regulating tick speed control that merges with existing DAWN tick engines.
"""

import time
import asyncio
import logging
import math
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class TickMetrics:
    """Performance metrics for tick adaptation."""
    duration: float
    entropy: float
    heat: float
    cognitive_load: float
    system_pressure: float
    timestamp: datetime


class AdaptiveTickController:
    """
    Self-regulating tick controller that adapts speed based on system state.
    Can merge with existing DAWN tick engines.
    """
    
    def __init__(self, 
                 base_interval: float = 2.0,
                 min_interval: float = 0.1,
                 max_interval: float = 10.0,
                 adaptation_sensitivity: float = 0.5):
        """
        Initialize adaptive tick controller.
        
        Args:
            base_interval: Default tick interval in seconds
            min_interval: Minimum allowed interval (fastest)
            max_interval: Maximum allowed interval (slowest)
            adaptation_sensitivity: How quickly to adapt (0.0-1.0)
        """
        self.base_interval = base_interval
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.adaptation_sensitivity = adaptation_sensitivity
        
        # Current state
        self.current_interval = base_interval
        self.target_interval = base_interval
        self.last_adaptation_time = time.time()
        
        # Performance tracking
        self.recent_metrics = deque(maxlen=20)
        self.adaptation_history = deque(maxlen=100)
        
        # Adaptation rules
        self.adaptation_rules = {
            'entropy_threshold': 0.8,      # High entropy → slow down
            'heat_threshold': 70.0,        # High heat → slow down
            'load_threshold': 0.7,         # High load → slow down
            'pressure_threshold': 0.9,     # High pressure → slow down
            'performance_threshold': 0.5   # Slow performance → slow down
        }
        
        # Speed modifiers
        self.speed_modifiers = {
            'entropy_factor': 2.0,         # Entropy impact on speed
            'heat_factor': 1.5,            # Heat impact on speed
            'load_factor': 1.8,            # Load impact on speed
            'pressure_factor': 2.5,        # Pressure impact on speed
            'smoothing_factor': 0.3        # Smoothing for transitions
        }
        
        logger.info(f"🎛️ Adaptive Tick Controller initialized")
        logger.info(f"   Base interval: {base_interval}s")
        logger.info(f"   Range: {min_interval}s - {max_interval}s")
        logger.info(f"   Sensitivity: {adaptation_sensitivity}")
    
    def calculate_adaptive_interval(self, 
                                  entropy: float = 0.5,
                                  heat: float = 25.0,
                                  cognitive_load: float = 0.5,
                                  system_pressure: float = 0.5,
                                  tick_duration: float = 0.1) -> float:
        """
        Calculate adaptive tick interval based on system state.
        
        Args:
            entropy: Current entropy level (0.0-1.0)
            heat: Current heat level (0.0-100.0)
            cognitive_load: Current cognitive load (0.0-1.0)
            system_pressure: Current system pressure (0.0-1.0)
            tick_duration: Last tick duration in seconds
            
        Returns:
            float: Recommended tick interval in seconds
        """
        # Record metrics
        metrics = TickMetrics(
            duration=tick_duration,
            entropy=entropy,
            heat=heat,
            cognitive_load=cognitive_load,
            system_pressure=system_pressure,
            timestamp=datetime.now()
        )
        self.recent_metrics.append(metrics)
        
        # Calculate base speed factor (1.0 = normal speed)
        speed_factor = 1.0
        
        # Entropy adaptation - high entropy slows down for stability
        if entropy > self.adaptation_rules['entropy_threshold']:
            entropy_impact = (entropy - self.adaptation_rules['entropy_threshold']) * self.speed_modifiers['entropy_factor']
            speed_factor *= (1.0 + entropy_impact)
        
        # Heat adaptation - high heat slows down for cooling
        heat_normalized = heat / 100.0
        if heat > self.adaptation_rules['heat_threshold']:
            heat_impact = (heat_normalized - 0.7) * self.speed_modifiers['heat_factor']
            speed_factor *= (1.0 + heat_impact)
        
        # Cognitive load adaptation - high load slows down
        if cognitive_load > self.adaptation_rules['load_threshold']:
            load_impact = (cognitive_load - self.adaptation_rules['load_threshold']) * self.speed_modifiers['load_factor']
            speed_factor *= (1.0 + load_impact)
        
        # System pressure adaptation - high pressure slows down
        if system_pressure > self.adaptation_rules['pressure_threshold']:
            pressure_impact = (system_pressure - self.adaptation_rules['pressure_threshold']) * self.speed_modifiers['pressure_factor']
            speed_factor *= (1.0 + pressure_impact)
        
        # Performance adaptation - slow ticks suggest system strain
        performance_ratio = tick_duration / self.current_interval
        if performance_ratio > self.adaptation_rules['performance_threshold']:
            performance_impact = (performance_ratio - self.adaptation_rules['performance_threshold']) * 1.2
            speed_factor *= (1.0 + performance_impact)
        
        # Calculate target interval
        raw_interval = self.base_interval * speed_factor
        
        # Apply sensitivity scaling
        interval_delta = (raw_interval - self.current_interval) * self.adaptation_sensitivity
        target_interval = self.current_interval + interval_delta
        
        # Smooth transitions
        smoothing = self.speed_modifiers['smoothing_factor']
        self.target_interval = (target_interval * smoothing) + (self.target_interval * (1 - smoothing))
        
        # Clamp to bounds
        self.target_interval = max(self.min_interval, min(self.max_interval, self.target_interval))
        
        # Store adaptation record
        adaptation_record = {
            'timestamp': datetime.now(),
            'input_metrics': {
                'entropy': entropy,
                'heat': heat,
                'cognitive_load': cognitive_load,
                'system_pressure': system_pressure,
                'tick_duration': tick_duration
            },
            'speed_factor': speed_factor,
            'old_interval': self.current_interval,
            'new_interval': self.target_interval,
            'change_reason': self._get_adaptation_reason(entropy, heat, cognitive_load, system_pressure, performance_ratio)
        }
        self.adaptation_history.append(adaptation_record)
        
        # Update current interval
        self.current_interval = self.target_interval
        self.last_adaptation_time = time.time()
        
        logger.debug(f"🎛️ Adaptive interval: {self.current_interval:.3f}s (factor: {speed_factor:.2f})")
        
        return self.current_interval
    
    def _get_adaptation_reason(self, entropy: float, heat: float, 
                             cognitive_load: float, system_pressure: float, 
                             performance_ratio: float) -> str:
        """Determine the primary reason for adaptation."""
        reasons = []
        
        if entropy > self.adaptation_rules['entropy_threshold']:
            reasons.append(f"high_entropy({entropy:.2f})")
        
        if heat > self.adaptation_rules['heat_threshold']:
            reasons.append(f"high_heat({heat:.1f})")
        
        if cognitive_load > self.adaptation_rules['load_threshold']:
            reasons.append(f"high_load({cognitive_load:.2f})")
        
        if system_pressure > self.adaptation_rules['pressure_threshold']:
            reasons.append(f"high_pressure({system_pressure:.2f})")
        
        if performance_ratio > self.adaptation_rules['performance_threshold']:
            reasons.append(f"slow_performance({performance_ratio:.2f})")
        
        return ",".join(reasons) if reasons else "baseline"
    
    def get_current_interval(self) -> float:
        """Get current tick interval."""
        return self.current_interval
    
    def get_adaptation_stats(self) -> Dict[str, Any]:
        """Get comprehensive adaptation statistics."""
        if not self.recent_metrics:
            return {'status': 'no_data'}
        
        recent_intervals = [record['new_interval'] for record in self.adaptation_history[-10:]]
        recent_reasons = [record['change_reason'] for record in self.adaptation_history[-5:]]
        
        avg_interval = sum(recent_intervals) / len(recent_intervals) if recent_intervals else self.current_interval
        interval_stability = 1.0 - (max(recent_intervals) - min(recent_intervals)) / self.base_interval if recent_intervals else 1.0
        
        return {
            'current_interval': self.current_interval,
            'target_interval': self.target_interval,
            'base_interval': self.base_interval,
            'average_interval': avg_interval,
            'interval_stability': interval_stability,
            'adaptations_count': len(self.adaptation_history),
            'recent_reasons': recent_reasons,
            'metrics_collected': len(self.recent_metrics),
            'last_adaptation': self.last_adaptation_time,
            'speed_ratio': self.base_interval / self.current_interval,
            'bounds': {
                'min_interval': self.min_interval,
                'max_interval': self.max_interval
            }
        }
    
    def force_interval(self, interval: float, reason: str = "manual_override"):
        """Force a specific interval (manual override)."""
        old_interval = self.current_interval
        self.current_interval = max(self.min_interval, min(self.max_interval, interval))
        self.target_interval = self.current_interval
        
        # Record the forced change
        override_record = {
            'timestamp': datetime.now(),
            'input_metrics': {'manual_override': True},
            'speed_factor': self.current_interval / self.base_interval,
            'old_interval': old_interval,
            'new_interval': self.current_interval,
            'change_reason': reason
        }
        self.adaptation_history.append(override_record)
        
        logger.info(f"🎛️ Interval forced to {self.current_interval:.3f}s: {reason}")
    
    def reset_to_base(self):
        """Reset to base interval."""
        self.force_interval(self.base_interval, "reset_to_base")
    
    def emergency_slowdown(self, factor: float = 3.0):
        """Emergency slowdown for system protection."""
        emergency_interval = min(self.max_interval, self.current_interval * factor)
        self.force_interval(emergency_interval, f"emergency_slowdown(x{factor})")


class MergedTickEngine:
    """
    Merged tick engine that combines adaptive control with existing DAWN tick engines.
    Can integrate with multiple existing tick systems.
    """
    
    def __init__(self, adaptive_controller: Optional[AdaptiveTickController] = None):
        """Initialize merged tick engine."""
        self.adaptive_controller = adaptive_controller or AdaptiveTickController()
        
        # Integration hooks for existing engines
        self.existing_engines = {}
        self.tick_hooks = []
        self.pre_tick_hooks = []
        self.post_tick_hooks = []
        
        # Merged state
        self.running = False
        self.tick_count = 0
        self.start_time = None
        
        logger.info("🔗 Merged Tick Engine initialized with adaptive control")
    
    def register_existing_engine(self, name: str, engine: Any, tick_method: str = "tick"):
        """
        Register an existing DAWN tick engine for integration.
        
        Args:
            name: Identifier for the engine
            engine: The existing engine instance
            tick_method: Method name to call for ticking
        """
        self.existing_engines[name] = {
            'engine': engine,
            'tick_method': tick_method,
            'enabled': True,
            'last_tick_time': 0.0,
            'tick_count': 0,
            'errors': 0
        }
        
        logger.info(f"🔗 Registered existing engine: {name}")
    
    def add_tick_hook(self, hook: Callable, phase: str = "main"):
        """
        Add a tick hook function.
        
        Args:
            hook: Function to call during tick
            phase: When to call ("pre", "main", "post")
        """
        if phase == "pre":
            self.pre_tick_hooks.append(hook)
        elif phase == "post":
            self.post_tick_hooks.append(hook)
        else:
            self.tick_hooks.append(hook)
        
        logger.info(f"🪝 Added {phase} tick hook: {hook.__name__}")
    
    async def merged_tick(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a merged tick that integrates all systems.
        
        Args:
            context: Optional context data for the tick
            
        Returns:
            Dict containing tick results and metrics
        """
        tick_start = time.time()
        self.tick_count += 1
        
        # Gather system state for adaptation
        entropy = context.get('entropy', 0.5) if context else 0.5
        heat = context.get('heat', 25.0) if context else 25.0
        cognitive_load = context.get('cognitive_load', 0.5) if context else 0.5
        system_pressure = context.get('system_pressure', 0.5) if context else 0.5
        
        # Calculate last tick duration
        last_duration = context.get('last_tick_duration', 0.1) if context else 0.1
        
        # Adaptive interval calculation
        adaptive_interval = self.adaptive_controller.calculate_adaptive_interval(
            entropy=entropy,
            heat=heat,
            cognitive_load=cognitive_load,
            system_pressure=system_pressure,
            tick_duration=last_duration
        )
        
        tick_results = {
            'tick_number': self.tick_count,
            'timestamp': datetime.now().isoformat(),
            'adaptive_interval': adaptive_interval,
            'system_state': {
                'entropy': entropy,
                'heat': heat,
                'cognitive_load': cognitive_load,
                'system_pressure': system_pressure
            },
            'engine_results': {},
            'hook_results': {},
            'errors': []
        }
        
        # Execute pre-tick hooks
        for hook in self.pre_tick_hooks:
            try:
                hook_start = time.time()
                result = await hook(context) if asyncio.iscoroutinefunction(hook) else hook(context)
                tick_results['hook_results'][f'pre_{hook.__name__}'] = {
                    'result': result,
                    'duration': time.time() - hook_start
                }
            except Exception as e:
                tick_results['errors'].append(f"Pre-hook {hook.__name__}: {e}")
                logger.error(f"Pre-tick hook error: {e}")
        
        # Execute existing engines
        for name, engine_info in self.existing_engines.items():
            if not engine_info['enabled']:
                continue
            
            try:
                engine_start = time.time()
                engine = engine_info['engine']
                method_name = engine_info['tick_method']
                
                if hasattr(engine, method_name):
                    method = getattr(engine, method_name)
                    
                    # Call with context if method supports it
                    try:
                        result = await method(context) if asyncio.iscoroutinefunction(method) else method(context)
                    except TypeError:
                        # Fallback to no parameters
                        result = await method() if asyncio.iscoroutinefunction(method) else method()
                    
                    engine_info['last_tick_time'] = time.time()
                    engine_info['tick_count'] += 1
                    
                    tick_results['engine_results'][name] = {
                        'result': result,
                        'duration': time.time() - engine_start,
                        'tick_count': engine_info['tick_count']
                    }
                
            except Exception as e:
                engine_info['errors'] += 1
                tick_results['errors'].append(f"Engine {name}: {e}")
                logger.error(f"Engine {name} error: {e}")
        
        # Execute main tick hooks
        for hook in self.tick_hooks:
            try:
                hook_start = time.time()
                result = await hook(context) if asyncio.iscoroutinefunction(hook) else hook(context)
                tick_results['hook_results'][f'main_{hook.__name__}'] = {
                    'result': result,
                    'duration': time.time() - hook_start
                }
            except Exception as e:
                tick_results['errors'].append(f"Main hook {hook.__name__}: {e}")
                logger.error(f"Main tick hook error: {e}")
        
        # Execute post-tick hooks
        for hook in self.post_tick_hooks:
            try:
                hook_start = time.time()
                result = await hook(context) if asyncio.iscoroutinefunction(hook) else hook(context)
                tick_results['hook_results'][f'post_{hook.__name__}'] = {
                    'result': result,
                    'duration': time.time() - hook_start
                }
            except Exception as e:
                tick_results['errors'].append(f"Post-hook {hook.__name__}: {e}")
                logger.error(f"Post-tick hook error: {e}")
        
        # Calculate total tick duration
        total_duration = time.time() - tick_start
        tick_results['duration_ms'] = int(total_duration * 1000)
        tick_results['performance'] = {
            'total_duration': total_duration,
            'adaptive_interval': adaptive_interval,
            'efficiency_ratio': adaptive_interval / total_duration if total_duration > 0 else 1.0
        }
        
        return tick_results
    
    async def run_merged_loop(self, max_ticks: Optional[int] = None):
        """
        Run the merged adaptive tick loop.
        
        Args:
            max_ticks: Maximum number of ticks (None for infinite)
        """
        logger.info("🚀 Starting merged adaptive tick loop")
        
        self.running = True
        self.start_time = time.time()
        last_tick_time = time.time()
        
        try:
            while self.running and (max_ticks is None or self.tick_count < max_ticks):
                # Prepare context
                current_time = time.time()
                last_tick_duration = current_time - last_tick_time
                
                context = {
                    'tick_count': self.tick_count,
                    'uptime': current_time - self.start_time,
                    'last_tick_duration': last_tick_duration,
                    'entropy': 0.5,  # These would come from real systems
                    'heat': 25.0,
                    'cognitive_load': 0.5,
                    'system_pressure': 0.5
                }
                
                # Execute merged tick
                tick_results = await self.merged_tick(context)
                
                # Use adaptive interval for sleep
                sleep_time = tick_results['adaptive_interval']
                await asyncio.sleep(sleep_time)
                
                last_tick_time = time.time()
                
        except KeyboardInterrupt:
            logger.info("🛑 Merged loop interrupted by user")
        except Exception as e:
            logger.error(f"Merged loop error: {e}")
        finally:
            self.running = False
            logger.info("✅ Merged adaptive tick loop stopped")
    
    def get_merged_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the merged system."""
        return {
            'running': self.running,
            'tick_count': self.tick_count,
            'uptime': time.time() - self.start_time if self.start_time else 0,
            'adaptive_stats': self.adaptive_controller.get_adaptation_stats(),
            'registered_engines': {
                name: {
                    'enabled': info['enabled'],
                    'tick_count': info['tick_count'],
                    'errors': info['errors'],
                    'last_tick_time': info['last_tick_time']
                }
                for name, info in self.existing_engines.items()
            },
            'hooks': {
                'pre_tick': len(self.pre_tick_hooks),
                'main_tick': len(self.tick_hooks),
                'post_tick': len(self.post_tick_hooks)
            }
        }


# Factory functions for easy integration
def create_adaptive_controller(**kwargs) -> AdaptiveTickController:
    """Factory function for creating adaptive tick controller."""
    return AdaptiveTickController(**kwargs)


def create_merged_engine(adaptive_controller: Optional[AdaptiveTickController] = None) -> MergedTickEngine:
    """Factory function for creating merged tick engine."""
    return MergedTickEngine(adaptive_controller)


def integrate_with_dawn_tick_engine(tick_engine_instance, merged_engine: MergedTickEngine):
    """Helper function to integrate with existing DAWN tick engine."""
    merged_engine.register_existing_engine("dawn_tick_engine", tick_engine_instance)
    logger.info("🔗 Integrated with DAWN tick engine") 