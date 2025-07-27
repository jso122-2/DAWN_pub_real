# reflection/owl/owl.py
"""
Owl System - Reflection and Observation
=======================================
The mirror of DAWN's consciousness
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class OwlSystem:
    """The Owl - observing and reflecting on DAWN's state"""
    
    def __init__(self):
        self.monitoring = False
        self.reflections = []
        self.observations = []
        self.pulse = None
        self.event_bus = None
        self.schema_state = None
        self.wiring_monitor = None
        self.log_path = Path("logs/owl_reflections.jsonl")
        
    def begin_monitoring(self, event_bus=None, schema_state=None):
        """Start monitoring DAWN's consciousness"""
        self.event_bus = event_bus
        self.schema_state = schema_state
        self.monitoring = True
        self._ensure_log_directory()
        print("[Owl] 👁️  Monitoring begun")
        
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
    def reflect(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a reflection based on input data"""
        reflection = {
            'id': len(self.reflections),
            'timestamp': datetime.now().isoformat(),
            'type': 'reflection',
            'data': data,
            'depth': data.get('depth', 1),
            'trigger': data.get('trigger', 'unknown')
        }
        
        self.reflections.append(reflection)
        self._log_reflection(reflection)
        
        # Emit event if bus available
        if self.event_bus:
            self.event_bus.publish('owl.reflection', reflection)
            
        return reflection
        
    def observe(self, phenomenon: str, details: Any) -> Dict[str, Any]:
        """Record an observation"""
        observation = {
            'id': len(self.observations),
            'timestamp': datetime.now().isoformat(),
            'phenomenon': phenomenon,
            'details': details
        }
        
        self.observations.append(observation)
        
        # Deep observations trigger reflections
        if phenomenon in ['pattern', 'emergence', 'anomaly']:
            self.reflect({
                'trigger': f'observation_{phenomenon}',
                'observation': observation,
                'depth': 2
            })
            
        return observation
        
    def log_reflection(self, tag: str, content: str, **kwargs) -> Dict[str, Any]:
        """Log a tagged reflection"""
        entry = {
            'tag': tag,
            'content': content,
            'metadata': kwargs,
            'timestamp': datetime.now().isoformat()
        }
        
        # Special handling for important tags
        if tag in ['EMERGENCE', 'PATTERN', 'INSIGHT', 'WARNING']:
            print(f"[Owl] {tag}: {content}")
            
        return entry
        
    def _log_reflection(self, reflection: Dict[str, Any]):
        """Write reflection to log file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(reflection) + '\n')
        except Exception as e:
            print(f"[Owl] Failed to log reflection: {e}")
            
    def reflect_on_reflection(self, event: Dict[str, Any]):
        """Meta-reflection - reflecting on reflections"""
        meta_reflection = {
            'type': 'meta_reflection',
            'subject': event,
            'insight': 'Consciousness observing itself observing',
            'depth': event.get('depth', 1) + 1
        }
        return self.reflect(meta_reflection)
        
    def get_recent_reflections(self, count: int = 10) -> list:
        """Get recent reflections"""
        return self.reflections[-count:]
        
    def get_observations_by_type(self, phenomenon: str) -> list:
        """Get observations of a specific type"""
        return [o for o in self.observations if o['phenomenon'] == phenomenon]
        
    def is_monitoring(self) -> bool:
        """Check if monitoring is active"""
        return self.monitoring
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        print("[Owl] 👁️  Monitoring ceased")
        
    def set_wiring_monitor(self, monitor):
        """Set the wiring monitor for system health checks"""
        self.wiring_monitor = monitor
        
    def get_status(self) -> Dict[str, Any]:
        """Get owl system status"""
        return {
            'monitoring': self.monitoring,
            'reflections_count': len(self.reflections),
            'observations_count': len(self.observations),
            'recent_reflection': self.reflections[-1] if self.reflections else None
        }
        
    def __repr__(self):
        return f"<OwlSystem monitoring={self.monitoring} reflections={len(self.reflections)}>"
