# utils/data_persistence.py
"""
Data Persistence System for DAWN
Provides flexible data storage and retrieval with multiple backends and versioning.
"""

import asyncio
import json
import os
import sqlite3
import threading
import time
import zlib
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import aiofiles
import numpy as np
import torch
from pydantic import BaseModel

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry

class DataCategory(Enum):
    """Categories of data that can be stored."""
    CONSCIOUSNESS_STATE = "consciousness_state"
    MEMORY = "memory"
    EXPERIENCE = "experience"
    CONFIGURATION = "configuration"
    METRICS = "metrics"
    MODEL_STATE = "model_state"
    TEMPORARY = "temporary"

class StorageBackend(Enum):
    """Available storage backends."""
    JSON = "json"
    SQLITE = "sqlite"
    MEMORY = "memory"
    HYBRID = "hybrid"

@dataclass
class DataVersion:
    """Represents a version of stored data."""
    version: int
    timestamp: float
    metadata: Dict[str, Any]
    checksum: str

class StorageBackendBase:
    """Base class for storage backends."""
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self._lock = threading.Lock()

    async def save(self, key: str, data: Any, category: DataCategory, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save data to storage."""
        raise NotImplementedError

    async def load(self, key: str, category: DataCategory, version: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Load data from storage."""
        raise NotImplementedError

    async def delete(self, key: str, category: DataCategory) -> None:
        """Delete data from storage."""
        raise NotImplementedError

    async def list_versions(self, key: str, category: DataCategory) -> List[DataVersion]:
        """List available versions of data."""
        raise NotImplementedError

class JSONStorageBackend(StorageBackendBase):
    """JSON-based storage backend."""
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save(self, key: str, data: Any, category: DataCategory, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save data to JSON file."""
        metadata = metadata or {}
        metadata["timestamp"] = time.time()
        metadata["category"] = category.value

        # Get next version number
        versions = await self.list_versions(key, category)
        version = len(versions) + 1

        # Prepare data
        data_dict = {
            "version": version,
            "metadata": metadata,
            "data": data
        }

        # Compress data
        compressed = zlib.compress(json.dumps(data_dict).encode())

        # Save to file
        file_path = self.base_path / f"{category.value}/{key}_{version}.json.gz"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(compressed)

    async def load(self, key: str, category: DataCategory, version: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Load data from JSON file."""
        if version is None:
            versions = await self.list_versions(key, category)
            if not versions:
                raise KeyError(f"No data found for key {key} in category {category}")
            version = versions[-1].version

        file_path = self.base_path / f"{category.value}/{key}_{version}.json.gz"
        if not file_path.exists():
            raise KeyError(f"Version {version} not found for key {key} in category {category}")

        async with aiofiles.open(file_path, "rb") as f:
            compressed = await f.read()
        
        data_dict = json.loads(zlib.decompress(compressed).decode())
        return data_dict["data"], data_dict["metadata"]

    async def delete(self, key: str, category: DataCategory) -> None:
        """Delete all versions of data."""
        pattern = self.base_path / f"{category.value}/{key}_*.json.gz"
        for file_path in pattern.parent.glob(pattern.name):
            file_path.unlink()

    async def list_versions(self, key: str, category: DataCategory) -> List[DataVersion]:
        """List available versions of data."""
        pattern = self.base_path / f"{category.value}/{key}_*.json.gz"
        versions = []
        
        for file_path in pattern.parent.glob(pattern.name):
            version = int(file_path.stem.split("_")[-1])
            async with aiofiles.open(file_path, "rb") as f:
                compressed = await f.read()
            data_dict = json.loads(zlib.decompress(compressed).decode())
            versions.append(DataVersion(
                version=version,
                timestamp=data_dict["metadata"]["timestamp"],
                metadata=data_dict["metadata"],
                checksum=hash(compressed)
            ))
        
        return sorted(versions, key=lambda v: v.version)

class SQLiteStorageBackend(StorageBackendBase):
    """SQLite-based storage backend."""
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.db_path = self.base_path / "data.db"
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    key TEXT,
                    category TEXT,
                    version INTEGER,
                    timestamp REAL,
                    metadata TEXT,
                    data BLOB,
                    PRIMARY KEY (key, category, version)
                )
            """)

    async def save(self, key: str, data: Any, category: DataCategory, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save data to SQLite database."""
        metadata = metadata or {}
        metadata["timestamp"] = time.time()
        metadata["category"] = category.value

        # Get next version number
        versions = await self.list_versions(key, category)
        version = len(versions) + 1

        # Prepare data
        data_dict = {
            "version": version,
            "metadata": metadata,
            "data": data
        }

        # Compress data
        compressed = zlib.compress(json.dumps(data_dict).encode())

        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO data (key, category, version, timestamp, metadata, data) VALUES (?, ?, ?, ?, ?, ?)",
                (key, category.value, version, time.time(), json.dumps(metadata), compressed)
            )

    async def load(self, key: str, category: DataCategory, version: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Load data from SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            if version is None:
                cursor = conn.execute(
                    "SELECT data, metadata FROM data WHERE key = ? AND category = ? ORDER BY version DESC LIMIT 1",
                    (key, category.value)
                )
            else:
                cursor = conn.execute(
                    "SELECT data, metadata FROM data WHERE key = ? AND category = ? AND version = ?",
                    (key, category.value, version)
                )
            
            row = cursor.fetchone()
            if not row:
                raise KeyError(f"No data found for key {key} in category {category}")

            compressed, metadata_json = row
            data_dict = json.loads(zlib.decompress(compressed).decode())
            return data_dict["data"], json.loads(metadata_json)

    async def delete(self, key: str, category: DataCategory) -> None:
        """Delete all versions of data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM data WHERE key = ? AND category = ?",
                (key, category.value)
            )

    async def list_versions(self, key: str, category: DataCategory) -> List[DataVersion]:
        """List available versions of data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT version, timestamp, metadata, data FROM data WHERE key = ? AND category = ? ORDER BY version",
                (key, category.value)
            )
            
            versions = []
            for row in cursor:
                version, timestamp, metadata_json, compressed = row
                versions.append(DataVersion(
                    version=version,
                    timestamp=timestamp,
                    metadata=json.loads(metadata_json),
                    checksum=hash(compressed)
                ))
            
            return versions

