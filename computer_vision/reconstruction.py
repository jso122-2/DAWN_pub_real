import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'algorithm': 'Poisson',
        'depth': 9,
        'scale': 1.1,
        'pointWeight': 4.0
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    print(f"Starting 3D reconstruction with algorithm: {config['algorithm']}")
    print(f"Config: {config}")
    
    # Main reconstruction loop
    while True:
        # Your reconstruction logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 