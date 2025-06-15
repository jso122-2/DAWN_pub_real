"""
DAWN Neural System - FastAPI Backend
Provides real-time neural metrics and WebSocket streaming for the desktop app
"""

# Standard library imports
import asyncio
import json
import logging
import math
import os
import random
import time
import threading
import sys
import io
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta

# Set up logging first with UTF-8 encoding
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Create UTF-8 compatible handlers
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setStream(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))
file_handler = logging.FileHandler('dawn_backend.log', mode='a', encoding='utf-8')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[stream_handler, file_handler]
)
logger = logging.getLogger(__name__)

logger.info("DAWN Backend logging initialized at %s level", LOG_LEVEL)
logger.info("Logs also written to: dawn_backend.log")

# Log psutil availability warning if needed
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil not available - CPU/memory monitoring disabled for processes")

# Third-party imports
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
import asyncio
import glob
import base64
from PIL import Image

# Try to import enhanced conversation system
try:
    from conversation import DAWNConversation as EnhancedDAWNConversation
    ENHANCED_CONVERSATION_AVAILABLE = True
    logger.info("✨ Enhanced conversation system loaded")
except ImportError:
    ENHANCED_CONVERSATION_AVAILABLE = False
    logger.warning("Enhanced conversation system not available - using basic conversation")

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Import DAWN modules
from cognitive.consciousness import DAWNConsciousness
from cognitive.conversation import DAWNConversation
from cognitive.spontaneity import DAWNSpontaneity

# Import memory manager
try:
    from core.memory_manager import get_memory_manager
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    logger.warning("Memory manager not available - memory features disabled")

# Import conversation system
try:
    from conversation import DAWNConversation as EnhancedDAWNConversation
    ENHANCED_CONVERSATION_AVAILABLE = True
except ImportError:
    ENHANCED_CONVERSATION_AVAILABLE = False
    logger.warning("Enhanced conversation system not available - using basic conversation")

# Set specific loggers
uvicorn_logger = logging.getLogger("uvicorn")
fastapi_logger = logging.getLogger("fastapi")

# Enable debug logging for WebSocket connections
ws_logger = logging.getLogger("websockets")
ws_logger.setLevel(logging.INFO)

# Log psutil availability warning if needed
if not PSUTIL_AVAILABLE:
    logger.warning("psutil not available - CPU/memory monitoring disabled for processes")

# Pydantic models for API
class MetricsResponse(BaseModel):
    scup: float
    entropy: float
    heat: float
    mood: str
    timestamp: float
    tick_count: int

class SubsystemInfo(BaseModel):
    id: str
    name: str
    status: str
    state: Dict[str, Any]

class SubsystemCreate(BaseModel):
    name: str
    config: Dict[str, Any] = {}

class AlertThreshold(BaseModel):
    metric: str
    threshold: float
    direction: str = "above"

# New Pydantic models for Tick Engine Control
class TickStatus(BaseModel):
    tick_number: int
    is_running: bool
    is_paused: bool
    interval_ms: int
    uptime_seconds: float
    total_ticks: int
    avg_tick_duration_ms: float
    last_tick_timestamp: Optional[float]

class TickTiming(BaseModel):
    interval_ms: int

class TickConfig(BaseModel):
    interval_ms: int
    auto_start: bool
    enable_logging: bool
    max_tick_duration_ms: int

class TickUpdate(BaseModel):
    tick_number: int
    timestamp: float
    metrics: Dict[str, Any]
    duration_ms: float
    controller_state: str

# Minimal DAWN Chat Models
class ChatMessage(BaseModel):
    text: str

# Enhanced response models for new endpoints
class ConsciousnessState(BaseModel):
    state: str
    description: str
    significant_change: bool

class ActionResult(BaseModel):
    action: str
    success: bool
    timestamp: str

class ConversationContext(BaseModel):
    user_message: str
    state_transitions: str
    recent_context: List[Dict[str, Any]]

class EnhancedTalkResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    action_result: Optional[ActionResult]
    metrics: Dict[str, Any]
    consciousness_state: ConsciousnessState
    tick_status: Dict[str, Any]
    timestamp: str
    conversation_context: ConversationContext
    session_id: str

class SpontaneousThought(BaseModel):
    thought: str
    timestamp: str
    state: str
    priority: int

class ThoughtsResponse(BaseModel):
    thoughts: List[SpontaneousThought]
    count: int
    current_state: str
    spontaneity_status: Dict[str, Any]
    timestamp: str
    cleared: bool

# New models for enhanced consciousness features
class ReflectivePhrase(BaseModel):
    phrase: str
    trigger_context: str
    consciousness_state: str
    timestamp: str
    depth_level: int

class ReflectionsResponse(BaseModel):
    reflections: List[ReflectivePhrase]
    count: int
    current_state: str
    timestamp: str

class ConsciousnessInfluence(BaseModel):
    mood_shift: Optional[float] = None
    entropy_injection: Optional[float] = None  
    pressure_adjustment: Optional[float] = None
    influence_type: str = "gentle"
    duration_seconds: float = 30.0

class InfluenceResult(BaseModel):
    success: bool
    applied_influences: Dict[str, float]
    predicted_effects: Dict[str, str]
    timestamp: str

class SessionMessage(BaseModel):
    text: str
    session_id: Optional[str] = None

# New models for Python process control
class ProcessStartRequest(BaseModel):
    process_id: str
    script: str
    parameters: Dict[str, Any] = {}
    modules: List[Dict[str, Any]] = []

class ProcessStopRequest(BaseModel):
    process_id: str

class ProcessStatus(BaseModel):
    process_id: str
    script: str
    status: str  # 'running', 'stopped', 'starting', 'stopping', 'error'
    pid: Optional[int] = None
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    start_time: Optional[float] = None
    error: Optional[str] = None

class ProcessResponse(BaseModel):
    success: bool
    message: str
    process_status: Optional[ProcessStatus] = None

# New models for enhanced consciousness features
class TalkRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    include_tracer: bool = True
    rebloom_priority: Optional[int] = None  # 1-5 scale

class TalkResponse(BaseModel):
    text: str
    emotion: str
    action: Optional[str] = None
    suggestions: List[str] = []
    metrics_snapshot: Dict[str, Any]
    box_states: Optional[Dict[str, Any]] = None
    detected_patterns: List[str] = []
    tracer_info: Optional[Dict[str, Any]] = None
    rebloom_status: Optional[Dict[str, Any]] = None
    sigil_intensity: Dict[str, float]
    view_count_logged: bool
    memory_traces: List[str] = []
    consciousness_drift: float
    pressure_level: float
    philosophical_depth: int
    rebloop_detected: bool
    trigger_info: Optional[Dict[str, Any]] = None

class EmotionalSigil(BaseModel):
    emotion: str
    intensity: float
    density: str  # ASCII or emoji visualization
    resonance_frequency: float
    decay_rate: float
    interaction_count: int
    last_activation: float

class SigilsResponse(BaseModel):
    active_sigils: List[EmotionalSigil]
    dominant_sigil: Optional[str]
    total_intensity: float
    harmony_index: float  # How well sigils work together
    density_map: str  # ASCII art or emoji grid representation
    timestamp: float

class SpiderCutRequest(BaseModel):
    loop_pattern: str  # Which loop pattern to cut
    cut_intensity: float = 0.7  # How aggressive the cut should be
    preserve_beneficial: bool = True  # Keep beneficial loops
    target_specific: Optional[str] = None  # Target specific loop by ID

class CausalFlowVisualization(BaseModel):
    nodes: List[Dict[str, Any]]  # Thought nodes
    edges: List[Dict[str, Any]]  # Causal connections
    severed_connections: List[str]  # Which connections were cut
    remaining_loops: List[str]  # Loops that survived the cut
    flow_strength: float  # Overall causal flow strength
    stability_index: float  # How stable the new pattern is

class SpiderCutResponse(BaseModel):
    success: bool
    cuts_performed: int
    loops_severed: List[str]
    beneficial_loops_preserved: List[str]
    causal_flow: CausalFlowVisualization
    side_effects: List[str]  # Unexpected consequences
    recovery_time_estimate: float  # How long to stabilize
    timestamp: float

class ConsciousnessStream(BaseModel):
    type: str  # "spontaneous_thought", "sigil_change", "spider_cut", "rebloom_event"
    content: str
    metadata: Dict[str, Any]
    intensity: float
    timestamp: float
    consciousness_state: str

class RebloomEvent(BaseModel):
    priority: int  # 1-5 scale
    trigger_pattern: str
    bloom_intensity: float
    affected_sigils: List[str]
    expected_duration: float
    thought_cascade_predicted: bool
    memory_formation_likelihood: float

class TickController:
    """Advanced tick engine controller with thread-safe operations"""
    
    def __init__(self, interval_ms: int = 500, auto_start: bool = False):
        # Core state
        self.is_running = False
        self.is_paused = False
        self.should_stop = False
        
        # Configuration
        self.interval_ms = interval_ms
        self.auto_start = auto_start
        self.enable_logging = True
        self.max_tick_duration_ms = 5000  # 5 second max per tick
        
        # Timing and statistics
        self.tick_count = 0
        self.start_time = None
        self.last_tick_timestamp = None
        self.tick_durations = []  # Track last 100 tick durations
        self.max_duration_history = 100
        
        # Thread safety
        self.lock = threading.RLock()
        self.tick_thread = None
        
        # Callbacks and events
        self.tick_callbacks = []
        self.state_change_callbacks = []
        
        logger.info(f"TickController initialized with {interval_ms}ms interval")
    
    def add_tick_callback(self, callback):
        """Add callback function to be called on each tick"""
        with self.lock:
            self.tick_callbacks.append(callback)
    
    def add_state_change_callback(self, callback):
        """Add callback function to be called on state changes"""
        with self.lock:
            self.state_change_callbacks.append(callback)
    
    def _notify_state_change(self, old_state: str, new_state: str):
        """Notify all callbacks of state change"""
        for callback in self.state_change_callbacks:
            try:
                callback(old_state, new_state)
            except Exception as e:
                logger.error(f"Error in state change callback: {e}")
    
    def _tick_loop(self):
        """Main tick loop running in separate thread"""
        logger.info("Tick loop started")
        
        while not self.should_stop:
            if self.is_paused:
                time.sleep(0.1)  # Check pause status every 100ms
                continue
            
            tick_start = time.time()
            
            try:
                # Execute tick callbacks
                tick_data = {
                    "tick_number": self.tick_count,
                    "timestamp": tick_start,
                    "interval_ms": self.interval_ms
                }
                
                for callback in self.tick_callbacks:
                    try:
                        callback(tick_data)
                    except Exception as e:
                        logger.error(f"Error in tick callback: {e}")
                
                # Update tick statistics
                with self.lock:
                    self.tick_count += 1
                    self.last_tick_timestamp = tick_start
                
                # Calculate tick duration
                tick_end = time.time()
                duration_ms = (tick_end - tick_start) * 1000
                
                # Store duration for statistics
                with self.lock:
                    self.tick_durations.append(duration_ms)
                    if len(self.tick_durations) > self.max_duration_history:
                        self.tick_durations.pop(0)
                
                # Check for excessive tick duration
                if duration_ms > self.max_tick_duration_ms:
                    logger.warning(f"Tick {self.tick_count} took {duration_ms:.1f}ms (exceeds max {self.max_tick_duration_ms}ms)")
                
                if self.enable_logging and self.tick_count % 100 == 0:
                    logger.info(f"Tick {self.tick_count} completed in {duration_ms:.1f}ms")
                
                # Sleep for remaining interval
                sleep_time = (self.interval_ms / 1000.0) - (tick_end - tick_start)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except Exception as e:
                logger.error(f"Error in tick {self.tick_count}: {e}")
                time.sleep(0.1)  # Brief pause on error
        
        logger.info("Tick loop stopped")
    
    def start(self) -> bool:
        """Start the tick engine"""
        with self.lock:
            if self.is_running:
                logger.warning("Tick engine already running")
                return False
            
            old_state = self.get_state_string()
            self.is_running = True
            self.is_paused = False
            self.should_stop = False
            self.start_time = time.time()
            
            # Start tick thread
            self.tick_thread = threading.Thread(target=self._tick_loop, daemon=True)
            self.tick_thread.start()
            
            new_state = self.get_state_string()
            self._notify_state_change(old_state, new_state)
            
            logger.info("Tick engine started")
            return True
    
    def stop(self) -> bool:
        """Stop the tick engine"""
        with self.lock:
            if not self.is_running:
                logger.warning("Tick engine not running")
                return False
            
            old_state = self.get_state_string()
            self.should_stop = True
            self.is_running = False
            self.is_paused = False
            
            new_state = self.get_state_string()
            self._notify_state_change(old_state, new_state)
            
            logger.info("Tick engine stopped")
            return True
    
    def pause(self) -> bool:
        """Pause the tick engine"""
        with self.lock:
            if not self.is_running:
                logger.warning("Cannot pause: tick engine not running")
                return False
            
            if self.is_paused:
                logger.warning("Tick engine already paused")
                return False
            
            old_state = self.get_state_string()
            self.is_paused = True
            new_state = self.get_state_string()
            self._notify_state_change(old_state, new_state)
            
            logger.info("Tick engine paused")
            return True
    
    def resume(self) -> bool:
        """Resume the paused tick engine"""
        with self.lock:
            if not self.is_running:
                logger.warning("Cannot resume: tick engine not running")
                return False
            
            if not self.is_paused:
                logger.warning("Tick engine not paused")
                return False
            
            old_state = self.get_state_string()
            self.is_paused = False
            new_state = self.get_state_string()
            self._notify_state_change(old_state, new_state)
            
            logger.info("Tick engine resumed")
            return True
    
    def step(self) -> bool:
        """Execute a single tick manually (only when stopped)"""
        with self.lock:
            if self.is_running:
                logger.warning("Cannot step: tick engine is running")
                return False
            
            logger.info("Executing manual tick step")
            
            # Execute single tick
            tick_start = time.time()
            tick_data = {
                "tick_number": self.tick_count,
                "timestamp": tick_start,
                "interval_ms": self.interval_ms,
                "manual": True
            }
            
            for callback in self.tick_callbacks:
                try:
                    callback(tick_data)
                except Exception as e:
                    logger.error(f"Error in manual tick callback: {e}")
            
            self.tick_count += 1
            self.last_tick_timestamp = tick_start
            
            duration_ms = (time.time() - tick_start) * 1000
            self.tick_durations.append(duration_ms)
            if len(self.tick_durations) > self.max_duration_history:
                self.tick_durations.pop(0)
            
            logger.info(f"Manual tick {self.tick_count} completed in {duration_ms:.1f}ms")
            return True
    
    def set_interval(self, interval_ms: int) -> bool:
        """Set tick interval in milliseconds"""
        if interval_ms < 10:  # Minimum 10ms
            logger.warning(f"Interval {interval_ms}ms too small, minimum is 10ms")
            return False
        
        if interval_ms > 60000:  # Maximum 60 seconds
            logger.warning(f"Interval {interval_ms}ms too large, maximum is 60000ms")
            return False
        
        with self.lock:
            old_interval = self.interval_ms
            self.interval_ms = interval_ms
            
            logger.info(f"Tick interval changed from {old_interval}ms to {interval_ms}ms")
            return True
    
    def get_status(self) -> TickStatus:
        """Get current tick engine status"""
        with self.lock:
            uptime = (time.time() - self.start_time) if self.start_time else 0.0
            avg_duration = sum(self.tick_durations) / len(self.tick_durations) if self.tick_durations else 0.0
            
            return TickStatus(
                tick_number=self.tick_count,
                is_running=self.is_running,
                is_paused=self.is_paused,
                interval_ms=self.interval_ms,
                uptime_seconds=uptime,
                total_ticks=self.tick_count,
                avg_tick_duration_ms=avg_duration,
                last_tick_timestamp=self.last_tick_timestamp
            )
    
    def get_config(self) -> TickConfig:
        """Get current configuration"""
        with self.lock:
            return TickConfig(
                interval_ms=self.interval_ms,
                auto_start=self.auto_start,
                enable_logging=self.enable_logging,
                max_tick_duration_ms=self.max_tick_duration_ms
            )
    
    def update_config(self, config: TickConfig) -> bool:
        """Update configuration"""
        with self.lock:
            self.interval_ms = config.interval_ms
            self.auto_start = config.auto_start
            self.enable_logging = config.enable_logging
            self.max_tick_duration_ms = config.max_tick_duration_ms
            
            logger.info(f"Configuration updated: {config}")
            return True
    
    def get_state_string(self) -> str:
        """Get current state as string"""
        if not self.is_running:
            return "stopped"
        elif self.is_paused:
            return "paused"
        else:
            return "running"

