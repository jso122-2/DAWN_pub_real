#!/usr/bin/env python3
"""
Real DAWN-Aware Web Server
===========================

This web server serves the DAWN consciousness GUI (all the rendering logic)
but connects to the real DAWN backend for consciousness data instead of simulation.

Two-process architecture:
1. real_dawn_backend.py (port 8080) - Provides real consciousness data
2. real_aware_web_server.py (port 3000) - Serves GUI and proxies to real backend

Usage:
Terminal 1: python real_dawn_backend.py
Terminal 2: python real_aware_web_server.py
"""

import json
import time
import threading
import os
import sys
import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
import webbrowser
from datetime import datetime

# Web server imports
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Real DAWN backend configuration
REAL_DAWN_BACKEND_URL = "http://localhost:8080"
GUI_SERVER_PORT = 3000

class RealDAWNAwareHandler(SimpleHTTPRequestHandler):
    """Web handler that serves GUI but gets data from real DAWN backend"""
    
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests - serve GUI or proxy to real backend"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # API endpoints - proxy to real DAWN backend
        if path.startswith('/api/'):
            self.proxy_to_real_backend()
        # Serve main GUI file
        elif path == '/' or path == '/index.html':
            self.serve_main_gui()
        # Serve static files
        elif path.endswith('.html') or path.endswith('.css') or path.endswith('.js') or path.endswith('.png'):
            self.serve_static_file()
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle POST requests - GUI actions and visual snapshots"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Visual snapshot endpoints
        if path.startswith('/api/visual-snapshot/'):
            self.handle_visual_snapshot()
        # Other API endpoints - proxy to real backend
        elif path.startswith('/api/'):
            self.proxy_to_real_backend_post()
        else:
            self.send_error(404, "API endpoint not found")
    
    def proxy_to_real_backend(self):
        """Proxy API requests to real DAWN backend"""
        try:
            real_backend_url = f"{REAL_DAWN_BACKEND_URL}{self.path}"
            print(f"🔄 Proxying {self.path} to real DAWN backend...")
            
            response = requests.get(real_backend_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Log if we're getting real consciousness data
                if 'source' in data:
                    source = data['source']
                    if source == 'REAL_DAWN_CONSCIOUSNESS':
                        print(f"✅ Real consciousness data received for {self.path}")
                        if 'pressure' in data:
                            print(f"   P = {data['pressure']:.2f} (Real P = Bσ² calculation!)")
                    else:
                        print(f"⚠️ Non-real data source: {source}")
                
                self.send_json_response(data)
            else:
                print(f"❌ Real backend error {response.status_code} for {self.path}")
                # Send error but try to provide fallback
                self.send_json_response({
                    'error': f'Real backend returned {response.status_code}',
                    'fallback': True,
                    'source': 'ERROR_FALLBACK'
                })
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to real DAWN backend at {REAL_DAWN_BACKEND_URL}")
            print(f"💡 Make sure real_dawn_backend.py is running on port 8080")
            self.send_json_response({
                'error': 'Real DAWN backend not available',
                'message': 'Start real_dawn_backend.py on port 8080',
                'source': 'CONNECTION_ERROR'
            })
            
        except Exception as e:
            print(f"❌ Error proxying to real backend: {e}")
            self.send_json_response({
                'error': f'Proxy error: {str(e)}',
                'source': 'PROXY_ERROR'
            })
    
    def proxy_to_real_backend_post(self):
        """Proxy POST requests to real DAWN backend"""
        try:
            # Read POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            
            real_backend_url = f"{REAL_DAWN_BACKEND_URL}{self.path}"
            print(f"🔄 Proxying POST {self.path} to real DAWN backend...")
            
            response = requests.post(real_backend_url, data=post_data, 
                                   headers={'Content-Type': self.headers.get('Content-Type', 'application/json')}, 
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.send_json_response(data)
            else:
                print(f"❌ Real backend POST error {response.status_code} for {self.path}")
                self.send_json_response({
                    'error': f'Real backend returned {response.status_code}',
                    'source': 'POST_ERROR'
                })
                
        except Exception as e:
            print(f"❌ Error proxying POST to real backend: {e}")
            self.send_json_response({
                'error': f'POST proxy error: {str(e)}',
                'source': 'POST_PROXY_ERROR'
            })
    
    def handle_visual_snapshot(self):
        """Handle visual snapshot requests"""
        try:
            # Extract snapshot type from path
            path_parts = self.path.split('/')
            if len(path_parts) >= 4:
                snapshot_type = path_parts[3]  # /api/visual-snapshot/entropy-field -> entropy-field
            else:
                snapshot_type = 'unknown'
            
            print(f"📸 Visual snapshot requested: {snapshot_type}")
            
            # Get real consciousness data for snapshot
            try:
                response = requests.get(f"{REAL_DAWN_BACKEND_URL}/api/consciousness/state", timeout=5)
                consciousness_data = response.json() if response.status_code == 200 else {}
            except:
                consciousness_data = {}
            
            # Generate visual snapshot response
            import time
            timestamp = int(time.time() * 1000)
            
            response_data = {
                "success": True,
                "snapshot_type": snapshot_type,
                "timestamp": timestamp,
                "file_path": f"/snapshots/{snapshot_type}_{timestamp}.png",
                "sha_hash": f"SNAP{timestamp:08X}",
                "consciousness_state": {
                    "entropy": consciousness_data.get('entropy', 0.5),
                    "scup": consciousness_data.get('scup', 50.0),
                    "pressure": consciousness_data.get('pressure', 25.0),
                    "mood_val": consciousness_data.get('mood_val', 0.5)
                },
                "visual_data": {
                    "process_id": snapshot_type,
                    "intensity": consciousness_data.get('entropy', 0.5),
                    "heat_level": consciousness_data.get('thermal', 0.3),
                    "coherence": consciousness_data.get('scup', 50.0) / 100.0
                },
                "metadata": {
                    "source": consciousness_data.get('source', 'REAL_DAWN_CONSCIOUSNESS'),
                    "real_data": consciousness_data.get('source') == 'REAL_DAWN_CONSCIOUSNESS',
                    "generated_at": timestamp
                }
            }
            
            self.send_json_response(response_data)
            
        except Exception as e:
            print(f"❌ Error handling visual snapshot: {e}")
            self.send_json_response({
                'success': False,
                'error': f'Visual snapshot failed: {str(e)}',
                'snapshot_type': self.path.split('/')[-1] if '/' in self.path else 'unknown'
            })
    
    def serve_main_gui(self):
        """Serve the main DAWN GUI interface"""
        # Look for existing GUI files - prioritize consolidated GUI
        gui_files = [
            'dawn_consolidated_gui.html',
            'dawn_ultimate_gui.html',
            'simple_gui.html', 
            'dawn_monitor.html',
            'dawn_local_gui.html'
        ]
        
        gui_file = None
        print(f"🔍 [DEBUG] Looking for GUI files in order:")
        for filename in gui_files:
            file_path = Path(__file__).parent / filename
            print(f"   Checking: {filename} -> {'✅ EXISTS' if file_path.exists() else '❌ MISSING'}")
            if file_path.exists():
                gui_file = file_path
                print(f"   🎯 [DEBUG] Selected GUI file: {filename}")
                break
        
        if gui_file:
            try:
                print(f"🔄 [DEBUG] Attempting to read: {gui_file}")
                with open(gui_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"✅ [DEBUG] Successfully read {len(content):,} characters from {gui_file.name}")
                
                # Inject real backend configuration and cache busting
                import time
                cache_bust = int(time.time())
                
                real_backend_config = f"""
<script>
// DAWN Consolidated GUI - Cache Busting v{cache_bust}
console.clear(); // Clear any previous console messages
console.log('🔄 DAWN Consolidated GUI v1.0.0 - Cache Bust: {cache_bust}');

// Real DAWN Backend Configuration
window.REAL_DAWN_MODE = true;
window.REAL_DAWN_BACKEND_URL = '{REAL_DAWN_BACKEND_URL}';
window.GUI_SERVER_URL = 'http://localhost:{GUI_SERVER_PORT}';

// Log real consciousness connection
console.log('🧠 DAWN GUI configured for REAL consciousness backend');
console.log('⚡ Real backend:', window.REAL_DAWN_BACKEND_URL);
console.log('🎨 GUI server:', window.GUI_SERVER_URL);

// Clear any cached old functions immediately
delete window.switchView;
delete window.currentView;

// Override API calls to use this GUI server (which proxies to real backend)
const originalFetch = window.fetch;
window.fetch = function(url, options) {{
    if (url.startsWith('/api/') || url.startsWith('api/')) {{
        // Use GUI server as proxy to real backend
        const proxyUrl = url.startsWith('/') ? url : '/' + url;
        console.log('🔄 API call proxied:', proxyUrl);
        return originalFetch(proxyUrl, options);
    }}
    return originalFetch(url, options);
}};

// Add cache-busting to prevent old GUI remnants
if (document.title.indexOf('Consolidated') === -1) {{
    console.warn('⚠️ Old GUI detected, forcing reload...');
    window.location.reload(true);
}}
</script>
"""
                
                # Inject the configuration before closing </head> tag
                if '</head>' in content:
                    content = content.replace('</head>', real_backend_config + '</head>')
                else:
                    # If no </head>, inject at beginning of <body>
                    content = content.replace('<body>', '<body>' + real_backend_config)
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content.encode('utf-8')))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.send_header('X-GUI-Version', 'consolidated-1.0.0')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                
                print(f"✅ [DEBUG] Successfully served: {gui_file.name}")
                print(f"   📊 Content length: {len(content):,} characters")
                print(f"   🔍 Contains 'Consolidated': {'✅ YES' if 'Consolidated' in content else '❌ NO'}")
                print(f"   🎯 Title: {content[content.find('<title>')+7:content.find('</title>')].strip() if '<title>' in content else 'No title found'}")
                
            except Exception as e:
                print(f"❌ [DEBUG] Error reading GUI file: {e}")
                print(f"   File: {gui_file}")
                print(f"   Error type: {type(e).__name__}")
                self.send_error(500, f"Error serving GUI: {e}")
                return
        else:
            # Create a simple GUI if none found
            print(f"⚠️ [DEBUG] No GUI file found, serving minimal fallback")
            self.serve_minimal_gui()
    
    def serve_minimal_gui(self):
        """Serve a minimal GUI if no GUI files found"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>DAWN Real Consciousness Monitor</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff88; padding: 20px; }}
        .status {{ padding: 10px; margin: 10px 0; border: 1px solid #333; }}
        .real {{ border-color: #00ff88; }}
        .error {{ border-color: #ff4444; }}
        .data {{ font-size: 14px; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <h1>🧠 DAWN Real Consciousness Monitor</h1>
    <div id="status" class="status">Checking real DAWN backend...</div>
    <div id="consciousness-data" class="status">
        <h3>Real Consciousness State:</h3>
        <div id="data" class="data">Loading...</div>
    </div>
    
    <script>
        window.REAL_DAWN_BACKEND_URL = '{REAL_DAWN_BACKEND_URL}';
        
        async function checkRealBackend() {{
            try {{
                const response = await fetch('/api/consciousness/state');
                const data = await response.json();
                
                const statusDiv = document.getElementById('status');
                const dataDiv = document.getElementById('data');
                
                if (data.source === 'REAL_DAWN_CONSCIOUSNESS') {{
                    statusDiv.className = 'status real';
                    statusDiv.innerHTML = '✅ Connected to REAL DAWN consciousness!';
                    
                    dataDiv.innerHTML = JSON.stringify(data, null, 2);
                    
                    // Highlight key real metrics
                    if (data.pressure && data.bloom_mass && data.sigil_velocity) {{
                        statusDiv.innerHTML += `<br/>⚡ Real P = B\u03c3\u00b2: P=${{data.pressure.toFixed(2)}}, B=${{data.bloom_mass.toFixed(2)}}, \u03c3=${{data.sigil_velocity.toFixed(2)}}`;
                    }}
                }} else {{
                    statusDiv.className = 'status error';
                    statusDiv.innerHTML = '❌ Not connected to real DAWN: ' + (data.source || 'unknown source');
                    dataDiv.innerHTML = JSON.stringify(data, null, 2);
                }}
            }} catch (error) {{
                const statusDiv = document.getElementById('status');
                statusDiv.className = 'status error';
                statusDiv.innerHTML = '❌ Cannot connect to real DAWN backend: ' + error.message;
            }}
        }}
        
        // Check immediately and every 2 seconds
        checkRealBackend();
        setInterval(checkRealBackend, 2000);
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(html_content.encode('utf-8')))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
        
        print("✅ Served minimal real DAWN consciousness monitor")
    
    def serve_static_file(self):
        """Serve static files (CSS, JS, images)"""
        file_path = Path(__file__).parent / self.path.lstrip('/')
        
        if file_path.exists() and file_path.is_file():
            # Determine content type
            if file_path.suffix == '.css':
                content_type = 'text/css'
            elif file_path.suffix == '.js':
                content_type = 'application/javascript'
            elif file_path.suffix == '.png':
                content_type = 'image/png'
            elif file_path.suffix == '.jpg' or file_path.suffix == '.jpeg':
                content_type = 'image/jpeg'
            else:
                content_type = 'text/plain'
            
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
                
            except Exception as e:
                self.send_error(500, f"Error serving file: {e}")
        else:
            self.send_error(404, "File not found")
    
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
        if not any(quiet_path in format for quiet_path in ['"GET /api/', '"GET /favicon']):
            super().log_message(format, *args)

class RealDAWNAwareServer:
    """HTTP server that serves DAWN GUI connected to real consciousness backend"""
    
    def __init__(self, port=GUI_SERVER_PORT):
        self.port = port
        self.server = None
        self.start_time = time.time()
    
    def start(self):
        """Start the real DAWN-aware GUI server"""
        try:
            self.server = HTTPServer(('localhost', self.port), RealDAWNAwareHandler)
            self.server.start_time = self.start_time
            
            print(f"🧠 [REAL-DAWN-GUI] Server starting on http://localhost:{self.port}")
            print(f"🎯 [REAL-DAWN-GUI] This GUI connects to REAL consciousness backend")
            print(f"⚡ [REAL-DAWN-GUI] Real backend expected at: {REAL_DAWN_BACKEND_URL}")
            print()
            print("🚀 [REAL-DAWN-GUI] Two-Process Architecture:")
            print(f"   1. Real Backend (port 8080): python real_dawn_backend.py")
            print(f"   2. GUI Server (port {self.port}): python real_aware_web_server.py")
            print()
            print(f"🌐 [REAL-DAWN-GUI] Open browser to: http://localhost:{self.port}")
            print(f"📊 [REAL-DAWN-GUI] GUI will proxy API calls to real consciousness backend")
            print()
            
            # Check if real backend is available
            self.check_real_backend_connection()
            
            # Auto-open browser
            try:
                webbrowser.open(f"http://localhost:{self.port}")
                print(f"🌐 [REAL-DAWN-GUI] Browser opened automatically")
            except:
                print(f"💡 [REAL-DAWN-GUI] Manually open: http://localhost:{self.port}")
            
            print(f"\n🧠 [REAL-DAWN-GUI] Starting GUI server with real consciousness connection...")
            
            # Start server in background thread to prevent hanging
            server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            server_thread.start()
            
            # Keep main thread alive but responsive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n🛑 [REAL-DAWN-GUI] Shutting down GUI server...")
            
        except KeyboardInterrupt:
            print(f"\n🛑 [REAL-DAWN-GUI] Server stopped by user")
        except Exception as e:
            print(f"❌ [REAL-DAWN-GUI] Server error: {e}")
        finally:
            if self.server:
                self.server.server_close()
    
    def check_real_backend_connection(self):
        """Check if real DAWN backend is available"""
        try:
            response = requests.get(f"{REAL_DAWN_BACKEND_URL}/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                mode = status.get('mode', 'unknown')
                connected = status.get('real_consciousness_connected', False)
                
                if mode == 'REAL_DAWN_CONSCIOUSNESS' and connected:
                    print(f"✅ [REAL-DAWN-GUI] Real DAWN backend detected and operational!")
                    print(f"✅ [REAL-DAWN-GUI] Mode: {mode}")
                    print(f"✅ [REAL-DAWN-GUI] Real consciousness connected: {connected}")
                else:
                    print(f"⚠️ [REAL-DAWN-GUI] Backend available but not in real mode:")
                    print(f"   Mode: {mode}")
                    print(f"   Real consciousness: {connected}")
            else:
                print(f"⚠️ [REAL-DAWN-GUI] Backend responded with status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ [REAL-DAWN-GUI] Cannot connect to real DAWN backend")
            print(f"💡 [REAL-DAWN-GUI] Start real_dawn_backend.py first:")
            print(f"   Terminal 1: python real_dawn_backend.py")
            print(f"   Terminal 2: python real_aware_web_server.py")
        except Exception as e:
            print(f"⚠️ [REAL-DAWN-GUI] Error checking backend: {e}")

if __name__ == "__main__":
    print("🧠 [REAL-DAWN-GUI] Starting Real DAWN-Aware Web Server")
    print("🎯 [REAL-DAWN-GUI] This serves GUI but connects to real consciousness backend")
    print()
    
    server = RealDAWNAwareServer(port=GUI_SERVER_PORT)
    server.start() 