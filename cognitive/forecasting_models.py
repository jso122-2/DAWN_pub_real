"""
DAWN Forecasting Models - Passion, Acquaintance, and Forecast Vectors
Core data models for behavioral prediction and intent gravity calculations.
Integrated into DAWN's cognitive consciousness system.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import math
import logging

logger = logging.getLogger(__name__)


class Passion:
    """
    Represents a directional desire or drive with intensity and fluidity.
    Forms the numerator (P) in the intent gravity equation F = P / A.
    """
    
    def __init__(self, direction: str, intensity: float, fluidity: float):
        """
        Initialize a passion vector.
        
        Args:
            direction: String or concept tag describing the passion's direction
            intensity: Float (0-1) representing passion strength
            fluidity: Float (0-1) representing how easily the passion shifts
                     (high fluidity = easily changed, low = rigid)
        """
        self.direction = direction
        self.intensity = max(0.0, min(1.0, intensity))  # Clamp to [0,1]
        self.fluidity = max(0.0, min(1.0, fluidity))    # Clamp to [0,1]
        
        # Metadata
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
        self.activation_count = 0
    
    def rigidity_score(self) -> float:
        """
        Calculate the rigidity score of this passion.
        Higher rigidity = stronger behavioral prediction power.
        
        Formula: intensity * (1 - fluidity)
        
        Returns:
            float: Rigidity score (0-1), used as P in F = P / A
        """
        return self.intensity * (1.0 - self.fluidity)
    
    def stability_index(self) -> float:
        """
        Calculate how stable this passion is over time.
        Combines intensity and inverse fluidity.
        
        Returns:
            float: Stability index (0-1)
        """
        return (self.intensity + (1.0 - self.fluidity)) / 2.0
    
    def modulate_intensity(self, delta: float) -> None:
        """
        Adjust passion intensity by delta amount.
        
        Args:
            delta: Change in intensity (-1 to +1)
        """
        old_intensity = self.intensity
        self.intensity = max(0.0, min(1.0, self.intensity + delta))
        self.last_modified = datetime.now()
        
        if abs(delta) > 0.01:  # Significant change
            self.activation_count += 1
    
    def decay(self, decay_rate: float = 0.01) -> None:
        """
        Apply natural decay to passion intensity over time.
        
        Args:
            decay_rate: Rate of intensity decay (0-1)
        """
        self.intensity *= (1.0 - decay_rate)
        if self.intensity < 0.001:  # Prevent infinite tiny values
            self.intensity = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert passion to dictionary for serialization."""
        return {
            'direction': self.direction,
            'intensity': self.intensity,
            'fluidity': self.fluidity,
            'rigidity_score': self.rigidity_score(),
            'stability_index': self.stability_index(),
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'activation_count': self.activation_count
        }
    
    def __str__(self) -> str:
        return f"Passion({self.direction}, I={self.intensity:.2f}, F={self.fluidity:.2f}, R={self.rigidity_score():.2f})"
    
    def __repr__(self) -> str:
        return f"Passion(direction='{self.direction}', intensity={self.intensity}, fluidity={self.fluidity})"


