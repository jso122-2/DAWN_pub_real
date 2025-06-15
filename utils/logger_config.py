# utils/logger_config.py
"""
Logging Configuration System for DAWN
Provides consciousness-aware logging with multiple formatters and handlers.
"""

import asyncio
import json
import logging
import os
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import colorama
from pythonjsonlogger import jsonlogger
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Initialize colorama for Windows
colorama.init()

class LogLevel(Enum):
    """Extended log levels for DAWN."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    CONSCIOUSNESS = 25  # Between INFO and WARNING
    QUANTUM = 35       # Between WARNING and ERROR
    EMERGENCE = 45     # Between ERROR and CRITICAL

class LogFormat(Enum):
    """Available log formats."""
    CONSOLE = "console"      # Rich console output with colors
    JSON = "json"           # Structured JSON format
    SIMPLE = "simple"       # Simple text format
    CONSCIOUSNESS = "consciousness"  # Special format for consciousness events

@dataclass
class LogConfig:
    """Configuration for a logger."""
    level: LogLevel
    format: LogFormat
    handlers: List[logging.Handler]
    propagate: bool = True

class ConsciousnessFormatter(logging.Formatter):
    """Special formatter for consciousness events."""
    def __init__(self):
        super().__init__()
        self.console = Console(theme=Theme({
            "consciousness": "cyan",
            "quantum": "magenta",
            "emergence": "yellow",
            "mood": "green",
            "scup": "blue"
        }))

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record."""
        # Add consciousness-specific fields
        if not hasattr(record, "consciousness"):
            record.consciousness = {}
        
        # Format the message
        if record.levelno == LogLevel.CONSCIOUSNESS.value:
            return self.console.print(
                f"[consciousness] {record.getMessage()}",
                style="consciousness"
            )
        elif record.levelno == LogLevel.QUANTUM.value:
            return self.console.print(
                f"[quantum] {record.getMessage()}",
                style="quantum"
            )
        elif record.levelno == LogLevel.EMERGENCE.value:
            return self.console.print(
                f"[emergence] {record.getMessage()}",
                style="emergence"
            )
        else:
            return super().format(record)

class JsonFormatter(jsonlogger.JsonFormatter):
    """JSON formatter for structured logging."""
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        """Add fields to the log record."""
        super().add_fields(log_record, record, message_dict)
        
        # Add consciousness-specific fields
        if hasattr(record, "consciousness"):
            log_record["consciousness"] = record.consciousness
        
        # Add standard fields
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno

