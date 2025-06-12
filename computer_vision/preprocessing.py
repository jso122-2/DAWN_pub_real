import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'denoising': True,
        'colorCorrection': True,
        'histogram': False,
        'sharpening': False
    }
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    print(f"Starting image preprocessing")
    print(f"Config: {config}")
    
    # Main preprocessing loop
    while True:
        # Your preprocessing logic here
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        main(params)
    else:
        main() 