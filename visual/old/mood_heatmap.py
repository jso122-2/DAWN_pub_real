# visual/mood_heatmap.py - Simple working mood visualization

import threading
import time
import queue
from typing import Dict, Any
from datetime import datetime

class SimpleMoodHeatmap:
    """
    Simple mood visualization that shows emotional state patterns
    """
    
    def __init__(self):
        self.mood_history = []
        self.max_history = 30
        self.last_mood_tag = "unknown"
        
    def update_visualization(self, consciousness_data: Dict[str, Any]):
        """Update mood visualization with consciousness data"""
        try:
            # Extract mood and entropy data
            mood_state = consciousness_data.get('mood_state', {})
            entropy_snapshot = consciousness_data.get('entropy_snapshot', {})
            
            # Get mood values
            valence = mood_state.get('valence', 0.5)
            arousal = mood_state.get('arousal', 0.5)
            mood_tag = mood_state.get('tag', 'neutral')
            
            # Get entropy values
            current_entropy = entropy_snapshot.get('current_entropy', 0.5)
            intensity = entropy_snapshot.get('intensity', 0.5)
            
            # Store in history
            mood_data = {
                'valence': valence,
                'arousal': arousal,
                'entropy': current_entropy,
                'intensity': intensity,
                'tag': mood_tag,
                'timestamp': datetime.now()
            }
            
            self.mood_history.append(mood_data)
            if len(self.mood_history) > self.max_history:
                self.mood_history.pop(0)
            
            # Render mood display
            self._render_mood_display(valence, arousal, current_entropy, mood_tag)
            
            # Check for mood transitions
            if mood_tag != self.last_mood_tag:
                print(f"[MoodHeatmap] 🎭 Mood transition: {self.last_mood_tag} → {mood_tag}")
                self.last_mood_tag = mood_tag
            
        except Exception as e:
            print(f"[MoodHeatmap] ❌ Update error: {e}")
    
    def _render_mood_display(self, valence: float, arousal: float, entropy: float, mood_tag: str):
        """Render simple mood display"""
        # Create emotional state visualization
        valence_bar = self._create_bar(valence, "😢", "😊")
        arousal_bar = self._create_bar(arousal, "😴", "⚡")
        entropy_bar = self._create_bar(entropy, "🧊", "🌪️")
        
        # Determine mood emoji
        mood_emoji = self._get_mood_emoji(valence, arousal)
        
        # Display mood state
        print(f"[MoodHeatmap] {mood_emoji} {mood_tag.upper()}")
        print(f"[MoodHeatmap] 💝 Valence: {valence_bar} ({valence:.2f})")
        print(f"[MoodHeatmap] ⚡ Arousal:  {arousal_bar} ({arousal:.2f})")
        print(f"[MoodHeatmap] 🌊 Entropy:  {entropy_bar} ({entropy:.2f})")
        
        # Show mood trend if we have history
        if len(self.mood_history) >= 3:
            self._show_mood_trend()
    
    def _create_bar(self, value: float, low_icon: str, high_icon: str) -> str:
        """Create a visual bar representation"""
        bar_length = 10
        filled = int(value * bar_length)
        empty = bar_length - filled
        
        return f"{low_icon}{'█' * filled}{'░' * empty}{high_icon}"
    
    def _get_mood_emoji(self, valence: float, arousal: float) -> str:
        """Get emoji based on valence/arousal quadrant"""
        if valence > 0.6 and arousal > 0.6:
            return "😄"  # Happy/Excited
        elif valence > 0.6 and arousal < 0.4:
            return "😌"  # Content/Calm
        elif valence < 0.4 and arousal > 0.6:
            return "😠"  # Angry/Frustrated
        elif valence < 0.4 and arousal < 0.4:
            return "😞"  # Sad/Depressed
        else:
            return "😐"  # Neutral
    
    def _show_mood_trend(self):
        """Show trend in mood over time"""
        if len(self.mood_history) < 3:
            return
        
        recent = self.mood_history[-3:]
        
        # Calculate valence trend
        valence_trend = recent[-1]['valence'] - recent[0]['valence']
        arousal_trend = recent[-1]['arousal'] - recent[0]['arousal']
        
        # Show trends
        val_arrow = "📈" if valence_trend > 0.1 else "📉" if valence_trend < -0.1 else "➡️"
        aro_arrow = "📈" if arousal_trend > 0.1 else "📉" if arousal_trend < -0.1 else "➡️"
        
        print(f"[MoodHeatmap] 📊 Trends: Valence {val_arrow} | Arousal {aro_arrow}")
        
        # Show unique mood tags in recent history
        recent_tags = [m['tag'] for m in recent]
        unique_tags = list(set(recent_tags))
        if len(unique_tags) > 1:
            print(f"[MoodHeatmap] 🏷️ Recent moods: {', '.join(unique_tags)}")

