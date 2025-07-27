"""
Owl Bloom Parser Module

This module implements the recursive scanning and parsing of fractal bloom strings
for Owl's memory system. It integrates with the fractal decoder to build a semantic
memory registry of bloom states.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

from .fractal_decoder import FractalDecoder

# Configure logging
logging.basicConfig(
    filename='logs/whisper.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class OwlBloomParser:
    """Parser for scanning and interpreting bloom strings in the filesystem."""
    
    def __init__(self):
        self.decoder = FractalDecoder()
        self.scan_directories = [
            "juliet_flowers/init",
            "juliet_flowers/bloom_metadata"
        ]
        self.registry_path = Path("reflection/owl/owl_memory/owl_registry.json")
        
    def write_registry(self, data: List[Dict]) -> None:
        """
        Save parsed bloom metadata into owl_registry.json.
        
        Args:
            data: List of dictionaries containing decoded bloom data
            
        The registry format is:
        {
            "blooms": {
                "seed_id": {
                    "depth": int,
                    "pattern": str,
                    "texture": str,
                    "modifier": str,
                    "intensity": int,
                    "entropy": float,
                    "color_override": bool,
                    "mood": str,
                    "rebloom_risk": bool
                },
                ...
            },
            "last_updated": str
        }
        """
        # Create registry structure
        registry = {
            "blooms": {},
            "last_updated": datetime.now().isoformat()
        }
        
        # Convert list to dictionary using seed_id as key
        for bloom in data:
            seed_id = bloom.pop('seed_id')  # Remove seed_id from bloom data
            registry["blooms"][seed_id] = bloom
            
        # Ensure directory exists
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        try:
            with open(self.registry_path, 'w') as f:
                json.dump(registry, f, indent=2)
            logging.info(f"Registry updated with {len(data)} blooms")
        except Exception as e:
            logging.error(f"Failed to write registry: {e}")
            raise
            
    def _scan_file(self, file_path: Path) -> List[Dict]:
        """
        Scan a single file for bloom strings and decode them.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            List of dictionaries containing decoded bloom data
        """
        blooms = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple line-by-line scan for bloom strings
                for line in content.split('\n'):
                    if self.decoder.validate_bloom_string(line):
                        try:
                            # Decode the bloom string
                            bloom_data = self.decoder.decode_bloom_string(line)
                            
                            # Add additional metadata
                            bloom_data.update({
                                'seed_id': datetime.now().strftime("%Y%m%d-%H%M-BF0"),
                                'mood': self._extract_mood(line),
                                'rebloom_risk': self._calculate_rebloom_risk(bloom_data)
                            })
                            
                            blooms.append(bloom_data)
                            
                            # Log high entropy blooms
                            if bloom_data['entropy'] > 0.6:
                                logging.info(
                                    f"Owl observed entropy bloom at depth {bloom_data['depth']}. "
                                    f"Entropy: {bloom_data['entropy']:.2f}"
                                )
                        except ValueError as e:
                            logging.warning(f"Failed to decode bloom string in {file_path}: {e}")
        except Exception as e:
            logging.error(f"Error scanning file {file_path}: {e}")
            
        return blooms
        
    def _extract_mood(self, bloom_string: str) -> str:
        """
        Extract mood information from bloom string if present.
        
        Args:
            bloom_string: The bloom string to analyze
            
        Returns:
            Extracted mood or 'neutral' if none found
        """
        # Look for mood indicators in the pattern
        if 'TH' in bloom_string:
            return 'thoughtful'
        elif 'AN' in bloom_string:
            return 'anxious'
        elif 'JO' in bloom_string:
            return 'joyful'
        return 'neutral'
        
    def _calculate_rebloom_risk(self, bloom_data: Dict) -> bool:
        """
        Calculate if a bloom has high rebloom risk based on entropy and intensity thresholds.
        
        Risk Rule:
        A bloom is considered high risk if:
        - entropy > 0.6 (indicating high complexity/chaos)
        - intensity > 5 (indicating strong bloom force)
        
        This combination suggests a bloom that may trigger cascading effects
        or require intervention to prevent system instability.
        
        Args:
            bloom_data: The decoded bloom data containing:
                - entropy: float (0-1)
                - intensity: int (0-10)
                
        Returns:
            bool: True if bloom meets high risk criteria
        """
        return (
            bloom_data['entropy'] > 0.6 and  # High complexity threshold
            bloom_data['intensity'] > 5      # Strong force threshold
        )
        
    def _write_whisper_reflection(self, blooms: List[Dict]) -> None:
        """
        Write reflection messages to whisper.log for high-risk blooms.
        
        Args:
            blooms: List of decoded bloom dictionaries
            
        Writes messages in format:
        [Owl] High entropy bloom detected at depth {depth}. Seed: {seed_id}. Recommend rebloom pause.
        """
        whisper_log = Path("logs/whisper.log")
        whisper_log.parent.mkdir(parents=True, exist_ok=True)
        
        high_risk_blooms = [b for b in blooms if b['rebloom_risk']]
        
        if high_risk_blooms:
            with open(whisper_log, 'a') as f:
                for bloom in high_risk_blooms:
                    message = (
                        f"[Owl] High entropy bloom detected at depth {bloom['depth']}. "
                        f"Seed: {bloom['seed_id']}. Recommend rebloom pause.\n"
                    )
                    f.write(message)
                    logging.info(f"Whisper reflection written for bloom {bloom['seed_id']}")

    def run_owl_scan(self) -> List[Dict]:
        """
        Run a full scan of configured directories for bloom strings.
        
        Returns:
            List of dictionaries containing decoded bloom data
        """
        all_blooms = []
        
        for directory in self.scan_directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                logging.warning(f"Directory not found: {directory}")
                continue
                
            # Recursively scan for .txt files
            for file_path in dir_path.rglob("*.txt"):
                if file_path.is_file():
                    blooms = self._scan_file(file_path)
                    all_blooms.extend(blooms)
                    
        # Sort blooms by entropy (highest first)
        all_blooms.sort(key=lambda x: x['entropy'], reverse=True)
        
        # Log summary
        logging.info(f"Scan complete. Found {len(all_blooms)} blooms.")
        if all_blooms:
            high_risk = sum(1 for b in all_blooms if b['rebloom_risk'])
            logging.info(f"High rebloom risk blooms: {high_risk}")
            
        # Write to registry
        try:
            self.write_registry(all_blooms)
        except Exception as e:
            logging.error(f"Failed to write registry during scan: {e}")
            
        # Write whisper reflections for high-risk blooms
        self._write_whisper_reflection(all_blooms)
            
        return all_blooms

def main():
    """Entry point for running Owl's bloom scan."""
    parser = OwlBloomParser()
    blooms = parser.run_owl_scan()
    
    # Print summary
    print(f"\nOwl Bloom Scan Results:")
    print(f"Total blooms found: {len(blooms)}")
    if blooms:
        high_risk = sum(1 for b in blooms if b['rebloom_risk'])
        print(f"High rebloom risk: {high_risk}")
        
        # Print details of highest entropy blooms
        print("\nTop 3 highest entropy blooms:")
        for bloom in blooms[:3]:
            print(f"- {bloom['pattern']} (E: {bloom['entropy']:.2f}, I: {bloom['intensity']})")
    
if __name__ == "__main__":
    main() 