#!/usr/bin/env python3
"""
DAWN Renderer Integration
Connects the SigilRenderer to DAWN's core systems for live symbolic state visualization.
"""

import time
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    from ...sigil_renderer import SigilRenderer, create_terminal_renderer, create_minimal_renderer, UrgencyLevel
    from core.pulse_engine import PulseEngine
    from core.memory_router import MemoryRouter
    from core.sigil_manager import SigilManager
    DAWN_CORE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN core components not available: {e}")
    print("🔧 Using mock implementations for testing")
    DAWN_CORE_AVAILABLE = False
    
    # Import local sigil renderer
    from ...sigil_renderer import SigilRenderer, create_terminal_renderer, create_minimal_renderer, UrgencyLevel
    
    # Mock implementations
    class MockPulseEngine:
        def __init__(self):
            self.entropy = 0.5
            self.heat = 30.0
            self.zone = "ACTIVE"
            self.pulse_state = {'focus': 0.7, 'chaos': 0.3}
        
        def get_current_entropy(self): return self.entropy
        def get_pulse_heat(self): return self.heat
        def get_pulse_zone(self): return self.zone
    
    class MockMemoryRouter:
        def __init__(self):
            self.chunks = {}
        
        def get_chunk_count(self): return len(self.chunks)
    
    class MockSigilManager:
        def __init__(self):
            self.active_sigils = []
        
        def get_active_sigils(self): return self.active_sigils
    
    PulseEngine = MockPulseEngine
    MemoryRouter = MockMemoryRouter
    SigilManager = MockSigilManager


