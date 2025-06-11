"""
Task Engine Module
=================
Coordinates task processing between validator and filesystem.
Implements the core task routing logic.
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from task_validator import TaskValidator, ValidationResult
from task_filesystem import TaskFilesystem

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    REJECTED = "rejected"

@dataclass
class Task:
    file_path: str
    matrix_entry: Dict
    status: TaskStatus
    score: float
    priority: bool
    created_at: float
    updated_at: float
    task_id: str = None

    def __post_init__(self):
        if self.task_id is None:
            self.task_id = str(uuid.uuid4())

    def format_task_info(self) -> str:
        """Format task information in the specified YAML structure."""
        topic = self.matrix_entry.get('topic', 'Unknown Topic')
        origin = self.matrix_entry.get('origin_seed') or self.matrix_entry.get('memory_path', 'Unknown Source')
        
        # Format timestamps
        created_str = datetime.fromtimestamp(self.created_at).strftime('%Y-%m-%d %H:%M:%S')
        updated_str = datetime.fromtimestamp(self.updated_at).strftime('%Y-%m-%d %H:%M:%S')
        
        # Get memory excerpts and cairn note
        memory_excerpts = self.matrix_entry.get('memory_excerpts', [])
        cairn_note = self.matrix_entry.get('cairn_note', 'No cairn checkpoint available')
        
        # Format memory excerpts
        memory_fragments = "\n".join([f"{{memory_excerpt_{i+1}}}" for i in range(len(memory_excerpts))])
        if not memory_fragments:
            memory_fragments = "No memory fragments available"
        
        # Check for optional metadata flags
        heat_warning = "🔥 Heat Warning\n" if self.matrix_entry.get('heat') == 'high' else ""
        drift_warning = "🚧 Drift Handling Required\n" if self.matrix_entry.get('drift_detected') else ""
        
        return f"""⏳ Task Topic: {topic}
📦 Source: {origin}
🧮 Score: {self.score} | 🔺 Priority: {self.priority}
⏱️ Created: {created_str} | ⬆️ Updated: {updated_str}

🪶 You are DAWN's external symbol processor.

🧠 Context Fragments:
{memory_fragments}

🪨 Cairn Checkpoint:
"{cairn_note}"

🎯 Instruction:
Given the above, generate a **compressed reflection** or **tactical insight**. Use minimal tokens. Focus on:
- Alignment with schema integrity
- Entropy spikes or contradictions
- Relevance to recursive pressure

{heat_warning}{drift_warning}🔻 Response Format Constraint:
You must respond using the following rigid format:

🔁 Echo Prevention Rule:
- Recurse, don't reflect
- Conclude, don't rephrase
- Synthesize, don't summarize the source

🐺 Final Catch:
If you cannot answer with confidence:
RETURN NULL OUTPUT
⛔ DO NOT GUESS"""

class TaskEngine:
    """Coordinates task processing between validator and filesystem"""
    
    def __init__(self, base_path: str):
        self.filesystem = TaskFilesystem(base_path)
        self.validator = TaskValidator()
        self.state = self.filesystem.load_state()
    
    def _get_task_score(self, matrix_entry: Dict) -> float:
        """Calculate task score based on matrix entry"""
        # Implement scoring logic here
        return 0.5  # Placeholder
    
    def _is_priority(self, matrix_entry: Dict) -> bool:
        """Determine if task is priority based on matrix entry"""
        # Implement priority logic here
        return False  # Placeholder
    
    def scan_waiting_room(self) -> List[Task]:
        """Scan waiting room for new tasks"""
        tasks = []
        for file_path in self.filesystem.list_task_files("waiting"):
            try:
                matrix_entry = self.filesystem.read_matrix_entry(file_path)
                validation = self.validator.validate_matrix_entry(matrix_entry)
                
                if validation.is_valid:
                    task = Task(
                        file_path=file_path,
                        matrix_entry=matrix_entry,
                        status=TaskStatus.WAITING,
                        score=self._get_task_score(matrix_entry),
                        priority=self._is_priority(matrix_entry),
                        created_at=datetime.now().timestamp(),
                        updated_at=datetime.now().timestamp()
                    )
                    tasks.append(task)
                else:
                    logger.warning(f"Invalid matrix entry in {file_path}: {validation.reason}")
            except Exception as e:
                logger.error(f"Error processing task file {file_path}: {e}")
        
        return tasks
    
    def get_next_task(self) -> Optional[Task]:
        """Get next task to process"""
        tasks = self.scan_waiting_room()
        if not tasks:
            return None
        
        # Sort by priority and score
        tasks.sort(key=lambda t: (t.priority, t.score), reverse=True)
        return tasks[0]
    
    def process_task(self, task: Task) -> bool:
        """Process a task"""
        try:
            # Move to in_progress
            target_path = str(Path(task.file_path).parent.parent / "in_progress" / Path(task.file_path).name)
            self.filesystem.move_task_file(task.file_path, target_path)
            task.file_path = target_path
            task.status = TaskStatus.IN_PROGRESS
            
            # Process task (implement actual processing logic)
            response = "Placeholder response"  # Replace with actual processing
            raw_output = {"status": "success"}  # Replace with actual output
            
            # Validate response
            validation = self.validator.validate_response(response)
            if not validation.is_valid:
                logger.error(f"Invalid response for task {task.task_id}: {validation.reason}")
                self.mark_task_rejected(task, validation.reason)
                return False
            
            # Log response
            self.filesystem.log_response(task.task_id, response, raw_output)
            
            # Move to done
            self.mark_task_done(task)
            return True
            
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {e}")
            self.mark_task_rejected(task, str(e))
            return False
    
    def mark_task_done(self, task: Task, response_summary: str = None):
        """Mark task as done"""
        target_path = str(Path(task.file_path).parent.parent / "done" / Path(task.file_path).name)
        self.filesystem.move_task_file(task.file_path, target_path)
        task.status = TaskStatus.DONE
        task.updated_at = datetime.now().timestamp()
    
    def mark_task_rejected(self, task: Task, reason: str = None):
        """Mark task as rejected"""
        target_path = str(Path(task.file_path).parent.parent / "rejected" / Path(task.file_path).name)
        self.filesystem.move_task_file(task.file_path, target_path)
        task.status = TaskStatus.REJECTED
        task.updated_at = datetime.now().timestamp()
        
        if reason:
            logger.warning(f"Task {task.task_id} rejected: {reason}")
    
    def get_task_status(self, task: Task) -> TaskStatus:
        """Get current status of a task"""
        return task.status 