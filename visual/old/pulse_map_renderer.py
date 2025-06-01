# visual/pulse_map_renderer.py - Simple working pulse visualization

import threading
import time
import queue
from typing import Dict, Any
from datetime import datetime

class SimplePulseRenderer:
    """
    Simple pulse/thermal visualization that works with the threading-based system
    """
    
    def __init__(self):
        self.current_heat = 0.0
        self.heat_history = []
        self.max_history = 50
        self.last_thermal_zone = "unknown"
        
    def update_visualization(self, consciousness_data: Dict[str, Any]):
        """Update pulse visualization with consciousness data"""
        try:
            # Extract thermal data
            thermal_stats = consciousness_data.get('thermal_stats', {})
            tick_stats = consciousness_data.get('tick_stats', {})
            
            # Get current heat and zone
            current_heat = thermal_stats.get('current_heat', 0.0)
            thermal_zone = thermal_stats.get('current_zone', '🟢 calm')
            stability = thermal_stats.get('stability_index', 1.0)
            
            # Update state
            self.current_heat = current_heat
            self.heat_history.append(current_heat)
            if len(self.heat_history) > self.max_history:
                self.heat_history.pop(0)
            
            # Render thermal state
            self._render_thermal_display(current_heat, thermal_zone, stability)
            
            # Check for zone transitions
            if thermal_zone != self.last_thermal_zone:
                print(f"[PulseRenderer] 🌡️ Zone transition: {self.last_thermal_zone} → {thermal_zone}")
                self.last_thermal_zone = thermal_zone
            
        except Exception as e:
            print(f"[PulseRenderer] ❌ Update error: {e}")
    
    def _render_thermal_display(self, heat: float, zone: str, stability: float):
        """Render simple thermal display"""
        # Create heat bar visualization
        bar_length = 20
        heat_level = min(int((heat / 10.0) * bar_length), bar_length)
        heat_bar = "█" * heat_level + "░" * (bar_length - heat_level)
        
        # Stability indicator
        stability_icon = "🟢" if stability > 0.8 else "🟡" if stability > 0.5 else "🔴"
        
        # Display thermal state
        print(f"[PulseRenderer] 🔥 Heat: {heat:.2f} |{heat_bar}| {zone} {stability_icon}")
        
        # Show heat trend if we have history
        if len(self.heat_history) >= 3:
            recent_trend = self.heat_history[-3:]
            if recent_trend[-1] > recent_trend[0]:
                trend = "📈"
            elif recent_trend[-1] < recent_trend[0]:
                trend = "📉"
            else:
                trend = "➡️"
            
            avg_heat = sum(self.heat_history) / len(self.heat_history)
            print(f"[PulseRenderer] 📊 Trend: {trend} | Avg: {avg_heat:.2f} | Stability: {stability:.2f}")

def run_visual_process(data_queue: queue.Queue, control_queue: queue.Queue, stop_event: threading.Event):
    """
    Standard interface for Visual Consciousness Manager (Threading version)
    """
    print("[PulseRenderer] 🎨 Starting pulse map renderer")
    
    renderer = SimplePulseRenderer()
    running = True
    last_update = time.time()
    
    while running and not stop_event.is_set():
        try:
            # Check for shutdown signal
            if not control_queue.empty():
                try:
                    control_msg = control_queue.get_nowait()
                    if control_msg.get('type') == 'shutdown':
                        print("[PulseRenderer] 🛑 Shutdown signal received")
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
                    renderer.update_visualization(consciousness_data)
                    data_processed = True
                    last_update = time.time()
                    
                except queue.Empty:
                    pass
            
            # Periodic status if no data for a while
            if not data_processed and time.time() - last_update > 5.0:
                print("[PulseRenderer] ⏳ Waiting for thermal data...")
                last_update = time.time()
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.1)  # 10 FPS max
            
        except KeyboardInterrupt:
            print("[PulseRenderer] 🛑 Keyboard interrupt")
            running = False
        except Exception as e:
            print(f"[PulseRenderer] ❌ Process error: {e}")
            time.sleep(0.5)  # Pause on error
    
    # Cleanup
    print("[PulseRenderer] 🎨 Pulse map renderer stopped")

# Alternative interfaces for flexibility
def main(data_queue: queue.Queue = None, control_queue: queue.Queue = None, stop_event: threading.Event = None):
    """Alternative main interface"""
    if data_queue and control_queue and stop_event:
        run_visual_process(data_queue, control_queue, stop_event)
    else:
        # Standalone mode for testing
        print("[PulseRenderer] Running in standalone test mode")
        test_visualization()

def test_visualization():
    """Test the visualization with dummy data"""
    import random
    
    renderer = SimplePulseRenderer()
    
    print("[PulseRenderer] 🧪 Testing pulse renderer with dummy data")
    
    for i in range(20):
        # Generate test thermal data
        base_heat = 3.0 + 2.0 * (i / 20.0)  # Gradually increase
        heat_noise = random.uniform(-0.5, 0.5)
        current_heat = max(0, base_heat + heat_noise)
        
        # Determine zone based on heat
        if current_heat < 2.0:
            zone = "🟢 calm"
        elif current_heat < 5.0:
            zone = "🟡 active"
        else:
            zone = "🔴 surge"
        
        test_data = {
            'thermal_stats': {
                'current_heat': current_heat,
                'current_zone': zone,
                'stability_index': random.uniform(0.3, 1.0)
            },
            'tick_stats': {
                'tick_count': i
            }
        }
        
        renderer.update_visualization(test_data)
        time.sleep(0.3)
    
    print("[PulseRenderer] 🧪 Test completed")

if __name__ == "__main__":
    # Test mode when run directly
    test_visualization()
