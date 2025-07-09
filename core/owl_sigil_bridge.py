#!/usr/bin/env python3
"""
Owl-Sigil Bridge System
=======================
Connects DAWN's Owl bloom monitoring system with the Sigil command stream
for real-time bidirectional cognitive command processing.

This bridge enables:
- Owl observations triggering sigil commands
- Sigil execution generating owl reflections
- Bloom activity influencing sigil priorities
- Real-time sigil stream updates from owl monitoring
"""

import time
import json
import threading
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import deque, defaultdict

# Import DAWN components
try:
    from reflection.owl.owl_memory.owl_bloom_parser import OwlBloomParser
    from reflection.owl.owl_tracer_log import owl_log
    from backend.visual.sigil_command_stream_visualizer import SigilCommandStreamVisualizer
    from core.sigil_engine import SigilEngine
    OWL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some components unavailable: {e}")
    OWL_AVAILABLE = False


@dataclass
class OwlSigilEvent:
    """Event structure for owl-sigil interactions"""
    event_type: str  # 'bloom_detected', 'sigil_triggered', 'reflection_generated'
    source: str      # 'owl' or 'sigil'
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1  # 1-10, higher = more urgent
    processed: bool = False


@dataclass
class BloomSigilMapping:
    """Maps bloom characteristics to sigil commands"""
    bloom_pattern: str
    entropy_threshold: float
    intensity_threshold: int
    suggested_sigils: List[str]
    cooldown_seconds: int = 30
    last_triggered: Optional[datetime] = None


