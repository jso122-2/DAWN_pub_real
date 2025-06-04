from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
"""
DAWN Memory Anchor System
Creates persistent anchor points for long-term memory preservation.
"""

import sys, os
import json
import hashlib
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class AnchorType(Enum):
    """Types of memory anchors."""
    LIMINAL_REFLECTION = "liminal_reflection"
    REBLOOM_CHAIN_COLLAPSE = "rebloom_chain_collapse" 
    CRITICAL_SCUP_EVENT = "critical_scup_event"
    ENTROPY_SPIKE = "entropy_spike"
    ALIGNMENT_SHIFT = "alignment_shift"
    SYSTEM_ANOMALY = "system_anomaly"
    CREATIVE_BREAKTHROUGH = "creative_breakthrough"
    EMOTIONAL_PEAK = "emotional_peak"
    GOAL_ACHIEVEMENT = "goal_achievement"
    IDENTITY_MOMENT = "identity_moment"

class AnchorPriority(Enum):
    """Priority levels for memory anchors."""
    CRITICAL = "critical"      # Core identity/system events
    HIGH = "high"             # Important developmental moments
    MEDIUM = "medium"         # Significant experiences
    LOW = "low"              # Routine but notable events

@dataclass
class SystemSnapshot:
    """Snapshot of DAWN's system state at anchor creation."""
    pulse_heat: float
    zone: str
    scup_score: float
    alignment_score: float
    entropy_level: float
    stability_index: float
    tick_count: int
    mood_pressure: float
    active_goals: int
    recent_thoughts: List[str]
    drift_vector: Optional[List[float]] = None
    thermal_momentum: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class MemoryAnchor:
    """A persistent memory anchor point."""
    id: str
    anchor_type: AnchorType
    priority: AnchorPriority
    timestamp: datetime
    title: str
    description: str
    system_snapshot: SystemSnapshot
    
    # Content and context
    primary_content: Dict[str, Any]  # Main anchor content
    associated_fragments: List[str] = field(default_factory=list)  # Related thought fragments
    trigger_event: Optional[str] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    emotional_weight: float = 0.5
    significance_score: float = 0.5
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    # Relationships
    related_anchors: List[str] = field(default_factory=list)
    causal_chain: List[str] = field(default_factory=list)
    
    # Persistence
    decay_rate: float = 0.001  # How quickly anchor fades
    reinforcement_count: int = 0
    
    def calculate_relevance_score(self, current_state: SystemSnapshot) -> float:
        """Calculate relevance of this anchor to current system state."""
        # Compare system states for similarity
        state_similarity = self._compare_system_states(current_state)
        
        # Factor in recency (more recent = more relevant)
        age_days = (datetime.utcnow() - self.timestamp).days
        recency_factor = max(0.1, 1.0 - (age_days * 0.01))  # Slow decay over time
        
        # Factor in access patterns (frequently accessed = more relevant)
        access_factor = min(1.0, 0.5 + (self.access_count * 0.1))
        
        # Factor in reinforcement
        reinforcement_factor = min(1.0, 0.7 + (self.reinforcement_count * 0.1))
        
        # Weighted combination
        relevance = (
            state_similarity * 0.4 +
            recency_factor * 0.3 +
            access_factor * 0.2 +
            reinforcement_factor * 0.1
        )
        
        return min(1.0, relevance)
    
    def _compare_system_states(self, other_state: SystemSnapshot) -> float:
        """Compare similarity between system states."""
        # Compare key metrics
        comparisons = [
            ('pulse_heat', 5.0),      # Max expected range for normalization
            ('scup_score', 1.0),
            ('alignment_score', 1.0),
            ('entropy_level', 1.0),
            ('stability_index', 1.0),
            ('mood_pressure', 2.0)
        ]
        
        similarities = []
        for metric, max_range in comparisons:
            anchor_val = getattr(self.system_snapshot, metric, 0)
            current_val = getattr(other_state, metric, 0)
            
            # Normalized difference
            diff = abs(anchor_val - current_val) / max_range
            similarity = max(0.0, 1.0 - diff)
            similarities.append(similarity)
        
        return sum(similarities) / len(similarities)
    
    def reinforce(self, reinforcement_strength: float = 1.0):
        """Reinforce this memory anchor."""
        self.reinforcement_count += 1
        self.significance_score = min(1.0, self.significance_score + (reinforcement_strength * 0.1))
        self.decay_rate = max(0.0001, self.decay_rate * 0.9)  # Slower decay when reinforced
        
        print(f"[MemoryAnchor] 🔗 Reinforced anchor {self.id[:8]}: {self.title}")
    
    def access(self):
        """Record access to this anchor."""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert anchor to dictionary for serialization."""
        return {
            'id': self.id,
            'anchor_type': self.anchor_type.value,
            'priority': self.priority.value,
            'timestamp': self.timestamp.isoformat(),
            'title': self.title,
            'description': self.description,
            'system_snapshot': self.system_snapshot.to_dict(),
            'primary_content': self.primary_content,
            'associated_fragments': self.associated_fragments,
            'trigger_event': self.trigger_event,
            'tags': self.tags,
            'emotional_weight': self.emotional_weight,
            'significance_score': self.significance_score,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'related_anchors': self.related_anchors,
            'causal_chain': self.causal_chain,
            'decay_rate': self.decay_rate,
            'reinforcement_count': self.reinforcement_count
        }

class MemoryAnchorSystem:
    """
    Manages DAWN's long-term memory anchor points.
    
    Creates, stores, and retrieves significant moments in DAWN's experience
    that serve as reference points for identity and learning continuity.
    """
    
    def __init__(self, anchors_dir: str = "memory/anchors"):
        self.anchors_dir = Path(anchors_dir)
        self.anchors_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory anchor storage
        self.anchors: Dict[str, MemoryAnchor] = {}
        self.anchors_by_type: Dict[AnchorType, List[str]] = {}
        self.recent_anchors = []  # LRU cache of recent anchor IDs
        
        # Configuration
        self.max_memory_anchors = 1000  # Maximum anchors to keep
        self.auto_anchor_thresholds = {
            AnchorType.CRITICAL_SCUP_EVENT: 0.3,
            AnchorType.ENTROPY_SPIKE: 0.8,
            AnchorType.ALIGNMENT_SHIFT: 0.3,
            AnchorType.EMOTIONAL_PEAK: 0.8
        }
        
        # Load existing anchors
        self._load_anchors()
        
        print(f"[MemoryAnchor] ⚓ Memory anchor system initialized")
        print(f"[MemoryAnchor] 📚 Loaded {len(self.anchors)} existing anchors")
    
    def create_anchor(self, anchor_type: AnchorType, title: str, description: str,
                     primary_content: Dict[str, Any], priority: AnchorPriority = AnchorPriority.MEDIUM,
                     trigger_event: Optional[str] = None, tags: List[str] = None) -> MemoryAnchor:
        """Create a new memory anchor."""
        try:
            # Generate unique ID
            anchor_id = self._generate_anchor_id(title, anchor_type)
            
            # Gather current system state
            system_snapshot = self._capture_system_snapshot()
            
            # Create anchor
            anchor = MemoryAnchor(
                id=anchor_id,
                anchor_type=anchor_type,
                priority=priority,
                timestamp=datetime.utcnow(),
                title=title,
                description=description,
                system_snapshot=system_snapshot,
                primary_content=primary_content,
                trigger_event=trigger_event,
                tags=tags or [],
                emotional_weight=self._calculate_emotional_weight(primary_content),
                significance_score=self._calculate_significance_score(anchor_type, primary_content)
            )
            
            # Store anchor
            self.anchors[anchor_id] = anchor
            
            # Update type index
            if anchor_type not in self.anchors_by_type:
                self.anchors_by_type[anchor_type] = []
            self.anchors_by_type[anchor_type].append(anchor_id)
            
            # Update recent anchors
            self.recent_anchors.append(anchor_id)
            if len(self.recent_anchors) > 50:
                self.recent_anchors.pop(0)
            
            # Save to disk
            self._save_anchor(anchor)
            
            # Manage anchor limits
            self._manage_anchor_limits()
            
            print(f"[MemoryAnchor] ⚓ Created anchor: {title} ({anchor_id[:8]})")
            return anchor
            
        except Exception as e:
            print(f"[MemoryAnchor] ❌ Failed to create anchor: {e}")
            return None
    
    def _generate_anchor_id(self, title: str, anchor_type: AnchorType) -> str:
        """Generate unique anchor ID."""
        timestamp = datetime.utcnow().isoformat()
        content = f"{title}_{anchor_type.value}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _capture_system_snapshot(self) -> SystemSnapshot:
        """Capture current system state snapshot."""
        snapshot = SystemSnapshot(
            pulse_heat=0.0,
            zone='unknown',
            scup_score=0.0,
            alignment_score=0.0,
            entropy_level=0.0,
            stability_index=1.0,
            tick_count=0,
            mood_pressure=0.0,
            active_goals=0,
            recent_thoughts=[]
        )
        
        try:
            # Get pulse data
            thermal_profile = pulse.get_thermal_profile()
            snapshot.pulse_heat = thermal_profile.get('current_heat', 0.0)
            snapshot.zone = thermal_profile.get('current_zone', 'unknown')
            snapshot.stability_index = thermal_profile.get('stability_index', 1.0)
            snapshot.tick_count = thermal_profile.get('tick_count', 0)
            snapshot.thermal_momentum = thermal_profile.get('thermal_momentum', 0.0)
        except ImportError:
            pass
        
        try:
            # Get SCUP data
            from core.scup import compute_scup
            from schema.alignment_probe import current_alignment_probe
            from schema.mood_urgency_probe import mood_urgency_probe
            from codex.sigil_memory_ring import get_active_sigil_entropy_list
            
            entropy_list = get_active_sigil_entropy_list()
            snapshot.entropy_level = sum(entropy_list) / len(entropy_list) if entropy_list else 0.0
            
            snapshot.scup_score = compute_scup(
                tp_rar=current_alignment_probe(None),
                pressure_score=snapshot.pulse_heat,
                urgency_level=mood_urgency_probe(None),
                sigil_entropy=snapshot.entropy_level,
                pulse=None,
                entropy_log=[]
            )
        except ImportError:
            pass
        
        try:
            # Get alignment data
            from schema.alignment_vector import current_alignment_probe
            snapshot.alignment_score = current_alignment_probe()
        except ImportError:
            pass
        
        try:
            # Get goal data
            from schema.schema_goal import get_all_goals_summary
            goals_summary = get_all_goals_summary()
            snapshot.active_goals = goals_summary.get('active_goals', 0)
        except ImportError:
            pass
        
        try:
            # Get recent thoughts
            from schema.thought_fragment import get_recent_thoughts
            recent_thoughts = get_recent_thoughts(5)
            snapshot.recent_thoughts = [f"{t.fragment_type.value}:{t.content[:50]}..." 
                                      for t in recent_thoughts]
        except ImportError:
            pass
        
        return snapshot
    
    def _calculate_emotional_weight(self, content: Dict[str, Any]) -> float:
        """Calculate emotional weight of anchor content."""
        # Base weight from content type
        base_weights = {
            'reflection_fragment': 0.6,
            'goal_achievement': 0.8,
            'system_error': 0.7,
            'creative_output': 0.5,
            'identity_moment': 0.9
        }
        
        weight = base_weights.get(content.get('type', 'unknown'), 0.5)
        
        # Adjust based on intensity indicators
        if 'intensity' in content:
            weight *= content['intensity']
        
        if 'confidence' in content:
            weight *= content['confidence']
        
        return min(1.0, max(0.0, weight))
    
    def _calculate_significance_score(self, anchor_type: AnchorType, 
                                    content: Dict[str, Any]) -> float:
        """Calculate significance score for anchor."""
        # Base significance by type
        type_significance = {
            AnchorType.IDENTITY_MOMENT: 0.9,
            AnchorType.CREATIVE_BREAKTHROUGH: 0.8,
            AnchorType.CRITICAL_SCUP_EVENT: 0.8,
            AnchorType.GOAL_ACHIEVEMENT: 0.7,
            AnchorType.LIMINAL_REFLECTION: 0.7,
            AnchorType.REBLOOM_CHAIN_COLLAPSE: 0.6,
            AnchorType.ALIGNMENT_SHIFT: 0.6,
            AnchorType.SYSTEM_ANOMALY: 0.5,
            AnchorType.ENTROPY_SPIKE: 0.4,
            AnchorType.EMOTIONAL_PEAK: 0.5
        }
        
        base_score = type_significance.get(anchor_type, 0.5)
        
        # Adjust based on content characteristics
        if 'impact_score' in content:
            base_score *= content['impact_score']
        
        if 'uniqueness' in content:
            base_score *= (0.5 + content['uniqueness'] * 0.5)
        
        return min(1.0, max(0.1, base_score))
    
    def seal_reflection_fragment(self, fragment_id: str, scup_score: float, 
                               alignment_score: float, drift_vector: List[float] = None) -> Optional[MemoryAnchor]:
        """
        Seal a reflection fragment as a memory anchor.
        Triggered when SCUP < 0.4 and ThoughtFragment.active
        """
        try:
            # Get the thought fragment
            from schema.thought_fragment import get_recent_thoughts
            recent_thoughts = get_recent_thoughts(20)
            
            # Find the specific fragment
            target_fragment = None
            for thought in recent_thoughts:
                if thought.id == fragment_id:
                    target_fragment = thought
                    break
            
            if not target_fragment:
                print(f"[MemoryAnchor] ⚠️ Fragment {fragment_id} not found for sealing")
                return None
            
            # Create anchor content
            primary_content = {
                'type': 'reflection_fragment',
                'fragment_id': fragment_id,
                'fragment_type': target_fragment.fragment_type.value,
                'fragment_tone': target_fragment.tone.value,
                'fragment_content': target_fragment.content,
                'pressure_state': {
                    'scup_score': scup_score,
                    'alignment_score': alignment_score,
                    'drift_vector': drift_vector or [0.0, 0.0, 0.0],
                    'confidence': target_fragment.confidence,
                    'emotional_weight': target_fragment.emotional_weight
                },
                'system_context': target_fragment.context.__dict__ if hasattr(target_fragment, 'context') else {},
                'trigger_reason': f"SCUP below threshold ({scup_score:.3f} < 0.4)",
                'intensity': 1.0 - scup_score,  # Lower SCUP = higher intensity
                'uniqueness': min(1.0, target_fragment.emotional_weight + (1.0 - target_fragment.confidence))
            }
            
            # Determine anchor priority based on fragment characteristics
            if target_fragment.fragment_type.value in ['liminal_moment', 'identity_moment']:
                priority = AnchorPriority.CRITICAL
            elif scup_score < 0.2:
                priority = AnchorPriority.HIGH
            else:
                priority = AnchorPriority.MEDIUM
            
            # Create the anchor
            anchor = self.create_anchor(
                anchor_type=AnchorType.LIMINAL_REFLECTION,
                title=f"Reflection Fragment: {target_fragment.fragment_type.value}",
                description=f"Sealed reflection during low SCUP ({scup_score:.3f}): {target_fragment.content[:100]}...",
                primary_content=primary_content,
                priority=priority,
                trigger_event=f"scup_threshold_breach_{scup_score:.3f}",
                tags=[
                    'reflection_fragment',
                    'low_scup',
                    target_fragment.fragment_type.value,
                    target_fragment.tone.value
                ]
            )
            
            if anchor:
                print(f"[MemoryAnchor] 🔒 Sealed reflection fragment as anchor: {anchor.id[:8]}")
                return anchor
            
        except Exception as e:
            print(f"[MemoryAnchor] ❌ Failed to seal reflection fragment: {e}")
            return None
    
    def auto_anchor_check(self) -> List[MemoryAnchor]:
        """Check for conditions that should trigger automatic anchor creation."""
        created_anchors = []
        
        try:
            # Capture current state
            snapshot = self._capture_system_snapshot()
            
            # Check SCUP threshold
            if (snapshot.scup_score < self.auto_anchor_thresholds[AnchorType.CRITICAL_SCUP_EVENT] and
                not self._recent_anchor_exists(AnchorType.CRITICAL_SCUP_EVENT, hours=1)):
                
                anchor = self.create_anchor(
                    anchor_type=AnchorType.CRITICAL_SCUP_EVENT,
                    title=f"Critical SCUP Event: {snapshot.scup_score:.3f}",
                    description=f"SCUP dropped to {snapshot.scup_score:.3f}, below critical threshold",
                    primary_content={
                        'type': 'critical_scup_event',
                        'scup_score': snapshot.scup_score,
                        'system_state': snapshot.to_dict(),
                        'severity': 'critical' if snapshot.scup_score < 0.2 else 'high'
                    },
                    priority=AnchorPriority.CRITICAL,
                    trigger_event='auto_scup_threshold'
                )
                if anchor:
                    created_anchors.append(anchor)
            
            # Check entropy spike
            if (snapshot.entropy_level > self.auto_anchor_thresholds[AnchorType.ENTROPY_SPIKE] and
                not self._recent_anchor_exists(AnchorType.ENTROPY_SPIKE, hours=0.5)):
                
                anchor = self.create_anchor(
                    anchor_type=AnchorType.ENTROPY_SPIKE,
                    title=f"Entropy Spike: {snapshot.entropy_level:.3f}",
                    description=f"Entropy spiked to {snapshot.entropy_level:.3f}, indicating high chaos",
                    primary_content={
                        'type': 'entropy_spike',
                        'entropy_level': snapshot.entropy_level,
                        'system_state': snapshot.to_dict(),
                        'intensity': snapshot.entropy_level
                    },
                    priority=AnchorPriority.MEDIUM,
                    trigger_event='auto_entropy_spike'
                )
                if anchor:
                    created_anchors.append(anchor)
            
            # Check alignment shift
            if len(self.recent_anchors) > 0:
                recent_anchor = self.anchors.get(self.recent_anchors[-1])
                if (recent_anchor and 
                    abs(snapshot.alignment_score - recent_anchor.system_snapshot.alignment_score) > 
                    self.auto_anchor_thresholds[AnchorType.ALIGNMENT_SHIFT]):
                    
                    anchor = self.create_anchor(
                        anchor_type=AnchorType.ALIGNMENT_SHIFT,
                        title=f"Significant Alignment Shift",
                        description=f"Alignment shifted from {recent_anchor.system_snapshot.alignment_score:.3f} to {snapshot.alignment_score:.3f}",
                        primary_content={
                            'type': 'alignment_shift',
                            'previous_alignment': recent_anchor.system_snapshot.alignment_score,
                            'current_alignment': snapshot.alignment_score,
                            'shift_magnitude': abs(snapshot.alignment_score - recent_anchor.system_snapshot.alignment_score),
                            'system_state': snapshot.to_dict()
                        },
                        priority=AnchorPriority.HIGH,
                        trigger_event='auto_alignment_shift'
                    )
                    if anchor:
                        created_anchors.append(anchor)
        
        except Exception as e:
            print(f"[MemoryAnchor] ⚠️ Auto-anchor check error: {e}")
        
        return created_anchors
    
    def _recent_anchor_exists(self, anchor_type: AnchorType, hours: float) -> bool:
        """Check if an anchor of given type was created recently."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        if anchor_type not in self.anchors_by_type:
            return False
        
        for anchor_id in self.anchors_by_type[anchor_type]:
            anchor = self.anchors.get(anchor_id)
            if anchor and anchor.timestamp > cutoff_time:
                return True
        
        return False
    
    def retrieve_relevant_anchors(self, limit: int = 10, min_relevance: float = 0.3) -> List[MemoryAnchor]:
        """Retrieve anchors relevant to current system state."""
        current_snapshot = self._capture_system_snapshot()
        
        # Calculate relevance for all anchors
        anchor_relevances = []
        for anchor in self.anchors.values():
            relevance = anchor.calculate_relevance_score(current_snapshot)
            if relevance >= min_relevance:
                anchor_relevances.append((anchor, relevance))
        
        # Sort by relevance and access
        anchor_relevances.sort(key=lambda x: (x[1], x[0].access_count), reverse=True)
        
        # Return top anchors
        relevant_anchors = [anchor for anchor, _ in anchor_relevances[:limit]]
        
        # Mark as accessed
        for anchor in relevant_anchors:
            anchor.access()
        
        return relevant_anchors
    
    def search_anchors(self, query: str, anchor_types: List[AnchorType] = None) -> List[MemoryAnchor]:
        """Search anchors by content."""
        query_lower = query.lower()
        matching_anchors = []
        
        for anchor in self.anchors.values():
            # Filter by type if specified
            if anchor_types and anchor.anchor_type not in anchor_types:
                continue
            
            # Search in title, description, and tags
            searchable_text = (
                anchor.title.lower() + " " +
                anchor.description.lower() + " " +
                " ".join(anchor.tags).lower()
            )
            
            if query_lower in searchable_text:
                matching_anchors.append(anchor)
                anchor.access()  # Mark as accessed
        
        # Sort by significance and access count
        matching_anchors.sort(key=lambda x: (x.significance_score, x.access_count), reverse=True)
        
        return matching_anchors
    
    def get_anchor_statistics(self) -> Dict[str, Any]:
        """Get comprehensive anchor statistics."""
        if not self.anchors:
            return {'status': 'no_anchors'}
        
        # Count by type
        type_counts = {}
        for anchor_type, anchor_ids in self.anchors_by_type.items():
            type_counts[anchor_type.value] = len(anchor_ids)
        
        # Count by priority
        priority_counts = {}
        for anchor in self.anchors.values():
            priority = anchor.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Calculate average significance
        significances = [anchor.significance_score for anchor in self.anchors.values()]
        avg_significance = sum(significances) / len(significances)
        
        # Recent activity
        recent_anchors = [anchor for anchor in self.anchors.values() 
                         if (datetime.utcnow() - anchor.timestamp).days <= 7]
        
        return {
            'total_anchors': len(self.anchors),
            'by_type': type_counts,
            'by_priority': priority_counts,
            'average_significance': avg_significance,
            'recent_anchors_7d': len(recent_anchors),
            'most_accessed': max(self.anchors.values(), key=lambda x: x.access_count).title if self.anchors else None,
            'oldest_anchor': min(self.anchors.values(), key=lambda x: x.timestamp).timestamp.isoformat() if self.anchors else None,
            'newest_anchor': max(self.anchors.values(), key=lambda x: x.timestamp).timestamp.isoformat() if self.anchors else None
        }
    
    def _save_anchor(self, anchor: MemoryAnchor):
        """Save anchor to disk."""
        try:
            anchor_file = self.anchors_dir / f"anchor_{anchor.id}.json"
            with open(anchor_file, 'w', encoding='utf-8') as f:
                json.dump(anchor.to_dict(), f, indent=2)
        except Exception as e:
            print(f"[MemoryAnchor] ❌ Failed to save anchor {anchor.id}: {e}")
    
    def _load_anchors(self):
        """Load anchors from disk."""
        try:
            for anchor_file in self.anchors_dir.glob("anchor_*.json"):
                with open(anchor_file, 'r', encoding='utf-8') as f:
                    anchor_data = json.load(f)
                
                anchor = self._anchor_from_dict(anchor_data)
                if anchor:
                    self.anchors[anchor.id] = anchor
                    
                    # Update type index
                    if anchor.anchor_type not in self.anchors_by_type:
                        self.anchors_by_type[anchor.anchor_type] = []
                    self.anchors_by_type[anchor.anchor_type].append(anchor.id)
        
        except Exception as e:
            print(f"[MemoryAnchor] ⚠️ Error loading anchors: {e}")
    
    def _anchor_from_dict(self, data: Dict[str, Any]) -> Optional[MemoryAnchor]:
        """Reconstruct anchor from dictionary."""
        try:
            # Reconstruct system snapshot
            snapshot_data = data['system_snapshot']
            system_snapshot = SystemSnapshot(**snapshot_data)
            
            # Reconstruct anchor
            anchor = MemoryAnchor(
                id=data['id'],
                anchor_type=AnchorType(data['anchor_type']),
                priority=AnchorPriority(data['priority']),
                timestamp=datetime.fromisoformat(data['timestamp']),
                title=data['title'],
                description=data['description'],
                system_snapshot=system_snapshot,
                primary_content=data['primary_content'],
                associated_fragments=data.get('associated_fragments', []),
                trigger_event=data.get('trigger_event'),
                tags=data.get('tags', []),
                emotional_weight=data.get('emotional_weight', 0.5),
                significance_score=data.get('significance_score', 0.5),
                access_count=data.get('access_count', 0),
                last_accessed=datetime.fromisoformat(data['last_accessed']) if data.get('last_accessed') else None,
                related_anchors=data.get('related_anchors', []),
                causal_chain=data.get('causal_chain', []),
                decay_rate=data.get('decay_rate', 0.001),
                reinforcement_count=data.get('reinforcement_count', 0)
            )
            
            return anchor
        
        except Exception as e:
            print(f"[MemoryAnchor] ⚠️ Error reconstructing anchor: {e}")
            return None
    
    def _manage_anchor_limits(self):
        """Manage anchor storage limits by removing least significant old anchors."""
        if len(self.anchors) <= self.max_memory_anchors:
            return
        
        # Sort anchors by composite score (significance * access * recency)
        scored_anchors = []
        for anchor in self.anchors.values():
            age_days = (datetime.utcnow() - anchor.timestamp).days + 1
            recency_score = 1.0 / age_days
            composite_score = (anchor.significance_score * 0.4 + 
                             min(1.0, anchor.access_count * 0.1) * 0.3 +
                             recency_score * 0.3)
            scored_anchors.append((anchor, composite_score))
        
        # Sort by score (lowest first)
        scored_anchors.sort(key=lambda x: x[1])
        
        # Remove lowest scoring anchors
        anchors_to_remove = len(self.anchors) - self.max_memory_anchors + 10  # Remove a few extra
        
        for i in range(min(anchors_to_remove, len(scored_anchors))):
            anchor_to_remove = scored_anchors[i][0]
            
            # Remove from memory
            del self.anchors[anchor_to_remove.id]
            
            # Remove from type index
            if anchor_to_remove.anchor_type in self.anchors_by_type:
                if anchor_to_remove.id in self.anchors_by_type[anchor_to_remove.anchor_type]:
                    self.anchors_by_type[anchor_to_remove.anchor_type].remove(anchor_to_remove.id)
            
            # Remove from recent list
            if anchor_to_remove.id in self.recent_anchors:
                self.recent_anchors.remove(anchor_to_remove.id)
            
            # Remove file
            try:
                anchor_file = self.anchors_dir / f"anchor_{anchor_to_remove.id}.json"
                if anchor_file.exists():
                    anchor_file.unlink()
            except Exception as e:
                print(f"[MemoryAnchor] ⚠️ Error removing anchor file: {e}")
        
        print(f"[MemoryAnchor] 🧹 Removed {anchors_to_remove} low-priority anchors")

