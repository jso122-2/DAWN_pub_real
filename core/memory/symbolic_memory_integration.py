"""
Symbolic Memory Integration - Bridge between Memory Routing and Symbolic Anatomy
Handles rebloom events and emotional memory processing through symbolic organs
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from ...memory_chunk import MemoryChunk

try:
    from cognitive.symbolic_router import get_symbolic_router
    SYMBOLIC_ROUTER_AVAILABLE = True
except ImportError:
    SYMBOLIC_ROUTER_AVAILABLE = False

logger = logging.getLogger(__name__)


class SymbolicMemoryIntegration:
    """
    Integration layer between DAWN's memory routing system and symbolic anatomy.
    Handles memory reblooms through embodied cognition organs.
    """
    
    def __init__(self, memory_routing_system=None, symbolic_router=None):
        """
        Initialize symbolic memory integration.
        
        Args:
            memory_routing_system: DAWN memory routing system
            symbolic_router: Symbolic anatomy router
        """
        self.memory_routing_system = memory_routing_system
        self.symbolic_router = symbolic_router or (get_symbolic_router() if SYMBOLIC_ROUTER_AVAILABLE else None)
        
        # Integration state
        self.is_active = True
        self.rebloom_count = 0
        self.symbolic_memory_cache = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Register memory event handlers
        if self.memory_routing_system:
            self._register_memory_handlers()
        
        logger.info("🔗 Symbolic memory integration initialized")
        if self.symbolic_router:
            logger.info("   🧠 Symbolic router: ✓")
        if self.memory_routing_system:
            logger.info("   💾 Memory routing: ✓")
    
    def _register_memory_handlers(self):
        """Register event handlers with the memory routing system."""
        try:
            # Handle memory creation events
            self.memory_routing_system.on('memory_created', self._handle_memory_created)
            
            # Handle memory retrieval events  
            self.memory_routing_system.on('memories_retrieved', self._handle_memories_retrieved)
            
            logger.debug("Registered memory event handlers")
        except Exception as e:
            logger.warning(f"Failed to register memory handlers: {e}")
    
    async def _handle_memory_created(self, event_data: Dict[str, Any]) -> None:
        """Handle memory creation events - trigger symbolic rebloom."""
        if not self.is_active or not self.symbolic_router:
            return
        
        try:
            chunk = event_data.get('chunk')
            routing_result = event_data.get('routing_result', {})
            
            if not chunk or not isinstance(chunk, MemoryChunk):
                return
            
            # Process through symbolic anatomy
            symbolic_response = self.symbolic_router.rebloom_trigger(
                memory_chunk=chunk,
                chunk_id=chunk.memory_id
            )
            
            # Cache symbolic response
            self.symbolic_memory_cache[chunk.memory_id] = symbolic_response
            self.rebloom_count += 1
            
            # Emit symbolic rebloom event
            await self._emit_event('symbolic_rebloom', {
                'memory_chunk': chunk,
                'symbolic_response': symbolic_response,
                'routing_result': routing_result
            })
            
            logger.debug(f"Processed symbolic rebloom for memory {chunk.memory_id}")
            
        except Exception as e:
            logger.error(f"Error in symbolic memory creation handler: {e}")
    
    async def _handle_memories_retrieved(self, event_data: Dict[str, Any]) -> None:
        """Handle memory retrieval events - provide symbolic context."""
        if not self.is_active or not self.symbolic_router:
            return
        
        try:
            query = event_data.get('query', '')
            context = event_data.get('context', {})
            results_count = event_data.get('results_count', 0)
            
            # Get current symbolic body state for context
            body_state = self.symbolic_router.get_body_state()
            
            # Add symbolic context to retrieval
            symbolic_context = {
                'query': query,
                'body_state': body_state,
                'results_count': results_count,
                'organ_synergy': body_state['organ_synergy'],
                'symbolic_constellation': body_state['symbolic_state']['constellation']
            }
            
            # Emit symbolic context event
            await self._emit_event('symbolic_retrieval_context', symbolic_context)
            
            logger.debug(f"Provided symbolic context for retrieval: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"Error in symbolic retrieval handler: {e}")
    
    async def process_memory_through_anatomy(self, memory_chunk: MemoryChunk) -> Dict[str, Any]:
        """
        Manually process a memory chunk through symbolic anatomy.
        
        Args:
            memory_chunk: Memory chunk to process
            
        Returns:
            Dict[str, Any]: Symbolic processing response
        """
        if not self.symbolic_router:
            return {'error': 'Symbolic router not available'}
        
        try:
            response = self.symbolic_router.rebloom_trigger(
                memory_chunk=memory_chunk,
                chunk_id=memory_chunk.memory_id
            )
            
            # Cache the response
            self.symbolic_memory_cache[memory_chunk.memory_id] = response
            self.rebloom_count += 1
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing memory through anatomy: {e}")
            return {'error': str(e)}
    
    def get_symbolic_memory_context(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Get symbolic context for a memory by ID.
        
        Args:
            memory_id: Memory identifier
            
        Returns:
            Optional[Dict[str, Any]]: Symbolic context or None
        """
        return self.symbolic_memory_cache.get(memory_id)
    
    def get_current_body_state(self) -> Dict[str, Any]:
        """Get current symbolic body state."""
        if not self.symbolic_router:
            return {'error': 'Symbolic router not available'}
        
        return self.symbolic_router.get_body_state()
    
    def get_somatic_commentary(self) -> str:
        """Get current somatic commentary from symbolic anatomy."""
        if not self.symbolic_router:
            return "Symbolic anatomy unavailable."
        
        try:
            body_state = self.symbolic_router.get_body_state()
            return body_state['symbolic_state']['somatic_commentary']
        except Exception as e:
            logger.warning(f"Failed to get somatic commentary: {e}")
            return "Unable to access somatic state."
    
    def get_symbolic_constellation(self) -> str:
        """Get current symbolic constellation."""
        if not self.symbolic_router:
            return "○○○"  # Default neutral constellation
        
        try:
            body_state = self.symbolic_router.get_body_state()
            return body_state['symbolic_state']['constellation']
        except Exception as e:
            logger.warning(f"Failed to get symbolic constellation: {e}")
            return "○○○"
    
    async def _emit_event(self, event_name: str, data: Dict[str, Any]) -> None:
        """Emit an event to registered handlers."""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    logger.warning(f"Symbolic event handler error for {event_name}: {e}")
    
    def on(self, event_name: str, handler: Callable) -> None:
        """Register an event handler."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)
        logger.debug(f"Registered symbolic handler for event: {event_name}")
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration statistics."""
        stats = {
            'is_active': self.is_active,
            'rebloom_count': self.rebloom_count,
            'cached_memories': len(self.symbolic_memory_cache),
            'integrations': {
                'symbolic_router': self.symbolic_router is not None,
                'memory_routing': self.memory_routing_system is not None
            }
        }
        
        # Add symbolic router stats if available
        if self.symbolic_router:
            router_stats = self.symbolic_router.get_routing_statistics()
            stats['symbolic_router_stats'] = router_stats
        
        return stats
    
    def activate(self):
        """Activate symbolic memory integration."""
        self.is_active = True
        logger.info("🔗 Symbolic memory integration activated")
    
    def deactivate(self):
        """Deactivate symbolic memory integration."""
        self.is_active = False
        logger.info("🔗 Symbolic memory integration deactivated")


