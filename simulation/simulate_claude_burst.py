"""
Claude Burst Simulator
Simulates Claude-like transcripts with urgency signals and routes them to appropriate handlers.
"""

import os
import json
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

# Constants
CACHE_DIR = "claude_cache"
LOGS_DIR = "logs"
BURST_LOG = "logs/claude_burst.log"
TRACE_LOG = "logs/claude_trace.json"

# Signal patterns and their severity levels
SIGNAL_PATTERNS = {
    "schema drift": 3,  # High severity
    "urgency spike": 2,  # Medium severity
    "pattern anomaly": 2,
    "semantic shift": 1,  # Low severity
    "drift detected": 3,
    "critical path": 3,
    "system stress": 2,
    "anomaly detected": 2,
    "pattern break": 1
}

# Sample transcript templates
TRANSCRIPT_TEMPLATES = [
    "I've detected a {signal} in the {component} subsystem. This requires immediate attention.",
    "Analysis shows {signal} patterns emerging in the {component} layer. Recommend investigation.",
    "The {component} module is showing signs of {signal}. This could impact system stability.",
    "Warning: {signal} detected in {component}. System integrity may be compromised.",
    "Critical: {signal} affecting {component}. Immediate action required."
]

# System components for randomization
COMPONENTS = [
    "tracer",
    "pulse",
    "semantic",
    "bloom",
    "schema",
    "core",
    "reflection",
    "memory",
    "cognitive"
]

class ClaudeBurstSimulator:
    """Simulates Claude-like transcripts with urgency signals."""
    
    def __init__(self):
        """Initialize the simulator with proper logging and directories."""
        # Ensure directories exist
        os.makedirs(CACHE_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=BURST_LOG,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Initialize trace log if needed
        self._init_trace_log()
        
    def _init_trace_log(self) -> None:
        """Initialize the trace log file if it doesn't exist."""
        if not os.path.exists(TRACE_LOG):
            with open(TRACE_LOG, 'w') as f:
                json.dump([], f)
                
    def _generate_transcript(self) -> str:
        """Generate a random Claude-like transcript with urgency signals."""
        signal = random.choice(list(SIGNAL_PATTERNS.keys()))
        component = random.choice(COMPONENTS)
        template = random.choice(TRANSCRIPT_TEMPLATES)
        
        return template.format(signal=signal, component=component)
        
    def _write_transcript(self, content: str, index: int) -> str:
        """Write transcript to cache directory and return filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"claude_burst_{timestamp}_{index}.txt"
        filepath = os.path.join(CACHE_DIR, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
            
        return filename
        
    def _extract_signals(self, transcript: str) -> List[Dict]:
        """Extract signals from transcript and calculate severity."""
        signals = []
        
        for pattern, severity in SIGNAL_PATTERNS.items():
            if pattern.lower() in transcript.lower():
                signals.append({
                    "pattern": pattern,
                    "severity": severity,
                    "line": transcript,
                    "timestamp": datetime.now().isoformat()
                })
                
        return signals
        
    def _route_signal(self, signal: Dict) -> None:
        """Route signal to appropriate handler based on severity."""
        severity = signal["severity"]
        pattern = signal["pattern"]
        
        if severity >= 3:  # High severity
            # Route to pulse_engine
            logging.warning(
                f"Routing high severity signal to pulse_engine:\n"
                f"Pattern: {pattern}\n"
                f"Severity: {severity}\n"
                f"Line: {signal['line']}"
            )
        elif severity >= 2:  # Medium severity
            # Route to tracer_router
            logging.info(
                f"Routing medium severity signal to tracer_router:\n"
                f"Pattern: {pattern}\n"
                f"Severity: {severity}\n"
                f"Line: {signal['line']}"
            )
        else:  # Low severity
            # Log only
            logging.info(
                f"Logging low severity signal:\n"
                f"Pattern: {pattern}\n"
                f"Severity: {severity}\n"
                f"Line: {signal['line']}"
            )
            
    def _update_trace_log(self, signals: List[Dict]) -> None:
        """Update the trace log with new signals."""
        try:
            with open(TRACE_LOG, 'r') as f:
                existing = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing = []
            
        existing.extend(signals)
        
        with open(TRACE_LOG, 'w') as f:
            json.dump(existing, f, indent=2)
            
    def simulate_burst(self) -> None:
        """Simulate a burst of Claude-like transcripts with signals."""
        logging.info("Starting Claude burst simulation")
        
        # Generate and process 3 transcripts
        for i in range(3):
            # Generate transcript
            transcript = self._generate_transcript()
            filename = self._write_transcript(transcript, i)
            
            # Extract signals
            signals = self._extract_signals(transcript)
            
            if signals:
                # Update trace log
                self._update_trace_log(signals)
                
                # Route most severe signal
                most_severe = max(signals, key=lambda x: x["severity"])
                self._route_signal(most_severe)
                
                logging.info(
                    f"Processed transcript {filename}:\n"
                    f"Found {len(signals)} signal(s)\n"
                    f"Most severe: {most_severe['pattern']} "
                    f"(severity {most_severe['severity']})"
                )
            else:
                logging.info(f"No signals found in transcript {filename}")
                
        logging.info("Claude burst simulation complete")

def main():
    """Main entry point for the Claude burst simulator."""
    try:
        simulator = ClaudeBurstSimulator()
        simulator.simulate_burst()
        print(f"Simulation complete. Check {BURST_LOG} for details.")
    except Exception as e:
        print(f"Error running simulation: {str(e)}")
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main() 