# /visual/visual_consciousness_manager.py - DAWN Visual Integration System (Threading-based)

import threading
import time
import queue
from typing import Dict, List, Optional, Set, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import traceback

class VisualPriority(Enum):
    """Priority levels for visual processes"""
    CRITICAL = 1    # Always running (pulse_map_renderer)
    HIGH = 2        # Core consciousness displays
    MEDIUM = 3      # Analysis and monitoring
    LOW = 4         # Artistic/aesthetic visualizations
    POETIC = 5      # Mythological elements (juliet_flowers, persephone)

class VisualMode(Enum):
    """Visual rendering modes"""
    REALTIME = "realtime"       # Continuous updates
    PERIODIC = "periodic"       # Scheduled updates
    TRIGGERED = "triggered"     # Event-driven updates
    SNAPSHOT = "snapshot"       # One-time captures

@dataclass
class VisualProcess:
    """Configuration for a visual thread"""
    name: str
    module_path: str
    priority: VisualPriority
    mode: VisualMode
    target_fps: float = 10.0
    memory_limit_mb: int = 100
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    data_requirements: List[str] = field(default_factory=list)
    
    # Runtime state
    thread: Optional[threading.Thread] = None
    last_update: Optional[datetime] = None
    error_count: int = 0
    performance_score: float = 1.0
    data_queue: Optional[queue.Queue] = None
    control_queue: Optional[queue.Queue] = None
    stop_event: Optional[threading.Event] = None

