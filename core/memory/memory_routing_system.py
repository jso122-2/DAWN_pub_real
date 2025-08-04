"""
DAWN Memory Routing System - Unified Memory Management
Integrates MemoryChunk-based routing with DAWN's existing memory infrastructure.
Provides routing, persistence, and retrieval for DAWN's consciousness system.
"""

import logging
import asyncio
import time
from typing import Dict, List, Optional, Any, Set, Callable
from datetime import datetime, timedelta
from collections import deque, defaultdict
from pathlib import Path
import threading

from ...memory_chunk import MemoryChunk, create_memory_now, memory_stats
from ...memory_loader import DAWNMemoryLoader
from ...cognitive_router import CognitiveRouter
from ...vector_index import DAWNVectorIndex, IndexConfig

# Integration with existing DAWN memory systems
try:
    from ...memory_trace_log import EnhancedMemoryTraceLog
    TRACE_LOG_AVAILABLE = True
except ImportError:
    TRACE_LOG_AVAILABLE = False

try:
    from ...memory_anchor import MemoryAnchorSystem, AnchorType
    MEMORY_ANCHOR_AVAILABLE = True
except ImportError:
    MEMORY_ANCHOR_AVAILABLE = False

try:
    from ...pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    PULSE_CONTROLLER_AVAILABLE = False

logger = logging.getLogger(__name__)


