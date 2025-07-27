"""
Optimized statistical operations for fallback memory routing.
Uses NumPy for efficient calculations and implements streaming statistics.
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

class FallbackStatistics:
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.coherence_buffer = np.zeros(window_size)
        self.entropy_buffer = np.zeros(window_size)
        self.buffer_index = 0
        self.buffer_filled = False
        
        # Exponential Moving Average parameters
        self.alpha = 0.1  # Smoothing factor
        self.ema_coherence = 0.0
        self.ema_entropy = 0.0
        
        # Initialize counters
        self.reason_counts = {}
        self.severity_counts = {
            "CRITICAL": 0, "HIGH": 0, 
            "MODERATE": 0, "LOW": 0
        }
        
    def update_streaming_stats(self, coherence: float, entropy: float):
        """Update streaming statistics with new values."""
        # Update circular buffer
        self.coherence_buffer[self.buffer_index] = coherence
        self.entropy_buffer[self.buffer_index] = entropy
        self.buffer_index = (self.buffer_index + 1) % self.window_size
        if self.buffer_index == 0:
            self.buffer_filled = True
            
        # Update EMA
        self.ema_coherence = (self.alpha * coherence + 
                            (1 - self.alpha) * self.ema_coherence)
        self.ema_entropy = (self.alpha * entropy + 
                          (1 - self.alpha) * self.ema_entropy)
    
    def get_current_stats(self) -> Dict:
        """Get current statistical measures."""
        if not self.buffer_filled and self.buffer_index == 0:
            return {
                "mean_coherence": 0.0,
                "mean_entropy": 0.0,
                "std_coherence": 0.0,
                "std_entropy": 0.0,
                "ema_coherence": self.ema_coherence,
                "ema_entropy": self.ema_entropy
            }
            
        # Calculate statistics only on filled portion of buffer
        end_idx = self.window_size if self.buffer_filled else self.buffer_index
        coherence_data = self.coherence_buffer[:end_idx]
        entropy_data = self.entropy_buffer[:end_idx]
        
        return {
            "mean_coherence": float(np.mean(coherence_data)),
            "mean_entropy": float(np.mean(entropy_data)),
            "std_coherence": float(np.std(coherence_data)),
            "std_entropy": float(np.std(entropy_data)),
            "ema_coherence": self.ema_coherence,
            "ema_entropy": self.ema_entropy
        }
    
    def update_reason_counts(self, reason: str):
        """Update reason frequency counts."""
        for r in reason.split(" | "):
            reason_type = r.split(":")[0] if ":" in r else r
            self.reason_counts[reason_type] = self.reason_counts.get(reason_type, 0) + 1
    
    def update_severity_counts(self, severity: str):
        """Update severity frequency counts."""
        if severity in self.severity_counts:
            self.severity_counts[severity] += 1
    
    def calculate_mtbf(self, first_trigger: str, last_trigger: str, 
                      total_triggers: int) -> float:
        """Calculate Mean Time Between Failures in hours."""
        if not first_trigger or not last_trigger or total_triggers <= 1:
            return 0.0
            
        first_dt = datetime.fromisoformat(first_trigger)
        last_dt = datetime.fromisoformat(last_trigger)
        total_hours = (last_dt - first_dt).total_seconds() / 3600
        return total_hours / (total_triggers - 1)
    
    def get_reason_distribution(self) -> Dict[str, int]:
        """Get current reason distribution."""
        return self.reason_counts
    
    def get_severity_distribution(self) -> Dict[str, int]:
        """Get current severity distribution."""
        return self.severity_counts
    
    def get_most_common_reason(self) -> str:
        """Get most frequently occurring reason."""
        if not self.reason_counts:
            return "none"
        return max(self.reason_counts.items(), key=lambda x: x[1])[0] 