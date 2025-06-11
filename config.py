#!/usr/bin/env python3
"""
DAWN Tick Engine - Boot Configuration Module
===========================================
This module contains all configuration parameters for the DAWN Tick Engine,
including boot sequences, system thresholds, safety mechanisms, and runtime parameters.
"""

import os
from datetime import datetime
from typing import Dict, List, Union, Any

# Environment detection
ENVIRONMENT = os.getenv("DAWN_ENV", "production")
DEBUG_MODE = os.getenv("DAWN_DEBUG", "false").lower() == "true"

# Core Boot Sequence Configuration
BOOT_SEQUENCE = {
    # Core Systems (Priority 1)
    "thermal_core": {
        "enabled": True,
        "priority": 1,
        "timeout": 5.0,
        "dependencies": [],
        "params": {
            "initial_temp": 20.0,
            "target_temp": 37.0,
            "ramp_rate": 2.0
        }
    },
    "pulse_engine": {
        "enabled": True,
        "priority": 1,
        "timeout": 3.0,
        "dependencies": ["thermal_core"],
        "params": {
            "base_frequency": 60,
            "variance": 5,
            "sync_mode": "adaptive"
        }
    },
    
    # Memory and Processing (Priority 2)
    "memory_matrix": {
        "enabled": True,
        "priority": 2,
        "timeout": 10.0,
        "dependencies": ["pulse_engine"],
        "params": {
            "initial_allocation": "2GB",
            "max_allocation": "16GB",
            "fragmentation_threshold": 0.15,
            "gc_interval": 300
        }
    },
    "consciousness_layer": {
        "enabled": True,
        "priority": 2,
        "timeout": 15.0,
        "dependencies": ["memory_matrix", "neural_network"],
        "params": {
            "awareness_level": 0.0,
            "target_awareness": 1.0,
            "integration_rate": 0.1
        }
    },
    
    # Neural Systems (Priority 3)
    "neural_network": {
        "enabled": True,
        "priority": 3,
        "timeout": 20.0,
        "dependencies": ["memory_matrix"],
        "params": {
            "layers": [64, 128, 256, 512, 256, 128, 64],
            "activation": "relu",
            "dropout": 0.2,
            "learning_rate": 0.001
        }
    },
    
    # Interface Systems (Priority 4)
    "sensory_interface": {
        "enabled": True,
        "priority": 4,
        "timeout": 5.0,
        "dependencies": ["neural_network"],
        "params": {
            "channels": ["visual", "auditory", "haptic", "proprioceptive"],
            "sampling_rate": 1000,
            "buffer_size": 4096
        }
    },
    "motor_control": {
        "enabled": True,
        "priority": 4,
        "timeout": 5.0,
        "dependencies": ["neural_network", "reflex_arcs"],
        "params": {
            "precision_mode": "high",
            "feedback_loop": True,
            "max_torque": 100.0
        }
    },
    
    # Auxiliary Systems (Priority 5)
    "reflex_arcs": {
        "enabled": True,
        "priority": 5,
        "timeout": 2.0,
        "dependencies": ["sensory_interface"],
        "params": {
            "response_time": 0.05,
            "threshold_multiplier": 0.8
        }
    },
    "diagnostic_system": {
        "enabled": True,
        "priority": 5,
        "timeout": 3.0,
        "dependencies": [],
        "params": {
            "scan_interval": 60,
            "log_level": "INFO",
            "metrics_enabled": True
        }
    },
    "adaptive_learning": {
        "enabled": True,
        "priority": 6,
        "timeout": 10.0,
        "dependencies": ["consciousness_layer", "neural_network"],
        "params": {
            "learning_enabled": True,
            "experience_buffer": 10000,
            "consolidation_interval": 3600
        }
    }
}

# System Thresholds and Limits
THRESHOLDS = {
    # Physical Parameters
    "pressure": {
        "min": 0.0,
        "max": 1.0,
        "warning": 0.85,
        "critical": 0.95,
        "unit": "bar"
    },
    "temperature": {
        "min": -10.0,
        "max": 50.0,
        "warning": 45.0,
        "critical": 48.0,
        "unit": "celsius"
    },
    
    # Performance Metrics
    "cpu_usage": {
        "min": 0.0,
        "max": 100.0,
        "warning": 80.0,
        "critical": 95.0,
        "unit": "percent"
    },
    "memory_usage": {
        "min": 0.0,
        "max": 100.0,
        "warning": 85.0,
        "critical": 95.0,
        "unit": "percent"
    },
    "response_time": {
        "min": 0.0,
        "max": 1000.0,
        "warning": 500.0,
        "critical": 800.0,
        "unit": "ms"
    },
    
    # Neural Activity
    "neural_activity": {
        "min": 0.0,
        "max": 1.0,
        "warning": 0.9,
        "critical": 0.95,
        "unit": "normalized"
    },
    "consciousness_coherence": {
        "min": 0.0,
        "max": 1.0,
        "warning": 0.3,
        "critical": 0.2,
        "unit": "index"
    }
}

# Safety and Security Configuration
SAFETY_CHECKS = {
    # Core Safety
    "enable_pressure_check": True,
    "enable_temp_check": True,
    "enable_overload_protection": True,
    "enable_emergency_shutdown": True,
    "allow_override": False,
    
    # System Integrity
    "checksum_validation": True,
    "memory_protection": True,
    "stack_canaries": True,
    "heap_guard": True,
    
    # Operational Safety
    "watchdog_timer": {
        "enabled": True,
        "timeout": 30.0,
        "action": "restart"
    },
    "deadlock_detection": {
        "enabled": True,
        "timeout": 60.0,
        "max_retries": 3
    },
    "resource_limits": {
        "max_threads": 1000,
        "max_file_descriptors": 10000,
        "max_memory_per_process": "4GB"
    }
}

