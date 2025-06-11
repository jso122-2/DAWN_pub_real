# Bloom System Directory

## Last Cleaned: 2025-06-05 15:25:49

This directory contains the consolidated bloom system for DAWN.

## Current Structure:

### Core Systems:
- `unified_bloom_engine.py` - Main bloom engine with mycelium integration
- `bloom_memory_system.py` - Unified memory management
- `bloom_spawner.py` - Enhanced bloom spawning with fractal generation

### Integration Systems:
- `bloom_integration_system.py` - Integration with other DAWN components
- `bloom_maintenance_system.py` - System maintenance and health checks
- `bloom_visualization_system.py` - Visualization and analysis tools

### Data Directories:
- `bloom_core/` - Core bloom data and configurations
- `memory_blooms/` - Stored bloom memories

## Archived Files:

Old and redundant files have been moved to:
`C:\Users\Admin\Documents\DAWN_Vault\Tick_engine\archive\bloom_cleanup_20250605_152543`

See the cleanup report in the archive for details on what was moved.

## Usage:

```python
from bloom.unified_bloom_engine import BloomEngine
from bloom.bloom_spawner import spawn_bloom
from bloom.bloom_memory_system import BloomMemoryManager

# Initialize the bloom engine
engine = BloomEngine()
engine.initialize()

# Spawn a bloom
bloom_data = {
    "seed_id": "example_001",
    "mood": "curious",
    "lineage_depth": 1,
    "bloom_factor": 1.5,
    "entropy_score": 0.7
}
result = spawn_bloom(bloom_data)
```