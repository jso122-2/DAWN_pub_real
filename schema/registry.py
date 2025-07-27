# /schema/registry.py
"""
Schema Registry for DAWN
========================
Central registry for all schema components with rhizome network integration.
Manages registration, discovery, and interconnection of consciousness elements.
"""

import time
import uuid
from typing import Dict, List, Set, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading
import weakref
import json

# Import rhizome (assuming this exists in your system)
try:
    from rhizome.rhizome_map import RhizomeMap
except ImportError:
    # Fallback implementation if rhizome module not available
    class RhizomeMap:
        def __init__(self):
            self.nodes = {}
            self.connections = defaultdict(set)
        
        def add_node(self, node_id: str, data: Any):
            self.nodes[node_id] = data
        
        def connect(self, node1: str, node2: str):
            self.connections[node1].add(node2)
            self.connections[node2].add(node1)
        
        def get_connections(self, node_id: str) -> Set[str]:
            return self.connections.get(node_id, set())

class ComponentType(Enum):
    """Types of components that can be registered"""
    MODULE = "module"
    VISUALIZER = "visualizer"
    PROCESSOR = "processor"
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    CONSCIOUSNESS_NODE = "consciousness_node"
    NUTRIENT_SOURCE = "nutrient_source"
    BLOOM_GENERATOR = "bloom_generator"
    SIGIL = "sigil"
    CUSTOM = "custom"

