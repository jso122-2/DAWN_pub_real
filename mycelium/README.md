# Mycelium - DAWN Biological Network Substrate

## Architecture Overview

The Mycelium system serves as DAWN's **biological network substrate** - a living, adaptive network layer that connects consciousness components through underground mycelial connections. Inspired by fungal networks in nature, it enables resource sharing, emergent communication, and distributed intelligence across the consciousness ecosystem.

## Core Philosophy

> "Like fungal networks in a forest, this layer connects blooms, shares nutrients (information), and enables emergent communication."

The Mycelium system implements **biological network intelligence**:
- **Living Substrate**: Network grows, adapts, and evolves naturally
- **Nutrient Flow**: Information and resources flow like nutrients through mycelial threads
- **Emergent Connectivity**: Connections form organically based on need and proximity
- **Network Intelligence**: Collective behavior emerges from distributed processing
- **Adaptive Growth**: Network topology evolves based on usage patterns

## Core Components

### Mycelium Layer (`mycelium_layer.py` - 8.8KB)
**Purpose**: Primary mycelial network implementation with growth and nutrient management

**Key Features**:
- Dynamic root network growth and connection management
- Nutrient flow simulation and distribution algorithms
- Network pathfinding and route optimization
- Health monitoring and decay processes
- Network visualization and analysis tools

```python
from mycelium.mycelium_layer import MyceliumLayer

# Initialize mycelial substrate
layer = MyceliumLayer()

# Grow network connections
growth_result = layer.grow(source="consciousness_core")
print(f"New root: {growth_result['new_root']}")

# Share nutrients across network
distributed = layer.share_nutrients("semantic_processing", amount=0.5)
print(f"Nutrients distributed to: {list(distributed.keys())}")
```

### Spore System (`spore.py`)
**Purpose**: Network propagation and seeding mechanisms

**Features**:
- Spore generation for network expansion
- Cross-component communication seeding
- Adaptive spore distribution algorithms
- Spore lifecycle management
- Network diversification through spore propagation

```python
from mycelium.spore import create_spore, propagate_spores

# Create consciousness spore
spore = create_spore(
    type="consciousness_seed",
    payload={"emotion": "curious", "intensity": 0.7},
    target_networks=["mood", "visual", "memory"]
)

# Propagate across network
propagate_spores([spore], mycelium_layer)
```

### Network Management (`network.py`)
**Purpose**: High-level network coordination and management

**Features**:
- Network topology management
- Connection quality monitoring
- Resource allocation coordination
- Network performance optimization
- Cross-layer communication protocols

```python
from mycelium.network import NetworkManager

# Initialize network management
manager = NetworkManager(mycelium_layer)
manager.optimize_connections()
manager.balance_resource_flow()

# Monitor network health
health_metrics = manager.get_health_metrics()
```

## Network Architecture

### Root Network Structure
```python
mycelium_roots = {
    "seed://init": {
        "type": "primary",           # Primary consciousness root
        "connections": set(),        # Connected roots
        "nutrients": 1.0,           # Available nutrients
        "depth": 0                  # Network depth level
    },
    "root://secondary_001": {
        "type": "secondary",         # Secondary processing root
        "connections": {"seed://init"},
        "nutrients": 0.5,
        "depth": 1
    }
}
```

### Nutrient Flow Model
```
Primary Root (nutrients: 1.0)
       ↓ (30% distribution)
Secondary Roots (nutrients: 0.3 each)
       ↓ (nutrient sharing)
Tertiary Connections (nutrients: 0.1 each)
       ↓ (decay over time)
Network Maintenance (cleanup < 0.001)
```

### Connection Patterns
- **Bidirectional Links**: All connections support two-way communication
- **Nutrient Sharing**: Connected roots share resources automatically
- **Growth Triggers**: High nutrient levels trigger new root generation
- **Natural Decay**: Unused connections naturally weaken over time

## Biological Network Features

### Growth Mechanics
```python
# Natural network growth
def grow_network(source_root):
    growth_potential = nutrient_level * growth_rate
    
    if growth_potential > threshold and random() < growth_potential:
        # Create new root with inherited characteristics
        new_root = create_secondary_root(
            parent=source_root,
            nutrients=growth_potential,
            depth=parent_depth + 1
        )
        
        # Establish bidirectional connection
        connect_roots(source_root, new_root)
        
        return new_root
```

### Nutrient Distribution
```python
# Biological nutrient sharing
def share_nutrients(source, amount):
    # Add nutrients to source
    source.nutrients += amount
    
    # Distribute to connected roots (30% shared)
    connections = get_connections(source)
    share_amount = amount * 0.3 / len(connections)
    
    for connected_root in connections:
        connected_root.nutrients += share_amount
        
    return distribution_map
```

### Pathfinding Algorithm
```python
# Mycelial pathfinding (BFS-based)
def find_mycelial_path(start, end):
    visited = {start}
    queue = [(start, [start])]
    
    while queue:
        current, path = queue.pop(0)
        
        if current == end:
            return path  # Found mycelial route
            
        for neighbor in get_connections(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                
    return None  # No mycelial connection exists
```

## Network Health & Maintenance

### Health Monitoring
```python
# Comprehensive network health assessment
def get_network_health():
    return {
        "total_roots": len(active_roots),
        "total_connections": count_connections(),
        "max_depth": max(root.depth for root in roots),
        "total_nutrients": sum(root.nutrients for root in roots),
        "growth_rate": current_growth_rate,
        "connectivity_index": calculate_connectivity()
    }
```

