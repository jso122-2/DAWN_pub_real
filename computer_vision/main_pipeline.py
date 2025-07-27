import json
import sys

def main(params=None, modules=None):
    # Default parameters
    config = {
        'fps': 30,
        'resolution': [1920, 1080],
        'recordOutput': False,
        'debugMode': False
    }
    
    # Default modules (matches processs_viewer.jsx)
    default_modules = [
        { 'name': 'Camera Capture', 'enabled': True },
        { 'name': 'Object Detection', 'enabled': True },
        { 'name': 'Object Tracking', 'enabled': True },
        { 'name': 'Depth Estimation', 'enabled': False },
        { 'name': '3D Reconstruction', 'enabled': False },
        { 'name': 'Point Cloud Gen', 'enabled': False },
        { 'name': 'Visualization', 'enabled': True }
    ]
    
    # Override with GUI parameters
    if params:
        config.update(params)
    
    # Use provided modules or defaults
    active_modules = modules if modules else default_modules
    
    print(f"Starting main CV pipeline")
    print(f"Config: {config}")
    print(f"Active modules: {[m['name'] for m in active_modules if m['enabled']]}")
    
    # Initialize pipeline components based on enabled modules
    pipeline_components = {}
    
    for module in active_modules:
        if module['enabled']:
            module_name = module['name']
            print(f"Initializing module: {module_name}")
            
            # Initialize specific modules here
            if module_name == 'Camera Capture':
                # Initialize camera
                pass
            elif module_name == 'Object Detection':
                # Initialize detection
                pass
            elif module_name == 'Object Tracking':
                # Initialize tracking
                pass
            elif module_name == 'Depth Estimation':
                # Initialize depth estimation
                pass
            elif module_name == '3D Reconstruction':
                # Initialize reconstruction
                pass
            elif module_name == 'Point Cloud Gen':
                # Initialize point cloud generation
                pass
            elif module_name == 'Visualization':
                # Initialize visualization
                pass
    
    # Main processing loop
    while True:
        # Your main pipeline logic here
        # Process through enabled modules
        # Check for stop signal from GUI
        pass

if __name__ == "__main__":
    # Can run standalone or from GUI
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
        modules = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
        main(params, modules)
    else:
        main() 