class ComponentStatus(Enum):
    """Status of registered components"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    SHUTDOWN = "shutdown"

@dataclass
class ComponentMetadata:
    """Metadata for registered components"""
    component_id: str
    name: str
    component_type: ComponentType
    status: ComponentStatus = ComponentStatus.INITIALIZING
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    registration_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    error_count: int = 0
    custom_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegistryEvent:
    """Events that occur in the registry"""
    event_type: str  # registered, unregistered, connected, disconnected, status_change
    component_id: str
    timestamp: float
    details: Dict[str, Any] = field(default_factory=dict)

class SchemaRegistry:
    """
    Central registry for all DAWN schema components with rhizome integration
    """
    
    def __init__(self):
        # Core registry storage
        self.components: Dict[str, ComponentMetadata] = {}
        self.component_instances: Dict[str, Any] = {}  # Weak references to actual instances
        
        # Rhizome network
        self.rhizome = RhizomeMap()
        
        # Component organization
        self.components_by_type: Dict[ComponentType, Set[str]] = defaultdict(set)
        self.components_by_capability: Dict[str, Set[str]] = defaultdict(set)
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Event system
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history = []
        self.max_event_history = 1000
        
        # Discovery and routing
        self.service_routes: Dict[str, str] = {}  # capability -> component_id mapping
        self.broadcast_channels: Dict[str, Set[str]] = defaultdict(set)
        
        # Health monitoring
        self.health_checks: Dict[str, Callable] = {}
        self.last_health_check = time.time()
        self.health_check_interval = 30.0  # seconds
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Start health monitoring
        self._start_health_monitor()
    
    def register(self, 
                component_id: str,
                name: str,
                component_type: ComponentType,
                instance: Optional[Any] = None,
                **kwargs) -> bool:
        """
        Register a component in the schema registry
        
        Args:
            component_id: Unique identifier for the component
            name: Human-readable name
            component_type: Type of component
            instance: Optional reference to the component instance
            **kwargs: Additional metadata (version, dependencies, capabilities, etc.)
        
        Returns:
            True if registration successful, False otherwise
        """
        with self.lock:
            if component_id in self.components:
                print(f"[REGISTRY] Component {component_id} already registered")
                return False
            
            # Create metadata
            metadata = ComponentMetadata(
                component_id=component_id,
                name=name,
                component_type=component_type,
                version=kwargs.get('version', '1.0.0'),
                dependencies=kwargs.get('dependencies', []),
                capabilities=kwargs.get('capabilities', []),
                custom_data=kwargs.get('custom_data', {})
            )
            
            # Validate dependencies
            for dep in metadata.dependencies:
                if dep not in self.components:
                    print(f"[REGISTRY] Warning: Dependency {dep} not found for {component_id}")
            
            # Store component
            self.components[component_id] = metadata
            self.components_by_type[component_type].add(component_id)
            
            # Store instance reference (weak ref to avoid circular references)
            if instance is not None:
                try:
                    self.component_instances[component_id] = weakref.ref(instance)
                except TypeError:
                    # Some objects don't support weak references
                    self.component_instances[component_id] = instance
            
            # Update capability mapping
            for capability in metadata.capabilities:
                self.components_by_capability[capability].add(component_id)
                
                # Auto-route first component with capability
                if capability not in self.service_routes:
                    self.service_routes[capability] = component_id
            
            # Add to rhizome network
            self.rhizome.add_node(component_id, {
                'name': name,
                'type': component_type.value,
                'metadata': metadata
            })
            
            # Connect dependencies in rhizome
            for dep in metadata.dependencies:
                if dep in self.components:
                    self.rhizome.connect(component_id, dep)
                    self.dependency_graph[component_id].add(dep)
            
            # Set status to active
            metadata.status = ComponentStatus.ACTIVE
            
            # Fire registration event
            self._fire_event('registered', component_id, {
                'name': name,
                'type': component_type.value,
                'capabilities': metadata.capabilities
            })
            
            print(f"[REGISTRY] Registered {name} ({component_id}) as {component_type.value}")
            return True
    
    def unregister(self, component_id: str) -> bool:
        """Unregister a component from the registry"""
        with self.lock:
            if component_id not in self.components:
                return False
            
            metadata = self.components[component_id]
            
            # Update status
            metadata.status = ComponentStatus.SHUTDOWN
            
            # Remove from type mapping
            self.components_by_type[metadata.component_type].discard(component_id)
            
            # Remove from capability mapping
            for capability in metadata.capabilities:
                self.components_by_capability[capability].discard(component_id)
                
                # Re-route capability if this was the primary provider
                if self.service_routes.get(capability) == component_id:
                    # Find alternative provider
                    alternatives = self.components_by_capability[capability]
                    if alternatives:
                        self.service_routes[capability] = next(iter(alternatives))
                    else:
                        del self.service_routes[capability]
            
            # Remove from dependency graph
            del self.dependency_graph[component_id]
            for deps in self.dependency_graph.values():
                deps.discard(component_id)
            
            # Remove instance reference
            if component_id in self.component_instances:
                del self.component_instances[component_id]
            
            # Fire event before removal
            self._fire_event('unregistered', component_id, {
                'name': metadata.name,
                'type': metadata.component_type.value
            })
            
            # Remove from registry
            del self.components[component_id]
            
            print(f"[REGISTRY] Unregistered {metadata.name} ({component_id})")
            return True
    
    def get_component(self, component_id: str) -> Optional[ComponentMetadata]:
        """Get component metadata by ID"""
        return self.components.get(component_id)
    
    def get_instance(self, component_id: str) -> Optional[Any]:
        """Get component instance by ID"""
        ref = self.component_instances.get(component_id)
        if ref is None:
            return None
        
        # Handle weak references
        if isinstance(ref, weakref.ref):
            instance = ref()
            if instance is None:
                # Instance was garbage collected
                del self.component_instances[component_id]
            return instance
        else:
            return ref
    
    def find_components(self, 
                       component_type: Optional[ComponentType] = None,
                       capability: Optional[str] = None,
                       status: Optional[ComponentStatus] = None) -> List[str]:
        """Find components matching criteria"""
        with self.lock:
            results = set(self.components.keys())
            
            # Filter by type
            if component_type is not None:
                results &= self.components_by_type[component_type]
            
            # Filter by capability
            if capability is not None:
                results &= self.components_by_capability[capability]
            
            # Filter by status
            if status is not None:
                results = {
                    cid for cid in results 
                    if self.components[cid].status == status
                }
            
            return list(results)
    
    def get_provider(self, capability: str) -> Optional[str]:
        """Get the primary provider for a capability"""
        return self.service_routes.get(capability)
    
    def update_status(self, component_id: str, status: ComponentStatus, error: Optional[str] = None):
        """Update component status"""
        with self.lock:
            if component_id not in self.components:
                return
            
            metadata = self.components[component_id]
            old_status = metadata.status
            metadata.status = status
            metadata.last_activity = time.time()
            
            if status == ComponentStatus.ERROR and error:
                metadata.error_count += 1
                metadata.metrics['last_error'] = error
            
            # Fire status change event
            if old_status != status:
                self._fire_event('status_change', component_id, {
                    'old_status': old_status.value,
                    'new_status': status.value,
                    'error': error
                })
    
    def update_metrics(self, component_id: str, metrics: Dict[str, Any]):
        """Update component metrics"""
        with self.lock:
            if component_id in self.components:
                self.components[component_id].metrics.update(metrics)
                self.components[component_id].last_activity = time.time()
    
    def connect_components(self, component1: str, component2: str, connection_type: str = "default"):
        """Create a connection between two components"""
        with self.lock:
            if component1 not in self.components or component2 not in self.components:
                return False
            
            # Add rhizome connection
            self.rhizome.connect(component1, component2)
            
            # Fire connection event
            self._fire_event('connected', component1, {
                'target': component2,
                'connection_type': connection_type
            })
            
            return True
    
    def subscribe_to_events(self, event_type: str, handler: Callable):
        """Subscribe to registry events"""
        with self.lock:
            self.event_handlers[event_type].append(handler)
    
    def broadcast(self, channel: str, message: Any, sender_id: Optional[str] = None):
        """Broadcast a message to all subscribers of a channel"""
        with self.lock:
            subscribers = self.broadcast_channels.get(channel, set())
            
            for subscriber_id in subscribers:
                if subscriber_id == sender_id:
                    continue  # Don't send to self
                
                instance = self.get_instance(subscriber_id)
                if instance and hasattr(instance, 'receive_broadcast'):
                    try:
                        instance.receive_broadcast(channel, message, sender_id)
                    except Exception as e:
                        print(f"[REGISTRY] Broadcast error for {subscriber_id}: {e}")
    
    def subscribe_to_channel(self, component_id: str, channel: str):
        """Subscribe a component to a broadcast channel"""
        with self.lock:
            self.broadcast_channels[channel].add(component_id)
    
    def register_health_check(self, component_id: str, check_function: Callable):
        """Register a health check function for a component"""
        with self.lock:
            self.health_checks[component_id] = check_function
    
    def _fire_event(self, event_type: str, component_id: str, details: Dict[str, Any]):
        """Fire a registry event"""
        event = RegistryEvent(
            event_type=event_type,
            component_id=component_id,
            timestamp=time.time(),
            details=details
        )
        
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_event_history:
            self.event_history.pop(0)
        
        # Call handlers
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"[REGISTRY] Event handler error: {e}")
    
    def _start_health_monitor(self):
        """Start background health monitoring"""
        def monitor():
            while True:
                time.sleep(self.health_check_interval)
                self._run_health_checks()
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def _run_health_checks(self):
        """Run health checks for all components"""
        with self.lock:
            for component_id, check_function in self.health_checks.items():
                if component_id not in self.components:
                    continue
                
                try:
                    health_status = check_function()
                    if not health_status:
                        self.update_status(component_id, ComponentStatus.ERROR, "Health check failed")
                except Exception as e:
                    self.update_status(component_id, ComponentStatus.ERROR, str(e))
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get comprehensive registry statistics"""
        with self.lock:
            type_counts = {
                ct.value: len(self.components_by_type[ct]) 
                for ct in ComponentType
            }
            
            status_counts = defaultdict(int)
            for component in self.components.values():
                status_counts[component.status.value] += 1
            
            return {
                'total_components': len(self.components),
                'components_by_type': type_counts,
                'components_by_status': dict(status_counts),
                'total_capabilities': len(self.service_routes),
                'total_connections': sum(
                    len(self.rhizome.get_connections(cid)) 
                    for cid in self.components
                ),
                'active_channels': len(self.broadcast_channels),
                'recent_events': len(self.event_history),
                'health_checks_registered': len(self.health_checks)
            }
    
    def export_graph(self) -> Dict[str, Any]:
        """Export the component graph for visualization"""
        with self.lock:
            nodes = []
            edges = []
            
            for component_id, metadata in self.components.items():
                nodes.append({
                    'id': component_id,
                    'label': metadata.name,
                    'type': metadata.component_type.value,
                    'status': metadata.status.value,
                    'capabilities': metadata.capabilities
                })
                
                # Add edges from rhizome connections
                for connected_id in self.rhizome.get_connections(component_id):
                    if connected_id in self.components:  # Ensure both nodes exist
                        edges.append({
                            'source': component_id,
                            'target': connected_id,
                            'type': 'rhizome'
                        })
            
            return {
                'nodes': nodes,
                'edges': edges,
                'stats': self.get_registry_stats()
            }

