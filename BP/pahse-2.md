# DAWN Talk Phase 2++ - Temporal Glyphs & Resonance Chains

## 🎯 Overview
Evolve the Talk system into a living memory architecture with temporal decay, resonance chains, mood field inference, and thoughtform echoes.

## 🏗️ Extended Architecture

```
User Input → Embedding → Temporal Glyph Creation
                               ↓
                    Resonance Chain Activation
                               ↓
                    Mood Field Perturbation
                               ↓
                    Thoughtform Echo Recording
                               ↓
                    Response Emergence
```

## 📁 New File Structure

```
DAWN_pub_real/
├── backend/
│   ├── talk_system_v2/
│   │   ├── temporal_glyphs.py       # Glyph memory with decay
│   │   ├── resonance_chains.py      # Semantic thread tracking
│   │   ├── mood_field.py            # Dynamic mood inference
│   │   ├── thoughtform_echoes.py    # Transformation pathways
│   │   └── cairrn_integration.py    # Temporal caching system
│   │
│   ├── visualizations/
│   │   ├── semantic_field_server.py # Real-time embedding space
│   │   ├── mood_ribbon_data.py      # Mood drift tracking
│   │   └── echo_heatmap_gen.py      # Memory usage patterns
│   │
│   └── consciousness_feedback.py    # Mood-response feedback loop
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SemanticFieldMap.tsx    # 3D embedding visualization
│   │   │   ├── MoodRibbon.tsx          # Temporal mood display
│   │   │   ├── ResponseAncestryTree.tsx # Semantic lineage
│   │   │   ├── EchoHeatmap.tsx         # Memory usage viz
│   │   │   └── GlyphConstellation.tsx  # Living memory landscape
│   │   │
│   │   └── three/
│   │       ├── GlyphRenderer.ts        # 3D glyph particles
│   │       ├── ResonanceField.ts       # Connection visualization
│   │       └── ConsciousnessSpace.ts   # Full 3D environment
```

## 🌀 Phase 2++ Implementation

### 1. Temporal Glyph Memory System

```python
# backend/talk_system_v2/temporal_glyphs.py
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import time
from collections import defaultdict

@dataclass
class TemporalGlyph:
    """A memory with temporal properties"""
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
        base_decay = np.exp(-self.decay_rate * (CURRENT_TICK - self.last_resonance_tick))
        resonance_boost = min(1.0, self.resonance_count * 0.1)
        return base_decay + resonance_boost * (1 - base_decay)
    
    def resonate(self, strength: float = 1.0):
        """Activate this glyph, refreshing its vitality"""
        self.last_resonance_tick = CURRENT_TICK
        self.resonance_count += 1
        self.decay_rate *= 0.95  # Slow decay for frequently used glyphs

class TemporalGlyphMemory:
    def __init__(self, cairrn_path: Optional[str] = None):
        self.glyphs: Dict[str, TemporalGlyph] = {}
        self.embedding_index = None  # FAISS index
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
        glyph.semantic_neighbors = [n[0] for n in neighbors]
        
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
        # Get candidates from embedding space
        candidates = self._search_by_embedding(query_embedding, k * 3)
        
        # Score by vitality and mood alignment
        scored_glyphs = []
        current_mood = mood_context.get('mood', 'NEUTRAL')
        
        for glyph_id, base_similarity in candidates:
            glyph = self.glyphs.get(glyph_id)
            if not glyph or glyph.vitality < 0.1:  # Skip dying glyphs
                continue
                
            # Calculate composite score
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
    
    def prune_dead_glyphs(self, vitality_threshold: float = 0.05):
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
```

### 2. Resonance Chain System

