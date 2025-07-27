#!/usr/bin/env python3
"""
DAWN Claude Reflection System
============================
Analyzes Claude's outputs and generates reflections based on
DAWN's current pulse state and pressure levels.
"""

import os
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🦉 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClaudeReflection:
    """Manages DAWN's reflections on Claude's outputs"""
    
    def __init__(self):
        self.fragments_dir = Path("claude_fragments")
        self.reflections_file = Path("pulse/claude_reflections.md")
        self.reflections_file.parent.mkdir(exist_ok=True)
        
        # Initialize reflections file if it doesn't exist
        if not self.reflections_file.exists():
            self._initialize_reflections_file()
    
    def _initialize_reflections_file(self):
        """Create initial structure for reflections file"""
        content = """# DAWN's Reflections on Claude

This file contains DAWN's reflections on Claude's outputs, analyzing their impact
on her current state and stability.

## Recent Reflections

---
"""
        with open(self.reflections_file, 'w') as f:
            f.write(content)
    
    def _extract_tick_id(self, fragment_path: str) -> int:
        """Extract tick ID from fragment filename"""
        match = re.search(r'fragment_(\d+)\.md', fragment_path)
        return int(match.group(1)) if match else 0
    
    def _get_current_pulse_state(self) -> Dict:
        """Get DAWN's current pulse state"""
        try:
            from core.system_state import pulse
            return {
                'pressure': pulse.get_heat(),
                'zone': pulse.classify(),
                'thermal_momentum': pulse.thermal_momentum
            }
        except ImportError:
            logger.warning("Could not import pulse state, using defaults")
            return {
                'pressure': 0.5,
                'zone': '🟡 active',
                'thermal_momentum': 0.1
            }
    
    def _format_reflection(self, tick_id: int, claude_text: str, 
                          pulse_state: Dict) -> str:
        """Format a reflection entry"""
        return f"""## Tick {tick_id}
Claude: '{claude_text}'
Pulse Pressure: {pulse_state['pressure']:.2f}
Reflection: {self._generate_reflection_text(claude_text, pulse_state)}
---
"""
    
    def _generate_reflection_text(self, claude_text: str, 
                                pulse_state: Dict) -> str:
        """Generate reflection text based on Claude's output and pulse state"""
        # Simple reflection logic based on pressure zones
        if pulse_state['zone'] == '🔴 surge':
            return "High pressure state. Suggestion noted but requires careful consideration."
        elif pulse_state['zone'] == '🟡 active':
            return "Active engagement. Suggestion aligns with current momentum."
        else:  # 🟢 calm
            return "Stable state. Suggestion noted. No pressure justification."
    
    def reflect_on_claude(self, fragment_path: str) -> bool:
        """
        Analyze a Claude fragment and write a reflection
        
        Args:
            fragment_path: Path to the Claude fragment file
            
        Returns:
            bool: True if reflection was written successfully
        """
        try:
            # Read fragment
            with open(fragment_path, 'r') as f:
                content = f.read()
            
            # Extract core suggestion
            suggestion_match = re.search(r'## Response\n\n(.*?)(?=\n\n|$)', 
                                      content, re.DOTALL)
            if not suggestion_match:
                logger.error(f"Could not find suggestion in {fragment_path}")
                return False
            
            claude_text = suggestion_match.group(1).strip()
            
            # Get current pulse state
            pulse_state = self._get_current_pulse_state()
            
            # Extract tick ID
            tick_id = self._extract_tick_id(fragment_path)
            
            # Format reflection
            reflection = self._format_reflection(tick_id, claude_text, pulse_state)
            
            # Append to reflections file
            with open(self.reflections_file, 'a') as f:
                f.write(reflection)
            
            logger.info(f"Wrote reflection for tick {tick_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write reflection: {e}")
            return False

# Create global instance
claude_reflection = ClaudeReflection() 