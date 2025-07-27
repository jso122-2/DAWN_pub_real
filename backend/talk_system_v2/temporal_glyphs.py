import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set
import time
from collections import defaultdict
import faiss
import pickle  # Using built-in pickle for Python 3.8+
import json

# Global tick counter for temporal operations
CURRENT_TICK = 0

def set_current_tick(tick: int):
    global CURRENT_TICK
    CURRENT_TICK = tick

@dataclass
class TemporalGlyph:
    """A memory with temporal properties and lifecycle"""
    id: str
    content: str
    embedding: np.ndarray
    birth_tick: int
    last_resonance_tick: int
    resonance_count: int
    decay_rate: float
    emotional_weight: Dict[str, float]  # mood -> weight
    semantic_neighbors: List[str]  # IDs of related glyphs
    transformation_history: List[Dict]
    
    @property
    def age(self) -> int:
        """Age in ticks since birth"""
        return CURRENT_TICK - self.birth_tick
    
    @property
    def vitality(self) -> float:
        """Current life force (0-1)"""
        if CURRENT_TICK == self.last_resonance_tick:
            return 1.0
            
        ticks_since_resonance = CURRENT_TICK - self.last_resonance_tick
        base_decay = np.exp(-self.decay_rate * ticks_since_resonance)
        resonance_boost = min(0.5, self.resonance_count * 0.05)
        
        vitality = base_decay + resonance_boost * (1 - base_decay)
        return max(0.0, min(1.0, vitality))
    
    def resonate(self, strength: float = 1.0):
        """Activate this glyph, refreshing its vitality"""
        self.last_resonance_tick = CURRENT_TICK
        self.resonance_count += 1
        
        # Slow decay for frequently used glyphs
        if self.resonance_count > 5:
            self.decay_rate *= 0.98
    
    def add_transformation(self, transform_type: str, params: Dict):
        """Record a transformation applied to this glyph"""
        self.transformation_history.append({
            'type': transform_type,
            'params': params,
            'tick': CURRENT_TICK,
            'vitality_at_time': self.vitality
        })

class CairrnCache:
    """Simple caching system for glyph persistence"""
    def __init__(self, cache_path: Optional[str] = None):
        self.cache_path = cache_path or "backend/embeddings/cairrn_cache.pkl"
        self.archived_glyphs: Dict[str, TemporalGlyph] = {}
        self.load_cache()
    
    def store(self, glyph_id: str, glyph: TemporalGlyph):
        """Store active glyph (called when glyph is created)"""
        pass  # Active glyphs stored in main memory
    
    def archive(self, glyph: TemporalGlyph):
        """Archive a dying glyph"""
        self.archived_glyphs[glyph.id] = glyph
        
        # Save periodically
        if len(self.archived_glyphs) % 10 == 0:
            self.save_cache()
    
    def save_cache(self):
        """Save archived glyphs to disk"""
        try:
            # Create directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            
            with open(self.cache_path, 'wb') as f:
                # Convert numpy arrays to lists for serialization
                serializable_glyphs = {}
                for glyph_id, glyph in self.archived_glyphs.items():
                    glyph_dict = {
                        'id': glyph.id,
                        'content': glyph.content,
                        'embedding': glyph.embedding.tolist(),
                        'birth_tick': glyph.birth_tick,
                        'last_resonance_tick': glyph.last_resonance_tick,
                        'resonance_count': glyph.resonance_count,
                        'decay_rate': glyph.decay_rate,
                        'emotional_weight': glyph.emotional_weight,
                        'semantic_neighbors': glyph.semantic_neighbors,
                        'transformation_history': glyph.transformation_history
                    }
                    serializable_glyphs[glyph_id] = glyph_dict
                    
                pickle.dump(serializable_glyphs, f)
        except Exception as e:
            print(f"Error saving cairrn cache: {e}")
    
    def load_cache(self):
        """Load archived glyphs from disk"""
        try:
            with open(self.cache_path, 'rb') as f:
                serializable_glyphs = pickle.load(f)
                
                for glyph_id, glyph_dict in serializable_glyphs.items():
                    glyph = TemporalGlyph(
                        id=glyph_dict['id'],
                        content=glyph_dict['content'],
                        embedding=np.array(glyph_dict['embedding']),
                        birth_tick=glyph_dict['birth_tick'],
                        last_resonance_tick=glyph_dict['last_resonance_tick'],
                        resonance_count=glyph_dict['resonance_count'],
                        decay_rate=glyph_dict['decay_rate'],
                        emotional_weight=glyph_dict['emotional_weight'],
                        semantic_neighbors=glyph_dict['semantic_neighbors'],
                        transformation_history=glyph_dict['transformation_history']
                    )
                    self.archived_glyphs[glyph_id] = glyph
                    
        except FileNotFoundError:
            pass  # Start with empty cache
        except Exception as e:
            print(f"Error loading cairrn cache: {e}")

