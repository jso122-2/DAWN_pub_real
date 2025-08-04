# Add parent directory to Python path for imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Visual API Server

Simple HTTP server that provides visual data to the Tauri GUI.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import time
from datetime import datetime

# Import our visual integration
try:
    from visual.visual_integration import get_visual_integration, get_current_visual_data, get_available_visual_modules
    VISUAL_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Visual integration not available: {e}")
    VISUAL_INTEGRATION_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for Tauri GUI

# Initialize visual integration
if VISUAL_INTEGRATION_AVAILABLE:
    visual_integration = get_visual_integration()
else:
    visual_integration = None

@app.route('/api/visual/status', methods=['GET'])
def get_status():
    """Get visual system status"""
    return jsonify({
        'status': 'connected' if VISUAL_INTEGRATION_AVAILABLE else 'demo',
        'timestamp': datetime.now().isoformat(),
        'visual_integration_available': VISUAL_INTEGRATION_AVAILABLE
    })

@app.route('/api/visual/data', methods=['GET'])
def get_visual_data():
    """Get current visual data"""
    if VISUAL_INTEGRATION_AVAILABLE:
        data = get_current_visual_data()
    else:
        # Generate demo data
        import math
        current_time = time.time()
        tick_number = int(current_time) % 1000
        
        data = {
            'tick_number': tick_number,
            'timestamp': current_time,
            'scup': 0.5 + 0.3 * math.sin(current_time * 0.1),
            'entropy': 0.4 + 0.4 * math.sin(current_time * 0.08),
            'heat': 25.0 + 10.0 * math.sin(current_time * 0.05),
            'zone': ['CALM', 'STABLE', 'OSCILLATING', 'TRENDING'][tick_number % 4],
            'mood': ['serene', 'focused', 'curious', 'contemplative'][tick_number % 4],
            'active_sigils': ['attention', 'memory'] if tick_number % 3 == 0 else [],
            'rebloom_count': tick_number % 5,
            'tracer_alerts': ['pressure_warning'] if tick_number % 10 == 0 else []
        }
    
    return jsonify(data)

@app.route('/api/visual/modules', methods=['GET'])
def get_modules():
    """Get available visual modules"""
    if VISUAL_INTEGRATION_AVAILABLE:
        modules = get_available_visual_modules()
    else:
        # Demo modules
        modules = {
            'tick_pulse': {
                'name': 'Tick Pulse',
                'description': 'Real-time cognitive heartbeat visualization',
                'type': 'real-time'
            },
            'consciousness_constellation': {
                'name': 'Consciousness Constellation',
                'description': '3D SCUP trajectory visualization',
                'type': 'real-time'
            },
            'heat_monitor': {
                'name': 'Heat Monitor',
                'description': 'Cognitive heat intensity gauge',
                'type': 'real-time'
            },
            'dawn_mood_state': {
                'name': 'Mood State',
                'description': 'Emotional landscape heatmap',
                'type': 'real-time'
            }
        }
    
    return jsonify(modules)

@app.route('/api/visual/generate/<module_id>', methods=['POST'])
def generate_visualization(module_id):
    """Generate visualization for a specific module"""
    try:
        # Get current data
        if VISUAL_INTEGRATION_AVAILABLE:
            data = get_current_visual_data()
            result = visual_integration.generate_visualization(module_id, data)
        else:
            # Generate demo visualization
            import math
            current_time = time.time()
            timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
            
            if module_id == 'tick_pulse':
                result = f"""
TICK PULSE VISUALIZATION
==========================
Time: {timestamp}
Module: Tick Pulse
Description: Real-time cognitive heartbeat visualization

Current State:
  Tick Number: {int(current_time) % 1000}
  SCUP: {0.5 + 0.3 * math.sin(current_time * 0.1):.3f}
  Entropy: {0.4 + 0.4 * math.sin(current_time * 0.08):.3f}
  Heat: {25.0 + 10.0 * math.sin(current_time * 0.05):.1f}C
  Zone: CALM
  Mood: focused

Pulse Analysis:
  Amplitude: {0.5 + 0.3 * math.sin(current_time * 0.1):.2f}
  Frequency: {0.1 + 0.05 * math.sin(current_time * 0.05):.3f} Hz
  Phase: {current_time * 0.1:.1f} rad

Visual Representation:
{'#' * int(10 + 5 * math.sin(current_time * 0.1))}
{'.' * (20 - int(10 + 5 * math.sin(current_time * 0.1)))}
"""
            else:
                result = f"""
{module_id.upper().replace('_', ' ')} VISUALIZATION
{'=' * (len(module_id) + 15)}
Time: {timestamp}
Module: {module_id.title()}
Description: Visualization module

Status: Demo mode - no real data available
"""
        
        return jsonify({
            'success': True,
            'module_id': module_id,
            'visualization': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'module_id': module_id,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/visual/process-tick', methods=['POST'])
def process_tick():
    """Process tick data from DAWN system"""
    try:
        if not VISUAL_INTEGRATION_AVAILABLE:
            return jsonify({'success': False, 'error': 'Visual integration not available'}), 400
        
        tick_data = request.json
        if not tick_data:
            return jsonify({'success': False, 'error': 'No tick data provided'}), 400
        
        visual_integration.process_tick(tick_data)
        
        return jsonify({
            'success': True,
            'message': 'Tick data processed',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🌅 DAWN Visual API Server")
    print("=" * 40)
    print(f"Visual Integration: {'✅ Available' if VISUAL_INTEGRATION_AVAILABLE else '⚠️ Demo Mode'}")
    print("🚀 Starting server on http://localhost:5001")
    print("📡 Available endpoints:")
    print("  GET  /api/visual/status")
    print("  GET  /api/visual/data")
    print("  GET  /api/visual/modules")
    print("  POST /api/visual/generate/<module_id>")
    print("  POST /api/visual/process-tick")
    print("\nPress Ctrl+C to stop...")
    
    app.run(host='0.0.0.0', port=5001, debug=False) 