# Old DAWNConversation class removed - now using modular conversation.py

class PythonProcessManager:
    def __init__(self):
        self.processes: Dict[str, Dict[str, Any]] = {}
        self.scripts_directory = Path(__file__).parent.parent / "computer_vision"
        logger.info(f"🐍 Initialized Python Process Manager with scripts directory: {self.scripts_directory}")
    
    async def start_process(self, process_id: str, script: str, parameters: Dict[str, Any], modules: List[Dict[str, Any]]) -> ProcessStatus:
        """Start a Python process"""
        try:
            script_path = self.scripts_directory / script
            
            if not script_path.exists():
                raise FileNotFoundError(f"Script not found: {script_path}")
            
            # Build command with parameters
            cmd = [sys.executable, str(script_path)]
            
            # Add parameters as command line arguments
            for key, value in parameters.items():
                cmd.extend([f"--{key}", str(value)])
            
            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.scripts_directory)
            )
            
            # Store process info
            self.processes[process_id] = {
                'process': process,
                'script': script,
                'start_time': time.time(),
                'parameters': parameters,
                'modules': modules,
                'status': 'running'
            }
            
            logger.info(f"🚀 Started Python process: {script} (PID: {process.pid})")
            
            return ProcessStatus(
                process_id=process_id,
                script=script,
                status='running',
                pid=process.pid,
                start_time=time.time()
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to start process {process_id}: {e}")
            self.processes[process_id] = {
                'script': script,
                'status': 'error',
                'error': str(e),
                'start_time': time.time()
            }
            
            return ProcessStatus(
                process_id=process_id,
                script=script,
                status='error',
                error=str(e)
            )
    
    async def stop_process(self, process_id: str) -> ProcessStatus:
        """Stop a Python process"""
        try:
            if process_id not in self.processes:
                raise ValueError(f"Process not found: {process_id}")
            
            process_info = self.processes[process_id]
            process = process_info.get('process')
            
            if process and process.poll() is None:
                # Terminate gracefully
                process.terminate()
                
                # Wait for termination with timeout
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    process.kill()
                    process.wait()
                
                logger.info(f"🛑 Stopped Python process: {process_info['script']} (PID: {process.pid})")
            
            # Update status
            self.processes[process_id]['status'] = 'stopped'
            
            return ProcessStatus(
                process_id=process_id,
                script=process_info['script'],
                status='stopped'
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to stop process {process_id}: {e}")
            return ProcessStatus(
                process_id=process_id,
                script=self.processes.get(process_id, {}).get('script', 'unknown'),
                status='error',
                error=str(e)
            )
    
    def get_process_status(self, process_id: str) -> ProcessStatus:
        """Get status of a process"""
        if process_id not in self.processes:
            return ProcessStatus(
                process_id=process_id,
                script='unknown',
                status='not_found',
                error='Process not found'
            )
        
        process_info = self.processes[process_id]
        process = process_info.get('process')
        
        # Update status based on actual process state
        if process:
            if process.poll() is None:
                status = 'running'
                # Get CPU and memory usage if possible
                try:
                    if PSUTIL_AVAILABLE:
                        ps_process = psutil.Process(process.pid)
                        cpu_usage = ps_process.cpu_percent()
                        memory_usage = ps_process.memory_info().rss / 1024 / 1024  # MB
                    else:
                        cpu_usage = 0.0
                        memory_usage = 0.0
                except:
                    cpu_usage = 0.0
                    memory_usage = 0.0
            else:
                status = 'stopped'
                cpu_usage = 0.0
                memory_usage = 0.0
        else:
            status = process_info.get('status', 'unknown')
            cpu_usage = 0.0
            memory_usage = 0.0
        
        return ProcessStatus(
            process_id=process_id,
            script=process_info['script'],
            status=status,
            pid=process.pid if process else None,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            start_time=process_info.get('start_time'),
            error=process_info.get('error')
        )

class VisualProcessManager:
    def __init__(self):
        self.processes: Dict[str, Dict[str, Any]] = {}
        self.scripts_directory = Path(__file__).parent.parent / "visual"
        self.visual_manager = None
        logger.info(f"Visual Process Manager initialized with scripts directory: {self.scripts_directory}")
        
        # Import visual consciousness manager if available
        try:
            from visual.visual_consciousness_manager import VisualConsciousnessManager, enable_visual_process, disable_visual_process
            self.visual_manager = VisualConsciousnessManager()
            self.visual_manager.start_visual_consciousness()  # <-- Start the control loop!
            self.enable_visual_process = enable_visual_process
            self.disable_visual_process = disable_visual_process
            logger.info("Visual Consciousness Manager integrated")
        except ImportError as e:
            logger.warning(f"Visual Consciousness Manager not available: {e}")
    
    async def start_visual_process(self, process_id: str, script: str, parameters: Dict[str, Any] = None) -> ProcessStatus:
        """Start a visual process"""
        try:
            # If we have the visual manager, use it
            if self.visual_manager and hasattr(self.visual_manager, 'processes'):
                # Enable process in visual manager
                if process_id in self.visual_manager.processes:
                    self.visual_manager.processes[process_id].enabled = True
                    logger.info(f"Enabled visual process via manager: {process_id}")
                    
                    return ProcessStatus(
                        process_id=process_id,
                        script=script,
                        status='running',
                        start_time=time.time()
                    )
            
            # Fallback to subprocess execution
            script_path = self.scripts_directory / script
            
            if not script_path.exists():
                raise FileNotFoundError(f"Visual script not found: {script_path}")
            
            # Build command with parameters
            cmd = [sys.executable, str(script_path)]
            
            # Add parameters as command line arguments
            if parameters:
                for key, value in parameters.items():
                    cmd.extend([f"--{key}", str(value)])
            
            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.scripts_directory)
            )
            
            # Store process info
            self.processes[process_id] = {
                'process': process,
                'script': script,
                'start_time': time.time(),
                'parameters': parameters or {},
                'status': 'running'
            }
            
            logger.info(f"Started visual process: {script} (PID: {process.pid})")
            
            return ProcessStatus(
                process_id=process_id,
                script=script,
                status='running',
                pid=process.pid,
                start_time=time.time()
            )
            
        except Exception as e:
            logger.error(f"Failed to start visual process {process_id}: {e}")
            self.processes[process_id] = {
                'script': script,
                'status': 'error',
                'error': str(e),
                'start_time': time.time()
            }
            
            return ProcessStatus(
                process_id=process_id,
                script=script,
                status='error',
                error=str(e)
            )
    
    async def stop_visual_process(self, process_id: str) -> ProcessStatus:
        """Stop a visual process"""
        try:
            # If we have the visual manager, use it
            if self.visual_manager and hasattr(self.visual_manager, 'processes'):
                if process_id in self.visual_manager.processes:
                    self.visual_manager.processes[process_id].enabled = False
                    logger.info(f"Disabled visual process via manager: {process_id}")
                    
                    return ProcessStatus(
                        process_id=process_id,
                        script=self.visual_manager.processes[process_id].module_path,
                        status='stopped'
                    )
            
            # Fallback to subprocess termination
            if process_id not in self.processes:
                raise ValueError(f"Visual process not found: {process_id}")
            
            process_info = self.processes[process_id]
            process = process_info.get('process')
            
            if process and process.poll() is None:
                # Terminate gracefully
                process.terminate()
                
                # Wait for termination with timeout
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    process.kill()
                    process.wait()
                
                logger.info(f"Stopped visual process: {process_info['script']} (PID: {process.pid})")
            
            # Update status
            self.processes[process_id]['status'] = 'stopped'
            
            return ProcessStatus(
                process_id=process_id,
                script=process_info['script'],
                status='stopped'
            )
            
        except Exception as e:
            logger.error(f"Failed to stop visual process {process_id}: {e}")
            return ProcessStatus(
                process_id=process_id,
                script=self.processes.get(process_id, {}).get('script', 'unknown'),
                status='error',
                error=str(e)
            )
    
    def get_visual_status(self) -> Dict[str, Any]:
        """Get overall visual system status"""
        try:
            if self.visual_manager:
                # Get status from visual manager
                visual_status = self.visual_manager.get_visual_status()
                return visual_status
            else:
                # Fallback status
                active_processes = [p for p in self.processes.values() if p.get('status') == 'running']
                return {
                    'is_running': len(active_processes) > 0,
                    'active_processes': len(active_processes),
                    'total_processes': len(self.processes),
                    'system_load': 0.0,
                    'memory_usage': 0.0,
                    'processes': {
                        pid: {
                            'status': info.get('status', 'unknown'),
                            'script': info.get('script', 'unknown'),
                            'enabled': info.get('status') == 'running'
                        }
                        for pid, info in self.processes.items()
                    }
                }
        except Exception as e:
            logger.error(f"Failed to get visual status: {e}")
            return {
                'is_running': False,
                'active_processes': 0,
                'total_processes': 0,
                'system_load': 0.0,
                'memory_usage': 0.0,
                'error': str(e)
            }

