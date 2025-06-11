#!/usr/bin/env python3
"""
DAWN Claude Suggestion Handler
=============================
Manages the injection of Claude's suggestions into DAWN's memory system.
Safely stores suggestions in juliet_flowers/suggested/ with metadata headers
but does not activate them until verified.
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
import logging
import hashlib
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌸 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClaudeSuggestionHandler:
    """Manages Claude's suggestions in DAWN's memory system"""
    
    def __init__(self):
        self.suggestions_dir = Path("juliet_flowers/suggested")
        self.suggestions_dir.mkdir(exist_ok=True)
        
        # Metadata fields that must be present
        self.required_metadata = {
            'Claude:signal',
            'Confidence',
            'Mood',
            'Timestamp',
            'SuggestionID',
            'Status'
        }
        
        # Valid mood states
        self.valid_moods = {
            'Low Entropy',
            'High Entropy',
            'Stable',
            'Drifting',
            'Reblooming',
            'Unknown'
        }
    
    def _generate_suggestion_id(self, text: str) -> str:
        """Generate a unique ID for the suggestion"""
        # Use first 8 chars of hash of text + timestamp
        timestamp = datetime.now().isoformat()
        hash_input = f"{text}{timestamp}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:8]
    
    def _extract_metadata_tags(self, text: str) -> Dict[str, str]:
        """Extract metadata tags from text"""
        metadata = {}
        tag_pattern = r'\[\[(.*?):(.*?)\]\]'
        
        for match in re.finditer(tag_pattern, text):
            key, value = match.groups()
            metadata[key.strip()] = value.strip()
        
        return metadata
    
    def _validate_metadata(self, metadata: Dict[str, str]) -> bool:
        """Validate that all required metadata is present and valid"""
        # Check required fields
        for field in self.required_metadata:
            if field not in metadata:
                logger.warning(f"Missing required metadata field: {field}")
                return False
        
        # Validate confidence
        try:
            confidence = float(metadata['Confidence'])
            if not 0 <= confidence <= 1:
                logger.warning(f"Invalid confidence value: {confidence}")
                return False
        except ValueError:
            logger.warning("Confidence must be a number between 0 and 1")
            return False
        
        # Validate mood
        if metadata['Mood'] not in self.valid_moods:
            logger.warning(f"Invalid mood state: {metadata['Mood']}")
            return False
        
        return True
    
    def _clean_text(self, text: str) -> str:
        """Remove metadata tags from text"""
        # Remove all [[tag:value]] patterns
        return re.sub(r'\[\[.*?\]\]', '', text).strip()
    
    def _format_suggestion(self, text: str, metadata: Dict[str, str]) -> str:
        """Format suggestion with metadata headers"""
        # Add timestamp if not present
        if 'Timestamp' not in metadata:
            metadata['Timestamp'] = datetime.now().isoformat()
        
        # Add status if not present
        if 'Status' not in metadata:
            metadata['Status'] = 'Pending'
        
        # Format headers
        headers = []
        for key, value in metadata.items():
            headers.append(f"[[{key}:{value}]]")
        
        # Combine headers and cleaned text
        return "\n".join(headers) + "\n\n" + self._clean_text(text)
    
    def inject_claude_bloom_suggestion(self, text: str, confidence: float) -> Optional[str]:
        """Store Claude's suggestion with metadata headers"""
        try:
            # Extract existing metadata
            metadata = self._extract_metadata_tags(text)
            
            # Add or update confidence
            metadata['Confidence'] = str(confidence)
            
            # Add Claude signal if not present
            if 'Claude:signal' not in metadata:
                metadata['Claude:signal'] = 'true'
            
            # Add mood if not present
            if 'Mood' not in metadata:
                metadata['Mood'] = 'Unknown'
            
            # Generate suggestion ID
            suggestion_id = self._generate_suggestion_id(text)
            metadata['SuggestionID'] = suggestion_id
            
            # Validate metadata
            if not self._validate_metadata(metadata):
                logger.error("Invalid metadata in suggestion")
                return None
            
            # Format suggestion
            formatted_suggestion = self._format_suggestion(text, metadata)
            
            # Write to file
            suggestion_path = self.suggestions_dir / f"suggestion_{suggestion_id}.txt"
            with open(suggestion_path, 'w', encoding='utf-8') as f:
                f.write(formatted_suggestion)
            
            logger.info(f"Stored Claude suggestion with ID: {suggestion_id}")
            return suggestion_id
            
        except Exception as e:
            logger.error(f"Failed to store Claude suggestion: {e}")
            return None
    
    def get_suggestion(self, suggestion_id: str) -> Optional[Dict]:
        """Retrieve a stored suggestion with its metadata"""
        try:
            suggestion_path = self.suggestions_dir / f"suggestion_{suggestion_id}.txt"
            if not suggestion_path.exists():
                logger.warning(f"Suggestion not found: {suggestion_id}")
                return None
            
            with open(suggestion_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata and text
            metadata = self._extract_metadata_tags(content)
            text = self._clean_text(content)
            
            return {
                'metadata': metadata,
                'text': text,
                'path': str(suggestion_path)
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve suggestion: {e}")
            return None
    
    def list_suggestions(self, status: Optional[str] = None) -> List[Dict]:
        """List all stored suggestions, optionally filtered by status"""
        suggestions = []
        
        try:
            for suggestion_path in self.suggestions_dir.glob('suggestion_*.txt'):
                with open(suggestion_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata = self._extract_metadata_tags(content)
                
                # Filter by status if specified
                if status and metadata.get('Status') != status:
                    continue
                
                suggestions.append({
                    'id': metadata.get('SuggestionID'),
                    'timestamp': metadata.get('Timestamp'),
                    'confidence': float(metadata.get('Confidence', 0)),
                    'mood': metadata.get('Mood'),
                    'status': metadata.get('Status'),
                    'path': str(suggestion_path)
                })
            
            # Sort by timestamp
            suggestions.sort(key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to list suggestions: {e}")
        
        return suggestions

# Create global instance
claude_suggestion_handler = ClaudeSuggestionHandler() 