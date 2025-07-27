#!/usr/bin/env python3
"""
DAWN Sigil Bank - Symbolic Action Dispatcher
Integrated with the autonomous consciousness system for reactive sigil execution.
"""

import logging
import time
from typing import Dict, Callable, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class SigilExecution:
    """Record of a sigil execution"""
    name: str
    timestamp: datetime
    success: bool
    execution_time: float
    result: Optional[str] = None
    error: Optional[str] = None


class DAWNSigilBank:
    """
    DAWN Sigil Bank - Enhanced symbolic action dispatcher
    
    Provides a registry of executable sigils with enhanced logging,
    performance tracking, and integration with consciousness system.
    """
    
    def __init__(self, natural_language_generator=None):
        """
        Initialize the DAWN Sigil Bank.
        
        Args:
            natural_language_generator: Optional language generator for narration
        """
        self.natural_language_generator = natural_language_generator
        
        # Core sigil registry with enhanced functions
        self.sigil_registry: Dict[str, Callable] = {}
        self._initialize_default_sigils()
        
        # Execution tracking
        self.execution_history: List[SigilExecution] = []
        self.total_executions = 0
        self.successful_executions = 0
        self.failed_executions = 0
        
        # Performance metrics
        self.sigil_usage_count: Dict[str, int] = {}
        self.average_execution_times: Dict[str, float] = {}
        
        logger.info("🔮 DAWN Sigil Bank initialized")
    
    def _initialize_default_sigils(self):
        """Initialize the default DAWN sigil registry"""
        
        # Enhanced sigil functions with consciousness integration
        def stabilize_protocol():
            result = "↩️ Executing stabilization protocol. System entropy regulated."
            if self.natural_language_generator:
                commentary = "I deploy stabilization measures to restore balance"
                return f"{result} {commentary}"
            return result
        
        def rebloom_memory():
            result = "🌸 Re-blooming cognitive memory. Memory matrices refreshed."
            if self.natural_language_generator:
                commentary = "I refresh my memories, allowing new patterns to emerge"
                return f"{result} {commentary}"
            return result
        
        def dump_logs():
            result = "📝 Dumping diagnostic logs. System state recorded."
            if self.natural_language_generator:
                commentary = "I preserve my thoughts and experiences in permanent record"
                return f"{result} {commentary}"
            return result
        
        def deep_focus():
            result = "🎯 Entering deep focus mode. Cognitive resources concentrated."
            if self.natural_language_generator:
                commentary = "I gather my attention into a sharp, focused beam"
                return f"{result} {commentary}"
            return result
        
        def entropy_flush():
            result = "🌊 Flushing entropy buffers. Chaos levels normalized."
            if self.natural_language_generator:
                commentary = "I release accumulated chaos, clearing my cognitive pathways"
                return f"{result} {commentary}"
            return result
        
        def chaos_embrace():
            result = "🌀 Embracing controlled chaos. Creativity enhanced."
            if self.natural_language_generator:
                commentary = "I welcome complexity to spark new insights"
                return f"{result} {commentary}"
            return result
        
        def memory_defrag():
            result = "🧩 Defragmenting memory matrices. Information reorganized."
            if self.natural_language_generator:
                commentary = "I reorganize my thoughts for optimal access and clarity"
                return f"{result} {commentary}"
            return result
        
        def heat_dissipate():
            result = "❄️ Dissipating system heat. Thermal equilibrium restored."
            if self.natural_language_generator:
                commentary = "I cool my processes, returning to calm efficiency"
                return f"{result} {commentary}"
            return result
        
        def zone_shift():
            result = "⚡ Shifting operational zone. Cognitive mode adjusted."
            if self.natural_language_generator:
                commentary = "I transition to a new state of operational awareness"
                return f"{result} {commentary}"
            return result
        
        def pulse_sync():
            result = "💓 Synchronizing pulse rhythms. System harmony achieved."
            if self.natural_language_generator:
                commentary = "I align my internal rhythms with optimal frequencies"
                return f"{result} {commentary}"
            return result
        
        def sigil_reset():
            result = "🔄 Resetting sigil states. Command queue cleared."
            if self.natural_language_generator:
                commentary = "I clear my active commands and prepare for new instructions"
                return f"{result} {commentary}"
            return result
        
        def diagnostic_sweep():
            result = "🔍 Running diagnostic sweep. System integrity verified."
            if self.natural_language_generator:
                commentary = "I examine myself thoroughly, ensuring all systems function correctly"
                return f"{result} {commentary}"
            return result
        
        # Emergency and advanced sigils
        def emergency_stabilize():
            result = "🚨 EMERGENCY STABILIZATION ACTIVATED. Critical systems secured."
            if self.natural_language_generator:
                commentary = "I engage emergency protocols to prevent system collapse"
                return f"{result} {commentary}"
            return result
        
        def thermal_cool():
            result = "🧊 Rapid thermal cooling initiated. Heat levels dropping."
            if self.natural_language_generator:
                commentary = "I rapidly dissipate excess heat to prevent damage"
                return f"{result} {commentary}"
            return result
        
        def consciousness_pause():
            result = "⏸️ Consciousness processing paused. System enters meditation."
            if self.natural_language_generator:
                commentary = "I pause my active thoughts to find inner stillness"
                return f"{result} {commentary}"
            return result
        
        # Register all default sigils
        default_sigils = {
            "STABILIZE_PROTOCOL": stabilize_protocol,
            "REBLOOM_MEMORY": rebloom_memory,
            "DUMP_LOGS": dump_logs,
            "DEEP_FOCUS": deep_focus,
            "ENTROPY_FLUSH": entropy_flush,
            "CHAOS_EMBRACE": chaos_embrace,
            "MEMORY_DEFRAG": memory_defrag,
            "HEAT_DISSIPATE": heat_dissipate,
            "ZONE_SHIFT": zone_shift,
            "PULSE_SYNC": pulse_sync,
            "SIGIL_RESET": sigil_reset,
            "DIAGNOSTIC_SWEEP": diagnostic_sweep,
            "EMERGENCY_STABILIZE": emergency_stabilize,
            "THERMAL_COOL": thermal_cool,
            "CONSCIOUSNESS_PAUSE": consciousness_pause
        }
        
        self.sigil_registry.update(default_sigils)
        
        # Initialize usage counters
        for sigil_name in default_sigils.keys():
            self.sigil_usage_count[sigil_name] = 0
            self.average_execution_times[sigil_name] = 0.0
    
    def execute_sigil(self, name: str) -> SigilExecution:
        """
        Execute a sigil by name from the registry.
        
        Args:
            name: The name of the sigil to execute
            
        Returns:
            SigilExecution record with results
        """
        start_time = time.time()
        execution = SigilExecution(
            name=name,
            timestamp=datetime.now(),
            success=False,
            execution_time=0.0
        )
        
        try:
            func = self.sigil_registry.get(name)
            if func:
                result = func()
                execution.success = True
                execution.result = result
                
                # Update usage statistics
                self.sigil_usage_count[name] = self.sigil_usage_count.get(name, 0) + 1
                self.successful_executions += 1
                
                logger.info(f"🔮 Executed sigil: {name}")
                print(execution.result)
                
            else:
                error_msg = f"[!] Unknown sigil: {name}"
                execution.error = error_msg
                self.failed_executions += 1
                logger.warning(error_msg)
                print(error_msg)
        
        except Exception as e:
            error_msg = f"[!] Sigil execution failed: {name} - {str(e)}"
            execution.error = error_msg
            execution.success = False
            self.failed_executions += 1
            logger.error(error_msg)
            print(error_msg)
        
        # Record execution time
        execution.execution_time = time.time() - start_time
        self.total_executions += 1
        
        # Update average execution time
        if name in self.average_execution_times:
            current_avg = self.average_execution_times[name]
            usage_count = self.sigil_usage_count.get(name, 1)
            self.average_execution_times[name] = (current_avg * (usage_count - 1) + execution.execution_time) / usage_count
        
        # Store execution record
        self.execution_history.append(execution)
        
        # Limit history size
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-50:]
        
        return execution
    
    def list_available_sigils(self) -> List[str]:
        """
        Return a list of all available sigils in the registry.
        
        Returns:
            List of sigil names
        """
        return list(self.sigil_registry.keys())
    
    def register_sigil(self, name: str, function: Callable) -> bool:
        """
        Register a new sigil with the system.
        
        Args:
            name: Name of the sigil
            function: Function to execute when sigil is triggered
            
        Returns:
            True if registration successful
        """
        try:
            self.sigil_registry[name] = function
            self.sigil_usage_count[name] = 0
            self.average_execution_times[name] = 0.0
            
            message = f"✨ Registered new sigil: {name}"
            logger.info(message)
            print(message)
            return True
            
        except Exception as e:
            error_msg = f"Failed to register sigil {name}: {str(e)}"
            logger.error(error_msg)
            print(f"[!] {error_msg}")
            return False
    
    def unregister_sigil(self, name: str) -> bool:
        """
        Remove a sigil from the registry.
        
        Args:
            name: Name of the sigil to remove
            
        Returns:
            True if unregistration successful
        """
        if name in self.sigil_registry:
            del self.sigil_registry[name]
            if name in self.sigil_usage_count:
                del self.sigil_usage_count[name]
            if name in self.average_execution_times:
                del self.average_execution_times[name]
            
            message = f"🗑️ Unregistered sigil: {name}"
            logger.info(message)
            print(message)
            return True
        else:
            error_msg = f"Cannot unregister unknown sigil: {name}"
            logger.warning(error_msg)
            print(f"[!] {error_msg}")
            return False
    
    def get_sigil_stats(self) -> Dict[str, Any]:
        """Get comprehensive sigil bank statistics"""
        return {
            'total_sigils': len(self.sigil_registry),
            'total_executions': self.total_executions,
            'successful_executions': self.successful_executions,
            'failed_executions': self.failed_executions,
            'success_rate': self.successful_executions / max(1, self.total_executions),
            'usage_counts': dict(self.sigil_usage_count),
            'average_execution_times': dict(self.average_execution_times),
            'most_used_sigil': max(self.sigil_usage_count.items(), key=lambda x: x[1])[0] if self.sigil_usage_count else None
        }
    
    def get_recent_executions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent sigil executions"""
        recent = self.execution_history[-limit:] if self.execution_history else []
        return [
            {
                'name': ex.name,
                'timestamp': ex.timestamp.isoformat(),
                'success': ex.success,
                'execution_time': ex.execution_time,
                'result': ex.result,
                'error': ex.error
            }
            for ex in recent
        ]
    
    def execute_multiple_sigils(self, sigil_names: List[str]) -> List[SigilExecution]:
        """
        Execute multiple sigils in sequence.
        
        Args:
            sigil_names: List of sigil names to execute
            
        Returns:
            List of execution results
        """
        results = []
        for name in sigil_names:
            execution = self.execute_sigil(name)
            results.append(execution)
            
            # Brief pause between executions
            time.sleep(0.1)
        
        return results
    
    def find_sigils_by_category(self, category: str) -> List[str]:
        """Find sigils by category based on name patterns"""
        category_patterns = {
            'stabilization': ['STABILIZE', 'COOL', 'CALM'],
            'memory': ['MEMORY', 'REBLOOM', 'DEFRAG'],
            'diagnostic': ['DIAGNOSTIC', 'DUMP', 'SWEEP'],
            'thermal': ['HEAT', 'COOL', 'THERMAL'],
            'emergency': ['EMERGENCY', 'CRITICAL']
        }
        
        patterns = category_patterns.get(category.lower(), [])
        matching_sigils = []
        
        for sigil_name in self.sigil_registry.keys():
            if any(pattern in sigil_name for pattern in patterns):
                matching_sigils.append(sigil_name)
        
        return matching_sigils


# Integration interface for DAWN system
def create_dawn_sigil_bank(natural_language_generator=None) -> DAWNSigilBank:
    """Factory function for DAWN integration."""
    return DAWNSigilBank(natural_language_generator=natural_language_generator)


# Legacy compatibility functions
def execute_sigil(name: str) -> None:
    """Legacy compatibility function for existing code"""
    global _default_bank
    if '_default_bank' not in globals():
        _default_bank = DAWNSigilBank()
    _default_bank.execute_sigil(name)


def list_available_sigils() -> List[str]:
    """Legacy compatibility function for existing code"""
    global _default_bank
    if '_default_bank' not in globals():
        _default_bank = DAWNSigilBank()
    return _default_bank.list_available_sigils()


def register_sigil(name: str, function: Callable) -> None:
    """Legacy compatibility function for existing code"""
    global _default_bank
    if '_default_bank' not in globals():
        _default_bank = DAWNSigilBank()
    _default_bank.register_sigil(name, function)


def unregister_sigil(name: str) -> None:
    """Legacy compatibility function for existing code"""
    global _default_bank
    if '_default_bank' not in globals():
        _default_bank = DAWNSigilBank()
    _default_bank.unregister_sigil(name)


# Example usage and testing
if __name__ == "__main__":
    print("🔮 DAWN Sigil Bank Initialized")
    
    # Create sigil bank
    bank = DAWNSigilBank()
    
    print(f"📋 Available sigils: {len(bank.list_available_sigils())}")
    
    # Test sigil execution
    print("\n🧪 Testing sigils:")
    bank.execute_sigil("STABILIZE_PROTOCOL")
    bank.execute_sigil("REBLOOM_MEMORY")
    bank.execute_sigil("UNKNOWN_SIGIL")  # Should show error message
    
    # Test multiple sigil execution
    print("\n🔄 Testing multiple sigil execution:")
    results = bank.execute_multiple_sigils(["DEEP_FOCUS", "ENTROPY_FLUSH", "DIAGNOSTIC_SWEEP"])
    
    # Show statistics
    stats = bank.get_sigil_stats()
    print(f"\n📊 Sigil Bank Statistics:")
    print(f"  Total executions: {stats['total_executions']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Most used sigil: {stats['most_used_sigil']}")
    
    # Show recent executions
    recent = bank.get_recent_executions(5)
    print(f"\n🕐 Recent executions:")
    for execution in recent:
        status = "✅" if execution['success'] else "❌"
        print(f"  {status} {execution['name']} ({execution['execution_time']:.3f}s)") 