class MemoryRouter:
    """
    Core memory routing component that decides where and how memories are stored.
    Integrates with DAWN's pulse system, entropy tracking, and sigil system.
    """
    
    def __init__(self, 
                 max_active_memories: int = 5000,
                 importance_threshold: float = 0.3,
                 pulse_controller: Optional['PulseController'] = None,
                 enable_cognitive_routing: bool = True,
                 enable_vector_search: bool = True):
        """
        Initialize the enhanced memory router.
        
        Args:
            max_active_memories: Maximum memories to keep in active routing
            importance_threshold: Minimum importance for memory retention
            pulse_controller: Optional pulse controller for thermal awareness
            enable_cognitive_routing: Enable cognitive routing capabilities
            enable_vector_search: Enable vector-based semantic search
        """
        self.max_active_memories = max_active_memories
        self.importance_threshold = importance_threshold
        self.pulse_controller = pulse_controller
        
        # Enhanced routing components
        self.cognitive_router = CognitiveRouter() if enable_cognitive_routing else None
        self.vector_index = DAWNVectorIndex() if enable_vector_search else None
        
        # Active memory pools (legacy support)
        self.working_memory: deque = deque(maxlen=50)  # High-priority active memories
        self.recent_memories: deque = deque(maxlen=200)  # Recently created memories
        self.significant_memories: List[MemoryChunk] = []  # High-importance memories
        
        # Routing rules and patterns
        self.routing_rules: Dict[str, Callable] = {}
        self.speaker_patterns: Dict[str, List[str]] = defaultdict(list)
        self.topic_patterns: Dict[str, Set[str]] = defaultdict(set)
        self.sigil_patterns: Dict[str, Set[str]] = defaultdict(set)
        
        # Performance tracking
        self.routing_decisions = 0
        self.memory_hits = 0
        self.memory_misses = 0
        self.rebloom_requests = 0
        self.vector_searches = 0
        
        # Thread safety
        self.lock = threading.RLock()
        
        logger.info("🔄 Enhanced memory router initialized")
        if self.cognitive_router:
            logger.info("   🧠 Cognitive routing: ✓")
        if self.vector_index:
            logger.info("   🔍 Vector search: ✓")
    
    def route_memory(self, chunk: MemoryChunk) -> Dict[str, bool]:
        """
        Route a memory chunk to appropriate storage systems.
        Enhanced with cognitive routing and vector indexing.
        
        Args:
            chunk: Memory chunk to route
            
        Returns:
            dict: Routing decisions made
        """
        with self.lock:
            routing_result = {
                'working_memory': False,
                'recent_memory': False,
                'significant_memory': False,
                'cognitive_stored': False,
                'vector_indexed': False,
                'trace_logged': False,
                'anchor_created': False
            }
            
            self.routing_decisions += 1
            
            # Calculate memory importance
            importance = self._calculate_importance(chunk)
            
            # Route to cognitive router
            if self.cognitive_router:
                try:
                    chunk_id = self.cognitive_router.add_chunk(chunk)
                    routing_result['cognitive_stored'] = True
                    logger.debug(f"Routed {chunk.memory_id} to cognitive router as {chunk_id[:8]}...")
                except Exception as e:
                    logger.warning(f"Failed to route to cognitive router: {e}")
            
            # Add to vector index for semantic search
            if self.vector_index:
                try:
                    self.vector_index.add(chunk)
                    routing_result['vector_indexed'] = True
                    logger.debug(f"Added {chunk.memory_id} to vector index")
                except Exception as e:
                    logger.warning(f"Failed to add to vector index: {e}")
            
            # Legacy routing (maintain compatibility)
            # Route to working memory if high importance or recent interaction
            if importance > 0.7 or self._is_recent_interaction(chunk):
                self.working_memory.append(chunk)
                routing_result['working_memory'] = True
                logger.debug(f"Routed {chunk.memory_id} to working memory (importance: {importance:.3f})")
            
            # Always route to recent memory
            self.recent_memories.append(chunk)
            routing_result['recent_memory'] = True
            
            # Route to significant memory if above threshold
            if importance > self.importance_threshold:
                self.significant_memories.append(chunk)
                routing_result['significant_memory'] = True
                
                # Prune significant memories if too many
                if len(self.significant_memories) > self.max_active_memories // 10:
                    self.significant_memories.sort(key=self._calculate_importance, reverse=True)
                    self.significant_memories = self.significant_memories[:self.max_active_memories // 10]
            
            # Update routing patterns
            self._update_routing_patterns(chunk)
            
            logger.debug(f"Memory {chunk.memory_id} routed with importance {importance:.3f}")
            return routing_result
    
    def retrieve_memories(self, 
                         query: str,
                         context: Optional[Dict[str, Any]] = None,
                         max_results: int = 10,
                         use_vector_search: bool = True,
                         use_cognitive_search: bool = True) -> List[MemoryChunk]:
        """
        Retrieve relevant memories based on query and context.
        Enhanced with cognitive routing and vector search capabilities.
        
        Args:
            query: Search query
            context: Optional context for relevance scoring
            max_results: Maximum number of results to return
            use_vector_search: Use vector-based semantic search
            use_cognitive_search: Use cognitive routing for rebloom candidates
            
        Returns:
            List[MemoryChunk]: Retrieved memories sorted by relevance
        """
        with self.lock:
            all_results = []
            
            # Vector search (semantic similarity)
            if use_vector_search and self.vector_index:
                try:
                    self.vector_searches += 1
                    
                    # Check for pulse state context for enhanced search
                    if context and 'pulse_state' in context:
                        vector_results = self.vector_index.search_with_pulse_state(
                            query, context['pulse_state'], max_results
                        )
                    # Check for filtering context
                    elif context and any(k in context for k in ['speaker', 'topic', 'mood']):
                        vector_results = self.vector_index.search_with_filters(
                            query, 
                            speaker=context.get('speaker'),
                            topic=context.get('topic'),
                            mood=context.get('mood'),
                            top_k=max_results
                        )
                    else:
                        vector_results = self.vector_index.search(query, max_results)
                    
                    # Convert SearchResults to MemoryChunks
                    vector_memories = [result.chunk for result in vector_results]
                    all_results.extend(vector_memories)
                    
                    logger.debug(f"Vector search found {len(vector_memories)} results")
                    
                except Exception as e:
                    logger.warning(f"Vector search failed: {e}")
            
            # Cognitive search (rebloom candidates)
            if use_cognitive_search and self.cognitive_router and all_results:
                try:
                    self.rebloom_requests += 1
                    
                    # Use the first vector result as query for rebloom
                    query_chunk = all_results[0]
                    rebloom_candidates = self.cognitive_router.rebloom_candidates(
                        query_chunk, max_candidates=max_results // 2
                    )
                    all_results.extend(rebloom_candidates)
                    
                    logger.debug(f"Cognitive rebloom found {len(rebloom_candidates)} candidates")
                    
                except Exception as e:
                    logger.warning(f"Cognitive search failed: {e}")
            
            # Legacy search (fallback and compatibility)
            legacy_candidates = []
            
            # Search working memory first (highest priority)
            legacy_candidates.extend(self.working_memory)
            
            # Search significant memories
            legacy_candidates.extend(self.significant_memories)
            
            # Search recent memories
            legacy_candidates.extend(self.recent_memories)
            
            # Score and filter legacy candidates
            scored_memories = []
            for chunk in legacy_candidates:
                score = self._calculate_relevance_score(chunk, query, context)
                if score > 0.1:  # Minimum relevance threshold
                    scored_memories.append((chunk, score))
            
            # Add legacy results
            legacy_results = [chunk for chunk, score in scored_memories]
            all_results.extend(legacy_results)
            
            # Remove duplicates (by memory_id)
            seen_ids = set()
            unique_results = []
            for chunk in all_results:
                chunk_id = getattr(chunk, 'memory_id', id(chunk))
                if chunk_id not in seen_ids:
                    seen_ids.add(chunk_id)
                    unique_results.append(chunk)
            
            # Limit results
            final_results = unique_results[:max_results]
            
            # Update hit/miss statistics
            if final_results:
                self.memory_hits += 1
            else:
                self.memory_misses += 1
            
            logger.debug(f"Retrieved {len(final_results)} memories for query: {query[:50]}...")
            return final_results
    
    def _calculate_importance(self, chunk: MemoryChunk) -> float:
        """Calculate the importance score for a memory chunk."""
        importance = 0.0
        
        # Base importance from content length and complexity
        content_score = min(1.0, len(chunk.content) / 500.0)
        importance += content_score * 0.2
        
        # Entropy contribution (higher entropy = more important)
        entropy_score = chunk.get_entropy()
        importance += entropy_score * 0.3
        
        # Heat contribution (thermal significance)
        heat_score = chunk.get_heat() / 100.0  # Normalize heat
        importance += heat_score * 0.2
        
        # SCUP contribution (consciousness unity)
        scup_score = abs(chunk.get_scup() - 0.5) * 2  # Distance from neutral
        importance += scup_score * 0.15
        
        # Sigil presence (symbolic significance)
        sigil_score = min(1.0, len(chunk.sigils) / 3.0)
        importance += sigil_score * 0.1
        
        # Speaker significance
        speaker_multiplier = {
            'dawn.core': 1.2,
            'j.orloff': 1.1,
            'owl.system': 1.15,
            'user': 0.9
        }.get(chunk.speaker, 1.0)
        
        importance *= speaker_multiplier
        
        # Topic significance
        if chunk.topic in ['system_event', 'critical_state', 'breakthrough', 'error']:
            importance *= 1.3
        elif chunk.topic in ['reflection', 'introspection']:
            importance *= 1.1
        
        return min(1.0, importance)
    
    def _calculate_relevance_score(self, chunk: MemoryChunk, query: str, context: Optional[Dict] = None) -> float:
        """Calculate relevance score for a memory chunk given a query."""
        score = 0.0
        query_lower = query.lower()
        
        # Content matching
        content_lower = chunk.content.lower()
        if query_lower in content_lower:
            score += 0.5
        
        # Word overlap
        query_words = set(query_lower.split())
        content_words = set(content_lower.split())
        overlap = len(query_words & content_words)
        if query_words:
            score += (overlap / len(query_words)) * 0.3
        
        # Topic matching
        if chunk.topic and chunk.topic.lower() in query_lower:
            score += 0.2
        
        # Speaker matching
        if chunk.speaker.lower() in query_lower:
            score += 0.1
        
        # Context matching if provided
        if context:
            if 'mood' in context and chunk.get_mood() == context['mood']:
                score += 0.1
            if 'entropy_range' in context:
                min_e, max_e = context['entropy_range']
                if min_e <= chunk.get_entropy() <= max_e:
                    score += 0.1
        
        # Recency bonus (more recent = more relevant)
        age_hours = (datetime.now() - chunk.timestamp).total_seconds() / 3600
        recency_bonus = max(0, 1 - age_hours / 168)  # Decay over a week
        score += recency_bonus * 0.1
        
        # Importance bonus
        importance = self._calculate_importance(chunk)
        score += importance * 0.1
        
        return min(1.0, score)
    
    def _is_recent_interaction(self, chunk: MemoryChunk) -> bool:
        """Check if this memory represents a recent interaction."""
        time_threshold = datetime.now() - timedelta(minutes=30)
        return chunk.timestamp > time_threshold
    
    def _update_routing_patterns(self, chunk: MemoryChunk) -> None:
        """Update routing patterns based on memory chunk."""
        # Update speaker patterns
        if chunk.topic:
            self.speaker_patterns[chunk.speaker].append(chunk.topic)
        
        # Update topic patterns
        self.topic_patterns[chunk.topic or 'general'].update(chunk.sigils)
        
        # Update sigil patterns
        for sigil in chunk.sigils:
            self.sigil_patterns[sigil].add(chunk.speaker)
    
    def rebloom_candidates(self, query_chunk: MemoryChunk, max_candidates: int = 10) -> List[MemoryChunk]:
        """
        Find memory chunks related to the query chunk using cognitive routing.
        
        Args:
            query_chunk: Memory chunk to find relations for
            max_candidates: Maximum number of candidates to return
            
        Returns:
            List[MemoryChunk]: List of related memory chunks
        """
        if self.cognitive_router:
            self.rebloom_requests += 1
            return self.cognitive_router.rebloom_candidates(query_chunk, max_candidates)
        return []
    
    def vector_search(self, query: str, top_k: int = 5, context: Optional[Dict] = None) -> List[MemoryChunk]:
        """
        Perform vector-based semantic search.
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            context: Optional context for enhanced search
            
        Returns:
            List[MemoryChunk]: Semantically similar memory chunks
        """
        if self.vector_index:
            self.vector_searches += 1
            
            if context and 'pulse_state' in context:
                results = self.vector_index.search_with_pulse_state(query, context['pulse_state'], top_k)
            elif context and any(k in context for k in ['speaker', 'topic', 'mood']):
                results = self.vector_index.search_with_filters(
                    query,
                    speaker=context.get('speaker'),
                    topic=context.get('topic'),
                    mood=context.get('mood'),
                    top_k=top_k
                )
            else:
                results = self.vector_index.search(query, top_k)
            
            return [result.chunk for result in results]
        return []
    
    def compress_memories(self) -> Dict[str, Any]:
        """
        Generate a compressed representation of all stored memories.
        
        Returns:
            Dict[str, Any]: Compressed memory representation
        """
        if self.cognitive_router:
            return self.cognitive_router.compress()
        return {'compressed_memories': 'Cognitive router not available'}
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get comprehensive routing system statistics."""
        with self.lock:
            stats = {
                'routing_decisions': self.routing_decisions,
                'memory_hits': self.memory_hits,
                'memory_misses': self.memory_misses,
                'rebloom_requests': self.rebloom_requests,
                'vector_searches': self.vector_searches,
                'hit_rate': self.memory_hits / max(1, self.memory_hits + self.memory_misses),
                'working_memory_size': len(self.working_memory),
                'recent_memory_size': len(self.recent_memories),
                'significant_memory_size': len(self.significant_memories),
                'total_active_memories': len(self.working_memory) + len(self.recent_memories) + len(self.significant_memories)
            }
            
            # Add cognitive router stats
            if self.cognitive_router:
                cognitive_stats = self.cognitive_router.get_stats()
                stats['cognitive_router'] = cognitive_stats
            
            # Add vector index stats
            if self.vector_index:
                vector_stats = self.vector_index.get_stats()
                stats['vector_index'] = vector_stats
            
            return stats


class DAWNMemoryRoutingSystem:
    """
    Unified memory routing system for DAWN consciousness.
    Integrates chunk-based routing with JSON persistence and existing memory systems.
    """
    
    def __init__(self, 
                 memories_dir: str = "memories",
                 auto_save_interval: int = 300,  # 5 minutes
                 pulse_controller: Optional['PulseController'] = None):
        """
        Initialize the DAWN memory routing system.
        
        Args:
            memories_dir: Directory for memory storage
            auto_save_interval: Automatic save interval in seconds
            pulse_controller: Optional pulse controller for integration
        """
        self.memories_dir = Path(memories_dir)
        self.memories_dir.mkdir(exist_ok=True, parents=True)
        
        # Core components
        self.router = MemoryRouter(pulse_controller=pulse_controller)
        self.loader = DAWNMemoryLoader(memories_dir=str(self.memories_dir))
        
        # Integration with existing DAWN systems
        self.trace_log = None
        self.anchor_system = None
        self.pulse_controller = pulse_controller
        
        # Auto-save management
        self.auto_save_interval = auto_save_interval
        self.last_save_time = time.time()
        self.unsaved_memories: List[MemoryChunk] = []
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Initialize integrations
        self._initialize_integrations()
        
        logger.info(f"🧠 DAWN Memory Routing System initialized at {self.memories_dir}")
    
    def _initialize_integrations(self) -> None:
        """Initialize integrations with existing DAWN memory systems."""
        # Initialize trace log integration
        if TRACE_LOG_AVAILABLE:
            try:
                self.trace_log = EnhancedMemoryTraceLog()
                self.loader.trace_log = self.trace_log
                logger.info("✅ Integrated with DAWN trace log system")
            except Exception as e:
                logger.warning(f"Failed to initialize trace log integration: {e}")
        
        # Initialize memory anchor integration
        if MEMORY_ANCHOR_AVAILABLE:
            try:
                self.anchor_system = MemoryAnchorSystem()
                logger.info("✅ Integrated with DAWN memory anchor system")
            except Exception as e:
                logger.warning(f"Failed to initialize memory anchor integration: {e}")
    
    async def store_memory(self, 
                          speaker: str,
                          content: str,
                          topic: Optional[str] = None,
                          pulse_state: Optional[Dict[str, Any]] = None,
                          sigils: Optional[List[str]] = None,
                          auto_save: bool = True) -> MemoryChunk:
        """
        Store a new memory in the routing system.
        
        Args:
            speaker: Identity of the speaker
            content: Memory content
            topic: Optional topic/category
            pulse_state: Current pulse system state
            sigils: Active sigils during memory creation
            auto_save: Whether to trigger auto-save check
            
        Returns:
            MemoryChunk: Created memory chunk
        """
        with self.lock:
            # Get current pulse state if not provided
            if pulse_state is None and self.pulse_controller:
                pulse_state = self._get_current_pulse_state()
            
            # Create memory chunk
            chunk = create_memory_now(
                speaker=speaker,
                content=content,
                topic=topic,
                pulse_state=pulse_state or {},
                sigils=sigils or []
            )
            
            # Route the memory
            routing_result = self.router.route_memory(chunk)
            
            # Add to unsaved memories
            self.unsaved_memories.append(chunk)
            
            # Emit memory created event
            await self._emit_event('memory_created', {
                'chunk': chunk,
                'routing_result': routing_result
            })
            
            # Create memory anchor if significant
            if self.anchor_system and routing_result['significant_memory']:
                await self._create_memory_anchor(chunk)
            
            # Check for auto-save
            if auto_save:
                await self._check_auto_save()
            
            logger.info(f"Stored memory: {chunk.summary()}")
            return chunk
    
    async def retrieve_memories(self,
                               query: str,
                               context: Optional[Dict[str, Any]] = None,
                               max_results: int = 10,
                               include_archived: bool = False) -> List[MemoryChunk]:
        """
        Retrieve memories based on query and context.
        
        Args:
            query: Search query
            context: Optional context for filtering
            max_results: Maximum results to return
            include_archived: Whether to search archived memories
            
        Returns:
            List[MemoryChunk]: Retrieved memories
        """
        # Get memories from router
        router_results = self.router.retrieve_memories(query, context, max_results)
        
        # If we need more results or include_archived is True, search saved files
        if include_archived or len(router_results) < max_results:
            archived_results = await self._search_archived_memories(
                query, context, max_results - len(router_results)
            )
            router_results.extend(archived_results)
        
        # Emit retrieval event
        await self._emit_event('memories_retrieved', {
            'query': query,
            'context': context,
            'results_count': len(router_results)
        })
        
        return router_results[:max_results]
    
    async def save_memories(self, filepath: Optional[str] = None) -> str:
        """
        Save unsaved memories to storage.
        
        Args:
            filepath: Optional specific filepath to save to
            
        Returns:
            str: Path where memories were saved
        """
        with self.lock:
            if not self.unsaved_memories:
                logger.debug("No unsaved memories to save")
                return ""
            
            # Generate filepath if not provided
            if filepath is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = self.memories_dir / f"memories_{timestamp}.jsonl"
            else:
                filepath = Path(filepath)
            
            # Save memories
            self.loader.save_memory_to_json(self.unsaved_memories, str(filepath))
            saved_count = len(self.unsaved_memories)
            
            # Clear unsaved memories
            self.unsaved_memories.clear()
            self.last_save_time = time.time()
            
            # Emit save event
            await self._emit_event('memories_saved', {
                'filepath': str(filepath),
                'count': saved_count
            })
            
            logger.info(f"Saved {saved_count} memories to {filepath}")
            return str(filepath)
    
    async def load_memories_from_file(self, filepath: str) -> List[MemoryChunk]:
        """
        Load memories from a file and route them into the system.
        
        Args:
            filepath: Path to memory file
            
        Returns:
            List[MemoryChunk]: Loaded memories
        """
        chunks = self.loader.load_memory_from_json(filepath)
        
        # Route loaded memories
        for chunk in chunks:
            self.router.route_memory(chunk)
        
        logger.info(f"Loaded and routed {len(chunks)} memories from {filepath}")
        return chunks
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        router_stats = self.router.get_routing_stats()
        loader_stats = self.loader.get_stats()
        
        return {
            'router': router_stats,
            'loader': loader_stats,
            'unsaved_memories': len(self.unsaved_memories),
            'last_save_time': self.last_save_time,
            'time_since_save': time.time() - self.last_save_time,
            'integrations': {
                'trace_log': self.trace_log is not None,
                'anchor_system': self.anchor_system is not None,
                'pulse_controller': self.pulse_controller is not None
            }
        }
    
    def _get_current_pulse_state(self) -> Dict[str, Any]:
        """Get current pulse state from the pulse controller."""
        if not self.pulse_controller:
            return {}
        
        try:
            return {
                'heat': self.pulse_controller.current_heat,
                'zone': self.pulse_controller.current_zone,
                'entropy': getattr(self.pulse_controller, 'entropy', 0.5),
                'timestamp': time.time()
            }
        except Exception as e:
            logger.warning(f"Failed to get pulse state: {e}")
            return {}
    
    async def _search_archived_memories(self, query: str, context: Optional[Dict], max_results: int) -> List[MemoryChunk]:
        """Search through archived memory files."""
        archived_memories = []
        
        # Search through existing memory files
        for memory_file in self.memories_dir.glob("*.jsonl"):
            try:
                chunks = self.loader.load_memory_from_json(str(memory_file))
                
                # Filter chunks based on query
                filtered_chunks = self.loader.filter_memories(
                    chunks,
                    content_contains=query if len(query) > 3 else None
                )
                
                archived_memories.extend(filtered_chunks)
                
                if len(archived_memories) >= max_results:
                    break
                    
            except Exception as e:
                logger.warning(f"Error searching archived file {memory_file}: {e}")
        
        return archived_memories[:max_results]
    
    async def _create_memory_anchor(self, chunk: MemoryChunk) -> None:
        """Create a memory anchor for significant memories."""
        if not self.anchor_system:
            return
        
        try:
            # Determine anchor type based on memory characteristics
            anchor_type = AnchorType.SIGNIFICANT_INTERACTION
            
            if chunk.get_entropy() > 0.8:
                anchor_type = AnchorType.ENTROPY_SPIKE
            elif chunk.get_heat() > 50:
                anchor_type = AnchorType.EMOTIONAL_PEAK
            elif 'STABILIZE_PROTOCOL' in chunk.sigils:
                anchor_type = AnchorType.CRITICAL_SCUP_EVENT
            
            # Create anchor
            anchor_data = {
                'memory_chunk_id': chunk.memory_id,
                'content_preview': chunk.get_preview(100),
                'pulse_state': chunk.pulse_state,
                'sigils': chunk.sigils
            }
            
            self.anchor_system.create_anchor(
                anchor_type=anchor_type,
                trigger_event=f"Memory: {chunk.topic or 'general'}",
                system_state=chunk.pulse_state,
                metadata=anchor_data
            )
            
            chunk.anchor_linked = True
            logger.debug(f"Created memory anchor for {chunk.memory_id}")
            
        except Exception as e:
            logger.warning(f"Failed to create memory anchor for {chunk.memory_id}: {e}")
    
    async def _check_auto_save(self) -> None:
        """Check if auto-save should be triggered."""
        current_time = time.time()
        
        if (current_time - self.last_save_time) > self.auto_save_interval:
            if self.unsaved_memories:
                await self.save_memories()
    
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
                    logger.warning(f"Event handler error for {event_name}: {e}")
    
    def on(self, event_name: str, handler: Callable) -> None:
        """Register an event handler."""
        self.event_handlers[event_name].append(handler)
        logger.debug(f"Registered handler for event: {event_name}")


# Global instance for DAWN integration
_memory_routing_system: Optional[DAWNMemoryRoutingSystem] = None


def get_memory_routing_system() -> DAWNMemoryRoutingSystem:
    """Get the global memory routing system instance."""
    global _memory_routing_system
    if _memory_routing_system is None:
        _memory_routing_system = DAWNMemoryRoutingSystem()
    return _memory_routing_system


def initialize_memory_routing(memories_dir: str = "memories", 
                            pulse_controller: Optional['PulseController'] = None) -> DAWNMemoryRoutingSystem:
    """Initialize the global memory routing system."""
    global _memory_routing_system
    _memory_routing_system = DAWNMemoryRoutingSystem(
        memories_dir=memories_dir,
        pulse_controller=pulse_controller
    )
    return _memory_routing_system


# Convenience functions for direct integration
async def store_dawn_memory(speaker: str, content: str, **kwargs) -> MemoryChunk:
    """Store a memory in the DAWN system."""
    system = get_memory_routing_system()
    return await system.store_memory(speaker, content, **kwargs)


async def retrieve_dawn_memories(query: str, **kwargs) -> List[MemoryChunk]:
    """Retrieve memories from the DAWN system."""
    system = get_memory_routing_system()
    return await system.retrieve_memories(query, **kwargs) 