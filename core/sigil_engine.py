#!/usr/bin/env python3
"""
DAWN Sigil Engine
Advanced cognitive command processing system with integrated pulse control

Manages sigil execution, priority queuing, thermal regulation, and decay cycles
"""

import time
import random
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import heapq
from datetime import datetime, timedelta

# Import DAWN Pulse Controller
try:
    from ...pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    print("⚠️ Pulse Controller not available, using fallback")
    PULSE_CONTROLLER_AVAILABLE = False
    PulseController = None

# Import existing components
from schema.sigil import Sigil
from pulse.scup_tracker import SCUPTracker

# Sigil trace logging
try:
    from sigil_trace import log_sigil_registration, log_sigil_execution, log_sigil_activation
    SIGIL_TRACE_AVAILABLE = True
except ImportError:
    SIGIL_TRACE_AVAILABLE = False
    def log_sigil_registration(*args, **kwargs): pass
    def log_sigil_execution(*args, **kwargs): pass
    def log_sigil_activation(*args, **kwargs): pass


class CognitiveHouse(Enum):
    """Cognitive processing houses for sigil routing"""
    MEMORY = "memory"
    ANALYSIS = "analysis" 
    SYNTHESIS = "synthesis"
    ATTENTION = "attention"
    INTEGRATION = "integration"
    META = "meta"
    ACTION = "action"
    MONITOR = "monitor"


class SigilStatus(Enum):
    """Sigil execution status"""
    PENDING = "pending"
    ACTIVE = "active"
    EXECUTED = "executed"
    DECAYED = "decayed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionResult:
    """Result of sigil execution"""
    sigil_id: str
    status: SigilStatus
    execution_time: float
    heat_generated: float
    output: Any = None
    error: Optional[str] = None