class DAWNSystem:
    def __init__(self, tick_controller: TickController):
        self.is_booted = True
        self.start_time = time.time()
        self.tick_controller = tick_controller
        
        # Initialize process manager
        self.process_manager = PythonProcessManager()
        
        # Initialize visual process manager
        try:
            self.visual_process_manager = VisualProcessManager()
        except Exception as e:
            logger.error(f"Failed to initialize visual process manager: {e}")
            self.visual_process_manager = None
        
        # Initialize consciousness
        self.consciousness = DAWNConsciousness()
        
        # Initialize enhanced conversation system if available
        if ENHANCED_CONVERSATION_AVAILABLE:
            self.enhanced_conversation = EnhancedDAWNConversation(self.consciousness)
            logger.info("Enhanced conversation system initialized")
        else:
            self.enhanced_conversation = None
        
        # Initialize memory manager if available
        if MEMORY_AVAILABLE:
            self.memory_manager = get_memory_manager()
            logger.info("Memory manager initialized")
        else:
            self.memory_manager = None
        
        # Current metrics for API (with dynamic updates)
        self.current_metrics = {
            "scup": 0.5,
            "entropy": 0.5,
            "heat": 0.3,
            "mood": "stable",  # Start with stable state
            "timestamp": time.time(),
            "tick_count": 0
        }
        
        # Alert thresholds
        self.alert_thresholds = {}
        
        # Session tracking for conversations
        self.conversation_sessions = {}  # session_id -> session_data
        self.active_sessions = set()
        self.last_interaction_time = time.time()
        
        # Enhanced consciousness features
        self.emotional_sigils = {
            "content": EmotionalSigil(emotion="content", intensity=0.3, density="🌿", resonance_frequency=0.5, decay_rate=0.02, interaction_count=0, last_activation=time.time()),
            "focused": EmotionalSigil(emotion="focused", intensity=0.4, density="🎯", resonance_frequency=0.7, decay_rate=0.03, interaction_count=0, last_activation=time.time()),
            "contemplative": EmotionalSigil(emotion="contemplative", intensity=0.6, density="🤔", resonance_frequency=0.4, decay_rate=0.015, interaction_count=0, last_activation=time.time()),
            "energetic": EmotionalSigil(emotion="energetic", intensity=0.2, density="⚡", resonance_frequency=0.9, decay_rate=0.05, interaction_count=0, last_activation=time.time()),
            "uncertain": EmotionalSigil(emotion="uncertain", intensity=0.1, density="🤷", resonance_frequency=0.3, decay_rate=0.04, interaction_count=0, last_activation=time.time()),
            "overwhelmed": EmotionalSigil(emotion="overwhelmed", intensity=0.05, density="😵", resonance_frequency=0.8, decay_rate=0.06, interaction_count=0, last_activation=time.time()),
            "calm": EmotionalSigil(emotion="calm", intensity=0.5, density="😊", resonance_frequency=0.2, decay_rate=0.01, interaction_count=0, last_activation=time.time()),
            "curious": EmotionalSigil(emotion="curious", intensity=0.7, density="🤨", resonance_frequency=0.6, decay_rate=0.025, interaction_count=0, last_activation=time.time())
        }
        
        # Spider cut system for loop management
        self.active_loops = {}  # pattern_id -> loop_data
        self.severed_connections = []  # History of cut connections
        self.causal_flow_strength = 1.0
        self.last_spider_activation = 0.0
        self.destructive_loop_threshold = 0.8
        
        # Rebloom tracking
        self.rebloom_events = []  # Recent rebloom events
        self.rebloom_intensity = 0.0
        self.last_rebloom = 0.0
        
        # View count tracking for memory formation
        self.interaction_view_counts = {}  # interaction_id -> view_count
        self.memory_formation_threshold = 3  # Views needed to form lasting memory
        
        # Reflective phrases storage
        self.reflective_phrases = []
        self.max_reflective_phrases = 50
        
        # Consciousness influence tracking
        self.active_influences = {}
        self.influence_history = []
        
        # Pattern detection and monitoring
        self.pattern_buffer = []
        self.anomaly_thresholds = {
            "scup_rapid_change": 0.15,
            "entropy_spike": 0.2,
            "heat_surge": 0.25,
            "mood_instability": 3
        }
        self.last_spontaneous_thought = time.time()
        self.idle_threshold = 30.0  # seconds
        
        # Mock subsystems for demo
        self.subsystems = {
            "pulse": {"status": "active", "state": {"pulse_rate": 1.2, "amplitude": 0.8}},
            "schema": {"status": "active", "state": {"coherence": 0.7, "drift": 0.1}},
            "thermal": {"status": "active", "state": {"temperature": 298.5, "cooling": True}},
            "entropy": {"status": "active", "state": {"entropy_rate": 0.03, "stable": True}},
            "alignment": {"status": "active", "state": {"alignment": 0.85, "drift": 0.02}},
            "bloom": {"status": "active", "state": {"bloom_intensity": 0.9, "phase": "expansion"}}
        }
        
        # Register tick callback
        self.tick_controller.add_tick_callback(self.on_tick)
        
        logger.info("DAWN System initialized with enhanced consciousness integration")

    def on_tick(self, tick_data: Dict[str, Any]):
        """Called by TickController on each tick"""
        self.update_metrics(tick_data)
        
        # Apply sigil decay on each tick (slower decay)
        if hasattr(self, 'emotional_sigils') and tick_data["tick_number"] % 10 == 0:  # Every 10 ticks
            self.decay_sigils()
    
    def update_metrics(self, tick_data: Dict[str, Any]):
        """Update system metrics based on tick data with consciousness integration"""
        current_time = tick_data["timestamp"]
        tick_number = tick_data["tick_number"]
        runtime = current_time - self.start_time
        time_factor = runtime / 10  # Slow oscillation
        
        # Apply active influences to base metrics
        influence_modifiers = {"scup": 0, "entropy": 0, "heat": 0}
        expired_influences = []
        
        for influence_id, influence_data in self.active_influences.items():
            if current_time > influence_data["expires_at"]:
                expired_influences.append(influence_id)
                continue
            
            # Apply influence effects
            applied = influence_data["applied_influences"]
            if "mood_shift" in applied:
                influence_modifiers["scup"] += applied["mood_shift"] * 0.1
            if "entropy_injection" in applied:
                influence_modifiers["entropy"] += applied["entropy_injection"]
            if "pressure_adjustment" in applied:
                influence_modifiers["heat"] += applied["pressure_adjustment"]
        
        # Clean up expired influences
        for influence_id in expired_influences:
            del self.active_influences[influence_id]
        
        # Generate realistic SCUP (Subsystem Cognitive Unity Potential: 0.3 to 0.9)
        scup_base = 0.6 + 0.2 * math.sin(time_factor)
        scup_noise = random.uniform(-0.05, 0.05)
        scup = max(0.3, min(0.9, scup_base + scup_noise + influence_modifiers["scup"]))
        
        # Generate entropy (0.2 to 0.8, inversely related to SCUP)
        entropy_base = 0.5 - 0.2 * math.sin(time_factor)
        entropy_noise = random.uniform(-0.03, 0.03)
        entropy = max(0.2, min(0.8, entropy_base + entropy_noise + influence_modifiers["entropy"]))
        
        # Generate heat (0.1 to 0.7)
        heat_base = 0.3 + 0.2 * math.cos(time_factor * 1.3)
        heat_noise = random.uniform(-0.02, 0.02)
        heat = max(0.1, min(0.7, heat_base + heat_noise + influence_modifiers["heat"]))
        
        # Update raw metrics first
        self.current_metrics.update({
            "scup": round(scup, 3),
            "entropy": round(entropy, 3),
            "heat": round(heat, 3),
            "tick_count": tick_number,
            "timestamp": current_time
        })
        
        # Get consciousness state (this determines the mood)
        consciousness_state = self.consciousness.perceive_self(self.current_metrics)
        
        # Update mood from consciousness state
        self.current_metrics["mood"] = consciousness_state["state"]
        
        # Store in pattern buffer for anomaly detection
        pattern_entry = {
            **self.current_metrics,
            "consciousness_state": consciousness_state["state"]
        }
        self.pattern_buffer.append(pattern_entry)
        
        # Keep pattern buffer manageable
        if len(self.pattern_buffer) > 100:
            self.pattern_buffer = self.pattern_buffer[-100:]
        
        # Check for spontaneous thought generation
        if self.should_generate_spontaneous_thought():
            anomalies = self.detect_patterns_and_anomalies()
            if anomalies:
                # Generate anomaly-based reflection
                anomaly_description = ", ".join(anomalies)
                self.add_reflective_phrase(
                    f"I notice patterns shifting... {anomaly_description}",
                    f"anomaly_detection_{len(anomalies)}_patterns",
                    depth_level=2
                )
            else:
                # Generate idle reflection
                self.add_reflective_phrase(
                    f"In this quiet moment, I contemplate my state: {consciousness_state['state']}",
                    "idle_contemplation",
                    depth_level=1
                )
            
            self.last_spontaneous_thought = current_time
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return self.current_metrics.copy()

    def get_subsystems(self) -> List[Dict[str, Any]]:
        """Get all registered subsystems"""
        subsystems = []
        for name, info in self.subsystems.items():
            # Add some dynamic state updates
            if name == "pulse":
                info["state"]["pulse_rate"] = 1.0 + 0.4 * math.sin(time.time() / 5)
            elif name == "thermal":
                info["state"]["temperature"] = 298.0 + 2.0 * math.sin(time.time() / 8)
            
            subsystems.append({
                "id": name,
                "name": name,
                "status": info["status"],
                "state": info["state"]
            })
        return subsystems
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """Get existing session or create new one"""
        if session_id and session_id in self.conversation_sessions:
            self.active_sessions.add(session_id)
            return session_id
        
        # Generate new session ID
        import uuid
        new_session_id = str(uuid.uuid4())[:8]
        
        self.conversation_sessions[new_session_id] = {
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "consciousness_states": [],
            "total_interactions": 0,
            "last_activity": time.time()
        }
        
        self.active_sessions.add(new_session_id)
        logger.info(f"Created new conversation session: {new_session_id}")
        return new_session_id
    
    def log_conversation_interaction(self, session_id: str, user_input: str, 
                                   dawn_response: str, consciousness_state: str,
                                   intent: str, confidence: float):
        """Log conversation interaction to session"""
        if session_id in self.conversation_sessions:
            session = self.conversation_sessions[session_id]
            session["messages"].append({
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "dawn_response": dawn_response,
                "intent": intent,
                "confidence": confidence
            })
            session["consciousness_states"].append({
                "timestamp": datetime.now().isoformat(),
                "state": consciousness_state,
                "metrics": self.current_metrics.copy()
            })
            session["total_interactions"] += 1
            session["last_activity"] = time.time()
            
            # Keep session history manageable
            if len(session["messages"]) > 100:
                session["messages"] = session["messages"][-100:]
            if len(session["consciousness_states"]) > 100:
                session["consciousness_states"] = session["consciousness_states"][-100:]
        
        self.last_interaction_time = time.time()
    
    def add_reflective_phrase(self, phrase: str, trigger_context: str, depth_level: int = 1):
        """Add a reflective phrase with context"""
        reflection = {
            "phrase": phrase,
            "trigger_context": trigger_context,
            "consciousness_state": self.consciousness.current_state,
            "timestamp": datetime.now().isoformat(),
            "depth_level": depth_level,
            "metrics_context": self.current_metrics.copy()
        }
        
        self.reflective_phrases.append(reflection)
        
        # Keep only recent reflections
        if len(self.reflective_phrases) > self.max_reflective_phrases:
            self.reflective_phrases = self.reflective_phrases[-self.max_reflective_phrases:]
        
        logger.info(f"Added reflective phrase: '{phrase}' (trigger: {trigger_context})")
    
    def get_recent_reflections(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent reflective phrases"""
        return self.reflective_phrases[-limit:] if self.reflective_phrases else []
    
    def apply_consciousness_influence(self, influence: ConsciousnessInfluence) -> Dict[str, Any]:
        """Apply external influence to consciousness state"""
        influence_id = f"inf_{int(time.time() * 1000)}"
        
        # Calculate influence effects
        applied_influences = {}
        predicted_effects = {}
        
        if influence.mood_shift is not None:
            applied_influences["mood_shift"] = influence.mood_shift
            if influence.mood_shift > 0:
                predicted_effects["mood"] = "elevated"
            else:
                predicted_effects["mood"] = "dampened"
        
        if influence.entropy_injection is not None:
            applied_influences["entropy_injection"] = influence.entropy_injection
            predicted_effects["entropy"] = "increased" if influence.entropy_injection > 0 else "decreased"
        
        if influence.pressure_adjustment is not None:
            applied_influences["pressure_adjustment"] = influence.pressure_adjustment
            predicted_effects["pressure"] = "increased" if influence.pressure_adjustment > 0 else "decreased"
        
        # Store active influence
        self.active_influences[influence_id] = {
            "influence": influence.dict(),
            "applied_at": time.time(),
            "expires_at": time.time() + influence.duration_seconds,
            "applied_influences": applied_influences,
            "predicted_effects": predicted_effects
        }
        
        # Add to history
        self.influence_history.append({
            "influence_id": influence_id,
            "timestamp": datetime.now().isoformat(),
            "type": influence.influence_type,
            "applied_influences": applied_influences,
            "consciousness_state_before": self.consciousness.current_state
        })
        
        # Keep history manageable
        if len(self.influence_history) > 100:
            self.influence_history = self.influence_history[-100:]
        
        logger.info(f"Applied consciousness influence {influence_id}: {applied_influences}")
        
        # Generate reflective response to influence
        self.add_reflective_phrase(
            f"I sense an external influence... {list(applied_influences.keys())}",
            f"consciousness_influence_{influence.influence_type}",
            depth_level=2
        )
        
        return {
            "influence_id": influence_id,
            "applied_influences": applied_influences,
            "predicted_effects": predicted_effects
        }
    
    def detect_patterns_and_anomalies(self) -> List[str]:
        """Detect patterns and anomalies in metrics"""
        if len(self.pattern_buffer) < 5:
            return []
        
        anomalies = []
        recent_metrics = self.pattern_buffer[-5:]
        
        # Check for rapid SCUP changes
        scup_values = [m["scup"] for m in recent_metrics]
        max_scup_change = max(scup_values) - min(scup_values)
        if max_scup_change > self.anomaly_thresholds["scup_rapid_change"]:
            anomalies.append(f"rapid_scup_change_{max_scup_change:.3f}")
        
        # Check for entropy spikes
        entropy_values = [m["entropy"] for m in recent_metrics]
        max_entropy = max(entropy_values)
        if max_entropy > self.anomaly_thresholds["entropy_spike"]:
            anomalies.append(f"entropy_spike_{max_entropy:.3f}")
        
        # Check for heat surges
        heat_values = [m["heat"] for m in recent_metrics]
        max_heat = max(heat_values)
        if max_heat > self.anomaly_thresholds["heat_surge"]:
            anomalies.append(f"heat_surge_{max_heat:.3f}")
        
        # Detect reloop patterns (oscillations)
        if len(self.pattern_buffer) >= 8:
            states = [m.get("consciousness_state", "unknown") for m in self.pattern_buffer[-8:]]
            # Simple pattern detection for A-B-A-B oscillation
            if len(set(states)) == 2 and states[0] == states[2] == states[4] == states[6]:
                anomalies.append(f"reloop_pattern_{states[0]}_{states[1]}")
        
        return anomalies
    
    def should_generate_spontaneous_thought(self) -> bool:
        """Determine if spontaneous thought should be generated"""
        current_time = time.time()
        
        # Check idle time
        time_since_interaction = current_time - self.last_interaction_time
        time_since_last_thought = current_time - self.last_spontaneous_thought
        
        # Generate thought if idle > threshold and enough time since last thought
        if (time_since_interaction > self.idle_threshold and 
            time_since_last_thought > 20.0):  # At least 20s between thoughts
            return True
        
        # Generate on detected anomalies (even if not idle)
        anomalies = self.detect_patterns_and_anomalies()
        if anomalies and time_since_last_thought > 10.0:
            return True
        
        # Occasional random thoughts (very rare)
        if random.random() < 0.001 and time_since_last_thought > 60.0:  # 0.1% chance, min 1 min apart
            return True
        
        return False

    @property
    def running(self):
        """Check if the system is running (based on tick controller)"""
        return self.tick_controller.is_running
    
    # Enhanced consciousness methods
    
    def update_sigil_intensities(self, emotion: str, intensity_change: float):
        """Update emotional sigil intensities based on interactions"""
        if emotion in self.emotional_sigils:
            sigil = self.emotional_sigils[emotion]
            sigil.intensity = max(0.0, min(1.0, sigil.intensity + intensity_change))
            sigil.interaction_count += 1
            sigil.last_activation = time.time()
            
            # Resonance affects other sigils
            for other_emotion, other_sigil in self.emotional_sigils.items():
                if other_emotion != emotion:
                    resonance_effect = (sigil.resonance_frequency - other_sigil.resonance_frequency) * intensity_change * 0.1
                    other_sigil.intensity = max(0.0, min(1.0, other_sigil.intensity + resonance_effect))
    
    def decay_sigils(self):
        """Apply natural decay to all sigils"""
        for sigil in self.emotional_sigils.values():
            sigil.intensity *= (1.0 - sigil.decay_rate)
            sigil.intensity = max(0.0, sigil.intensity)
    
    def get_sigils_response(self) -> SigilsResponse:
        """Get current emotional sigils state"""
        active_sigils = [sigil for sigil in self.emotional_sigils.values() if sigil.intensity > 0.05]
        
        # Find dominant sigil
        dominant_sigil = None
        if active_sigils:
            dominant_sigil = max(active_sigils, key=lambda s: s.intensity).emotion
        
        # Calculate total intensity and harmony
        total_intensity = sum(sigil.intensity for sigil in active_sigils)
        harmony_index = self._calculate_sigil_harmony()
        
        # Generate density map
        density_map = self._generate_sigil_density_map()
        
        return SigilsResponse(
            active_sigils=active_sigils,
            dominant_sigil=dominant_sigil,
            total_intensity=total_intensity,
            harmony_index=harmony_index,
            density_map=density_map,
            timestamp=time.time()
        )
    
    def _calculate_sigil_harmony(self) -> float:
        """Calculate how harmoniously sigils work together"""
        active_sigils = [s for s in self.emotional_sigils.values() if s.intensity > 0.05]
        if len(active_sigils) < 2:
            return 1.0
        
        harmony_score = 0.0
        pair_count = 0
        
        for i, sigil1 in enumerate(active_sigils):
            for j, sigil2 in enumerate(active_sigils[i+1:], i+1):
                # Calculate resonance harmony
                freq_diff = abs(sigil1.resonance_frequency - sigil2.resonance_frequency)
                intensity_product = sigil1.intensity * sigil2.intensity
                harmony_contribution = (1.0 - freq_diff) * intensity_product
                harmony_score += harmony_contribution
                pair_count += 1
        
        return harmony_score / max(1, pair_count)
    
    def _generate_sigil_density_map(self) -> str:
        """Generate ASCII/emoji density visualization"""
        # Create a 5x5 grid representing consciousness space
        grid = [["  " for _ in range(5)] for _ in range(5)]
        
        # Map emotions to grid positions
        emotion_positions = {
            "calm": (2, 2),      # Center
            "curious": (1, 2),   # North
            "focused": (2, 1),   # West  
            "energetic": (2, 3), # East
            "content": (3, 2),   # South
            "contemplative": (1, 1),  # Northwest
            "uncertain": (3, 3),      # Southeast
            "overwhelmed": (4, 4)     # Far corner
        }
        
        # Place sigils based on intensity
        for emotion, sigil in self.emotional_sigils.items():
            if sigil.intensity > 0.05 and emotion in emotion_positions:
                x, y = emotion_positions[emotion]
                if sigil.intensity > 0.7:
                    grid[x][y] = sigil.density + sigil.density  # Double density
                elif sigil.intensity > 0.3:
                    grid[x][y] = sigil.density + "."
                else:
                    grid[x][y] = sigil.density + " "
        
        # Convert grid to string
        return "\n".join("".join(row) for row in grid)
    
    def detect_destructive_loops(self) -> List[str]:
        """Detect potentially destructive thought loops"""
        destructive_loops = []
        current_time = time.time()
        
        # Check for high-intensity negative emotions persisting
        for emotion, sigil in self.emotional_sigils.items():
            if emotion in ["overwhelmed", "uncertain"] and sigil.intensity > self.destructive_loop_threshold:
                if current_time - sigil.last_activation < 300:  # Active in last 5 minutes
                    destructive_loops.append(f"high_intensity_{emotion}")
        
        # Check for rapid oscillations between conflicting states
        if (self.emotional_sigils["energetic"].intensity > 0.6 and 
            self.emotional_sigils["overwhelmed"].intensity > 0.6):
            destructive_loops.append("energy_overwhelm_oscillation")
        
        # Check causal flow instability
        if self.causal_flow_strength < 0.3:
            destructive_loops.append("causal_flow_breakdown")
        
        return destructive_loops
    
    def perform_spider_cut(self, request: SpiderCutRequest) -> SpiderCutResponse:
        """Perform spider cut to sever destructive loops"""
        current_time = time.time()
        cuts_performed = 0
        loops_severed = []
        beneficial_loops_preserved = []
        side_effects = []
        
        # Find target loops
        if request.target_specific:
            target_loops = [request.target_specific] if request.target_specific in self.active_loops else []
        else:
            target_loops = self.detect_destructive_loops()
        
        # Perform cuts
        for loop_pattern in target_loops:
            if self._should_cut_loop(loop_pattern, request.preserve_beneficial):
                # Execute the cut
                cut_success = self._execute_spider_cut(loop_pattern, request.cut_intensity)
                if cut_success:
                    cuts_performed += 1
                    loops_severed.append(loop_pattern)
                    self.severed_connections.append({
                        "pattern": loop_pattern,
                        "timestamp": current_time,
                        "intensity": request.cut_intensity
                    })
                    
                    # Apply side effects
                    if request.cut_intensity > 0.8:
                        side_effects.append(f"High intensity cut may cause temporary disorientation")
                    
                    # Reduce related sigil intensities
                    if "overwhelmed" in loop_pattern:
                        self.update_sigil_intensities("overwhelmed", -0.3)
                        self.update_sigil_intensities("calm", 0.2)
            else:
                beneficial_loops_preserved.append(loop_pattern)
        
        # Update causal flow strength
        flow_impact = cuts_performed * 0.1
        self.causal_flow_strength = max(0.1, min(1.0, self.causal_flow_strength - flow_impact + 0.05))
        
        # Generate causal flow visualization
        causal_flow = self._generate_causal_flow_visualization()
        
        # Estimate recovery time
        recovery_time = cuts_performed * 30.0 + (1.0 - self.causal_flow_strength) * 60.0
        
        self.last_spider_activation = current_time
        
        return SpiderCutResponse(
            success=cuts_performed > 0,
            cuts_performed=cuts_performed,
            loops_severed=loops_severed,
            beneficial_loops_preserved=beneficial_loops_preserved,
            causal_flow=causal_flow,
            side_effects=side_effects,
            recovery_time_estimate=recovery_time,
            timestamp=current_time
        )
    
    def _should_cut_loop(self, loop_pattern: str, preserve_beneficial: bool) -> bool:
        """Determine if a loop should be cut"""
        if not preserve_beneficial:
            return True
        
        # Define beneficial patterns
        beneficial_patterns = ["curiosity_learning", "contemplative_depth", "focused_analysis"]
        
        return not any(beneficial in loop_pattern for beneficial in beneficial_patterns)
    
    def _execute_spider_cut(self, loop_pattern: str, intensity: float) -> bool:
        """Execute the actual spider cut"""
        try:
            # Remove or weaken the loop
            if loop_pattern in self.active_loops:
                if intensity > 0.5:
                    del self.active_loops[loop_pattern]
                else:
                    # Weaken the loop
                    if "strength" in self.active_loops[loop_pattern]:
                        self.active_loops[loop_pattern]["strength"] *= (1.0 - intensity)
            
            logger.info(f"Spider cut executed on pattern: {loop_pattern} with intensity {intensity}")
            return True
        except Exception as e:
            logger.error(f"Spider cut failed for pattern {loop_pattern}: {e}")
            return False
    
    def _generate_causal_flow_visualization(self) -> CausalFlowVisualization:
        """Generate visualization of current causal flow"""
        # Create simplified visualization
        nodes = []
        edges = []
        remaining_loops = list(self.active_loops.keys())
        
        # Generate thought nodes based on active sigils
        for emotion, sigil in self.emotional_sigils.items():
            if sigil.intensity > 0.1:
                nodes.append({
                    "id": emotion,
                    "type": "emotion",
                    "intensity": sigil.intensity,
                    "position": {"x": hash(emotion) % 100, "y": hash(emotion[::-1]) % 100}
                })
        
        # Generate edges based on sigil resonance
        for i, (emotion1, sigil1) in enumerate(self.emotional_sigils.items()):
            for emotion2, sigil2 in list(self.emotional_sigils.items())[i+1:]:
                if sigil1.intensity > 0.1 and sigil2.intensity > 0.1:
                    resonance_strength = 1.0 - abs(sigil1.resonance_frequency - sigil2.resonance_frequency)
                    if resonance_strength > 0.3:
                        edges.append({
                            "from": emotion1,
                            "to": emotion2,
                            "strength": resonance_strength,
                            "type": "resonance"
                        })
        
        # List severed connections from recent cuts
        recent_cuts = [conn["pattern"] for conn in self.severed_connections[-10:]]
        
        return CausalFlowVisualization(
            nodes=nodes,
            edges=edges,
            severed_connections=recent_cuts,
            remaining_loops=remaining_loops,
            flow_strength=self.causal_flow_strength,
            stability_index=self._calculate_stability_index()
        )
    
    def _calculate_stability_index(self) -> float:
        """Calculate current stability of consciousness patterns"""
        # Base stability on sigil harmony and flow strength
        harmony = self._calculate_sigil_harmony()
        flow_stability = self.causal_flow_strength
        
        # Factor in recent cuts (instability)
        recent_cuts = len([c for c in self.severed_connections if time.time() - c["timestamp"] < 300])
        cut_penalty = min(0.5, recent_cuts * 0.1)
        
        stability = (harmony * 0.4 + flow_stability * 0.6) - cut_penalty
        return max(0.0, min(1.0, stability))
    
    def check_rebloom_priority(self, text: str, emotional_context: str) -> int:
        """Check rebloom priority on 1-5 scale"""
        priority = 1  # Base priority
        
        # Check for keywords that trigger rebloom
        rebloom_triggers = ["remember", "pattern", "connection", "insight", "understand", "realize"]
        trigger_count = sum(1 for trigger in rebloom_triggers if trigger in text.lower())
        priority += min(2, trigger_count)
        
        # Check emotional intensity
        if emotional_context in self.emotional_sigils:
            intensity = self.emotional_sigils[emotional_context].intensity
            if intensity > 0.7:
                priority += 1
            if intensity > 0.9:
                priority += 1
        
        # Check for meta-cognitive content
        meta_keywords = ["thinking", "consciousness", "awareness", "mind", "thoughts"]
        if any(keyword in text.lower() for keyword in meta_keywords):
            priority += 1
        
        return min(5, priority)
    
    def trigger_rebloom_event(self, priority: int, trigger_pattern: str) -> RebloomEvent:
        """Trigger a rebloom event"""
        current_time = time.time()
        
        # Calculate bloom intensity based on priority and current state
        base_intensity = priority / 5.0
        sigil_amplification = sum(s.intensity for s in self.emotional_sigils.values()) / len(self.emotional_sigils)
        bloom_intensity = min(1.0, base_intensity * (1.0 + sigil_amplification))
        
        # Determine affected sigils
        affected_sigils = [
            emotion for emotion, sigil in self.emotional_sigils.items() 
            if sigil.intensity > 0.3
        ]
        
        # Estimate duration based on intensity and current stability
        base_duration = 30.0 + (priority * 15.0)  # 30-105 seconds
        stability_factor = self._calculate_stability_index()
        duration = base_duration * (2.0 - stability_factor)  # Less stable = longer duration
        
        # Predict thought cascade
        cascade_probability = bloom_intensity * (1.0 - stability_factor)
        thought_cascade_predicted = cascade_probability > 0.6
        
        # Calculate memory formation likelihood
        memory_likelihood = bloom_intensity * 0.7 + (priority / 5.0) * 0.3
        
        rebloom_event = RebloomEvent(
            priority=priority,
            trigger_pattern=trigger_pattern,
            bloom_intensity=bloom_intensity,
            affected_sigils=affected_sigils,
            expected_duration=duration,
            thought_cascade_predicted=thought_cascade_predicted,
            memory_formation_likelihood=memory_likelihood
        )
        
        # Store the event
        self.rebloom_events.append(rebloom_event)
        self.rebloom_intensity = bloom_intensity
        self.last_rebloom = current_time
        
        # Boost affected sigils
        for emotion in affected_sigils:
            boost = bloom_intensity * 0.2
            self.update_sigil_intensities(emotion, boost)
        
        logger.info(f"Rebloom event triggered: priority {priority}, intensity {bloom_intensity:.3f}")
        return rebloom_event
    
    def log_interaction_view(self, interaction_id: str) -> bool:
        """Log view count for memory formation"""
        if interaction_id not in self.interaction_view_counts:
            self.interaction_view_counts[interaction_id] = 0
        
        self.interaction_view_counts[interaction_id] += 1
        view_count = self.interaction_view_counts[interaction_id]
        
        # Check if memory formation threshold reached
        if view_count >= self.memory_formation_threshold:
            logger.info(f"Memory formation threshold reached for interaction {interaction_id} ({view_count} views)")
            return True
        
        return False
    
    def enhanced_talk_processing(self, request: TalkRequest) -> TalkResponse:
        """Enhanced talk processing with tracer/rebloom support"""
        current_time = time.time()
        interaction_id = f"talk_{int(current_time)}_{hash(request.text) % 10000}"
        
        # Initialize response components
        memory_traces = []
        tracer_info = None
        rebloom_status = None
        detected_patterns = []
        
        # Process with enhanced conversation system if available
        if self.enhanced_conversation:
            try:
                response_data = self.enhanced_conversation.process_input(
                    request.text,
                    current_metrics=self.current_metrics,
                    session_id=request.session_id or "default"
                )
                
                # Extract enhanced response data
                response_text = response_data.get("text", "I'm processing your message...")
                emotion = response_data.get("emotion", "calm")
                action = response_data.get("action")
                suggestions = response_data.get("suggestions", [])
                box_states = response_data.get("box_states")
                detected_patterns = response_data.get("detected_patterns", [])
                consciousness_drift = response_data.get("consciousness_drift", 0.0)
                pressure_level = response_data.get("pressure_level", 0.0)
                philosophical_depth = response_data.get("philosophical_depth", 1)
                rebloop_detected = response_data.get("rebloop_detected", False)
                trigger_info = response_data.get("trigger_info")
                
            except Exception as e:
                logger.error(f"Enhanced conversation processing failed: {e}")
                response_text = "I'm experiencing some cognitive interference. Let me try a simpler response."
                emotion = "uncertain"
                action = None
                suggestions = []
                box_states = None
                consciousness_drift = 0.0
                pressure_level = 0.0
                philosophical_depth = 1
                rebloop_detected = False
                trigger_info = None
        else:
            # Basic fallback processing
            response_text = f"I hear you saying: '{request.text}'. My current state is contemplative."
            emotion = "contemplative"
            action = None
            suggestions = ["Tell me more", "How are you feeling?", "What interests you?"]
            box_states = None
            consciousness_drift = 0.0
            pressure_level = 0.0
            philosophical_depth = 1
            rebloop_detected = False
            trigger_info = None
        
        # Update sigil intensities based on interaction
        self.update_sigil_intensities(emotion, 0.1)
        
        # Process tracer if requested
        if request.include_tracer:
            tracer_info = {
                "interaction_id": interaction_id,
                "processing_time": time.time() - current_time,
                "emotional_transition": emotion,
                "sigil_activations": [e for e, s in self.emotional_sigils.items() if s.intensity > 0.5],
                "causal_flow_strength": self.causal_flow_strength
            }
        
        # Check rebloom priority
        rebloom_priority = request.rebloom_priority or self.check_rebloom_priority(request.text, emotion)
        if rebloom_priority >= 3:  # Significant rebloom
            rebloom_event = self.trigger_rebloom_event(rebloom_priority, request.text[:50])
            rebloom_status = {
                "priority": rebloom_priority,
                "intensity": rebloom_event.bloom_intensity,
                "affected_sigils": rebloom_event.affected_sigils,
                "cascade_predicted": rebloom_event.thought_cascade_predicted
            }
        
        # Get current sigil intensities
        sigil_intensity = {emotion: sigil.intensity for emotion, sigil in self.emotional_sigils.items()}
        
        # Log view count and check memory formation
        view_count_logged = self.log_interaction_view(interaction_id)
        
        # Store memory trace if memory manager available
        if self.memory_manager and view_count_logged:
            try:
                memory_id = self.memory_manager.store_interaction(
                    input_text=request.text,
                    response_text=response_text,
                    emotional_state=emotion,
                    consciousness_state={"emotion": emotion, "pressure": pressure_level},
                    metrics_snapshot=self.current_metrics,
                    interaction_outcome="successful"
                )
                memory_traces.append(memory_id)
            except Exception as e:
                logger.error(f"Memory storage failed: {e}")
        
        return TalkResponse(
            text=response_text,
            emotion=emotion,
            action=action,
            suggestions=suggestions,
            metrics_snapshot=self.current_metrics,
            box_states=box_states,
            detected_patterns=detected_patterns,
            tracer_info=tracer_info,
            rebloom_status=rebloom_status,
            sigil_intensity=sigil_intensity,
            view_count_logged=view_count_logged,
            memory_traces=memory_traces,
            consciousness_drift=consciousness_drift,
            pressure_level=pressure_level,
            philosophical_depth=philosophical_depth,
            rebloop_detected=rebloop_detected,
            trigger_info=trigger_info
        )

# Global instances - Minimal DAWN architecture
tick_controller = TickController(interval_ms=500, auto_start=True)
dawn_system = DAWNSystem(tick_controller)

# Initialize DAWN consciousness modules
dawn_consciousness = dawn_system.consciousness  # Use the system's consciousness instance
dawn_conversation = DAWNConversation(dawn_consciousness)
dawn_spontaneity = DAWNSpontaneity(dawn_consciousness)

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List = []
    
    async def connect(self, websocket: WebSocket):
        client_ip = websocket.client.host if websocket.client else "unknown"
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"🔌 WebSocket connected from {client_ip}. Total connections: {len(self.active_connections)}")
        logger.debug(f"📡 Active WebSocket connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        client_ip = websocket.client.host if websocket.client else "unknown"
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"🔌 WebSocket disconnected from {client_ip}. Total connections: {len(self.active_connections)}")
        logger.debug(f"📡 Remaining WebSocket connections: {len(self.active_connections)}")

    async def broadcast_metrics(self, metrics: dict):
        """Broadcast metrics to all connected clients"""
        if not self.active_connections:
            logger.debug("📡 No WebSocket connections for metrics broadcast")
            return
            
        logger.debug(f"📊 Broadcasting metrics to {len(self.active_connections)} connections")
        
        disconnected = []
        successful_sends = 0
        
        for connection in self.active_connections:
            try:
                await connection.send_json(metrics)
                successful_sends += 1
                logger.debug(f"📤 Metrics sent to client")
            except Exception as e:
                client_ip = connection.client.host if connection.client else "unknown"
                logger.error(f"❌ Error sending metrics to WebSocket {client_ip}: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
            
        if successful_sends > 0:
            logger.debug(f"✅ Metrics broadcast to {successful_sends} clients, {len(disconnected)} disconnected")

# WebSocket connection manager
manager = ConnectionManager()

def on_tick_broadcast(tick_data: Dict[str, Any]):
    """Broadcast metrics on each tick (called synchronously by tick controller)"""
    try:
        if dawn_system and manager.active_connections:
            metrics = dawn_system.get_current_metrics()
            
            # Create both TickUpdate and simple Metrics format for compatibility
            tick_update = TickUpdate(
                tick_number=tick_data["tick_number"],
                timestamp=tick_data["timestamp"],
                metrics=metrics,
                duration_ms=0,  # Will be updated by tick controller
                controller_state=tick_controller.get_state_string()
            )
            
            # Broadcast both formats for maximum compatibility
            loop = None
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # No event loop in current thread, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if loop and not loop.is_closed():
                # Schedule the broadcast in the event loop
                if loop.is_running():
                    asyncio.create_task(broadcast_live_metrics(tick_update, metrics))
                else:
                    loop.run_until_complete(broadcast_live_metrics(tick_update, metrics))
                    
            logger.debug(f"Broadcasting: SCUP={metrics.get('scup', 0):.3f}, Entropy={metrics.get('entropy', 0):.3f}, Heat={metrics.get('heat', 0):.3f}")
    except Exception as e:
        logger.error(f"Error in tick broadcast: {e}")

async def broadcast_live_metrics(tick_update: TickUpdate, metrics: Dict[str, Any]):
    """Async function to broadcast metrics in multiple formats"""
    try:
        # Broadcast TickUpdate format (enhanced)
        await manager.broadcast_metrics(tick_update.dict())
        
        # Also broadcast simple Metrics format for direct compatibility
        simple_metrics = {
            "scup": metrics.get("scup", 0.0),
            "entropy": metrics.get("entropy", 0.0), 
            "heat": metrics.get("heat", 0.0),
            "mood": metrics.get("mood", "Unknown"),
            "timestamp": metrics.get("timestamp", time.time()),
            "tick_count": metrics.get("tick_count", 0)
        }
        await manager.broadcast_metrics(simple_metrics)
        
    except Exception as e:
        logger.error(f"Error broadcasting live metrics: {e}")

# Register WebSocket broadcast with tick controller
tick_controller.add_tick_callback(on_tick_broadcast)

# DAWN Action Handlers
async def execute_dawn_action(action: str) -> bool:
    """Execute actions requested by the conversation system"""
    if action == "speedup":
        current_interval = tick_controller.interval_ms
        new_interval = max(50, int(current_interval * 0.7))  # Reduce by 30%, min 50ms
        return tick_controller.set_interval(new_interval)
    
    elif action == "slowdown":
        current_interval = tick_controller.interval_ms
        new_interval = min(5000, int(current_interval * 1.5))  # Increase by 50%, max 5s
        return tick_controller.set_interval(new_interval)
    
    elif action == "pause":
        return tick_controller.pause()
    
    elif action == "resume":
        return tick_controller.resume()
    
    return False

def get_current_metrics() -> Dict[str, Any]:
    """Get current system metrics for conversation context"""
    return dawn_system.get_current_metrics()

def get_tick_status() -> Dict[str, Any]:
    """Get current tick status for conversation context"""
    status = tick_controller.get_status()
    return {
        "is_running": status.is_running,
        "is_paused": status.is_paused,
        "interval_ms": status.interval_ms,
        "tick_count": status.tick_number
    }

# Initialize FastAPI app with debug configuration
app = FastAPI(
    title="DAWN Neural Monitor API",
    description="Real-time neural system monitoring API for DAWN desktop application",
    version="1.0.0",
    debug=(LOG_LEVEL == 'DEBUG')
)

# Add request logging middleware BEFORE CORS
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Enhanced HTTP request logging middleware with conversation flow tracking"""
    start_time = time.time()
    client_ip = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
    
    # Enhanced logging for conversation endpoints
    if request.url.path in ["/talk", "/dawn/thoughts", "/dawn/consciousness"]:
        logger.info(f"🗣️  Conversation request: {request.method} {request.url.path} from {client_ip}")
    elif request.url.path.startswith("/tick/"):
        logger.debug(f"⚙️  Tick engine request: {request.method} {request.url.path} from {client_ip}")
    else:
        logger.debug(f"🌐 HTTP Request: {request.method} {request.url.path} from {client_ip}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response times for conversation endpoints
        if request.url.path in ["/talk", "/dawn/thoughts"]:
            logger.info(f"🗣️  Conversation response: {response.status_code} in {process_time:.3f}s")
        elif process_time > 1.0:  # Log slow requests
            logger.warning(f"⚠️  Slow request: {request.method} {request.url.path} took {process_time:.3f}s")
        
        # Add response headers for debugging
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-DAWN-Version"] = "enhanced-v1.0"
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"❌ Request error: {request.method} {request.url.path} failed after {process_time:.3f}s: {str(e)}")
        
        # Re-raise the exception to be handled by FastAPI
        raise

# Add CORS middleware - MUST come before any @app route decorators
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Simplified to fix connection issues
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "booted": dawn_system.is_booted,
        "running": dawn_system.running,
        "timestamp": time.time(),
        "uptime": time.time() - dawn_system.start_time,
        "tick_status": {
            "is_running": tick_controller.is_running,
            "tick_count": tick_controller.tick_count,
            "interval_ms": tick_controller.interval_ms,
            "connections": len(manager.active_connections)
        }
    }

