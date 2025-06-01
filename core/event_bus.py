# event_bus.py

import asyncio
from collections import defaultdict
from typing import Callable, Coroutine, Dict, List, Type

class Event:
    """Base class for all events."""
    pass

class TickEvent(Event):
    pass

class SigilExpired(Event):
    pass

class BloomEmitted(Event):
    pass

class EventBus:
    def __init__(self):
        self.subscribers: Dict[Type[Event], List[Callable[[Event], Coroutine]]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Callable[[Event], Coroutine]):
        """Register a handler to an event type."""
        self.subscribers[event_type].append(handler)

    async def publish(self, event: Event):
        """Broadcast an event to all matching subscribers."""
        for handler in self.subscribers[type(event)]:
            await handler(event)

# Singleton bus for global use
event_bus = EventBus()