class TemporalGlyphMemory:
    def __init__(self, cairrn_path: Optional[str] = None, embedding_dim: int = 384):
        self.glyphs: Dict[str, TemporalGlyph] = {}
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)  # Inner product for cosine similarity
        self.glyph_ids: List[str] = []  # Maps index positions to glyph IDs
        self.cairrn_cache = CairrnCache(cairrn_path) if cairrn_path else None
        
        # Glyph constellation tracking
        self.constellations: Dict[str, List[str]] = defaultdict(list)
        self.mood_attractors: Dict[str, np.ndarray] = {}
        
    def create_glyph(self, content: str, embedding: np.ndarray, 
                     mood_context: Dict, tick: int) -> TemporalGlyph:
        """Birth a new glyph into the memory landscape"""
        glyph_id = f"glyph_{tick}_{hash(content) % 10000}"
        
        # Calculate initial decay rate based on mood
        mood = mood_context.get('mood', 'NEUTRAL')
        decay_rates = {
            'DREAMING': 0.001,      # Dreams fade slowly
            'CONTEMPLATIVE': 0.005,  # Thoughts linger
            'FOCUSED': 0.01,         # Sharp but temporary
            'HYPERACTIVE': 0.02,     # Quick turnover
            'TRANSCENDENT': 0.0005   # Near eternal
        }
        
        glyph = TemporalGlyph(
            id=glyph_id,
            content=content,
            embedding=embedding,
            birth_tick=tick,
            last_resonance_tick=tick,
            resonance_count=0,
            decay_rate=decay_rates.get(mood, 0.01),
            emotional_weight=self._calculate_emotional_weight(mood_context),
            semantic_neighbors=[],
            transformation_history=[]
        )
        
        # Find semantic neighbors
        neighbors = self._find_neighbors(embedding, k=5)
        glyph.semantic_neighbors = [n[0] for n in neighbors if n[0] in self.glyphs]
        
        # Update constellations
        self._update_constellations(glyph, neighbors)
        
        # Store in memory
        self.glyphs[glyph_id] = glyph
        self._update_index(glyph)
        
        # Cache if using Cairrn
        if self.cairrn_cache:
            self.cairrn_cache.store(glyph_id, glyph)
        
        return glyph
    
    def search_living_memories(self, query_embedding: np.ndarray, 
                              mood_context: Dict, k: int = 10) -> List[Tuple[TemporalGlyph, float]]:
        """Search for glyphs, weighted by vitality and mood resonance"""
        if self.index.ntotal == 0:
            return []
            
        # Get candidates from embedding space
        norm_query = query_embedding / np.linalg.norm(query_embedding)
        distances, indices = self.index.search(norm_query.reshape(1, -1), min(k * 3, self.index.ntotal))
        
        # Score by vitality and mood alignment
        scored_glyphs = []
        current_mood = mood_context.get('mood', 'NEUTRAL')
        
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= len(self.glyph_ids):
                continue
                
            glyph_id = self.glyph_ids[idx]
            glyph = self.glyphs.get(glyph_id)
            
            if not glyph or glyph.vitality < 0.1:  # Skip dying glyphs
                continue
                
            # Calculate composite score
            base_similarity = float(dist)
            vitality_weight = glyph.vitality
            mood_weight = glyph.emotional_weight.get(current_mood, 0.5)
            constellation_bonus = self._get_constellation_bonus(glyph_id, query_embedding)
            
            final_score = (
                base_similarity * 0.4 +
                vitality_weight * 0.3 +
                mood_weight * 0.2 +
                constellation_bonus * 0.1
            )
            
            scored_glyphs.append((glyph, final_score))
        
        # Sort and return top k
        scored_glyphs.sort(key=lambda x: x[1], reverse=True)
        return scored_glyphs[:k]
    
    def prune_dead_glyphs(self, vitality_threshold: float = 0.05) -> int:
        """Remove glyphs that have faded beyond recovery"""
        dead_glyphs = [
            glyph_id for glyph_id, glyph in self.glyphs.items()
            if glyph.vitality < vitality_threshold
        ]
        
        for glyph_id in dead_glyphs:
            # Archive to Cairrn before deletion
            if self.cairrn_cache:
                self.cairrn_cache.archive(self.glyphs[glyph_id])
            
            # Remove from active memory
            del self.glyphs[glyph_id]
            
            # Remove from index (rebuild index)
            if glyph_id in self.glyph_ids:
                self._rebuild_index()
            
            # Update constellations
            for constellation in self.constellations.values():
                if glyph_id in constellation:
                    constellation.remove(glyph_id)
        
        return len(dead_glyphs)
    
    def _calculate_emotional_weight(self, mood_context: Dict) -> Dict[str, float]:
        """Calculate how well a glyph resonates with each mood"""
        scup = mood_context.get('scup', 50) / 100
        entropy = mood_context.get('entropy', 500000) / 1000000
        
        return {
            'DREAMING': entropy * 0.8 + (1 - scup) * 0.2,
            'CONTEMPLATIVE': (1 - abs(scup - 0.5)) * 0.6 + entropy * 0.4,
            'FOCUSED': scup * 0.7 + (1 - entropy) * 0.3,
            'HYPERACTIVE': entropy * 0.6 + scup * 0.4,
            'TRANSCENDENT': scup * 0.5 + entropy * 0.5
        }
    
    def _find_neighbors(self, embedding: np.ndarray, k: int = 5) -> List[Tuple[str, float]]:
        """Find k nearest neighbors to given embedding"""
        if self.index.ntotal == 0:
            return []
            
        norm_embedding = embedding / np.linalg.norm(embedding)
        distances, indices = self.index.search(norm_embedding.reshape(1, -1), min(k, self.index.ntotal))
        
        neighbors = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.glyph_ids):
                neighbors.append((self.glyph_ids[idx], float(dist)))
        
        return neighbors
    
    def _update_constellations(self, glyph: TemporalGlyph, neighbors: List[Tuple[str, float]]):
        """Update glyph constellations based on semantic neighbors"""
        # Create constellation for this glyph
        constellation_id = f"constellation_{glyph.id[:8]}"
        self.constellations[constellation_id] = [glyph.id] + [n[0] for n in neighbors[:3]]
        
        # Add to existing constellations if neighbors are there
        for neighbor_id, _ in neighbors:
            if neighbor_id in self.glyphs:
                for const_id, const_members in self.constellations.items():
                    if neighbor_id in const_members and glyph.id not in const_members:
                        const_members.append(glyph.id)
                        break
    
    def _get_constellation_bonus(self, glyph_id: str, query_embedding: np.ndarray) -> float:
        """Calculate bonus score based on constellation relationships"""
        bonus = 0.0
        
        # Find constellations containing this glyph
        for constellation in self.constellations.values():
            if glyph_id in constellation:
                # Check if other constellation members are similar to query
                for member_id in constellation:
                    if member_id != glyph_id and member_id in self.glyphs:
                        member_glyph = self.glyphs[member_id]
                        similarity = np.dot(
                            query_embedding / np.linalg.norm(query_embedding),
                            member_glyph.embedding / np.linalg.norm(member_glyph.embedding)
                        )
                        bonus += similarity * 0.1
        
        return min(bonus, 0.3)  # Cap constellation bonus
    
    def _update_index(self, glyph: TemporalGlyph):
        """Add glyph to FAISS index"""
        norm_embedding = glyph.embedding / np.linalg.norm(glyph.embedding)
        self.index.add(norm_embedding.reshape(1, -1))
        self.glyph_ids.append(glyph.id)
    
    def _rebuild_index(self):
        """Rebuild FAISS index after removing glyphs"""
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.glyph_ids = []
        
        for glyph in self.glyphs.values():
            self._update_index(glyph)
    
    def get_constellation_data(self) -> Dict:
        """Get constellation data for visualization"""
        constellation_data = {}
        
        for const_id, members in self.constellations.items():
            # Only include constellations with living members
            living_members = [m for m in members if m in self.glyphs and self.glyphs[m].vitality > 0.1]
            
            if len(living_members) >= 2:
                constellation_data[const_id] = {
                    'members': living_members,
                    'center': self._calculate_constellation_center(living_members),
                    'coherence': self._calculate_constellation_coherence(living_members)
                }
        
        return constellation_data
    
    def _calculate_constellation_center(self, member_ids: List[str]) -> np.ndarray:
        """Calculate the centroid of a constellation"""
        embeddings = []
        for member_id in member_ids:
            if member_id in self.glyphs:
                embeddings.append(self.glyphs[member_id].embedding)
        
        if embeddings:
            return np.mean(embeddings, axis=0)
        return np.zeros(self.embedding_dim)
    
    def _calculate_constellation_coherence(self, member_ids: List[str]) -> float:
        """Calculate how coherent a constellation is"""
        if len(member_ids) < 2:
            return 0.0
            
        embeddings = []
        for member_id in member_ids:
            if member_id in self.glyphs:
                embeddings.append(self.glyphs[member_id].embedding)
        
        if len(embeddings) < 2:
            return 0.0
            
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i+1, len(embeddings)):
                sim = np.dot(
                    embeddings[i] / np.linalg.norm(embeddings[i]),
                    embeddings[j] / np.linalg.norm(embeddings[j])
                )
                similarities.append(sim)
        
        return np.mean(similarities) if similarities else 0.0 