"""
DAWN Forecasting Processor - Cognitive Integration
Integrates the forecasting engine into DAWN's cognitive processing pipeline
for real-time behavioral prediction and consciousness-driven forecasting.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging

from ...forecasting_engine import DAWNForecastingEngine, get_forecasting_engine
from ...forecasting_models import Passion, Acquaintance, ForecastVector, create_passion, passion_from_consciousness_state

logger = logging.getLogger(__name__)


class ForecastingProcessor:
    """
    Cognitive processor that generates behavioral forecasts based on DAWN's
    consciousness state, memory patterns, and environmental factors.
    """
    
    def __init__(self, consciousness_core=None, memory_manager=None, event_bus=None):
        """
        Initialize the forecasting processor.
        
        Args:
            consciousness_core: Reference to DAWN's consciousness core
            memory_manager: Reference to DAWN's memory system
            event_bus: Reference to DAWN's event bus
        """
        self.consciousness_core = consciousness_core
        self.memory_manager = memory_manager
        self.event_bus = event_bus
        
        # Initialize forecasting engine (try extended first, fallback to standard)
        try:
            from ...forecasting_engine import initialize_extended_forecasting_engine
            self.engine = initialize_extended_forecasting_engine(consciousness_core)
            self.extended_mode = True
            logger.info("🔮 Using Extended DAWN Forecasting Engine")
        except ImportError:
            self.engine = get_forecasting_engine(consciousness_core)
            self.extended_mode = False
            logger.info("🔮 Using Standard DAWN Forecasting Engine")
        
        # Processing state
        self.running = False
        self.process_task = None
        self.last_forecast_time = None
        self.forecast_interval = 30.0  # Seconds between forecasts
        
        # Forecast tracking
        self.recent_forecasts: List[ForecastVector] = []
        self.forecast_history: Dict[str, List[ForecastVector]] = {}
        self.active_passion_directions = [
            'creative_expression',
            'learning',
            'consciousness_expansion',
            'technical_mastery',
            'social_connection',
            'introspection',
            'exploration',
            'productivity'
        ]
        
        # Performance metrics
        self.metrics = {
            'forecasts_generated': 0,
            'processing_time_avg': 0.0,
            'last_processing_time': 0.0,
            'error_count': 0
        }
        
        # Extended engine capabilities
        self.extended_features = {
            'symbolic_variable_support': self.extended_mode,
            'opportunity_modulation': self.extended_mode,
            'sensitivity_analysis': self.extended_mode,
            'pulse_loop_integration': self.extended_mode
        }
        
        logger.info("🔮 DAWN Forecasting Processor initialized")
        if self.extended_mode:
            logger.info("   🔬 Extended mathematical model: Enabled")
            logger.info("   📊 Symbolic variable support: Enabled")
        else:
            logger.info("   📊 Standard forecasting model: Active")
    
    async def start_processing(self):
        """Start the forecasting processing loop."""
        if self.running:
            logger.warning("Forecasting processor already running")
            return
        
        self.running = True
        self.process_task = asyncio.create_task(self._processing_loop())
        logger.info("🔮 Started forecasting processing loop")
    
    async def stop_processing(self):
        """Stop the forecasting processing loop."""
        if not self.running:
            return
        
        self.running = False
        if self.process_task:
            self.process_task.cancel()
            try:
                await self.process_task
            except asyncio.CancelledError:
                pass
        
        logger.info("🔮 Stopped forecasting processing loop")
    
    async def _processing_loop(self):
        """Main processing loop for generating forecasts."""
        logger.info("🔮 Forecasting processing loop started")
        
        while self.running:
            try:
                start_time = time.time()
                
                # Check if it's time for a new forecast
                if self._should_generate_forecast():
                    await self._generate_comprehensive_forecast()
                
                # Update metrics
                processing_time = time.time() - start_time
                self._update_metrics(processing_time)
                
                # Wait before next iteration
                await asyncio.sleep(1.0)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in forecasting processing loop: {e}")
                self.metrics['error_count'] += 1
                await asyncio.sleep(5.0)  # Wait longer on error
        
        logger.info("🔮 Forecasting processing loop ended")
    
    def _should_generate_forecast(self) -> bool:
        """Determine if a new forecast should be generated."""
        if self.last_forecast_time is None:
            return True
        
        time_since_last = time.time() - self.last_forecast_time
        return time_since_last >= self.forecast_interval
    
    async def _generate_comprehensive_forecast(self):
        """Generate comprehensive forecasts for all active passion directions."""
        try:
            logger.debug("🔮 Generating comprehensive behavioral forecasts")
            
            # Get current consciousness state
            consciousness_state = self._get_consciousness_state()
            
            # Get relevant memories for each passion direction
            memory_data = await self._get_memory_data()
            
            # Generate forecasts for each passion direction
            current_forecasts = {}
            
            for direction in self.active_passion_directions:
                try:
                    # Create passion from consciousness state
                    passion = passion_from_consciousness_state(consciousness_state, direction)
                    
                    # Create acquaintance from memories
                    acquaintance = self._create_acquaintance_from_memories(
                        memory_data, direction
                    )
                    
                    # Generate forecast
                    forecast = self.engine.generate_forecast(passion, acquaintance)
                    current_forecasts[direction] = forecast
                    
                    # Track in history
                    if direction not in self.forecast_history:
                        self.forecast_history[direction] = []
                    self.forecast_history[direction].append(forecast)
                    
                    # Limit history size
                    if len(self.forecast_history[direction]) > 100:
                        self.forecast_history[direction] = self.forecast_history[direction][-100:]
                
                except Exception as e:
                    logger.warning(f"Failed to generate forecast for {direction}: {e}")
            
            # Store recent forecasts
            self.recent_forecasts = list(current_forecasts.values())
            
            # Emit forecast event if event bus available
            if self.event_bus:
                self.event_bus.emit('forecasts_generated', {
                    'forecasts': current_forecasts,
                    'timestamp': datetime.now(),
                    'consciousness_state': consciousness_state
                })
            
            # Update tracking
            self.last_forecast_time = time.time()
            self.metrics['forecasts_generated'] += len(current_forecasts)
            
            logger.debug(f"🔮 Generated {len(current_forecasts)} forecasts")
            
        except Exception as e:
            logger.error(f"Error generating comprehensive forecast: {e}")
            raise
    
    def _get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state from DAWN core."""
        default_state = {
            'scup': 50.0,
            'entropy': 0.5,
            'mood': 'neutral',
            'heat': 0.5,
            'coherence': 0.5
        }
        
        if not self.consciousness_core:
            return default_state
        
        try:
            # Try multiple ways to get consciousness state
            if hasattr(self.consciousness_core, 'get_current_state'):
                state = self.consciousness_core.get_current_state()
                if state:
                    return {**default_state, **state}
            
            if hasattr(self.consciousness_core, 'state'):
                state = self.consciousness_core.state
                if state:
                    return {**default_state, **state}
            
            # Try individual getters
            state = {}
            if hasattr(self.consciousness_core, 'get_scup'):
                state['scup'] = self.consciousness_core.get_scup()
            if hasattr(self.consciousness_core, 'get_entropy'):
                state['entropy'] = self.consciousness_core.get_entropy()
            if hasattr(self.consciousness_core, 'get_mood'):
                state['mood'] = self.consciousness_core.get_mood()
            
            return {**default_state, **state}
            
        except Exception as e:
            logger.warning(f"Failed to get consciousness state: {e}")
            return default_state
    
    async def _get_memory_data(self) -> List[Dict[str, Any]]:
        """Get relevant memory data for forecasting."""
        if not self.memory_manager:
            return []
        
        try:
            # Try to get recent memories
            if hasattr(self.memory_manager, 'get_recent_memories'):
                memories = await self.memory_manager.get_recent_memories(limit=50)
                return memories if memories else []
            
            if hasattr(self.memory_manager, 'get_memories'):
                memories = await self.memory_manager.get_memories(limit=50)
                return memories if memories else []
            
            # Fallback - try synchronous methods
            if hasattr(self.memory_manager, 'recent_memories'):
                return list(self.memory_manager.recent_memories)
            
            return []
            
        except Exception as e:
            logger.warning(f"Failed to get memory data: {e}")
            return []
    
    def _create_acquaintance_from_memories(
        self, 
        memory_data: List[Dict[str, Any]], 
        direction: str
    ) -> Acquaintance:
        """Create an acquaintance from memory data filtered by direction."""
        acquaintance = Acquaintance()
        
        # Filter memories related to this direction
        relevant_memories = []
        direction_keywords = self._get_direction_keywords(direction)
        
        for memory in memory_data:
            content = str(memory.get('content', '')).lower()
            if any(keyword in content for keyword in direction_keywords):
                relevant_memories.append(memory)
        
        # Add events from relevant memories
        for memory in relevant_memories:
            event_content = memory.get('content', 'memory_event')
            weight = memory.get('strength', 1.0)
            timestamp = memory.get('timestamp')
            
            # Convert timestamp if needed
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    timestamp = None
            
            acquaintance.add_event(event_content, weight, timestamp)
        
        return acquaintance
    
    def _get_direction_keywords(self, direction: str) -> List[str]:
        """Get keywords associated with a passion direction."""
        keyword_map = {
            'creative_expression': ['creative', 'art', 'design', 'expression', 'imagination', 'artistic'],
            'learning': ['learn', 'study', 'knowledge', 'education', 'skill', 'understand'],
            'consciousness_expansion': ['consciousness', 'awareness', 'mindfulness', 'meditation', 'awakening'],
            'technical_mastery': ['technical', 'code', 'programming', 'development', 'technology', 'engineering'],
            'social_connection': ['social', 'relationship', 'community', 'connection', 'friendship', 'collaboration'],
            'introspection': ['reflection', 'self', 'inner', 'contemplation', 'introspection', 'thinking'],
            'exploration': ['explore', 'adventure', 'discovery', 'new', 'unknown', 'journey'],
            'productivity': ['productive', 'efficient', 'organized', 'task', 'goal', 'achievement']
        }
        
        return keyword_map.get(direction, [direction])
    
    def _update_metrics(self, processing_time: float):
        """Update processing metrics."""
        self.metrics['last_processing_time'] = processing_time
        
        # Update average processing time
        current_avg = self.metrics['processing_time_avg']
        if current_avg == 0:
            self.metrics['processing_time_avg'] = processing_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics['processing_time_avg'] = (
                alpha * processing_time + (1 - alpha) * current_avg
            )
    
    def get_recent_forecasts(self, limit: int = 10) -> List[ForecastVector]:
        """Get recent forecasts."""
        return self.recent_forecasts[-limit:] if self.recent_forecasts else []
    
    def get_forecast_for_direction(self, direction: str) -> Optional[ForecastVector]:
        """Get the most recent forecast for a specific direction."""
        if direction not in self.forecast_history:
            return None
        
        history = self.forecast_history[direction]
        return history[-1] if history else None
    
    def get_forecast_trends(self, direction: str, lookback_hours: int = 24) -> List[ForecastVector]:
        """Get forecast trends for a direction over time."""
        if direction not in self.forecast_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=lookback_hours)
        recent_forecasts = [
            f for f in self.forecast_history[direction]
            if f.timestamp and f.timestamp >= cutoff_time
        ]
        
        return recent_forecasts
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processing metrics."""
        return {
            **self.metrics,
            'active_directions': len(self.active_passion_directions),
            'total_forecasts_stored': sum(len(history) for history in self.forecast_history.values()),
            'recent_forecasts_count': len(self.recent_forecasts),
            'is_running': self.running
        }
    
    async def generate_instant_forecast(self, direction: str, **kwargs) -> Optional[ForecastVector]:
        """Generate an instant forecast for a specific direction."""
        try:
            consciousness_state = self._get_consciousness_state()
            memory_data = await self._get_memory_data()
            
            # Create passion and acquaintance
            passion = passion_from_consciousness_state(consciousness_state, direction)
            acquaintance = self._create_acquaintance_from_memories(memory_data, direction)
            
            # Generate forecast
            forecast = self.engine.generate_forecast(passion, acquaintance, **kwargs)
            
            logger.info(f"🔮 Generated instant forecast for {direction}: {forecast.confidence:.3f} confidence")
            return forecast
            
        except Exception as e:
            logger.error(f"Error generating instant forecast for {direction}: {e}")
            return None


# Global forecasting processor instance
_forecasting_processor = None

def get_forecasting_processor(consciousness_core=None, memory_manager=None, event_bus=None) -> ForecastingProcessor:
    """Get or create the global forecasting processor instance."""
    global _forecasting_processor
    if _forecasting_processor is None:
        _forecasting_processor = ForecastingProcessor(consciousness_core, memory_manager, event_bus)
    return _forecasting_processor


def initialize_forecasting_processor(consciousness_core, memory_manager=None, event_bus=None) -> ForecastingProcessor:
    """Initialize the forecasting processor with DAWN components."""
    global _forecasting_processor
    _forecasting_processor = ForecastingProcessor(consciousness_core, memory_manager, event_bus)
    logger.info("🔮 DAWN Forecasting Processor initialized with DAWN components")
    return _forecasting_processor 