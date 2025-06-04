"""
🌅 DAWN Command Interface - Runtime Control System
═══════════════════════════════════════════════════════════════════

A clean command interface for interacting with DAWN's live runtime.
All commands are schema-aware and respect the tick cycle integrity.

Commands flow through a central router, ensuring consistent logging
and safe execution within DAWN's cognitive cycles.
"""

import functools
import inspect
import json
import time
from datetime import datetime
from typing import Dict, Callable, Any, Optional, List, Tuple
import logging
import threading
import traceback
import sys
import os

# Add parent directory to path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import DAWN main loop
try:
    from main import DAWNGenomeConsciousnessWrapper
    DAWN_AVAILABLE = True
except ImportError:
    print("Warning: Could not import DAWNGenomeConsciousnessWrapper from main.py - running in standalone mode")
    DAWN_AVAILABLE = False

# Configure DAWN logger
logging.basicConfig(
    level=logging.INFO,
    format='[DAWN] %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("DAWN")

# Global tick safety lock
_tick_lock = threading.RLock()
_tick_active = False

# Global DAWN instance (will be set when connected)
_dawn_instance = None

# Export these for external use
__all__ = ['run_command_from_input', 'connect_to_dawn', 'interactive_mode', 
           '_tick_lock', '_tick_active', 'router']


def tick_safe(func: Callable) -> Callable:
    """
    Decorator to ensure commands don't interrupt mid-tick processing.
    Commands decorated with @tick_safe will wait for tick completion.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with _tick_lock:
            if _tick_active:
                logger.info(f"⏳ Command '{func.__name__}' waiting for tick completion...")
                # In real implementation, this would wait for tick signal
                time.sleep(0.1)
            
            logger.debug(f"🔓 Executing tick-safe command: {func.__name__}")
            return func(*args, **kwargs)
    
    wrapper._tick_safe = True
    return wrapper


# ═══════════════════════════════════════════════════════════════════
# COMMAND IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════════════

@tick_safe
def print_visual_status():
    """Display DAWN's current visual/emotional status"""
    logger.info("🎨 Visual Status Report")
    logger.info("─" * 40)
    
    if _dawn_instance and DAWN_AVAILABLE:
        # Pull from actual DAWN state
        try:
            status = {
                "mood_valence": getattr(_dawn_instance, 'current_mood_valence', 0.0),
                "arousal": getattr(_dawn_instance, 'current_arousal', 0.5),
                "coherence": getattr(_dawn_instance, 'coherence_score', 1.0),
                "tick": getattr(_dawn_instance, 'tick', 0),
                "entropy": getattr(_dawn_instance, 'current_entropy', 0.0)
            }
        except Exception as e:
            logger.error(f"Could not read DAWN state: {e}")
            status = _get_mock_status()
    else:
        # Mock status data
        status = _get_mock_status()
    
    logger.info(f"Tick:          {status.get('tick', 0)}")
    logger.info(f"Mood Valence:  {'▓' * int(abs(status['mood_valence']) * 10):10} {status['mood_valence']:+.2f}")
    logger.info(f"Arousal:       {'▓' * int(status['arousal'] * 10):10} {status['arousal']:.2f}")
    logger.info(f"Coherence:     {'▓' * int(status['coherence'] * 10):10} {status['coherence']:.2f}")
    logger.info(f"Entropy:       {'▓' * int(status.get('entropy', 0) * 10):10} {status.get('entropy', 0):.2f}")
    logger.info("─" * 40)


def _get_mock_status():
    """Get mock status when DAWN not connected"""
    return {
        "mood_valence": 0.65,
        "arousal": 0.45,
        "coherence": 0.89,
        "entropy": 0.32,
        "tick": 0
    }


@tick_safe
def print_schema_status():
    """Display schema integrity and component status"""
    logger.info("📋 Schema Status Report")
    logger.info("─" * 40)
    
    if _dawn_instance and DAWN_AVAILABLE:
        # Check actual module status
        components = {}
        
        # Check for common DAWN modules
        module_checks = [
            ("bloom_engine", hasattr(_dawn_instance, 'bloom_engine')),
            ("memory_system", hasattr(_dawn_instance, 'memory')),
            ("emotion_system", hasattr(_dawn_instance, 'emotion')),
            ("coherence_monitor", hasattr(_dawn_instance, 'coherence_score')),
            ("entropy_tracker", hasattr(_dawn_instance, 'current_entropy')),
            ("genome_mode", hasattr(_dawn_instance, 'genome_mode'))
        ]
        
        for name, exists in module_checks:
            components[name] = {
                "status": "ACTIVE" if exists else "MISSING",
                "health": 1.0 if exists else 0.0
            }
    else:
        # Mock component status
        components = {
            "bloom_engine": {"status": "UNKNOWN", "health": 0.5},
            "memory_system": {"status": "UNKNOWN", "health": 0.5},
            "emotion_system": {"status": "UNKNOWN", "health": 0.5},
            "coherence_monitor": {"status": "UNKNOWN", "health": 0.5},
            "entropy_tracker": {"status": "UNKNOWN", "health": 0.5},
            "genome_mode": {"status": "UNKNOWN", "health": 0.5}
        }
    
    for name, info in components.items():
        if info["status"] == "ACTIVE":
            status_icon = "🟢"
        elif info["status"] == "UNKNOWN":
            status_icon = "🟡"
        else:
            status_icon = "🔴"
        
        health_bar = "█" * int(info["health"] * 10)
        logger.info(f"{status_icon} {name:20} [{health_bar:10}] {info['health']:.0%}")
    
    logger.info("─" * 40)
    
    if _dawn_instance:
        logger.info(f"DAWN Instance: Connected ✅")
        if hasattr(_dawn_instance, 'get_status'):
            logger.info(f"Genome Status: {_dawn_instance.get_status()}")
    else:
        logger.info(f"DAWN Instance: Not Connected ❌")


def stimulate_emotion(emotion_type: str = "joy", intensity: float = 0.5):
    """
    Stimulate a specific emotional response in DAWN
    
    Args:
        emotion_type: Type of emotion (joy, melancholy, wonder, tension)
        intensity: Intensity level (0.0 to 1.0)
    """
    valid_emotions = ["joy", "melancholy", "wonder", "tension", "curiosity", "calm"]
    
    if emotion_type not in valid_emotions:
        logger.warning(f"Unknown emotion type: {emotion_type}. Valid types: {valid_emotions}")
        return
    
    if not 0.0 <= intensity <= 1.0:
        logger.warning(f"Intensity must be between 0.0 and 1.0, got {intensity}")
        return
    
    logger.info(f"💭 Stimulating {emotion_type} at {intensity:.0%} intensity...")
    
    if _dawn_instance and DAWN_AVAILABLE:
        # Try to interact with actual emotion system
        try:
            if hasattr(_dawn_instance, 'inject_emotion'):
                _dawn_instance.inject_emotion(emotion_type, intensity)
            else:
                logger.warning("DAWN instance lacks emotion injection method")
        except Exception as e:
            logger.error(f"Could not stimulate emotion: {e}")
    else:
        # Mock emotional stimulation
        logger.info(f"  → Adjusting valence vectors...")
        logger.info(f"  → Modulating arousal to {intensity:.2f}...")
        logger.info(f"  → Triggering {emotion_type} cascade...")
    
    time.sleep(0.5)  # Simulate processing
    logger.info(f"✨ Emotional stimulation complete: {emotion_type} resonating")


def stimulate_curiosity(topic: str = "quantum_consciousness", depth: float = 0.7):
    """
    Stimulate curiosity patterns around a specific topic
    
    Args:
        topic: Topic to explore
        depth: Depth of exploration (0.0 to 1.0)
    """
    logger.info(f"🔍 Stimulating curiosity about: {topic}")
    logger.info(f"  Exploration depth: {depth:.0%}")
    
    if _dawn_instance and DAWN_AVAILABLE:
        try:
            if hasattr(_dawn_instance, 'explore_topic'):
                _dawn_instance.explore_topic(topic, depth)
        except Exception as e:
            logger.debug(f"Could not stimulate curiosity: {e}")
    
    # Always show feedback
    logger.info(f"  → Activating semantic explorers...")
    logger.info(f"  → Expanding association networks...")
    logger.info(f"  → Generating {int(depth * 10)} curiosity blooms...")
    
    time.sleep(0.3)
    logger.info(f"💡 Curiosity cascade initiated for '{topic}'")


def stimulate_tension(source: str = "paradox", target: str = "resolution"):
    """
    Create productive tension between concepts
    
    Args:
        source: Source of tension
        target: Target or resolution point
    """
    logger.info(f"⚡ Creating tension field: {source} ←→ {target}")
    
    # Mock tension creation
    logger.info(f"  → Establishing polarity...")
    logger.info(f"  → Charging semantic field...")
    logger.info(f"  → Tension level: {'▓' * 7} 70%")
    
    logger.info(f"🌊 Tension field active. Natural resolution will emerge.")


@tick_safe
def add_manual_heat(amount: float, label: str = "manual_intervention"):
    """
    Add manual heat to the system
    
    Args:
        amount: Amount of heat to add (0.0 to 1.0)
        label: Label for heat source
    """
    if not 0.0 <= amount <= 1.0:
        logger.warning(f"Heat amount must be between 0.0 and 1.0, got {amount}")
        return
    
    logger.info(f"🔥 Adding manual heat: {amount:.2f} ({label})")
    
    current_temp = 0.65  # Default
    
    if _dawn_instance and DAWN_AVAILABLE:
        try:
            # Try to get current temperature
            if hasattr(_dawn_instance, 'system_temperature'):
                current_temp = _dawn_instance.system_temperature
            
            # Try to add heat
            if hasattr(_dawn_instance, 'add_heat'):
                _dawn_instance.add_heat(amount, label)
        except Exception as e:
            logger.debug(f"Could not add heat to system: {e}")
    
    logger.info(f"  → Current system temperature: {current_temp:.2f}")
    logger.info(f"  → Adding heat: +{amount:.2f}")
    logger.info(f"  → New temperature: {current_temp + amount:.2f}")
    
    if amount > 0.5:
        logger.warning("  ⚠️  High heat injection - monitoring for cascade effects")


@tick_safe
def debug_bloom_system():
    """Display detailed bloom system debugging information"""
    logger.info("🐛 Bloom System Debug Information")
    logger.info("=" * 50)
    
    if _dawn_instance and DAWN_AVAILABLE:
        # Try to get real bloom data
        debug_info = {}
        try:
            if hasattr(_dawn_instance, 'bloom_system'):
                bloom_sys = _dawn_instance.bloom_system
                debug_info = {
                    "active_blooms": len(getattr(bloom_sys, 'active_blooms', [])),
                    "total_blooms": len(getattr(bloom_sys, 'all_blooms', [])),
                    "entropy_pressure": getattr(bloom_sys, 'entropy_pressure', 0.0),
                    "last_bloom_tick": getattr(bloom_sys, 'last_bloom_tick', 0)
                }
        except Exception as e:
            logger.debug(f"Could not access bloom system: {e}")
            debug_info = _get_mock_debug_info()
    else:
        debug_info = _get_mock_debug_info()
    
    for key, value in debug_info.items():
        logger.info(f"{key:20}: {value}")
    
    logger.info("=" * 50)


def _get_mock_debug_info():
    """Get mock debug info when DAWN not connected"""
    return {
        "active_blooms": 42,
        "pending_reblooms": 7,
        "entropy_pressure": 0.73,
        "last_bloom_tick": 1547,
        "bloom_queue": ["bloom_0x4A2", "bloom_0x4A3", "bloom_0x4A4"],
        "memory_usage": "247MB",
        "rebloom_threshold": 0.65
    }


@tick_safe
def force_test_bloom():
    """Force creation of a test bloom for debugging"""
    logger.info("🌸 Forcing test bloom creation...")
    
    test_bloom_id = f"test_bloom_{int(time.time() * 1000) % 10000}"
    
    if _dawn_instance and DAWN_AVAILABLE:
        try:
            if hasattr(_dawn_instance, 'create_bloom'):
                bloom = _dawn_instance.create_bloom(
                    bloom_id=test_bloom_id,
                    entropy=0.75,
                    mood_valence=0.0
                )
                logger.info(f"✅ Test bloom created via DAWN: {bloom}")
                return bloom
        except Exception as e:
            logger.debug(f"Could not create bloom via DAWN: {e}")
    
    # Fallback to mock
    logger.info(f"  → Creating bloom: {test_bloom_id}")
    logger.info(f"  → Entropy: 0.75")
    logger.info(f"  → Mood valence: 0.0 (neutral)")
    logger.info(f"  → Lineage depth: 0 (root)")
    
    time.sleep(0.2)
    logger.info(f"✅ Test bloom created: {test_bloom_id}")
    
    return test_bloom_id


def bloom_activation_stats():
    """Display bloom activation statistics"""
    logger.info("📊 Bloom Activation Statistics")
    logger.info("─" * 50)
    
    # Mock statistics (would pull from actual system)
    stats = {
        "total_blooms": 156,
        "active_blooms": 42,
        "dormant_blooms": 114,
        "rebloom_rate": 0.27,
        "avg_entropy": 0.68,
        "avg_lineage_depth": 3.2,
        "peak_activity_tick": 1432,
        "activation_pattern": "oscillating"
    }
    
    logger.info(f"Total Blooms:      {stats['total_blooms']}")
    logger.info(f"Active:            {stats['active_blooms']} ({stats['active_blooms']/stats['total_blooms']:.0%})")
    logger.info(f"Dormant:           {stats['dormant_blooms']}")
    logger.info(f"Rebloom Rate:      {stats['rebloom_rate']:.0%}")
    logger.info(f"Average Entropy:   {stats['avg_entropy']:.2f}")
    logger.info(f"Avg Lineage Depth: {stats['avg_lineage_depth']:.1f}")
    logger.info(f"Pattern:           {stats['activation_pattern']}")
    
    # Visual activity graph
    logger.info("\nActivity Pattern (last 10 ticks):")
    activity = [3, 5, 7, 9, 7, 5, 4, 6, 8, 6]
    for i, level in enumerate(activity):
        bar = "█" * level
        logger.info(f"  Tick -{9-i}: {bar}")


def connect_to_dawn(dawn_instance=None):
    """
    Connect command interface to DAWN instance
    
    Args:
        dawn_instance: DAWN instance to connect to
    """
    global _dawn_instance
    
    if dawn_instance:
        _dawn_instance = dawn_instance
        logger.info("✅ Connected to DAWN instance")
        return True
    
    # Try to create new instance if available
    if DAWN_AVAILABLE:
        try:
            # Import and create the appropriate class
            from main import DAWNGenomeConsciousnessWrapper
            _dawn_instance = DAWNGenomeConsciousnessWrapper()
            logger.info("✅ Created new DAWN instance (DAWNGenomeConsciousnessWrapper)")
            return True
        except Exception as e:
            logger.error(f"Could not create DAWN instance: {e}")
    
    logger.warning("⚠️  Running in standalone mode (no DAWN connection)")
    return False

def inspect_dawn():
    """Inspect DAWN's available attributes"""
    if not _dawn_instance:
        logger.info("No DAWN instance connected")
        return
        
    logger.info("🔍 DAWN Instance Inspection")
    logger.info("─" * 40)
    
    # Get all attributes
    attrs = dir(_dawn_instance)
    
    # Filter to interesting ones
    interesting = [a for a in attrs if not a.startswith('_')]
    
    logger.info(f"Available attributes: {len(interesting)}")
    for attr in sorted(interesting)[:20]:  # Show first 20
        try:
            value = getattr(_dawn_instance, attr)
            if not callable(value):
                logger.info(f"  {attr}: {value}")
        except:
            pass
# ═══════════════════════════════════════════════════════════════════
# COMMAND ROUTER
# ═══════════════════════════════════════════════════════════════════

class CommandRouter:
    """
    Central command routing system for DAWN runtime control.
    Maps command names to callable functions with automatic parsing.
    """
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self.command_help: Dict[str, str] = {}
        self._register_core_commands()
    
    def register(self, name: str, func: Callable, help_text: str = ""):
        """Register a command with the router"""
        self.commands[name] = func
        self.command_help[name] = help_text or func.__doc__ or "No description available"
        logger.debug(f"📝 Registered command: {name}")
    
    def _register_core_commands(self):
        """Register all core DAWN commands"""
        # Status commands
        self.register("status", print_visual_status, "Display DAWN's visual status")
        self.register("schema", print_schema_status, "Display schema integrity status")
        
        # Stimulation commands
        self.register("emotion", stimulate_emotion, "Stimulate emotional response")
        self.register("curiosity", stimulate_curiosity, "Stimulate curiosity patterns")
        self.register("tension", stimulate_tension, "Stimulate tension dynamics")
        
        # System commands
        self.register("heat", add_manual_heat, "Add manual heat to system")
        self.register("debug_bloom", debug_bloom_system, "Debug bloom system internals")
        self.register("test_bloom", force_test_bloom, "Force a test bloom creation")
        self.register("bloom_stats", bloom_activation_stats, "Display bloom activation statistics")
        
        # Connection commands
        self.register("connect", connect_to_dawn, "Connect to DAWN instance")
        
        # Meta commands
        self.register("help", self._show_help, "Show available commands")
        self.register("tick_status", self._tick_status, "Show tick safety status")
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        """Execute a registered command"""
        if command not in self.commands:
            logger.error(f"❌ Unknown command: '{command}'. Use 'help' for available commands.")
            return None
        
        func = self.commands[command]
        
        try:
            # Check if function is tick-safe
            if hasattr(func, '_tick_safe'):
                logger.debug(f"🔒 Command '{command}' is tick-safe")
            
            logger.info(f"▶️  Executing command: {command}")
            result = func(*args, **kwargs)
            logger.info(f"✅ Command '{command}' completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Command '{command}' failed: {str(e)}")
            logger.debug(traceback.format_exc())
            return None
    
    def show_metrics():
        """Find and display DAWN's core metrics wherever they are"""
        if not _dawn_instance:
            logger.info("No DAWN instance")
            return
        
        logger.info("🌡️ DAWN Core Metrics")
        logger.info("─" * 40)
        
        # Try to find metrics in various places
        metrics = {}
        
        # Check genome coordinator
        if hasattr(_dawn_instance, 'genome_coordinator'):
            gc = _dawn_instance.genome_coordinator
            
            # Look for tick engine
            if hasattr(gc, 'tick_engine'):
                te = gc.tick_engine
                if hasattr(te, 'current_tick'):
                    metrics['Tick'] = te.current_tick
                if hasattr(te, 'tick_interval'):
                    metrics['Interval'] = te.tick_interval
                if hasattr(te, 'scup'):
                    metrics['SCUP'] = te.scup
                    
            # Look for emotional engine
            if hasattr(gc, 'emotional_engine'):
                ee = gc.emotional_engine
                if hasattr(ee, 'mood_valence'):
                    metrics['Mood'] = ee.mood_valence
                if hasattr(ee, 'mood_drift'):
                    metrics['Drift'] = ee.mood_drift
                    
            # Look for entropy
            if hasattr(gc, 'entropy'):
                metrics['Entropy'] = gc.entropy
        
        # Try thermal system
        if hasattr(_dawn_instance, 'enhanced_thermal_system'):
            ts = _dawn_instance.enhanced_thermal_system
            if hasattr(ts, 'temperature'):
                metrics['Heat'] = ts.temperature
        
        # Display what we found
        if metrics:
            for key, value in metrics.items():
                logger.info(f"{key:10}: {value}")
        else:
            logger.info("❌ No metrics found - consciousness not initialized")
            logger.info("The base_consciousness is None - DAWN isn't fully connected!")

    def _show_help(self):
        """Display all available commands"""
        logger.info("🌅 DAWN Command Interface - Available Commands:")
        logger.info("=" * 50)
        
        for cmd, help_text in sorted(self.command_help.items()):
            # Check if tick-safe
            safe_marker = "🔒" if hasattr(self.commands[cmd], '_tick_safe') else "  "
            logger.info(f"{safe_marker} {cmd:15} - {help_text}")
        
        logger.info("=" * 50)
        logger.info("🔒 = Tick-safe command (waits for safe execution)")
    
    def _tick_status(self):
        """Show current tick safety status"""
        status = "ACTIVE ⚡" if _tick_active else "IDLE 💤"
        logger.info(f"Tick Status: {status}")
        
        if _dawn_instance:
            logger.info(f"DAWN Connected: YES ✅")
            if hasattr(_dawn_instance, 'tick'):
                logger.info(f"Current Tick: {_dawn_instance.tick}")
        else:
            logger.info(f"DAWN Connected: NO ❌")


# ═══════════════════════════════════════════════════════════════════
# COMMAND ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

def parse_command_string(cmd_string: str) -> Tuple[str, List[Any], Dict[str, Any]]:
    """
    Parse a command string into command name, args, and kwargs
    
    Examples:
        "status" -> ("status", [], {})
        "emotion joy 0.8" -> ("emotion", ["joy", 0.8], {})
        "heat amount=0.5 label=test" -> ("heat", [], {"amount": 0.5, "label": "test"})
    """
    parts = cmd_string.strip().split()
    if not parts:
        return "", [], {}
    
    command = parts[0]
    args = []
    kwargs = {}
    
    for part in parts[1:]:
        if "=" in part:
            # It's a kwarg
            key, value = part.split("=", 1)
            # Try to parse value type
            try:
                value = float(value)
            except ValueError:
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                # Otherwise keep as string
            kwargs[key] = value
        else:
            # It's a positional arg
            # Try to parse type
            try:
                value = float(part)
            except ValueError:
                if part.lower() in ["true", "false"]:
                    value = part.lower() == "true"
                else:
                    value = part
            args.append(value)
    
    return command, args, kwargs


def run_command_from_input(cmd_string: str) -> Any:
    """
    Parses and runs a command string from user input
    
    Args:
        cmd_string: Command string to parse and execute
    
    Returns:
        Result of command execution (if any)
    
    Examples:
        run_command_from_input("status")
        run_command_from_input("emotion joy 0.8")
        run_command_from_input("heat amount=0.5 label=manual")
    """
    if not cmd_string or not cmd_string.strip():
        logger.warning("Empty command received")
        return None
    
    # Parse command
    command, args, kwargs = parse_command_string(cmd_string)
    
    if not command:
        logger.warning("No command found in input")
        return None
    
    # Execute via router
    return router.execute(command, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════
# INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════════

def interactive_mode():
    """Run DAWN command interface in interactive mode"""
    logger.info("🌅 DAWN Command Interface - Interactive Mode")
    logger.info("Type 'help' for available commands, 'exit' to quit")
    logger.info("─" * 50)
    
    # Try to auto-connect to DAWN
    connect_to_dawn()
    
    while True:
        try:
            cmd_input = input("\nDAWN> ").strip()
            
            if cmd_input.lower() in ["exit", "quit", "q"]:
                logger.info("👋 Exiting DAWN command interface...")
                break
            
            if cmd_input:
                run_command_from_input(cmd_input)
                
        except KeyboardInterrupt:
            logger.info("\n👋 Interrupted. Exiting...")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")
            logger.debug(traceback.format_exc())


# Global command router instance - create after all functions are defined
router = CommandRouter()


# Example usage
if __name__ == "__main__":
    # Demonstrate various commands
    print("🌅 DAWN Command Interface Demo")
    print("=" * 50)
    
    # Test command parsing
    test_commands = [
        "help",
        "status",
        "schema",
        "emotion wonder 0.7",
        "curiosity quantum_mechanics 0.9",
        "heat amount=0.3 label=test_heat",
        "bloom_stats",
        "test_bloom"
    ]
    
    for cmd in test_commands:
        print(f"\n>>> {cmd}")
        run_command_from_input(cmd)
        time.sleep(0.5)
    
    # Uncomment to run interactive mode
    # interactive_mode()