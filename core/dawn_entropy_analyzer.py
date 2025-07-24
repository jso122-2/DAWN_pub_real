#!/usr/bin/env python3
"""
DAWN Enhanced Entropy Analyzer
Reactive entropy shift detection with autonomous threshold-based alerting.
Designed for seamless integration with pulse and sigil engines.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

# DAWN Core Integration
try:
    from core.pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    PULSE_CONTROLLER_AVAILABLE = False
    PulseController = None

try:
    from core.sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    SIGIL_ENGINE_AVAILABLE = False
    SigilEngine = None

try:
    from core.entropy_analyzer import EntropyAnalyzer as DAWNEntropyAnalyzer
    DAWN_ENTROPY_AVAILABLE = True
except ImportError:
    DAWN_ENTROPY_AVAILABLE = False
    DAWNEntropyAnalyzer = None

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class EntropyDelta:
    """Entropy change analysis result"""
    current_entropy: float
    previous_entropy: Optional[float]
    delta: Optional[float]
    warning_triggered: bool
    status: str
    analysis_count: int
    timestamp: datetime = field(default_factory=datetime.now)
    thermal_context: Optional[Dict] = None
    sigil_context: Optional[Dict] = None


class EnhancedEntropyAnalyzer:
    """
    Enhanced DAWN Entropy Shift Detection Module
    
    Monitors entropy changes and triggers warnings when rapid increases occur.
    Designed for integration with pulse and sigil engines.
    Extends the original DAWN entropy system with reactive threshold detection.
    """
    
    def __init__(self, pulse_controller: Optional[PulseController] = None,
                 sigil_engine: Optional[SigilEngine] = None,
                 rapid_rise_threshold: float = 0.1,
                 rapid_drop_threshold: float = -0.1):
        """
        Initialize the enhanced entropy analyzer.
        
        Args:
            pulse_controller: DAWN pulse controller for thermal integration
            sigil_engine: DAWN sigil engine for cognitive load tracking
            rapid_rise_threshold: Delta threshold for rapid entropy rise warnings
            rapid_drop_threshold: Delta threshold for significant entropy drops
        """
        # Core entropy tracking
        self.previous_entropy = None
        self.analysis_count = 0
        self.rapid_rise_threshold = rapid_rise_threshold
        self.rapid_drop_threshold = rapid_drop_threshold
        
        # DAWN Integration
        self.pulse_controller = pulse_controller
        self.sigil_engine = sigil_engine
        self.dawn_entropy_analyzer = None
        
        # History tracking
        self.entropy_history: deque = deque(maxlen=1000)
        self.delta_history: deque = deque(maxlen=500)
        self.warning_history: deque = deque(maxlen=100)
        
        # Performance metrics
        self.total_warnings = 0
        self.rapid_rise_events = 0
        self.rapid_drop_events = 0
        self.last_warning_time: Optional[float] = None
        
        # Integration with existing DAWN entropy system
        if DAWN_ENTROPY_AVAILABLE and pulse_controller:
            try:
                self.dawn_entropy_analyzer = DAWNEntropyAnalyzer(
                    pulse_controller=pulse_controller,
                    sigil_engine=sigil_engine
                )
                logger.info("🧬 Enhanced entropy analyzer connected to DAWN entropy system")
            except Exception as e:
                logger.warning(f"Could not connect to DAWN entropy system: {e}")
        
        # Register with pulse controller if available
        if self.pulse_controller and PULSE_CONTROLLER_AVAILABLE:
            self.pulse_controller.set_entropy_analyzer(self)
            logger.info("🔥 Enhanced entropy analyzer registered with pulse controller")
        
        logger.info("🔍 Enhanced DAWN Entropy Analyzer initialized")
    
    def analyze(self, current_entropy: float, source: str = "system") -> EntropyDelta:
        """
        Analyze current entropy against previous value with enhanced detection.
        
        Args:
            current_entropy (float): Current entropy measurement (0.0-1.0)
            source (str): Source of entropy measurement
            
        Returns:
            EntropyDelta: Comprehensive analysis results including delta and warning status
        """
        # Validate input
        current_entropy = max(0.0, min(1.0, current_entropy))
        
        # Create result structure
        result = EntropyDelta(
            current_entropy=current_entropy,
            previous_entropy=self.previous_entropy,
            delta=None,
            warning_triggered=False,
            status='baseline_set',
            analysis_count=self.analysis_count
        )
        
        # Add thermal context if available
        if self.pulse_controller:
            try:
                thermal_stats = self.pulse_controller.get_heat_statistics()
                result.thermal_context = {
                    'current_heat': thermal_stats['current_heat'],
                    'current_zone': thermal_stats['current_zone'],
                    'zone_stability': thermal_stats.get('time_in_zone', 0)
                }
            except Exception as e:
                logger.debug(f"Could not get thermal context: {e}")
        
        # Add sigil context if available
        if self.sigil_engine:
            try:
                result.sigil_context = {
                    'active_sigils': len(self.sigil_engine.active_sigils),
                    'queue_size': len(self.sigil_engine.priority_queue),
                    'engine_running': self.sigil_engine.is_running
                }
            except Exception as e:
                logger.debug(f"Could not get sigil context: {e}")
        
        # First measurement - establish baseline
        if self.previous_entropy is None:
            print(f"🔍 DAWN: Entropy baseline established at {current_entropy:.3f}")
            result.status = 'baseline_set'
            self._log_to_dawn_system(current_entropy, result, source)
        else:
            # Calculate entropy delta
            delta = current_entropy - self.previous_entropy
            result.delta = delta
            result.previous_entropy = self.previous_entropy
            
            # Enhanced threshold analysis
            warning_triggered, status = self._analyze_entropy_shift(
                delta, current_entropy, result.thermal_context
            )
            
            result.warning_triggered = warning_triggered
            result.status = status
            
            # Update warning tracking
            if warning_triggered:
                self.total_warnings += 1
                self.last_warning_time = time.time()
                self.warning_history.append(result)
                
                if delta > self.rapid_rise_threshold:
                    self.rapid_rise_events += 1
                elif delta < self.rapid_drop_threshold:
                    self.rapid_drop_events += 1
        
        # Update state and history
        self.previous_entropy = current_entropy
        self.analysis_count += 1
        self.entropy_history.append(current_entropy)
        if result.delta is not None:
            self.delta_history.append(result.delta)
        
        # Sync with DAWN entropy system
        if self.dawn_entropy_analyzer:
            try:
                self.dawn_entropy_analyzer.add_entropy_sample(
                    bloom_id=f"system_{source}",
                    entropy=current_entropy,
                    source=source
                )
            except Exception as e:
                logger.debug(f"DAWN entropy sync error: {e}")
        
        return result
    
    def _analyze_entropy_shift(self, delta: float, current_entropy: float, 
                              thermal_context: Optional[Dict]) -> tuple[bool, str]:
        """
        Enhanced entropy shift analysis with thermal correlation.
        
        Args:
            delta: Entropy change amount
            current_entropy: Current entropy value
            thermal_context: Current thermal system state
            
        Returns:
            Tuple of (warning_triggered, status_description)
        """
        # Base threshold analysis
        if delta > self.rapid_rise_threshold:
            # Enhanced warning with thermal correlation
            thermal_amplification = 1.0
            if thermal_context and thermal_context.get('current_zone') == 'SURGE':
                thermal_amplification = 1.5
                print("🔥⚠️ Entropy rising rapidly during thermal surge.")
            else:
                print("⚠️ Entropy rising rapidly.")
            
            return True, 'rapid_rise'
            
        elif delta < self.rapid_drop_threshold:
            # Significant entropy drop
            if thermal_context and thermal_context.get('current_zone') == 'CALM':
                print("❄️📉 Entropy dropping significantly during thermal calm.")
            else:
                print("📉 Entropy dropping significantly.")
            return True, 'rapid_drop'
            
        elif abs(delta) < 0.02:
            return False, 'stable'
        elif delta > 0:
            return False, 'gradual_rise'
        else:
            return False, 'gradual_decline'
    
    def _log_to_dawn_system(self, entropy: float, result: EntropyDelta, source: str):
        """Log entropy data to DAWN system components"""
        try:
            # Log to pulse controller thermal system
            if self.pulse_controller:
                # Create thermal awareness data
                awareness_data = {
                    'entropy': entropy,
                    'entropy_delta': result.delta,
                    'warning_triggered': result.warning_triggered,
                    'source': source,
                    'analysis_count': self.analysis_count
                }
                
                # Inject awareness if method exists
                if hasattr(self.pulse_controller, 'inject_entropy_awareness'):
                    self.pulse_controller.inject_entropy_awareness(awareness_data)
            
            # Log to sigil engine if available
            if self.sigil_engine:
                sigil_data = {
                    'system_entropy': entropy,
                    'entropy_trend': result.status,
                    'warning_active': result.warning_triggered
                }
                
                if hasattr(self.sigil_engine, 'inject_entropy_awareness'):
                    self.sigil_engine.inject_entropy_awareness(sigil_data)
                    
        except Exception as e:
            logger.debug(f"DAWN system logging error: {e}")
    
    def reset(self):
        """Reset analyzer state - useful for system restarts."""
        self.previous_entropy = None
        self.analysis_count = 0
        self.entropy_history.clear()
        self.delta_history.clear()
        self.warning_history.clear()
        
        # Reset performance metrics
        self.total_warnings = 0
        self.rapid_rise_events = 0
        self.rapid_drop_events = 0
        self.last_warning_time = None
        
        print("🔄 Enhanced EntropyAnalyzer reset")
        logger.info("Enhanced entropy analyzer state reset")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current analyzer state for system integration."""
        state = {
            'previous_entropy': self.previous_entropy,
            'analysis_count': self.analysis_count,
            'is_initialized': self.previous_entropy is not None,
            'total_warnings': self.total_warnings,
            'rapid_rise_events': self.rapid_rise_events,
            'rapid_drop_events': self.rapid_drop_events,
            'last_warning_time': self.last_warning_time
        }
        
        # Add recent entropy trend
        if len(self.entropy_history) >= 5:
            recent_entropies = list(self.entropy_history)[-5:]
            state['recent_trend'] = 'rising' if recent_entropies[-1] > recent_entropies[0] else 'falling'
            state['recent_volatility'] = max(recent_entropies) - min(recent_entropies)
        
        # Add thermal correlation if available
        if self.pulse_controller:
            try:
                thermal_stats = self.pulse_controller.get_heat_statistics()
                state['thermal_correlation'] = {
                    'current_heat': thermal_stats['current_heat'],
                    'current_zone': thermal_stats['current_zone']
                }
            except Exception:
                pass
        
        return state
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance and diagnostic metrics."""
        return {
            'total_analyses': self.analysis_count,
            'total_warnings': self.total_warnings,
            'rapid_rise_events': self.rapid_rise_events,
            'rapid_drop_events': self.rapid_drop_events,
            'warning_rate': self.total_warnings / max(1, self.analysis_count),
            'last_warning_time': self.last_warning_time,
            'entropy_history_size': len(self.entropy_history),
            'dawn_integration_active': self.dawn_entropy_analyzer is not None,
            'pulse_controller_connected': self.pulse_controller is not None,
            'sigil_engine_connected': self.sigil_engine is not None
        }
    
    def inject_thermal_awareness(self, thermal_data: Dict[str, Any]):
        """
        Receive thermal awareness data from pulse controller.
        This method is called by the pulse controller for bidirectional integration.
        """
        try:
            # Use thermal data to adjust entropy analysis sensitivity
            current_heat = thermal_data.get('heat', 50.0)
            current_zone = thermal_data.get('zone', 'ACTIVE')
            
            # Adjust thresholds based on thermal state
            if current_zone == 'SURGE' and current_heat > 80.0:
                # More sensitive during thermal surges
                self.rapid_rise_threshold = 0.08
                self.rapid_drop_threshold = -0.08
            elif current_zone == 'CALM' and current_heat < 30.0:
                # Less sensitive during calm periods
                self.rapid_rise_threshold = 0.12
                self.rapid_drop_threshold = -0.12
            else:
                # Standard thresholds
                self.rapid_rise_threshold = 0.1
                self.rapid_drop_threshold = -0.1
            
            logger.debug(f"Thermal awareness updated: zone={current_zone}, heat={current_heat:.1f}")
            
        except Exception as e:
            logger.warning(f"Thermal awareness injection failed: {e}")
    
    def inject_sigil_awareness(self, sigil_data: Dict[str, Any]):
        """
        Receive sigil awareness data from sigil engine.
        This method is called by the sigil engine for bidirectional integration.
        """
        try:
            # Use sigil data to understand cognitive load context
            active_sigils = sigil_data.get('active_sigils', [])
            execution_heat = sigil_data.get('execution_heat', 0.0)
            cognitive_house = sigil_data.get('cognitive_house', 'unknown')
            
            # Adjust analysis based on cognitive load
            cognitive_load = len(active_sigils) + (execution_heat / 10.0)
            
            if cognitive_load > 5.0:
                # High cognitive load - expect more entropy fluctuations
                logger.debug(f"High cognitive load detected: {cognitive_load:.1f}")
            
        except Exception as e:
            logger.warning(f"Sigil awareness injection failed: {e}")


# Integration interface for DAWN system
def create_enhanced_entropy_analyzer(pulse_controller: Optional[PulseController] = None,
                                   sigil_engine: Optional[SigilEngine] = None) -> EnhancedEntropyAnalyzer:
    """Factory function for DAWN integration."""
    return EnhancedEntropyAnalyzer(
        pulse_controller=pulse_controller,
        sigil_engine=sigil_engine
    )


# Backward compatibility with original interface
class EntropyAnalyzer(EnhancedEntropyAnalyzer):
    """Backward compatibility wrapper for the original interface"""
    
    def __init__(self):
        super().__init__()
        print("🔍 DAWN: Using enhanced entropy analyzer with backward compatibility")


# Example usage for testing
if __name__ == "__main__":
    # Test the enhanced analyzer
    analyzer = EnhancedEntropyAnalyzer()
    
    # Simulate entropy readings that will trigger warnings
    test_values = [0.2, 0.25, 0.4, 0.35, 0.5]  # Will trigger warning at 0.4
    
    print("🧪 Testing Enhanced Entropy Analyzer")
    print("=" * 50)
    
    for i, entropy in enumerate(test_values):
        result = analyzer.analyze(entropy, source=f"test_{i}")
        print(f"Analysis {i+1}: entropy={entropy:.3f}, delta={result.delta}, status={result.status}")
        if result.warning_triggered:
            print(f"  🚨 WARNING: {result.status}")
        print("-" * 40)
    
    # Display performance metrics
    metrics = analyzer.get_performance_metrics()
    print("\n📊 Performance Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}") 