class Acquaintance:
    """
    Represents accumulated experience and reinforcement patterns.
    Forms the denominator (A) in the intent gravity equation F = P / A.
    """
    
    def __init__(self, event_log: Optional[List[str]] = None):
        """
        Initialize an acquaintance with optional event history.
        
        Args:
            event_log: List of timestamped reinforcements (strings or tags)
        """
        self.event_log = event_log or []
        self.created_at = datetime.now()
        self.last_event = None
        self.event_weights = {}  # For weighted reinforcement scoring
    
    def add_event(self, event: str, weight: float = 1.0, timestamp: Optional[datetime] = None) -> None:
        """
        Add a reinforcement event to the log.
        
        Args:
            event: Event description or tag
            weight: Importance weight of the event (default 1.0)
            timestamp: When the event occurred (default now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Store event with timestamp
        timestamped_event = f"{timestamp.isoformat()}:{event}"
        self.event_log.append(timestamped_event)
        self.event_weights[timestamped_event] = weight
        self.last_event = timestamp
    
    def reinforcement_score(self, decay_factor: float = 0.1) -> float:
        """
        Calculate reinforcement score based on event history.
        More recent events have higher weight.
        
        Args:
            decay_factor: How much older events decay (0-1)
            
        Returns:
            float: Reinforcement score (≥0)
        """
        if not self.event_log:
            return 0.0
        
        now = datetime.now()
        total_score = 0.0
        
        for event in self.event_log:
            # Parse timestamp from event
            try:
                timestamp_str = event.split(':', 1)[0]
                event_time = datetime.fromisoformat(timestamp_str)
            except (ValueError, IndexError):
                # Fallback for simple events without timestamps
                event_time = self.created_at
            
            # Calculate time-based decay
            time_diff = (now - event_time).total_seconds() / 3600  # Hours
            decay_multiplier = math.exp(-decay_factor * time_diff)
            
            # Get event weight
            event_weight = self.event_weights.get(event, 1.0)
            
            total_score += event_weight * decay_multiplier
        
        return total_score
    
    def recent_activity(self, hours: int = 24) -> int:
        """
        Count events within the last N hours.
        
        Args:
            hours: Time window to check (default 24 hours)
            
        Returns:
            int: Number of recent events
        """
        if not self.event_log:
            return 0
        
        now = datetime.now()
        cutoff = now.timestamp() - (hours * 3600)
        recent_count = 0
        
        for event in self.event_log:
            try:
                timestamp_str = event.split(':', 1)[0]
                event_time = datetime.fromisoformat(timestamp_str)
                if event_time.timestamp() > cutoff:
                    recent_count += 1
            except (ValueError, IndexError):
                continue
        
        return recent_count
    
    def get_event_frequency(self) -> Dict[str, int]:
        """
        Analyze frequency of different event types.
        
        Returns:
            dict: Event type frequencies
        """
        frequency = {}
        
        for event in self.event_log:
            # Extract event type (after timestamp)
            try:
                event_type = event.split(':', 1)[1]
                frequency[event_type] = frequency.get(event_type, 0) + 1
            except IndexError:
                frequency[event] = frequency.get(event, 0) + 1
        
        return frequency
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert acquaintance to dictionary for serialization."""
        return {
            'event_log': self.event_log,
            'event_weights': self.event_weights,
            'reinforcement_score': self.reinforcement_score(),
            'total_events': len(self.event_log),
            'recent_activity_24h': self.recent_activity(24),
            'event_frequency': self.get_event_frequency(),
            'created_at': self.created_at.isoformat(),
            'last_event': self.last_event.isoformat() if self.last_event else None
        }
    
    def __str__(self) -> str:
        return f"Acquaintance({len(self.event_log)} events, R={self.reinforcement_score():.2f})"
    
    def __repr__(self) -> str:
        return f"Acquaintance(events={len(self.event_log)}, score={self.reinforcement_score():.2f})"


