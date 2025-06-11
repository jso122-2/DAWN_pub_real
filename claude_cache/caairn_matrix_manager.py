#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
import re
import math
from collections import Counter

class CAIRNMatrixManager:
    def __init__(self, matrix_file='claude_cache/caairn_matrix.json'):
        self.matrix_file = matrix_file
        self.matrix = self._load_matrix()
        
    def _load_matrix(self):
        """Load the CAIRN matrix from file."""
        if os.path.exists(self.matrix_file):
            with open(self.matrix_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_new_matrix()
    
    def _create_new_matrix(self):
        """Create a new CAIRN matrix structure."""
        return {
            "meta": {
                "version": "1.0",
                "created": datetime.utcnow().isoformat() + "Z",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "schema_version": "1.0",
                "location": "claude_cache/",
                "update_mechanism": ["rebuild_index.sh", "claude_write"],
                "field_definitions": {
                    "sigil": "Symbolic linkage between related concepts",
                    "heat": "Emotional pressure or intensity of content",
                    "entropy": "Semantic chaos or unpredictability",
                    "coherence": "Internal logic alignment and consistency",
                    "timestamp": "Index age and temporal context",
                    "author": "Source of creation or modification",
                    "session_id": "Compression, rebloom, or recursion tracking"
                }
            },
            "sigil_index": {},
            "stats": {
                "total_sigils": 0,
                "total_files": 0,
                "by_type": {"C": 0, "A": 0, "I": 0, "R": 0, "N": 0},
                "heat_distribution": {"low": 0, "medium": 0, "high": 0},
                "entropy_distribution": {"low": 0, "medium": 0, "high": 0},
                "coherence_distribution": {"low": 0, "medium": 0, "high": 0}
            }
        }
    
    def _save_matrix(self):
        """Save the current matrix state to file."""
        self.matrix["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
        os.makedirs(os.path.dirname(self.matrix_file), exist_ok=True)
        with open(self.matrix_file, 'w', encoding='utf-8') as f:
            json.dump(self.matrix, f, indent=4)
    
    def _calculate_entropy(self, content):
        """Calculate semantic entropy based on word distribution."""
        # Split into words and count frequencies
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
            
        word_counts = Counter(words)
        total_words = len(words)
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in word_counts.values():
            probability = count / total_words
            entropy -= probability * math.log2(probability)
            
        # Normalize to 0-1 range (assuming max entropy of 16 bits for English)
        return min(1.0, entropy / 16.0)
    
    def _calculate_coherence(self, content):
        """Calculate internal logic coherence."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.0
            
        # Calculate average sentence length
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Calculate length variance
        length_variance = sum((len(s.split()) - avg_length) ** 2 for s in sentences) / len(sentences)
        
        # Calculate coherence score (inverse of variance, normalized)
        coherence = 1.0 / (1.0 + length_variance)
        return min(1.0, coherence)
    
    def _calculate_heat(self, content):
        """Calculate emotional pressure based on content characteristics."""
        # Base heat from content length
        content_length = len(content)
        base_heat = min(1.0, content_length / 10000)
        
        # Adjust heat based on punctuation intensity
        exclamation_count = content.count('!')
        question_count = content.count('?')
        intensity_factor = min(1.0, (exclamation_count + question_count) / 100)
        
        # Combine factors
        heat = (base_heat * 0.7) + (intensity_factor * 0.3)
        return min(1.0, heat)
    
    def _extract_metadata(self, file_path, content):
        """Extract metadata from file content."""
        metadata = {
            "sigil": None,
            "heat": 0.0,
            "entropy": 0.0,
            "coherence": 0.0,
            "author": None,
            "session_id": None
        }
        
        # Extract sigil (assuming format: "sigil: ⊙")
        sigil_match = re.search(r'sigil:\s*([^\s]+)', content)
        if sigil_match:
            metadata["sigil"] = sigil_match.group(1)
        
        # Extract author (assuming format: "author: XXXX")
        author_match = re.search(r'author:\s*(\w+)', content)
        if author_match:
            metadata["author"] = author_match.group(1)
        
        # Extract session ID (assuming format: "session_id: S_YYYYMMDD_XXX")
        session_match = re.search(r'session_id:\s*(S_\d{8}_\d{3})', content)
        if session_match:
            metadata["session_id"] = session_match.group(1)
        
        # Calculate semantic metrics
        metadata["heat"] = self._calculate_heat(content)
        metadata["entropy"] = self._calculate_entropy(content)
        metadata["coherence"] = self._calculate_coherence(content)
        
        return metadata
    
    def _update_distributions(self):
        """Update all distribution statistics."""
        distributions = {
            "heat": self.matrix["stats"]["heat_distribution"],
            "entropy": self.matrix["stats"]["entropy_distribution"],
            "coherence": self.matrix["stats"]["coherence_distribution"]
        }
        
        ranges = {
            "low": (0, 0.33),
            "medium": (0.33, 0.66),
            "high": (0.66, 1.0)
        }
        
        # Reset all distributions
        for dist in distributions.values():
            for range_name in dist:
                dist[range_name] = 0
        
        # Update distributions
        for sigil_data in self.matrix["sigil_index"].values():
            for metric, dist in distributions.items():
                value = sigil_data[metric]
                for range_name, (min_val, max_val) in ranges.items():
                    if min_val <= value < max_val:
                        dist[range_name] += 1
                        break
    
    def add_file(self, file_path):
        """Add a file to the matrix."""
        file_path = Path(file_path)
        
        # Validate CAIRN prefix
        cairn_type = file_path.name[0]
        if cairn_type not in self.matrix["stats"]["by_type"]:
            raise ValueError(f"Invalid CAIRN type: {cairn_type}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        metadata = self._extract_metadata(file_path, content)
        if not metadata["sigil"]:
            raise ValueError(f"No sigil found in {file_path}")
        
        # Generate sigil key
        sigil_key = f"sigil_{metadata['sigil']}"
        
        # Update or create sigil entry
        if sigil_key not in self.matrix["sigil_index"]:
            self.matrix["sigil_index"][sigil_key] = {
                "files": [],
                **metadata,
                "last_used": datetime.utcnow().isoformat() + "Z"
            }
            self.matrix["stats"]["total_sigils"] += 1
        
        # Add file to sigil entry
        if str(file_path) not in self.matrix["sigil_index"][sigil_key]["files"]:
            self.matrix["sigil_index"][sigil_key]["files"].append(str(file_path))
            self.matrix["stats"]["total_files"] += 1
            self.matrix["stats"]["by_type"][cairn_type] += 1
        
        # Update metrics and last used
        self.matrix["sigil_index"][sigil_key].update(metadata)
        self.matrix["sigil_index"][sigil_key]["last_used"] = datetime.utcnow().isoformat() + "Z"
        
        # Update distributions
        self._update_distributions()
        
        self._save_matrix()
        return sigil_key
    
    def get_sigil_info(self, sigil_key):
        """Get information for a specific sigil."""
        return self.matrix["sigil_index"].get(sigil_key)
    
    def search_by_metrics(self, min_heat=None, max_heat=None, min_entropy=None, max_entropy=None, 
                         min_coherence=None, max_coherence=None):
        """Search sigils by metric ranges."""
        matches = []
        for sigil_key, data in self.matrix["sigil_index"].items():
            if min_heat is not None and data["heat"] < min_heat:
                continue
            if max_heat is not None and data["heat"] > max_heat:
                continue
            if min_entropy is not None and data["entropy"] < min_entropy:
                continue
            if max_entropy is not None and data["entropy"] > max_entropy:
                continue
            if min_coherence is not None and data["coherence"] < min_coherence:
                continue
            if max_coherence is not None and data["coherence"] > max_coherence:
                continue
            matches.append(data)
        return matches
    
    def get_stats(self):
        """Get current matrix statistics."""
        return self.matrix["stats"]

def main():
    """Example usage of CAIRNMatrixManager."""
    manager = CAIRNMatrixManager()
    
    # Example: Add a new file
    try:
        sigil_key = manager.add_file("claude_cache/C_001_sigil_parser.md")
        print(f"Added file to sigil: {sigil_key}")
    except Exception as e:
        print(f"Error adding file: {e}")
    
    # Example: Get matrix stats
    stats = manager.get_stats()
    print("\nMatrix Statistics:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main() 