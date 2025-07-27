# core/config_loader.py
"""
Configuration Loader for DAWN
Manages all configuration files and environment variables
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Centralized configuration management"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.config_dir = self.base_path / "config"
        self.data_dir = self.base_path / "data"
        self._config_cache: Dict[str, Any] = {}
        
    def load_all(self) -> Dict[str, Any]:
        """Load all configuration from various sources"""
        config = {}
        
        # 1. Load environment variables
        logger.info("Loading environment variables...")
        env_config = self._load_env()
        config["env"] = env_config
        
        # 2. Load JSON configs
        logger.info("Loading JSON configurations...")
        json_configs = self._load_json_configs()
        config.update(json_configs)
        
        # 3. Load YAML configs
        logger.info("Loading YAML configurations...")
        yaml_configs = self._load_yaml_configs()
        config.update(yaml_configs)
        
        # 4. Load data files
        logger.info("Loading data files...")
        data_files = self._load_data_files()
        config["data"] = data_files
        
        # Cache the configuration
        self._config_cache = config
        
        logger.info(f"Loaded {len(config)} configuration sections")
        return config
        
    def _load_env(self) -> Dict[str, str]:
        """Load environment variables"""
        # Load .env file if it exists
        env_file = self.base_path / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.debug(f"Loaded .env from {env_file}")
            
        # Collect DAWN-specific environment variables
        env_vars = {}
        for key, value in os.environ.items():
            if key.startswith("DAWN_"):
                env_vars[key] = value
                
        return env_vars
        
    def _load_json_configs(self) -> Dict[str, Any]:
        """Load all JSON configuration files"""
        configs = {}
        
        if not self.config_dir.exists():
            logger.warning(f"Config directory not found: {self.config_dir}")
            return configs
            
        for json_file in self.config_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                config_name = json_file.stem
                configs[config_name] = data
                logger.debug(f"Loaded {config_name}.json")
            except Exception as e:
                logger.error(f"Failed to load {json_file}: {e}")
                
        return configs
        
    def _load_yaml_configs(self) -> Dict[str, Any]:
        """Load all YAML configuration files"""
        configs = {}
        
        if not self.config_dir.exists():
            return configs
            
        for yaml_file in self.config_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                config_name = yaml_file.stem
                configs[config_name] = data
                logger.debug(f"Loaded {config_name}.yaml")
            except Exception as e:
                logger.error(f"Failed to load {yaml_file}: {e}")
                
        return configs
        
    def _load_data_files(self) -> Dict[str, Any]:
        """Load data files from the data directory"""
        data_files = {}
        
        # Load bloom registry
        bloom_registry_path = self.data_dir / "bloom" / "bloom_registry.json"
        if bloom_registry_path.exists():
            try:
                with open(bloom_registry_path, 'r') as f:
                    data_files["bloom_registry"] = json.load(f)
                logger.debug("Loaded bloom registry")
            except Exception as e:
                logger.error(f"Failed to load bloom registry: {e}")
                
        # Load schema states
        for state_file in (self.data_dir / "bloom").glob("*_state.json"):
            try:
                with open(state_file, 'r') as f:
                    state_name = state_file.stem
                    data_files[state_name] = json.load(f)
                logger.debug(f"Loaded state: {state_name}")
            except Exception as e:
                logger.error(f"Failed to load state {state_file}: {e}")
                
        return data_files
        
    def load_file(self, filepath: str) -> Dict[str, Any]:
        """Load a specific configuration file"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
            
        if path.suffix == ".json":
            with open(path, 'r') as f:
                return json.load(f)
        elif path.suffix in [".yaml", ".yml"]:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported configuration format: {path.suffix}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key"""
        # Try cache first
        if key in self._config_cache:
            return self._config_cache[key]
            
        # Check nested keys (e.g., "env.DAWN_MODE")
        if "." in key:
            parts = key.split(".")
            value = self._config_cache
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return default
            return value
            
        return default
        
    def reload(self):
        """Reload all configurations"""
        logger.info("Reloading configurations...")
        self._config_cache.clear()
        self.load_all()
        
    def save_config(self, name: str, data: Dict[str, Any], format: str = "json"):
        """Save a configuration file"""
        if format == "json":
            filepath = self.config_dir / f"{name}.json"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == "yaml":
            filepath = self.config_dir / f"{name}.yaml"
            with open(filepath, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        logger.info(f"Saved configuration: {filepath}")