import json
from pathlib import Path
from typing import Dict

def build_context_from_task(task) -> str:
    """
    Build a context string from a task object.
    
    Args:
        task: Task object containing matrix_entry and other metadata
        
    Returns:
        str: Formatted context string for Claude
    """
    # Get the task info in the required format
    context = task.format_task_info()
    
    # Add any additional metadata or context if needed
    if task.matrix_entry.get('heat') == 'high':
        context += "\n\n⚠️ High heat task - prioritize stability and safety"
    
    if task.matrix_entry.get('drift_detected'):
        context += "\n\n⚠️ Drift detected - focus on alignment and correction"
        
    return context 