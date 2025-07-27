from typing import Dict, Any, List
import numpy as np
from datetime import datetime

class PatternDetector:
    def __init__(self):
        self.patterns = []
        self.detection_threshold = 0.7
        self.max_patterns = 100
        self.last_update = datetime.now()
    
    def detect_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect patterns in the input data"""
        # Basic pattern detection logic
        patterns = []
        
        # Example: Detect SCUP patterns
        if 'scup' in data:
            scup_value = data['scup']
            if scup_value > self.detection_threshold:
                patterns.append({
                    'type': 'scup_spike',
                    'value': scup_value,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Example: Detect entropy patterns
        if 'entropy' in data:
            entropy_value = data['entropy']
            if entropy_value > self.detection_threshold:
                patterns.append({
                    'type': 'entropy_spike',
                    'value': entropy_value,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Update stored patterns
        self.patterns.extend(patterns)
        if len(self.patterns) > self.max_patterns:
            self.patterns = self.patterns[-self.max_patterns:]
        
        self.last_update = datetime.now()
        return patterns
    
    def get_patterns(self) -> List[Dict[str, Any]]:
        """Get all detected patterns"""
        return self.patterns
    
    def clear_patterns(self) -> None:
        """Clear all stored patterns"""
        self.patterns = []
    
    def set_threshold(self, threshold: float) -> None:
        """Set the pattern detection threshold"""
        self.detection_threshold = max(0.0, min(1.0, threshold))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get pattern detector metrics"""
        return {
            'pattern_count': len(self.patterns),
            'threshold': self.detection_threshold,
            'last_update': self.last_update.isoformat()
        }

def create_pattern_detector() -> PatternDetector:
    """Create and return a new pattern detector instance"""
    return PatternDetector() 