"""
Owl Read Simulator
Processes bloom encodings from juliet_flowers/init/ and updates owl_registry.json.
Detects high entropy blooms and manages rebloom risk assessment.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from reflection.owl.owl_memory.fractal_decoder import FractalDecoder

# Constants
INIT_DIR = "juliet_flowers/init"
OWL_REGISTRY = "owl_registry.json"
WHISPER_LOG = "whisper.log"
ENTROPY_THRESHOLD = 0.65
INTENSITY_THRESHOLD = 5

# Sample bloom strings for testing
SAMPLE_BLOOMS = [
    "cTH~+5|EN@70|CO|1",  # High entropy, high intensity
    "cBL~-3|EN@30|CO|0",  # Low entropy, low intensity
    "cOW~+7|EN@80|CO|1"   # Very high entropy, high intensity
]

class OwlReadSimulator:
    """Simulates owl reading of bloom encodings with risk assessment."""
    
    def __init__(self):
        """Initialize the simulator with proper logging and state management."""
        # Ensure directories exist
        os.makedirs(INIT_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(OWL_REGISTRY), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=WHISPER_LOG,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Initialize decoder
        self.decoder = FractalDecoder()
        
        # Initialize registry
        self.registry = self._load_registry()
        
        # Ensure sample blooms exist
        self._ensure_sample_blooms()
        
    def _ensure_sample_blooms(self) -> None:
        """Create sample bloom files if init directory is empty."""
        try:
            if not os.path.exists(INIT_DIR) or not os.listdir(INIT_DIR):
                logging.info("Creating sample bloom files")
                for i, bloom in enumerate(SAMPLE_BLOOMS):
                    filename = os.path.join(INIT_DIR, f"bloom_{i+1}.bloom")
                    with open(filename, 'w') as f:
                        f.write(bloom)
                logging.info(f"Created {len(SAMPLE_BLOOMS)} sample bloom files")
        except Exception as e:
            logging.error(f"Error creating sample blooms: {str(e)}")
        
    def _load_registry(self) -> Dict:
        """Load existing owl registry or create new one."""
        try:
            if os.path.exists(OWL_REGISTRY):
                with open(OWL_REGISTRY, 'r') as f:
                    registry = json.load(f)
                    logging.info("Loaded existing owl registry")
                    return registry
            else:
                # Create new registry
                registry = {
                    'blooms': {},
                    'rebloom_risk': False,
                    'last_updated': datetime.now().isoformat(),
                    'risk_zones': {}
                }
                self._save_registry(registry)
                logging.info("Created new owl registry")
                return registry
        except Exception as e:
            logging.error(f"Error loading owl registry: {str(e)}")
            return {
                'blooms': {},
                'rebloom_risk': False,
                'last_updated': datetime.now().isoformat(),
                'risk_zones': {}
            }
            
    def _save_registry(self, registry: Dict) -> None:
        """Save owl registry to file."""
        try:
            with open(OWL_REGISTRY, 'w') as f:
                json.dump(registry, f, indent=2)
            logging.info("Saved owl registry")
        except Exception as e:
            logging.error(f"Error saving owl registry: {str(e)}")
            
    def _load_bloom_strings(self) -> List[str]:
        """Load bloom strings from init directory."""
        bloom_strings = []
        try:
            if os.path.exists(INIT_DIR):
                bloom_files = [f for f in os.listdir(INIT_DIR) if f.endswith('.bloom')]
                if not bloom_files:
                    logging.warning("No bloom files found in init directory")
                    return []
                    
                # Sort files to ensure consistent order
                bloom_files.sort()
                
                # Load up to 3 bloom files
                for filename in bloom_files[:3]:
                    with open(os.path.join(INIT_DIR, filename), 'r') as f:
                        bloom_string = f.read().strip()
                        if self.decoder.validate_bloom_string(bloom_string):
                            bloom_strings.append(bloom_string)
                        else:
                            logging.warning(f"Invalid bloom string in {filename}")
            else:
                logging.warning(f"Init directory {INIT_DIR} not found")
        except Exception as e:
            logging.error(f"Error loading bloom strings: {str(e)}")
            
        return bloom_strings
        
    def _check_risk_conditions(self, bloom_data: Dict) -> bool:
        """Check if bloom meets risk conditions."""
        return (bloom_data['entropy'] > ENTROPY_THRESHOLD and 
                bloom_data['intensity'] > INTENSITY_THRESHOLD)
                
    def _log_high_entropy(self, bloom_id: str, bloom_data: Dict) -> None:
        """Log high entropy detection to whisper log."""
        logging.warning(
            f"High entropy bloom detected: {bloom_id}\n"
            f"Entropy: {bloom_data['entropy']:.3f}\n"
            f"Intensity: {bloom_data['intensity']}\n"
            f"Pattern: {bloom_data['pattern']}"
        )
        
    def run_owl_read(self) -> None:
        """Run the owl read simulation."""
        logging.info("Starting owl read simulation")
        
        # Load bloom strings
        bloom_strings = self._load_bloom_strings()
        if not bloom_strings:
            logging.error("No valid bloom strings found")
            return
            
        # Process each bloom
        for i, bloom_string in enumerate(bloom_strings):
            bloom_id = f"bloom_{i+1}"
            
            # Decode bloom
            bloom_data = self.decoder.decode_bloom_string(bloom_string)
            
            # Store in registry
            self.registry['blooms'][bloom_id] = {
                'data': bloom_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Check risk conditions
            if self._check_risk_conditions(bloom_data):
                self.registry['rebloom_risk'] = True
                self.registry['risk_zones'][bloom_id] = bloom_data['entropy']
                self._log_high_entropy(bloom_id, bloom_data)
                
        # Update registry timestamp
        self.registry['last_updated'] = datetime.now().isoformat()
        
        # Save registry
        self._save_registry(self.registry)
        logging.info("Owl read simulation complete")

def main():
    """Main entry point for the owl read simulator."""
    try:
        simulator = OwlReadSimulator()
        simulator.run_owl_read()
        print(f"Simulation complete. Check {WHISPER_LOG} for details.")
    except Exception as e:
        print(f"Error running simulation: {str(e)}")
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main() 