class DAWNRendererIntegration:
    """
    Integration layer between DAWN core systems and the sigil renderer.
    Provides live visualization of DAWN's symbolic cognitive state.
    """
    
    def __init__(self, 
                 pulse_engine: Optional[Any] = None,
                 memory_router: Optional[Any] = None,
                 sigil_manager: Optional[Any] = None,
                 use_minimal: bool = False,
                 auto_render: bool = True):
        """
        Initialize the renderer integration.
        
        Args:
            pulse_engine: DAWN pulse engine instance
            memory_router: DAWN memory router instance  
            sigil_manager: DAWN sigil manager instance
            use_minimal: Use minimal rendering mode
            auto_render: Enable automatic rendering on updates
        """
        # Initialize core components
        self.pulse_engine = pulse_engine or PulseEngine()
        self.memory_router = memory_router or MemoryRouter()
        self.sigil_manager = sigil_manager or SigilManager()
        
        # Create appropriate renderer
        if use_minimal:
            self.renderer = create_minimal_renderer()
        else:
            self.renderer = create_terminal_renderer()
        
        self.auto_render = auto_render
        self.last_update_time = 0.0
        self.render_stats = {
            'total_renders': 0,
            'last_render_time': None,
            'average_render_interval': 0.0
        }
        
        # Subscribe to system events if available
        self._setup_event_listeners()
        
        print(f"🎨 DAWN Renderer Integration initialized")
        print(f"   Renderer mode: {'Minimal' if use_minimal else 'Full'}")
        print(f"   Auto-render: {self.auto_render}")
        print(f"   Core systems: {'Live' if DAWN_CORE_AVAILABLE else 'Mock'}")
    
    def _setup_event_listeners(self):
        """Setup event listeners for automatic rendering."""
        # If DAWN has event systems, subscribe to relevant events
        if hasattr(self.pulse_engine, 'on_pulse_update'):
            self.pulse_engine.on_pulse_update(self._on_pulse_update)
        if hasattr(self.sigil_manager, 'on_sigil_change'):
            self.sigil_manager.on_sigil_change(self._on_sigil_change)
        if hasattr(self.memory_router, 'on_memory_update'):
            self.memory_router.on_memory_update(self._on_memory_update)
    
    def _on_pulse_update(self, pulse_data: Dict[str, Any]):
        """Handle pulse engine updates."""
        if self.auto_render:
            self.render_current_state()
    
    def _on_sigil_change(self, sigil_data: Dict[str, Any]):
        """Handle sigil manager updates."""
        if self.auto_render:
            self.render_current_state()
    
    def _on_memory_update(self, memory_data: Dict[str, Any]):
        """Handle memory router updates."""
        if self.auto_render:
            self.render_current_state()
    
    def gather_system_state(self) -> Dict[str, Any]:
        """Gather current state from all DAWN systems."""
        try:
            # Gather pulse state
            pulse_state = {
                'entropy': getattr(self.pulse_engine, 'get_current_entropy', lambda: 0.5)(),
                'heat': getattr(self.pulse_engine, 'get_pulse_heat', lambda: 30.0)(),
                'zone': getattr(self.pulse_engine, 'get_pulse_zone', lambda: 'ACTIVE')(),
                'focus': getattr(self.pulse_engine, 'pulse_state', {}).get('focus', 0.7),
                'chaos': getattr(self.pulse_engine, 'pulse_state', {}).get('chaos', 0.3),
                'timestamp': datetime.now().isoformat()
            }
            
            # Gather active sigils
            active_sigils = []
            if hasattr(self.sigil_manager, 'get_active_sigils'):
                raw_sigils = self.sigil_manager.get_active_sigils()
                for sigil in raw_sigils:
                    # Convert to renderer format
                    sigil_data = {
                        'name': sigil.get('name', 'UNKNOWN'),
                        'urgency': self._map_urgency(sigil.get('urgency', 'low')),
                        'duration': sigil.get('duration', 0.0),
                        'trigger_count': sigil.get('trigger_count', 1)
                    }
                    active_sigils.append(sigil_data)
            
            # Gather symbolic organs (if available)
            symbolic_organs = {}
            if hasattr(self.pulse_engine, 'get_symbolic_organs'):
                symbolic_organs = self.pulse_engine.get_symbolic_organs()
            elif hasattr(self.pulse_engine, 'organs'):
                # Fallback: extract from organs attribute
                organs = getattr(self.pulse_engine, 'organs', {})
                for name, organ in organs.items():
                    if hasattr(organ, 'get_state'):
                        symbolic_organs[name] = organ.get_state()
                    else:
                        symbolic_organs[name] = str(organ)
            
            # Gather memory statistics
            memory_stats = {}
            if hasattr(self.memory_router, 'get_chunk_count'):
                memory_stats['memory_chunks'] = self.memory_router.get_chunk_count()
            if hasattr(self.memory_router, 'get_memory_stats'):
                memory_stats.update(self.memory_router.get_memory_stats())
            
            # Combine system stats
            system_stats = {**pulse_state, **memory_stats}
            
            return {
                'sigils': active_sigils,
                'organs': symbolic_organs,
                'stats': system_stats
            }
            
        except Exception as e:
            print(f"⚠️ Error gathering system state: {e}")
            return {
                'sigils': [],
                'organs': {},
                'stats': {'error': str(e)}
            }
    
    def _map_urgency(self, urgency_str: str) -> UrgencyLevel:
        """Map string urgency to UrgencyLevel enum."""
        mapping = {
            'low': UrgencyLevel.LOW,
            'medium': UrgencyLevel.MEDIUM,
            'high': UrgencyLevel.HIGH,
            'critical': UrgencyLevel.CRITICAL
        }
        return mapping.get(urgency_str.lower(), UrgencyLevel.LOW)
    
    def render_current_state(self, force: bool = False):
        """Render the current DAWN system state."""
        current_time = time.time()
        
        # Gather system state
        state_data = self.gather_system_state()
        
        # Render using the configured renderer
        self.renderer.render(
            sigil_data=state_data['sigils'],
            organ_data=state_data['organs'],
            system_data=state_data['stats'],
            force_render=force
        )
        
        # Update statistics
        self._update_render_stats(current_time)
    
    def render_minimal_live(self):
        """Render a minimal single-line live status."""
        state_data = self.gather_system_state()
        
        # Extract sigil names for minimal display
        sigil_names = [s['name'] for s in state_data['sigils']]
        
        # Extract key stats for minimal display
        stats = state_data['stats']
        quick_stats = {
            'E': stats.get('entropy', 0.0),
            'H': stats.get('heat', 0.0),
            'F': stats.get('focus', 0.0),
            'C': stats.get('chaos', 0.0)
        }
        
        self.renderer.render_minimal(sigil_names, quick_stats)
    
    def _update_render_stats(self, current_time: float):
        """Update rendering statistics."""
        if self.last_update_time > 0:
            interval = current_time - self.last_update_time
            # Calculate rolling average
            count = self.render_stats['total_renders']
            avg = self.render_stats['average_render_interval']
            self.render_stats['average_render_interval'] = (avg * count + interval) / (count + 1)
        
        self.render_stats['total_renders'] += 1
        self.render_stats['last_render_time'] = datetime.now().isoformat()
        self.last_update_time = current_time
    
    def start_live_monitor(self, interval: float = 2.0):
        """Start continuous live monitoring of DAWN state."""
        print(f"🔴 Starting DAWN live monitor (interval: {interval}s)")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                self.render_current_state(force=True)
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n⏹️ Live monitor stopped")
            self._print_final_stats()
    
    async def start_async_monitor(self, interval: float = 2.0):
        """Start asynchronous live monitoring."""
        print(f"🔴 Starting DAWN async monitor (interval: {interval}s)")
        
        try:
            while True:
                self.render_current_state(force=True)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print(f"\n⏹️ Async monitor stopped")
            self._print_final_stats()
    
    def _print_final_stats(self):
        """Print final rendering statistics."""
        stats = self.render_stats
        print(f"\n📊 Rendering Statistics:")
        print(f"   Total renders: {stats['total_renders']}")
        print(f"   Average interval: {stats['average_render_interval']:.2f}s")
        print(f"   Last render: {stats['last_render_time']}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status information about the integration."""
        return {
            'core_available': DAWN_CORE_AVAILABLE,
            'renderer_type': 'minimal' if hasattr(self.renderer.config, 'show_borders') and not self.renderer.config.show_borders else 'full',
            'auto_render': self.auto_render,
            'render_stats': self.render_stats,
            'system_components': {
                'pulse_engine': type(self.pulse_engine).__name__,
                'memory_router': type(self.memory_router).__name__,
                'sigil_manager': type(self.sigil_manager).__name__
            }
        }


# Factory functions for easy integration
def create_dawn_terminal_monitor(pulse_engine=None, memory_router=None, sigil_manager=None) -> DAWNRendererIntegration:
    """Create a full terminal monitor for DAWN systems."""
    return DAWNRendererIntegration(
        pulse_engine=pulse_engine,
        memory_router=memory_router,
        sigil_manager=sigil_manager,
        use_minimal=False,
        auto_render=True
    )


def create_dawn_minimal_monitor(pulse_engine=None, memory_router=None, sigil_manager=None) -> DAWNRendererIntegration:
    """Create a minimal monitor for DAWN systems."""
    return DAWNRendererIntegration(
        pulse_engine=pulse_engine,
        memory_router=memory_router,
        sigil_manager=sigil_manager,
        use_minimal=True,
        auto_render=True
    )


def quick_dawn_render(pulse_engine=None, memory_router=None, sigil_manager=None):
    """Quick function to render current DAWN state once."""
    monitor = create_dawn_terminal_monitor(pulse_engine, memory_router, sigil_manager)
    monitor.render_current_state(force=True)


# Example integration
if __name__ == "__main__":
    print("🎨 Testing DAWN Renderer Integration")
    
    # Create mock systems for testing
    pulse_engine = PulseEngine()
    memory_router = MemoryRouter()
    sigil_manager = SigilManager()
    
    # Test full monitor
    print("\n🧪 Testing full monitor:")
    monitor = create_dawn_terminal_monitor(pulse_engine, memory_router, sigil_manager)
    monitor.render_current_state(force=True)
    
    # Test minimal monitor
    print("\n🧪 Testing minimal monitor:")
    minimal_monitor = create_dawn_minimal_monitor(pulse_engine, memory_router, sigil_manager)
    minimal_monitor.render_minimal_live()
    
    # Show integration status
    print(f"\n📊 Integration Status:")
    status = monitor.get_integration_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print(f"\n✨ Integration ready!")
    print(f"   Use create_dawn_terminal_monitor() for full monitoring")
    print(f"   Use create_dawn_minimal_monitor() for minimal display")
    print(f"   Use quick_dawn_render() for one-time renders") 