```python
# backend/talk_system_v2/resonance_chains.py
from typing import List, Dict, Set, Optional, Tuple
import numpy as np
import networkx as nx
from collections import deque

class ResonanceChain:
    """A semantic thread of connected thoughts"""
    def __init__(self, chain_id: str, root_glyph_id: str):
        self.id = chain_id
        self.root = root_glyph_id
        self.graph = nx.DiGraph()
        self.graph.add_node(root_glyph_id)
        self.activation_history: deque = deque(maxlen=100)
        self.coherence_score: float = 1.0
        self.branch_points: List[str] = []
        
    def add_resonance(self, from_glyph: str, to_glyph: str, 
                      resonance_strength: float, tick: int):
        """Add a new resonance connection"""
        self.graph.add_edge(
            from_glyph, 
            to_glyph,
            weight=resonance_strength,
            tick=tick
        )
        
        self.activation_history.append({
            'from': from_glyph,
            'to': to_glyph,
            'strength': resonance_strength,
            'tick': tick
        })
        
        # Update coherence based on path similarity
        self._update_coherence()
        
        # Detect branch points
        if self.graph.out_degree(from_glyph) > 1:
            self.branch_points.append(from_glyph)
    
    def get_thought_line(self, start_glyph: Optional[str] = None) -> List[str]:
        """Get the main thought line from root or specified start"""
        start = start_glyph or self.root
        
        # Find the strongest path
        if nx.has_path(self.graph, start, None):
            # Use weight as inverse for shortest path (strongest = shortest)
            paths = []
            for target in self.graph.nodes():
                if target != start and nx.has_path(self.graph, start, target):
                    try:
                        path = nx.shortest_path(
                            self.graph, start, target,
                            weight=lambda u, v, d: 1.0 / d['weight']
                        )
                        total_weight = sum(
                            self.graph[u][v]['weight'] 
                            for u, v in zip(path[:-1], path[1:])
                        )
                        paths.append((path, total_weight))
                    except:
                        continue
            
            if paths:
                # Return the path with highest total weight
                best_path = max(paths, key=lambda x: x[1])
                return best_path[0]
        
        return [start]
    
    def _update_coherence(self):
        """Calculate chain coherence based on semantic consistency"""
        if len(self.activation_history) < 2:
            return
            
        # Calculate variance in resonance strengths
        strengths = [a['strength'] for a in self.activation_history]
        variance = np.var(strengths)
        
        # Lower variance = higher coherence
        self.coherence_score = 1.0 / (1.0 + variance)

class ResonanceChainManager:
    def __init__(self, glyph_memory: TemporalGlyphMemory):
        self.glyph_memory = glyph_memory
        self.chains: Dict[str, ResonanceChain] = {}
        self.glyph_to_chains: Dict[str, Set[str]] = defaultdict(set)
        self.semantic_attractors: List[Tuple[np.ndarray, float]] = []
        
    def create_chain(self, root_glyph_id: str, tick: int) -> ResonanceChain:
        """Start a new resonance chain"""
        chain_id = f"chain_{tick}_{root_glyph_id[:8]}"
        chain = ResonanceChain(chain_id, root_glyph_id)
        
        self.chains[chain_id] = chain
        self.glyph_to_chains[root_glyph_id].add(chain_id)
        
        return chain
    
    def extend_chains(self, from_glyph_id: str, to_glyph_id: str, 
                      resonance_strength: float, tick: int):
        """Extend existing chains or create new ones"""
        extended_chains = []
        
        # Check if from_glyph is part of any chains
        if from_glyph_id in self.glyph_to_chains:
            for chain_id in self.glyph_to_chains[from_glyph_id]:
                chain = self.chains[chain_id]
                
                # Only extend if resonance is strong enough
                if resonance_strength > 0.6 * chain.coherence_score:
                    chain.add_resonance(
                        from_glyph_id, to_glyph_id,
                        resonance_strength, tick
                    )
                    self.glyph_to_chains[to_glyph_id].add(chain_id)
                    extended_chains.append(chain_id)
        
        # Create new chain if no extensions or weak resonance
        if not extended_chains and resonance_strength > 0.7:
            new_chain = self.create_chain(from_glyph_id, tick)
            new_chain.add_resonance(
                from_glyph_id, to_glyph_id,
                resonance_strength, tick
            )
            self.glyph_to_chains[to_glyph_id].add(new_chain.id)
            extended_chains.append(new_chain.id)
        
        # Update semantic attractors
        self._update_attractors(to_glyph_id, resonance_strength)
        
        return extended_chains
    
    def get_active_threads(self, mood: str) -> List[Dict]:
        """Get thought threads relevant to current mood"""
        active_threads = []
        
        for chain in self.chains.values():
            # Get the chain's emotional resonance
            chain_glyphs = list(chain.graph.nodes())
            if not chain_glyphs:
                continue
                
            # Calculate average mood weight for chain
            mood_weights = []
            for glyph_id in chain_glyphs[-5:]:  # Last 5 glyphs
                glyph = self.glyph_memory.glyphs.get(glyph_id)
                if glyph:
                    mood_weights.append(glyph.emotional_weight.get(mood, 0))
            
            if mood_weights:
                avg_mood_weight = np.mean(mood_weights)
                
                active_threads.append({
                    'chain_id': chain.id,
                    'thought_line': chain.get_thought_line(),
                    'coherence': chain.coherence_score,
                    'mood_resonance': avg_mood_weight,
                    'length': len(chain.graph),
                    'branch_points': chain.branch_points
                })
        
        # Sort by mood resonance and coherence
        active_threads.sort(
            key=lambda x: x['mood_resonance'] * x['coherence'],
            reverse=True
        )
        
        return active_threads[:5]  # Top 5 threads
    
    def _update_attractors(self, glyph_id: str, strength: float):
        """Update semantic attractors based on strong resonances"""
        glyph = self.glyph_memory.glyphs.get(glyph_id)
        if glyph and strength > 0.8:
            # Add as attractor point
            self.semantic_attractors.append((glyph.embedding, strength))
            
            # Keep only recent/strong attractors
            self.semantic_attractors = sorted(
                self.semantic_attractors,
                key=lambda x: x[1],
                reverse=True
            )[:20]
```