class OwlSigilBridge:
    """Bridge between Owl observation system and Sigil command stream"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Core components
        self.owl_parser = OwlBloomParser() if OWL_AVAILABLE else None
        self.sigil_visualizer = None
        self.sigil_engine = None
        
        # Event processing
        self.event_queue = deque(maxlen=1000)
        self.event_history = deque(maxlen=5000)
        self.processing_thread = None
        
        # Bloom-to-sigil mappings
        self.bloom_mappings = self._initialize_bloom_mappings()
        
        # Sigil-to-reflection mappings  
        self.sigil_reflection_handlers = self._initialize_sigil_handlers()
        
        # State tracking
        self.active_blooms: Dict[str, Dict] = {}
        self.recent_sigils: deque = deque(maxlen=50)
        self.performance_metrics = {
            'events_processed': 0,
            'sigils_triggered': 0,
            'reflections_generated': 0,
            'bridge_uptime': 0
        }
        
        # Configuration
        self.config = {
            'bloom_scan_interval': 2.0,  # seconds
            'sigil_cooldown_default': 30,  # seconds
            'max_concurrent_sigils': 5,
            'entropy_alert_threshold': 0.7,
            'enable_auto_reflection': True,
            'log_all_events': True
        }
        
        # Callbacks for external systems
        self.bloom_detected_callbacks: List[Callable] = []
        self.sigil_triggered_callbacks: List[Callable] = []
        self.reflection_generated_callbacks: List[Callable] = []
        
        self.logger.info("🦉🔮 Owl-Sigil Bridge initialized")
    
    def _initialize_bloom_mappings(self) -> List[BloomSigilMapping]:
        """Initialize bloom pattern to sigil command mappings"""
        return [
            # High entropy bloom patterns
            BloomSigilMapping(
                bloom_pattern="high_entropy",
                entropy_threshold=0.7,
                intensity_threshold=6,
                suggested_sigils=["⚡", "◉", "▲"],  # action, attention, reasoning
                cooldown_seconds=45
            ),
            
            # Memory-intensive patterns
            BloomSigilMapping(
                bloom_pattern="memory_access",
                entropy_threshold=0.3,
                intensity_threshold=4,
                suggested_sigils=["◆", "⬢"],  # memory, integration
                cooldown_seconds=20
            ),
            
            # Creative synthesis patterns
            BloomSigilMapping(
                bloom_pattern="creative_synthesis",
                entropy_threshold=0.6,
                intensity_threshold=5,
                suggested_sigils=["✦", "◇", "⬡"],  # creativity, memory_lite, integration_lite
                cooldown_seconds=35
            ),
            
            # Critical rebloom risk
            BloomSigilMapping(
                bloom_pattern="rebloom_risk",
                entropy_threshold=0.8,
                intensity_threshold=7,
                suggested_sigils=["🚨", "⟁", "/suppress"],  # alert, contradiction, suppress
                cooldown_seconds=60
            ),
            
            # Mood-driven patterns
            BloomSigilMapping(
                bloom_pattern="mood_shift",
                entropy_threshold=0.4,
                intensity_threshold=3,
                suggested_sigils=["○", "△"],  # attention_soft, reasoning_lite
                cooldown_seconds=15
            )
        ]
    
    def _initialize_sigil_handlers(self) -> Dict[str, Callable]:
        """Initialize sigil execution to reflection handlers"""
        return {
            "⚡": self._handle_action_sigil,
            "◉": self._handle_attention_sigil,
            "◆": self._handle_memory_sigil,
            "▲": self._handle_reasoning_sigil,
            "✦": self._handle_creativity_sigil,
            "⬢": self._handle_integration_sigil,
            "🚨": self._handle_alert_sigil,
            "⟁": self._handle_contradiction_sigil,
            "/suppress": self._handle_suppression_sigil
        }
    
    def connect_sigil_engine(self, engine):
        """Connect to a sigil engine for command execution"""
        self.sigil_engine = engine
        self.logger.info("🔮 Connected to sigil engine")
    
    def connect_sigil_visualizer(self, visualizer):
        """Connect to sigil command stream visualizer"""
        self.sigil_visualizer = visualizer
        self.logger.info("🎨 Connected to sigil visualizer")
    
    def start_monitoring(self):
        """Start the owl-sigil bridge monitoring system"""
        if self.running:
            return
        
        self.running = True
        
        # Start event processing thread
        self.processing_thread = threading.Thread(
            target=self._event_processing_loop,
            daemon=True
        )
        self.processing_thread.start()
        
        # Start bloom monitoring
        self._start_bloom_monitoring()
        
        self.logger.info("🦉🔮 Bridge monitoring started")
    
    def stop_monitoring(self):
        """Stop the bridge monitoring system"""
        self.running = False
        
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        
        self.logger.info("🦉🔮 Bridge monitoring stopped")
    
    def _start_bloom_monitoring(self):
        """Start monitoring bloom activity"""
        def bloom_monitor():
            while self.running:
                try:
                    self._scan_for_new_blooms()
                    time.sleep(self.config['bloom_scan_interval'])
                except Exception as e:
                    self.logger.error(f"Bloom monitoring error: {e}")
                    time.sleep(5)
        
        bloom_thread = threading.Thread(target=bloom_monitor, daemon=True)
        bloom_thread.start()
    
    def _scan_for_new_blooms(self):
        """Scan for new bloom activity and analyze patterns"""
        if not self.owl_parser:
            return
        
        try:
            # Run owl scan for new blooms
            new_blooms = self.owl_parser.run_owl_scan()
            
            for bloom_data in new_blooms:
                bloom_id = bloom_data.get('seed_id')
                
                # Skip if already processed
                if bloom_id in self.active_blooms:
                    continue
                
                # Store bloom for tracking
                self.active_blooms[bloom_id] = bloom_data
                
                # Analyze bloom and trigger sigils if needed
                self._analyze_bloom_for_sigils(bloom_data)
                
                # Generate owl reflection
                self._generate_bloom_reflection(bloom_data)
                
                # Notify callbacks
                for callback in self.bloom_detected_callbacks:
                    try:
                        callback(bloom_data)
                    except Exception as e:
                        self.logger.error(f"Bloom callback error: {e}")
        
        except Exception as e:
            self.logger.error(f"Bloom scan error: {e}")
    
    def _analyze_bloom_for_sigils(self, bloom_data: Dict):
        """Analyze bloom data and trigger appropriate sigils"""
        entropy = bloom_data.get('entropy', 0.0)
        intensity = bloom_data.get('intensity', 0)
        pattern = bloom_data.get('pattern', '')
        rebloom_risk = bloom_data.get('rebloom_risk', False)
        
        # Check each mapping pattern
        for mapping in self.bloom_mappings:
            if self._bloom_matches_mapping(bloom_data, mapping):
                # Check cooldown
                if self._is_mapping_on_cooldown(mapping):
                    continue
                
                # Trigger sigils
                for sigil in mapping.suggested_sigils:
                    self._trigger_sigil_from_bloom(sigil, bloom_data, mapping)
                
                # Update cooldown
                mapping.last_triggered = datetime.now()
    
    def _bloom_matches_mapping(self, bloom_data: Dict, mapping: BloomSigilMapping) -> bool:
        """Check if bloom matches a sigil mapping pattern"""
        entropy = bloom_data.get('entropy', 0.0)
        intensity = bloom_data.get('intensity', 0)
        rebloom_risk = bloom_data.get('rebloom_risk', False)
        
        # Basic thresholds
        entropy_match = entropy >= mapping.entropy_threshold
        intensity_match = intensity >= mapping.intensity_threshold
        
        # Pattern-specific logic
        if mapping.bloom_pattern == "high_entropy":
            return entropy_match and intensity_match
        elif mapping.bloom_pattern == "memory_access":
            return entropy < 0.5 and intensity_match
        elif mapping.bloom_pattern == "creative_synthesis":
            return 0.4 <= entropy <= 0.8 and intensity_match
        elif mapping.bloom_pattern == "rebloom_risk":
            return rebloom_risk and entropy_match
        elif mapping.bloom_pattern == "mood_shift":
            mood = bloom_data.get('mood', 'neutral')
            return mood != 'neutral' and intensity >= 2
        
        return False
    
    def _is_mapping_on_cooldown(self, mapping: BloomSigilMapping) -> bool:
        """Check if mapping is on cooldown"""
        if not mapping.last_triggered:
            return False
        
        elapsed = (datetime.now() - mapping.last_triggered).total_seconds()
        return elapsed < mapping.cooldown_seconds
    
    def _trigger_sigil_from_bloom(self, sigil: str, bloom_data: Dict, mapping: BloomSigilMapping):
        """Trigger a sigil command based on bloom analysis"""
        event = OwlSigilEvent(
            event_type='sigil_triggered',
            source='owl',
            data={
                'sigil': sigil,
                'bloom_id': bloom_data.get('seed_id'),
                'bloom_entropy': bloom_data.get('entropy'),
                'bloom_intensity': bloom_data.get('intensity'),
                'trigger_pattern': mapping.bloom_pattern,
                'urgency': self._calculate_sigil_urgency(bloom_data, sigil)
            },
            priority=self._calculate_event_priority(bloom_data, sigil)
        )
        
        self.event_queue.append(event)
        
        # Log the trigger
        owl_log(f"[Bridge] 🔮 Sigil {sigil} triggered by bloom pattern {mapping.bloom_pattern}")
        
        self.logger.info(f"Sigil {sigil} triggered by bloom {bloom_data.get('seed_id')}")
    
    def _calculate_sigil_urgency(self, bloom_data: Dict, sigil: str) -> float:
        """Calculate urgency score for sigil execution"""
        base_urgency = 0.5
        
        # Entropy factor
        entropy = bloom_data.get('entropy', 0.0)
        entropy_factor = min(entropy * 2, 1.0)
        
        # Intensity factor
        intensity = bloom_data.get('intensity', 0)
        intensity_factor = min(intensity / 10.0, 1.0)
        
        # Rebloom risk factor
        risk_factor = 0.3 if bloom_data.get('rebloom_risk', False) else 0.0
        
        # Sigil-specific urgency
        sigil_urgency = {
            "🚨": 0.9,  # Alert sigils are high urgency
            "⟁": 0.8,   # Contradiction handling
            "/suppress": 0.7,  # Suppression commands
            "⚡": 0.6,   # Action commands
            "◉": 0.5,   # Attention
            "▲": 0.4,   # Reasoning
            "◆": 0.3,   # Memory
            "✦": 0.2,   # Creativity
            "⬢": 0.2    # Integration
        }.get(sigil, 0.3)
        
        return min(base_urgency + entropy_factor + intensity_factor + risk_factor + sigil_urgency, 1.0)
    
    def _calculate_event_priority(self, bloom_data: Dict, sigil: str) -> int:
        """Calculate event priority (1-10)"""
        urgency = self._calculate_sigil_urgency(bloom_data, sigil)
        return max(1, min(10, int(urgency * 10)))
    
    def _generate_bloom_reflection(self, bloom_data: Dict):
        """Generate owl reflection based on bloom activity"""
        if not self.config['enable_auto_reflection']:
            return
        
        bloom_id = bloom_data.get('seed_id')
        entropy = bloom_data.get('entropy', 0.0)
        intensity = bloom_data.get('intensity', 0)
        pattern = bloom_data.get('pattern', 'unknown')
        rebloom_risk = bloom_data.get('rebloom_risk', False)
        
        # Generate contextual reflection
        if rebloom_risk:
            reflection = f"🦉 High-risk bloom detected: {bloom_id}. Entropy {entropy:.3f} exceeds stability threshold. Intervention recommended."
        elif entropy > 0.6:
            reflection = f"🦉 Complex bloom emerging: {bloom_id}. Pattern '{pattern}' shows elevated entropy {entropy:.3f}. Monitoring closely."
        elif intensity > 6:
            reflection = f"🦉 Intense bloom activity: {bloom_id}. Strong manifestation detected (intensity {intensity}). Significance noted."
        else:
            reflection = f"🦉 Bloom observed: {bloom_id}. Standard pattern '{pattern}' with normal parameters. System stable."
        
        # Log reflection
        owl_log(reflection)
        
        # Create reflection event
        event = OwlSigilEvent(
            event_type='reflection_generated',
            source='owl',
            data={
                'reflection': reflection,
                'bloom_id': bloom_id,
                'bloom_data': bloom_data,
                'analysis': {
                    'entropy_level': 'high' if entropy > 0.6 else 'medium' if entropy > 0.3 else 'low',
                    'intensity_level': 'high' if intensity > 6 else 'medium' if intensity > 3 else 'low',
                    'risk_assessment': 'critical' if rebloom_risk else 'normal'
                }
            },
            priority=8 if rebloom_risk else 3
        )
        
        self.event_queue.append(event)
        
        # Notify callbacks
        for callback in self.reflection_generated_callbacks:
            try:
                callback(reflection, bloom_data)
            except Exception as e:
                self.logger.error(f"Reflection callback error: {e}")
    
    def _event_processing_loop(self):
        """Main event processing loop"""
        while self.running:
            try:
                if self.event_queue:
                    event = self.event_queue.popleft()
                    self._process_event(event)
                else:
                    time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Event processing error: {e}")
                time.sleep(1)
    
    def _process_event(self, event: OwlSigilEvent):
        """Process a single owl-sigil event"""
        try:
            if event.event_type == 'sigil_triggered':
                self._execute_sigil_command(event)
            elif event.event_type == 'reflection_generated':
                self._handle_reflection_event(event)
            elif event.event_type == 'bloom_detected':
                self._handle_bloom_event(event)
            
            # Mark as processed
            event.processed = True
            self.event_history.append(event)
            self.performance_metrics['events_processed'] += 1
            
            if self.config['log_all_events']:
                self.logger.debug(f"Processed event: {event.event_type} from {event.source}")
        
        except Exception as e:
            self.logger.error(f"Error processing event {event.event_type}: {e}")
    
    def _execute_sigil_command(self, event: OwlSigilEvent):
        """Execute sigil command through connected systems"""
        sigil = event.data.get('sigil')
        urgency = event.data.get('urgency', 0.5)
        
        # Execute through sigil engine if connected
        if self.sigil_engine:
            try:
                # Create sigil for execution
                from schema.sigil import Sigil
                sigil_obj = Sigil(
                    sigil_id=f"owl_{int(time.time())}",
                    command=f"owl_triggered_{sigil}",
                    symbol=sigil,
                    cognitive_house="monitor",
                    level=int(urgency * 10),
                    thermal_signature=urgency * 50,
                    lifespan=30.0,
                    priority_score=urgency
                )
                
                self.sigil_engine.add_sigil(sigil_obj)
                self.performance_metrics['sigils_triggered'] += 1
                
            except Exception as e:
                self.logger.error(f"Sigil engine execution error: {e}")
        
        # Update visualizer if connected
        if self.sigil_visualizer:
            try:
                # Determine category from sigil
                category = self._get_sigil_category(sigil)
                self.sigil_visualizer._add_sigil(category, sigil, urgency, "owl_trigger")
            except Exception as e:
                self.logger.error(f"Visualizer update error: {e}")
        
        # Track recent sigils
        self.recent_sigils.append({
            'sigil': sigil,
            'timestamp': datetime.now(),
            'urgency': urgency,
            'source': 'owl_bloom'
        })
        
        # Execute sigil-specific handler
        handler = self.sigil_reflection_handlers.get(sigil)
        if handler:
            handler(event)
    
    def _get_sigil_category(self, sigil: str) -> str:
        """Map sigil symbol to category for visualizer"""
        category_map = {
            "◉": "attention", "○": "attention",
            "◆": "memory", "◇": "memory",
            "▲": "reasoning", "△": "reasoning",
            "✦": "creativity", "✧": "creativity",
            "⬢": "integration", "⬡": "integration",
            "⚡": "action", "➤": "action",
            "🚨": "meta", "⟁": "meta"
        }
        return category_map.get(sigil, "meta")
    
    def _handle_reflection_event(self, event: OwlSigilEvent):
        """Handle reflection generation events"""
        reflection = event.data.get('reflection')
        bloom_data = event.data.get('bloom_data', {})
        
        # Additional processing based on reflection content
        if "High-risk" in reflection:
            # Trigger additional monitoring
            self._escalate_monitoring(bloom_data)
        
        self.performance_metrics['reflections_generated'] += 1
    
    def _handle_bloom_event(self, event: OwlSigilEvent):
        """Handle bloom detection events"""
        bloom_data = event.data
        
        # Update active blooms tracking
        bloom_id = bloom_data.get('seed_id')
        if bloom_id:
            self.active_blooms[bloom_id] = bloom_data
    
    def _escalate_monitoring(self, bloom_data: Dict):
        """Escalate monitoring for high-risk blooms"""
        bloom_id = bloom_data.get('seed_id')
        
        # Reduce scan interval temporarily
        original_interval = self.config['bloom_scan_interval']
        self.config['bloom_scan_interval'] = max(0.5, original_interval / 2)
        
        # Schedule return to normal interval
        def restore_interval():
            time.sleep(30)  # Monitor intensely for 30 seconds
            self.config['bloom_scan_interval'] = original_interval
        
        threading.Thread(target=restore_interval, daemon=True).start()
        
        owl_log(f"[Bridge] 📈 Escalated monitoring for high-risk bloom {bloom_id}")
    
    # Sigil execution handlers
    def _handle_action_sigil(self, event: OwlSigilEvent):
        """Handle action sigil execution"""
        owl_log("[Bridge] ⚡ Action sigil executed - cognitive response initiated")
    
    def _handle_attention_sigil(self, event: OwlSigilEvent):
        """Handle attention sigil execution"""
        owl_log("[Bridge] 👁️ Attention sigil executed - focus redirected")
    
    def _handle_memory_sigil(self, event: OwlSigilEvent):
        """Handle memory sigil execution"""
        owl_log("[Bridge] 🧠 Memory sigil executed - recall process activated")
    
    def _handle_reasoning_sigil(self, event: OwlSigilEvent):
        """Handle reasoning sigil execution"""
        owl_log("[Bridge] 🔍 Reasoning sigil executed - logical analysis engaged")
    
    def _handle_creativity_sigil(self, event: OwlSigilEvent):
        """Handle creativity sigil execution"""
        owl_log("[Bridge] ✨ Creativity sigil executed - synthesis pathways opened")
    
    def _handle_integration_sigil(self, event: OwlSigilEvent):
        """Handle integration sigil execution"""
        owl_log("[Bridge] 🔗 Integration sigil executed - coherence consolidation")
    
    def _handle_alert_sigil(self, event: OwlSigilEvent):
        """Handle alert sigil execution"""
        bloom_id = event.data.get('bloom_id', 'unknown')
        owl_log(f"[Bridge] 🚨 ALERT: Critical bloom pattern detected in {bloom_id}")
    
    def _handle_contradiction_sigil(self, event: OwlSigilEvent):
        """Handle contradiction sigil execution"""
        owl_log("[Bridge] ⚠️ Contradiction detection activated - seeking resolution")
    
    def _handle_suppression_sigil(self, event: OwlSigilEvent):
        """Handle suppression sigil execution"""
        bloom_id = event.data.get('bloom_id', 'unknown')
        owl_log(f"[Bridge] 🛑 Suppression protocol activated for bloom {bloom_id}")
    
    # External interface methods
    def inject_external_sigil(self, sigil: str, source: str = "external", urgency: float = 0.5):
        """Inject sigil from external system"""
        event = OwlSigilEvent(
            event_type='sigil_triggered',
            source=source,
            data={
                'sigil': sigil,
                'urgency': urgency,
                'external_trigger': True
            },
            priority=int(urgency * 10)
        )
        
        self.event_queue.append(event)
        self.logger.info(f"External sigil {sigil} injected from {source}")
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """Get current bridge status and metrics"""
        return {
            'running': self.running,
            'active_blooms': len(self.active_blooms),
            'queued_events': len(self.event_queue),
            'recent_sigils': len(self.recent_sigils),
            'performance_metrics': self.performance_metrics.copy(),
            'config': self.config.copy(),
            'uptime_seconds': time.time() - self.performance_metrics.get('start_time', time.time())
        }
    
    def get_recent_activity(self, count: int = 10) -> List[Dict]:
        """Get recent bridge activity"""
        recent_events = list(self.event_history)[-count:]
        return [
            {
                'event_type': event.event_type,
                'source': event.source,
                'timestamp': event.timestamp.isoformat(),
                'priority': event.priority,
                'data_summary': str(event.data)[:100] + "..." if len(str(event.data)) > 100 else str(event.data)
            }
            for event in recent_events
        ]
    
    # Callback registration
    def on_bloom_detected(self, callback: Callable):
        """Register callback for bloom detection events"""
        self.bloom_detected_callbacks.append(callback)
    
    def on_sigil_triggered(self, callback: Callable):
        """Register callback for sigil trigger events"""
        self.sigil_triggered_callbacks.append(callback)
    
    def on_reflection_generated(self, callback: Callable):
        """Register callback for reflection generation events"""
        self.reflection_generated_callbacks.append(callback)


# Global bridge instance
_bridge_instance = None

def get_owl_sigil_bridge() -> OwlSigilBridge:
    """Get global owl-sigil bridge instance"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = OwlSigilBridge()
    return _bridge_instance


