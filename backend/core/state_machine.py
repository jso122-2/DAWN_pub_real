from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import numpy as np
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)

class SystemState(Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    RECOVERING = "recovering"
    OPTIMIZING = "optimizing"
    LEARNING = "learning"

class StateTransition:
    def __init__(self, from_state: SystemState, to_state: SystemState, 
                 condition: Optional[Callable[[], bool]] = None,
                 action: Optional[Callable[[], None]] = None):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.action = action

class StateMachine:
    def __init__(self):
        self.current_state = SystemState.INITIALIZING
        self.previous_state = None
        self.state_history = []
        self.max_history = 100
        self.last_update = datetime.now()
        self.state_metrics = {state: {} for state in SystemState}
        self.transition_handlers = {}
        self.state_handlers = {}
        self.error_count = 0
        self.max_errors = 3
        self.recovery_attempts = 0
        self.max_recovery_attempts = 5
        
        # Initialize state transitions
        self.transitions = {
            SystemState.INITIALIZING: [
                StateTransition(SystemState.INITIALIZING, SystemState.READY),
                StateTransition(SystemState.INITIALIZING, SystemState.ERROR)
            ],
            SystemState.READY: [
                StateTransition(SystemState.READY, SystemState.RUNNING),
                StateTransition(SystemState.READY, SystemState.OPTIMIZING),
                StateTransition(SystemState.READY, SystemState.ERROR)
            ],
            SystemState.RUNNING: [
                StateTransition(SystemState.RUNNING, SystemState.PAUSED),
                StateTransition(SystemState.RUNNING, SystemState.STOPPED),
                StateTransition(SystemState.RUNNING, SystemState.LEARNING),
                StateTransition(SystemState.RUNNING, SystemState.ERROR)
            ],
            SystemState.PAUSED: [
                StateTransition(SystemState.PAUSED, SystemState.RUNNING),
                StateTransition(SystemState.PAUSED, SystemState.STOPPED),
                StateTransition(SystemState.PAUSED, SystemState.ERROR)
            ],
            SystemState.STOPPED: [
                StateTransition(SystemState.STOPPED, SystemState.READY),
                StateTransition(SystemState.STOPPED, SystemState.ERROR)
            ],
            SystemState.ERROR: [
                StateTransition(SystemState.ERROR, SystemState.RECOVERING),
                StateTransition(SystemState.ERROR, SystemState.STOPPED)
            ],
            SystemState.RECOVERING: [
                StateTransition(SystemState.RECOVERING, SystemState.READY),
                StateTransition(SystemState.RECOVERING, SystemState.ERROR)
            ],
            SystemState.OPTIMIZING: [
                StateTransition(SystemState.OPTIMIZING, SystemState.READY),
                StateTransition(SystemState.OPTIMIZING, SystemState.ERROR)
            ],
            SystemState.LEARNING: [
                StateTransition(SystemState.LEARNING, SystemState.RUNNING),
                StateTransition(SystemState.LEARNING, SystemState.ERROR)
            ]
        }
    
    async def transition_to(self, new_state: SystemState) -> bool:
        """Attempt to transition to a new state asynchronously"""
        if new_state not in SystemState:
            logger.error(f"Invalid state: {new_state}")
            return False
        
        # Check if transition is allowed
        allowed_transitions = self.transitions[self.current_state]
        if not any(t.to_state == new_state for t in allowed_transitions):
            logger.error(f"Invalid transition from {self.current_state} to {new_state}")
            return False
        
        # Execute transition handlers
        transition_key = (self.current_state, new_state)
        if transition_key in self.transition_handlers:
            try:
                await self.transition_handlers[transition_key]()
            except Exception as e:
                logger.error(f"Transition handler failed: {e}")
                return False
        
        # Update state
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # Record transition
        self.state_history.append({
            "from": self.previous_state.value,
            "to": new_state.value,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        # Execute state handler
        if new_state in self.state_handlers:
            try:
                await self.state_handlers[new_state]()
            except Exception as e:
                logger.error(f"State handler failed: {e}")
                if new_state == SystemState.ERROR:
                    self.error_count += 1
                return False
        
        self.last_update = datetime.now()
        return True
    
    def register_transition_handler(self, from_state: SystemState, to_state: SystemState, 
                                  handler: Callable[[], None]) -> None:
        """Register a handler for a specific state transition"""
        self.transition_handlers[(from_state, to_state)] = handler
    
    def register_state_handler(self, state: SystemState, handler: Callable[[], None]) -> None:
        """Register a handler for a specific state"""
        self.state_handlers[state] = handler
    
    def get_current_state(self) -> SystemState:
        """Get the current state"""
        return self.current_state
    
    def get_state_history(self) -> List[Dict[str, Any]]:
        """Get the state transition history"""
        return self.state_history
    
    def get_available_transitions(self) -> List[SystemState]:
        """Get available transitions from current state"""
        return [t.to_state for t in self.transitions[self.current_state]]
    
    def update_state_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update metrics for current state"""
        self.state_metrics[self.current_state].update(metrics)
        self.last_update = datetime.now()
    
    def get_state_metrics(self) -> Dict[str, Any]:
        """Get metrics for current state"""
        return self.state_metrics[self.current_state]
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all state metrics"""
        return {
            state.value: metrics
            for state, metrics in self.state_metrics.items()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get state machine metrics"""
        return {
            'current_state': self.current_state.value,
            'previous_state': self.previous_state.value if self.previous_state else None,
            'available_transitions': [s.value for s in self.get_available_transitions()],
            'state_metrics': self.get_state_metrics(),
            'history_length': len(self.state_history),
            'error_count': self.error_count,
            'recovery_attempts': self.recovery_attempts,
            'last_update': self.last_update.isoformat()
        }

def create_state_machine() -> StateMachine:
    """Create and return a new state machine instance"""
    return StateMachine() 