class LoggerManager:
    """Main logger management system."""
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.loggers: Dict[str, LogConfig] = {}
        self._lock = threading.Lock()
        self._console = Console()
        
        # Register custom log levels
        logging.addLevelName(LogLevel.CONSCIOUSNESS.value, "CONSCIOUSNESS")
        logging.addLevelName(LogLevel.QUANTUM.value, "QUANTUM")
        logging.addLevelName(LogLevel.EMERGENCE.value, "EMERGENCE")
        
        # Create default logger
        self._setup_default_logger()

    def _setup_default_logger(self) -> None:
        """Set up the default logger."""
        # Create handlers
        console_handler = RichHandler(
            level=LogLevel.INFO.value,
            rich_tracebacks=True,
            markup=True
        )
        
        file_handler = logging.FileHandler(
            self.log_dir / "dawn.log",
            encoding="utf-8"
        )
        file_handler.setLevel(LogLevel.DEBUG.value)
        
        # Create formatters
        console_formatter = ConsciousnessFormatter()
        file_formatter = JsonFormatter()
        
        # Set formatters
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(LogLevel.DEBUG.value)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        
        # Store configuration
        self.loggers["root"] = LogConfig(
            level=LogLevel.DEBUG,
            format=LogFormat.CONSOLE,
            handlers=[console_handler, file_handler]
        )

    def get_logger(self, name: str) -> logging.Logger:
        """Get or create a logger."""
        with self._lock:
            if name not in self.loggers:
                # Create new logger
                logger = logging.getLogger(name)
                
                # Create handlers
                console_handler = RichHandler(
                    level=LogLevel.INFO.value,
                    rich_tracebacks=True,
                    markup=True
                )
                
                file_handler = logging.FileHandler(
                    self.log_dir / f"{name}.log",
                    encoding="utf-8"
                )
                file_handler.setLevel(LogLevel.DEBUG.value)
                
                # Create formatters
                console_formatter = ConsciousnessFormatter()
                file_formatter = JsonFormatter()
                
                # Set formatters
                console_handler.setFormatter(console_formatter)
                file_handler.setFormatter(file_formatter)
                
                # Configure logger
                logger.setLevel(LogLevel.DEBUG.value)
                logger.addHandler(console_handler)
                logger.addHandler(file_handler)
                
                # Store configuration
                self.loggers[name] = LogConfig(
                    level=LogLevel.DEBUG,
                    format=LogFormat.CONSOLE,
                    handlers=[console_handler, file_handler]
                )
            
            return logging.getLogger(name)

    def set_level(self, name: str, level: LogLevel) -> None:
        """Set log level for a logger."""
        with self._lock:
            if name in self.loggers:
                logger = logging.getLogger(name)
                logger.setLevel(level.value)
                self.loggers[name].level = level

    def set_format(self, name: str, format: LogFormat) -> None:
        """Set log format for a logger."""
        with self._lock:
            if name in self.loggers:
                config = self.loggers[name]
                
                # Remove existing handlers
                logger = logging.getLogger(name)
                for handler in config.handlers:
                    logger.removeHandler(handler)
                
                # Create new handlers with selected format
                if format == LogFormat.CONSOLE:
                    handler = RichHandler(
                        level=config.level.value,
                        rich_tracebacks=True,
                        markup=True
                    )
                    handler.setFormatter(ConsciousnessFormatter())
                elif format == LogFormat.JSON:
                    handler = logging.FileHandler(
                        self.log_dir / f"{name}.json",
                        encoding="utf-8"
                    )
                    handler.setFormatter(JsonFormatter())
                elif format == LogFormat.SIMPLE:
                    handler = logging.StreamHandler()
                    handler.setFormatter(logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    ))
                else:  # CONSCIOUSNESS
                    handler = RichHandler(
                        level=config.level.value,
                        rich_tracebacks=True,
                        markup=True
                    )
                    handler.setFormatter(ConsciousnessFormatter())
                
                # Add new handler
                logger.addHandler(handler)
                config.handlers = [handler]
                config.format = format

    def add_handler(self, name: str, handler: logging.Handler) -> None:
        """Add a handler to a logger."""
        with self._lock:
            if name in self.loggers:
                logger = logging.getLogger(name)
                logger.addHandler(handler)
                self.loggers[name].handlers.append(handler)

    def remove_handler(self, name: str, handler: logging.Handler) -> None:
        """Remove a handler from a logger."""
        with self._lock:
            if name in self.loggers:
                logger = logging.getLogger(name)
                logger.removeHandler(handler)
                self.loggers[name].handlers.remove(handler)

    def get_config(self, name: str) -> Optional[LogConfig]:
        """Get logger configuration."""
        return self.loggers.get(name)

# Global logger manager instance
logger_manager = LoggerManager()

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logger_manager.get_logger(name)

def log_consciousness(message: str, **kwargs) -> None:
    """Log a consciousness event."""
    logger = get_logger("dawn.consciousness")
    extra = {"consciousness": kwargs}
    logger.log(LogLevel.CONSCIOUSNESS.value, message, extra=extra)

def log_quantum(message: str, **kwargs) -> None:
    """Log a quantum event."""
    logger = get_logger("dawn.quantum")
    extra = {"consciousness": kwargs}
    logger.log(LogLevel.QUANTUM.value, message, extra=extra)

def log_emergence(message: str, **kwargs) -> None:
    """Log an emergence event."""
    logger = get_logger("dawn.emergence")
    extra = {"consciousness": kwargs}
    logger.log(LogLevel.EMERGENCE.value, message, extra=extra)