def initialize_bridge_with_systems(sigil_engine=None, sigil_visualizer=None):
    """Initialize bridge with connected systems"""
    bridge = get_owl_sigil_bridge()
    
    if sigil_engine:
        bridge.connect_sigil_engine(sigil_engine)
    
    if sigil_visualizer:
        bridge.connect_sigil_visualizer(sigil_visualizer)
    
    return bridge


if __name__ == "__main__":
    # Demo/test mode
    logging.basicConfig(level=logging.INFO)
    bridge = OwlSigilBridge()
    
    # Demo callbacks
    def demo_bloom_callback(bloom_data):
        print(f"🦉 Demo: Bloom detected - {bloom_data.get('seed_id')}")
    
    def demo_sigil_callback(sigil, urgency):
        print(f"🔮 Demo: Sigil triggered - {sigil} (urgency: {urgency})")
    
    def demo_reflection_callback(reflection, bloom_data):
        print(f"💭 Demo: Reflection - {reflection}")
    
    # Register callbacks
    bridge.on_bloom_detected(demo_bloom_callback)
    bridge.on_reflection_generated(demo_reflection_callback)
    
    # Start monitoring
    bridge.start_monitoring()
    
    print("🦉🔮 Owl-Sigil Bridge demo started")
    print("Monitoring for bloom activity and generating sigil commands...")
    print("Press Ctrl+C to stop")
    
    try:
        # Inject some demo sigils
        time.sleep(2)
        bridge.inject_external_sigil("◉", "demo", 0.7)
        time.sleep(3)
        bridge.inject_external_sigil("✦", "demo", 0.5)
        
        # Keep running
        while True:
            time.sleep(5)
            status = bridge.get_bridge_status()
            print(f"Bridge status: {status['performance_metrics']}")
            
    except KeyboardInterrupt:
        print("\nStopping bridge...")
        bridge.stop_monitoring()
        print("���� Bridge stopped") 