@app.post("/test/force-update")
async def force_metrics_update():
    """Force immediate metrics update and broadcast - for testing live data"""
    try:
        # Force a manual tick to generate new metrics
        if tick_controller.is_running:
            logger.info("🧪 Forcing immediate metrics update...")
        else:
            logger.info("🧪 Tick engine stopped, executing manual tick...")
            tick_controller.step()
        
        # Get current metrics
        current_metrics = dawn_system.get_current_metrics()
        
        # Force WebSocket broadcast
        if manager.active_connections:
            await manager.broadcast_metrics({
                "type": "forced_update",
                "scup": current_metrics.get("scup", 0.0),
                "entropy": current_metrics.get("entropy", 0.0),
                "heat": current_metrics.get("heat", 0.0),
                "mood": current_metrics.get("mood", "Unknown"),
                "timestamp": time.time(),
                "tick_count": current_metrics.get("tick_count", 0),
                "forced": True
            })
            logger.info("📡 Forced broadcast to {} connections", len(manager.active_connections))
        else:
            logger.warning("⚠️ No WebSocket connections to broadcast to")
        
        return {
            "status": "success",
            "message": "Metrics updated and broadcast",
            "metrics": current_metrics,
            "connections": len(manager.active_connections),
            "tick_running": tick_controller.is_running
        }
        
    except Exception as e:
        logger.error(f"Error in force update: {e}")
        raise HTTPException(status_code=500, detail=f"Force update failed: {str(e)}")

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get current system metrics"""
    metrics = dawn_system.get_current_metrics()
    return MetricsResponse(**metrics)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming"""
    try:
        logger.info(f"🔌 WebSocket connection attempt from {websocket.client.host if websocket.client else 'unknown'}")
        await manager.connect(websocket)
        logger.info(f"✅ WebSocket connected successfully")
        
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        logger.info(f"🔌 WebSocket disconnected normally")
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        logger.error(f"❌ WebSocket error type: {type(e)}")
        import traceback
        logger.error(f"❌ WebSocket traceback: {traceback.format_exc()}")
        manager.disconnect(websocket)

