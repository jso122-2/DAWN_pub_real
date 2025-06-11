#!/usr/bin/env python3
"""
DAWN Heartbeat Watchdog
======================
Monitors system pulse and Claude interactions for:
- Tick loop freezes
- Semantic stalls
- Unacknowledged Claude drift
- Directory size anomalies
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 💓 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class WatchdogState:
    """Current state of the watchdog monitoring"""
    last_tick: int = 0
    last_tick_time: float = 0.0
    last_claude_injection: int = 0
    injection_count: int = 0
    last_response_tick: int = 0
    freeze_warnings: int = 0
    stall_warnings: int = 0
    last_dir_sizes: Dict[str, int] = None
    
    def __post_init__(self):
        if self.last_dir_sizes is None:
            self.last_dir_sizes = {}

class HeartbeatWatchdog:
    """Monitors system pulse and Claude interactions"""
    
    def __init__(self):
        self.state = WatchdogState()
        self.log_path = Path("logs/watchdog_heartbeat.json")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.pulse_state_path = Path("pulse/pulse_state.json")
        self.fragments_dir = Path("claude_fragments")
        
        # Critical directories to monitor
        self.monitored_dirs = {
            "pulse": Path("pulse"),
            "logs": Path("logs"),
            "claude_fragments": self.fragments_dir,
            "schema": Path("schema"),
            "core": Path("core")
        }
        
        # Size thresholds (in bytes)
        self.size_thresholds = {
            "logs": 2 * 1024 * 1024,  # 2MB
            "claude_fragments": 1024 * 1024,  # 1MB
            "schema": 512 * 1024,  # 512KB
            "core": 1024 * 1024,  # 1MB
            "pulse": 512 * 1024  # 512KB
        }
        
        # Growth rate thresholds (bytes per hour)
        self.growth_thresholds = {
            "logs": 100 * 1024,  # 100KB/hour
            "claude_fragments": 50 * 1024,  # 50KB/hour
            "schema": 10 * 1024,  # 10KB/hour
            "core": 20 * 1024,  # 20KB/hour
            "pulse": 10 * 1024  # 10KB/hour
        }
        
        # Initialize log file if it doesn't exist
        if not self.log_path.exists():
            self._initialize_log()
    
    def _get_dir_size(self, path: Path) -> int:
        """Calculate total size of directory in bytes"""
        total_size = 0
        try:
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
        except Exception as e:
            logger.error(f"Error calculating size for {path}: {e}")
        return total_size
    
    def _check_directory_sizes(self) -> List[Dict]:
        """Check for directory size anomalies"""
        anomalies = []
        current_time = time.time()
        
        for name, path in self.monitored_dirs.items():
            if not path.exists():
                continue
                
            current_size = self._get_dir_size(path)
            last_size = self.state.last_dir_sizes.get(name, current_size)
            
            # Check absolute size threshold
            if current_size > self.size_thresholds.get(name, float('inf')):
                anomalies.append({
                    "type": "size_threshold",
                    "directory": name,
                    "current_size": current_size,
                    "threshold": self.size_thresholds[name]
                })
            
            # Check growth rate
            if name in self.state.last_dir_sizes:
                time_diff = current_time - self.state.last_tick_time
                if time_diff > 0:
                    growth_rate = (current_size - last_size) / (time_diff / 3600)  # bytes per hour
                    if growth_rate > self.growth_thresholds.get(name, float('inf')):
                        anomalies.append({
                            "type": "growth_rate",
                            "directory": name,
                            "growth_rate": growth_rate,
                            "threshold": self.growth_thresholds[name]
                        })
            
            # Update last size
            self.state.last_dir_sizes[name] = current_size
        
        return anomalies
    
    def _initialize_log(self) -> None:
        """Initialize the watchdog log file"""
        initial_log = {
            "heartbeat_events": [],
            "stats": {
                "total_checks": 0,
                "freeze_warnings": 0,
                "stall_warnings": 0,
                "size_warnings": 0,
                "growth_warnings": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        with open(self.log_path, "w") as f:
            json.dump(initial_log, f, indent=2)
        
        logger.info("Created initial watchdog log")
    
    def _log_event(self, event_type: str, details: Dict) -> None:
        """Log a watchdog event"""
        try:
            # Load existing log
            with open(self.log_path, "r") as f:
                log_data = json.load(f)
            
            # Create event entry
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "details": details
            }
            
            # Update log
            log_data["heartbeat_events"].append(event)
            log_data["stats"]["total_checks"] += 1
            
            if event_type == "freeze_warning":
                log_data["stats"]["freeze_warnings"] += 1
            elif event_type == "stall_warning":
                log_data["stats"]["stall_warnings"] += 1
            elif event_type == "size_warning":
                log_data["stats"]["size_warnings"] += 1
            elif event_type == "growth_warning":
                log_data["stats"]["growth_warnings"] += 1
                
            log_data["stats"]["last_updated"] = datetime.now().isoformat()
            
            # Keep only last 1000 events
            log_data["heartbeat_events"] = log_data["heartbeat_events"][-1000:]
            
            # Save updated log
            with open(self.log_path, "w") as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log watchdog event: {e}")
    
    def _check_tick_freeze(self) -> bool:
        """Check if system tick has frozen"""
        try:
            if not self.pulse_state_path.exists():
                return False
            
            with open(self.pulse_state_path, "r") as f:
                pulse_state = json.load(f)
            
            current_tick = pulse_state.get("tick", 0)
            current_time = time.time()
            
            # First check
            if self.state.last_tick == 0:
                self.state.last_tick = current_tick
                self.state.last_tick_time = current_time
                return False
            
            # Check for freeze
            if current_tick == self.state.last_tick:
                time_since_update = current_time - self.state.last_tick_time
                if time_since_update >= 60:  # 60 seconds threshold
                    self._log_event("freeze_warning", {
                        "tick": current_tick,
                        "frozen_for_seconds": time_since_update,
                        "warning_count": self.state.freeze_warnings + 1
                    })
                    self.state.freeze_warnings += 1
                    logger.warning(f"System tick frozen at {current_tick} for {time_since_update:.1f}s")
                    return True
            
            # Update state
            self.state.last_tick = current_tick
            self.state.last_tick_time = current_time
            return False
            
        except Exception as e:
            logger.error(f"Error checking tick freeze: {e}")
            return False
    
    def _check_claude_stall(self) -> bool:
        """Check for Claude semantic stalls"""
        try:
            # Get latest Claude fragment
            fragments = list(self.fragments_dir.glob("fragment_*.md"))
            if not fragments:
                return False
            
            latest_fragment = max(fragments, key=lambda p: p.stat().st_mtime)
            fragment_tick = int(latest_fragment.stem.split("_")[1])
            
            # Get latest DAWN response
            responses = list(self.fragments_dir.glob("DAWN_response_*.md"))
            latest_response_tick = 0
            if responses:
                latest_response = max(responses, key=lambda p: p.stat().st_mtime)
                latest_response_tick = int(latest_response.stem.split("_")[1])
            
            # Update injection count
            if fragment_tick > self.state.last_claude_injection:
                self.state.injection_count += 1
                self.state.last_claude_injection = fragment_tick
            elif latest_response_tick > self.state.last_response_tick:
                self.state.injection_count = 0
                self.state.last_response_tick = latest_response_tick
            
            # Check for stall
            if self.state.injection_count >= 3:
                self._log_event("stall_warning", {
                    "last_injection_tick": self.state.last_claude_injection,
                    "last_response_tick": self.state.last_response_tick,
                    "injection_count": self.state.injection_count,
                    "warning_count": self.state.stall_warnings + 1
                })
                self.state.stall_warnings += 1
                logger.warning(f"Claude semantic stall detected: {self.state.injection_count} injections without response")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking Claude stall: {e}")
            return False
    
    def check_heartbeat(self) -> Tuple[bool, bool, List[Dict]]:
        """
        Check system heartbeat and Claude interactions
        
        Returns:
            Tuple of (freeze_detected, stall_detected, directory_anomalies)
        """
        freeze_detected = self._check_tick_freeze()
        stall_detected = self._check_claude_stall()
        directory_anomalies = self._check_directory_sizes()
        
        # Log directory anomalies
        for anomaly in directory_anomalies:
            if anomaly["type"] == "size_threshold":
                self._log_event("size_warning", anomaly)
            else:
                self._log_event("growth_warning", anomaly)
        
        return freeze_detected, stall_detected, directory_anomalies

# Create global instance
heartbeat_watchdog = HeartbeatWatchdog() 