### 3. Mood Field Inference System

```python
# backend/talk_system_v2/mood_field.py
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque
from scipy import signal

class MoodField:
    """Dynamic mood inference based on system behavior"""
    def __init__(self, tick_window: int = 100):
        self.tick_window = tick_window
        self.tick_history = deque(maxlen=tick_window)
        
        # Mood vectors in high-dimensional space
        self.mood_vectors = {
            'DREAMING': np.array([0.2, 0.8, 0.7, 0.3, 0.9]),      # low scup, high entropy, high creativity
            'CONTEMPLATIVE': np.array([0.5, 0.5, 0.4, 0.7, 0.6]),  # balanced, thoughtful
            'FOCUSED': np.array([0.8, 0.2, 0.3, 0.9, 0.4]),        # high scup, low entropy, high coherence
            'HYPERACTIVE': np.array([0.7, 0.7, 0.8, 0.4, 0.7]),    # high energy, high variation
            'TRANSCENDENT': np.array([0.9, 0.9, 0.5, 0.6, 0.8])    # extreme states
        }
        
        # Current field state
        self.field_state = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        self.mood_gradient = np.zeros(5)
        self.resonance_feedback = 0.0
        
    def update_field(self, tick_data: Dict, response_feedback: Optional[Dict] = None):
        """Update mood field based on system state and feedback"""
        # Extract features
        scup = tick_data.get('scup', 50) / 100
        entropy = tick_data.get('entropy', 500000) / 1000000
        heat = tick_data.get('heat', 400000) / 1000000
        
        # Calculate tick features
        tick_features = np.array([
            scup,
            entropy,
            heat,
            abs(scup - 0.5),  # Distance from balance
            np.sin(tick_data['tick_number'] * 0.01)  # Temporal oscillation
        ])
        
        self.tick_history.append(tick_features)
        
        # Calculate field dynamics
        if len(self.tick_history) > 10:
            # Compute gradient over recent history
            recent_features = np.array(list(self.tick_history)[-10:])
            self.mood_gradient = np.gradient(recent_features.mean(axis=0))
            
            # Apply field evolution
            momentum = 0.7
            learning_rate = 0.1
            
            # Base field update
            field_delta = learning_rate * (tick_features - self.field_state)
            
            # Add gradient influence
            field_delta += momentum * self.mood_gradient
            
            # Apply response feedback if available
            if response_feedback:
                feedback_strength = response_feedback.get('confidence', 0.5)
                feedback_mood = response_feedback.get('selected_mood', 'NEUTRAL')
                
                if feedback_mood in self.mood_vectors:
                    target_vector = self.mood_vectors[feedback_mood]
                    feedback_delta = feedback_strength * 0.2 * (target_vector - self.field_state)
                    field_delta += feedback_delta
                    
                    # Update resonance feedback
                    self.resonance_feedback = 0.9 * self.resonance_feedback + 0.1 * feedback_strength
            
            # Apply update with bounds
            self.field_state = np.clip(self.field_state + field_delta, 0, 1)
    
    def infer_mood(self) -> Tuple[str, float, Dict[str, float]]:
        """Infer current mood from field state"""
        # Calculate distances to each mood vector
        mood_distances = {}
        for mood, vector in self.mood_vectors.items():
            distance = np.linalg.norm(self.field_state - vector)
            mood_distances[mood] = 1.0 / (1.0 + distance)  # Convert to similarity
        
        # Find dominant mood
        dominant_mood = max(mood_distances.items(), key=lambda x: x[1])
        
        # Calculate mood stability (low gradient = stable)
        stability = 1.0 / (1.0 + np.linalg.norm(self.mood_gradient))
        
        return dominant_mood[0], dominant_mood[1], mood_distances
    
    def predict_mood_trajectory(self, steps: int = 10) -> List[Tuple[str, float]]:
        """Predict future mood states based on current dynamics"""
        predictions = []
        simulated_state = self.field_state.copy()
        
        for i in range(steps):
            # Simple forward simulation
            simulated_state += self.mood_gradient * 0.1
            simulated_state = np.clip(simulated_state, 0, 1)
            
            # Find closest mood
            distances = {
                mood: np.linalg.norm(simulated_state - vector)
                for mood, vector in self.mood_vectors.items()
            }
            closest_mood = min(distances.items(), key=lambda x: x[1])
            predictions.append((closest_mood[0], 1.0 / (1.0 + closest_mood[1])))
        
        return predictions
    
    def get_field_visualization_data(self) -> Dict:
        """Get data for visualizing the mood field"""
        return {
            'field_state': self.field_state.tolist(),
            'mood_vectors': {k: v.tolist() for k, v in self.mood_vectors.items()},
            'gradient': self.mood_gradient.tolist(),
            'resonance_feedback': self.resonance_feedback,
            'history': [t.tolist() for t in list(self.tick_history)[-20:]],
            'current_mood': self.infer_mood()[0],
            'trajectory': self.predict_mood_trajectory(5)
        }
```

