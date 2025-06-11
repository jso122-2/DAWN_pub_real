"""
JSONL logging for DAWN tick engine
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

def ensure_log_dir() -> Path:
    """Ensure logs directory exists"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    return log_dir

def get_log_file(prefix: str) -> Path:
    """Get log file path with timestamp"""
    log_dir = ensure_log_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return log_dir / f"{prefix}_{timestamp}.jsonl"

def log_tick(ctx: Any) -> None:
    """Log tick data to JSONL file"""
    try:
        log_file = get_log_file("tick_log")
        data = ctx.to_dict()
        
        with open(log_file, "a") as f:
            f.write(json.dumps(data) + "\n")
            
    except Exception as e:
        logger.error(f"Error logging tick: {e}")

def log_metrics(metrics: Dict[str, Any]) -> None:
    """Log performance metrics to JSONL file"""
    try:
        log_file = get_log_file("metrics")
        metrics["timestamp"] = datetime.now().isoformat()
        
        with open(log_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")
            
    except Exception as e:
        logger.error(f"Error logging metrics: {e}")