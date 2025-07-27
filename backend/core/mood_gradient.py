from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from datetime import datetime
import math
from scipy import signal
from scipy.stats import entropy
from scipy.interpolate import interp1d

class MoodPoint:
    def __init__(self, value: float, timestamp: Optional[datetime] = None):
        self.value = value
        self.timestamp = timestamp or datetime.now()
        self.velocity = 0.0
        self.acceleration = 0.0
        self.volatility = 0.0

class MoodGradientPlotter:
    def __init__(self, window_size: int = 100):
        self.mood_history = []
        self.window_size = window_size
        self.last_update = datetime.now()
        self.gradient_history = []
        self.volatility_history = []
        self.velocity_history = []
        self.acceleration_history = []
        self.mood_stats = {
            'mean': 0.0,
            'std': 0.0,
            'min': 0.0,
            'max': 0.0,
            'entropy': 0.0
        }
        self.gradient_stats = {
            'mean': 0.0,
            'std': 0.0,
            'trend': 0.0
        }
    
    def _calculate_velocity(self, points: List[MoodPoint]) -> List[float]:
        """Calculate mood velocity"""
        if len(points) < 2:
            return [0.0]
        
        velocities = []
        for i in range(1, len(points)):
            time_diff = (points[i].timestamp - points[i-1].timestamp).total_seconds()
            if time_diff > 0:
                velocity = (points[i].value - points[i-1].value) / time_diff
            else:
                velocity = 0.0
            velocities.append(velocity)
            points[i].velocity = velocity
        
        return velocities
    
    def _calculate_acceleration(self, points: List[MoodPoint]) -> List[float]:
        """Calculate mood acceleration"""
        if len(points) < 3:
            return [0.0]
        
        accelerations = []
        for i in range(2, len(points)):
            time_diff = (points[i].timestamp - points[i-1].timestamp).total_seconds()
            if time_diff > 0:
                acceleration = (points[i].velocity - points[i-1].velocity) / time_diff
            else:
                acceleration = 0.0
            accelerations.append(acceleration)
            points[i].acceleration = acceleration
        
        return accelerations
    
    def _calculate_volatility(self, points: List[MoodPoint], window: int = 10) -> List[float]:
        """Calculate mood volatility using rolling standard deviation"""
        if len(points) < window:
            return [0.0] * len(points)
        
        volatilities = []
        for i in range(len(points)):
            start_idx = max(0, i - window + 1)
            window_points = points[start_idx:i+1]
            if window_points:
                volatility = np.std([p.value for p in window_points])
            else:
                volatility = 0.0
            volatilities.append(volatility)
            points[i].volatility = volatility
        
        return volatilities
    
    def _update_stats(self) -> None:
        """Update mood and gradient statistics"""
        if not self.mood_history:
            return
        
        values = [p.value for p in self.mood_history]
        self.mood_stats.update({
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'entropy': float(entropy(np.histogram(values, bins=20)[0]))
        })
        
        if self.gradient_history:
            gradients = [g for g in self.gradient_history]
            self.gradient_stats.update({
                'mean': float(np.mean(gradients)),
                'std': float(np.std(gradients)),
                'trend': float(np.polyfit(range(len(gradients)), gradients, 1)[0])
            })
    
    def add_mood_point(self, value: float, timestamp: Optional[datetime] = None) -> None:
        """Add a new mood data point"""
        point = MoodPoint(value, timestamp)
        self.mood_history.append(point)
        
        if len(self.mood_history) > self.window_size:
            self.mood_history.pop(0)
        
        # Calculate derivatives
        velocities = self._calculate_velocity(self.mood_history)
        accelerations = self._calculate_acceleration(self.mood_history)
        volatilities = self._calculate_volatility(self.mood_history)
        
        # Update histories
        self.velocity_history = velocities
        self.acceleration_history = accelerations
        self.volatility_history = volatilities
        
        # Calculate gradient
        if len(velocities) > 0:
            gradient = velocities[-1]
            self.gradient_history.append(gradient)
            if len(self.gradient_history) > self.window_size:
                self.gradient_history.pop(0)
        
        self._update_stats()
        self.last_update = datetime.now()
    
    def get_mood_history(self) -> List[Dict[str, Any]]:
        """Get mood history with all metrics"""
        return [{
            'value': p.value,
            'velocity': p.velocity,
            'acceleration': p.acceleration,
            'volatility': p.volatility,
            'timestamp': p.timestamp.isoformat()
        } for p in self.mood_history]
    
    def get_mood_stats(self) -> Dict[str, float]:
        """Get current mood statistics"""
        return self.mood_stats
    
    def get_mood_gradient(self) -> float:
        """Get current mood gradient"""
        return self.gradient_history[-1] if self.gradient_history else 0.0
    
    def get_gradient_stats(self) -> Dict[str, float]:
        """Get gradient statistics"""
        return self.gradient_stats
    
    def get_mood_prediction(self, steps: int = 10) -> List[float]:
        """Predict future mood values"""
        if len(self.mood_history) < 2:
            return [self.mood_history[-1].value] * steps if self.mood_history else [0.0] * steps
        
        # Extract time series
        times = [(p.timestamp - self.mood_history[0].timestamp).total_seconds() 
                for p in self.mood_history]
        values = [p.value for p in self.mood_history]
        
        # Create interpolation function
        f = interp1d(times, values, kind='cubic', fill_value='extrapolate')
        
        # Generate future timestamps
        last_time = times[-1]
        future_times = [last_time + i * (times[-1] - times[-2]) for i in range(1, steps + 1)]
        
        # Predict values
        predictions = f(future_times)
        return [float(v) for v in predictions]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get mood gradient metrics"""
        return {
            'mood_stats': self.mood_stats,
            'gradient_stats': self.gradient_stats,
            'current_gradient': self.get_mood_gradient(),
            'history_length': len(self.mood_history),
            'volatility': self.volatility_history[-1] if self.volatility_history else 0.0,
            'last_update': self.last_update.isoformat()
        }

def create_mood_gradient_plotter(window_size: int = 100) -> MoodGradientPlotter:
    """Create and return a new mood gradient plotter instance"""
    return MoodGradientPlotter(window_size) 