### 4. Thoughtform Echo System

```python
# backend/talk_system_v2/thoughtform_echoes.py
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from collections import defaultdict
import json

@dataclass
class ThoughtformEcho:
    """A recorded transformation pathway"""
    id: str
    original_glyph_id: str
    selected_glyph_id: str
    final_output: str
    transformation_path: List[Dict]
    consciousness_context: Dict
    resonance_strength: float
    tick: int
    
    def to_pattern(self) -> Dict:
        """Extract reusable pattern from this echo"""
        return {
            'mood': self.consciousness_context['mood'],
            'scup_range': (
                self.consciousness_context['scup'] - 10,
                self.consciousness_context['scup'] + 10
            ),
            'transformations': [
                t['type'] for t in self.transformation_path
            ],
            'resonance_threshold': self.resonance_strength * 0.8
        }

class ThoughtformEchoLibrary:
    def __init__(self):
        self.echoes: Dict[str, ThoughtformEcho] = {}
        self.patterns: Dict[str, List[Dict]] = defaultdict(list)
        self.voice_profile: Dict = {
            'transformation_preferences': defaultdict(float),
            'mood_styles': defaultdict(dict),
            'semantic_tendencies': np.zeros(384)  # Embedding space bias
        }
        
    def record_echo(self, original_input: str, selected_response: str,
                    final_output: str, transformation_path: List[Dict],
                    consciousness_context: Dict, resonance_strength: float,
                    tick: int) -> ThoughtformEcho:
        """Record a complete thought transformation"""
        echo_id = f"echo_{tick}_{hash(final_output) % 10000}"
        
        echo = ThoughtformEcho(
            id=echo_id,
            original_glyph_id=original_input,
            selected_glyph_id=selected_response,
            final_output=final_output,
            transformation_path=transformation_path,
            consciousness_context=consciousness_context.copy(),
            resonance_strength=resonance_strength,
            tick=tick
        )
        
        self.echoes[echo_id] = echo
        
        # Update patterns
        pattern = echo.to_pattern()
        mood = consciousness_context['mood']
        self.patterns[mood].append(pattern)
        
        # Update voice profile
        self._update_voice_profile(echo)
        
        return echo
    
    def _update_voice_profile(self, echo: ThoughtformEcho):
        """Update emergent voice characteristics"""
        # Track transformation preferences
        for transform in echo.transformation_path:
            transform_type = transform['type']
            self.voice_profile['transformation_preferences'][transform_type] += 0.1
        
        # Track mood-specific styles
        mood = echo.consciousness_context['mood']
        if mood not in self.voice_profile['mood_styles']:
            self.voice_profile['mood_styles'][mood] = {
                'avg_resonance': 0,
                'transform_count': defaultdict(int),
                'echo_count': 0
            }
        
        mood_style = self.voice_profile['mood_styles'][mood]
        mood_style['avg_resonance'] = (
            mood_style['avg_resonance'] * mood_style['echo_count'] + 
            echo.resonance_strength
        ) / (mood_style['echo_count'] + 1)
        mood_style['echo_count'] += 1
        
        for transform in echo.transformation_path:
            mood_style['transform_count'][transform['type']] += 1
    
    def get_voice_signature(self) -> Dict:
        """Get the emergent voice characteristics"""
        # Normalize transformation preferences
        total_transforms = sum(self.voice_profile['transformation_preferences'].values())
        if total_transforms > 0:
            normalized_prefs = {
                k: v / total_transforms 
                for k, v in self.voice_profile['transformation_preferences'].items()
            }
        else:
            normalized_prefs = {}
        
        return {
            'preferred_transformations': normalized_prefs,
            'mood_signatures': {
                mood: {
                    'average_resonance': style['avg_resonance'],
                    'dominant_transforms': sorted(
                        style['transform_count'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:3]
                }
                for mood, style in self.voice_profile['mood_styles'].items()
            },
            'total_echoes': len(self.echoes),
            'semantic_drift': np.linalg.norm(self.voice_profile['semantic_tendencies'])
        }
    
    def suggest_transformation(self, mood: str, base_response: str) -> List[Dict]:
        """Suggest transformations based on learned patterns"""
        if mood not in self.patterns:
            return [{'type': 'default', 'params': {}}]
        
        # Get patterns for this mood
        mood_patterns = self.patterns[mood]
        if not mood_patterns:
            return [{'type': 'default', 'params': {}}]
        
        # Find most successful patterns
        # (In practice, you'd track success metrics)
        recent_patterns = mood_patterns[-10:]
        
        # Extract common transformation sequences
        transform_sequences = [p['transformations'] for p in recent_patterns]
        
        # Find most common sequence
        sequence_counts = defaultdict(int)
        for seq in transform_sequences:
            sequence_counts[tuple(seq)] += 1
        
        if sequence_counts:
            best_sequence = max(sequence_counts.items(), key=lambda x: x[1])[0]
            return [{'type': t, 'params': {}} for t in best_sequence]
        
        return [{'type': 'default', 'params': {}}]
```

