#!/usr/bin/env python3

import os
import subprocess
import datetime
import concurrent.futures
import logging
import glob

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_visualization_scripts():
    """Get all Python scripts in the visual directory."""
    # Get all .py files in the current directory
    scripts = glob.glob("*.py")
    # Exclude the batch runner itself
    scripts = [s for s in scripts if s != "visual_batch_runner.py"]
    return scripts

def run_visualization(script_name):
    """Run a single visualization script and capture its output."""
    try:
        # Create a timestamp for the output
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"visual_outputs/{script_name.replace('.py', '')}_{timestamp}.log"
        
        # Run the script and capture output
        result = subprocess.run(
            ["python3", script_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Save output to file
        with open(output_file, "w") as f:
            f.write(f"Script: {script_name}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Output:\n{result.stdout}\n")
            if result.stderr:
                f.write(f"Errors:\n{result.stderr}\n")
        
        logger.info(f"Successfully ran {script_name}")
        return True, script_name
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run {script_name}: {str(e)}")
        # Save error output
        with open(output_file, "w") as f:
            f.write(f"Script: {script_name}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Error:\n{str(e)}\n")
            if e.stdout:
                f.write(f"Output:\n{e.stdout}\n")
            if e.stderr:
                f.write(f"Errors:\n{e.stderr}\n")
        return False, script_name

def main():
    # Create output directory if it doesn't exist
    os.makedirs("visual_outputs", exist_ok=True)
    
    # Get all visualization scripts
    scripts = get_visualization_scripts()
    
    if not scripts:
        logger.error("No visualization scripts found!")
        return
    
    logger.info(f"Found {len(scripts)} visualization scripts to run")
    
    # Determine number of parallel processes (use 75% of available CPU cores)
    num_cores = max(1, int(os.cpu_count() * 0.75))
    logger.info(f"Running with {num_cores} parallel processes")
    
    # Run visualizations in parallel
    successful = 0
    failed = 0
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Submit all tasks
        future_to_script = {executor.submit(run_visualization, script): script for script in scripts}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_script):
            success, script_name = future.result()
            if success:
                successful += 1
            else:
                failed += 1
    
    # Report results
    logger.info(f"Batch run completed:")
    logger.info(f"Total scripts: {len(scripts)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")

if __name__ == "__main__":
    main() 