class VisualConsciousnessManager:
    """
    Manages all visual processes for DAWN consciousness monitoring using threading.
    Coordinates data flow, resource allocation, and thread lifecycle.
    """
    
    def __init__(self, max_concurrent_processes: int = 8):
        self.max_concurrent_processes = max_concurrent_processes
        self.is_running = False
        self.processes: Dict[str, VisualProcess] = {}
        self.shared_state_queue = queue.Queue(maxsize=100)
        self.control_thread = None
        self.update_thread = None
        self.stop_event = threading.Event()
        
        # Performance monitoring
        self.system_load = 0.0
        self.memory_usage = 0.0
        self.active_process_count = 0
        
        # Data pipeline
        self.latest_consciousness_state = {}
        self.state_update_callbacks: List[Callable] = []
        
        print("🎬 Visual Consciousness Manager initialized (Threading mode)")
        self._register_visual_processes()
    
    def _register_visual_processes(self):
        """Register all available visual processes"""
        
        # === CRITICAL PROCESSES (Always Running) ===
        self.register_process(VisualProcess(
            name="pulse_map_renderer",
            module_path="visual.pulse_map_renderer",
            priority=VisualPriority.CRITICAL,
            mode=VisualMode.REALTIME,
            target_fps=15.0,
            data_requirements=["thermal_stats", "tick_stats"]
        ))
        
        # === HIGH PRIORITY (Core Consciousness) ===
        self.register_process(VisualProcess(
            name="mood_heatmap",
            module_path="visual.mood_heatmap", 
            priority=VisualPriority.HIGH,
            mode=VisualMode.REALTIME,
            target_fps=10.0,
            data_requirements=["mood_state", "entropy_snapshot"]
        ))
        
        self.register_process(VisualProcess(
            name="entropy_cluster_plot",
            module_path="visual.entropy_cluster_plot",
            priority=VisualPriority.HIGH,
            mode=VisualMode.PERIODIC,
            target_fps=5.0,
            data_requirements=["entropy_snapshot", "system_health"]
        ))
        
        self.register_process(VisualProcess(
            name="cognition_pressure_map",
            module_path="visual.cognition_pressure_map",
            priority=VisualPriority.HIGH,
            mode=VisualMode.REALTIME,
            target_fps=8.0,
            data_requirements=["thermal_stats", "alignment_snapshot", "performance_metrics"]
        ))
        
        # === MEDIUM PRIORITY (Analysis & Monitoring) ===
        self.register_process(VisualProcess(
            name="mood_transition_animator",
            module_path="visual.mood_transition_animator",
            priority=VisualPriority.MEDIUM,
            mode=VisualMode.TRIGGERED,
            data_requirements=["mood_state", "tick_count"]
        ))
        
        self.register_process(VisualProcess(
            name="entropy_arc_animator", 
            module_path="visual.entropy_arc_animator",
            priority=VisualPriority.MEDIUM,
            mode=VisualMode.REALTIME,
            target_fps=12.0,
            data_requirements=["entropy_snapshot"]
        ))
        
        self.register_process(VisualProcess(
            name="drift_vector_animation",
            module_path="visual.drift_vector_animation",
            priority=VisualPriority.MEDIUM,
            mode=VisualMode.PERIODIC,
            target_fps=6.0,
            data_requirements=["semantic_field", "alignment_snapshot"]
        ))
        
        self.register_process(VisualProcess(
            name="memory_clusters",
            module_path="visual.memory_clusters",
            priority=VisualPriority.MEDIUM,
            mode=VisualMode.PERIODIC,
            target_fps=3.0,
            data_requirements=["semantic_field"]
        ))
        
        self.register_process(VisualProcess(
            name="belief_resonance_scatter",
            module_path="visual.belief_resonance_scatter",
            priority=VisualPriority.MEDIUM,
            mode=VisualMode.TRIGGERED,
            data_requirements=["alignment_snapshot", "semantic_field"]
        ))
        
        # === LOW PRIORITY (Detailed Analysis) ===
        self.register_process(VisualProcess(
            name="synthesis_lineage_animator",
            module_path="visual.synthesis_lineage_animator",
            priority=VisualPriority.LOW,
            mode=VisualMode.PERIODIC,
            target_fps=2.0,
            data_requirements=["semantic_field", "tick_count"]
        ))
        
        self.register_process(VisualProcess(
            name="recursive_bloom_tree",
            module_path="visual.recursive_bloom_tree",
            priority=VisualPriority.LOW,
            mode=VisualMode.SNAPSHOT,
            data_requirements=["semantic_field"]
        ))
        
        self.register_process(VisualProcess(
            name="semantic_timeline_animator",
            module_path="visual.semantic_timeline_animator",
            priority=VisualPriority.LOW,
            mode=VisualMode.PERIODIC,
            target_fps=4.0,
            data_requirements=["semantic_field", "tick_count"]
        ))
        
        # === POETIC ELEMENTS (Mythological/Artistic) ===
        self.register_process(VisualProcess(
            name="persephone_decay_map",
            module_path="visual.persephone_decay_map",
            priority=VisualPriority.POETIC,
            mode=VisualMode.TRIGGERED,
            data_requirements=["entropy_snapshot", "thermal_stats"]
        ))
        
        self.register_process(VisualProcess(
            name="crow_stall_heatmap",
            module_path="visual.crow_stall_heatmap", 
            priority=VisualPriority.POETIC,
            mode=VisualMode.PERIODIC,
            target_fps=1.0,
            data_requirements=["system_health"]
        ))
        
        print(f"🎨 Registered {len(self.processes)} visual processes")
    
    def register_process(self, visual_process: VisualProcess):
        """Register a visual process"""
        visual_process.data_queue = queue.Queue(maxsize=50)
        visual_process.control_queue = queue.Queue(maxsize=10)
        visual_process.stop_event = threading.Event()
        self.processes[visual_process.name] = visual_process
    
    def start_visual_consciousness(self):
        """Start the visual consciousness system"""
        if self.is_running:
            print("⚠️ Visual consciousness already running")
            return
        
        print("🌅 Starting Visual Consciousness System (Threading mode)")
        print("="*50)
        
        self.is_running = True
        self.stop_event.clear()
        
        # Start control thread
        self.control_thread = threading.Thread(
            target=self._control_loop,
            name="VisualControl",
            daemon=True
        )
        self.control_thread.start()
        
        # Start update thread  
        self.update_thread = threading.Thread(
            target=self._update_loop,
            name="VisualUpdate", 
            daemon=True
        )
        self.update_thread.start()
        
        # Start critical processes immediately
        self._start_critical_processes()
        
        print("✨ Visual consciousness system online")
        print("="*50)
    
    def _start_critical_processes(self):
        """Start critical priority processes immediately"""
        critical_processes = [p for p in self.processes.values() 
                            if p.priority == VisualPriority.CRITICAL]
        
        for process in critical_processes:
            if self._start_process(process):
                print(f"🔥 Critical process started: {process.name}")
    
    def _control_loop(self):
        """Main control loop for managing visual processes"""
        print("[VisualControl] 🎛️ Control loop started")
        
        while not self.stop_event.is_set():
            try:
                # Monitor system resources
                self._update_system_metrics()
                
                # Manage process lifecycle
                self._manage_process_lifecycle()
                
                # Handle priority changes based on consciousness state
                self._adapt_to_consciousness_state()
                
                # Performance optimization
                self._optimize_resource_allocation()
                
                time.sleep(0.5)  # Control loop frequency
                
            except Exception as e:
                print(f"[VisualControl] ❌ Control loop error: {e}")
                traceback.print_exc()
                time.sleep(1.0)
        
        print("[VisualControl] 🛑 Control loop stopped")
    
    def _update_loop(self):
        """Data update loop for feeding consciousness state to processes"""
        print("[VisualUpdate] 📡 Update loop started")
        
        while not self.stop_event.is_set():
            try:
                # Get latest consciousness state from shared queue
                if not self.shared_state_queue.empty():
                    try:
                        state_data = self.shared_state_queue.get_nowait()
                        self.latest_consciousness_state = state_data
                        self._distribute_state_data(state_data)
                    except queue.Empty:
                        pass
                
                time.sleep(0.1)  # Update frequency
                
            except Exception as e:
                print(f"[VisualUpdate] ❌ Update loop error: {e}")
                time.sleep(0.5)
        
        print("[VisualUpdate] 🛑 Update loop stopped")
    
    def _distribute_state_data(self, state_data: Dict):
        """Distribute consciousness state data to relevant processes"""
        for process in self.processes.values():
            if not process.enabled or not process.thread or not process.thread.is_alive():
                continue
            
            # Check if process needs this data
            required_data = self._extract_required_data(state_data, process.data_requirements)
            if not required_data:
                continue
            
            # Send data based on process mode
            if process.mode == VisualMode.REALTIME:
                self._send_realtime_data(process, required_data)
            elif process.mode == VisualMode.PERIODIC:
                self._send_periodic_data(process, required_data)
            elif process.mode == VisualMode.TRIGGERED:
                self._send_triggered_data(process, required_data, state_data)
    
    def _extract_required_data(self, state_data: Dict, requirements: List[str]) -> Dict:
        """Extract only the data required by a process"""
        extracted = {}
        for req in requirements:
            if req in state_data:
                extracted[req] = state_data[req]
        return extracted if extracted else None
    
    def _send_realtime_data(self, process: VisualProcess, data: Dict):
        """Send data to realtime processes"""
        try:
            if not process.data_queue.full():
                process.data_queue.put_nowait({
                    'type': 'state_update',
                    'timestamp': datetime.now(),
                    'data': data
                })
        except queue.Full:
            pass  # Skip if queue full - realtime processes should drain quickly
    
    def _send_periodic_data(self, process: VisualProcess, data: Dict):
        """Send data to periodic processes"""
        now = datetime.now()
        if (process.last_update is None or 
            (now - process.last_update).total_seconds() >= 1.0/process.target_fps):
            
            try:
                process.data_queue.put_nowait({
                    'type': 'periodic_update',
                    'timestamp': now,
                    'data': data
                })
                process.last_update = now
            except queue.Full:
                pass
    
    def _send_triggered_data(self, process: VisualProcess, data: Dict, full_state: Dict):
        """Send data to triggered processes based on state changes"""
        # Implement trigger logic based on state changes
        should_trigger = False
        
        # Example triggers
        if process.name == "mood_transition_animator":
            # Trigger on mood changes
            current_mood = full_state.get('mood_state', {}).get('tag', '')
            last_mood = getattr(process, '_last_mood', '')
            should_trigger = current_mood != last_mood
            process._last_mood = current_mood
        
        elif process.name == "belief_resonance_scatter":
            # Trigger on alignment changes
            current_alignment = full_state.get('alignment_snapshot', {}).get('current_alignment', 0)
            last_alignment = getattr(process, '_last_alignment', 0)
            should_trigger = abs(current_alignment - last_alignment) > 0.1
            process._last_alignment = current_alignment
        
        if should_trigger:
            try:
                process.data_queue.put_nowait({
                    'type': 'trigger_update',
                    'timestamp': datetime.now(),
                    'data': data,
                    'trigger_reason': f'{process.name}_state_change'
                })
            except queue.Full:
                pass
    
    def _manage_process_lifecycle(self):
        """Manage starting/stopping processes based on priority and resources"""
        active_count = sum(1 for p in self.processes.values() if p.thread and p.thread.is_alive())
        self.active_process_count = active_count
        
        # Start high priority processes if under limit
        if active_count < self.max_concurrent_processes:
            self._start_priority_processes()
        
        # Stop low priority processes if over limit
        elif active_count > self.max_concurrent_processes:
            self._stop_lowest_priority_processes()
        
        # Restart failed processes
        self._restart_failed_processes()
    
    def _start_priority_processes(self):
        """Start processes by priority order"""
        candidates = [p for p in self.processes.values() 
                     if p.enabled and (not p.thread or not p.thread.is_alive())]
        
        # Sort by priority (lower number = higher priority)
        candidates.sort(key=lambda p: p.priority.value)
        
        for process in candidates:
            if self.active_process_count >= self.max_concurrent_processes:
                break
            
            if self._start_process(process):
                self.active_process_count += 1
                print(f"🚀 Started visual process: {process.name} (Priority: {process.priority.name})")
    
    def _stop_lowest_priority_processes(self):
        """Stop lowest priority processes to free resources"""
        active_processes = [p for p in self.processes.values() 
                          if p.thread and p.thread.is_alive()]
        
        # Sort by priority (higher number = lower priority)  
        active_processes.sort(key=lambda p: p.priority.value, reverse=True)
        
        for process in active_processes:
            if self.active_process_count <= self.max_concurrent_processes:
                break
            
            self._stop_process(process)
            self.active_process_count -= 1
            print(f"⏸️ Stopped visual process: {process.name} (freed resources)")
    
    def _start_process(self, visual_process: VisualProcess) -> bool:
        """Start a visual process thread"""
        try:
            # Reset stop event
            visual_process.stop_event.clear()
            
            # Create and start thread
            thread = threading.Thread(
                target=self._run_visual_process,
                args=(visual_process.name, visual_process.module_path, 
                      visual_process.data_queue, visual_process.control_queue,
                      visual_process.stop_event),
                name=f"Visual_{visual_process.name}",
                daemon=True
            )
            thread.start()
            visual_process.thread = thread
            visual_process.error_count = 0
            return True
            
        except Exception as e:
            print(f"❌ Failed to start {visual_process.name}: {e}")
            visual_process.error_count += 1
            return False
    
    def _stop_process(self, visual_process: VisualProcess):
        """Stop a visual process gracefully"""
        if visual_process.thread and visual_process.thread.is_alive():
            try:
                # Signal stop
                visual_process.stop_event.set()
                visual_process.control_queue.put_nowait({'type': 'shutdown'})
                
                # Wait for thread to finish
                visual_process.thread.join(timeout=2.0)
                
            except Exception as e:
                print(f"⚠️ Error stopping {visual_process.name}: {e}")
            finally:
                visual_process.thread = None
    
    def _run_visual_process(self, name: str, module_path: str, 
                           data_queue: queue.Queue, control_queue: queue.Queue,
                           stop_event: threading.Event):
        """Run a visual process in its own thread"""
        try:
            print(f"[{name}] 🎨 Visual process started")
            
            # Import the visual module
            try:
                module = __import__(module_path, fromlist=[''])
            except ModuleNotFoundError:
                print(f"[{name}] ⚠️ Module not found: {module_path} - using placeholder")
                self._run_placeholder_visual(name, data_queue, control_queue, stop_event)
                return
            
            # Look for standard interface functions with backward compatibility
            if hasattr(module, 'run_visual_process'):
                # Check function signature for backward compatibility
                import inspect
                sig = inspect.signature(module.run_visual_process)
                param_count = len(sig.parameters)
                
                if param_count == 2:
                    # Old interface (data_queue, control_queue)
                    print(f"[{name}] 🔄 Using legacy 2-argument interface")
                    self._run_legacy_visual_process(name, module, data_queue, control_queue, stop_event)
                elif param_count >= 3:
                    # New interface (data_queue, control_queue, stop_event)
                    module.run_visual_process(data_queue, control_queue, stop_event)
                else:
                    print(f"[{name}] ❌ Invalid run_visual_process signature")
                    self._run_placeholder_visual(name, data_queue, control_queue, stop_event)
                    
            elif hasattr(module, 'main'):
                # Try main function with similar compatibility check
                import inspect
                try:
                    sig = inspect.signature(module.main)
                    param_count = len(sig.parameters)
                    if param_count >= 3:
                        module.main(data_queue, control_queue, stop_event)
                    else:
                        self._run_legacy_main(name, module, data_queue, control_queue, stop_event)
                except:
                    self._run_legacy_main(name, module, data_queue, control_queue, stop_event)
                    
            else:
                print(f"[{name}] 🔧 No standard interface found - using generic runner")
                self._generic_visual_runner(name, module, data_queue, control_queue, stop_event)
                
        except Exception as e:
            print(f"[{name}] ❌ Visual process error: {e}")
            traceback.print_exc()
    
    def _run_legacy_visual_process(self, name: str, module, data_queue: queue.Queue, 
                                  control_queue: queue.Queue, stop_event: threading.Event):
        """Run legacy visual process with 2-argument interface"""
        print(f"[{name}] 🔧 Running legacy visual process wrapper")
        
        # Create a thread to monitor stop_event and inject shutdown signal
        def stop_monitor():
            stop_event.wait()
            try:
                control_queue.put_nowait({'type': 'shutdown'})
            except queue.Full:
                pass
        
        monitor_thread = threading.Thread(target=stop_monitor, daemon=True)
        monitor_thread.start()
        
        try:
            # Call the legacy function
            module.run_visual_process(data_queue, control_queue)
        except Exception as e:
            print(f"[{name}] ❌ Legacy process error: {e}")
        
        print(f"[{name}] 🛑 Legacy visual process stopped")
    
    def _run_legacy_main(self, name: str, module, data_queue: queue.Queue, 
                        control_queue: queue.Queue, stop_event: threading.Event):
        """Run legacy main function"""
        print(f"[{name}] 🔧 Running legacy main wrapper")
        
        # Create stop monitor
        def stop_monitor():
            stop_event.wait()
            try:
                control_queue.put_nowait({'type': 'shutdown'})
            except queue.Full:
                pass
        
        monitor_thread = threading.Thread(target=stop_monitor, daemon=True)
        monitor_thread.start()
        
        try:
            # Try different call patterns
            if data_queue and control_queue:
                module.main(data_queue, control_queue)
            else:
                module.main()
        except Exception as e:
            print(f"[{name}] ❌ Legacy main error: {e}")
        
        print(f"[{name}] 🛑 Legacy main stopped")

    def _run_placeholder_visual(self, name: str, data_queue: queue.Queue, 
                               control_queue: queue.Queue, stop_event: threading.Event):
        """Placeholder runner for missing visual modules"""
        print(f"[{name}] 🔧 Running placeholder visualization")
        
        while not stop_event.is_set():
            try:
                # Check for shutdown signal
                if not control_queue.empty():
                    msg = control_queue.get_nowait()
                    if msg.get('type') == 'shutdown':
                        break
                
                # Process data if available (just drain the queue)
                if not data_queue.empty():
                    data = data_queue.get_nowait()
                    # Could log interesting data here
                    if name == "pulse_map_renderer":
                        thermal_data = data.get('data', {}).get('thermal_stats', {})
                        if thermal_data:
                            heat = thermal_data.get('current_heat', 0)
                            print(f"[{name}] 🔥 Thermal: {heat:.2f}")
                
                time.sleep(0.5)  # Slower update for placeholder
                
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                print(f"[{name}] ❌ Placeholder error: {e}")
                break
        
        print(f"[{name}] 🛑 Placeholder process stopped")
    
    def _generic_visual_runner(self, name: str, module, data_queue: queue.Queue, 
                              control_queue: queue.Queue, stop_event: threading.Event):
        """Generic runner for visual modules without standard interface"""
        print(f"[{name}] 🔧 Using generic visual runner")
        
        while not stop_event.is_set():
            try:
                # Check for shutdown signal
                if not control_queue.empty():
                    msg = control_queue.get_nowait()
                    if msg.get('type') == 'shutdown':
                        break
                
                # Process data if available
                if not data_queue.empty():
                    data = data_queue.get_nowait()
                    # Attempt to call common visualization functions
                    if hasattr(module, 'update_visualization'):
                        module.update_visualization(data['data'])
                    elif hasattr(module, 'render'):
                        module.render(data['data'])
                    elif hasattr(module, 'process_data'):
                        module.process_data(data['data'])
                
                time.sleep(0.1)
                
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                print(f"[{name}] ❌ Generic runner error: {e}")
                break
        
        print(f"[{name}] 🛑 Visual process stopped")
    
    def update_consciousness_state(self, state_data: Dict):
        """Update consciousness state data for visual processes"""
        try:
            self.shared_state_queue.put_nowait(state_data)
        except queue.Full:
            # Remove oldest state and add new one
            try:
                self.shared_state_queue.get_nowait()
                self.shared_state_queue.put_nowait(state_data)
            except queue.Empty:
                pass
    
    def _adapt_to_consciousness_state(self):
        """Adapt visual priorities based on consciousness state"""
        if not self.latest_consciousness_state:
            return
        
        # Get consciousness metrics
        coherence = self.latest_consciousness_state.get('system_health', {}).get('overall_coherence', 0.5)
        thermal_zone = self.latest_consciousness_state.get('thermal_stats', {}).get('current_zone', '🟢 calm')
        
        # Adaptive behavior based on consciousness state
        if coherence < 0.3:
            # Low coherence - focus on diagnostic visuals
            self._boost_priority(['cognition_pressure_map', 'entropy_cluster_plot'])
            self._reduce_priority(VisualPriority.POETIC)
        
        elif thermal_zone == '🔴 surge':
            # High activity - emphasize thermal and entropy monitoring
            self._boost_priority(['pulse_map_renderer', 'mood_heatmap', 'entropy_arc_animator'])
        
        elif coherence > 0.8:
            # High coherence - allow poetic/aesthetic processes
            self._restore_priority(VisualPriority.POETIC)
    
    def _boost_priority(self, process_names: List[str]):
        """Temporarily boost priority of specific processes"""
        for name in process_names:
            if name in self.processes:
                process = self.processes[name]
                if not process.enabled:
                    process.enabled = True
                    print(f"⚡ Boosted priority for {name}")
    
    def _reduce_priority(self, priority_level: VisualPriority):
        """Reduce priority of processes at given level"""
        affected = [p for p in self.processes.values() if p.priority == priority_level]
        for process in affected:
            if process.enabled:
                process.enabled = False
                print(f"🔽 Reduced priority for {process.name}")
    
    def _restore_priority(self, priority_level: VisualPriority):
        """Restore priority of processes at given level"""
        affected = [p for p in self.processes.values() if p.priority == priority_level]
        for process in affected:
            if not process.enabled:
                process.enabled = True
                print(f"🔼 Restored priority for {process.name}")
    
    def _restart_failed_processes(self):
        """Restart processes that have failed"""
        for process in self.processes.values():
            if (process.enabled and process.thread and 
                not process.thread.is_alive() and process.error_count < 3):
                
                # Add delay before restart to prevent rapid cycling
                import time
                if not hasattr(process, '_last_restart_time'):
                    process._last_restart_time = 0
                
                current_time = time.time()
                if current_time - process._last_restart_time < 10.0:  # 10 second cooldown
                    continue
                
                print(f"🔄 Restarting failed process: {process.name} (attempt {process.error_count + 1})")
                if self._start_process(process):
                    print(f"✅ Successfully restarted {process.name}")
                    process._last_restart_time = current_time
                else:
                    process.error_count += 1
                    if process.error_count >= 3:
                        print(f"❌ Disabling {process.name} after 3 failures")
                        process.enabled = False
    
    def _update_system_metrics(self):
        """Update system performance metrics"""
        # Simple resource monitoring
        active_processes = sum(1 for p in self.processes.values() 
                             if p.thread and p.thread.is_alive())
        self.system_load = min(active_processes / self.max_concurrent_processes, 1.0)
    
    def _optimize_resource_allocation(self):
        """Optimize resource allocation based on performance"""
        if self.system_load > 0.9:
            # High load - reduce target fps for medium/low priority processes
            for process in self.processes.values():
                if process.priority.value >= 3:  # Medium or lower priority
                    process.target_fps = max(process.target_fps * 0.8, 1.0)
        
        elif self.system_load < 0.5:
            # Low load - restore fps for processes
            for process in self.processes.values():
                if hasattr(process, '_original_fps'):
                    process.target_fps = min(process.target_fps * 1.1, process._original_fps)
    
    def shutdown_visual_consciousness(self):
        """Shutdown all visual processes gracefully"""
        if not self.is_running:
            return
        
        print("🌅 Shutting down Visual Consciousness System...")
        
        # Stop control loops
        self.stop_event.set()
        
        if self.control_thread and self.control_thread.is_alive():
            self.control_thread.join(timeout=2.0)
        
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=2.0)
        
        # Stop all visual processes
        for process in self.processes.values():
            self._stop_process(process)
        
        self.is_running = False
        print("🎬 Visual consciousness system shutdown complete")
    
    def get_visual_status(self) -> Dict:
        """Get comprehensive visual system status"""
        process_status = {}
        for name, process in self.processes.items():
            process_status[name] = {
                'enabled': process.enabled,
                'running': process.thread.is_alive() if process.thread else False,
                'priority': process.priority.name,
                'mode': process.mode.value,
                'target_fps': process.target_fps,
                'error_count': process.error_count,
                'last_update': process.last_update.isoformat() if process.last_update else None
            }
        
        return {
            'is_running': self.is_running,
            'active_processes': self.active_process_count,
            'max_processes': self.max_concurrent_processes,
            'system_load': self.system_load,
            'processes': process_status
        }

# Global visual manager instance
visual_manager = VisualConsciousnessManager()

# Convenience functions for integration with main DAWN system
def start_visual_consciousness():
    """Start the visual consciousness system"""
    visual_manager.start_visual_consciousness()

def update_visual_consciousness_state(state_data: Dict):
    """Update consciousness state for visual processes"""
    visual_manager.update_consciousness_state(state_data)

def shutdown_visual_consciousness():
    """Shutdown visual consciousness system"""
    visual_manager.shutdown_visual_consciousness()

def get_visual_status() -> Dict:
    """Get visual system status"""
    return visual_manager.get_visual_status()

def enable_visual_process(name: str):
    """Enable a specific visual process"""
    if name in visual_manager.processes:
        visual_manager.processes[name].enabled = True
        print(f"✅ Enabled visual process: {name}")

def disable_visual_process(name: str):
    """Disable a specific visual process"""
    if name in visual_manager.processes:
        visual_manager.processes[name].enabled = False
        visual_manager._stop_process(visual_manager.processes[name])
        print(f"⏸️ Disabled visual process: {name}")