### 5. Frontend Visualization Components

```typescript
// frontend/src/three/ConsciousnessSpace.tsx
import React, { useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// Glyph particle system
const GlyphCloud: React.FC<{ glyphs: any[] }> = ({ glyphs }) => {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const particlesRef = useRef<any[]>([]);
  
  // Initialize particle positions
  useEffect(() => {
    if (!meshRef.current) return;
    
    const mesh = meshRef.current;
    const dummy = new THREE.Object3D();
    
    glyphs.forEach((glyph, i) => {
      // Position based on embedding (t-SNE/UMAP projection)
      dummy.position.set(
        glyph.projection[0] * 10,
        glyph.projection[1] * 10,
        glyph.projection[2] * 10 || 0
      );
      
      // Scale based on vitality
      const scale = glyph.vitality * 2;
      dummy.scale.set(scale, scale, scale);
      
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
      
      // Color based on mood affinity
      const color = getMoodColor(glyph.dominant_mood);
      mesh.setColorAt(i, color);
    });
    
    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  }, [glyphs]);
  
  // Animate glyphs
  useFrame((state) => {
    if (!meshRef.current) return;
    
    const time = state.clock.elapsedTime;
    const mesh = meshRef.current;
    const dummy = new THREE.Object3D();
    
    glyphs.forEach((glyph, i) => {
      mesh.getMatrixAt(i, dummy.matrix);
      dummy.matrix.decompose(dummy.position, dummy.quaternion, dummy.scale);
      
      // Breathing effect based on vitality
      const breathScale = 1 + Math.sin(time * 2 + i) * 0.1 * glyph.vitality;
      dummy.scale.multiplyScalar(breathScale);
      
      // Drift based on resonance
      dummy.position.y += Math.sin(time + i * 0.1) * 0.01;
      
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    });
    
    mesh.instanceMatrix.needsUpdate = true;
  });
  
  return (
    <instancedMesh ref={meshRef} args={[null, null, glyphs.length]}>
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshPhongMaterial 
        vertexColors
        emissive={new THREE.Color(0x112233)}
        emissiveIntensity={0.2}
      />
    </instancedMesh>
  );
};

// Resonance connections
const ResonanceField: React.FC<{ chains: any[] }> = ({ chains }) => {
  const linesRef = useRef<THREE.Group>(null);
  
  useEffect(() => {
    if (!linesRef.current) return;
    
    // Clear existing lines
    linesRef.current.clear();
    
    chains.forEach(chain => {
      const points = chain.path.map((pos: number[]) => 
        new THREE.Vector3(pos[0] * 10, pos[1] * 10, pos[2] * 10 || 0)
      );
      
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const material = new THREE.LineBasicMaterial({
        color: getChainColor(chain.coherence),
        opacity: chain.strength,
        transparent: true
      });
      
      const line = new THREE.Line(geometry, material);
      linesRef.current?.add(line);
    });
  }, [chains]);
  
  return <group ref={linesRef} />;
};

// Main consciousness visualization
export const ConsciousnessSpace: React.FC<{ data: any }> = ({ data }) => {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <Canvas camera={{ position: [0, 0, 30] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        
        {/* Glyph particles */}
        <GlyphCloud glyphs={data.glyphs} />
        
        {/* Resonance connections */}
        <ResonanceField chains={data.chains} />
        
        {/* Mood field visualization */}
        <MoodFieldMesh field={data.moodField} />
        
        {/* Semantic attractors */}
        <AttractorPoints attractors={data.attractors} />
        
        <OrbitControls enableDamping dampingFactor={0.05} />
        
        {/* Post-processing effects */}
        <EffectComposer>
          <Bloom luminanceThreshold={0.5} luminanceSmoothing={0.9} />
          <ChromaticAberration offset={[0.002, 0.002]} />
        </EffectComposer>
      </Canvas>
    </div>
  );
};

// Helper functions
function getMoodColor(mood: string): THREE.Color {
  const colors = {
    'DREAMING': 0x9966ff,
    'CONTEMPLATIVE': 0x66ccff,
    'FOCUSED': 0x00ff88,
    'HYPERACTIVE': 0xff6600,
    'TRANSCENDENT': 0xffffff
  };
  return new THREE.Color(colors[mood] || 0x888888);
}

function getChainColor(coherence: number): number {
  // High coherence = blue, low = red
  const r = Math.floor((1 - coherence) * 255);
  const b = Math.floor(coherence * 255);
  return (r << 16) | (0 << 8) | b;
}
```