# Global instance for DAWN integration
_symbolic_memory_integration: Optional[SymbolicMemoryIntegration] = None


def get_symbolic_memory_integration() -> Optional[SymbolicMemoryIntegration]:
    """Get the global symbolic memory integration instance."""
    return _symbolic_memory_integration


def initialize_symbolic_memory_integration(memory_routing_system=None, symbolic_router=None) -> SymbolicMemoryIntegration:
    """Initialize the global symbolic memory integration."""
    global _symbolic_memory_integration
    _symbolic_memory_integration = SymbolicMemoryIntegration(
        memory_routing_system=memory_routing_system,
        symbolic_router=symbolic_router
    )
    return _symbolic_memory_integration


# Convenience functions for direct integration
async def process_memory_symbolically(memory_chunk: MemoryChunk) -> Dict[str, Any]:
    """Process a memory chunk through symbolic anatomy."""
    integration = get_symbolic_memory_integration()
    if integration:
        return await integration.process_memory_through_anatomy(memory_chunk)
    return {'error': 'Symbolic integration not available'}


def get_current_somatic_commentary() -> str:
    """Get current somatic commentary."""
    integration = get_symbolic_memory_integration()
    if integration:
        return integration.get_somatic_commentary()
    return "Symbolic integration not available."


def get_current_symbolic_constellation() -> str:
    """Get current symbolic constellation."""
    integration = get_symbolic_memory_integration()
    if integration:
        return integration.get_symbolic_constellation()
    return "○○○" 