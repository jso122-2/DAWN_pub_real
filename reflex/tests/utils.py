from typing import Dict, Any, List
from dataclasses import dataclass
import numpy as np
from datetime import datetime

@dataclass
class MockTask:
    """Mock task for testing"""
    task_id: str
    priority: bool
    score: float
    matrix_entry: Dict[str, Any]

@dataclass
class MockResponse:
    """Mock Claude response for testing"""
    summary: str
    metadata: Dict[str, Any]
    tokens: List[str]
    embedding: List[float]

class MockClaude:
    """Simulates Claude's response generation"""
    
    @staticmethod
    def generate_response(task_id: str) -> Dict[str, Any]:
        """Generate a mock response with varying characteristics"""
        # Simulate different response patterns
        patterns = {
            "stable": {
                "summary": "Clear and focused response with minimal drift",
                "metadata": {
                    "heat": 0.3,
                    "entropy": 0.4,
                    "mood": "focused"
                },
                "tokens": ["clear", "focused", "stable"],
                "embedding": [0.1, 0.2, 0.3, 0.4, 0.5]
            },
            "drifting": {
                "summary": "Response shows signs of conceptual drift",
                "metadata": {
                    "heat": 0.7,
                    "entropy": 0.8,
                    "mood": "unstable"
                },
                "tokens": ["unclear", "drifting", "unstable"],
                "embedding": [0.8, 0.7, 0.6, 0.5, 0.4]
            },
            "overloaded": {
                "summary": "Response indicates emotional overload",
                "metadata": {
                    "heat": 0.9,
                    "entropy": 0.9,
                    "mood": "tense"
                },
                "tokens": ["overloaded", "tense", "unstable"],
                "embedding": [0.9, 0.8, 0.7, 0.6, 0.5]
            }
        }
        
        # Select pattern based on task_id
        pattern_key = "stable"
        if "drift" in task_id:
            pattern_key = "drifting"
        elif "overload" in task_id:
            pattern_key = "overloaded"
            
        return patterns[pattern_key]

class MockCAIRNMatrix:
    """Simulates CAIRN matrix behavior"""
    
    def __init__(self):
        self.entries = {}
    
    def get_entry(self, task_id: str) -> Dict[str, Any]:
        """Get matrix entry for task"""
        return self.entries.get(task_id, {
            "memory_excerpts": ["Default memory excerpt"],
            "sigil": "default/sigil"
        })
    
    def update_entry(self, task_id: str, entry: Dict[str, Any]) -> None:
        """Update matrix entry"""
        self.entries[task_id] = entry

def generate_test_tasks(num_tasks: int = 5) -> List[MockTask]:
    """Generate a list of test tasks with varying characteristics"""
    tasks = []
    for i in range(num_tasks):
        task_id = f"test_{i:03d}"
        pattern = "stable"
        if i % 3 == 1:
            pattern = "drift"
        elif i % 3 == 2:
            pattern = "overload"
            
        tasks.append(MockTask(
            task_id=f"{task_id}_{pattern}",
            priority=i % 2 == 0,
            score=0.7 + (i * 0.05),
            matrix_entry={
                "memory_excerpts": [f"Memory excerpt for {task_id}"],
                "sigil": f"{pattern}/sigil"
            }
        ))
    return tasks 