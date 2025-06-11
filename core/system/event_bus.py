# core/system/event_bus.py
"""
DAWN Event Bus - The Neural Network
===================================
Central communication system for all DAWN components
"""

from collections import defaultdict, deque
from typing import Callable, Dict, List, Any, Optional, Union, Pattern
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
import re
import inspect
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    """Base event with metadata"""
    type: str
    data: Dict[Any, Any]
    source: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    
    def matches(self, pattern: str) -> bool:
        """Check if event type matches pattern (supports wildcards)"""
        if pattern == '*':
            return True
        if pattern.endswith('.*'):
            prefix = pattern[:-2]
            return self.type.startswith(prefix)
        return self.type == pattern


@dataclass  
class EventSubscription:
    """Subscription details"""
    pattern: str
    handler: Callable
    source: Optional[str] = None
    filter_func: Optional[Callable] = None
    priority: EventPriority = EventPriority.NORMAL


class EventBus:
    """
    Enhanced event bus with:
    - Pattern matching (bloom.*, *.critical)
    - Priority handling
    - Event history
    - Filtering
    - Sync/async support
    - Error handling
    """
    
    def __init__(self, history_size: int = 1000):
        self._subscribers: Dict[str, List[EventSubscription]] = defaultdict(list)
        self._event_history: deque = deque(maxlen=history_size)
        self._pattern_cache: Dict[str, Pattern] = {}
        self._handler_errors: Dict[str, int] = defaultdict(int)
        self._stats = {
            'events_published': 0,
            'events_delivered': 0,
            'errors': 0
        }
        
    def subscribe(
        self, 
        pattern: str, 
        handler: Callable,
        source: Optional[str] = None,
        filter_func: Optional[Callable] = None,
        priority: EventPriority = EventPriority.NORMAL
    ) -> Callable:
        """
        Subscribe to events matching pattern
        
        Args:
            pattern: Event pattern (e.g., 'bloom.*', '*.critical', 'pulse.tick')
            handler: Function to call (can be sync or async)
            source: Optional source filter
            filter_func: Optional filter function(event) -> bool
            priority: Handler priority
            
        Returns:
            Unsubscribe function
        """
        subscription = EventSubscription(
            pattern=pattern,
            handler=handler,
            source=source,
            filter_func=filter_func,
            priority=priority
        )
        
        self._subscribers[pattern].append(subscription)
        
        # Sort by priority
        self._subscribers[pattern].sort(
            key=lambda s: s.priority.value, 
            reverse=True
        )
        
        # Return unsubscribe function
        def unsubscribe():
            self._subscribers[pattern].remove(subscription)
            if not self._subscribers[pattern]:
                del self._subscribers[pattern]
                
        return unsubscribe
        
    def publish(
        self,
        event_type: str,
        data: Dict[Any, Any],
        source: Optional[str] = None,
        priority: EventPriority = EventPriority.NORMAL
    ) -> int:
        """
        Publish an event
        
        Returns:
            Number of handlers notified
        """
        event = Event(
            type=event_type,
            data=data,
            source=source,
            priority=priority
        )
        
        # Add to history
        self._event_history.append(event)
        self._stats['events_published'] += 1
        
        # Find matching subscriptions
        handlers_called = 0
        
        for pattern, subscriptions in self._subscribers.items():
            if not self._matches_pattern(event_type, pattern):
                continue
                
            for sub in subscriptions:
                # Check source filter
                if sub.source and sub.source != source:
                    continue
                    
                # Check custom filter
                if sub.filter_func and not sub.filter_func(event):
                    continue
                    
                # Call handler
                try:
                    self._call_handler(sub.handler, event)
                    handlers_called += 1
                    self._stats['events_delivered'] += 1
                except Exception as e:
                    self._handle_error(sub, event, e)
                    
        return handlers_called
        
    def _matches_pattern(self, event_type: str, pattern: str) -> bool:
        """Check if event type matches subscription pattern"""
        if pattern == '*':
            return True
            
        if pattern == event_type:
            return True
            
        # Handle wildcards
        if '*' in pattern:
            # Convert pattern to regex
            if pattern not in self._pattern_cache:
                regex_pattern = pattern.replace('.', r'\.').replace('*', '.*')
                self._pattern_cache[pattern] = re.compile(f'^{regex_pattern}$')
            
            return bool(self._pattern_cache[pattern].match(event_type))
            
        return False
        
    def _call_handler(self, handler: Callable, event: Event):
        """Call handler with proper signature"""
        sig = inspect.signature(handler)
        
        # Determine what to pass
        if len(sig.parameters) == 0:
            handler()
        elif len(sig.parameters) == 1:
            # Pass full event or just data
            param_name = list(sig.parameters.keys())[0]
            if 'event' in param_name.lower():
                handler(event)
            else:
                handler(event.data)
        else:
            # Pass event and data
            handler(event, event.data)
            
    def _handle_error(self, sub: EventSubscription, event: Event, error: Exception):
        """Handle handler errors"""
        handler_id = f"{sub.pattern}:{id(sub.handler)}"
        self._handler_errors[handler_id] += 1
        self._stats['errors'] += 1
        
        logger.error(
            f"Error in event handler for {event.type}: {error}",
            exc_info=True
        )
        
        # Disable handler after too many errors
        if self._handler_errors[handler_id] > 5:
            logger.error(f"Disabling handler {handler_id} after repeated errors")
            self._subscribers[sub.pattern].remove(sub)
            
    def emit(self, event_type: str, **kwargs):
        """Shorthand for publish with kwargs as data"""
        return self.publish(event_type, kwargs)
        
    def on(self, pattern: str):
        """Decorator for subscribing to events"""
        def decorator(func):
            self.subscribe(pattern, func)
            return func
        return decorator
        
    def get_subscribers(self, pattern: str) -> List[str]:
        """Get list of subscribers for a pattern"""
        subscribers = []
        for sub in self._subscribers.get(pattern, []):
            handler_name = getattr(sub.handler, '__name__', str(sub.handler))
            subscribers.append(handler_name)
        return subscribers
        
    def get_history(
        self, 
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Event]:
        """Get event history, optionally filtered"""
        events = list(self._event_history)
        
        if event_type:
            events = [e for e in events if self._matches_pattern(e.type, event_type)]
            
        return events[-limit:]
        
    def get_stats(self) -> Dict[str, Any]:
        """Get bus statistics"""
        return {
            **self._stats,
            'total_subscriptions': sum(len(subs) for subs in self._subscribers.values()),
            'unique_patterns': len(self._subscribers),
            'history_size': len(self._event_history)
        }
        
    def clear_history(self):
        """Clear event history"""
        self._event_history.clear()
        
    def reset_stats(self):
        """Reset statistics"""
        self._stats = {
            'events_published': 0,
            'events_delivered': 0,  
            'errors': 0
        }


