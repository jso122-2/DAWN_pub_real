import argparse
import json
import importlib
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('script', help='Script to run')
    parser.add_argument('--params', type=str, default='{}')
    parser.add_argument('--modules', type=str, default='[]')
    
    args = parser.parse_args()
    
    # Parse parameters
    params = json.loads(args.params)
    modules = json.loads(args.modules)
    
    # Import and run the specified script
    script_name = args.script.replace('.py', '')
    module = importlib.import_module(script_name)
    
    # Pass parameters to the module's main function
    if hasattr(module, 'main'):
        module.main(params, modules)
    else:
        print(f"No main function found in {script_name}")

if __name__ == "__main__":
    main() 