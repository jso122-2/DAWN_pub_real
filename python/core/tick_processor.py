import asyncio
import logging
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class TriggerType(Enum):
    """Types of tick triggers"""
    INTERVAL = "interval"
    THRESHOLD = "threshold"
    PATTERN = "pattern"
    EVENT = "event"


@dataclass
class TickTrigger:
    """Defines a trigger that fires on certain tick conditions"""
    id: str
    name: str
    trigger_type: TriggerType
    condition: Dict[str, Any]
    callback: Callable
    enabled: bool = True
    last_fired: int = 0
    fire_count: int = 0


class TickProcessor:
    """
    Processes tick-based triggers and manages active processes
    """
    
    def __init__(self):
        self.triggers: Dict[str, TickTrigger] = {}
        self.active_processes: Dict[str, Dict[str, Any]] = {}
        self.process_queue: List[Dict[str, Any]] = []
        
        logger.info("TickProcessor initialized")
    
    def register_trigger(
        self,
        trigger_id: str,
        name: str,
        trigger_type: TriggerType,
        condition: Dict[str, Any],
        callback: Callable,
        enabled: bool = True
    ):
        """Register a new tick trigger"""
        trigger = TickTrigger(
            id=trigger_id,
            name=name,
            trigger_type=trigger_type,
            condition=condition,
            callback=callback,
            enabled=enabled
        )
        
        self.triggers[trigger_id] = trigger
        logger.info(f"Registered trigger: {name} ({trigger_type.value})")
    
    def unregister_trigger(self, trigger_id: str):
        """Remove a tick trigger"""
        if trigger_id in self.triggers:
            del self.triggers[trigger_id]
            logger.info(f"Unregistered trigger: {trigger_id}")
    
    def enable_trigger(self, trigger_id: str):
        """Enable a trigger"""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].enabled = True
            logger.info(f"Enabled trigger: {trigger_id}")
    
    def disable_trigger(self, trigger_id: str):
        """Disable a trigger"""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].enabled = False
            logger.info(f"Disabled trigger: {trigger_id}")
    
    async def process_tick_triggers(self, tick_data):
        """Process all triggers for the current tick"""
        for trigger in self.triggers.values():
            if not trigger.enabled:
                continue
            
            try:
                should_fire = await self._evaluate_trigger(trigger, tick_data)
                
                if should_fire:
                    await self._fire_trigger(trigger, tick_data)
                    
            except Exception as e:
                logger.error(f"Error processing trigger {trigger.id}: {e}")
    
    async def _evaluate_trigger(self, trigger: TickTrigger, tick_data) -> bool:
        """Evaluate if a trigger should fire"""
        tick_number = tick_data.tick_number
        
        if trigger.trigger_type == TriggerType.INTERVAL:
            interval = trigger.condition.get('interval', 100)
            return (tick_number - trigger.last_fired) >= interval
        
        elif trigger.trigger_type == TriggerType.THRESHOLD:
            metric = trigger.condition.get('metric')
            threshold = trigger.condition.get('threshold')
            operator = trigger.condition.get('operator', 'gt')
            
            if metric and threshold is not None:
                value = getattr(tick_data, metric, None)
                if value is None:
                    return False
                
                if operator == 'gt':
                    return value > threshold
                elif operator == 'lt':
                    return value < threshold
                elif operator == 'eq':
                    return abs(value - threshold) < 0.01
                elif operator == 'gte':
                    return value >= threshold
                elif operator == 'lte':
                    return value <= threshold
        
        elif trigger.trigger_type == TriggerType.PATTERN:
            # Pattern detection would go here
            # For now, just return False
            return False
        
        elif trigger.trigger_type == TriggerType.EVENT:
            # Event-based triggers
            event_type = trigger.condition.get('event')
            # Check if the event occurred in tick_data
            return False
        
        return False
    
    async def _fire_trigger(self, trigger: TickTrigger, tick_data):
        """Fire a trigger"""
        try:
            trigger.last_fired = tick_data.tick_number
            trigger.fire_count += 1
            
            logger.debug(f"Firing trigger: {trigger.name}")
            
            # Call the trigger callback
            if asyncio.iscoroutinefunction(trigger.callback):
                await trigger.callback(tick_data)
            else:
                trigger.callback(tick_data)
                
        except Exception as e:
            logger.error(f"Error firing trigger {trigger.id}: {e}")
    
    def start_process(
        self,
        process_id: str,
        name: str,
        category: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Start a new process"""
        process = {
            'id': process_id,
            'name': name,
            'category': category,
            'status': 'running',
            'start_time': time.time(),
            'metadata': metadata or {}
        }
        
        self.active_processes[process_id] = process
        logger.info(f"Started process: {name} ({process_id})")
    
    def stop_process(self, process_id: str):
        """Stop a running process"""
        if process_id in self.active_processes:
            process = self.active_processes[process_id]
            process['status'] = 'completed'
            process['end_time'] = time.time()
            
            # Move to completed or remove after some time
            del self.active_processes[process_id]
            logger.info(f"Stopped process: {process_id}")
    
    async def get_active_processes(self) -> List[str]:
        """Get list of active process names"""
        return [
            f"{proc['category']}.{proc['name']}" 
            for proc in self.active_processes.values()
            if proc['status'] == 'running'
        ]
    
    def get_process_info(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific process"""
        return self.active_processes.get(process_id)
    
    def get_all_processes(self) -> Dict[str, Dict[str, Any]]:
        """Get all active processes"""
        return self.active_processes.copy()
    
    def get_trigger_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics about all triggers"""
        stats = {}
        for trigger_id, trigger in self.triggers.items():
            stats[trigger_id] = {
                'name': trigger.name,
                'type': trigger.trigger_type.value,
                'enabled': trigger.enabled,
                'fire_count': trigger.fire_count,
                'last_fired': trigger.last_fired
            }
        return stats
    
    async def cleanup_completed_processes(self):
        """Clean up old completed processes"""
        current_time = time.time()
        to_remove = []
        
        for process_id, process in self.active_processes.items():
            if process['status'] == 'completed':
                end_time = process.get('end_time', current_time)
                if current_time - end_time > 300:  # 5 minutes
                    to_remove.append(process_id)
        
        for process_id in to_remove:
            del self.active_processes[process_id]
            logger.debug(f"Cleaned up completed process: {process_id}")
    
    def queue_process(self, process_data: Dict[str, Any]):
        """Queue a process for later execution"""
        self.process_queue.append(process_data)
        logger.debug(f"Queued process: {process_data.get('name', 'unknown')}")
    
    async def process_queue_tick(self):
        """Process queued items on each tick"""
        if not self.process_queue:
            return
        
        # Process one item from queue per tick
        process_data = self.process_queue.pop(0)
        
        try:
            # Execute the queued process
            process_id = process_data.get('id', f"queued_{int(time.time())}")
            self.start_process(
                process_id,
                process_data.get('name', 'queued_process'),
                process_data.get('category', 'queued'),
                process_data.get('metadata', {})
            )
        except Exception as e:
            logger.error(f"Error processing queued item: {e}")
    
    def get_queue_size(self) -> int:
        """Get number of items in process queue"""
        return len(self.process_queue) 