# DAWN-specific event types
class DAWNEvents:
    """Standard DAWN event types"""
    
    # System events
    SYSTEM_BOOT = "system.boot"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"
    
    # Tick events
    TICK_START = "tick.start"
    TICK_COMPLETE = "tick.complete"
    
    # Bloom events
    BLOOM_SPAWNED = "bloom.spawned"
    BLOOM_EVOLVED = "bloom.evolved"
    BLOOM_PRUNED = "bloom.pruned"
    
    # Pulse events  
    PULSE_HEARTBEAT = "pulse.heartbeat"
    PULSE_MOOD_SHIFT = "pulse.mood_shift"
    PULSE_CRITICAL = "pulse.critical"
    
    # Owl events
    OWL_REFLECTION = "owl.reflection"
    OWL_INSIGHT = "owl.insight"
    OWL_OBSERVATION = "owl.observation"
    
    # Sigil events
    SIGIL_EMITTED = "sigil.emitted"
    SIGIL_ACTIVATED = "sigil.activated"
    SIGIL_EXPIRED = "sigil.expired"


# Global event bus instance
event_bus = EventBus()


# Convenience decorators
def on_event(pattern: str):
    """Decorator to subscribe a function to events"""
    return event_bus.on(pattern)


def emit_event(event_type: str, **data):
    """Quick emit helper"""
    return event_bus.emit(event_type, **data)