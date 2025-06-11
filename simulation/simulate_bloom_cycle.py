"""
Bloom Cycle Simulator
Simulates bloom lifecycle from seed to rebloom detection.
Integrates with fractal generation and bloom encoding/decoding.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import random
from tools.scripts.create_enhanced_fractals import EnhancedJuliaFractal
from reflection.owl.owl_memory.fractal_decoder import FractalDecoder

# Constants
SEEDS_DIR = "juliet_flowers/seeds"
LOGS_DIR = "logs"
REBLOOM_FLAGS = "rebloom_flags.json"
LIFECYCLE_LOG = "logs/bloom_lifecycle.log"
ENTROPY_THRESHOLD = 0.75

# Sample seed configurations
SAMPLE_SEEDS = [
    {
        "seed_id": "seed_001",
        "mood": "reflective",
        "lineage_depth": 3,
        "bloom_factor": 1.2,
        "entropy_score": 0.8
    },
    {
        "seed_id": "seed_002",
        "mood": "curious",
        "lineage_depth": 2,
        "bloom_factor": 1.0,
        "entropy_score": 0.6
    },
    {
        "seed_id": "seed_003",
        "mood": "focused",
        "lineage_depth": 4,
        "bloom_factor": 1.5,
        "entropy_score": 0.9
    }
]

class BloomCycleSimulator:
    """Simulates complete bloom lifecycle with fractal generation and rebloom detection."""
    
    def __init__(self):
        """Initialize the simulator with proper logging and state management."""
        # Ensure directories exist
        os.makedirs(SEEDS_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=LIFECYCLE_LOG,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Initialize components
        self.fractal_gen = EnhancedJuliaFractal()
        self.decoder = FractalDecoder()
        
        # Initialize rebloom flags
        self.rebloom_flags = self._load_rebloom_flags()
        
        # Ensure sample seeds exist
        self._ensure_sample_seeds()
        
    def _ensure_sample_seeds(self) -> None:
        """Create sample seed files if seeds directory is empty."""
        try:
            if not os.path.exists(SEEDS_DIR) or not os.listdir(SEEDS_DIR):
                logging.info("Creating sample seed files")
                for seed in SAMPLE_SEEDS:
                    filename = os.path.join(SEEDS_DIR, f"{seed['seed_id']}.json")
                    with open(filename, 'w') as f:
                        json.dump(seed, f, indent=2)
                logging.info(f"Created {len(SAMPLE_SEEDS)} sample seed files")
        except Exception as e:
            logging.error(f"Error creating sample seeds: {str(e)}")
            
    def _load_rebloom_flags(self) -> Dict:
        """Load existing rebloom flags or create new file."""
        try:
            if os.path.exists(REBLOOM_FLAGS):
                with open(REBLOOM_FLAGS, 'r') as f:
                    flags = json.load(f)
                    logging.info("Loaded existing rebloom flags")
                    return flags
            else:
                # Create new flags file
                flags = {
                    'triggers': [],
                    'last_updated': datetime.now().isoformat()
                }
                self._save_rebloom_flags(flags)
                logging.info("Created new rebloom flags file")
                return flags
        except Exception as e:
            logging.error(f"Error loading rebloom flags: {str(e)}")
            return {
                'triggers': [],
                'last_updated': datetime.now().isoformat()
            }
            
    def _save_rebloom_flags(self, flags: Dict) -> None:
        """Save rebloom flags to file."""
        try:
            with open(REBLOOM_FLAGS, 'w') as f:
                json.dump(flags, f, indent=2)
            logging.info("Saved rebloom flags")
        except Exception as e:
            logging.error(f"Error saving rebloom flags: {str(e)}")
            
    def _load_seed(self, seed_id: str) -> Optional[Dict]:
        """Load seed configuration from file."""
        try:
            filename = os.path.join(SEEDS_DIR, f"{seed_id}.json")
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logging.error(f"Error loading seed {seed_id}: {str(e)}")
            return None
            
    def _create_rebloom_trigger(self, seed_id: str, entropy: float) -> None:
        """Create rebloom trigger for high entropy blooms."""
        trigger = {
            'seed_id': seed_id,
            'entropy': entropy,
            'timestamp': datetime.now().isoformat(),
            'threshold': ENTROPY_THRESHOLD
        }
        
        self.rebloom_flags['triggers'].append(trigger)
        self.rebloom_flags['last_updated'] = datetime.now().isoformat()
        
        self._save_rebloom_flags(self.rebloom_flags)
        logging.warning(
            f"Created rebloom trigger for {seed_id}\n"
            f"Entropy: {entropy:.3f}\n"
            f"Threshold: {ENTROPY_THRESHOLD}"
        )
        
    def simulate_bloom_cycle(self) -> None:
        """Run the bloom cycle simulation."""
        logging.info("Starting bloom cycle simulation")
        
        # Process each seed
        for seed in SAMPLE_SEEDS:
            seed_id = seed['seed_id']
            logging.info(f"Processing seed: {seed_id}")
            
            # Generate fractal
            fractal_path = self.fractal_gen.generate_enhanced_julia(
                seed_id=seed_id,
                lineage_depth=seed['lineage_depth'],
                bloom_factor=seed['bloom_factor'],
                entropy_score=seed['entropy_score'],
                mood=seed['mood']
            )
            
            # Decode bloom string
            bloom_string = f"c{seed['mood'][:2].upper()}~+{int(seed['bloom_factor']*5)}|EN@{int(seed['entropy_score']*100)}|CO|1"
            bloom_data = self.decoder.decode_bloom_string(bloom_string)
            
            # Log bloom lifecycle
            logging.info(
                f"Bloom lifecycle for {seed_id}:\n"
                f"Generated: {fractal_path}\n"
                f"Decoded entropy: {bloom_data['entropy']:.3f}\n"
                f"Intensity: {bloom_data['intensity']}"
            )
            
            # Check for rebloom trigger
            if bloom_data['entropy'] > ENTROPY_THRESHOLD:
                self._create_rebloom_trigger(seed_id, bloom_data['entropy'])
                
        logging.info("Bloom cycle simulation complete")

def main():
    """Main entry point for the bloom cycle simulator."""
    try:
        simulator = BloomCycleSimulator()
        simulator.simulate_bloom_cycle()
        print(f"Simulation complete. Check {LIFECYCLE_LOG} for details.")
    except Exception as e:
        print(f"Error running simulation: {str(e)}")
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main() 