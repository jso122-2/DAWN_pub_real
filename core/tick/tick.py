"""
Main entry point for DAWN tick engine
"""

import asyncio
import logging
import os
from pathlib import Path
import yaml
from typing import Optional, Dict, Any

from ...tick_loop import TickLoop
from ...tick_signals import set_signal, get_signal
from ...tick_engine import TickEngine

log = logging.getLogger(__name__)

# Global tick loop instance
_tick_loop = None

DEFAULT_CONFIG = {
    "tick_rate": 1.0,
    "log_level": "INFO"
}

def get_config_path(config_path: str) -> str:
    """Resolve config path relative to project root."""
    if os.path.isabs(config_path):
        return config_path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(project_root, config_path)

def load_config(config_path: str) -> dict:
    """Load or create default configuration."""
    config_path = get_config_path(config_path)
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except FileNotFoundError:
        log.warning("tick_config.yaml missing → creating defaults")
        config_dir = Path(config_path).parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(DEFAULT_CONFIG, fh)
        return DEFAULT_CONFIG
    except Exception as e:
        log.error("Error loading config: %s", e)
        return DEFAULT_CONFIG

async def start_engine(config_path: str = "core/tick/tick_config.yaml"):
    """Start the tick engine with configuration."""
    global _tick_loop
    
    if _tick_loop is not None:
        log.warning("Tick engine already running")
        return
        
    config = load_config(config_path)
    engine = TickEngine(config_path)
    _tick_loop = TickLoop(engine=engine, config=config)
    
    try:
        await _tick_loop.start()
    except Exception as e:
        log.error("Error starting tick engine: %s", e)
        _tick_loop = None
        raise

async def stop_engine():
    """Stop the tick engine gracefully."""
    global _tick_loop
    
    if _tick_loop is None:
        return
        
    try:
        _tick_loop.stop()
        _tick_loop = None
    except Exception as e:
        log.error("Error stopping tick engine: %s", e)
        raise

def get_tick_loop() -> Optional[TickLoop]:
    """Get current tick loop instance"""
    return _tick_loop