"""
Signal bus for DAWN tick engine
"""

import asyncio
import logging
from typing import Dict, List, Callable, Any
from collections import defaultdict
from ...async_utils import run_maybe_async

logger = logging.getLogger(__name__)

# Signal handlers
_handlers: Dict[str, List[Callable]] = defaultdict(list)

# Signal state
_signals: Dict[str, Any] = {}

def emit_signal(name: str, data: dict = None):
    """Emit a signal to all registered handlers."""
    if data is None:
        data = {}
    
    for handler in _handlers.get(name, []):
        asyncio.create_task(run_maybe_async(handler, name, data))

def listen_signal(name: str, handler: Callable) -> None:
    """Register a handler for a signal"""
    logger.debug(f"Registering handler for signal: {name}")
    _handlers[name].append(handler)

def unlisten_signal(name: str, handler: Callable) -> None:
    """Remove a handler for a signal"""
    if name in _handlers:
        try:
            _handlers[name].remove(handler)
            logger.debug(f"Removed handler for signal: {name}")
        except ValueError:
            pass

def set_signal(name: str, value: Any) -> None:
    """Set a signal value"""
    logger.debug(f"Setting signal {name} = {value}")
    _signals[name] = value

def get_signal(name: str, default: Any = None) -> Any:
    """Get a signal value"""
    return _signals.get(name, default)

def clear_signal(name: str) -> None:
    """Clear a signal value"""
    if name in _signals:
        del _signals[name]

def clear_handlers(name: str) -> None:
    """Clear all handlers for a signal"""
    if name in _handlers:
        del _handlers[name] 