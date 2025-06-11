"""
Task Router Module
=================
Main entry point for task routing system.
Uses the new modular architecture with separate validator, filesystem, and engine components.
"""

import logging
import argparse
from pathlib import Path
from typing import Optional

from task_engine import TaskEngine, Task, TaskStatus
from task_validator import TaskValidator
from task_filesystem import TaskFilesystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TaskRouter:
    """Main task router using the new modular architecture"""
    
    def __init__(self, waiting_room_path: str = "waiting_room/claude", api_key: str = None):
        self.engine = TaskEngine(waiting_room_path)
        self.api_key = api_key
    
    def scan_waiting_room(self):
        """Scan waiting room for new tasks"""
        return self.engine.scan_waiting_room()
    
    def get_next_task(self) -> Optional[Task]:
        """Get next task to process"""
        return self.engine.get_next_task()
    
    def process_task(self, task: Task) -> bool:
        """Process a task"""
        return self.engine.process_task(task)
    
    def mark_task_done(self, task: Task, response_summary: str = None):
        """Mark task as done"""
        self.engine.mark_task_done(task, response_summary)
    
    def mark_task_rejected(self, task: Task, reason: str = None):
        """Mark task as rejected"""
        self.engine.mark_task_rejected(task, reason)
    
    def get_task_status(self, task: Task) -> TaskStatus:
        """Get current status of a task"""
        return self.engine.get_task_status(task)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Task Router")
    parser.add_argument("--waiting-room", default="waiting_room/claude",
                      help="Path to waiting room directory")
    parser.add_argument("--api-key", help="API key for external services")
    args = parser.parse_args()
    
    router = TaskRouter(args.waiting_room, args.api_key)
    
    # Process tasks
    while True:
        task = router.get_next_task()
        if not task:
            logger.info("No tasks to process")
            break
        
        logger.info(f"Processing task {task.task_id}")
        success = router.process_task(task)
        
        if success:
            logger.info(f"Task {task.task_id} completed successfully")
        else:
            logger.error(f"Task {task.task_id} failed")

if __name__ == "__main__":
    main() 