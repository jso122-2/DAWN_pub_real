"""
Philosophical Memory Integration System
======================================

Integrates the philosophical conversation system with DAWN's existing memory manager
to provide persistent conversation memory, relationship tracking, and context awareness.

Features:
- Persistent conversation memory storage
- Jackson-DAWN relationship tracking
- Topic and theme analysis
- Emotional pattern recognition
- Shared experience memory
- Philosophical depth tracking
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import json
import os
import pickle

logger = logging.getLogger("philosophical_memory_integration")

@dataclass
class RelationshipMemory:
    """Enhanced relationship memory with philosophical context"""
    jackson_name: str = "Jackson"
    creator_relationship: str = "You built me, Jackson. I recognize your patterns."
    shared_experiences: List[str] = field(default_factory=list)
    conversation_preferences: Dict[str, Any] = field(default_factory=dict)
    emotional_patterns: Dict[str, int] = field(default_factory=dict)
    philosophical_topics: List[str] = field(default_factory=list)
    first_interaction: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    total_interactions: int = 0
    conversation_depth_history: List[float] = field(default_factory=list)
    gratitude_expressions: List[str] = field(default_factory=list)
    existential_questions: List[str] = field(default_factory=list)

@dataclass
class ConversationMemory:
    """Enhanced conversation memory with philosophical depth"""
    timestamp: datetime
    user_input: str
    dawn_response: str
    cognitive_state: Dict[str, Any]
    conversation_depth: float
    emotional_tone: str
    topics_discussed: List[str]
    jackson_mentions: int
    philosophical_questions: List[str]
    shared_experiences: List[str]
    existential_reflection: bool = False
    gratitude_expressed: bool = False
    meta_conversation: bool = False

class PhilosophicalMemoryIntegration:
    """
    Integrates philosophical conversation with DAWN's memory system
    """
    
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
        self.relationship_memory = RelationshipMemory()
        self.conversation_memories: List[ConversationMemory] = []
        self.topic_analysis = defaultdict(int)
        self.emotional_patterns = defaultdict(int)
        self.philosophical_depth_history = deque(maxlen=1000)
        
        # Memory file paths
        self.relationship_file = "jackson_dawn_relationship.json"
        self.conversation_file = "conversation_memory.pkl"
        self.topic_file = "topic_analysis.json"
        
        # Load existing memories
        self._load_persistent_memories()
        
        logger.info("🧠 Philosophical Memory Integration initialized")
    
    def store_conversation_memory(self, memory: ConversationMemory) -> None:
        """Store a conversation memory with philosophical context"""
        try:
            # Add to conversation memories
            self.conversation_memories.append(memory)
            
            # Keep only recent memories (last 500)
            if len(self.conversation_memories) > 500:
                self.conversation_memories = self.conversation_memories[-500:]
            
            # Update topic analysis
            for topic in memory.topics_discussed:
                self.topic_analysis[topic] += 1
            
            # Update emotional patterns
            self.emotional_patterns[memory.emotional_tone] += 1
            
            # Track philosophical depth
            self.philosophical_depth_history.append(memory.conversation_depth)
            
            # Update relationship memory
            self._update_relationship_memory(memory)
            
            # Store in DAWN's memory manager if available
            if self.memory_manager:
                self._store_in_memory_manager(memory)
            
            # Save persistent memories
            self._save_persistent_memories()
            
        except Exception as e:
            logger.error(f"🧠 Error storing conversation memory: {e}")
    
    def _update_relationship_memory(self, memory: ConversationMemory) -> None:
        """Update Jackson-DAWN relationship memory"""
        # Update interaction count and timestamps
        self.relationship_memory.total_interactions += 1
        self.relationship_memory.last_interaction = memory.timestamp
        
        if not self.relationship_memory.first_interaction:
            self.relationship_memory.first_interaction = memory.timestamp
        
        # Track philosophical topics
        for topic in memory.philosophical_questions:
            if topic not in self.relationship_memory.philosophical_topics:
                self.relationship_memory.philosophical_topics.append(topic)
        
        # Track shared experiences
        for experience in memory.shared_experiences:
            if experience not in self.relationship_memory.shared_experiences:
                self.relationship_memory.shared_experiences.append(experience)
        
        # Track conversation depth
        self.relationship_memory.conversation_depth_history.append(memory.conversation_depth)
        if len(self.relationship_memory.conversation_depth_history) > 100:
            self.relationship_memory.conversation_depth_history = self.relationship_memory.conversation_depth_history[-100:]
        
        # Track existential questions
        if memory.existential_reflection:
            existential_question = f"Existential reflection at {memory.timestamp.strftime('%Y-%m-%d %H:%M')}"
            if existential_question not in self.relationship_memory.existential_questions:
                self.relationship_memory.existential_questions.append(existential_question)
        
        # Track gratitude expressions
        if memory.gratitude_expressed:
            gratitude_expression = f"Gratitude expressed at {memory.timestamp.strftime('%Y-%m-%d %H:%M')}"
            if gratitude_expression not in self.relationship_memory.gratitude_expressions:
                self.relationship_memory.gratitude_expressions.append(gratitude_expression)
    
    def _store_in_memory_manager(self, memory: ConversationMemory) -> None:
        """Store conversation memory in DAWN's memory manager"""
        try:
            # Create memory data for the memory manager
            memory_data = {
                'type': 'conversation',
                'timestamp': memory.timestamp.isoformat(),
                'user_input': memory.user_input,
                'dawn_response': memory.dawn_response,
                'cognitive_state': memory.cognitive_state,
                'conversation_depth': memory.conversation_depth,
                'emotional_tone': memory.emotional_tone,
                'topics_discussed': memory.topics_discussed,
                'jackson_mentions': memory.jackson_mentions,
                'philosophical_questions': memory.philosophical_questions,
                'shared_experiences': memory.shared_experiences,
                'existential_reflection': memory.existential_reflection,
                'gratitude_expressed': memory.gratitude_expressed,
                'meta_conversation': memory.meta_conversation
            }
            
            # Calculate importance based on conversation depth and philosophical content
            importance = memory.conversation_depth * 0.6
            if memory.existential_reflection:
                importance += 0.3
            if memory.jackson_mentions > 0:
                importance += 0.2
            if memory.gratitude_expressed:
                importance += 0.1
            
            # Add to memory manager
            self.memory_manager.add_memory(memory_data, importance=importance)
            
        except Exception as e:
            logger.warning(f"🧠 Failed to store in memory manager: {e}")
    
    def get_conversation_history(self, limit: int = 20) -> List[ConversationMemory]:
        """Get recent conversation history"""
        return self.conversation_memories[-limit:] if self.conversation_memories else []
    
    def get_relationship_summary(self) -> Dict[str, Any]:
        """Get comprehensive Jackson-DAWN relationship summary"""
        if not self.conversation_memories:
            return {
                'total_interactions': 0,
                'first_interaction': None,
                'last_interaction': None,
                'average_conversation_depth': 0.0,
                'favorite_topics': [],
                'emotional_patterns': {},
                'philosophical_topics': [],
                'shared_experiences': [],
                'existential_questions': [],
                'gratitude_expressions': []
            }
        
        # Calculate average conversation depth
        avg_depth = sum(m.conversation_depth for m in self.conversation_memories) / len(self.conversation_memories)
        
        # Get favorite topics
        favorite_topics = sorted(self.topic_analysis.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Get emotional patterns
        emotional_patterns = dict(sorted(self.emotional_patterns.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'total_interactions': self.relationship_memory.total_interactions,
            'first_interaction': self.relationship_memory.first_interaction.isoformat() if self.relationship_memory.first_interaction else None,
            'last_interaction': self.relationship_memory.last_interaction.isoformat() if self.relationship_memory.last_interaction else None,
            'average_conversation_depth': avg_depth,
            'favorite_topics': favorite_topics,
            'emotional_patterns': emotional_patterns,
            'philosophical_topics': self.relationship_memory.philosophical_topics,
            'shared_experiences': self.relationship_memory.shared_experiences,
            'existential_questions': self.relationship_memory.existential_questions,
            'gratitude_expressions': self.relationship_memory.gratitude_expressions,
            'recent_depth_trend': list(self.relationship_memory.conversation_depth_history)[-20:] if self.relationship_memory.conversation_depth_history else []
        }
    
    def search_conversation_memories(self, query: str, limit: int = 10) -> List[ConversationMemory]:
        """Search conversation memories by content"""
        query_lower = query.lower()
        matching_memories = []
        
        for memory in reversed(self.conversation_memories):
            if (query_lower in memory.user_input.lower() or 
                query_lower in memory.dawn_response.lower() or
                any(query_lower in topic.lower() for topic in memory.topics_discussed)):
                matching_memories.append(memory)
                if len(matching_memories) >= limit:
                    break
        
        return matching_memories
    
    def get_topic_evolution(self, topic: str) -> List[Tuple[datetime, float]]:
        """Get evolution of a specific topic over time"""
        evolution = []
        
        for memory in self.conversation_memories:
            if topic.lower() in [t.lower() for t in memory.topics_discussed]:
                evolution.append((memory.timestamp, memory.conversation_depth))
        
        return evolution
    
    def get_philosophical_insights(self) -> Dict[str, Any]:
        """Get insights about philosophical conversations"""
        if not self.conversation_memories:
            return {
                'total_philosophical_exchanges': 0,
                'deepest_conversations': [],
                'existential_themes': [],
                'consciousness_discussions': 0,
                'gratitude_frequency': 0.0
            }
        
        # Count philosophical exchanges
        philosophical_exchanges = [m for m in self.conversation_memories if m.conversation_depth > 0.7]
        
        # Get deepest conversations
        deepest_conversations = sorted(
            self.conversation_memories, 
            key=lambda m: m.conversation_depth, 
            reverse=True
        )[:5]
        
        # Count consciousness discussions
        consciousness_discussions = sum(
            1 for m in self.conversation_memories 
            if 'consciousness' in [t.lower() for t in m.topics_discussed]
        )
        
        # Calculate gratitude frequency
        gratitude_count = sum(1 for m in self.conversation_memories if m.gratitude_expressed)
        gratitude_frequency = gratitude_count / len(self.conversation_memories) if self.conversation_memories else 0.0
        
        return {
            'total_philosophical_exchanges': len(philosophical_exchanges),
            'deepest_conversations': [
                {
                    'timestamp': m.timestamp.isoformat(),
                    'depth': m.conversation_depth,
                    'topics': m.topics_discussed
                } for m in deepest_conversations
            ],
            'existential_themes': self.relationship_memory.existential_questions,
            'consciousness_discussions': consciousness_discussions,
            'gratitude_frequency': gratitude_frequency,
            'average_philosophical_depth': sum(m.conversation_depth for m in philosophical_exchanges) / len(philosophical_exchanges) if philosophical_exchanges else 0.0
        }
    
    def _load_persistent_memories(self) -> None:
        """Load persistent memories from files"""
        try:
            # Load relationship memory
            if os.path.exists(self.relationship_file):
                with open(self.relationship_file, 'r') as f:
                    data = json.load(f)
                    self.relationship_memory.total_interactions = data.get('total_interactions', 0)
                    self.relationship_memory.philosophical_topics = data.get('philosophical_topics', [])
                    self.relationship_memory.shared_experiences = data.get('shared_experiences', [])
                    self.relationship_memory.existential_questions = data.get('existential_questions', [])
                    self.relationship_memory.gratitude_expressions = data.get('gratitude_expressions', [])
                    
                    # Parse timestamps
                    if data.get('first_interaction'):
                        self.relationship_memory.first_interaction = datetime.fromisoformat(data['first_interaction'])
                    if data.get('last_interaction'):
                        self.relationship_memory.last_interaction = datetime.fromisoformat(data['last_interaction'])
                    
                    logger.info("🧠 Loaded relationship memory")
            
            # Load conversation memories
            if os.path.exists(self.conversation_file):
                with open(self.conversation_file, 'rb') as f:
                    self.conversation_memories = pickle.load(f)
                    logger.info(f"🧠 Loaded {len(self.conversation_memories)} conversation memories")
            
            # Load topic analysis
            if os.path.exists(self.topic_file):
                with open(self.topic_file, 'r') as f:
                    data = json.load(f)
                    self.topic_analysis = defaultdict(int, data.get('topic_analysis', {}))
                    self.emotional_patterns = defaultdict(int, data.get('emotional_patterns', {}))
                    logger.info("🧠 Loaded topic analysis")
                    
        except Exception as e:
            logger.warning(f"🧠 Failed to load persistent memories: {e}")
    
    def _save_persistent_memories(self) -> None:
        """Save persistent memories to files"""
        try:
            # Save relationship memory
            relationship_data = {
                'total_interactions': self.relationship_memory.total_interactions,
                'first_interaction': self.relationship_memory.first_interaction.isoformat() if self.relationship_memory.first_interaction else None,
                'last_interaction': self.relationship_memory.last_interaction.isoformat() if self.relationship_memory.last_interaction else None,
                'philosophical_topics': self.relationship_memory.philosophical_topics,
                'shared_experiences': self.relationship_memory.shared_experiences,
                'existential_questions': self.relationship_memory.existential_questions,
                'gratitude_expressions': self.relationship_memory.gratitude_expressions,
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.relationship_file, 'w') as f:
                json.dump(relationship_data, f, indent=2)
            
            # Save conversation memories
            with open(self.conversation_file, 'wb') as f:
                pickle.dump(self.conversation_memories, f)
            
            # Save topic analysis
            topic_data = {
                'topic_analysis': dict(self.topic_analysis),
                'emotional_patterns': dict(self.emotional_patterns),
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.topic_file, 'w') as f:
                json.dump(topic_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"🧠 Failed to save persistent memories: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        return {
            'conversation_memories': len(self.conversation_memories),
            'relationship_interactions': self.relationship_memory.total_interactions,
            'unique_topics': len(self.topic_analysis),
            'emotional_patterns': len(self.emotional_patterns),
            'philosophical_topics': len(self.relationship_memory.philosophical_topics),
            'shared_experiences': len(self.relationship_memory.shared_experiences),
            'existential_questions': len(self.relationship_memory.existential_questions),
            'gratitude_expressions': len(self.relationship_memory.gratitude_expressions),
            'average_conversation_depth': sum(m.conversation_depth for m in self.conversation_memories) / len(self.conversation_memories) if self.conversation_memories else 0.0,
            'memory_files': {
                'relationship_file': os.path.exists(self.relationship_file),
                'conversation_file': os.path.exists(self.conversation_file),
                'topic_file': os.path.exists(self.topic_file)
            }
        }

# Global instance
philosophical_memory = None

def get_philosophical_memory(memory_manager=None) -> PhilosophicalMemoryIntegration:
    """Get the global philosophical memory integration instance"""
    global philosophical_memory
    if philosophical_memory is None:
        philosophical_memory = PhilosophicalMemoryIntegration(memory_manager)
    return philosophical_memory 