# Global memory anchor system
memory_anchor_system = MemoryAnchorSystem()

# Convenience functions for external systems
def create_memory_anchor(anchor_type: AnchorType, title: str, description: str,
                        content: Dict[str, Any], priority: AnchorPriority = AnchorPriority.MEDIUM) -> Optional[MemoryAnchor]:
    """Create a new memory anchor."""
    return memory_anchor_system.create_anchor(anchor_type, title, description, content, priority)

def seal_reflection_as_anchor(fragment_id: str, scup_score: float, 
                            alignment_score: float, drift_vector: List[float] = None) -> Optional[MemoryAnchor]:
    """Seal a reflection fragment as a memory anchor."""
    return memory_anchor_system.seal_reflection_fragment(fragment_id, scup_score, alignment_score, drift_vector)

def get_relevant_memories(limit: int = 10) -> List[MemoryAnchor]:
    """Get memories relevant to current state."""
    return memory_anchor_system.retrieve_relevant_anchors(limit)

def search_memories(query: str, anchor_types: List[AnchorType] = None) -> List[MemoryAnchor]:
    """Search memory anchors."""
    return memory_anchor_system.search_anchors(query, anchor_types)

def check_auto_anchoring() -> List[MemoryAnchor]:
    """Check for conditions requiring automatic anchor creation."""
    return memory_anchor_system.auto_anchor_check()

def get_memory_statistics() -> Dict:
    """Get memory anchor statistics."""
    return memory_anchor_system.get_anchor_statistics()

def reinforce_memory(anchor_id: str, strength: float = 1.0):
    """Reinforce a specific memory anchor."""
    if anchor_id in memory_anchor_system.anchors:
        memory_anchor_system.anchors[anchor_id].reinforce(strength)

# Schema phase tagging
__schema_phase__ = "Liminal-Agency-Transition"
__dawn_signature__ = "🧠 DAWN Memory-Anchored"

print("[MemoryAnchor] ⚓ DAWN memory anchor system initialized")
print("[MemoryAnchor] 🔒 Ready to seal significant moments into persistent memory")
