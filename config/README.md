# Config - DAWN Configuration Management System

## Architecture Overview

The Config system provides **comprehensive configuration management** for DAWN's consciousness ecosystem. From central system configuration and YAML-based component settings to advanced UI configuration tools and environment management, this system ensures consistent, maintainable, and flexible configuration across all consciousness components.

## Core Philosophy

The Config system embodies **configuration-as-code principles**:
- **Centralized Management**: Single source of truth for system configuration
- **Environment Awareness**: Different configurations for development, testing, and production
- **Type Safety**: Validated configuration with proper type checking
- **Hot Reloading**: Dynamic configuration updates without system restart
- **UI Configuration**: Advanced user interface for configuration management

## Core Components

### Central Configuration (`config.py` - 11KB)
**Purpose**: Master configuration module with boot sequences, thresholds, and safety mechanisms

**Key Features**:
- **Boot Sequence Configuration**: Multi-priority component startup orchestration
- **System Thresholds**: Performance and safety limits for all components
- **Safety Checks**: Comprehensive safety and security validation
- **Environment Detection**: Automatic environment configuration
- **Dynamic Validation**: Runtime configuration validation and enforcement

```python
from config.config import BOOT_SEQUENCE, THRESHOLDS, SAFETY_CHECKS

# Boot sequence with priorities and dependencies
BOOT_SEQUENCE = {
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
    }
}

# System thresholds and limits
THRESHOLDS = {
    "consciousness_coherence": {
        "min": 0.0,
        "max": 1.0,
        "warning": 0.3,
        "critical": 0.2,
        "unit": "index"
    }
}
```

### DAWN Configuration (`dawn_config.json` - 2.8KB)
**Purpose**: JSON-based central system configuration with component settings

**Configuration Sections**:
- **System Parameters**: Core system operational parameters
- **Component Settings**: Individual component configuration
- **Performance Tuning**: Optimization and performance settings
- **Integration Settings**: Cross-component communication configuration
- **Debug and Logging**: Development and monitoring configuration

```json
{
  "system": {
    "environment": "production",
    "debug_mode": false,
    "log_level": "INFO",
    "max_memory_usage": "16GB"
  },
  "consciousness": {
    "default_emotion": "curious",
    "awareness_threshold": 0.7,
    "integration_rate": 0.1,
    "coherence_target": 0.8
  },
  "networking": {
    "websocket_port": 8000,
    "max_connections": 100,
    "heartbeat_interval": 30
  }
}
```

### Component Configurations

#### Tick Configuration (`tick_config.yaml` - 1.6KB)
**Purpose**: Tick engine timing and processing configuration

```yaml
# Tick engine configuration
tick_engine:
  base_frequency: 60  # Base ticks per second
  adaptive_scaling: true
  max_frequency: 120
  min_frequency: 10
  
performance:
  cpu_threshold: 80
  memory_threshold: 85
  auto_scaling: true
  
monitoring:
  metrics_enabled: true
  logging_level: "INFO"
  telemetry_interval: 5
```

#### Pulse Configuration (`pulse_config.yaml` - 1.3KB)
**Purpose**: Pulse system thermal and rhythm configuration

```yaml
# Pulse system configuration
pulse_system:
  thermal:
    target_temperature: 37.0
    variance_tolerance: 0.5
    cooling_rate: 0.1
    heating_rate: 0.05
    
  rhythm:
    base_pulse: 60  # BPM
    variability: 5
    adaptation_rate: 0.1
    
safety:
  max_temperature: 50.0
  min_temperature: 20.0
  emergency_cooling: true
```

#### Routing Configuration (`routing_config.yaml` - 888B)
**Purpose**: Network routing and communication configuration

```yaml
# Network routing configuration
routing:
  default_timeout: 5.0
  retry_attempts: 3
  circuit_breaker_threshold: 0.5
  
endpoints:
  consciousness: "/consciousness"
  metrics: "/metrics" 
  health: "/health"
  
load_balancing:
  enabled: true
  algorithm: "round_robin"
  health_checks: true
```

### UI Configuration Tools

#### Tiling Configuration UI (`TilingConfigUI.tsx` - 2.7KB)
**Purpose**: Advanced window management and layout configuration interface

