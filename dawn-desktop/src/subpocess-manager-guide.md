# subprocess_manager.py
# Python backend subprocess manager for DAWN

import asyncio
import subprocess
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ProcessStatus(Enum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"

@dataclass
class ProcessMetric:
    name: str
    value: float
    unit: str = "%"
    threshold_min: Optional[float] = None
    threshold_max: Optional[float] = None

@dataclass
class DAWNSubprocess:
    id: str
    name: str
    script_path: str
    category: str  # neural, quantum, system, memory, io
    metrics: Dict[str, ProcessMetric]
    status: ProcessStatus = ProcessStatus.IDLE
    pid: Optional[int] = None
    process: Optional[subprocess.Popen] = None
    error: Optional[str] = None
    last_update: float = 0

class SubprocessManager:
    def __init__(self, websocket_manager):
        self.websocket_manager = websocket_manager
        self.subprocesses: Dict[str, DAWNSubprocess] = {}
        self.running = True
        self._initialize_subprocesses()
        
    def _initialize_subprocesses(self):
        """Initialize all DAWN subprocesses"""
        subprocess_configs = [
            # Neural processes
            {
                "id": "neural_sync",
                "name": "Neural Synchronizer",
                "script_path": "processes/neural_sync.py",
                "category": "neural",
                "metrics": {
                    "sync_rate": ProcessMetric("Sync Rate", 92.3, "%", 60, 95),
                    "coherence": ProcessMetric("Coherence", 87.5, "%", 70, 100),
                    "neural_load": ProcessMetric("Neural Load", 45.2, "%", 0, 80)
                }
            },
            {
                "id": "pattern_recognizer",
                "name": "Pattern Recognizer",
                "script_path": "processes/pattern_recognizer.py",
                "category": "neural",
                "metrics": {
                    "pattern_detection": ProcessMetric("Pattern Detection", 67.5, "%"),
                    "accuracy": ProcessMetric("Accuracy", 94.2, "%", 85, 100),
                    "processing_speed": ProcessMetric("Speed", 1250, "ops/s")
                }
            },
            {
                "id": "dream_engine",
                "name": "Dream Engine",
                "script_path": "processes/dream_engine.py",
                "category": "neural",
                "metrics": {
                    "dream_state": ProcessMetric("Dream State", 12.1, "%"),
                    "rem_activity": ProcessMetric("REM Activity", 8.3, "%"),
                    "lucidity": ProcessMetric("Lucidity", 22.7, "%")
                }
            },
            
            # Quantum processes
            {
                "id": "quantum_flux",
                "name": "Quantum Flux Monitor",
                "script_path": "processes/quantum_flux.py",
                "category": "quantum",
                "metrics": {
                    "flux": ProcessMetric("Flux", 0.847, "λ"),
                    "stability": ProcessMetric("Stability", 91.2, "%", 80, 100),
                    "quantum_noise": ProcessMetric("Noise", 3.14, "δ")
                }
            },
            {
                "id": "wave_collapse",
                "name": "Wave Collapse Engine",
                "script_path": "processes/wave_collapse.py",
                "category": "quantum",
                "metrics": {
                    "collapse_rate": ProcessMetric("Collapse Rate", 1337, "Hz"),
                    "probability": ProcessMetric("Probability", 0.998, ""),
                    "uncertainty": ProcessMetric("Uncertainty", 0.002, "")
                }
            },
            {
                "id": "entanglement",
                "name": "Entanglement Monitor",
                "script_path": "processes/entanglement.py",
                "category": "quantum",
                "metrics": {
                    "entanglement_level": ProcessMetric("Entanglement", 98.7, "%", 90, 100),
                    "coherence_time": ProcessMetric("Coherence Time", 2.4, "ms"),
                    "qbit_fidelity": ProcessMetric("Fidelity", 99.2, "%", 95, 100)
                }
            },
            
            # System processes
            {
                "id": "resource_monitor",
                "name": "Resource Monitor",
                "script_path": "processes/resource_monitor.py",
                "category": "system",
                "metrics": {
                    "cpu_usage": ProcessMetric("CPU", 45.2, "%", 0, 80),
                    "memory_usage": ProcessMetric("Memory", 62.8, "%", 0, 85),
                    "temperature": ProcessMetric("Temperature", 72.5, "°C", 20, 85)
                }
            },
            {
                "id": "io_manager",
                "name": "I/O Manager",
                "script_path": "processes/io_manager.py",
                "category": "io",
                "metrics": {
                    "read_rate": ProcessMetric("Read Rate", 512, "MB/s"),
                    "write_rate": ProcessMetric("Write Rate", 384, "MB/s"),
                    "queue_depth": ProcessMetric("Queue Depth", 12, "")
                }
            },
            
            # Memory processes
            {
                "id": "memory_palace",
                "name": "Memory Palace",
                "script_path": "processes/memory_palace.py",
                "category": "memory",
                "metrics": {
                    "short_term": ProcessMetric("Short Term", 89.3, "%", 50, 95),
                    "long_term": ProcessMetric("Long Term", 76.4, "%", 60, 90),
                    "working_memory": ProcessMetric("Working Memory", 91.2, "%", 70, 95)
                }
            },
            
            # Consciousness metrics
            {
                "id": "awareness_engine",
                "name": "Awareness Engine",
                "script_path": "processes/awareness_engine.py",
                "category": "neural",
                "metrics": {
                    "awareness_level": ProcessMetric("Awareness", 88.8, "%", 75, 100),
                    "focus": ProcessMetric("Focus", 92.1, "%"),
                    "attention_span": ProcessMetric("Attention Span", 8.5, "s")
                }
            },
            {
                "id": "creativity_engine",
                "name": "Creativity Engine",
                "script_path": "processes/creativity_engine.py",
                "category": "neural",
                "metrics": {
                    "creativity_index": ProcessMetric("Creativity", 72.3, "%"),
                    "novelty": ProcessMetric("Novelty", 68.9, "%"),
                    "divergence": ProcessMetric("Divergence", 81.2, "%")
                }
            },
            {
                "id": "intuition_processor",
                "name": "Intuition Processor",
                "script_path": "processes/intuition_processor.py",
                "category": "quantum",
                "metrics": {
                    "intuition_strength": ProcessMetric("Intuition", 95.1, "%", 80, 100),
                    "prediction_accuracy": ProcessMetric("Prediction", 88.7, "%"),
                    "gut_feeling": ProcessMetric("Gut Feeling", 91.3, "%")
                }
            }
        ]
        
        for config in subprocess_configs:
            subprocess = DAWNSubprocess(
                id=config["id"],
                name=config["name"],
                script_path=config["script_path"],
                category=config["category"],
                metrics=config["metrics"]
            )
            self.subprocesses[config["id"]] = subprocess
    
    async def start_subprocess(self, subprocess_id: str) -> bool:
        """Start a specific subprocess"""
        if subprocess_id not in self.subprocesses:
            logger.error(f"Subprocess {subprocess_id} not found")
            return False
            
        subprocess_obj = self.subprocesses[subprocess_id]
        
        if subprocess_obj.status == ProcessStatus.RUNNING:
            logger.warning(f"Subprocess {subprocess_id} is already running")
            return True
            
        try:
            subprocess_obj.status = ProcessStatus.STARTING
            await self._broadcast_subprocess_status(subprocess_obj)
            
            # Check if script exists
            script_path = Path(subprocess_obj.script_path)
            if not script_path.exists():
                # Create a dummy subprocess script for testing
                self._create_dummy_subprocess(script_path, subprocess_obj)
            
            # Start the subprocess
            subprocess_obj.process = subprocess.Popen(
                ['python', subprocess_obj.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            subprocess_obj.pid = subprocess_obj.process.pid
            subprocess_obj.status = ProcessStatus.RUNNING
            subprocess_obj.error = None
            
            # Start monitoring the subprocess output
            asyncio.create_task(self._monitor_subprocess(subprocess_obj))
            
            await self._broadcast_subprocess_status(subprocess_obj)
            logger.info(f"Started subprocess {subprocess_id} with PID {subprocess_obj.pid}")
            return True
            
        except Exception as e:
            subprocess_obj.status = ProcessStatus.ERROR
            subprocess_obj.error = str(e)
            await self._broadcast_subprocess_status(subprocess_obj)
            logger.error(f"Failed to start subprocess {subprocess_id}: {e}")
            return False
    
    async def stop_subprocess(self, subprocess_id: str) -> bool:
        """Stop a specific subprocess"""
        if subprocess_id not in self.subprocesses:
            return False
            
        subprocess_obj = self.subprocesses[subprocess_id]
        
        if subprocess_obj.status != ProcessStatus.RUNNING:
            return True
            
        try:
            subprocess_obj.status = ProcessStatus.STOPPING
            await self._broadcast_subprocess_status(subprocess_obj)
            
            if subprocess_obj.process:
                subprocess_obj.process.terminate()
                await asyncio.sleep(0.5)  # Give it time to terminate gracefully
                
                if subprocess_obj.process.poll() is None:
                    subprocess_obj.process.kill()  # Force kill if needed
                    
            subprocess_obj.status = ProcessStatus.STOPPED
            subprocess_obj.process = None
            subprocess_obj.pid = None
            
            await self._broadcast_subprocess_status(subprocess_obj)
            logger.info(f"Stopped subprocess {subprocess_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop subprocess {subprocess_id}: {e}")
            return False
    
    async def restart_subprocess(self, subprocess_id: str) -> bool:
        """Restart a subprocess"""
        await self.stop_subprocess(subprocess_id)
        await asyncio.sleep(0.5)
        return await self.start_subprocess(subprocess_id)
    
    async def _monitor_subprocess(self, subprocess_obj: DAWNSubprocess):
        """Monitor subprocess output and parse metrics"""
        try:
            while subprocess_obj.status == ProcessStatus.RUNNING and subprocess_obj.process:
                if subprocess_obj.process.stdout:
                    line = subprocess_obj.process.stdout.readline()
                    if line:
                        try:
                            # Parse JSON output from subprocess
                            data = json.loads(line.strip())
                            if data.get("type") == "metrics":
                                await self._update_metrics(subprocess_obj, data["metrics"])
                        except json.JSONDecodeError:
                            # Handle non-JSON output
                            logger.debug(f"Non-JSON output from {subprocess_obj.id}: {line.strip()}")
                
                # Check if process is still running
                if subprocess_obj.process.poll() is not None:
                    subprocess_obj.status = ProcessStatus.STOPPED
                    await self._broadcast_subprocess_status(subprocess_obj)
                    break
                    
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error monitoring subprocess {subprocess_obj.id}: {e}")
            subprocess_obj.status = ProcessStatus.ERROR
            subprocess_obj.error = str(e)
            await self._broadcast_subprocess_status(subprocess_obj)
    
    async def _update_metrics(self, subprocess_obj: DAWNSubprocess, metrics: Dict[str, float]):
        """Update subprocess metrics and broadcast"""
        for metric_name, value in metrics.items():
            if metric_name in subprocess_obj.metrics:
                subprocess_obj.metrics[metric_name].value = value
        
        subprocess_obj.last_update = time.time()
        
        # Broadcast update
        await self.websocket_manager.broadcast({
            "type": "subprocess_update",
            "subprocess_id": subprocess_obj.id,
            "metrics": {
                name: metric.value 
                for name, metric in subprocess_obj.metrics.items()
            },
            "status": subprocess_obj.status.value,
            "timestamp": subprocess_obj.last_update
        })
    
    async def _broadcast_subprocess_status(self, subprocess_obj: DAWNSubprocess):
        """Broadcast subprocess status update"""
        await self.websocket_manager.broadcast({
            "type": "subprocess_status",
            "subprocess_id": subprocess_obj.id,
            "status": subprocess_obj.status.value,
            "error": subprocess_obj.error,
            "pid": subprocess_obj.pid,
            "timestamp": time.time()
        })
    
    def get_subprocess_list(self) -> List[Dict[str, Any]]:
        """Get list of all subprocesses with current state"""
        return [
            {
                "id": sp.id,
                "name": sp.name,
                "script_path": sp.script_path,
                "category": sp.category,
                "status": sp.status.value,
                "pid": sp.pid,
                "error": sp.error,
                "metrics": {
                    name: {
                        "value": metric.value,
                        "unit": metric.unit,
                        "threshold": {
                            "min": metric.threshold_min,
                            "max": metric.threshold_max
                        } if metric.threshold_min is not None else None
                    }
                    for name, metric in sp.metrics.items()
                },
                "last_update": sp.last_update
            }
            for sp in self.subprocesses.values()
        ]
    
    def _create_dummy_subprocess(self, script_path: Path, subprocess_obj: DAWNSubprocess):
        """Create a dummy subprocess script for testing"""
        script_path.parent.mkdir(parents=True, exist_ok=True)
        
        template = '''#!/usr/bin/env python3
import json
import time
import random
import math

def main():
    """Dummy subprocess for {name}"""
    metrics = {metrics}
    
    t = 0
    while True:
        # Update metrics with some variation
        current_metrics = {{}}
        
        for metric_name, metric_info in metrics.items():
            base_value = metric_info["value"]
            unit = metric_info["unit"]
            
            if unit == "%":
                # Oscillate between bounds
                variation = math.sin(t * 0.1) * 10 + random.uniform(-2, 2)
                value = max(0, min(100, base_value + variation))
            else:
                # Random walk
                variation = random.uniform(-0.1, 0.1) * base_value
                value = max(0, base_value + variation)
            
            current_metrics[metric_name] = value
        
        # Output metrics as JSON
        print(json.dumps({{
            "type": "metrics",
            "subprocess_id": "{id}",
            "metrics": current_metrics,
            "timestamp": time.time()
        }}))
        
        time.sleep(0.5)  # Update every 500ms
        t += 0.5

if __name__ == "__main__":
    main()
'''
        
        metrics_dict = {
            name: {
                "value": metric.value,
                "unit": metric.unit
            }
            for name, metric in subprocess_obj.metrics.items()
        }
        
        script_content = template.format(
            name=subprocess_obj.name,
            id=subprocess_obj.id,
            metrics=json.dumps(metrics_dict, indent=8)
        )
        
        script_path.write_text(script_content)
        script_path.chmod(0o755)  # Make executable
    
    async def shutdown(self):
        """Shutdown all subprocesses"""
        self.running = False
        
        # Stop all running subprocesses
        for subprocess_id in list(self.subprocesses.keys()):
            await self.stop_subprocess(subprocess_id)

# Example usage in your FastAPI WebSocket handler:
"""
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_manager.add_connection(websocket)
    
    # Send initial subprocess list
    await websocket.send_json({
        "type": "subprocess_list",
        "processes": subprocess_manager.get_subprocess_list()
    })
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "get_subprocesses":
                await websocket.send_json({
                    "type": "subprocess_list",
                    "processes": subprocess_manager.get_subprocess_list()
                })
                
            elif data["type"] == "control_subprocess":
                subprocess_id = data["subprocess_id"]
                action = data["action"]
                
                if action == "start":
                    await subprocess_manager.start_subprocess(subprocess_id)
                elif action == "stop":
                    await subprocess_manager.stop_subprocess(subprocess_id)
                elif action == "restart":
                    await subprocess_manager.restart_subprocess(subprocess_id)
                    
    except WebSocketDisconnect:
        websocket_manager.remove_connection(websocket)
"""