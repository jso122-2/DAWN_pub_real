from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import cv2
import json
import base64
import threading
import numpy as np
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for process states
detection_enabled = False
tracking_enabled = False
depth_enabled = False
camera = None
camera_lock = threading.Lock()

# Stats tracking
frame_count = 0
start_time = time.time()
fps = 0

def initialize_camera():
    """Initialize the camera with error handling"""
    global camera
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Warning: Could not open camera, using test pattern")
            camera = None
        else:
            # Set camera properties for better performance
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            camera.set(cv2.CAP_PROP_FPS, 30)
            print("Camera initialized successfully")
    except Exception as e:
        print(f"Error initializing camera: {e}")
        camera = None

def create_test_frame():
    """Create a test pattern when camera is not available"""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Create a gradient background
    for i in range(frame.shape[0]):
        frame[i, :, 0] = int(255 * i / frame.shape[0])  # Red gradient
        frame[i, :, 1] = int(128 * (1 - i / frame.shape[0]))  # Green gradient
        frame[i, :, 2] = 100  # Blue constant
    
    # Add text overlay
    text = f"CV Server Test Pattern - {datetime.now().strftime('%H:%M:%S')}"
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Add feature status indicators
    y_offset = 100
    if detection_enabled:
        cv2.putText(frame, "DETECTION: ON", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "DETECTION: OFF", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    y_offset += 30
    if tracking_enabled:
        cv2.putText(frame, "TRACKING: ON", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "TRACKING: OFF", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    y_offset += 30
    if depth_enabled:
        cv2.putText(frame, "DEPTH: ON", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "DEPTH: OFF", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Add FPS counter
    cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    return frame

def run_detection(frame):
    """Simple detection simulation - replace with actual detection logic"""
    detections = []
    
    # Simulate some random detections
    import random
    num_detections = random.randint(0, 3)
    
    for i in range(num_detections):
        # Random bounding box
        x = random.randint(50, frame.shape[1] - 150)
        y = random.randint(50, frame.shape[0] - 150)
        width = random.randint(50, 100)
        height = random.randint(50, 100)
        
        # Random class and confidence
        classes = ['person', 'car', 'bicycle', 'dog', 'cat']
        class_name = random.choice(classes)
        confidence = random.uniform(0.6, 0.95)
        
        detection = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'class': class_name,
            'confidence': confidence
        }
        detections.append(detection)
        
        # Draw bounding box on frame
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.putText(frame, f"{class_name} {confidence:.2f}", 
                   (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return detections

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'camera_available': camera is not None,
        'detection_enabled': detection_enabled,
        'tracking_enabled': tracking_enabled,
        'depth_enabled': depth_enabled,
        'fps': fps
    })

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def get_status():
    """Get current system status"""
    return jsonify({
        'detection_enabled': detection_enabled,
        'tracking_enabled': tracking_enabled,
        'depth_enabled': depth_enabled,
        'fps': fps,
        'frame_count': frame_count,
        'uptime': time.time() - start_time
    })

def generate_frames():
    """Generate video frames for streaming"""
    global frame_count, fps
    
    with camera_lock:
        if camera is None:
            initialize_camera()
    
    while True:
        frame = None
        
        # Try to get frame from camera
        if camera is not None:
            with camera_lock:
                success, frame = camera.read()
                if not success:
                    print("Failed to read from camera, switching to test pattern")
                    frame = None
        
        # Use test pattern if no camera frame
        if frame is None:
            frame = create_test_frame()
        
        # Update FPS calculation
        frame_count += 1
        if frame_count % 30 == 0:  # Update FPS every 30 frames
            current_time = time.time()
            fps = 30 / (current_time - (start_time + (frame_count - 30) / 30))
        
        # Process frame based on enabled features
        detections = []
        if detection_enabled:
            detections = run_detection(frame)
            
            # Emit detection data via SocketIO
            socketio.emit('cv_data', {
                'type': 'detection',
                'detections': detections,
                'timestamp': datetime.now().isoformat()
            })
        
        if tracking_enabled:
            # Add tracking logic here
            pass
        
        if depth_enabled:
            # Add depth processing here
            pass
        
        # Encode frame for streaming
        try:
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                print("Failed to encode frame")
        except Exception as e:
            print(f"Error encoding frame: {e}")
        
        # Small delay to control frame rate
        time.sleep(1/30)  # Target 30 FPS

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    # Send current status to newly connected client
    socketio.emit('status_update', {
        'detection_enabled': detection_enabled,
        'tracking_enabled': tracking_enabled,
        'depth_enabled': depth_enabled,
        'fps': fps
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('cv_command')
def handle_command(data):
    """Handle commands from frontend"""
    global detection_enabled, tracking_enabled, depth_enabled
    
    command = data.get('command')
    params = data.get('params', {})
    
    print(f"Received command: {command} with params: {params}")
    
    response = {'status': 'ok', 'command': command}
    
    if command == 'toggle_detection':
        detection_enabled = not detection_enabled
        response['detection_enabled'] = detection_enabled
        print(f"Detection {'enabled' if detection_enabled else 'disabled'}")
        
    elif command == 'toggle_tracking':
        tracking_enabled = not tracking_enabled
        response['tracking_enabled'] = tracking_enabled
        print(f"Tracking {'enabled' if tracking_enabled else 'disabled'}")
        
    elif command == 'toggle_depth':
        depth_enabled = not depth_enabled
        response['depth_enabled'] = depth_enabled
        print(f"Depth processing {'enabled' if depth_enabled else 'disabled'}")
        
    elif command == 'capture_frame':
        # Capture and save current frame
        if camera is not None:
            with camera_lock:
                success, frame = camera.read()
                if success:
                    filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename, frame)
                    response['filename'] = filename
                    print(f"Frame captured: {filename}")
                else:
                    response['status'] = 'error'
                    response['error'] = 'Failed to capture frame'
        else:
            response['status'] = 'error'
            response['error'] = 'Camera not available'
    
    # Broadcast status update to all clients
    socketio.emit('status_update', {
        'detection_enabled': detection_enabled,
        'tracking_enabled': tracking_enabled,
        'depth_enabled': depth_enabled,
        'fps': fps
    })
    
    return response

def cleanup():
    """Cleanup resources"""
    global camera
    if camera is not None:
        camera.release()
        camera = None
    print("Camera resources cleaned up")

if __name__ == '__main__':
    print("Starting CV Server...")
    print("Initializing camera...")
    initialize_camera()
    
    try:
        print("Server starting on http://0.0.0.0:8081")
        print("Video feed available at: http://localhost:8081/video_feed")
        print("Health check at: http://localhost:8081/health")
        socketio.run(app, host='0.0.0.0', port=8081, debug=True)
    except KeyboardInterrupt:
        print("\nShutting down CV Server...")
    finally:
        cleanup() 