**Features**:
- **Window Layout Management**: Dynamic window arrangement and tiling
- **Consciousness Workspace**: Specialized layouts for consciousness monitoring
- **Responsive Design**: Adaptive layouts for different screen sizes
- **User Preferences**: Personalized workspace configuration
- **Real-Time Preview**: Live preview of configuration changes

```typescript
import { TilingConfigUI } from './config/TilingConfigUI';

// Advanced UI configuration
<TilingConfigUI
  layout="consciousness-dashboard"
  windows={['metrics', 'conversation', 'visualization']}
  onLayoutChange={handleLayoutChange}
  enableAutoSave={true}
/>
```

#### Tiling Aware Panel (`TilingAwarePanel.example.tsx` - 1.4KB)
**Purpose**: Smart panel component that adapts to tiling configurations

**Features**:
- **Auto-Resizing**: Panels that adapt to available space
- **Context Awareness**: Panels adjust content based on size constraints
- **Performance Optimization**: Efficient rendering for small panels
- **Interaction Adaptation**: Touch vs mouse interaction optimization

#### UI Mode Configuration (`uiMode.ts` - 7.5KB)
**Purpose**: Comprehensive UI mode and theme management

**Features**:
- **Theme Management**: Dark/light mode with consciousness aesthetics
- **Accessibility Modes**: High contrast and accessibility configurations
- **Performance Modes**: Reduced animation for low-performance devices
- **Layout Modes**: Different UI layouts for different use cases

```typescript
import { UIMode, setUIMode, getUIMode } from './config/uiMode';

// UI mode configuration
const uiConfig = {
  theme: 'consciousness-dark',
  animations: 'full',
  layout: 'dashboard',
  accessibility: {
    highContrast: false,
    reducedMotion: false,
    screenReader: false
  }
};

setUIMode(uiConfig);
```

### Environment & Platform Configuration

#### Electron Window Management (`electron-wm-bridge.js` - 2.9KB)
**Purpose**: Electron-specific window management and system integration

**Features**:
- **Native Window Controls**: Platform-native window management
- **System Tray Integration**: Background operation with system tray
- **Desktop Notifications**: Native OS notification integration
- **File System Access**: Secure file system operations
- **Auto-Updater**: Automatic application updates

#### Cursor Guard Configuration (`cursor_guard.yaml` - 977B)
**Purpose**: Development environment protection and automation

```yaml
# Cursor guard configuration
guard:
  auto_save_interval: 30  # seconds
  backup_frequency: 300   # seconds
  max_backups: 10
  
protection:
  file_monitoring: true
  change_detection: true
  conflict_resolution: "prompt"
  
automation:
  format_on_save: true
  lint_on_save: true
  test_on_change: false
```

## Configuration Architecture

### Hierarchical Configuration
```
Global Config (config.py)
├── Environment-Specific (.env files)
├── Component Configs (YAML files)
├── User Preferences (JSON files)
└── Runtime Overrides (API/UI)
```

### Configuration Loading Priority
1. **Runtime Overrides**: Highest priority, API or UI changes
2. **User Preferences**: User-specific settings and customizations
3. **Environment Variables**: Environment-specific overrides
4. **Component Configs**: YAML-based component settings
5. **Global Defaults**: Default values from config.py

### Type-Safe Configuration
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

@dataclass
class ConsciousnessConfig:
    default_emotion: str = "curious"
    awareness_threshold: float = 0.7
    integration_rate: float = 0.1
    coherence_target: float = 0.8
    
@dataclass 
class SystemConfig:
    environment: str = "development"
    debug_mode: bool = True
    log_level: str = "INFO"
    max_memory_usage: str = "8GB"
    
# Configuration validation
def validate_config(config: Dict) -> SystemConfig:
    return SystemConfig(**config)
```

## Dynamic Configuration Management

### Hot Reloading
```python
import watchdog
from config import reload_configuration

class ConfigWatcher:
    def __init__(self):
        self.observer = watchdog.observers.Observer()
        
    def on_config_change(self, event):
        if event.src_path.endswith('.yaml') or event.src_path.endswith('.json'):
            print(f"Reloading configuration: {event.src_path}")
            reload_configuration(event.src_path)
            
    def start_watching(self):
        self.observer.schedule(self, path='config/', recursive=True)
        self.observer.start()
