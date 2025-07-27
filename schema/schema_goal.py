"""
DAWN Schema Goal System
Implements DAWN's goal tracking and proximity monitoring system.
"""

import sys, os
import json
import time
from typing import Dict, List, Optional, Callable, Union, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class GoalStatus(Enum):
    """Status of schema goals."""
    ACTIVE = "active"
    ACHIEVED = "achieved"
    PAUSED = "paused"
    FAILED = "failed"
    ABANDONED = "abandoned"

class GoalPriority(Enum):
    """Priority levels for goals."""
    CRITICAL = "critical"      # System stability goals
    HIGH = "high"             # Important operational goals
    MEDIUM = "medium"         # Development goals
    LOW = "low"              # Exploratory goals

class GoalSource(Enum):
    """Source of goal creation."""
    INTERNAL = "internal"     # Self-generated goals
    EXTERNAL = "external"     # User-specified goals
    SYSTEM = "system"        # System-generated goals
    EMERGENT = "emergent"    # Goals emerging from experience

@dataclass
class GoalMetric:
    """A measurable metric for goal tracking."""
    name: str
    target_value: float
    current_value: float = 0.0
    tolerance: float = 0.1  # Acceptable range around target
    weight: float = 1.0     # Importance weight
    getter_func: Optional[Callable] = None  # Function to get current value
    
    def get_proximity(self) -> float:
        """Calculate proximity to target (1.0 = achieved, 0.0 = far)."""
        if self.target_value == 0:
            return 1.0 if abs(self.current_value) <= self.tolerance else 0.0
        
        distance = abs(self.current_value - self.target_value)
        max_distance = abs(self.target_value) + 1.0  # Prevent division by zero
        proximity = max(0.0, 1.0 - (distance / max_distance))
        
        return proximity
    
    def is_achieved(self) -> bool:
        """Check if metric is within tolerance of target."""
        return abs(self.current_value - self.target_value) <= self.tolerance
    
    def update_current_value(self):
        """Update current value using getter function if available."""
        if self.getter_func:
            try:
                self.current_value = self.getter_func()
            except Exception as e:
                print(f"[SchemaGoal] ⚠️ Error updating metric {self.name}: {e}")

@dataclass
class SchemaGoal:
    """A schema goal with multiple metrics and tracking."""
    id: str
    name: str
    description: str
    metrics: List[GoalMetric]
    priority: GoalPriority
    source: GoalSource
    status: GoalStatus = GoalStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    target_date: Optional[datetime] = None
    
    # Tracking data
    proximity_history: List[Tuple[datetime, float]] = field(default_factory=list)
    achievement_threshold: float = 0.85  # Proximity needed to consider achieved
    persistence_required: int = 3  # Ticks goal must stay achieved
    achievement_streak: int = 0
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    last_updated: datetime = field(default_factory=datetime.utcnow)
    
    def calculate_proximity(self) -> float:
        """Calculate overall proximity to goal achievement."""
        if not self.metrics:
            return 0.0
        
        # Update all metric values
        for metric in self.metrics:
            metric.update_current_value()
        
        # Weighted average of metric proximities
        total_weight = sum(metric.weight for metric in self.metrics)
        if total_weight == 0:
            return 0.0
        
        weighted_proximity = sum(
            metric.get_proximity() * metric.weight 
            for metric in self.metrics
        ) / total_weight
        
        # Record in history
        self.proximity_history.append((datetime.utcnow(), weighted_proximity))
        
        # Keep history manageable
        if len(self.proximity_history) > 1000:
            self.proximity_history = self.proximity_history[-500:]
        
        self.last_updated = datetime.utcnow()
        
        return weighted_proximity
    
    def is_achieved(self) -> bool:
        """Check if goal is achieved based on proximity threshold."""
        proximity = self.calculate_proximity()
        
        if proximity >= self.achievement_threshold:
            self.achievement_streak += 1
            return self.achievement_streak >= self.persistence_required
        else:
            self.achievement_streak = 0
            return False
    
    def get_blocking_metrics(self) -> List[GoalMetric]:
        """Get metrics that are preventing goal achievement."""
        blocking = []
        
        for metric in self.metrics:
            metric.update_current_value()
            if not metric.is_achieved():
                blocking.append(metric)
        
        return blocking
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get comprehensive progress summary."""
        proximity = self.calculate_proximity()
        blocking_metrics = self.get_blocking_metrics()
        
        return {
            'goal_id': self.id,
            'name': self.name,
            'proximity': proximity,
            'status': self.status.value,
            'priority': self.priority.value,
            'is_achieved': self.is_achieved(),
            'achievement_streak': self.achievement_streak,
            'blocking_metrics': len(blocking_metrics),
            'blocking_details': [
                {
                    'name': metric.name,
                    'current': metric.current_value,
                    'target': metric.target_value,
                    'proximity': metric.get_proximity()
                }
                for metric in blocking_metrics
            ],
            'days_active': (datetime.utcnow() - self.created_at).days,
            'last_updated': self.last_updated.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'metrics': [
                {
                    'name': m.name,
                    'target_value': m.target_value,
                    'current_value': m.current_value,
                    'tolerance': m.tolerance,
                    'weight': m.weight
                }
                for m in self.metrics
            ],
            'priority': self.priority.value,
            'source': self.source.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'achievement_threshold': self.achievement_threshold,
            'persistence_required': self.persistence_required,
            'achievement_streak': self.achievement_streak,
            'tags': self.tags,
            'notes': self.notes,
            'last_updated': self.last_updated.isoformat(),
            'proximity_history': [
                [ts.isoformat(), prox] for ts, prox in self.proximity_history[-50:]
            ]  # Keep recent history only
        }

class SchemaGoalSystem:
    """
    Comprehensive goal tracking system for DAWN.
    
    Manages goal creation, tracking, achievement detection, and provides
    insights into DAWN's progress toward various objectives.
    """
    
    def __init__(self, goals_dir: str = "dawn_goals"):
        self.goals_dir = Path(goals_dir)
        self.goals_dir.mkdir(exist_ok=True)
        
        # Goal storage
        self.goals: Dict[str, SchemaGoal] = {}
        self.active_goals: Dict[str, SchemaGoal] = {}
        
        # System configuration
        self.auto_update_interval = 30  # seconds
        self.last_auto_update = time.time()
        
        # Metric getter registry
        self.metric_getters: Dict[str, Callable] = {}
        
        # Achievement callbacks
        self.achievement_callbacks: List[Callable] = []
        self.failure_callbacks: List[Callable] = []
        
        # Initialize default metric getters
        self._register_default_metrics()
        
        # Load existing goals
        self._load_goals()
        
        print(f"[SchemaGoal] 🎯 Goal system initialized with {len(self.goals)} goals")