class SigilEngine:
    """Advanced sigil processing engine with thermal regulation"""
    
    def __init__(self, initial_heat: float = 25.0):
        # Core engine state
        self.engine_id = f"SIGIL_{int(time.time())}"
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        
        # Initialize Pulse Controller for thermal regulation
        if PULSE_CONTROLLER_AVAILABLE:
            self.pulse_controller = PulseController(initial_heat=initial_heat)
            self.logger.info("🔥 Pulse Controller integrated for thermal regulation")
        else:
            self.pulse_controller = None
            self.current_heat = initial_heat
            self.logger.warning("⚠️ Running without Pulse Controller - limited thermal management")
        
        # Sigil management
        self.active_sigils: Dict[str, Sigil] = {}
        self.priority_queue: List[tuple] = []  # (priority, timestamp, sigil_id)
        self.execution_history: List[ExecutionResult] = []
        self.decay_queue: List[tuple] = []  # (decay_time, sigil_id)
        
        # Performance metrics
        self.total_executions = 0
        self.successful_executions = 0
        self.heat_events = []
        self.start_time = time.time()
        
        # Cognitive house routing
        self.house_processors = {
            CognitiveHouse.MEMORY: self._process_memory_sigil,
            CognitiveHouse.ANALYSIS: self._process_analysis_sigil,
            CognitiveHouse.SYNTHESIS: self._process_synthesis_sigil,
            CognitiveHouse.ATTENTION: self._process_attention_sigil,
            CognitiveHouse.INTEGRATION: self._process_integration_sigil,
            CognitiveHouse.META: self._process_meta_sigil,
            CognitiveHouse.ACTION: self._process_action_sigil,
            CognitiveHouse.MONITOR: self._process_monitor_sigil,
        }
        
        # Entropy integration
        self.entropy_analyzer = None
        self.entropy_tracking_enabled = True
        self.last_entropy_sync = time.time()
        
        self.logger.info(f"🔮 DAWN Sigil Engine initialized")
    
    def register_sigil(self, sigil: Sigil) -> bool:
        """
        Register a new sigil with automatic priority calculation and thermal management
        
        Args:
            sigil: Sigil object to register
            
        Returns:
            bool: True if successfully registered
        """
        try:
            # Calculate automatic lifespan if not set
            if sigil.lifespan <= 0:
                sigil.lifespan = self._calculate_lifespan(sigil)
            
            # Calculate priority score
            sigil.priority_score = self._calculate_priority_score(sigil)
            
            # Register sigil
            self.active_sigils[sigil.sigil_id] = sigil
            
            # Add to priority queue
            priority_tuple = (-sigil.priority_score, time.time(), sigil.sigil_id)
            heapq.heappush(self.priority_queue, priority_tuple)
            
            # Schedule decay
            decay_time = time.time() + sigil.lifespan
            heapq.heappush(self.decay_queue, (decay_time, sigil.sigil_id))
            
            # Update thermal state
            self._update_thermal_state(sigil.thermal_signature)
            
            self.logger.info(
                f"✨ Registered sigil: {sigil.sigil_id} | {sigil.command} | "
                f"{sigil.symbol}{sigil.cognitive_house.title()} | "
                f"L{sigil.level} | T{sigil.thermal_signature}"
            )
            
            # Log to sigil trace
            if SIGIL_TRACE_AVAILABLE:
                tick_number = getattr(self, 'current_tick', int(time.time()))
                log_sigil_registration(tick_number, sigil.sigil_id, sigil.priority_score)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to register sigil {sigil.sigil_id}: {e}")
            return False
    
    def execute_next_sigil(self) -> Optional[ExecutionResult]:
        """
        Execute the next highest-priority sigil with thermal regulation
        
        Returns:
            ExecutionResult or None if no sigils available
        """
        try:
            # Check thermal constraints
            if self.pulse_controller:
                current_zone = self.pulse_controller.get_pulse_zone()
                grace_period = self.pulse_controller.apply_grace_period()
                
                if grace_period > 0:
                    self.logger.info(f"⏸️ Execution paused - Grace period: {grace_period:.1f}s")
                    return None
                
                if current_zone == "SURGE":
                    self.logger.warning(f"🔥 System in SURGE mode - Heat: {self.pulse_controller.current_heat:.1f}")
            
            # Process decay queue
            self._process_decay_queue()
            
            # Get next sigil
            if not self.priority_queue:
                return None
            
            _, _, sigil_id = heapq.heappop(self.priority_queue)
            
            if sigil_id not in self.active_sigils:
                # Sigil was already decayed
                return self.execute_next_sigil()
            
            sigil = self.active_sigils[sigil_id]
            
            # Execute sigil
            start_time = time.time()
            result = self._execute_sigil(sigil)
            execution_time = time.time() - start_time
            
            # Update thermal state with execution heat
            heat_generated = sigil.thermal_signature * (1.0 + sigil.level * 0.1)
            self._update_thermal_state(heat_generated)
            
            # Create execution result
            exec_result = ExecutionResult(
                sigil_id=sigil.sigil_id,
                status=SigilStatus.EXECUTED,
                execution_time=execution_time,
                heat_generated=heat_generated,
                output=result
            )
            
            # Record execution
            self.execution_history.append(exec_result)
            self.total_executions += 1
            self.successful_executions += 1
            
            # Remove from active sigils
            del self.active_sigils[sigil_id]
            
            self.logger.info(
                f"⚡ Executed: {sigil.sigil_id} | "
                f"Time: {execution_time:.3f}s | Heat: +{heat_generated:.1f}"
            )
            
            # Log to sigil trace
            if SIGIL_TRACE_AVAILABLE:
                tick_number = getattr(self, 'current_tick', int(time.time()))
                log_sigil_execution(tick_number, sigil.sigil_id, heat_generated)
            
            # Sync with entropy analyzer
            self._sync_entropy_data(sigil, exec_result)
            
            return exec_result
            
        except Exception as e:
            self.logger.error(f"❌ Execution error: {e}")
            return ExecutionResult(
                sigil_id=sigil_id if 'sigil_id' in locals() else "unknown",
                status=SigilStatus.CANCELLED,
                execution_time=0.0,
                heat_generated=0.0,
                error=str(e)
            )
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get comprehensive engine status including thermal metrics"""
        current_time = time.time()
        uptime = current_time - self.start_time
        
        # Base status
        status = {
            'engine_id': self.engine_id,
            'is_running': self.is_running,
            'uptime': round(uptime, 1),
            'active_sigils': len(self.active_sigils),
            'queued_sigils': len(self.priority_queue),
            'total_executions': self.total_executions,
            'successful_executions': self.successful_executions,
            'execution_rate': round(self.total_executions / uptime, 2) if uptime > 0 else 0.0
        }
        
        # Add thermal status if pulse controller available
        if self.pulse_controller:
            thermal_stats = self.pulse_controller.get_heat_statistics()
            status.update({
                'current_heat': thermal_stats['current_heat'],
                'current_zone': thermal_stats['current_zone'],
                'time_in_zone': thermal_stats['time_in_current_zone'],
                'tick_interval': thermal_stats['current_tick_interval'],
                'grace_period': thermal_stats['current_grace_period'],
                'total_surges': thermal_stats['total_surges'],
                'heat_variance': thermal_stats['heat_variance']
            })
        else:
            status.update({
                'current_heat': getattr(self, 'current_heat', 25.0),
                'current_zone': 'UNKNOWN',
                'thermal_regulation': 'DISABLED'
            })
        
        return status
    
    def apply_decay_cycle(self, temperature: float = None) -> Dict[str, Any]:
        """
        Apply thermal decay to all active sigils
        
        Args:
            temperature: Optional temperature override
            
        Returns:
            Decay cycle results
        """
        if temperature is None:
            temperature = self.pulse_controller.current_heat if self.pulse_controller else 25.0
        
        decay_factor = 1.0 + (temperature - 50.0) / 100.0  # Scales with temperature
        decayed_sigils = []
        
        current_time = time.time()
        for sigil_id, sigil in list(self.active_sigils.items()):
            # Apply decay
            decay_amount = sigil.decay_rate * decay_factor
            sigil.lifespan -= decay_amount
            
            if sigil.lifespan <= 0:
                # Sigil has decayed
                decayed_sigils.append(sigil_id)
                del self.active_sigils[sigil_id]
                
                # Record decay event
                decay_result = ExecutionResult(
                    sigil_id=sigil_id,
                    status=SigilStatus.DECAYED,
                    execution_time=0.0,
                    heat_generated=-sigil.thermal_signature * 0.1  # Slight cooling
                )
                self.execution_history.append(decay_result)
        
        # Apply thermal decay
        if self.pulse_controller:
            self.pulse_controller.apply_heat_decay()
        
        self.logger.info(f"🧪 Decay cycle: {len(decayed_sigils)} sigils decayed at T={temperature:.1f}")
        
        return {
            'decayed_count': len(decayed_sigils),
            'decayed_sigils': decayed_sigils,
            'temperature': temperature,
            'decay_factor': decay_factor,
            'remaining_sigils': len(self.active_sigils)
        }
    
    def _calculate_lifespan(self, sigil: Sigil) -> float:
        """Calculate automatic lifespan based on sigil properties"""
        base_lifespan = 60.0  # 1 minute base
        
        # Level modifier (higher level = longer life)
        level_modifier = 1.0 + (sigil.level - 1) * 0.2
        
        # Thermal modifier (higher heat = shorter life)
        thermal_modifier = max(0.5, 1.0 - (sigil.thermal_signature - 50.0) / 100.0)
        
        # House modifier
        house_modifiers = {
            CognitiveHouse.MEMORY: 1.5,     # Memory sigils last longer
            CognitiveHouse.META: 1.3,       # Meta sigils persist
            CognitiveHouse.ACTION: 0.8,     # Action sigils are quick
            CognitiveHouse.MONITOR: 2.0,    # Monitor sigils are persistent
        }
        
        house_modifier = house_modifiers.get(
            CognitiveHouse(sigil.cognitive_house), 1.0
        )
        
        lifespan = base_lifespan * level_modifier * thermal_modifier * house_modifier
        return max(10.0, lifespan)  # Minimum 10 second lifespan
    
    def _calculate_priority_score(self, sigil: Sigil) -> float:
        """Calculate priority score for queue ordering"""
        # Base priority from level
        priority = float(sigil.level) * 10.0
        
        # Thermal urgency (higher heat = higher priority)
        thermal_urgency = sigil.thermal_signature / 10.0
        
        # House priority modifiers
        house_priorities = {
            CognitiveHouse.ACTION: 15.0,        # Actions are urgent
            CognitiveHouse.ATTENTION: 12.0,     # Attention is high priority
            CognitiveHouse.MONITOR: 8.0,        # Monitoring is important
            CognitiveHouse.INTEGRATION: 10.0,   # Integration is valuable
            CognitiveHouse.ANALYSIS: 7.0,       # Analysis is medium
            CognitiveHouse.SYNTHESIS: 6.0,      # Synthesis can wait
            CognitiveHouse.MEMORY: 5.0,         # Memory is background
            CognitiveHouse.META: 3.0,           # Meta is lowest
        }
        
        house_priority = house_priorities.get(
            CognitiveHouse(sigil.cognitive_house), 5.0
        )
        
        # Decay urgency (shorter lifespan = higher priority)
        if sigil.lifespan > 0:
            decay_urgency = max(0, 60.0 - sigil.lifespan) / 10.0
        else:
            decay_urgency = 0
        
        total_priority = priority + thermal_urgency + house_priority + decay_urgency
        return round(total_priority, 2)
    
    def _update_thermal_state(self, heat_change: float):
        """Update thermal state through pulse controller"""
        if self.pulse_controller:
            new_heat = self.pulse_controller.current_heat + heat_change
            result = self.pulse_controller.update_heat(new_heat)
            
            # Log significant thermal events
            if result.get('zone_changed'):
                self.heat_events.append({
                    'timestamp': time.time(),
                    'event': 'zone_change',
                    'from_zone': result['previous_zone'],
                    'to_zone': result['current_zone'],
                    'heat': result['current_heat']
                })
        else:
            # Fallback thermal management
            self.current_heat = max(0, min(100, getattr(self, 'current_heat', 25.0) + heat_change))
    
    def _process_decay_queue(self):
        """Process sigils scheduled for decay"""
        current_time = time.time()
        
        while self.decay_queue and self.decay_queue[0][0] <= current_time:
            _, sigil_id = heapq.heappop(self.decay_queue)
            
            if sigil_id in self.active_sigils:
                sigil = self.active_sigils[sigil_id]
                del self.active_sigils[sigil_id]
                
                # Record natural decay
                decay_result = ExecutionResult(
                    sigil_id=sigil_id,
                    status=SigilStatus.DECAYED,
                    execution_time=0.0,
                    heat_generated=-sigil.thermal_signature * 0.05
                )
                self.execution_history.append(decay_result)
                
                self.logger.info(f"⏳ Natural decay: {sigil_id}")
    
    def _execute_sigil(self, sigil: Sigil) -> Any:
        """Route sigil to appropriate cognitive house processor"""
        try:
            house = CognitiveHouse(sigil.cognitive_house)
            processor = self.house_processors.get(house)
            
            if processor:
                return processor(sigil)
            else:
                return f"Processed {sigil.command} in {sigil.cognitive_house}"
                
        except Exception as e:
            self.logger.error(f"❌ Execution error for {sigil.sigil_id}: {e}")
            raise
    
    # Cognitive house processors
    def _process_memory_sigil(self, sigil: Sigil) -> str:
        """Process memory-related sigils"""
        return f"🧠 Memory operation: {sigil.command} | Level {sigil.level}"
    
    def _process_analysis_sigil(self, sigil: Sigil) -> str:
        """Process analysis-related sigils"""
        return f"🔍 Analysis operation: {sigil.command} | Level {sigil.level}"
    
    def _process_synthesis_sigil(self, sigil: Sigil) -> str:
        """Process synthesis-related sigils"""
        return f"🌟 Synthesis operation: {sigil.command} | Level {sigil.level}"
    
    def _process_attention_sigil(self, sigil: Sigil) -> str:
        """Process attention-related sigils"""
        return f"👁️ Attention operation: {sigil.command} | Level {sigil.level}"
    
    def _process_integration_sigil(self, sigil: Sigil) -> str:
        """Process integration-related sigils"""
        return f"🔗 Integration operation: {sigil.command} | Level {sigil.level}"
    
    def _process_meta_sigil(self, sigil: Sigil) -> str:
        """Process meta-cognitive sigils"""
        return f"🧠 Meta operation: {sigil.command} | Level {sigil.level}"
    
    def _process_action_sigil(self, sigil: Sigil) -> str:
        """Process action-related sigils"""
        return f"⚡ Action operation: {sigil.command} | Level {sigil.level}"
    
    def _process_monitor_sigil(self, sigil: Sigil) -> str:
        """Process monitoring-related sigils"""
        return f"🎯 Monitor operation: {sigil.command} | Level {sigil.level}"
    
    def inject_test_sigils(self, count: int = 5) -> List[str]:
        """Inject test sigils for demonstration"""
        test_templates = [
            {"command": "SystemWatchPro", "symbol": "🎯", "house": "monitor", "level": 5, "thermal": 56.5},
            {"command": "MemoryRecall", "symbol": "🧠", "house": "memory", "level": 6, "thermal": 67.4},
            {"command": "SystemWatchPlus", "symbol": "🎯", "house": "monitor", "level": 4, "thermal": 53.0},
            {"command": "DataIntegrationPro", "symbol": "🔗", "house": "integration", "level": 7, "thermal": 47.4},
            {"command": "MemoryRecallPro", "symbol": "🧠", "house": "memory", "level": 6, "thermal": 34.5},
            {"command": "DeepAnalysis", "symbol": "🔍", "house": "analysis", "level": 8, "thermal": 72.1},
            {"command": "CreativeSynth", "symbol": "🌟", "house": "synthesis", "level": 5, "thermal": 45.8},
            {"command": "FocusLock", "symbol": "👁️", "house": "attention", "level": 7, "thermal": 63.2},
            {"command": "ActionTrigger", "symbol": "⚡", "house": "action", "level": 9, "thermal": 81.4},
            {"command": "MetaMonitor", "symbol": "🧠", "house": "meta", "level": 4, "thermal": 38.9}
        ]
        
        injected_ids = []
        for i in range(min(count, len(test_templates))):
            template = test_templates[i]
            
            sigil = Sigil(
                sigil_id=f"{template['house'][:3].upper()}{int(time.time()) % 10000}",
                command=template['command'],
                symbol=template['symbol'],
                cognitive_house=template['house'],
                level=template['level'],
                thermal_signature=template['thermal']
            )
            
            if self.register_sigil(sigil):
                injected_ids.append(sigil.sigil_id)
        
        self.logger.info(f"🧪 Injected {len(injected_ids)} test sigils for demonstration")
        return injected_ids
    
    def set_entropy_analyzer(self, entropy_analyzer) -> None:
        """
        Set the entropy analyzer for cognitive load tracking
        
        Args:
            entropy_analyzer: EntropyAnalyzer instance
        """
        self.entropy_analyzer = entropy_analyzer
        self.logger.info(f"🧬 Entropy analyzer connected to sigil engine")
    
    def _sync_entropy_data(self, sigil: Sigil, result: ExecutionResult) -> None:
        """
        Sync sigil execution data with entropy analyzer
        
        Args:
            sigil: Executed sigil
            result: Execution result
        """
        try:
            if not self.entropy_analyzer or not self.entropy_tracking_enabled:
                return
            
            current_time = time.time()
            
            # Throttle updates to every 3 seconds
            if current_time - self.last_entropy_sync < 3.0:
                return
            
            # Create sigil data for entropy analysis
            sigil_data = {
                'active_sigils': list(self.active_sigils.keys()) if isinstance(self.active_sigils, dict) else [],
                'execution_heat': result.heat_generated,
                'cognitive_house': sigil.cognitive_house,
                'sigil_level': sigil.level,
                'queue_size': len(self.priority_queue),
                'execution_time': result.execution_time,
                'thermal_signature': sigil.thermal_signature
            }
            
            # Add thermal context if available
            if self.pulse_controller:
                thermal_status = self.pulse_controller.get_heat_statistics()
                sigil_data.update({
                    'system_heat': thermal_status['current_heat'],
                    'thermal_zone': thermal_status['current_zone'],
                    'grace_period': thermal_status['current_grace_period']
                })
            
            # Inject sigil awareness into entropy analyzer
            self.entropy_analyzer.inject_sigil_awareness(sigil_data)
            
            # Check for entropy-based recommendations
            if hasattr(self.entropy_analyzer, 'get_chaos_alerts'):
                alerts = self.entropy_analyzer.get_chaos_alerts('medium')
                if alerts:
                    # Adjust processing based on entropy alerts
                    for alert in alerts:
                        if alert.risk_level in ['high', 'critical']:
                            self.logger.warning(f"🌪️ Entropy alert for bloom {alert.bloom_id}: {alert.risk_level}")
                            
                            # Apply sigil-based stabilization
                            self._apply_entropy_stabilization(alert)
            
            self.last_entropy_sync = current_time
            
        except Exception as e:
            self.logger.warning(f"❌ Error syncing entropy data: {e}")
    
    def _apply_entropy_stabilization(self, alert) -> None:
        """
        Apply sigil-based entropy stabilization
        
        Args:
            alert: ChaosAlert instance
        """
        try:
            stabilization_sigils = []
            
            if alert.risk_level == 'critical':
                # Emergency cooling sigils
                stabilization_sigils.extend([
                    "CooldownEmergency", "EntropyDampen", "ChaosContain"
                ])
            elif alert.risk_level == 'high':
                # Preventive stabilization sigils  
                stabilization_sigils.extend([
                    "EntropyRegulate", "PatternStabilize", "HeatDisperse"
                ])
            
            # Generate and register stabilization sigils
            for sigil_name in stabilization_sigils:
                stabilization_sigil = self._create_stabilization_sigil(sigil_name, alert)
                if stabilization_sigil:
                    self.register_sigil(stabilization_sigil)
                    self.logger.info(f"🧬 Generated entropy stabilization sigil: {sigil_name}")
        
        except Exception as e:
            self.logger.warning(f"❌ Error applying entropy stabilization: {e}")
    
    def _create_stabilization_sigil(self, sigil_name: str, alert) -> Optional[Sigil]:
        """
        Create a stabilization sigil based on entropy alert
        
        Args:
            sigil_name: Name of stabilization sigil
            alert: ChaosAlert instance
            
        Returns:
            Stabilization sigil or None
        """
        try:
            sigil_id = f"STAB_{sigil_name}_{int(time.time())}"
            
            # Map sigil types to properties
            sigil_configs = {
                "CooldownEmergency": {
                    "symbol": "❄️",
                    "house": CognitiveHouse.ACTION,
                    "level": 8,
                    "thermal": -30.0,  # Cooling effect
                    "command": f"emergency_cooldown_bloom_{alert.bloom_id}"
                },
                "EntropyDampen": {
                    "symbol": "🌊", 
                    "house": CognitiveHouse.INTEGRATION,
                    "level": 6,
                    "thermal": -15.0,
                    "command": f"dampen_entropy_bloom_{alert.bloom_id}"
                },
                "ChaosContain": {
                    "symbol": "🌀",
                    "house": CognitiveHouse.META,
                    "level": 7,
                    "thermal": -20.0,
                    "command": f"contain_chaos_bloom_{alert.bloom_id}"
                },
                "EntropyRegulate": {
                    "symbol": "⚙️",
                    "house": CognitiveHouse.MONITOR,
                    "level": 5,
                    "thermal": -10.0,
                    "command": f"regulate_entropy_bloom_{alert.bloom_id}"
                },
                "PatternStabilize": {
                    "symbol": "🔗",
                    "house": CognitiveHouse.SYNTHESIS,
                    "level": 4,
                    "thermal": -8.0,
                    "command": f"stabilize_pattern_bloom_{alert.bloom_id}"
                },
                "HeatDisperse": {
                    "symbol": "💨",
                    "house": CognitiveHouse.ACTION,
                    "level": 3,
                    "thermal": -12.0,
                    "command": f"disperse_heat_bloom_{alert.bloom_id}"
                }
            }
            
            config = sigil_configs.get(sigil_name)
            if not config:
                return None
            
            # Create stabilization sigil
            stabilization_sigil = Sigil(
                sigil_id=sigil_id,
                command=config["command"],
                symbol=config["symbol"],
                cognitive_house=config["house"].value,
                level=config["level"],
                thermal_signature=config["thermal"],
                lifespan=30.0,  # Short-lived emergency sigils
                decay_rate=0.5,  # Fast decay
                metadata={
                    "type": "entropy_stabilization",
                    "target_bloom": alert.bloom_id,
                    "chaos_score": alert.chaos_score,
                    "generated_at": time.time()
                }
            )
            
            return stabilization_sigil
            
        except Exception as e:
            self.logger.warning(f"❌ Error creating stabilization sigil {sigil_name}: {e}")
            return None
    
    def get_entropy_metrics(self) -> Dict[str, Any]:
        """
        Get entropy-related metrics from sigil engine
        
        Returns:
            Dictionary with entropy correlation data
        """
        metrics = {
            'active_sigil_count': len(self.active_sigils),
            'queue_size': len(self.priority_queue),
            'entropy_analyzer_connected': self.entropy_analyzer is not None,
            'entropy_tracking_enabled': self.entropy_tracking_enabled
        }
        
        if self.entropy_analyzer:
            try:
                # Get entropy feedback
                alerts = self.entropy_analyzer.get_chaos_alerts() if hasattr(self.entropy_analyzer, 'get_chaos_alerts') else []
                hot_blooms = self.entropy_analyzer.get_hot_blooms() if hasattr(self.entropy_analyzer, 'get_hot_blooms') else []
                
                metrics.update({
                    'chaos_alerts_count': len(alerts),
                    'hot_blooms_count': len(hot_blooms),
                    'entropy_correlation': True
                })
                
                # Count stabilization sigils
                stabilization_count = sum(1 for sigil in self.active_sigils.values() 
                                        if sigil.metadata.get('type') == 'entropy_stabilization')
                metrics['active_stabilization_sigils'] = stabilization_count
                
            except Exception as e:
                metrics['entropy_error'] = str(e)
        
        return metrics


def create_test_sigil_engine() -> SigilEngine:
    """Create a test sigil engine with sample data"""
    engine = SigilEngine(initial_heat=30.0)
    engine.inject_test_sigils(5)
    return engine


if __name__ == "__main__":
    # Test the integrated sigil engine
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
    
    print("🔮 Testing DAWN Sigil Engine with Pulse Controller Integration")
    print("=" * 60)
    
    engine = create_test_sigil_engine()
    
    print(f"\n📊 Initial Status:")
    status = engine.get_engine_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print(f"\n⚡ Executing sigils...")
    for i in range(3):
        result = engine.execute_next_sigil()
        if result:
            print(f"  Execution {i+1}: {result.sigil_id} | "
                  f"Status: {result.status.value} | "
                  f"Heat: +{result.heat_generated:.1f}")
        else:
            print(f"  Execution {i+1}: No sigils available")
        
        time.sleep(0.5)
    
    print(f"\n🧪 Testing decay cycle...")
    decay_result = engine.apply_decay_cycle(temperature=75.0)
    print(f"  Decayed: {decay_result['decayed_count']} sigils")
    print(f"  Remaining: {decay_result['remaining_sigils']} sigils")
    
    print(f"\n📊 Final Status:")
    final_status = engine.get_engine_status()
    for key, value in final_status.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ DAWN Sigil Engine with Pulse Controller integration test complete!") 