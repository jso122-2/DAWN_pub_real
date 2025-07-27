import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'algorithm': 'DeepSORT',
        'maxAge': 30,
        'minHits': 3,
        'iouThreshold': 0.3
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    print(f"Starting object tracking with algorithm: {config['algorithm']}")
    print(f"Config: {config}")
    
    # Main tracking loop
    while True:
        # Your tracking logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 