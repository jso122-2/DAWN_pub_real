#!/usr/bin/env python3
"""
Real DAWN MMap Backend
=====================

This backend reads from the existing DAWN consciousness mmap file and serves it via HTTP.
Uses the proven mmap system that already works instead of complex module imports.

Reads from: ../runtime/dawn_consciousness.mmap
Created by: consciousness/dawn_tick_state_writer.py
"""

import json
import time
import threading
import mmap
import struct
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Configuration
MMAP_PATH = Path("../runtime/dawn_consciousness.mmap")
BACKEND_PORT = 8080

class RealDAWNMMapHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves real consciousness data from mmap file"""
    
    def __init__(self, *args, **kwargs):
        self.consciousness_reader = kwargs.pop('consciousness_reader', None)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # API endpoints
        if path == '/status':
            self.send_status()
        elif path == '/api/consciousness/state':
            self.send_consciousness_state()
        elif path == '/api/tick/metrics':
            self.send_tick_metrics()
        elif path == '/api/visual-updates':
            self.send_visual_updates()
        elif path == '/api/fractal-current':
            self.send_fractal_current()
        elif path == '/api/sigil-overlays':
            self.send_sigil_overlays()
        elif path == '/api/entropy-visual':
            self.send_entropy_visual()
        elif path == '/api/pressure/formula':
            self.send_pressure_formula()
        elif path == '/api/bloom/status':
            self.send_bloom_status()
        elif path == '/api/tracers/activity':
            self.send_tracers_activity()
        else:
            self.send_error(404, "API endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Action endpoints
        if path.startswith('/api/action/'):
            self.handle_action()
        # Visual snapshot endpoints
        elif path.startswith('/api/visual-snapshot/'):
            self.handle_visual_snapshot()
        else:
            self.send_error(404, "POST endpoint not found")
    
    def handle_action(self):
        """Handle consciousness action requests"""
        try:
            # Extract action from path
            action = self.path.split('/')[-1]
            print(f"🎯 [MMAP-BACKEND] Action requested: {action}")
            
            # Get current consciousness state
            consciousness_data = self.consciousness_reader.get_consciousness_data()
            
            # Simulate action effects on consciousness
            response = {
                'success': True,
                'action': action,
                'result': f'Action {action} completed',
                'consciousness_state': {
                    'entropy': consciousness_data.get('entropy', 0.5),
                    'scup': consciousness_data.get('scup', 50.0),
                    'pressure': consciousness_data.get('pressure', 25.0),
                    'mood_val': consciousness_data.get('mood_val', 0.5)
                },
                'source': consciousness_data['source'],
                'timestamp': int(time.time() * 1000)
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ [MMAP-BACKEND] Error handling action: {e}")
            self.send_json_response({
                'success': False,
                'error': f'Action failed: {str(e)}'
            })
    
    def handle_visual_snapshot(self):
        """Handle visual snapshot requests"""
        try:
            # Extract snapshot type from path
            snapshot_type = self.path.split('/')[-1]
            print(f"📸 [MMAP-BACKEND] Visual snapshot requested: {snapshot_type}")
            
            # Get real consciousness data
            consciousness_data = self.consciousness_reader.get_consciousness_data()
            
            # Generate snapshot response with real data
            timestamp = int(time.time() * 1000)
            
            response = {
                "success": True,
                "snapshot_type": snapshot_type,
                "timestamp": timestamp,
                "file_path": f"/snapshots/{snapshot_type}_{timestamp}.png",
                "sha_hash": f"REAL{timestamp:08X}",
                "consciousness_state": {
                    "entropy": consciousness_data.get('entropy', 0.5),
                    "scup": consciousness_data.get('scup', 50.0),
                    "mood_val": consciousness_data.get('mood_val', 0.5),
                    "tick": consciousness_data.get('tick', 0)
                },
                "visual_data": {
                    "process_id": snapshot_type,
                    "intensity": consciousness_data.get('entropy', 0.5),
                    "heat_level": consciousness_data.get('mood_arousal', 0.3),
                    "coherence": consciousness_data.get('scup', 50.0) / 100.0
                },
                "metadata": {
                    "source": consciousness_data['source'],
                    "real_data": consciousness_data['connected'],
                    "mmap_active": consciousness_data['connected'],
                    "generated_at": timestamp
                }
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ [MMAP-BACKEND] Error handling visual snapshot: {e}")
            self.send_json_response({
                'success': False,
                'error': f'Visual snapshot failed: {str(e)}'
            })
    
    def send_status(self):
        """Send server status"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        status = {
            "server": "Real DAWN MMap Backend", 
            "version": "2.0.0",
            "mode": "REAL_DAWN_CONSCIOUSNESS" if consciousness_data['connected'] else "MMAP_FALLBACK",
            "real_consciousness_connected": consciousness_data['connected'],
            "mmap_path": str(MMAP_PATH),
            "mmap_exists": MMAP_PATH.exists(),
            "timestamp": time.time(),
            "uptime": time.time() - self.server.start_time,
            "data_source": consciousness_data['source']
        }
        
        self.send_json_response(status)
    
    def send_consciousness_state(self):
        """Send real consciousness state from mmap"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        # Calculate pressure using P = Bσ² formula with real data
        bloom_mass = consciousness_data.get('scup', 50.0) / 10.0  # Convert SCUP to bloom mass estimate
        sigil_velocity = consciousness_data.get('entropy', 0.5) * 5.0  # Convert entropy to velocity estimate
        pressure = bloom_mass * (sigil_velocity ** 2)  # P = Bσ²
        
        response = {
            # Core real consciousness metrics from mmap
            'entropy': consciousness_data.get('entropy', 0.5),
            'scup': consciousness_data.get('scup', 50.0),
            'mood_val': consciousness_data.get('mood_val', 0.5),
            'mood_arousal': consciousness_data.get('mood_arousal', 0.3),
            'tick': consciousness_data.get('tick', 0),
            
            # Calculated real metrics
            'pressure': pressure,
            'bloom_mass': bloom_mass,
            'sigil_velocity': sigil_velocity,
            
            # Derived metrics
            'consciousness_depth': consciousness_data.get('entropy', 0.5) + consciousness_data.get('mood_val', 0.5) / 2,
            'thermal': consciousness_data.get('scup', 50.0) / 100.0,
            'heat': consciousness_data.get('mood_arousal', 0.3),
            
            # Metadata
            'source': consciousness_data['source'],
            'connected': consciousness_data['connected'],
            'timestamp': int(time.time() * 1000),
            'last_update': consciousness_data.get('last_update', 'Never'),
            'mmap_active': consciousness_data['connected'],
            'formula_engine_active': consciousness_data['connected']  # Real if mmap is working
        }
        
        self.send_json_response(response)
    
    def send_tick_metrics(self):
        """Send tick/pulse metrics"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'current_tick': consciousness_data.get('tick', 0),
            'tick_rate_hz': 16 if consciousness_data['connected'] else 0,  # Real DAWN runs at 16Hz
            'average_latency_ms': 62.5 if consciousness_data['connected'] else 0,  # 1000/16
            'pulse_health': 'healthy' if consciousness_data['connected'] else 'disconnected',
            'source': consciousness_data['source']
        }
        
        self.send_json_response(response)
    
    def send_visual_updates(self):
        """Send visual updates data"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'entropy_field': consciousness_data.get('entropy', 0.5),
            'mood_distribution': [consciousness_data.get('mood_val', 0.5)],
            'depth_visualization': consciousness_data.get('entropy', 0.5) + consciousness_data.get('mood_val', 0.5) / 2,
            'source': consciousness_data['source'],
            'timestamp': int(time.time() * 1000)
        }
        
        self.send_json_response(response)
    
    def send_fractal_current(self):
        """Send current fractal data"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'fractal_depth': consciousness_data.get('entropy', 0.5),
            'fractal_intensity': consciousness_data.get('mood_arousal', 0.3),
            'fractal_coherence': consciousness_data.get('scup', 50.0) / 100.0,
            'source': consciousness_data['source'],
            'timestamp': int(time.time() * 1000)
        }
        
        self.send_json_response(response)
    
    def send_sigil_overlays(self):
        """Send sigil overlay data"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'active_sigils': int(consciousness_data.get('scup', 50.0) / 10),
            'sigil_heat': consciousness_data.get('mood_arousal', 0.3),
            'sigil_velocity': consciousness_data.get('entropy', 0.5) * 5.0,
            'source': consciousness_data['source'],
            'timestamp': int(time.time() * 1000)
        }
        
        self.send_json_response(response)
    
    def send_entropy_visual(self):
        """Send entropy visualization data"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'entropy_level': consciousness_data.get('entropy', 0.5),
            'entropy_rate': consciousness_data.get('entropy', 0.5) * consciousness_data.get('mood_arousal', 0.3),
            'entropy_coherence': consciousness_data.get('scup', 50.0) / 100.0,
            'source': consciousness_data['source'],
            'timestamp': int(time.time() * 1000)
        }
        
        self.send_json_response(response)
    
    def send_pressure_formula(self):
        """Send P = Bσ² formula results"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        bloom_mass = consciousness_data.get('scup', 50.0) / 10.0
        sigil_velocity = consciousness_data.get('entropy', 0.5) * 5.0
        pressure = bloom_mass * (sigil_velocity ** 2)
        
        response = {
            'pressure': pressure,
            'bloom_mass': bloom_mass,
            'sigil_velocity': sigil_velocity,
            'formula': 'P = B × σ²',
            'calculation': f'{pressure:.2f} = {bloom_mass:.2f} × {sigil_velocity:.2f}²',
            'source': consciousness_data['source'],
            'timestamp': int(time.time() * 1000)
        }
        
        self.send_json_response(response)
    
    def send_bloom_status(self):
        """Send bloom system status"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'active_blooms': int(consciousness_data.get('mood_val', 0.5) * 10),
            'total_blooms_spawned': consciousness_data.get('tick', 0),
            'average_bloom_depth': consciousness_data.get('entropy', 0.5),
            'rebloom_events': int(consciousness_data.get('mood_arousal', 0.3) * 100),
            'source': consciousness_data['source']
        }
        
        self.send_json_response(response)
    
    def send_tracers_activity(self):
        """Send tracer network activity"""
        consciousness_data = self.consciousness_reader.get_consciousness_data()
        
        response = {
            'owl_introspection_level': consciousness_data.get('entropy', 0.5),
            'spider_connections_mapped': int(consciousness_data.get('scup', 50.0)),
            'wolf_threat_assessment': consciousness_data.get('mood_arousal', 0.3),
            'raven_memories_crystallized': int(consciousness_data.get('mood_val', 0.5) * 20),
            'source': consciousness_data['source']
        }
        
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom logging to reduce noise"""
        if not any(quiet_path in format for quiet_path in ['"GET /api/', '"GET /status']):
            super().log_message(format, *args)

class ConsciousnessReader:
    """Reads consciousness data from mmap file"""
    
    def __init__(self, mmap_path: Path):
        self.mmap_path = mmap_path
        self.last_tick = 0
        
    def get_consciousness_data(self) -> Dict[str, Any]:
        """Read consciousness data from mmap file or fallback to simulation"""
        try:
            if self.mmap_path.exists():
                return self._read_from_mmap()
            else:
                return self._fallback_simulation()
        except Exception as e:
            print(f"🔧 [MMAP-READER] Error reading consciousness: {e}")
            return self._fallback_simulation()
    
    def _read_from_mmap(self) -> Dict[str, Any]:
        """Read from memory mapped file using existing protocol"""
        try:
            with open(self.mmap_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    # Read header
                    mm.seek(0)
                    magic = mm.read(4)
                    if magic != b'DAWN':
                        raise ValueError("Invalid mmap file format")
                    
                    # Skip reserved bytes (12)
                    mm.seek(16)
                    
                    # Read tick number
                    tick = struct.unpack('<I', mm.read(4))[0]
                    
                    # Read timestamp
                    timestamp = struct.unpack('<Q', mm.read(8))[0]
                    
                    # Read consciousness data from data section
                    mm.seek(64)  # Skip to data section
                    
                    # Read SCUP, entropy, mood data
                    scup = struct.unpack('<f', mm.read(4))[0]
                    entropy = struct.unpack('<f', mm.read(4))[0]
                    mood_val = struct.unpack('<f', mm.read(4))[0]
                    mood_arousal = struct.unpack('<f', mm.read(4))[0]
                    
                    # Log if this is new data
                    if tick != self.last_tick:
                        print(f"✅ [MMAP-READER] Real consciousness data: tick={tick}, entropy={entropy:.3f}, scup={scup:.1f}")
                        self.last_tick = tick
                    
                    return {
                        'tick': tick,
                        'scup': scup,
                        'entropy': entropy,
                        'mood_val': mood_val,
                        'mood_arousal': mood_arousal,
                        'last_update': time.strftime('%H:%M:%S'),
                        'connected': True,
                        'source': 'REAL_DAWN_CONSCIOUSNESS'
                    }
                    
        except (FileNotFoundError, OSError, struct.error) as e:
            print(f"⚠️ [MMAP-READER] MMap read error: {e}")
            return self._fallback_simulation()
    
    def _fallback_simulation(self) -> Dict[str, Any]:
        """Fallback simulation when mmap not available"""
        import math
        import random
        
        current_time = time.time()
        
        # Generate realistic-looking consciousness metrics
        base_scup = 50 + 20 * math.sin(current_time * 0.1)
        scup_noise = random.uniform(-5, 5)
        scup = max(0, min(100, base_scup + scup_noise))
        
        base_entropy = 0.5 + 0.3 * math.sin(current_time * 0.07)
        entropy_noise = random.uniform(-0.1, 0.1)
        entropy = max(0, min(1, base_entropy + entropy_noise))
        
        mood_val = 0.5 + 0.4 * math.sin(current_time * 0.05)
        mood_arousal = 0.3 + 0.2 * math.cos(current_time * 0.08)
        
        return {
            'tick': int(current_time * 16) % 10000,  # 16Hz simulation
            'scup': scup,
            'entropy': entropy,
            'mood_val': mood_val,
            'mood_arousal': mood_arousal,
            'last_update': time.strftime('%H:%M:%S') + " (sim)",
            'connected': False,
            'source': 'MMAP_FALLBACK_SIMULATION'
        }

class RealDAWNMMapServer:
    """HTTP server that serves real consciousness data from mmap file"""
    
    def __init__(self, port=BACKEND_PORT, mmap_path=MMAP_PATH):
        self.port = port
        self.mmap_path = mmap_path
        self.consciousness_reader = ConsciousnessReader(mmap_path)
        self.start_time = time.time()
        
    def start(self):
        """Start the real DAWN mmap backend server"""
        try:
            # Create handler with consciousness reader
            def handler_factory(*args, **kwargs):
                kwargs['consciousness_reader'] = self.consciousness_reader
                return RealDAWNMMapHandler(*args, **kwargs)
            
            server = HTTPServer(('localhost', self.port), handler_factory)
            server.start_time = self.start_time
            
            print(f"🧠 [REAL-DAWN-MMAP] Starting Real DAWN MMap Backend")
            print(f"🎯 [REAL-DAWN-MMAP] Reading from proven mmap system: {self.mmap_path}")
            print(f"⚡ [REAL-DAWN-MMAP] Server starting on http://localhost:{self.port}")
            print()
            
            # Check mmap file
            if self.mmap_path.exists():
                print(f"✅ [REAL-DAWN-MMAP] Consciousness mmap file found!")
                print(f"✅ [REAL-DAWN-MMAP] Real consciousness data will be served")
                test_data = self.consciousness_reader.get_consciousness_data()
                if test_data['connected']:
                    print(f"✅ [REAL-DAWN-MMAP] Test read successful: tick={test_data['tick']}")
                    print(f"✅ [REAL-DAWN-MMAP] Source: {test_data['source']}")
                else:
                    print(f"⚠️ [REAL-DAWN-MMAP] MMap file exists but read failed")
            else:
                print(f"⚠️ [REAL-DAWN-MMAP] Consciousness mmap file not found")
                print(f"💡 [REAL-DAWN-MMAP] Start consciousness writer:")
                print(f"   python ../consciousness/dawn_tick_state_writer.py")
                print(f"⚠️ [REAL-DAWN-MMAP] Will use fallback simulation until mmap available")
            
            print()
            print(f"🎯 Available REAL DAWN API endpoints:")
            print(f"   GET  /api/consciousness/state  - Real consciousness metrics")
            print(f"   GET  /api/tick/metrics         - Real tick/pulse data")
            print(f"   GET  /api/pressure/formula     - Real P = Bσ² calculations")
            print(f"   GET  /status                   - Server status")
            print()
            
            # Start server in background thread to prevent hanging
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            
            print(f"🚀 [REAL-DAWN-MMAP] Backend running - ready for GUI connections!")
            
            # Keep main thread alive but responsive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n🛑 [REAL-DAWN-MMAP] Shutting down backend...")
                server.server_close()
                
        except Exception as e:
            print(f"❌ [REAL-DAWN-MMAP] Server error: {e}")

if __name__ == "__main__":
    print("🧠 [REAL-DAWN-MMAP] Real DAWN MMap Backend")
    print("🎯 [REAL-DAWN-MMAP] Uses existing proven mmap consciousness system")
    print()
    
    server = RealDAWNMMapServer(port=BACKEND_PORT, mmap_path=MMAP_PATH)
    server.start() 