import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'checkerboardSize': [9, 6],
        'squareSize': 25,
        'stereoMode': False
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    print(f"Starting camera calibration")
    print(f"Checkerboard size: {config['checkerboardSize']}")
    print(f"Square size: {config['squareSize']} mm")
    print(f"Stereo mode: {config['stereoMode']}")
    
    # Main calibration loop
    while True:
        # Your calibration logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 