def run_visual_process(data_queue: queue.Queue, control_queue: queue.Queue, stop_event: threading.Event):
    """
    Standard interface for Visual Consciousness Manager (Threading version)
    """
    print("[MoodHeatmap] 🎨 Starting mood heatmap visualization")
    
    visualizer = SimpleMoodHeatmap()
    running = True
    last_update = time.time()
    
    while running and not stop_event.is_set():
        try:
            # Check for shutdown signal
            if not control_queue.empty():
                try:
                    control_msg = control_queue.get_nowait()
                    if control_msg.get('type') == 'shutdown':
                        print("[MoodHeatmap] 🛑 Shutdown signal received")
                        running = False
                        break
                except queue.Empty:
                    pass
            
            # Process incoming data
            data_processed = False
            if not data_queue.empty():
                try:
                    data_msg = data_queue.get_nowait()
                    consciousness_data = data_msg.get('data', {})
                    
                    # Update visualization
                    visualizer.update_visualization(consciousness_data)
                    data_processed = True
                    last_update = time.time()
                    
                except queue.Empty:
                    pass
            
            # Periodic status if no data for a while
            if not data_processed and time.time() - last_update > 10.0:
                print("[MoodHeatmap] ⏳ Waiting for mood data...")
                last_update = time.time()
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.2)  # 5 FPS max for mood updates
            
        except KeyboardInterrupt:
            print("[MoodHeatmap] 🛑 Keyboard interrupt")
            running = False
        except Exception as e:
            print(f"[MoodHeatmap] ❌ Process error: {e}")
            time.sleep(0.5)  # Pause on error
    
    # Cleanup
    print("[MoodHeatmap] 🎨 Mood heatmap visualization stopped")

# Alternative interfaces for flexibility
def main(data_queue: queue.Queue = None, control_queue: queue.Queue = None, stop_event: threading.Event = None):
    """Alternative main interface"""
    if data_queue and control_queue and stop_event:
        run_visual_process(data_queue, control_queue, stop_event)
    else:
        # Standalone mode for testing
        print("[MoodHeatmap] Running in standalone test mode")
        test_visualization()

def test_visualization():
    """Test the visualization with dummy data"""
    import random
    import math
    
    visualizer = SimpleMoodHeatmap()
    
    print("[MoodHeatmap] 🧪 Testing mood heatmap with dummy data")
    
    mood_tags = ['curious', 'reflective', 'excited', 'contemplative', 'creative', 'analytical']
    
    for i in range(15):
        # Generate test mood data with some patterns
        t = i / 15.0
        base_valence = 0.5 + 0.3 * math.sin(t * 4)
        base_arousal = 0.5 + 0.2 * math.cos(t * 3)
        
        # Add some noise
        valence = max(0, min(1, base_valence + random.uniform(-0.2, 0.2)))
        arousal = max(0, min(1, base_arousal + random.uniform(-0.2, 0.2)))
        entropy = random.uniform(0.2, 0.8)
        
        # Pick mood tag
        mood_tag = random.choice(mood_tags)
        
        test_data = {
            'mood_state': {
                'valence': valence,
                'arousal': arousal,
                'tag': mood_tag
            },
            'entropy_snapshot': {
                'current_entropy': entropy,
                'intensity': random.uniform(0.3, 0.7)
            }
        }
        
        visualizer.update_visualization(test_data)
        time.sleep(0.4)
    
    print("[MoodHeatmap] 🧪 Test completed")

if __name__ == "__main__":
    # Test mode when run directly
    test_visualization()
