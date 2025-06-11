# core/event_bus.py
"""
Event Bus - Core Communication System
=====================================
"""

from typing import Dict, List, Callable, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class EventBus:
    """
    Dynamic event bus for loose coupling between DAWN components.
    Supports event registration, emission, and dynamic hook binding.
    """
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("DAWN.EventBus")
        
    def on(self, event: str, handler: Callable) -> None:
        """Register a handler for an event"""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(handler)
        self.logger.debug(f"Registered handler for event: {event}")
        
    def off(self, event: str, handler: Callable) -> None:
        """Remove a handler for an event"""
        if event in self.listeners and handler in self.listeners[event]:
            self.listeners[event].remove(handler)
            self.logger.debug(f"Removed handler for event: {event}")
            
    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Emit an event to all registered handlers"""
        if event not in self.listeners:
            return
            
        self.logger.debug(f"Emitting event: {event}")
        for handler in self.listeners[event]:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event}: {str(e)}")
                
    def clear(self, event: str = None) -> None:
        """Clear all handlers for an event or all events"""
        if event:
            if event in self.listeners:
                del self.listeners[event]
                self.logger.debug(f"Cleared handlers for event: {event}")
        else:
            self.listeners.clear()
            self.logger.debug("Cleared all event handlers")
            
    def get_handlers(self, event: str) -> List[Callable]:
        """Get all handlers for an event"""
        return self.listeners.get(event, [])
        
    def has_handlers(self, event: str) -> bool:
        """Check if an event has any handlers"""
        return event in self.listeners and len(self.listeners[event]) > 0


# Global event bus instance
event_bus = EventBus()
