import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'model': 'yolov8n',
        'confidence': 0.5,
        'nmsThreshold': 0.4,
        'classes': ['person', 'car', 'bicycle']
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    # Initialize YOLO with config
    from ultralytics import YOLO
    model = YOLO(config['model'])
    
    # Main processing loop
    while True:
        # Your detection logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 