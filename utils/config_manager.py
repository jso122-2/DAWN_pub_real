# utils/config_manager.py
"""
Configuration Management System for DAWN
Provides flexible configuration management with multi-format support and hot-reload.
"""

import asyncio
import json
import os
import threading
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import yaml
import toml
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from watchfiles import watch
import jsonschema

class ConfigFormat(Enum):
    """Supported configuration formats."""
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    ENV = "env"
    PYTHON = "python"

@dataclass
class ConfigValue:
    """Represents a configuration value with metadata."""
    value: Any
    source: str
    timestamp: float
    format: ConfigFormat
    metadata: Dict[str, Any]

class ConfigSchema(BaseModel):
    """Base class for configuration schemas."""
    class Config:
        arbitrary_types_allowed = True

class ConfigManager:
    """Main configuration management system."""
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._config: Dict[str, ConfigValue] = {}
        self._schemas: Dict[str, jsonschema.Schema] = {}
        self._lock = threading.Lock()
        self._watchers: Dict[str, asyncio.Task] = {}
        self._callbacks: Dict[str, List[callable]] = {}
        self._running = False

    def register_schema(self, name: str, schema: jsonschema.Schema) -> None:
        """Register a JSON schema for configuration validation."""
        with self._lock:
            self._schemas[name] = schema

    def add_callback(self, key: str, callback: callable) -> None:
        """Add a callback for configuration changes."""
        with self._lock:
            if key not in self._callbacks:
                self._callbacks[key] = []
            self._callbacks[key].append(callback)

    async def start(self) -> None:
        """Start the configuration manager."""
        self._running = True
        # Load all configuration files
        await self._load_all_configs()
        # Start file watchers
        await self._start_watchers()

    async def stop(self) -> None:
        """Stop the configuration manager."""
        self._running = False
        # Stop all watchers
        for watcher in self._watchers.values():
            watcher.cancel()
        self._watchers.clear()

    async def _load_all_configs(self) -> None:
        """Load all configuration files from the config directory."""
        for file_path in self.config_dir.glob("**/*"):
            if file_path.is_file():
                await self._load_config_file(file_path)

    async def _load_config_file(self, file_path: Path) -> None:
        """Load a single configuration file."""
        format = self._get_format(file_path)
        if format is None:
            return

        try:
            if format == ConfigFormat.JSON:
                async with aiofiles.open(file_path, "r") as f:
                    content = await f.read()
                data = json.loads(content)
            elif format == ConfigFormat.YAML:
                async with aiofiles.open(file_path, "r") as f:
                    content = await f.read()
                data = yaml.safe_load(content)
            elif format == ConfigFormat.TOML:
                async with aiofiles.open(file_path, "r") as f:
                    content = await f.read()
                data = toml.loads(content)
            elif format == ConfigFormat.ENV:
                load_dotenv(file_path)
                data = dict(os.environ)
            elif format == ConfigFormat.PYTHON:
                # Load Python file as module
                import importlib.util
                spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                data = {k: v for k, v in module.__dict__.items() if not k.startswith("_")}
            else:
                return

            # Update configuration
            await self._update_config(data, str(file_path), format)

        except Exception as e:
            print(f"Error loading config file {file_path}: {e}")

    def _get_format(self, file_path: Path) -> Optional[ConfigFormat]:
        """Determine the format of a configuration file."""
        suffix = file_path.suffix.lower()
        if suffix == ".json":
            return ConfigFormat.JSON
        elif suffix in [".yaml", ".yml"]:
            return ConfigFormat.YAML
        elif suffix == ".toml":
            return ConfigFormat.TOML
        elif suffix == ".env":
            return ConfigFormat.ENV
        elif suffix == ".py":
            return ConfigFormat.PYTHON
        return None

    async def _update_config(self, data: Dict[str, Any], source: str, format: ConfigFormat) -> None:
        """Update configuration with new data."""
        with self._lock:
            for key, value in data.items():
                # Validate against schema if exists
                if key in self._schemas:
                    try:
                        jsonschema.validate(value, self._schemas[key])
                    except jsonschema.exceptions.ValidationError as e:
                        print(f"Validation error for {key}: {e}")
                        continue

                # Update value
                self._config[key] = ConfigValue(
                    value=value,
                    source=source,
                    timestamp=time.time(),
                    format=format,
                    metadata={}
                )

                # Call callbacks
                if key in self._callbacks:
                    for callback in self._callbacks[key]:
                        try:
                            await callback(value)
                        except Exception as e:
                            print(f"Error in config callback for {key}: {e}")

    async def _start_watchers(self) -> None:
        """Start file watchers for all configuration files."""
        for file_path in self.config_dir.glob("**/*"):
            if file_path.is_file() and self._get_format(file_path) is not None:
                self._watchers[str(file_path)] = asyncio.create_task(
                    self._watch_file(file_path)
                )

    async def _watch_file(self, file_path: Path) -> None:
        """Watch a configuration file for changes."""
        async for changes in watch(file_path):
            if not self._running:
                break
            await self._load_config_file(file_path)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        with self._lock:
            if key in self._config:
                return self._config[key].value
            return default

    def set(self, key: str, value: Any, persist: bool = False) -> None:
        """Set a configuration value."""
        with self._lock:
            # Validate against schema if exists
            if key in self._schemas:
                try:
                    jsonschema.validate(value, self._schemas[key])
                except jsonschema.exceptions.ValidationError as e:
                    raise ValueError(f"Validation error for {key}: {e}")

            # Update value
            self._config[key] = ConfigValue(
                value=value,
                source="runtime",
                timestamp=time.time(),
                format=ConfigFormat.PYTHON,
                metadata={}
            )

            # Persist if requested
            if persist:
                self._persist_value(key, value)

    def _persist_value(self, key: str, value: Any) -> None:
        """Persist a configuration value to file."""
        # Determine the appropriate file to write to
        file_path = self.config_dir / "runtime.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Read existing config
        if file_path.exists():
            with open(file_path, "r") as f:
                config = json.load(f)
        else:
            config = {}

        # Update config
        config[key] = value

        # Write back to file
        with open(file_path, "w") as f:
            json.dump(config, f, indent=2)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        with self._lock:
            return {k: v.value for k, v in self._config.items()}

    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a configuration value."""
        with self._lock:
            if key in self._config:
                return {
                    "source": self._config[key].source,
                    "timestamp": self._config[key].timestamp,
                    "format": self._config[key].format.value,
                    "metadata": self._config[key].metadata
                }
            return None

# Global configuration manager instance
config = ConfigManager()