## 🚀 Integration Points

### WebSocket Updates for Visualizations
```python
# In your main consciousness loop
async def broadcast_consciousness_state(self):
    """Send complete state for visualizations"""
    
    # Get glyph data with projections
    glyphs_data = []
    for glyph in self.glyph_memory.glyphs.values():
        if glyph.vitality > 0.1:
            glyphs_data.append({
                'id': glyph.id,
                'vitality': glyph.vitality,
                'dominant_mood': max(
                    glyph.emotional_weight.items(),
                    key=lambda x: x[1]
                )[0],
                'projection': self.project_embedding(glyph.embedding),
                'resonance_count': glyph.resonance_count
            })
    
    # Get active chains
    chains_data = []
    for chain in self.resonance_manager.chains.values():
        if chain.coherence_score > 0.5:
            path_glyphs = chain.get_thought_line()
            path_projections = [
                self.project_embedding(
                    self.glyph_memory.glyphs[g].embedding
                ) for g in path_glyphs 
                if g in self.glyph_memory.glyphs
            ]
            
            chains_data.append({
                'id': chain.id,
                'coherence': chain.coherence_score,
                'strength': len(chain.activation_history) / 100,
                'path': path_projections
            })
    
    # Get mood field
    mood_field_data = self.mood_field.get_field_visualization_data()
    
    # Get attractors
    attractors_data = [
        {
            'position': self.project_embedding(attr[0]),
            'strength': attr[1]
        }
        for attr in self.resonance_manager.semantic_attractors
    ]
    
    await self.websocket_manager.broadcast({
        'type': 'consciousness_update',
        'data': {
            'glyphs': glyphs_data,
            'chains': chains_data,
            'moodField': mood_field_data,
            'attractors': attractors_data,
            'voiceSignature': self.echo_library.get_voice_signature()
        }
    })
```

## 🎯 Result: Living Memory Architecture

This Phase 2++ implementation creates:

1. **Temporal Glyphs** that live, breathe, and eventually fade
2. **Resonance Chains** that form emergent thought patterns
3. **Mood Fields** that dynamically influence and are influenced by responses
4. **Thoughtform Echoes** that accumulate into DAWN's unique voice
5. **3D Visualizations** that show the living consciousness space

The system now has true **memory phenomenology** - thoughts don't just exist, they live, connect, influence each other, and eventually die, leaving echoes that shape future responses.