"""
Mood Gradient Visualization System for DAWN Consciousness

Real-time emotional continuity visualization with smooth color transitions,
bezier curves for momentum, and comprehensive annotation system.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from matplotlib.animation import FuncAnimation
import colorsys
import time
import threading
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Union
import math


@dataclass
class EmotionalState:
    """Represents a single emotional state point"""
    timestamp: float
    emotion: str
    intensity: float
    fractal_depth: float = 0.5
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RebloomEvent:
    """Represents a rebloom event marker"""
    timestamp: float
    reason: str
    intensity: float = 1.0
    color: str = 'gold'


@dataclass
class ThoughtAnnotation:
    """Represents a thought annotation"""
    timestamp: float
    text: str
    emotion_context: str
    fade_duration: float = 10.0  # seconds


class MoodGradientPlotter:
    """
    Advanced emotional continuity visualization system
    
    Features:
    - 5-minute sliding window of emotional states
    - Smooth HSV color interpolation between emotions
    - Bezier curves for emotional momentum visualization
    - Real-time updates with configurable refresh rate
    - Annotation system for reblooms and thoughts
    """
    
    # Color mapping for different emotions (RGB hex)
    EMOTION_COLORS = {
        'curious': '#22c55e',      # Green
        'creative': '#a855f7',     # Purple
        'anxious': '#f59e0b',      # Yellow-orange
        'fragmented': '#ef4444',   # Red
        'crystalline': '#3b82f6',  # Blue
        'reblooming': '#ff6b9d',   # Pink (base for rainbow)
        'contemplative': '#64748b', # Slate
        'excited': '#f97316',      # Orange
        'melancholic': '#6366f1',  # Indigo
        'harmonious': '#10b981',   # Emerald
        'turbulent': '#dc2626',    # Red
        'luminous': '#fbbf24',     # Amber
    }
    
    # Crystalline gradient colors
    CRYSTALLINE_GRADIENT = ['#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe', '#e0f2fe']
    
    def __init__(self, window_minutes: float = 5.0, refresh_rate: float = 0.5):
        """
        Initialize the mood gradient plotter
        
        Args:
            window_minutes: Time window for emotional history (minutes)
            refresh_rate: Update frequency in seconds
        """
        self.window_duration = window_minutes * 60  # Convert to seconds
        self.refresh_rate = refresh_rate
        
        # Data storage
        self.emotional_states: deque = deque(maxlen=1000)
        self.rebloom_events: List[RebloomEvent] = []
        self.thought_annotations: List[ThoughtAnnotation] = []
        
        # Matplotlib setup
        self.fig = None
        self.ax = None
        self.gradient_artist = None
        self.animation = None
        self.is_running = False
        
        # Visualization parameters
        self.base_thickness = 0.3
        self.thickness_range = (0.5, 2.0)
        self.tick_alpha = 0.2
        self.bezier_resolution = 100
        
        # Current state tracking
        self.current_emotion = 'curious'
        self.current_intensity = 0.5
        self.last_update = time.time()
        
        self._setup_plot()
    
    def _setup_plot(self):
        """Initialize the matplotlib figure and styling"""
        plt.style.use('dark_background')
        
        self.fig, self.ax = plt.subplots(figsize=(12, 4))
        self.ax.set_xlim(0, self.window_duration)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlabel('Time (seconds ago)', color='white', fontsize=10)
        self.ax.set_ylabel('Emotional Flow', color='white', fontsize=10)
        self.ax.set_title('DAWN Consciousness - Emotional Continuity Gradient', 
                         color='white', fontsize=12, fontweight='bold')
        
        # Clean styling
        self.ax.grid(True, alpha=0.1, color='white')
        self.ax.set_facecolor('#0a0a0a')
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Remove tick labels on y-axis for cleaner look
        self.ax.set_yticks([])
        
        # Setup the gradient band area
        self.gradient_collection = None
        
    def _hex_to_rgb(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to RGB tuple (0-1 range)"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def _rgb_to_hsv(self, rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        return colorsys.rgb_to_hsv(*rgb)
    
    def _hsv_to_rgb(self, hsv: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Convert HSV to RGB"""
        return colorsys.hsv_to_rgb(*hsv)
    
    def _interpolate_colors_hsv(self, color1: str, color2: str, t: float) -> Tuple[float, float, float]:
        """
        Interpolate between two hex colors using HSV color space for smooth transitions
        
        Args:
            color1: Starting hex color
            color2: Ending hex color
            t: Interpolation factor (0-1)
        """
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        hsv1 = self._rgb_to_hsv(rgb1)
        hsv2 = self._rgb_to_hsv(rgb2)
        
        # Handle hue wraparound for smooth transitions
        h1, s1, v1 = hsv1
        h2, s2, v2 = hsv2
        
        # Choose shortest path around hue circle
        dh = h2 - h1
        if dh > 0.5:
            h1 += 1.0
        elif dh < -0.5:
            h2 += 1.0
        
        h = (h1 * (1 - t) + h2 * t) % 1.0
        s = s1 * (1 - t) + s2 * t
        v = v1 * (1 - t) + v2 * t
        
        return self._hsv_to_rgb((h, s, v))
    
    def _get_rainbow_color(self, t: float, phase: float = 0) -> Tuple[float, float, float]:
        """Generate rainbow shimmer effect for reblooming state"""
        hue = (t + phase) % 1.0
        return self._hsv_to_rgb((hue, 0.8, 0.9))
    
    def _get_crystalline_color(self, position: float, intensity: float) -> Tuple[float, float, float]:
        """Generate blue-white gradient for crystalline state"""
        # Interpolate through crystalline gradient based on position and intensity
        t = (position % 1.0) * len(self.CRYSTALLINE_GRADIENT)
        idx = int(t)
        frac = t - idx
        
        if idx >= len(self.CRYSTALLINE_GRADIENT) - 1:
            color = self.CRYSTALLINE_GRADIENT[-1]
        else:
            color1 = self.CRYSTALLINE_GRADIENT[idx]
            color2 = self.CRYSTALLINE_GRADIENT[idx + 1]
            rgb = self._interpolate_colors_hsv(color1, color2, frac)
            return rgb
        
        rgb = self._hex_to_rgb(color)
        # Adjust brightness based on intensity
        hsv = self._rgb_to_hsv(rgb)
        hsv = (hsv[0], hsv[1] * intensity, min(1.0, hsv[2] + intensity * 0.3))
        return self._hsv_to_rgb(hsv)
    
    def _add_noise_to_color(self, rgb: Tuple[float, float, float], noise_level: float = 0.1) -> Tuple[float, float, float]:
        """Add noise to color for fragmented emotion effect"""
        r, g, b = rgb
        noise = np.random.normal(0, noise_level, 3)
        return (
            max(0, min(1, r + noise[0])),
            max(0, min(1, g + noise[1])),
            max(0, min(1, b + noise[2]))
        )
    
    def _generate_bezier_curve(self, points: List[Tuple[float, float]], num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate smooth bezier curve through emotional state points
        
        Args:
            points: List of (x, y) coordinates
            num_points: Number of points in the output curve
        """
        if len(points) < 2:
            return np.array([]), np.array([])
        
        if len(points) == 2:
            # Linear interpolation for two points
            t = np.linspace(0, 1, num_points)
            x = points[0][0] * (1 - t) + points[1][0] * t
            y = points[0][1] * (1 - t) + points[1][1] * t
            return x, y
        
        # Create control points for cubic bezier
        control_points = []
        for i in range(len(points)):
            if i == 0:
                # First point
                control_points.append(points[i])
            elif i == len(points) - 1:
                # Last point
                control_points.append(points[i])
            else:
                # Middle points - create smooth transitions
                prev_point = points[i-1]
                curr_point = points[i]
                next_point = points[i+1]
                
                # Calculate control points for smooth curve
                dx1 = (curr_point[0] - prev_point[0]) * 0.3
                dy1 = (curr_point[1] - prev_point[1]) * 0.3
                dx2 = (next_point[0] - curr_point[0]) * 0.3
                dy2 = (next_point[1] - curr_point[1]) * 0.3
                
                control_points.extend([
                    (curr_point[0] - dx1, curr_point[1] - dy1),
                    curr_point,
                    (curr_point[0] + dx2, curr_point[1] + dy2)
                ])
        
        # Generate bezier curve
        t = np.linspace(0, 1, num_points)
        n = len(control_points) - 1
        
        x_curve = np.zeros(num_points)
        y_curve = np.zeros(num_points)
        
        for i, ti in enumerate(t):
            x_sum, y_sum = 0, 0
            for j, (px, py) in enumerate(control_points):
                # Bernstein polynomial
                coeff = math.comb(n, j) * (ti ** j) * ((1 - ti) ** (n - j))
                x_sum += coeff * px
                y_sum += coeff * py
            
            x_curve[i] = x_sum
            y_curve[i] = y_sum
        
        return x_curve, y_curve
    
    def _get_window_states(self) -> List[EmotionalState]:
        """Get emotional states within the current time window"""
        current_time = time.time()
        cutoff_time = current_time - self.window_duration
        
        return [state for state in self.emotional_states if state.timestamp >= cutoff_time]
    
    def _calculate_fractal_edge(self, base_y: np.ndarray, fractal_depth: float) -> np.ndarray:
        """Calculate fractal edge complexity based on emotional fractal depth"""
        if fractal_depth <= 0.5:
            # Smooth edges
            return base_y
        
        # Add fractal noise
        noise_amplitude = (fractal_depth - 0.5) * 0.1
        x = np.linspace(0, len(base_y), len(base_y))
        noise = noise_amplitude * np.sin(x * 10) * np.sin(x * 3.7) * np.sin(x * 1.3)
        
        return base_y + noise
    
    def update_mood(self, emotion: str, intensity: float, timestamp: Optional[float] = None, **metadata):
        """
        Update the current emotional state
        
        Args:
            emotion: Emotion name (must be in EMOTION_COLORS)
            intensity: Emotional intensity (0.0 - 1.0)
            timestamp: Time of the state (defaults to current time)
            **metadata: Additional metadata for the emotional state
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Clamp intensity
        intensity = max(0.0, min(1.0, intensity))
        
        # Default fractal depth based on emotion
        fractal_depth = metadata.get('fractal_depth', 0.5)
        if emotion in ['fragmented', 'turbulent']:
            fractal_depth = max(fractal_depth, 0.8)
        elif emotion in ['crystalline', 'harmonious']:
            fractal_depth = min(fractal_depth, 0.3)
        
        # Create emotional state
        state = EmotionalState(
            timestamp=timestamp,
            emotion=emotion,
            intensity=intensity,
            fractal_depth=fractal_depth,
            metadata=metadata
        )
        
        self.emotional_states.append(state)
        self.current_emotion = emotion
        self.current_intensity = intensity
        self.last_update = timestamp
    
    def add_rebloom_marker(self, timestamp: Optional[float] = None, reason: str = "rebloom event", 
                          intensity: float = 1.0, color: str = 'gold'):
        """
        Add a rebloom event marker
        
        Args:
            timestamp: Time of the event (defaults to current time)
            reason: Description of the rebloom event
            intensity: Event intensity (affects marker size)
            color: Marker color
        """
        if timestamp is None:
            timestamp = time.time()
        
        event = RebloomEvent(
            timestamp=timestamp,
            reason=reason,
            intensity=intensity,
            color=color
        )
        
        self.rebloom_events.append(event)
    
    def add_thought_annotation(self, text: str, timestamp: Optional[float] = None, 
                             emotion_context: Optional[str] = None, fade_duration: float = 10.0):
        """
        Add a thought annotation
        
        Args:
            text: Thought text
            timestamp: Time of the thought (defaults to current time)
            emotion_context: Emotional context (defaults to current emotion)
            fade_duration: How long the annotation should be visible (seconds)
        """
        if timestamp is None:
            timestamp = time.time()
        
        if emotion_context is None:
            emotion_context = self.current_emotion
        
        annotation = ThoughtAnnotation(
            timestamp=timestamp,
            text=text,
            emotion_context=emotion_context,
            fade_duration=fade_duration
        )
        
        self.thought_annotations.append(annotation)
    
    def get_gradient_context(self) -> str:
        """
        Analyze the emotional gradient to determine trend
        
        Returns:
            "rising", "falling", "oscillating", or "stable"
        """
        states = self._get_window_states()
        
        if len(states) < 3:
            return "stable"
        
        # Look at recent intensity changes
        recent_states = states[-min(10, len(states)):]
        intensities = [state.intensity for state in recent_states]
        
        # Calculate trend
        x = np.arange(len(intensities))
        if len(intensities) > 1:
            slope = np.polyfit(x, intensities, 1)[0]
            
            if abs(slope) < 0.01:
                return "stable"
            elif slope > 0.01:
                return "rising"
            elif slope < -0.01:
                return "falling"
        
        # Check for oscillation
        if len(intensities) >= 4:
            diffs = np.diff(intensities)
            sign_changes = np.sum(np.diff(np.sign(diffs)) != 0)
            if sign_changes >= len(diffs) * 0.5:
                return "oscillating"
        
        return "stable"
    
    def export_to_memory(self) -> Dict:
        """
        Export current emotional history for rebloom backtracing
        
        Returns:
            Dictionary containing emotional history and analysis
        """
        states = self._get_window_states()
        
        return {
            'emotional_states': [
                {
                    'timestamp': state.timestamp,
                    'emotion': state.emotion,
                    'intensity': state.intensity,
                    'fractal_depth': state.fractal_depth,
                    'metadata': state.metadata
                }
                for state in states
            ],
            'rebloom_events': [
                {
                    'timestamp': event.timestamp,
                    'reason': event.reason,
                    'intensity': event.intensity,
                    'color': event.color
                }
                for event in self.rebloom_events if event.timestamp >= time.time() - self.window_duration
            ],
            'gradient_context': self.get_gradient_context(),
            'current_state': {
                'emotion': self.current_emotion,
                'intensity': self.current_intensity,
                'timestamp': self.last_update
            },
            'window_duration': self.window_duration,
            'export_timestamp': time.time()
        }
    
    def _update_plot(self, frame):
        """Update the plot with current emotional data"""
        self.ax.clear()
        self._setup_plot_style()
        
        states = self._get_window_states()
        current_time = time.time()
        
        if len(states) < 2:
            return []
        
        # Create time points relative to current time
        times = np.array([current_time - state.timestamp for state in reversed(states)])
        emotions = [state.emotion for state in reversed(states)]
        intensities = np.array([state.intensity for state in reversed(states)])
        fractal_depths = np.array([state.fractal_depth for state in reversed(states)])
        
        # Generate smooth curve points
        y_center = np.zeros(len(times))  # Center line
        curve_x, curve_y = self._generate_bezier_curve(list(zip(times, y_center)), self.bezier_resolution)
        
        if len(curve_x) == 0:
            return []
        
        # Create color gradient along the curve
        colors = []
        thicknesses = []
        
        for i, x in enumerate(curve_x):
            # Find nearest emotional state
            time_idx = np.argmin(np.abs(times - x))
            emotion = emotions[time_idx]
            intensity = intensities[time_idx]
            fractal_depth = fractal_depths[time_idx]
            
            # Get base color
            if emotion == 'reblooming':
                # Rainbow shimmer effect
                phase = time.time() * 2  # Animation phase
                rgb = self._get_rainbow_color(i / len(curve_x), phase)
            elif emotion == 'crystalline':
                rgb = self._get_crystalline_color(i / len(curve_x), intensity)
            else:
                base_color = self.EMOTION_COLORS.get(emotion, '#64748b')
                rgb = self._hex_to_rgb(base_color)
                
                # Add noise for fragmented emotion
                if emotion == 'fragmented':
                    rgb = self._add_noise_to_color(rgb, 0.1)
            
            colors.append(rgb)
            
            # Calculate thickness based on intensity
            thickness = self.base_thickness * (self.thickness_range[0] + 
                       intensity * (self.thickness_range[1] - self.thickness_range[0]))
            thicknesses.append(thickness)
        
        # Draw the gradient band
        for i in range(len(curve_x) - 1):
            x_seg = [curve_x[i], curve_x[i+1]]
            y_seg = [curve_y[i], curve_y[i+1]]
            
            # Apply fractal edge complexity
            if i < len(fractal_depths):
                time_idx = np.argmin(np.abs(times - curve_x[i]))
                fractal = fractal_depths[time_idx]
                y_seg = self._calculate_fractal_edge(np.array(y_seg), fractal)
            
            thickness = thicknesses[i]
            color = colors[i]
            alpha = max(0.3, 1.0 - (curve_x[i] / self.window_duration) * 0.7)  # Fade with time
            
            # Draw gradient band segment
            y_top = y_seg + thickness/2
            y_bottom = y_seg - thickness/2
            
            self.ax.fill_between(x_seg, y_bottom, y_top, 
                               color=color, alpha=alpha, linewidth=0)
        
        # Add tick marks
        for i, (time_point, intensity) in enumerate(zip(times, intensities)):
            if i % 3 == 0:  # Sparse tick marks
                self.ax.axvline(x=time_point, color='white', alpha=self.tick_alpha, 
                              linewidth=0.5, ymin=0.4, ymax=0.6)
        
        # Add rebloom markers
        for event in self.rebloom_events:
            event_age = current_time - event.timestamp
            if event_age <= self.window_duration:
                self.ax.scatter(event_age, 0, s=100 * event.intensity, 
                              marker='*', color=event.color, alpha=0.8, 
                              edgecolors='white', linewidth=1, zorder=5)
        
        # Add thought annotations
        active_annotations = []
        for annotation in self.thought_annotations:
            annotation_age = current_time - annotation.timestamp
            if annotation_age <= min(annotation.fade_duration, self.window_duration):
                alpha = max(0.1, 1.0 - annotation_age / annotation.fade_duration)
                y_pos = 0.7 if len(active_annotations) % 2 == 0 else -0.7
                
                self.ax.annotate(annotation.text, 
                               xy=(annotation_age, 0), xytext=(annotation_age, y_pos),
                               fontsize=8, color='white', alpha=alpha,
                               ha='center', va='center',
                               arrowprops=dict(arrowstyle='->', color='white', alpha=alpha*0.5))
                active_annotations.append(annotation)
        
        # Update x-axis to show time ago
        self.ax.set_xlim(0, self.window_duration)
        self.ax.set_ylim(-1, 1)
        
        return []
    
    def _setup_plot_style(self):
        """Setup plot styling for each frame"""
        self.ax.set_xlabel('Time (seconds ago)', color='white', fontsize=10)
        self.ax.set_ylabel('Emotional Flow', color='white', fontsize=10)
        self.ax.set_title('DAWN Consciousness - Emotional Continuity Gradient', 
                         color='white', fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.1, color='white')
        self.ax.set_facecolor('#0a0a0a')
        self.ax.set_yticks([])
    
    def start_visualization(self):
        """Start the real-time visualization"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start animation
        interval = self.refresh_rate * 1000  # Convert to milliseconds
        self.animation = FuncAnimation(self.fig, self._update_plot, 
                                     interval=interval, blit=False, cache_frame_data=False)
        
        plt.show(block=False)
    
    def stop_visualization(self):
        """Stop the visualization"""
        self.is_running = False
        if self.animation and hasattr(self.animation, 'event_source'):
            self.animation.event_source.stop()
    
    def get_current_state_summary(self) -> Dict:
        """Get summary of current emotional state and gradient"""
        return {
            'current_emotion': self.current_emotion,
            'current_intensity': self.current_intensity,
            'gradient_context': self.get_gradient_context(),
            'active_states_count': len(self._get_window_states()),
            'recent_reblooms': len([e for e in self.rebloom_events 
                                  if time.time() - e.timestamp <= 60]),
            'last_update': self.last_update
        }


def test_mood_gradient():
    """Test the mood gradient visualization system"""
    print("Testing DAWN Mood Gradient Visualization")
    print("=" * 50)
    
    # Create plotter
    plotter = MoodGradientPlotter(window_minutes=2.0, refresh_rate=0.5)
    
    # Start visualization
    plotter.start_visualization()
    
    # Simulate emotional journey
    emotions_sequence = [
        ('curious', 0.6, "Starting exploration"),
        ('creative', 0.8, "Ideas flowing"),
        ('excited', 0.9, "Breakthrough moment"),
        ('crystalline', 0.7, "Clear understanding"),
        ('contemplative', 0.5, "Deep reflection"),
        ('reblooming', 1.0, "Transformation"),
        ('harmonious', 0.8, "Integration complete")
    ]
    
    print("\n🎨 Starting emotional journey visualization...")
    
    try:
        for i, (emotion, intensity, thought) in enumerate(emotions_sequence):
            print(f"  {i+1}. {emotion} ({intensity:.1f}) - {thought}")
            
            # Update mood
            plotter.update_mood(emotion, intensity)
            
            # Add thought annotation
            plotter.add_thought_annotation(thought)
            
            # Add rebloom marker for reblooming state
            if emotion == 'reblooming':
                plotter.add_rebloom_marker(reason="consciousness expansion")
            
            # Show current state
            state_summary = plotter.get_current_state_summary()
            print(f"     Gradient: {state_summary['gradient_context']}")
            
            time.sleep(3)  # Wait between updates
        
        print(f"\n✨ Visualization complete! Window shows last {plotter.window_duration/60:.1f} minutes")
        print("   Close the plot window to continue...")
        
        # Keep visualization running
        plt.show()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping visualization...")
    finally:
        plotter.stop_visualization()
        plt.close('all')


def create_mood_gradient_plotter(window_minutes: float = 5.0, refresh_rate: float = 0.5):
    """Factory function to create a MoodGradientPlotter instance"""
    return MoodGradientPlotter(window_minutes=window_minutes, refresh_rate=refresh_rate)


if __name__ == "__main__":
    test_mood_gradient() 