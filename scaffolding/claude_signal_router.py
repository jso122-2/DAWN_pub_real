#!/usr/bin/env python3
"""
DAWN Claude Signal Router
========================
Processes Claude fragments and launches appropriate tracers based on signal content.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🎯 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class SignalMatch:
    """Represents a matched signal in Claude's output."""
    keyword: str
    context: str
    urgency: float
    line_number: int

class ClaudeSignalRouter:
    """Routes Claude's signals to appropriate tracers."""
    
    def __init__(self):
        self.fragments_dir = Path("claude_fragments")
        self.feedback_file = Path("logs/claude_feedback.json")
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Signal keywords and their urgency levels
        self.signal_map = {
            "rebloom": 0.8,
            "schema drift": 0.9,
            "operator offline": 0.95,
            "fail-safe": 0.9,
            "critical path": 0.85,
            "system stress": 0.8,
            "anomaly": 0.85,
            "entropy spike": 0.9,
            "pattern break": 0.8,
            "memory leak": 0.85
        }
        
        # Initialize feedback log
        self._init_feedback_log()
    
    def _init_feedback_log(self) -> None:
        """Initialize the feedback log file if it doesn't exist."""
        if not self.feedback_file.exists():
            initial_data = {
                "routing_history": [],
                "signal_stats": {
                    "total_signals": 0,
                    "successful_routes": 0,
                    "failed_routes": 0,
                    "last_updated": datetime.now().isoformat()
                }
            }
            with open(self.feedback_file, "w") as f:
                json.dump(initial_data, f, indent=2)
    
    def _get_latest_fragment(self) -> Optional[Path]:
        """Get the path to the most recent Claude fragment."""
        try:
            fragments = list(self.fragments_dir.glob("fragment_*.md"))
            if not fragments:
                return None
            return max(fragments, key=lambda p: p.stat().st_mtime)
        except Exception as e:
            logger.error(f"Error finding latest fragment: {e}")
            return None
    
    def _scan_for_signals(self, fragment_path: Path) -> List[SignalMatch]:
        """Scan fragment content for signal keywords."""
        matches = []
        try:
            with open(fragment_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
                
                for i, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    for keyword, urgency in self.signal_map.items():
                        if keyword in line_lower:
                            # Extract context (surrounding text)
                            start = max(0, i - 2)
                            end = min(len(lines), i + 2)
                            context = "\n".join(lines[start:end])
                            
                            matches.append(SignalMatch(
                                keyword=keyword,
                                context=context,
                                urgency=urgency,
                                line_number=i
                            ))
        except Exception as e:
            logger.error(f"Error scanning fragment: {e}")
        
        return matches
    
    def _build_tracer_payload(self, match: SignalMatch) -> Dict:
        """Build a tracer payload from a signal match."""
        return {
            "signal": match.keyword,
            "origin": "claude_signal",
            "urgency": match.urgency,
            "mood_context": "analytical",  # Default mood for Claude signals
            "metadata": {
                "context": match.context,
                "line_number": match.line_number,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _log_feedback(self, fragment_path: Path, matches: List[SignalMatch], 
                     results: List[Dict]) -> None:
        """Log routing feedback to the feedback file."""
        try:
            with open(self.feedback_file, "r") as f:
                feedback_data = json.load(f)
            
            # Update routing history
            feedback_data["routing_history"].append({
                "timestamp": datetime.now().isoformat(),
                "fragment": str(fragment_path),
                "matches": [vars(m) for m in matches],
                "results": results
            })
            
            # Update stats
            feedback_data["signal_stats"]["total_signals"] += len(matches)
            feedback_data["signal_stats"]["successful_routes"] += sum(
                1 for r in results if r.get("success", False)
            )
            feedback_data["signal_stats"]["failed_routes"] += sum(
                1 for r in results if not r.get("success", False)
            )
            feedback_data["signal_stats"]["last_updated"] = datetime.now().isoformat()
            
            # Keep only last 1000 entries
            feedback_data["routing_history"] = feedback_data["routing_history"][-1000:]
            
            with open(self.feedback_file, "w") as f:
                json.dump(feedback_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error logging feedback: {e}")
    
    def process_latest_fragment(self) -> None:
        """Process the latest Claude fragment and route signals."""
        try:
            # Get latest fragment
            fragment_path = self._get_latest_fragment()
            if not fragment_path:
                logger.info("No fragments found to process")
                return
            
            # Scan for signals
            matches = self._scan_for_signals(fragment_path)
            if not matches:
                logger.info(f"No signals found in {fragment_path}")
                return
            
            # Route each signal
            results = []
            for match in matches:
                try:
                    # Import here to avoid circular imports
                    from router.tracer_router import TracerRouter, TracerPayload
                    
                    # Build and route payload
                    payload_data = self._build_tracer_payload(match)
                    payload = TracerPayload(**payload_data)
                    
                    # Get tracer router instance
                    tracer_router = TracerRouter()
                    
                    # Route the signal
                    result = tracer_router.evaluate_route(
                        source="claude_signal",
                        target="system_core",
                        payload=payload,
                        current_pressure=0.5,  # Default pressure
                        tracer_type="OwlTracer"  # Default tracer type
                    )
                    
                    results.append({
                        "signal": match.keyword,
                        "success": result.get("success", False),
                        "route": result.get("route", []),
                        "score": result.get("score", 0.0)
                    })
                    
                except Exception as e:
                    logger.error(f"Error routing signal {match.keyword}: {e}")
                    results.append({
                        "signal": match.keyword,
                        "success": False,
                        "error": str(e)
                    })
            
            # Log feedback
            self._log_feedback(fragment_path, matches, results)
            
        except Exception as e:
            logger.error(f"Error processing fragment: {e}")

# Create global instance
claude_signal_router = ClaudeSignalRouter() 