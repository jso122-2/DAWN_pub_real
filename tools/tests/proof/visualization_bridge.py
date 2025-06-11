"""
DAWN Visualization Bridge
Connects the Python test scaffold to the local HTML visualization
"""

import json
import time
import os
from datetime import datetime
import webbrowser
import http.server
import socketserver
import threading

class DAWNVisualizationBridge:
    """Bridge between Python test scaffold and HTML visualization"""
    
    def __init__(self, output_dir="test_output", port=8000):
        self.output_dir = output_dir
        self.port = port
        self.server_thread = None
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Current visualization state
        self.visualization_state = {
            "blooms": [],
            "connections": [],
            "metrics": {
                "entropy": 0.3,
                "coherence": 0.7,
                "heat": 0.5,
                "mood": 0.0
            },
            "tick": 0
        }
    
    def start_local_server(self):
        """Start a local HTTP server to serve files"""
        class Handler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                # Add CORS headers for local development
                self.send_header('Access-Control-Allow-Origin', '*')
                super().end_headers()
        
        def run_server():
            with socketserver.TCPServer(("", self.port), Handler) as httpd:
                print(f"Server running at http://localhost:{self.port}")
                httpd.serve_forever()
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(1)
        
        # Open browser
        webbrowser.open(f'http://localhost:{self.port}/dawn_local_integration.html')
    
    def update_visualization(self, state_data):
        """Update the visualization state file"""
        # Add timestamp
        state_data['timestamp'] = datetime.now().isoformat()
        
        # Write to JSON file that the HTML will read
        vis_file = os.path.join(self.output_dir, 'current_state.json')
        with open(vis_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)
    
    def add_bloom(self, x, y, metrics):
        """Add a new bloom to the visualization"""
        bloom = {
            "id": len(self.visualization_state["blooms"]),
            "x": x,
            "y": y,
            "heat": metrics.get('heat', 0.5),
            "entropy": metrics.get('entropy', 0.3),
            "mood": metrics.get('mood', 0.0),
            "timestamp": time.time()
        }
        
        self.visualization_state["blooms"].append(bloom)
        self.update_visualization(self.visualization_state)
        
        return bloom["id"]
    
    def connect_blooms(self, bloom1_id, bloom2_id):
        """Create a connection between two blooms"""
        connection = [bloom1_id, bloom2_id]
        if connection not in self.visualization_state["connections"]:
            self.visualization_state["connections"].append(connection)
            self.update_visualization(self.visualization_state)
    
    def update_metrics(self, metrics):
        """Update global metrics"""
        self.visualization_state["metrics"].update(metrics)
        self.visualization_state["tick"] += 1
        self.update_visualization(self.visualization_state)
    
    def create_test_sequence(self):
        """Create a test sequence for demonstration"""
        print("Creating test visualization sequence...")
        
        # Create central bloom
        center_id = self.add_bloom(400, 300, {
            "heat": 0.8,
            "entropy": 0.2,
            "mood": 0.3
        })
        
        time.sleep(0.5)
        
        # Create surrounding blooms
        for i in range(6):
            angle = i * 60 * 3.14159 / 180
            x = 400 + 100 * np.cos(angle)
            y = 300 + 100 * np.sin(angle)
            
            bloom_id = self.add_bloom(x, y, {
                "heat": 0.5 + i * 0.08,
                "entropy": 0.3 + i * 0.1,
                "mood": -0.5 + i * 0.3
            })
            
            # Connect to center
            self.connect_blooms(center_id, bloom_id)
            
            # Update global metrics
            self.update_metrics({
                "entropy": 0.3 + i * 0.1,
                "coherence": 0.8 - i * 0.1,
                "heat": 0.5 + i * 0.05
            })
            
            time.sleep(0.3)


# Integration with existing dawn_test_scaffold.py
def integrate_with_test_scaffold():
    """Example of how to integrate with your existing test scaffold"""
    
    # Import your test scaffold
    try:
        from dawn_test_scaffold import DAWNTestScaffold
    except ImportError:
        print("dawn_test_scaffold.py not found in current directory")
        return
    
    # Create visualization bridge
    bridge = DAWNVisualizationBridge()
    bridge.start_local_server()
    
    # Create test scaffold with custom process_input that updates visualization
    class VisualizedTestScaffold(DAWNTestScaffold):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bridge = bridge
            self.bloom_positions = {}
            
        def process_input(self, input_text, intensity=1.0):
            # Call parent process_input
            result = super().process_input(input_text, intensity)
            
            # Update visualization
            tick = self.current_tick
            
            # Create bloom for this tick if not exists
            if tick not in self.bloom_positions:
                x = 100 + (tick * 30) % 700
                y = 100 + (tick // 20) * 50
                bloom_id = self.bridge.add_bloom(x, y, {
                    "heat": self.input_pressure,
                    "entropy": self.entropy_index,
                    "mood": self.valence
                })
                self.bloom_positions[tick] = bloom_id
                
                # Connect to previous bloom
                if tick > 1 and (tick - 1) in self.bloom_positions:
                    self.bridge.connect_blooms(
                        self.bloom_positions[tick - 1],
                        self.bloom_positions[tick]
                    )
            
            # Update global metrics
            self.bridge.update_metrics({
                "entropy": self.entropy_index,
                "coherence": self.coherence_index,
                "heat": self.input_pressure,
                "mood": self.valence,
                "drift_velocity": self.drift_velocity
            })
            
            return result
    
    # Run the test with visualization
    print("Starting DAWN Visualized Test...")
    scaffold = VisualizedTestScaffold(enable_visualization=False)  # We use HTML viz instead
    scaffold.run_contradiction_test()
    scaffold.close()
    
    print("\nVisualization running at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")


# Standalone usage
if __name__ == "__main__":
    import numpy as np  # For test sequence
    
    # Option 1: Just run the visualization with test data
    bridge = DAWNVisualizationBridge()
    bridge.start_local_server()
    bridge.create_test_sequence()
    
    # Option 2: Integrate with test scaffold (uncomment below)
    # integrate_with_test_scaffold()
    
    print("\nVisualization is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")