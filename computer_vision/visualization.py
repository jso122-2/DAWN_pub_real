import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'mode': '2D',
        'showTrajectories': True,
        'showDepth': False,
        'showPointCloud': False
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    print(f"Starting visualization engine in {config['mode']} mode")
    print(f"Config: {config}")
    
    # Main visualization loop
    while True:
        # Your visualization logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 