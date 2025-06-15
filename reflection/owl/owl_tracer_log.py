"""
Owl Tracer Log - Logging system for DAWN's reflection and tracing capabilities
"""

import logging
import os
from datetime import datetime
from typing import Optional, Any
import time
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('owl_tracer')

def owl_log(message: str, level: str = 'info', context: Optional[dict] = None) -> None:
    """
    Log a message with the Owl Tracer system.
    
    Args:
        message (str): The message to log
        level (str): Log level ('info', 'warning', 'error', 'debug')
        context (Optional[dict]): Additional context to include in the log
    """
    # Remove emoji and special characters
    message = message.encode('ascii', 'ignore').decode('ascii')
    
    log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'owl_trace_{datetime.now().strftime("%Y%m%d")}.log')
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
        "context": context,
    }
    
    # Use UTF-8 encoding for writing to file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{json.dumps(log_entry)}\n")
    
    # Print to console with level indicator
    level_indicator = {
        "info": "[INFO]",
        "warning": "[WARN]",
        "error": "[ERROR]",
        "debug": "[DEBUG]"
    }.get(level, "[INFO]")
    
    print(f"{level_indicator} {message}")

__all__ = ['owl_log']