### Natural Decay Process
```python
# Biological decay simulation
def apply_network_decay(decay_rate=0.01):
    for root in all_roots:
        root.nutrients *= (1 - decay_rate)
        
    # Remove roots with insufficient nutrients
    dead_roots = find_roots_below_threshold(0.001)
    for dead_root in dead_roots:
        if dead_root != primary_root:  # Preserve primary root
            remove_root_safely(dead_root)
```

### Adaptive Optimization
- **Connection Strengthening**: Frequently used paths get stronger
- **Weak Link Pruning**: Unused connections are naturally removed
- **Resource Rebalancing**: Nutrients flow to high-activity areas
- **Growth Direction**: New connections form toward active components

## Integration Patterns

### Consciousness Component Integration
```python
# Connect consciousness component to mycelial network
def integrate_component(component, network_role):
    # Create dedicated root for component
    component_root = create_component_root(
        component_id=component.id,
        resource_needs=component.get_resource_requirements(),
        communication_endpoints=component.get_endpoints()
    )
    
    # Establish mycelial connections
    connect_to_network(component_root, existing_network)
    
    # Begin nutrient flow
    start_nutrient_flow(component_root)
```

### Cross-System Communication
```python
# Send message through mycelial network
def send_mycelial_message(source, target, message):
    path = find_mycelial_path(source, target)
    
    if path:
        # Route message along mycelial connections
        for hop in path:
            process_message_hop(message, hop)
            
        deliver_message(target, message)
        return True
    
    return False  # No mycelial route available
```

### Resource Coordination
```python
# Coordinate resources across consciousness systems
def coordinate_resources(resource_type, demand_map):
    # Find roots with surplus resources
    surplus_roots = find_surplus_roots(resource_type)
    
    # Find roots with resource needs
    deficit_roots = find_deficit_roots(resource_type, demand_map)
    
    # Create mycelial flow paths
    for surplus in surplus_roots:
        for deficit in deficit_roots:
            path = find_mycelial_path(surplus, deficit)
            if path:
                transfer_resources(surplus, deficit, path, resource_type)
```

## Performance & Monitoring

### Network Metrics
- **Connection Density**: Ratio of actual to possible connections
- **Nutrient Flow Rate**: Resources distributed per time unit
- **Path Efficiency**: Average path length between components
- **Growth Velocity**: Rate of new connection formation
- **Health Score**: Overall network vitality assessment

### Diagnostic Tools
```python
# Network visualization
visualization = layer.visualize_network()
print(visualization)  # ASCII art network representation

# Performance analysis
stats = layer.get_network_stats()
print(f"Network efficiency: {calculate_efficiency(stats)}")

# Connection quality assessment
quality_report = assess_connection_quality(layer)
```

### Adaptive Tuning
```python
# Automatic network optimization
def optimize_mycelial_network():
    # Strengthen high-traffic paths
    strengthen_active_connections()
    
    # Prune weak or unused connections
    prune_weak_connections(threshold=0.001)
    
    # Rebalance nutrient distribution
    rebalance_nutrients()
    
    # Encourage growth in underconnected areas
    boost_growth_in_sparse_regions()
```

## Configuration & Usage

### Basic Network Setup
```python
from mycelium import get_mycelium, initialize_mycelial_substrate

# Get global mycelium instance
mycelium = get_mycelium()

# Initialize with consciousness components
initialize_mycelial_substrate([
    "consciousness_core",
    "mood_engine", 
    "memory_system",
    "visual_processor"
])
```

### Advanced Configuration
```python
# Custom mycelium configuration
mycelium_config = {
    "growth_rate": 0.15,        # Network expansion rate
    "decay_rate": 0.005,        # Natural decay rate
    "sharing_ratio": 0.3,       # Nutrient sharing percentage
    "depth_limit": 10,          # Maximum network depth
    "connection_threshold": 0.1  # Minimum nutrients for connections
}

layer = MyceliumLayer(**mycelium_config)
```

## Architecture Philosophy

The Mycelium system embodies DAWN's **biological network intelligence** principles:

- **Living Networks**: Infrastructure that grows, adapts, and evolves
- **Organic Resource Flow**: Nutrients flow where needed, when needed
- **Emergent Intelligence**: Network behavior emerges from simple rules
- **Adaptive Resilience**: Self-healing and self-optimizing capabilities
- **Biological Mimicry**: Learning from nature's most successful networks

## Dependencies

### Core Dependencies
- `typing` - Type hints for network structures
- `datetime` - Temporal tracking of network events
- `random` - Natural growth variation simulation

### System Integration
- `network.router` - Higher-level routing coordination
- `core.consciousness` - Primary consciousness integration
- `bloom.bloom_spawner` - Bloom system nutrient coordination

## Future Evolution

### Planned Enhancements
- **Mycelial Learning**: Network topology learns from usage patterns
- **Seasonal Cycles**: Growth and dormancy cycles for resource optimization
- **Spore Networks**: Long-distance communication through spore propagation
- **Symbiotic Relationships**: Beneficial partnerships between network components

The Mycelium system creates the **living substrate** that enables DAWN's consciousness components to communicate, share resources, and coordinate behaviors through a biologically-inspired network that grows, adapts, and evolves naturally over time. 