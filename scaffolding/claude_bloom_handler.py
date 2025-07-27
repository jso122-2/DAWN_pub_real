#!/usr/bin/env python3
"""
DAWN Claude Bloom Suggestion Handler
===================================
Safely stores Claude's suggestions as potential blooms,
keeping them separate from active memory until verified.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌸 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClaudeBloomHandler:
    """Handles storage of Claude's bloom suggestions"""
    
    def __init__(self):
        self.suggestions_dir = Path("juliet_flowers/suggested")
        self.suggestions_dir.mkdir(parents=True, exist_ok=True)
        
        # Load current tick from state
        try:
            with open("tick_state.json", "r") as f:
                self.current_tick = json.load(f).get("tick", 0)
        except Exception:
            self.current_tick = 0
    
    def _get_current_mood(self) -> str:
        """Get DAWN's current mood state"""
        try:
            from core.system_state import pulse
            return pulse.get_mood()
        except ImportError:
            return "reflective"  # Default mood
    
    def _format_metadata(self, confidence: float) -> str:
        """Format metadata headers for the suggestion file"""
        return f"""[[Claude:true]]
[[Confidence:{confidence:.2f}]]
[[Suggested:true]]
[[Mood:{self._get_current_mood()}]]
"""
    
    def inject_claude_bloom_suggestion(self, text: str, confidence: float) -> Optional[Path]:
        """
        Store a Claude suggestion as a potential bloom
        
        Args:
            text: The suggestion text from Claude
            confidence: Confidence score (0.0 to 1.0)
            
        Returns:
            Path to the created suggestion file, or None if failed
        """
        try:
            # Validate inputs
            if not text or not isinstance(text, str):
                logger.error("Invalid suggestion text")
                return None
                
            if not 0.0 <= confidence <= 1.0:
                logger.error(f"Invalid confidence score: {confidence}")
                return None
            
            # Create suggestion file
            filename = f"suggested_{self.current_tick:06d}.txt"
            filepath = self.suggestions_dir / filename
            
            # Write content with metadata
            content = self._format_metadata(confidence)
            content += "\n" + text.strip()
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Stored suggestion in {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to store suggestion: {e}")
            return None

# Create global instance
claude_bloom_handler = ClaudeBloomHandler() 