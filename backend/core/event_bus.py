"""
Event Bus - Handles event distribution and subscription in the DAWN system
"""

import logging
import asyncio
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """Event data structure"""
    type: str
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "system"

class EventBus:
    """Event bus for distributing events across the system"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.max_history: int = 1000
        logger.info("Initialized EventBus")
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event type: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event type: {event_type}")
    
    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers"""
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history = self.event_history[-self.max_history:]
        
        # Notify subscribers
        if event.type in self.subscribers:
            for callback in self.subscribers[event.type]:
                try:
                    await callback(event)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")
    
    def get_history(self, event_type: Optional[str] = None) -> List[Event]:
        """Get event history, optionally filtered by type"""
        if event_type:
            return [e for e in self.event_history if e.type == event_type]
        return self.event_history.copy()

# Global event bus instance
_event_bus = None

def get_event_bus() -> EventBus:
    """Get the global event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus 