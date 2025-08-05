#!/usr/bin/env python3
"""
DAWN Local Data Server
======================

Lightweight local HTTP server that provides DAWN consciousness data
to the HTML GUI interface. Runs completely locally with no external dependencies.
"""

import json
import time
import threading
import struct
import mmap
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class DAWNDataHandler(BaseHTTPRequestHandler):
    """HTTP handler for DAWN consciousness data requests"""
    
    def __init__(self, *args, **kwargs):
        self.data_provider = kwargs.pop('data_provider', None)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests for consciousness data"""
        if self.path == '/consciousness-state':
            self.send_consciousness_data()
        elif self.path == '/status':
            self.send_status()
        elif self.path.endswith('.html'):
            self.serve_file()
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        """Send CORS headers for local access"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def send_consciousness_data(self):
        """Send current consciousness state as JSON"""
        try:
            data = self.server.data_provider.get_consciousness_data()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            
            json_data = json.dumps(data, indent=2)
            self.wfile.write(json_data.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Data error: {e}")
    
    def send_status(self):
        """Send server status"""
        status = {
            "server": "DAWN Local Data Server",
            "version": "1.0.0",
            "status": "online",
            "mode": self.server.data_provider.get_mode(),
            "timestamp": time.time()
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        
        json_data = json.dumps(status, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def serve_file(self):
        """Serve local HTML files"""
        file_path = Path(__file__).parent / self.path[1:]
        
        if file_path.exists() and file_path.suffix == '.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

class LocalDataProvider:
    """Provides consciousness data from various local sources"""
    
    def __init__(self):
        self.last_data = None
        self.mode = "simulation"
        
        # Possible memory map file locations
        self.mmap_paths = [
            Path("../runtime/dawn_consciousness.mmap"),
            Path("runtime/dawn_consciousness.mmap"),
            Path("../dawn_consciousness.mmap"),
            Path("dawn_consciousness.mmap")
        ]
        
        # Simulation parameters
        self.sim_start_time = time.time()
        self.sim_params = {
            'entropy_base': 0.3,
            'scup_base': 50.0,
            'mood_base': 0.5,
            'tick_base': 0
        }
    
    def get_consciousness_data(self):
        """Get consciousness data from available sources"""
        # Try to read from memory map first
        mmap_data = self.try_read_mmap()
        if mmap_data:
            self.mode = "live_mmap"
            self.last_data = mmap_data
            return mmap_data
        
        # Try to import live DAWN system
        live_data = self.try_read_live_dawn()
        if live_data:
            self.mode = "live_system"
            self.last_data = live_data
            return live_data
        
        # Fall back to enhanced simulation
        self.mode = "simulation"
        sim_data = self.generate_simulation_data()
        self.last_data = sim_data
        return sim_data
    
    def try_read_mmap(self):
        """Try to read from memory-mapped file"""
        for mmap_path in self.mmap_paths:
            if mmap_path.exists():
                try:
                    with open(mmap_path, 'rb') as f:
                        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                            # Read DAWN consciousness data format
                            mm.seek(0)
                            magic = mm.read(4)
                            if magic != b'DAWN':
                                continue
                            
                            # Skip reserved bytes
                            mm.seek(16)
                            tick = struct.unpack('<I', mm.read(4))[0]
                            timestamp = struct.unpack('<Q', mm.read(8))[0]
                            
                            # Read consciousness metrics
                            mm.seek(64)
                            scup = struct.unpack('<f', mm.read(4))[0]
                            entropy = struct.unpack('<f', mm.read(4))[0]
                            mood_val = struct.unpack('<f', mm.read(4))[0]
                            mood_arousal = struct.unpack('<f', mm.read(4))[0]
                            
                            return {
                                'tick': tick,
                                'entropy': entropy,
                                'scup': scup,
                                'mood_val': mood_val,
                                'mood_arousal': mood_arousal,
                                'consciousness_depth': 0.5 + entropy * 0.5,
                                'neural_activity': 0.4 + entropy * 0.6,
                                'memory_pressure': 0.3 + scup / 200.0,
                                'heat_level': 25.0 + abs(mood_val) * 20.0,
                                'timestamp': timestamp,
                                'source': 'memory_map'
                            }
                            
                except Exception as e:
                    print(f"Memory map read error for {mmap_path}: {e}")
                    continue
        
        return None
    
    def try_read_live_dawn(self):
        """Try to read from live DAWN system"""
        try:
            # Try to import and get data from running DAWN
            from launcher_scripts.launch_dawn_unified import DAWNUnifiedLauncher
            
            # This is a simplified approach - in practice you'd need
            # a proper interface to the running DAWN system
            return None
            
        except Exception:
            return None
    
    def generate_simulation_data(self):
        """Generate realistic consciousness simulation data"""
        current_time = time.time()
        elapsed = current_time - self.sim_start_time
        
        # Realistic 16Hz tick simulation
        tick = int(elapsed * 16) % 10000
        
        # Natural entropy fluctuations
        entropy_noise = (
            0.15 * math.sin(elapsed * 0.1) +
            0.08 * math.sin(elapsed * 0.07) +
            0.05 * math.sin(elapsed * 0.13)
        )
        entropy = max(0, min(1, self.sim_params['entropy_base'] + entropy_noise))
        
        # SCUP variations
        scup_noise = (
            15 * math.sin(elapsed * 0.05) +
            8 * math.cos(elapsed * 0.03) +
            3 * math.sin(elapsed * 0.11)
        )
        scup = max(0, min(100, self.sim_params['scup_base'] + scup_noise))
        
        # Mood with emotional drift
        mood_noise = (
            0.3 * math.sin(elapsed * 0.04) +
            0.1 * math.cos(elapsed * 0.08) +
            0.05 * math.sin(elapsed * 0.15)
        )
        mood_val = max(-1, min(1, self.sim_params['mood_base'] + mood_noise))
        
        # Derived metrics
        consciousness_depth = 0.5 + (entropy - 0.5) * 0.6 + 0.2 * math.sin(elapsed * 0.02)
        consciousness_depth = max(0, min(1, consciousness_depth))
        
        neural_activity = 0.4 + entropy * 0.4 + 0.2 * math.sin(elapsed * 0.15)
        memory_pressure = 0.2 + consciousness_depth * 0.5 + 0.1 * math.cos(elapsed * 0.06)
        heat_level = 20 + neural_activity * 30 + 5 * math.sin(elapsed * 0.12)
        
        return {
            'tick': tick,
            'entropy': entropy,
            'scup': scup,
            'mood_val': mood_val,
            'mood_arousal': abs(mood_val) * 0.8,
            'consciousness_depth': consciousness_depth,
            'neural_activity': neural_activity,
            'memory_pressure': memory_pressure,
            'heat_level': heat_level,
            'timestamp': int(current_time * 1000),
            'source': 'simulation'
        }
    
    def get_mode(self):
        """Get current data mode"""
        return self.mode

class DAWNLocalServer:
    """Local HTTP server for DAWN consciousness data"""
    
    def __init__(self, port=8765):
        self.port = port
        self.server = None
        self.data_provider = LocalDataProvider()
        
    def start(self):
        """Start the local server"""
        try:
            # Create custom handler with data provider
            def handler(*args, **kwargs):
                return DAWNDataHandler(*args, data_provider=self.data_provider, **kwargs)
            
            self.server = HTTPServer(('localhost', self.port), handler)
            self.server.data_provider = self.data_provider
            
            print(f"🌐 DAWN Local Data Server starting on http://localhost:{self.port}")
            print(f"📊 Data mode: {self.data_provider.get_mode()}")
            print(f"🔗 Consciousness state: http://localhost:{self.port}/consciousness-state")
            print(f"⚡ Server status: http://localhost:{self.port}/status")
            print("🛑 Press Ctrl+C to stop")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Server stopping...")
            self.stop()
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("✅ DAWN Local Data Server stopped")

def main():
    """Main server entry point"""
    import math  # Import math for simulation
    globals()['math'] = math
    
    print("🧠 DAWN Local Data Server")
    print("=" * 40)
    print("🔗 Fully local consciousness data provider")
    print("📊 No external dependencies or rate limits")
    print()
    
    # Check for memory map files
    data_provider = LocalDataProvider()
    print(f"📡 Data source: {data_provider.get_mode()}")
    
    # Start server
    server = DAWNLocalServer(port=8765)
    server.start()

if __name__ == "__main__":
    main() 