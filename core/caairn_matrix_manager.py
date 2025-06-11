#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
import hashlib
import re

class CAIRNMatrixManager:
    def __init__(self, matrix_file='caairn_matrix.json'):
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
                "schema_version": "1.0"
            },
            "matrix": {
                "C": {"description": "Claude-generated content", "entries": {}},
                "A": {"description": "Analysis and assessment", "entries": {}},
                "I": {"description": "Integration and implementation", "entries": {}},
                "R": {"description": "Reflection and review", "entries": {}},
                "N": {"description": "Network and navigation", "entries": {}}
            },
            "stats": {
                "total_entries": 0,
                "by_type": {"C": 0, "A": 0, "I": 0, "R": 0, "N": 0},
                "by_file_type": {"md": 0, "json": 0, "txt": 0}
            }
        }
    
    def _save_matrix(self):
        """Save the current matrix state to file."""
        self.matrix["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(self.matrix_file, 'w', encoding='utf-8') as f:
            json.dump(self.matrix, f, indent=4)
    
    def _generate_entry_id(self, file_path, content):
        """Generate a unique ID for a matrix entry."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        return f"{file_path.stem}_{content_hash}"
    
    def _extract_metadata(self, file_path, content):
        """Extract metadata from file content."""
        metadata = {
            "sigil": None,
            "session_id": None,
            "author": None,
            "pressure": 0.0,
            "entropy": 0.0
        }
        
        # Extract sigil (assuming format: "sigil: XXXX")
        sigil_match = re.search(r'sigil:\s*(\w+)', content)
        if sigil_match:
            metadata["sigil"] = sigil_match.group(1)
        
        # Extract session ID (assuming format: "session_id: XXXX")
        session_match = re.search(r'session_id:\s*(\w+)', content)
        if session_match:
            metadata["session_id"] = session_match.group(1)
        
        # Extract author (assuming format: "author: XXXX")
        author_match = re.search(r'author:\s*(\w+)', content)
        if author_match:
            metadata["author"] = author_match.group(1)
        
        # Calculate pressure (heat) based on content length and complexity
        content_length = len(content)
        metadata["pressure"] = min(1.0, content_length / 10000)  # Normalize to 0-1
        
        # Calculate entropy based on unique character distribution
        unique_chars = len(set(content))
        total_chars = len(content)
        metadata["entropy"] = unique_chars / total_chars if total_chars > 0 else 0
        
        return metadata
    
    def add_entry(self, file_path):
        """Add a new entry to the matrix."""
        file_path = Path(file_path)
        
        # Validate file type
        if file_path.suffix[1:] not in self.matrix["stats"]["by_file_type"]:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Validate CAIRN prefix
        cairn_type = file_path.name[0]
        if cairn_type not in self.matrix["matrix"]:
            raise ValueError(f"Invalid CAIRN type: {cairn_type}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate entry ID and extract metadata
        entry_id = self._generate_entry_id(file_path, content)
        metadata = self._extract_metadata(file_path, content)
        
        # Create entry
        entry = {
            "id": entry_id,
            "file_path": str(file_path),
            "file_type": file_path.suffix[1:],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **metadata
        }
        
        # Add to matrix
        self.matrix["matrix"][cairn_type]["entries"][entry_id] = entry
        
        # Update stats
        self.matrix["stats"]["total_entries"] += 1
        self.matrix["stats"]["by_type"][cairn_type] += 1
        self.matrix["stats"]["by_file_type"][file_path.suffix[1:]] += 1
        
        self._save_matrix()
        return entry_id
    
    def get_entry(self, entry_id):
        """Retrieve an entry from the matrix."""
        for cairn_type in self.matrix["matrix"]:
            if entry_id in self.matrix["matrix"][cairn_type]["entries"]:
                return self.matrix["matrix"][cairn_type]["entries"][entry_id]
        return None
    
    def search_entries(self, **criteria):
        """Search entries based on criteria."""
        matches = []
        for cairn_type in self.matrix["matrix"]:
            for entry_id, entry in self.matrix["matrix"][cairn_type]["entries"].items():
                if all(entry.get(k) == v for k, v in criteria.items()):
                    matches.append(entry)
        return matches
    
    def get_stats(self):
        """Get current matrix statistics."""
        return self.matrix["stats"]

def main():
    """Example usage of CAIRNMatrixManager."""
    manager = CAIRNMatrixManager()
    
    # Example: Add a new entry
    try:
        entry_id = manager.add_entry("claude_cache/C_example.md")
        print(f"Added entry: {entry_id}")
    except Exception as e:
        print(f"Error adding entry: {e}")
    
    # Example: Get matrix stats
    stats = manager.get_stats()
    print("\nMatrix Statistics:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main() 