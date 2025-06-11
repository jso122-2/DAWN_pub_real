"""
tick_config.py - Configuration management for DAWN's tick engine
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "tick_interval": 1.0,
    "tick_interval_min": 0.1,
    "tick_interval_max": 5.0,
    "max_ticks": None,  # None = run forever
    "max_errors": 5,
    "error_retry_delay": 2.0,
    
    "subsystems": [
        "pulse",
        "schema", 
        "memory",
        "visual"
    ],
    
    "thresholds": {
        "scup_trigger": 0.8,
        "heat_critical": 0.95,
        "entropy_high": 0.7
    },
    
    "cairn": {
        "enabled": True,
        "cooldown": 30.0,  # seconds between Claude queries
        "max_queries_per_hour": 10
    },
    
    "logging": {
        "level": "INFO",
        "log_dir": "logs",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    
    "performance": {
        "monitor_interval": 5.0,
        "metrics_buffer_size": 100
    }
}


class TickConfig:
    """Configuration manager for tick engine"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = DEFAULT_CONFIG.copy()
        
        if config_path:
            self.load_from_file(config_path)
        
        # Load environment overrides
        self._load_env_overrides()
    
    def load_from_file(self, path: str) -> None:
        """Load configuration from YAML or JSON file"""
        path = Path(path)
        
        if not path.exists():
            print(f"Config file not found: {path}, using defaults")
            return
        
        try:
            with open(path, 'r') as f:
                if path.suffix in ['.yaml', '.yml']:
                    file_config = yaml.safe_load(f)
                elif path.suffix == '.json':
                    file_config = json.load(f)
                else:
                    raise ValueError(f"Unsupported config format: {path.suffix}")
            
            # Merge with defaults
            self._deep_merge(self.config, file_config)
            print(f"Loaded config from: {path}")
            
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
    
    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """Deep merge update dict into base dict"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def _load_env_overrides(self) -> None:
        """Load configuration overrides from environment variables"""
        # DAWN_TICK_INTERVAL
        if interval := os.getenv("DAWN_TICK_INTERVAL"):
            self.config["tick_interval"] = float(interval)
        
        # DAWN_MAX_TICKS
        if max_ticks := os.getenv("DAWN_MAX_TICKS"):
            self.config["max_ticks"] = int(max_ticks)
        
        # DAWN_CAIRN_ENABLED
        if cairn := os.getenv("DAWN_CAIRN_ENABLED"):
            self.config["cairn"]["enabled"] = cairn.lower() in ["true", "1", "yes"]
        
        # DAWN_LOG_LEVEL
        if log_level := os.getenv("DAWN_LOG_LEVEL"):
            self.config["logging"]["level"] = log_level.upper()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key (supports dot notation)"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: str) -> None:
        """Save current configuration to file"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                json.dump(self.config, f, indent=2)


# Convenience function
def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults"""
    config = TickConfig(path)
    return config.config