```

### Configuration API
```python
from flask import Flask, request, jsonify
from config import get_config, update_config, validate_config

app = Flask(__name__)

@app.route('/config/<component>', methods=['GET'])
def get_component_config(component):
    config = get_config(component)
    return jsonify(config)

@app.route('/config/<component>', methods=['PUT'])
def update_component_config(component):
    new_config = request.json
    
    # Validate configuration
    if validate_config(component, new_config):
        update_config(component, new_config)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Invalid configuration"})
```

### UI Configuration Interface
```typescript
// Real-time configuration management
import { useConfig } from './hooks/useConfig';

function ConfigurationPanel() {
  const { config, updateConfig, isLoading } = useConfig('consciousness');
  
  const handleConfigChange = (key: string, value: any) => {
    updateConfig({
      ...config,
      [key]: value
    });
  };
  
  return (
    <div className="config-panel">
      <h2>Consciousness Configuration</h2>
      <ConfigSlider 
        label="Awareness Threshold"
        value={config.awareness_threshold}
        onChange={(value) => handleConfigChange('awareness_threshold', value)}
        min={0}
        max={1}
        step={0.1}
      />
      <ConfigSelect
        label="Default Emotion"
        value={config.default_emotion}
        onChange={(value) => handleConfigChange('default_emotion', value)}
        options={['curious', 'focused', 'creative', 'contemplative']}
      />
    </div>
  );
}
```

## Development & Production Patterns

### Environment-Specific Configuration
```python
import os
from dataclasses import dataclass

@dataclass
class EnvironmentConfig:
    def __post_init__(self):
        env = os.getenv('DAWN_ENV', 'development')
        
        if env == 'development':
            self.debug_mode = True
            self.log_level = 'DEBUG'
            self.enable_hot_reload = True
        elif env == 'production':
            self.debug_mode = False
            self.log_level = 'INFO'
            self.enable_hot_reload = False
        elif env == 'testing':
            self.debug_mode = True
            self.log_level = 'WARNING'
            self.mock_external_services = True
```

### Configuration Testing
```python
import unittest
from config import validate_config, load_config

class ConfigurationTests(unittest.TestCase):
    def test_default_configuration_valid(self):
        config = load_config('default')
        self.assertTrue(validate_config(config))
        
    def test_consciousness_config_ranges(self):
        config = load_config('consciousness')
        self.assertGreaterEqual(config['awareness_threshold'], 0.0)
        self.assertLessEqual(config['awareness_threshold'], 1.0)
        
    def test_configuration_hot_reload(self):
        # Test configuration reloading without restart
        original_config = get_config('pulse')
        update_config_file('pulse_config.yaml', {'target_temperature': 38.0})
        reload_configuration('pulse')
        updated_config = get_config('pulse')
        
        self.assertNotEqual(original_config, updated_config)
```

## Architecture Philosophy

The Config system embodies DAWN's **configuration management excellence** principles:

- **Single Source of Truth**: Centralized configuration with clear hierarchy
- **Type Safety**: Validated configuration with proper error handling
- **Dynamic Updates**: Hot reloading and runtime configuration changes
- **Environment Awareness**: Seamless configuration across different environments
- **User Experience**: Intuitive UI tools for configuration management

## Dependencies

### Core Dependencies
- **PyYAML**: YAML configuration file parsing
- **JSON**: Native JSON configuration support
- **Dataclasses**: Type-safe configuration structures
- **Watchdog**: File system monitoring for hot reloading

### UI Dependencies
- **React**: Configuration UI components
- **TypeScript**: Type-safe configuration interfaces
- **Electron**: Desktop application configuration management

### System Integration
- **Environment Variables**: System environment integration
- **File System**: Configuration file management
- **WebSocket**: Real-time configuration updates
- **Validation Libraries**: Configuration validation and type checking

The Config system provides the **configuration backbone** that enables DAWN's consciousness ecosystem to operate consistently across environments while providing flexible, user-friendly configuration management for both developers and end users. 