# Global registry instances
rhizome = RhizomeMap()
registry = SchemaRegistry()

# Convenience functions for backward compatibility
def register_component(component_id: str, name: str, component_type: str = "module", **kwargs):
    """Legacy registration function"""
    try:
        comp_type = ComponentType[component_type.upper()]
    except KeyError:
        comp_type = ComponentType.CUSTOM
    
    return registry.register(component_id, name, comp_type, **kwargs)

def get_component(component_id: str):
    """Legacy component getter"""
    return registry.get_component(component_id)

def connect(component1: str, component2: str):
    """Legacy connection function"""
    return registry.connect_components(component1, component2)

# Auto-register core components
def _register_core_components():
    """Register DAWN's core components"""
    core_components = [
        ("core.scup", "SCUP System", ComponentType.MODULE, ["calculate_scup", "monitor_coherence"]),
        ("core.shi", "Schema Health Index", ComponentType.MODULE, ["calculate_health", "monitor_schema"]),
        ("core.climate", "Schema Climate", ComponentType.MODULE, ["manage_weather", "nutrient_dynamics"]),
        ("core.anomaly_logger", "Anomaly Logger", ComponentType.MODULE, ["log_anomalies", "pattern_detection"]),
        ("consciousness.engine", "Consciousness Engine", ComponentType.PROCESSOR, ["process_consciousness", "tick_generation"])
    ]
    
    for comp_id, name, comp_type, capabilities in core_components:
        registry.register(
            component_id=comp_id,
            name=name,
            component_type=comp_type,
            capabilities=capabilities,
            version="2.0.0"
        )

# Initialize core components on import
_register_core_components()