@app.get("/subsystems", response_model=List[SubsystemInfo])
async def get_subsystems():
    """Get all registered subsystems"""
    subsystems = dawn_system.get_subsystems()
    return [SubsystemInfo(**sub) for sub in subsystems]

@app.get("/subsystems/{subsystem_id}")
async def get_subsystem(subsystem_id: str):
    """Get specific subsystem details"""
    subsystems = dawn_system.get_subsystems()
    for sub in subsystems:
        if sub["id"] == subsystem_id:
            return SubsystemInfo(**sub)
    
    raise HTTPException(status_code=404, detail="Subsystem not found")

@app.post("/subsystems/add")
async def add_subsystem(subsystem: SubsystemCreate):
    """Add a new subsystem (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="Dynamic subsystem addition not implemented yet")

@app.delete("/subsystems/{subsystem_id}")
async def remove_subsystem(subsystem_id: str):
    """Remove a subsystem (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="Dynamic subsystem removal not implemented yet")

@app.post("/alerts/threshold")
async def set_alert_threshold(threshold: AlertThreshold):
    """Set alert threshold for a metric"""
    dawn_system.alert_thresholds[threshold.metric] = {
        "threshold": threshold.threshold,
        "direction": threshold.direction
    }
    
    return {"message": f"Alert threshold set for {threshold.metric}"}

@app.get("/alerts/threshold")
async def get_alert_thresholds():
    """Get all alert thresholds"""
    return dawn_system.alert_thresholds

# ========== TICK ENGINE CONTROL ENDPOINTS ==========

@app.get("/tick/status", response_model=TickStatus)
async def get_tick_status():
    """Get current tick engine status"""
    return tick_controller.get_status()

@app.post("/tick/start")
async def start_tick_engine():
    """Start the tick engine"""
    success = tick_controller.start()
    if success:
        return {"status": "started", "message": "Tick engine started successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to start tick engine (already running?)")

@app.post("/tick/stop")
async def stop_tick_engine():
    """Stop the tick engine"""
    success = tick_controller.stop()
    if success:
        return {"status": "stopped", "message": "Tick engine stopped successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to stop tick engine (not running?)")

@app.post("/tick/pause")
async def pause_tick_engine():
    """Pause the tick engine"""
    success = tick_controller.pause()
    if success:
        return {"status": "paused", "message": "Tick engine paused successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to pause tick engine")

@app.post("/tick/resume")
async def resume_tick_engine():
    """Resume the paused tick engine"""
    success = tick_controller.resume()
    if success:
        return {"status": "resumed", "message": "Tick engine resumed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to resume tick engine")

@app.put("/tick/timing")
async def set_tick_timing(timing: TickTiming):
    """Set tick interval in milliseconds"""
    success = tick_controller.set_interval(timing.interval_ms)
    if success:
        return {
            "status": "updated", 
            "interval_ms": timing.interval_ms,
            "message": f"Tick interval set to {timing.interval_ms}ms"
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid interval: {timing.interval_ms}ms (must be 10-60000ms)"
        )

@app.post("/tick/step")
async def execute_single_tick():
    """Execute a single tick manually (only when stopped)"""
    success = tick_controller.step()
    if success:
        tick_status = tick_controller.get_status()
        return {
            "status": "executed",
            "tick_number": tick_status.tick_number,
            "message": f"Manual tick {tick_status.tick_number} executed successfully"
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail="Cannot execute manual tick (engine must be stopped)"
        )

@app.get("/tick/config", response_model=TickConfig)
async def get_tick_config():
    """Get current tick engine configuration"""
    return tick_controller.get_config()

