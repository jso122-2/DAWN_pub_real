import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'method': 'SGBM',
        'numDisparities': 96,
        'blockSize': 11,
        'preFilterCap': 63
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    print(f"Starting depth estimation with method: {config['method']}")
    print(f"Config: {config}")
    
    # Main depth estimation loop
    while True:
        # Your depth estimation logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 