@dataclass
class ForecastVector:
    """
    Represents a behavioral prediction with confidence and risk assessment.
    Output of the intent gravity calculation F = P / A.
    """
    predicted_behavior: str
    confidence: float
    risk: Optional[Union[str, float]] = None
    
    # Additional metadata
    passion_direction: Optional[str] = None
    forecast_horizon: Optional[str] = None  # "short", "medium", "long"
    entropy_factor: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate and set defaults after initialization."""
        # Clamp confidence to [0,1]
        self.confidence = max(0.0, min(1.0, self.confidence))
        
        # Set timestamp if not provided
        if self.timestamp is None:
            self.timestamp = datetime.now()
        
        # Determine forecast horizon based on confidence
        if self.forecast_horizon is None:
            if self.confidence > 0.8:
                self.forecast_horizon = "short"
            elif self.confidence > 0.5:
                self.forecast_horizon = "medium"
            else:
                self.forecast_horizon = "long"
    
    def risk_level(self) -> str:
        """
        Determine risk level based on confidence and risk value.
        
        Returns:
            str: Risk level ("low", "medium", "high", "critical")
        """
        if isinstance(self.risk, str):
            return self.risk.lower()
        
        if isinstance(self.risk, (int, float)):
            if self.risk < 0.2:
                return "low"
            elif self.risk < 0.5:
                return "medium"
            elif self.risk < 0.8:
                return "high"
            else:
                return "critical"
        
        # Default based on inverse confidence
        inverse_confidence = 1.0 - self.confidence
        if inverse_confidence < 0.3:
            return "low"
        elif inverse_confidence < 0.6:
            return "medium"
        else:
            return "high"
    
    def certainty_band(self) -> str:
        """
        Get human-readable certainty description.
        
        Returns:
            str: Certainty level description
        """
        if self.confidence > 0.9:
            return "very high certainty"
        elif self.confidence > 0.7:
            return "high certainty"
        elif self.confidence > 0.5:
            return "moderate certainty"
        elif self.confidence > 0.3:
            return "low certainty"
        else:
            return "very low certainty"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert forecast vector to dictionary for serialization."""
        return {
            'predicted_behavior': self.predicted_behavior,
            'confidence': self.confidence,
            'risk': self.risk,
            'risk_level': self.risk_level(),
            'certainty_band': self.certainty_band(),
            'passion_direction': self.passion_direction,
            'forecast_horizon': self.forecast_horizon,
            'entropy_factor': self.entropy_factor,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __str__(self) -> str:
        return f"ForecastVector({self.predicted_behavior}, confidence={self.confidence:.2f}, {self.certainty_band()})"


# Utility functions for model creation and manipulation
def create_passion(direction: str, intensity: float, fluidity: float = 0.5) -> Passion:
    """Factory function for creating passion objects."""
    return Passion(direction, intensity, fluidity)


def create_acquaintance_with_events(events: List[str]) -> Acquaintance:
    """Factory function for creating acquaintance with event history."""
    acquaintance = Acquaintance()
    for event in events:
        acquaintance.add_event(event)
    return acquaintance


# DAWN integration utilities
def passion_from_consciousness_state(consciousness_state: Dict[str, Any], direction: str) -> Passion:
    """
    Create a passion from DAWN's consciousness state.
    
    Args:
        consciousness_state: DAWN consciousness data
        direction: Passion direction to create
        
    Returns:
        Passion: Created passion based on consciousness
    """
    # Map SCUP to intensity
    scup = consciousness_state.get('scup', 0.5)
    intensity = scup / 100.0 if scup > 1 else scup
    
    # Map entropy to fluidity
    entropy = consciousness_state.get('entropy', 0.5)
    fluidity = entropy if entropy <= 1 else min(entropy / 1000000.0, 1.0)
    
    return create_passion(direction, intensity, fluidity)


def acquaintance_from_dawn_memory(memory_fragments: List[Dict], filter_direction: Optional[str] = None) -> Acquaintance:
    """
    Create an acquaintance from DAWN's memory fragments.
    
    Args:
        memory_fragments: List of memory fragments from DAWN
        filter_direction: Optional filter for direction-related memories
        
    Returns:
        Acquaintance: Created acquaintance from memories
    """
    acquaintance = Acquaintance()
    
    for fragment in memory_fragments:
        # Filter by direction if specified
        if filter_direction and filter_direction.lower() not in fragment.get('content', '').lower():
            continue
            
        # Extract event details
        event_content = fragment.get('content', 'memory_event')
        weight = fragment.get('strength', 1.0)
        timestamp = fragment.get('timestamp')
        
        # Convert timestamp if needed
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                timestamp = None
        
        acquaintance.add_event(event_content, weight, timestamp)
    
    return acquaintance 