class MemoryStorageBackend(StorageBackendBase):
    """In-memory storage backend."""
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self._storage: Dict[str, Dict[str, List[Tuple[int, float, Dict[str, Any], Any]]]] = {}

    async def save(self, key: str, data: Any, category: DataCategory, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save data to memory."""
        metadata = metadata or {}
        metadata["timestamp"] = time.time()
        metadata["category"] = category.value

        with self._lock:
            if category.value not in self._storage:
                self._storage[category.value] = {}
            if key not in self._storage[category.value]:
                self._storage[category.value][key] = []
            
            versions = self._storage[category.value][key]
            version = len(versions) + 1
            versions.append((version, time.time(), metadata, data))

    async def load(self, key: str, category: DataCategory, version: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Load data from memory."""
        with self._lock:
            if category.value not in self._storage or key not in self._storage[category.value]:
                raise KeyError(f"No data found for key {key} in category {category}")
            
            versions = self._storage[category.value][key]
            if not versions:
                raise KeyError(f"No data found for key {key} in category {category}")
            
            if version is None:
                version_data = versions[-1]
            else:
                version_data = next((v for v in versions if v[0] == version), None)
                if not version_data:
                    raise KeyError(f"Version {version} not found for key {key} in category {category}")
            
            return version_data[3], version_data[2]

    async def delete(self, key: str, category: DataCategory) -> None:
        """Delete all versions of data."""
        with self._lock:
            if category.value in self._storage:
                self._storage[category.value].pop(key, None)

    async def list_versions(self, key: str, category: DataCategory) -> List[DataVersion]:
        """List available versions of data."""
        with self._lock:
            if category.value not in self._storage or key not in self._storage[category.value]:
                return []
            
            return [
                DataVersion(
                    version=v[0],
                    timestamp=v[1],
                    metadata=v[2],
                    checksum=hash(str(v[3]))
                )
                for v in self._storage[category.value][key]
            ]

class HybridStorageBackend(StorageBackendBase):
    """Hybrid storage backend that uses multiple backends."""
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.backends = {
            StorageBackend.JSON: JSONStorageBackend(base_path),
            StorageBackend.SQLITE: SQLiteStorageBackend(base_path),
            StorageBackend.MEMORY: MemoryStorageBackend(base_path)
        }
        self._category_backend_map = {
            DataCategory.CONSCIOUSNESS_STATE: StorageBackend.SQLITE,
            DataCategory.MEMORY: StorageBackend.SQLITE,
            DataCategory.EXPERIENCE: StorageBackend.JSON,
            DataCategory.CONFIGURATION: StorageBackend.JSON,
            DataCategory.METRICS: StorageBackend.SQLITE,
            DataCategory.MODEL_STATE: StorageBackend.JSON,
            DataCategory.TEMPORARY: StorageBackend.MEMORY
        }

    def _get_backend(self, category: DataCategory) -> StorageBackendBase:
        """Get the appropriate backend for a category."""
        backend_type = self._category_backend_map.get(category, StorageBackend.JSON)
        return self.backends[backend_type]

    async def save(self, key: str, data: Any, category: DataCategory, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save data using appropriate backend."""
        backend = self._get_backend(category)
        await backend.save(key, data, category, metadata)

    async def load(self, key: str, category: DataCategory, version: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Load data using appropriate backend."""
        backend = self._get_backend(category)
        return await backend.load(key, category, version)

    async def delete(self, key: str, category: DataCategory) -> None:
        """Delete data using appropriate backend."""
        backend = self._get_backend(category)
        await backend.delete(key, category)

    async def list_versions(self, key: str, category: DataCategory) -> List[DataVersion]:
        """List versions using appropriate backend."""
        backend = self._get_backend(category)
        return await backend.list_versions(key, category)

class DataPersistence:
    """Main data persistence system."""
    def __init__(self, base_path: str = "data"):
        self.backend = HybridStorageBackend(base_path)
        self._checkpoints: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    async def save(self, key: str, data: Any, category: DataCategory, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save data."""
        await self.backend.save(key, data, category, metadata)

    async def load(self, key: str, category: DataCategory, version: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Load data."""
        return await self.backend.load(key, category, version)

    async def delete(self, key: str, category: DataCategory) -> None:
        """Delete data."""
        await self.backend.delete(key, category)

    async def list_versions(self, key: str, category: DataCategory) -> List[DataVersion]:
        """List available versions of data."""
        return await self.backend.list_versions(key, category)

    def create_checkpoint(self, name: str) -> str:
        """Create a checkpoint of current state."""
        with self._lock:
            checkpoint_id = f"{name}_{int(time.time())}"
            self._checkpoints[checkpoint_id] = {
                "name": name,
                "timestamp": time.time(),
                "metadata": {}
            }
            return checkpoint_id

    def restore_checkpoint(self, checkpoint_id: str) -> None:
        """Restore state from a checkpoint."""
        with self._lock:
            if checkpoint_id not in self._checkpoints:
                raise KeyError(f"Checkpoint {checkpoint_id} not found")
            # Implementation would depend on what state needs to be restored

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List available checkpoints."""
        with self._lock:
            return [
                {
                    "id": checkpoint_id,
                    "name": data["name"],
                    "timestamp": data["timestamp"],
                    "metadata": data["metadata"]
                }
                for checkpoint_id, data in self._checkpoints.items()
            ]

# Global persistence instance
persistence = DataPersistence()

# Convenience functions
def save_data(key: str, data: Any, category: str = "custom") -> bool:
    """Save data to persistence"""
    try:
        cat = DataCategory(category)
    except:
        cat = DataCategory.CUSTOM
    
    return persistence.save(key, data, cat)

def load_data(key: str, category: str = "custom") -> Optional[Any]:
    """Load data from persistence"""
    try:
        cat = DataCategory(category)
    except:
        cat = DataCategory.CUSTOM
    
    return persistence.load(key, cat)

def create_checkpoint(name: Optional[str] = None) -> str:
    """Create a checkpoint"""
    return persistence.create_checkpoint(name)

def restore_checkpoint(name: str) -> bool:
    """Restore from checkpoint"""
    return persistence.restore_checkpoint(name)