# Runtime Configuration
RUNTIME_CONFIG = {
    "tick_rate": 20,  # Hz
    "frame_interpolation": True,
    "async_operations": True,
    "thread_pool_size": 8,
    "event_queue_size": 10000,
    
    "networking": {
        "enabled": True,
        "port": 8080,
        "max_connections": 1000,
        "timeout": 30.0,
        "buffer_size": 65536
    },
    
    "persistence": {
        "enabled": True,
        "save_interval": 300,
        "backup_count": 5,
        "compression": "lz4",
        "encryption": "aes256"
    },
    
    "monitoring": {
        "metrics_enabled": True,
        "metrics_interval": 60,
        "telemetry_enabled": True,
        "profiling_enabled": DEBUG_MODE,
        "trace_level": "INFO" if not DEBUG_MODE else "DEBUG"
    }
}

# Feature Flags
FEATURES = {
    "experimental_quantum_layer": False,
    "advanced_prediction": True,
    "multi_dimensional_processing": False,
    "temporal_coherence": True,
    "emotional_synthesis": True,
    "dream_state_simulation": False,
    "collective_consciousness": False,
    "reality_anchoring": True
}

# Performance Tuning
PERFORMANCE = {
    "cache_sizes": {
        "l1_cache": "64KB",
        "l2_cache": "512KB",
        "l3_cache": "8MB"
    },
    "optimization_level": "O3" if not DEBUG_MODE else "O0",
    "vectorization": True,
    "prefetching": True,
    "numa_aware": True,
    "gpu_acceleration": {
        "enabled": True,
        "device_id": 0,
        "memory_fraction": 0.8
    }
}

# System Metadata
SYSTEM_METADATA = {
    "version": "1.0.0",
    "build": datetime.now().strftime("%Y-%m-%d"),
    "build_number": os.getenv("BUILD_NUMBER", "local"),
    "git_commit": os.getenv("GIT_COMMIT", "unknown"),
    "author": "root",
    "maintainers": ["root", "system"],
    "environment": ENVIRONMENT,
    "platform": os.name,
    "architecture": os.uname().machine if hasattr(os, 'uname') else "unknown",
    "capabilities": [
        "neural_processing",
        "adaptive_learning",
        "real_time_response",
        "distributed_computation",
        "quantum_ready"
    ]
}

# Logging Configuration
LOGGING = {
    "level": "DEBUG" if DEBUG_MODE else "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
        "console": {
            "enabled": True,
            "colored": True
        },
        "file": {
            "enabled": True,
            "path": "logs/engine.log",
            "rotation": "daily",
            "retention": 30
        },
        "syslog": {
            "enabled": ENVIRONMENT == "production",
            "facility": "local0"
        }
    }
}

# API Configuration
API_CONFIG = {
    "version": "v1",
    "base_path": "/api",
    "rate_limiting": {
        "enabled": True,
        "requests_per_minute": 60,
        "burst_size": 10
    },
    "authentication": {
        "enabled": True,
        "type": "bearer",
        "token_expiry": 3600
    },
    "cors": {
        "enabled": True,
        "origins": ["*"] if DEBUG_MODE else ["https://dawn.local"]
    }
}

# Cluster Configuration (for distributed deployment)
CLUSTER_CONFIG = {
    "enabled": False,
    "node_id": os.getenv("NODE_ID", "dawn-01"),
    "cluster_size": 1,
    "heartbeat_interval": 5.0,
    "election_timeout": 15.0,
    "replication_factor": 3,
    "sharding": {
        "enabled": False,
        "strategy": "consistent_hash",
        "shard_count": 16
    }
}

# Helper Functions
def get_boot_order() -> List[str]:
    """Get ordered list of components to boot based on priority and dependencies."""
    components = []
    for name, config in sorted(BOOT_SEQUENCE.items(), 
                              key=lambda x: x[1].get("priority", 99)):
        if config.get("enabled", True):
            components.append(name)
    return components

def validate_config() -> Dict[str, Any]:
    """Validate configuration integrity."""
    issues = []
    
    # Check boot sequence dependencies
    for name, config in BOOT_SEQUENCE.items():
        for dep in config.get("dependencies", []):
            if dep not in BOOT_SEQUENCE:
                issues.append(f"Unknown dependency '{dep}' for component '{name}'")
    
    # Check threshold ranges
    for param, thresholds in THRESHOLDS.items():
        if thresholds["min"] >= thresholds["max"]:
            issues.append(f"Invalid threshold range for '{param}'")
        if thresholds["warning"] >= thresholds["critical"]:
            issues.append(f"Warning threshold >= critical for '{param}'")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "timestamp": datetime.now().isoformat()
    }

# Configuration export
__all__ = [
    "BOOT_SEQUENCE",
    "THRESHOLDS", 
    "SAFETY_CHECKS",
    "RUNTIME_CONFIG",
    "FEATURES",
    "PERFORMANCE",
    "SYSTEM_METADATA",
    "LOGGING",
    "API_CONFIG",
    "CLUSTER_CONFIG",
    "get_boot_order",
    "validate_config",
    "ENVIRONMENT",
    "DEBUG_MODE"
] 