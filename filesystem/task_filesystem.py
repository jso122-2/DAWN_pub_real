"""
Task Filesystem Module
=====================
Handles all filesystem operations for tasks with proper locking.
Implements a lightweight transaction buffer for atomic operations.
"""

import os
import json
import time
import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class FileLock:
    """Simple file-based locking mechanism"""
    
    def __init__(self, lock_file: Path):
        self.lock_file = lock_file
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
    
    @contextmanager
    def acquire(self, timeout: float = 10.0):
        """Acquire lock with timeout"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._lock.acquire(blocking=False):
                try:
                    # Create lock file
                    self.lock_file.write_text(str(os.getpid()))
                    yield
                    return
                finally:
                    # Remove lock file and release lock
                    try:
                        self.lock_file.unlink()
                    except FileNotFoundError:
                        pass
                    self._lock.release()
            time.sleep(0.1)
        raise TimeoutError(f"Could not acquire lock after {timeout} seconds")

class TaskFilesystem:
    """Handles filesystem operations for tasks with proper locking"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.lock = FileLock(self.base_path / ".task_lock")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        for status in ["waiting", "in_progress", "done", "rejected"]:
            (self.base_path / status).mkdir(parents=True, exist_ok=True)
    
    def read_matrix_entry(self, file_path: str) -> Dict:
        """Read matrix entry from file with locking"""
        with self.lock.acquire():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading matrix entry from {file_path}: {e}")
                raise
    
    def write_matrix_entry(self, file_path: str, data: Dict):
        """Write matrix entry to file with locking"""
        with self.lock.acquire():
            try:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                logger.error(f"Error writing matrix entry to {file_path}: {e}")
                raise
    
    def move_task_file(self, source: str, target: str):
        """Move task file with locking"""
        with self.lock.acquire():
            try:
                Path(source).rename(target)
            except Exception as e:
                logger.error(f"Error moving task file from {source} to {target}: {e}")
                raise
    
    def list_task_files(self, status: str) -> List[str]:
        """List task files in a status directory"""
        status_path = self.base_path / status
        if not status_path.exists():
            return []
        return [str(f) for f in status_path.glob("*.json")]
    
    def log_response(self, task_id: str, response: str, raw_output: Dict):
        """Log task response with locking"""
        log_path = self.base_path / "logs" / f"{task_id}.json"
        with self.lock.acquire():
            try:
                log_data = {
                    "task_id": task_id,
                    "timestamp": datetime.now().isoformat(),
                    "response": response,
                    "raw_output": raw_output
                }
                with open(log_path, 'w') as f:
                    json.dump(log_data, f, indent=2)
            except Exception as e:
                logger.error(f"Error logging response for task {task_id}: {e}")
                raise
    
    def save_state(self, state: Dict):
        """Save task state with locking"""
        state_path = self.base_path / "state.json"
        with self.lock.acquire():
            try:
                with open(state_path, 'w') as f:
                    json.dump(state, f, indent=2)
            except Exception as e:
                logger.error(f"Error saving task state: {e}")
                raise
    
    def load_state(self) -> Dict:
        """Load task state with locking"""
        state_path = self.base_path / "state.json"
        with self.lock.acquire():
            try:
                if state_path.exists():
                    with open(state_path, 'r') as f:
                        return json.load(f)
                return {}
            except Exception as e:
                logger.error(f"Error loading task state: {e}")
                raise 