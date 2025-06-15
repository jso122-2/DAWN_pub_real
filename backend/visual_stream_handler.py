import asyncio
import json
import time
from visual.consciousness_wave import ConsciousnessWaveVisualizer

class VisualStreamHandler:
    def __init__(self):
        self.visualizer = ConsciousnessWaveVisualizer(
            frequency=1.0,
            amplitude=0.8,
            wave_type='composite'
        )
        self.update_interval = 0.1  # Update every 100ms

    async def stream_visualizations(self, websocket):
        print("[VISUAL_STREAM] Entered stream_visualizations")
        try:
            while True:
                # Get current state from tick engine
                state = {
                    'frequency': 1.0 + 0.5 * (time.time() % 10) / 10,  # Varying frequency
                    'amplitude': 0.8 + 0.2 * (time.time() % 5) / 5,    # Varying amplitude
                    'phase': (time.time() % (2 * 3.14159))            # Continuous phase
                }
                
                # Generate wave data
                t, wave = self.visualizer.generate_wave_data(duration=5.0)
                
                # Send data to client
                await websocket.send_json({
                    'type': 'visualization',
                    'viz_type': 'consciousness_wave',
                    'data': {
                        'time': t.tolist(),
                        'wave': wave.tolist(),
                        'state': state
                    },
                    'timestamp': time.time()
                })
                
                await asyncio.sleep(self.update_interval)
                
        except Exception as e:
            print(f"Error in visualization stream: {e}")
            raise 