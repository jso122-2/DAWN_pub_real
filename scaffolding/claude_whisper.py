#!/usr/bin/env python3
"""
DAWN Claude Whisper Back
=======================
Allows DAWN to respond to Claude's outputs by summarizing system feedback
and saving responses as markdown fragments.
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌸 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClaudeWhisper:
    """Handles DAWN's responses back to Claude"""
    
    def __init__(self):
        self.reflections_path = Path("pulse/claude_reflections.md")
        self.fragments_dir = Path("claude_fragments")
        self.fragments_dir.mkdir(exist_ok=True)
        
        # Load current tick from state
        try:
            with open("tick_state.json", "r") as f:
                self.current_tick = json.load(f).get("tick", 0)
        except Exception:
            self.current_tick = 0
    
    def _extract_reflections(self) -> List[Dict]:
        """Extract the last two reflections from the reflections file"""
        reflections = []
        try:
            if not self.reflections_path.exists():
                logger.warning("No reflections file found")
                return reflections
            
            with open(self.reflections_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Split into reflection blocks
            blocks = content.split("---\n")
            for block in blocks[-3:-1]:  # Get last 2 reflections
                if not block.strip():
                    continue
                    
                try:
                    # Parse YAML front matter
                    yaml_part = block.split("\n\n")[0]
                    reflection = yaml.safe_load(yaml_part)
                    reflections.append(reflection)
                except Exception as e:
                    logger.error(f"Failed to parse reflection block: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting reflections: {e}")
        
        return reflections
    
    def _summarize_feedback(self, reflections: List[Dict]) -> str:
        """Generate a summary of system feedback from reflections"""
        if not reflections:
            return "No recent reflections available."
        
        summary = []
        summary.append("# DAWN's Response to Claude\n\n")
        summary.append(f"Timestamp: {datetime.now().isoformat()}\n")
        summary.append(f"Tick: {self.current_tick}\n\n")
        
        # Add reflection summaries
        summary.append("## Recent Reflections\n\n")
        for reflection in reflections:
            tick = reflection.get("tick", "unknown")
            categories = reflection.get("categories", [])
            agreement = reflection.get("agreement_score", 0.0)
            confidence = reflection.get("confidence_score", 0.0)
            
            summary.append(f"### Tick {tick}\n\n")
            summary.append(f"- Categories: {', '.join(categories)}\n")
            summary.append(f"- Agreement: {agreement:.2f}\n")
            summary.append(f"- Confidence: {confidence:.2f}\n")
            
            if "reasoning" in reflection:
                summary.append(f"\nReasoning:\n{reflection['reasoning']}\n")
            
            if "evidence" in reflection:
                summary.append(f"\nEvidence:\n{reflection['evidence']}\n")
            
            summary.append("\n")
        
        # Add system state
        summary.append("## System State\n\n")
        try:
            with open("trust_checkpoint.yaml", "r") as f:
                trust_state = yaml.safe_load(f)
                summary.append(f"- Trust Score: {trust_state['claude_access']['trust_score']:.2f}\n")
                summary.append(f"- Status: {trust_state['claude_access']['status']}\n")
        except Exception:
            summary.append("- Trust state unavailable\n")
        
        # Add stability metrics
        try:
            with open("pulse/pulse_state.yaml", "r") as f:
                pulse_state = yaml.safe_load(f)
                summary.append(f"- SCUP: {pulse_state.get('scup', 0.0):.2f}\n")
                summary.append(f"- Schema Stability: {pulse_state.get('schema_stability', 0.0):.2f}\n")
        except Exception:
            summary.append("- Pulse state unavailable\n")
        
        return "\n".join(summary)
    
    def whisper_back_to_claude(self) -> Optional[Path]:
        """
        Generate and save DAWN's response to Claude's recent outputs
        
        Returns:
            Path to the created response file, or None if failed
        """
        try:
            # Get recent reflections
            reflections = self._extract_reflections()
            if not reflections:
                logger.warning("No reflections found to respond to")
                return None
            
            # Generate response
            response = self._summarize_feedback(reflections)
            
            # Save response
            response_path = self.fragments_dir / f"DAWN_response_{self.current_tick:06d}.md"
            with open(response_path, "w", encoding="utf-8") as f:
                f.write(response)
            
            logger.info(f"Saved whisper back response to {response_path}")
            return response_path
            
        except Exception as e:
            logger.error(f"Failed to whisper back to Claude: {e}")
            return None

# Create global instance
claude_whisper = ClaudeWhisper() 