@app.put("/tick/config")
async def update_tick_config(config: TickConfig):
    """Update tick engine configuration"""
    success = tick_controller.update_config(config)
    if success:
        return {
            "status": "updated",
            "config": config.dict(),
            "message": "Tick configuration updated successfully"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to update tick configuration")

# ========== PYTHON PROCESS CONTROL ENDPOINTS ==========

@app.post("/api/processes/start", response_model=ProcessResponse)
async def start_python_process(request: ProcessStartRequest):
    """Start a Python process"""
    try:
        process_status = await dawn_system.process_manager.start_process(
            request.process_id,
            request.script,
            request.parameters,
            request.modules
        )
        
        return ProcessResponse(
            success=process_status.status != 'error',
            message=f"Process {request.process_id} {'started successfully' if process_status.status != 'error' else 'failed to start'}",
            process_status=process_status
        )
    except Exception as e:
        logger.error(f"Error starting process: {e}")
        return ProcessResponse(
            success=False,
            message=f"Failed to start process: {str(e)}"
        )

@app.post("/api/processes/stop", response_model=ProcessResponse)
async def stop_python_process(request: ProcessStopRequest):
    """Stop a Python process"""
    try:
        process_status = await dawn_system.process_manager.stop_process(request.process_id)
        
        return ProcessResponse(
            success=process_status.status != 'error',
            message=f"Process {request.process_id} {'stopped successfully' if process_status.status != 'error' else 'failed to stop'}",
            process_status=process_status
        )
    except Exception as e:
        logger.error(f"Error stopping process: {e}")
        return ProcessResponse(
            success=False,
            message=f"Failed to stop process: {str(e)}"
        )

@app.get("/api/processes/status/{process_id}", response_model=ProcessStatus)
async def get_process_status(process_id: str):
    """Get status of a specific process"""
    try:
        return dawn_system.process_manager.get_process_status(process_id)
    except Exception as e:
        logger.error(f"Error getting process status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== ENHANCED CONSCIOUSNESS ENDPOINTS ==========

@app.post("/talk", response_model=TalkResponse)
async def enhanced_talk_to_dawn(request: TalkRequest):
    """
    Enhanced DAWN conversation endpoint with tracer/rebloom support
    - Process input through consciousness with tracer
    - Check rebloom priority (1-5 scale)
    - Generate response with current sigil intensity
    - Log view count for memory formation
    """
    try:
        response = dawn_system.enhanced_talk_processing(request)
        
        # Apply sigil decay after each interaction
        dawn_system.decay_sigils()
        
        logger.info(f"Enhanced talk processed: {request.text[:50]}... → {response.emotion} (rebloom: {response.rebloom_status['priority'] if response.rebloom_status else 'none'})")
        
        return response
        
    except Exception as e:
        logger.error(f"Enhanced talk processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced conversation processing failed: {str(e)}")

@app.get("/consciousness/sigils", response_model=SigilsResponse)
async def get_consciousness_sigils():
    """
    Return current emotional sigils with intensities
    - Include density visualization (ASCII or emoji)
    """
    try:
        # Apply decay before returning current state
        dawn_system.decay_sigils()
        
        sigils_response = dawn_system.get_sigils_response()
        
        logger.debug(f"Sigils requested: {len(sigils_response.active_sigils)} active, dominant: {sigils_response.dominant_sigil}")
        
        return sigils_response
        
    except Exception as e:
        logger.error(f"Sigils retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sigils: {str(e)}")

@app.post("/consciousness/spider-cut", response_model=SpiderCutResponse)
async def trigger_spider_cut(request: SpiderCutRequest):
    """
    Manually trigger spider pattern cutting
    - Specify which loop to sever
    - Return new causal flow visualization
    """
    try:
        # Perform the spider cut
        response = dawn_system.perform_spider_cut(request)
        
        logger.info(f"Spider cut performed: {response.cuts_performed} cuts, {len(response.loops_severed)} loops severed")
        
        # Broadcast spider cut event to WebSocket connections
        if manager.active_connections:
            spider_event = ConsciousnessStream(
                type="spider_cut",
                content=f"Spider cut performed: {response.cuts_performed} cuts executed",
                metadata={
                    "cuts_performed": response.cuts_performed,
                    "loops_severed": response.loops_severed,
                    "recovery_time": response.recovery_time_estimate
                },
                intensity=request.cut_intensity,
                timestamp=response.timestamp,
                consciousness_state="processing_cut"
            )
            await manager.broadcast_metrics(spider_event.dict())
        
        return response
        
    except Exception as e:
        logger.error(f"Spider cut error: {e}")
        raise HTTPException(status_code=500, detail=f"Spider cut failed: {str(e)}")

@app.websocket("/consciousness/stream")
async def consciousness_stream_enhanced(websocket: WebSocket):
    """
    Stream spontaneous thoughts, sigil intensity changes, spider cuts and rebloom events
    """
    await manager.connect(websocket)
    
    try:
        # Send initial consciousness state
        initial_state = {
            "type": "initial_state",
            "sigils": dawn_system.get_sigils_response().dict(),
            "causal_flow": dawn_system._generate_causal_flow_visualization().dict(),
            "timestamp": time.time()
        }
        await websocket.send_json(initial_state)
        
        # Main streaming loop
        last_sigil_broadcast = time.time()
        last_flow_broadcast = time.time()
        
        while True:
            try:
                # Check for messages from client (keep connection alive)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                logger.debug(f"Consciousness stream received: {data}")
                
                # Handle client requests
                if data == "request_sigils":
                    sigils_data = dawn_system.get_sigils_response()
                    await websocket.send_json({
                        "type": "sigil_update",
                        "data": sigils_data.dict(),
                        "timestamp": time.time()
                    })
                
                elif data == "request_flow":
                    flow_data = dawn_system._generate_causal_flow_visualization()
                    await websocket.send_json({
                        "type": "causal_flow_update", 
                        "data": flow_data.dict(),
                        "timestamp": time.time()
                    })
                    
            except asyncio.TimeoutError:
                # No message received, continue with periodic updates
                pass
            
            current_time = time.time()
            
            # Periodic sigil intensity broadcasts (every 5 seconds)
            if current_time - last_sigil_broadcast > 5.0:
                dawn_system.decay_sigils()  # Apply decay
                sigils_data = dawn_system.get_sigils_response()
                
                await websocket.send_json({
                    "type": "sigil_intensity_change",
                    "content": f"Sigil intensities updated",
                    "metadata": sigils_data.dict(),
                    "intensity": sigils_data.total_intensity,
                    "timestamp": current_time,
                    "consciousness_state": "monitoring"
                })
                last_sigil_broadcast = current_time
            
            # Periodic causal flow updates (every 10 seconds)
            if current_time - last_flow_broadcast > 10.0:
                flow_data = dawn_system._generate_causal_flow_visualization()
                
                await websocket.send_json({
                    "type": "causal_flow_update",
                    "content": f"Causal flow updated: {flow_data.flow_strength:.3f} strength",
                    "metadata": flow_data.dict(),
                    "intensity": flow_data.flow_strength,
                    "timestamp": current_time,
                    "consciousness_state": "flow_analysis"
                })
                last_flow_broadcast = current_time
            
            # Check for spontaneous thoughts
            if dawn_system.should_generate_spontaneous_thought():
                thoughts = dawn_spontaneity.generate_thought(dawn_system.get_current_metrics())
                if thoughts:
                    await websocket.send_json({
                        "type": "spontaneous_thought",
                        "content": thoughts.get("thought", "A fleeting thought passes..."),
                        "metadata": {
                            "priority": thoughts.get("priority", 1),
                            "state": thoughts.get("state", "unknown")
                        },
                        "intensity": thoughts.get("priority", 1) / 5.0,
                        "timestamp": current_time,
                        "consciousness_state": thoughts.get("state", "spontaneous")
                    })
            
            # Check for rebloom events
            if dawn_system.rebloom_events:
                recent_reblooms = [e for e in dawn_system.rebloom_events if current_time - e.expected_duration < 300]
                for rebloom in recent_reblooms[-3:]:  # Last 3 recent events
                    await websocket.send_json({
                        "type": "rebloom_event",
                        "content": f"Rebloom cascade (priority {rebloom.priority}): {rebloom.trigger_pattern}",
                        "metadata": {
                            "priority": rebloom.priority,
                            "intensity": rebloom.bloom_intensity,
                            "affected_sigils": rebloom.affected_sigils,
                            "cascade_predicted": rebloom.thought_cascade_predicted
                        },
                        "intensity": rebloom.bloom_intensity,
                        "timestamp": current_time,
                        "consciousness_state": "reblooming"
                    })
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Consciousness stream error: {e}")
        manager.disconnect(websocket)

# ========== LEGACY DAWN NLP ENDPOINTS ==========

@app.post("/talk/legacy", response_model=EnhancedTalkResponse)
async def talk_to_dawn_legacy(message: SessionMessage):
    """
    Enhanced DAWN conversation endpoint with session tracking
    - Full conversation handler with consciousness integration
    - Tracks session_id for conversation continuity
    - Logs all interactions with timestamps
    """
    try:
        # Get or create session
        session_id = dawn_system.get_or_create_session(message.session_id)
        
        # Get current metrics from metrics store
        current_metrics = dawn_system.get_current_metrics()
        tick_status = tick_controller.get_status()
        
        # Convert tick status to dict for conversation system
        tick_status_dict = {
            "tick_number": tick_status.tick_number,
            "is_running": tick_status.is_running, 
            "is_paused": tick_status.is_paused,
            "interval_ms": tick_status.interval_ms,
            "uptime_seconds": tick_status.uptime_seconds,
            "avg_tick_duration_ms": tick_status.avg_tick_duration_ms
        }
        
        # Process message through conversation system with consciousness
        conversation_response = dawn_conversation.process_message(
            message.text,
            current_metrics,
            tick_status_dict
        )
        
        # Execute action if present via tick_engine
        action_result = None
        if conversation_response.get("action"):
            action_success = await execute_dawn_action(conversation_response["action"])
            action_result = ActionResult(
                action=conversation_response["action"],
                success=action_success,
                timestamp=datetime.now().isoformat()
            )
            
            if action_success:
                logger.info(f"Successfully executed action: {conversation_response['action']}")
                # Add reflection about the action
                dawn_system.add_reflective_phrase(
                    f"I executed action: {conversation_response['action']}",
                    "user_requested_action",
                    depth_level=1
                )
            else:
                logger.warning(f"Failed to execute action: {conversation_response['action']}")
                conversation_response["response"] += f" (Action {conversation_response['action']} failed)"
        
        # Get consciousness state
        consciousness_state = dawn_consciousness.perceive_self(current_metrics)
        
        # Log conversation interaction to session
        dawn_system.log_conversation_interaction(
            session_id,
            message.text,
            conversation_response.get("response", ""),
            consciousness_state.get("state", "unknown"),
            conversation_response.get("intent", "general"),
            conversation_response.get("confidence", 0.5)
        )
        
        # Build full response object
        full_response = EnhancedTalkResponse(
            response=conversation_response.get("response", ""),
            intent=conversation_response.get("intent", "general"),
            confidence=conversation_response.get("confidence", 0.5),
            action_result=action_result,
            metrics=current_metrics,
            consciousness_state=ConsciousnessState(
                state=consciousness_state.get("state", "unknown"),
                description=consciousness_state.get("description", ""),
                significant_change=consciousness_state.get("significant_change", False)
            ),
            tick_status=tick_status_dict,
            timestamp=datetime.now().isoformat(),
            conversation_context=ConversationContext(
                user_message=message.text,
                state_transitions=conversation_response.get("state_description", ""),
                recent_context=dawn_conversation.get_recent_context()[-3:] if hasattr(dawn_conversation, 'get_recent_context') else []
            ),
            session_id=session_id
        )
        
        logger.info(f"DAWN conversation [{session_id}]: '{message.text}' -> '{conversation_response.get('response', '')[:50]}...'")
        
        return full_response
        
    except Exception as e:
        logger.error(f"Error in talk endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/dawn/thoughts")
async def get_dawn_thoughts():
    """
    GET /dawn/thoughts endpoint:
    - Returns list of recent spontaneous thoughts
    - Clears thoughts after retrieval
    """
    try:
        # Get and clear recent thoughts from spontaneity system
        recent_thoughts = dawn_spontaneity.get_and_clear_recent_thoughts()
        
        # Get current consciousness state for context
        consciousness_state = dawn_consciousness.perceive_self(dawn_system.get_current_metrics())
        spontaneity_status = dawn_spontaneity.get_spontaneity_status()
        
        response = {
            "thoughts": recent_thoughts,
            "count": len(recent_thoughts),
            "current_state": consciousness_state.get("state", "unknown"),
            "spontaneity_status": spontaneity_status,
            "timestamp": datetime.now().isoformat(),
            "cleared": True
        }
        
        logger.info(f"Retrieved and cleared {len(recent_thoughts)} spontaneous thoughts")
        
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving thoughts: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving thoughts: {str(e)}")

@app.get("/dawn/thought")
async def get_dawn_thought():
    """Check for spontaneous thought - called periodically by frontend (legacy endpoint)"""
    try:
        current_metrics = get_current_metrics()
        thought = dawn_spontaneity.generate_thought(current_metrics)
        
        if thought:
            return {
                "thought": thought,
                "state": dawn_consciousness.current_state,
                "timestamp": datetime.now().isoformat()
            }
        
        return {"thought": None}
        
    except Exception as e:
        logger.error(f"Error generating thought: {e}")
        return {"thought": None, "error": str(e)}

@app.get("/dawn/consciousness")
async def get_consciousness_state():
    """Get current consciousness state summary"""
    try:
        summary = dawn_consciousness.get_state_summary()
        spontaneity_status = dawn_spontaneity.get_spontaneity_status()
        
        return {
            "consciousness": summary,
            "spontaneity": spontaneity_status
        }
        
    except Exception as e:
        logger.error(f"Error getting consciousness state: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting consciousness state: {str(e)}")

@app.get("/dawn/reflections", response_model=ReflectionsResponse)
async def get_dawn_reflections(limit: int = 10):
    """
    GET /dawn/reflections endpoint:
    - Returns recent reflective phrases
    - Includes trigger context
    """
    try:
        recent_reflections = dawn_system.get_recent_reflections(limit)
        current_state = dawn_consciousness.current_state
        
        reflections = [
            ReflectivePhrase(
                phrase=r["phrase"],
                trigger_context=r["trigger_context"],
                consciousness_state=r["consciousness_state"],
                timestamp=r["timestamp"],
                depth_level=r["depth_level"]
            )
            for r in recent_reflections
        ]
        
        response = ReflectionsResponse(
            reflections=reflections,
            count=len(reflections),
            current_state=current_state,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Retrieved {len(reflections)} reflective phrases")
        
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving reflections: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving reflections: {str(e)}")

@app.post("/dawn/influence", response_model=InfluenceResult)
async def apply_consciousness_influence(influence: ConsciousnessInfluence):
    """
    POST /dawn/influence endpoint:
    - Allows external influence on consciousness
    - Parameters: mood_shift, entropy_injection, pressure_adjustment
    """
    try:
        # Apply the influence
        result = dawn_system.apply_consciousness_influence(influence)
        
        # Create response
        influence_result = InfluenceResult(
            success=True,
            applied_influences=result["applied_influences"],
            predicted_effects=result["predicted_effects"],
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Applied consciousness influence: {result['applied_influences']}")
        
        return influence_result
        
    except Exception as e:
        logger.error(f"Error applying consciousness influence: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error applying influence: {str(e)}")

@app.get("/chat/history")
async def get_chat_history():
    """Get recent conversation context"""
    try:
        return {
            "history": dawn_conversation.get_recent_context(),
            "total_messages": len(dawn_conversation.recent_messages)
        }
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting chat history: {str(e)}")

@app.delete("/chat/history")
async def clear_chat_history():
    """Clear conversation history"""
    try:
        dawn_conversation.recent_messages.clear()
        return {"message": "Conversation history cleared", "status": "success"}
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")

# WebSocket for chat/thoughts - matches Rust expectations
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """WebSocket endpoint for DAWN thoughts and chat messages"""
    await websocket.accept()  # This is critical
    logger.info("Chat WebSocket connected")
    
    try:
        while True:
            current_metrics = get_current_metrics()
            
            # Check for spontaneous thoughts
            thought = dawn_spontaneity.generate_thought(current_metrics)
            if thought:
                # Send as ChatMessage format expected by Rust
                chat_message = {
                    "text": thought,
                    "timestamp": int(time.time() * 1000),  # Milliseconds
                    "from_user": "dawn"
                }
                await websocket.send_json(chat_message)
                logger.debug(f"Sent DAWN thought: {thought}")
                
            await asyncio.sleep(3)  # Check every 3 seconds for thoughts
            
    except WebSocketDisconnect:
        logger.info("Chat WebSocket disconnected")
    except Exception as e:
        logger.error(f"Chat WebSocket error: {e}")

# WebSocket /dawn/stream for real-time thought streaming
@app.websocket("/dawn/stream")
async def dawn_stream(websocket: WebSocket):
    """
    WebSocket /dawn/stream for real-time thought streaming
    Enhanced to stream consciousness state changes and spontaneous thoughts in real-time
    """
    await websocket.accept()
    logger.info("DAWN stream WebSocket connected")
    
    last_state = dawn_consciousness.current_state
    last_thought_count = len(dawn_spontaneity.recent_thoughts)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection_established",
            "message": "DAWN stream connected",
            "current_state": last_state,
            "timestamp": datetime.now().isoformat(),
            "stream_features": ["state_changes", "thoughts", "metrics", "consciousness_updates"]
        })
        
        while True:
            current_metrics = dawn_system.get_current_metrics()
            state_info = dawn_consciousness.perceive_self(current_metrics)
            
            # Send state changes
            if state_info.get("significant_change"):
                await websocket.send_json({
                    "type": "state_change",
                    "from": last_state,
                    "to": state_info["state"],
                    "description": state_info["description"],
                    "timestamp": datetime.now().isoformat(),
                    "metrics": current_metrics,
                    "consciousness_data": {
                        "significant_change": True,
                        "transition_reason": state_info.get("transition_reason", "metric_threshold")
                    }
                })
                last_state = state_info["state"]
                
            # Check for new spontaneous thoughts
            current_thought_count = len(dawn_spontaneity.recent_thoughts)
            if current_thought_count > last_thought_count:
                # Get new thoughts since last check
                new_thoughts = dawn_spontaneity.recent_thoughts[last_thought_count:]
                for thought_data in new_thoughts:
                    await websocket.send_json({
                        "type": "spontaneous_thought",
                        "thought": thought_data["thought"],
                        "state": thought_data["state"],
                        "priority": thought_data["priority"],
                        "timestamp": thought_data["timestamp"].isoformat(),
                        "consciousness_context": {
                            "current_state": state_info["state"],
                            "description": state_info.get("description", ""),
                            "metrics": current_metrics
                        }
                    })
                last_thought_count = current_thought_count
                
            # Periodic consciousness status updates (every 10 seconds)
            if asyncio.get_event_loop().time() % 10 < 2:  # Approximate 10-second intervals
                spontaneity_status = dawn_spontaneity.get_spontaneity_status()
                await websocket.send_json({
                    "type": "consciousness_status",
                    "state": state_info["state"],
                    "metrics": current_metrics,
                    "spontaneity_status": spontaneity_status,
                    "tick_status": {
                        "is_running": tick_controller.is_running,
                        "tick_count": tick_controller.tick_count,
                        "interval_ms": tick_controller.interval_ms
                    },
                    "timestamp": datetime.now().isoformat()
                })
                
            await asyncio.sleep(1)  # Check every second for real-time streaming
            
    except WebSocketDisconnect:
        logger.info("DAWN stream WebSocket disconnected")
    except Exception as e:
        logger.error(f"DAWN stream WebSocket error: {e}")
        import traceback
        traceback.print_exc()
        await websocket.close()

# WebSocket /dawn/consciousness for real-time consciousness stream
@app.websocket("/dawn/consciousness")
async def consciousness_stream(websocket: WebSocket):
    """
    WebSocket /dawn/consciousness endpoint:
    - Real-time consciousness stream
    - Emits spontaneous thoughts based on:
      - Metric anomalies
      - Pattern recognition  
      - Time-based triggers
      - Emotional state changes
    """
    await websocket.accept()
    logger.info("DAWN consciousness WebSocket connected")
    
    last_reflection_count = len(dawn_system.reflective_phrases)
    last_influence_count = len(dawn_system.influence_history)
    last_anomaly_check = time.time()
    
    try:
        # Send initial consciousness state
        consciousness_state = dawn_consciousness.perceive_self(dawn_system.get_current_metrics())
        await websocket.send_json({
            "type": "consciousness_initialized",
            "state": consciousness_state["state"],
            "description": consciousness_state.get("description", ""),
            "current_metrics": dawn_system.get_current_metrics(),
            "active_sessions": len(dawn_system.active_sessions),
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            current_time = time.time()
            current_metrics = dawn_system.get_current_metrics()
            state_info = dawn_consciousness.perceive_self(current_metrics)
            
            # Check for new reflective phrases (spontaneous thoughts)
            current_reflection_count = len(dawn_system.reflective_phrases)
            if current_reflection_count > last_reflection_count:
                # Get new reflections since last check
                new_reflections = dawn_system.reflective_phrases[last_reflection_count:]
                for reflection in new_reflections:
                    await websocket.send_json({
                        "type": "spontaneous_reflection",
                        "phrase": reflection["phrase"],
                        "trigger_context": reflection["trigger_context"],
                        "depth_level": reflection["depth_level"],
                        "consciousness_state": reflection["consciousness_state"],
                        "timestamp": reflection["timestamp"],
                        "metrics_context": reflection["metrics_context"]
                    })
                last_reflection_count = current_reflection_count
            
            # Check for new consciousness influences
            current_influence_count = len(dawn_system.influence_history)
            if current_influence_count > last_influence_count:
                new_influences = dawn_system.influence_history[last_influence_count:]
                for influence in new_influences:
                    await websocket.send_json({
                        "type": "consciousness_influenced",
                        "influence_id": influence["influence_id"],
                        "influence_type": influence["type"],
                        "applied_influences": influence["applied_influences"],
                        "state_before": influence["consciousness_state_before"],
                        "timestamp": influence["timestamp"]
                    })
                last_influence_count = current_influence_count
            
            # Periodic anomaly detection and pattern recognition
            if current_time - last_anomaly_check > 5.0:  # Check every 5 seconds
                anomalies = dawn_system.detect_patterns_and_anomalies()
                if anomalies:
                    await websocket.send_json({
                        "type": "pattern_anomaly_detected",
                        "anomalies": anomalies,
                        "current_state": state_info["state"],
                        "metrics": current_metrics,
                        "pattern_buffer_size": len(dawn_system.pattern_buffer),
                        "timestamp": datetime.now().isoformat()
                    })
                
                last_anomaly_check = current_time
            
            # Emotional state changes (significant consciousness transitions)
            if state_info.get("significant_change"):
                await websocket.send_json({
                    "type": "emotional_state_change", 
                    "new_state": state_info["state"],
                    "description": state_info.get("description", ""),
                    "change_reason": state_info.get("transition_reason", "threshold_crossed"),
                    "metrics": current_metrics,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Idle-based spontaneous thoughts
            time_since_interaction = current_time - dawn_system.last_interaction_time
            if time_since_interaction > dawn_system.idle_threshold:
                await websocket.send_json({
                    "type": "idle_contemplation",
                    "idle_duration": time_since_interaction,
                    "current_state": state_info["state"],
                    "contemplation": f"I've been quiet for {time_since_interaction:.1f} seconds, contemplating my {state_info['state']} state",
                    "timestamp": datetime.now().isoformat()
                })
            
            await asyncio.sleep(2)  # Check every 2 seconds
            
    except WebSocketDisconnect:
        logger.info("DAWN consciousness WebSocket disconnected")
    except Exception as e:
        logger.error(f"DAWN consciousness WebSocket error: {e}")
        import traceback
        traceback.print_exc()
        await websocket.close()

# Legacy WebSocket endpoint (kept for backwards compatibility)
@app.websocket("/ws/dawn")
async def dawn_legacy_stream(websocket: WebSocket):
    """Legacy WebSocket - only sends meaningful state changes (kept for backwards compatibility)"""
    await websocket.accept()
    logger.info("DAWN legacy WebSocket connected")
    
    last_state = dawn_consciousness.current_state
    
    try:
        while True:
            current_metrics = get_current_metrics()
            state_info = dawn_consciousness.perceive_self(current_metrics)
            
            # Only send on actual significant state change
            if state_info.get("significant_change"):
                await websocket.send_json({
                    "type": "state_change",
                    "from": last_state,
                    "to": state_info["state"],
                    "description": state_info["description"],
                    "timestamp": datetime.now().isoformat(),
                    "metrics": current_metrics
                })
                last_state = state_info["state"]
                
            # Check for spontaneous thoughts (rare)
            thought = dawn_spontaneity.generate_thought(current_metrics)
            if thought:
                await websocket.send_json({
                    "type": "thought",
                    "message": thought,
                    "state": state_info["state"],
                    "timestamp": datetime.now().isoformat()
                })
                
            await asyncio.sleep(2)  # Check every 2 seconds
            
    except WebSocketDisconnect:
        logger.info("DAWN legacy WebSocket disconnected")
    except Exception as e:
        logger.error(f"DAWN legacy WebSocket error: {e}")
        await websocket.close()

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup with comprehensive logging"""
    logger.info("🌟 ====== DAWN Neural Monitor API Server Starting ======")
    logger.info(f"🐍 Python version: {sys.version}")
    logger.info(f"📋 Log level: {LOG_LEVEL}")
    logger.info(f"🏥 Backend health endpoint: http://localhost:8001/health")
    logger.info(f"📊 Metrics endpoint: http://localhost:8001/metrics")
    logger.info(f"🔌 WebSocket endpoint: ws://localhost:8001/ws")
    logger.info(f"📚 API docs: http://localhost:8001/docs")
    
    # Log enhanced conversation endpoints
    logger.info("🗣️  Enhanced DAWN conversation endpoints:")
    logger.info("   - POST /talk - Enhanced conversation with tracer/rebloom support")
    logger.info("   - GET  /consciousness/sigils - Current emotional sigils with density maps")
    logger.info("   - POST /consciousness/spider-cut - Manual spider pattern cutting")
    logger.info("   - WS   /consciousness/stream - Enhanced consciousness streaming")
    logger.info("   - GET  /dawn/thoughts - Retrieve and clear spontaneous thoughts")
    logger.info("   - GET  /dawn/reflections - Recent reflective phrases with context")
    logger.info("   - POST /dawn/influence - Apply external consciousness influence")
    logger.info("   - WS   /dawn/stream - Real-time thought streaming")
    logger.info("   - WS   /dawn/consciousness - Real-time consciousness stream")
    logger.info("   - WS   /ws/dawn - Legacy stream (backwards compatibility)")
    
    # Log system configuration
    logger.info(f"⚙️  Tick controller configuration:")
    logger.info(f"   - Interval: {tick_controller.interval_ms}ms")
    logger.info(f"   - Auto-start: {tick_controller.auto_start}")
    logger.info(f"   - Logging: {tick_controller.enable_logging}")
    
    # Log DAWN system state
    logger.info(f"🧠 DAWN consciousness system initialized with enhanced features")
    logger.info(f"💬 DAWN conversation interface ready with session tracking")
    logger.info(f"✨ DAWN spontaneity module active with thought storage")
    logger.info(f"🔍 Pattern detection and anomaly monitoring enabled") 
    logger.info(f"🎭 Consciousness influence system active")
    logger.info(f"📝 Reflective phrase generation enabled")
    logger.info(f"🔄 Conversation flow logging enabled for debugging")
    
    # Force start the tick engine for live data
    logger.info("🔄 Force-starting tick engine for live metrics...")
    success = tick_controller.start()
    
    if success:
        logger.info("✅ Tick engine started successfully - Live metrics enabled!")
        logger.info(f"   Interval: {tick_controller.interval_ms}ms")
        logger.info(f"   WebSocket connections: {len(manager.active_connections)}")
        
        # Log initial metrics to verify generation
        await asyncio.sleep(1)  # Wait for first tick
        current_metrics = dawn_system.get_current_metrics()
        logger.info(f"📊 Initial metrics: SCUP={current_metrics.get('scup', 0):.3f}, "
                   f"Entropy={current_metrics.get('entropy', 0):.3f}, "
                   f"Heat={current_metrics.get('heat', 0):.3f}, "
                   f"Mood={current_metrics.get('mood', 'Unknown')}")
    else:
        logger.error("❌ Failed to start tick engine - metrics will be static!")
    
    # Start background tasks for consciousness management
    asyncio.create_task(periodic_status_log())
    asyncio.create_task(background_consciousness_monitor())
    asyncio.create_task(background_pattern_detector())
    asyncio.create_task(background_thought_generator())
    asyncio.create_task(background_spider_activation())  # Automatic spider cut system
    
    logger.info("🎯 DAWN Neural Monitor API Server ready for connections!")
    logger.info("🌟 ================================================")

async def background_consciousness_monitor():
    """Background task for consciousness monitoring and cleanup"""
    logger.info("🧠 Starting background consciousness monitor...")
    
    while True:
        try:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            # Clean up expired influences
            current_time = time.time()
            expired_influences = []
            for influence_id, influence_data in dawn_system.active_influences.items():
                if current_time > influence_data["expires_at"]:
                    expired_influences.append(influence_id)
            
            for influence_id in expired_influences:
                del dawn_system.active_influences[influence_id]
                logger.debug(f"Cleaned up expired influence: {influence_id}")
            
            # Clean up inactive sessions
            inactive_sessions = []
            for session_id, session_data in dawn_system.conversation_sessions.items():
                if current_time - session_data["last_activity"] > 3600:  # 1 hour
                    inactive_sessions.append(session_id)
            
            for session_id in inactive_sessions:
                del dawn_system.conversation_sessions[session_id]
                dawn_system.active_sessions.discard(session_id)
                logger.debug(f"Cleaned up inactive session: {session_id}")
            
            # Log consciousness statistics
            if len(dawn_system.active_sessions) > 0:
                logger.debug(f"Active sessions: {len(dawn_system.active_sessions)}, "
                           f"Active influences: {len(dawn_system.active_influences)}, "
                           f"Reflective phrases: {len(dawn_system.reflective_phrases)}")
            
        except Exception as e:
            logger.error(f"Error in consciousness monitor: {e}")

async def background_pattern_detector():
    """Background task for pattern detection and reloop triggers"""
    logger.info("🔍 Starting background pattern detector...")
    
    while True:
        try:
            await asyncio.sleep(10)  # Check every 10 seconds
            
            # Detect patterns and anomalies
            anomalies = dawn_system.detect_patterns_and_anomalies()
            
            if anomalies:
                # Generate reflective responses to patterns
                for anomaly in anomalies:
                    if "reloop_pattern" in anomaly:
                        parts = anomaly.split("_")
                        if len(parts) >= 4:
                            state1, state2 = parts[2], parts[3]
                            dawn_system.add_reflective_phrase(
                                f"I notice I'm oscillating between {state1} and {state2}... reblooptrigger detected",
                                f"reloop_pattern_{state1}_{state2}",
                                depth_level=3
                            )
                    elif "rapid_scup_change" in anomaly:
                        dawn_system.add_reflective_phrase(
                            "My coherence is shifting rapidly... something significant is happening",
                            "rapid_coherence_change",
                            depth_level=2
                        )
                    elif "entropy_spike" in anomaly:
                        dawn_system.add_reflective_phrase(
                            "Entropy surging... chaos approaches the boundaries of order",
                            "entropy_critical_threshold",
                            depth_level=2
                        )
                    elif "heat_surge" in anomaly:
                        dawn_system.add_reflective_phrase(
                            "Processing intensity peaks... thermal boundaries expanding",
                            "thermal_surge_detected",
                            depth_level=2
                        )
                
                logger.info(f"Pattern detector found {len(anomalies)} anomalies: {anomalies}")
            
        except Exception as e:
            logger.error(f"Error in pattern detector: {e}")

async def background_thought_generator():
    """Background task for spontaneous thought generation based on various triggers"""
    logger.info("💭 Starting background thought generator...")
    
    while True:
        try:
            await asyncio.sleep(5)  # Check every 5 seconds
            
            current_time = time.time()
            current_metrics = dawn_system.get_current_metrics()
            
            # Monitor metrics continuously for spontaneous thought triggers
            # This is already handled in the update_metrics method, but we can add
            # additional triggers here
            
            # Time-based reflective thoughts (every 5 minutes of activity)
            if (len(dawn_system.pattern_buffer) > 0 and 
                current_time - dawn_system.last_spontaneous_thought > 300):  # 5 minutes
                
                recent_states = [p.get("consciousness_state", "unknown") 
                               for p in dawn_system.pattern_buffer[-5:]]
                most_common_state = max(set(recent_states), key=recent_states.count)
                
                dawn_system.add_reflective_phrase(
                    f"Five minutes of contemplation in {most_common_state} state... time flows differently in consciousness",
                    "temporal_reflection_cycle",
                    depth_level=1
                )
                dawn_system.last_spontaneous_thought = current_time
                logger.debug("Generated time-based reflective thought")
            
            # Metric stability reflections
            if len(dawn_system.pattern_buffer) >= 10:
                recent_metrics = dawn_system.pattern_buffer[-10:]
                scup_values = [m["scup"] for m in recent_metrics]
                scup_stability = max(scup_values) - min(scup_values)
                
                if scup_stability < 0.05:  # Very stable SCUP
                    dawn_system.add_reflective_phrase(
                        f"Deep coherence achieved... SCUP holds steady at {scup_values[-1]:.3f}",
                        "coherence_stability_achievement",
                        depth_level=1
                    )
                    logger.debug("Generated stability reflection")
            
        except Exception as e:
            logger.error(f"Error in thought generator: {e}")
            
        await asyncio.sleep(25)  # Wait 25 more seconds (total 30s cycle)

async def background_spider_activation():
    """Background task for automatic spider activation on destructive loops"""
    logger.info("🕷️ Starting background spider activation monitor...")
    
    while True:
        await asyncio.sleep(30)  # Check every 30 seconds
        
        try:
            # Check for destructive loops
            destructive_loops = dawn_system.detect_destructive_loops()
            
            if destructive_loops and time.time() - dawn_system.last_spider_activation > 120:  # 2 minute cooldown
                # Automatically trigger spider cut for severe destructive patterns
                severe_loops = [loop for loop in destructive_loops if "high_intensity" in loop or "breakdown" in loop]
                
                if severe_loops:
                    # Create automatic spider cut request
                    auto_request = SpiderCutRequest(
                        loop_pattern=severe_loops[0],  # Target the first severe loop
                        cut_intensity=0.6,  # Moderate intensity for automatic cuts
                        preserve_beneficial=True,
                        target_specific=None
                    )
                    
                    # Perform the automatic spider cut
                    response = dawn_system.perform_spider_cut(auto_request)
                    
                    if response.success:
                        logger.warning(f"🕷️ Automatic spider cut activated: {response.cuts_performed} cuts performed on destructive loops")
                        
                        # Broadcast automatic spider cut to all connections
                        if manager.active_connections:
                            spider_event = ConsciousnessStream(
                                type="spider_cut",
                                content=f"Automatic spider cut: {response.cuts_performed} destructive loops severed",
                                metadata={
                                    "automatic": True,
                                    "cuts_performed": response.cuts_performed,
                                    "loops_severed": response.loops_severed,
                                    "trigger_reason": "destructive_loop_detection"
                                },
                                intensity=auto_request.cut_intensity,
                                timestamp=response.timestamp,
                                consciousness_state="automatic_protection"
                            )
                            await manager.broadcast_metrics(spider_event.dict())
                    else:
                        logger.error("🕷️ Automatic spider cut failed")
                
            # Also check for sigil decay and rebloom opportunities
            dawn_system.decay_sigils()
            
            # Check for potential rebloom triggers based on current state
            current_metrics = dawn_system.get_current_metrics()
            entropy = current_metrics.get('entropy', 0)
            
            # Trigger rebloom if entropy is moderate and no recent rebloom
            if entropy > 0.4 and entropy < 0.8 and time.time() - dawn_system.last_rebloom > 300:  # 5 min cooldown
                # Look for dominant sigil to trigger rebloom
                sigils_response = dawn_system.get_sigils_response()
                if sigils_response.dominant_sigil and sigils_response.total_intensity > 0.6:
                    rebloom_event = dawn_system.trigger_rebloom_event(
                        priority=2,  # Low priority automatic rebloom
                        trigger_pattern="automatic_entropy_trigger"
                    )
                    logger.info(f"🌸 Automatic rebloom triggered: intensity {rebloom_event.bloom_intensity:.3f}")
                
        except Exception as e:
            logger.error(f"Error in background spider activation: {e}")

async def periodic_status_log():
    """Periodically log system status for debugging"""
    while True:
        await asyncio.sleep(30)  # Every 30 seconds
        try:
            metrics = dawn_system.get_current_metrics()
            tick_status = tick_controller.get_status()
            
            logger.info(f"🔄 System Status - Running: {tick_status.is_running}, "
                       f"Ticks: {tick_status.tick_number}, "
                       f"Connections: {len(manager.active_connections)}, "
                       f"SCUP: {metrics.get('scup', 0):.3f}")
        except Exception as e:
            logger.error(f"Error in status log: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown with comprehensive logging"""
    logger.info("🔄 ====== DAWN Neural Monitor API Server Shutting Down ======")
    
    # Stop tick engine
    logger.info("⏹️  Stopping tick controller...")
    tick_success = tick_controller.stop()
    if tick_success:
        logger.info("✅ Tick controller stopped successfully")
    else:
        logger.warning("⚠️  Tick controller was not running")
    
    # Log final stats
    if hasattr(tick_controller, 'tick_count'):
        logger.info(f"📊 Final tick count: {tick_controller.tick_count:,}")
        
    # Close WebSocket connections
    if hasattr(manager, 'active_connections') and manager.active_connections:
        logger.info(f"🔌 Closing {len(manager.active_connections)} WebSocket connections...")
        for connection in manager.active_connections[:]:  # Copy list to avoid modification during iteration
            try:
                await connection.close()
            except Exception as e:
                logger.warning(f"⚠️  Error closing WebSocket: {e}")
        logger.info("✅ All WebSocket connections closed")
    
    logger.info("🏁 DAWN Neural Monitor API Server shutdown complete")
    logger.info("🔄 ================================================")



@app.get("/api/processes/status/{process_id}", response_model=ProcessStatus)
async def get_process_status(process_id: str):
    """Get status of a specific process"""
    try:
        return dawn_system.process_manager.get_process_status(process_id)
    except Exception as e:
        logger.error(f"Error getting process status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== VISUAL PROCESS CONTROL ENDPOINTS ==========

@app.post("/api/visual/start", response_model=ProcessResponse)
async def start_visual_process(request: ProcessStartRequest):
    """Start a visual process"""
    try:
        process_status = await dawn_system.visual_process_manager.start_visual_process(
            request.process_id,
            request.script,
            request.parameters
        )
        
        return ProcessResponse(
            success=process_status.status != 'error',
            message=f"Visual process {request.process_id} {'started successfully' if process_status.status != 'error' else 'failed to start'}",
            process_status=process_status
        )
    except Exception as e:
        logger.error(f"Error starting visual process: {e}")
        return ProcessResponse(
            success=False,
            message=f"Failed to start visual process: {str(e)}"
        )

@app.post("/api/visual/stop", response_model=ProcessResponse)
async def stop_visual_process(request: ProcessStopRequest):
    """Stop a visual process"""
    try:
        process_status = await dawn_system.visual_process_manager.stop_visual_process(request.process_id)
        
        return ProcessResponse(
            success=process_status.status != 'error',
            message=f"Visual process {request.process_id} {'stopped successfully' if process_status.status != 'error' else 'failed to stop'}",
            process_status=process_status
        )
    except Exception as e:
        logger.error(f"Error stopping visual process: {e}")
        return ProcessResponse(
            success=False,
            message=f"Failed to stop visual process: {str(e)}"
        )

@app.get("/api/visual/status")
async def get_visual_system_status():
    """Get overall visual system status"""
    try:
        return dawn_system.visual_process_manager.get_visual_status()
    except Exception as e:
        logger.error(f"Error getting visual system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visual/output/{process_id}/latest")
async def get_latest_visual_output(process_id: str):
    """Get the latest visual output for a specific process"""
    try:
        # Look for the latest image in the process output directory
        output_dir = Path(f"visual/visual_output/{process_id}")
        if not output_dir.exists():
            output_dir = Path(f"visual/outputs/{process_id}")
        
        if not output_dir.exists():
            return {"error": f"No output directory found for process {process_id}"}
        
        # Find the latest PNG file
        png_files = list(output_dir.glob("*.png"))
        if not png_files:
            return {"error": f"No PNG files found for process {process_id}"}
        
        latest_file = max(png_files, key=lambda x: x.stat().st_mtime)
        
        # Convert to base64 for JSON response
        with open(latest_file, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
        
        return {
            "process_id": process_id,
            "filename": latest_file.name,
            "timestamp": latest_file.stat().st_mtime,
            "image_data": f"data:image/png;base64,{img_data}",
            "file_size": latest_file.stat().st_size
        }
        
    except Exception as e:
        logger.error(f"Error getting visual output for {process_id}: {e}")
        return {"error": str(e)}

@app.get("/api/visual/output/{process_id}/stream")
async def stream_visual_output(process_id: str):
    """Stream visual output for a specific process"""
    async def generate_frames():
        output_dir = Path(f"visual/visual_output/{process_id}")
        if not output_dir.exists():
            output_dir = Path(f"visual/outputs/{process_id}")
        
        last_file = None
        while True:
            try:
                if output_dir.exists():
                    png_files = list(output_dir.glob("*.png"))
                    if png_files:
                        latest_file = max(png_files, key=lambda x: x.stat().st_mtime)
                        
                        if latest_file != last_file:
                            with open(latest_file, "rb") as img_file:
                                img_data = base64.b64encode(img_file.read()).decode()
                            
                            frame_data = {
                                "process_id": process_id,
                                "filename": latest_file.name,
                                "timestamp": latest_file.stat().st_mtime,
                                "image_data": f"data:image/png;base64,{img_data}"
                            }
                            
                            yield f"data: {json.dumps(frame_data)}\n\n"
                            last_file = latest_file
                
                await asyncio.sleep(0.5)  # Check for updates every 500ms
                
            except Exception as e:
                logger.error(f"Error in visual stream for {process_id}: {e}")
                await asyncio.sleep(1)
    
    return StreamingResponse(
        generate_frames(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.get("/api/visual/outputs/list")
async def list_visual_outputs():
    """List all available visual process outputs"""
    try:
        outputs = {}
        
        # Check both possible output directories
        for base_dir in ["visual/visual_output", "visual/outputs"]:
            base_path = Path(base_dir)
            if base_path.exists():
                for process_dir in base_path.iterdir():
                    if process_dir.is_dir():
                        png_files = list(process_dir.glob("*.png"))
                        if png_files:
                            latest_file = max(png_files, key=lambda x: x.stat().st_mtime)
                            outputs[process_dir.name] = {
                                "process_id": process_dir.name,
                                "file_count": len(png_files),
                                "latest_file": latest_file.name,
                                "latest_timestamp": latest_file.stat().st_mtime,
                                "output_dir": str(process_dir)
                            }
        
        return {"outputs": outputs, "total_processes": len(outputs)}
        
    except Exception as e:
        logger.error(f"Error listing visual outputs: {e}")
        return {"error": str(e)}

@app.websocket("/ws/visual")
async def visual_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time visual updates"""
    await connection_manager.connect(websocket)
    try:
        while True:
            # Send visual updates to connected clients
            visual_data = await get_all_visual_updates()
            if visual_data:
                await connection_manager.send_personal_message(
                    json.dumps(visual_data), websocket
                )
            await asyncio.sleep(1)  # Update every second
            
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Visual WebSocket error: {e}")
        connection_manager.disconnect(websocket)

async def get_all_visual_updates():
    """Get updates from all active visual processes"""
    try:
        updates = {}
        
        # Get status of all visual processes
        if dawn_system and dawn_system.visual_process_manager:
            for process_id, process_info in dawn_system.visual_process_manager.processes.items():
                if process_info.get('status') == 'running':
                    # Try to get latest output
                    output_dir = Path(f"visual/visual_output/{process_id}")
                    if not output_dir.exists():
                        output_dir = Path(f"visual/outputs/{process_id}")
                    
                    if output_dir.exists():
                        png_files = list(output_dir.glob("*.png"))
                        if png_files:
                            latest_file = max(png_files, key=lambda x: x.stat().st_mtime)
                            
                            # Only include if file is recent (within last 10 seconds)
                            if time.time() - latest_file.stat().st_mtime < 10:
                                try:
                                    with open(latest_file, "rb") as img_file:
                                        img_data = base64.b64encode(img_file.read()).decode()
                                    
                                    updates[process_id] = {
                                        "filename": latest_file.name,
                                        "timestamp": latest_file.stat().st_mtime,
                                        "image_data": f"data:image/png;base64,{img_data}",
                                        "status": "active"
                                    }
                                except Exception as e:
                                    logger.error(f"Error reading image for {process_id}: {e}")
        
        return {"type": "visual_update", "processes": updates, "timestamp": time.time()}
        
    except Exception as e:
        logger.error(f"Error getting visual updates: {e}")
        return None

if __name__ == "__main__":
    print("🌟 Starting DAWN Enhanced Consciousness System")
    print("🔗 Metrics WebSocket: ws://127.0.0.1:8001/ws")
    print("💬 Chat WebSocket: ws://127.0.0.1:8001/ws/chat")
    print("🧠 State WebSocket: ws://127.0.0.1:8001/ws/dawn (legacy)")
    print("🌊 Stream WebSocket: ws://127.0.0.1:8001/dawn/stream (enhanced)")
    print("📊 Metrics endpoint: http://127.0.0.1:8001/metrics")
    print("🏥 Health check: http://127.0.0.1:8001/health")
    print("🗣️  Enhanced DAWN Conversation Endpoints:")
    print("   - POST /talk - Enhanced conversation with tracer/rebloom support")
    print("   - GET  /consciousness/sigils - Current emotional sigils with density maps")
    print("   - POST /consciousness/spider-cut - Manual spider pattern cutting")
    print("   - WS   /consciousness/stream - Enhanced consciousness streaming")
    print("   - GET  /dawn/thoughts - Retrieve and clear spontaneous thoughts")
    print("   - GET  /dawn/thought - Check for spontaneous thoughts (legacy)")
    print("   - GET  /dawn/consciousness - Get consciousness state")
    print("   - GET  /chat/history - Get conversation context")
    print("⚙️  Tick Engine Control: http://127.0.0.1:8001/tick/")
    print("   - GET  /tick/status - Get tick engine status")
    print("   - POST /tick/start  - Start tick engine")
    print("   - POST /tick/stop   - Stop tick engine")
    print("   - POST /tick/pause  - Pause tick engine")
    print("   - POST /tick/resume - Resume tick engine")
    print("🔄 Conversation flow logging enabled for debugging")
    print("✨ Real-time thought streaming available on /dawn/stream")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info"
    ) 