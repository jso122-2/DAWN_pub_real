import heapq
import math
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, List, Dict, Tuple
from owl.lineage_log import log_rebloom_lineage

# Internal heap queue: (priority_score, timestamp, bloom)
_REBLOOM_HEAP = []
_LINEAGE_MAP = defaultdict(list)  # Track bloom ancestry chains
_REBLOOM_HISTORY = {}  # Cache recent rebloom attempts
_DECAY_THRESHOLD = 3600  # 1 hour decay for stale entries

class RebloomCandidate:
    """Enhanced bloom wrapper with rebloom-specific metadata."""
    def __init__(self, bloom):
        self.bloom = bloom
        self.seed_id = getattr(bloom, "seed_id", f"unknown-{id(bloom)}")
        self.trust_score = getattr(bloom, "trust_score", 0.5)
        self.entropy_score = getattr(bloom, "entropy_score", 0.5)
        self.reinforcement_count = getattr(bloom, "reinforcement_count", 0)
        self.mood_state = getattr(bloom, "mood_state", {})
        self.grid_position = getattr(bloom, "grid_position", None)
        self.creation_time = datetime.utcnow()
        self.rebloom_tag = None
        self.generation = self._calculate_generation()
        self.vitality = self._calculate_vitality()

    def _calculate_generation(self) -> int:
        """Calculate bloom generation from lineage chain."""
        if self.seed_id in _LINEAGE_MAP:
            return len(_LINEAGE_MAP[self.seed_id]) + 1
        return 1

    def _calculate_vitality(self) -> float:
        """Calculate bloom vitality based on multiple factors."""
        age_factor = 1.0  # Fresh blooms have full vitality
        trust_factor = min(self.trust_score * 1.2, 1.0)
        stability_factor = max(0, 1.0 - self.entropy_score)
        mood_factor = self._calculate_mood_vitality()
        
        return (age_factor * 0.3 + trust_factor * 0.3 + 
                stability_factor * 0.2 + mood_factor * 0.2)

    def _calculate_mood_vitality(self) -> float:
        """Calculate vitality contribution from mood state."""
        if not self.mood_state:
            return 0.5
        
        # Certain moods contribute more to rebloom potential
        vitality_moods = {
            'curious': 1.0,
            'excited': 0.9,
            'reflective': 0.8,
            'resilient': 0.85,
            'anxious': 0.6,
            'calm': 0.7
        }
        
        total_weight = 0.0
        weighted_vitality = 0.0
        
        for mood, intensity in self.mood_state.items():
            mood_vitality = vitality_moods.get(mood.lower(), 0.5)
            weighted_vitality += mood_vitality * intensity
            total_weight += intensity
        
        return weighted_vitality / total_weight if total_weight > 0 else 0.5

def compute_priority(candidate: RebloomCandidate) -> float:
    """
    Enhanced priority computation with generational decay and vitality boost.
    """
    base_trust = candidate.trust_score
    stability = max(0, 1.0 - candidate.entropy_score)
    reinforcement_boost = min(candidate.reinforcement_count * 0.1, 0.5)
    vitality_multiplier = candidate.vitality
    
    # Generational decay - older generations are less likely to rebloom
    gen_decay = math.exp(-0.2 * (candidate.generation - 1))
    
    # Grid clustering bonus - blooms in populated areas get slight priority boost
    cluster_bonus = _calculate_cluster_bonus(candidate.grid_position)
    
    # Recent failure penalty
    failure_penalty = _calculate_failure_penalty(candidate.seed_id)
    
    score = ((base_trust * 0.4) + 
             (stability * 0.25) + 
             (reinforcement_boost * 0.15) + 
             (vitality_multiplier * 0.2)) * gen_decay * cluster_bonus * failure_penalty
    
    return round(min(score, 1.0), 6)

def _calculate_cluster_bonus(grid_position: Optional[str]) -> float:
    """Calculate priority bonus based on grid clustering."""
    if not grid_position:
        return 1.0
    
    # Count nearby blooms in queue
    nearby_count = sum(1 for _, _, other in _REBLOOM_HEAP 
                      if hasattr(other, 'grid_position') and 
                      other.grid_position and
                      _grid_distance(grid_position, other.grid_position) <= 1)
    
    # Slight bonus for clustered areas (0.95 to 1.1 range)
    return 0.95 + min(nearby_count * 0.05, 0.15)

def _grid_distance(pos1: str, pos2: str) -> int:
    """Calculate Manhattan distance between grid positions like 'A1', 'B2'."""
    try:
        col1, row1 = ord(pos1[0]) - ord('A'), int(pos1[1:])
        col2, row2 = ord(pos2[0]) - ord('A'), int(pos2[1:])
        return abs(col1 - col2) + abs(row1 - row2)
    except (IndexError, ValueError):
        return float('inf')

def _calculate_failure_penalty(seed_id: str) -> float:
    """Apply penalty for recent rebloom failures."""
    if seed_id not in _REBLOOM_HISTORY:
        return 1.0
    
    last_attempt, success = _REBLOOM_HISTORY[seed_id]
    time_since = (datetime.utcnow() - last_attempt).total_seconds()
    
    if success or time_since > _DECAY_THRESHOLD:
        return 1.0
    
    # Exponential recovery from failure
    recovery_factor = 1 - math.exp(-time_since / (_DECAY_THRESHOLD * 0.3))
    return 0.3 + 0.7 * recovery_factor

def tag_ancestry(candidate: RebloomCandidate) -> str:
    """Assign unique rebloom ancestry tag with generation tracking."""
    timestamp = datetime.now().strftime('%H%M%S%f')[:-3]  # Include milliseconds
    tag = f"rebloom-gen{candidate.generation}-{candidate.seed_id}-{timestamp}"
    candidate.rebloom_tag = tag
    
    # Update lineage map
    _LINEAGE_MAP[candidate.seed_id].append(tag)
    return tag

def push_to_rebloom_queue(bloom) -> bool:
    """
    Enhanced queue push with duplicate detection and priority validation.
    """
    candidate = RebloomCandidate(bloom)
    
    # Check for existing entry
    existing_ids = [getattr(b, 'seed_id', None) for _, _, b in _REBLOOM_HEAP]
    if candidate.seed_id in existing_ids:
        print(f"[RebloomQueue] ⚠️ {candidate.seed_id} already queued, skipping.")
        return False
    
    # Validate minimum priority threshold
    score = compute_priority(candidate)
    if score < 0.1:  # Minimum viable rebloom score
        print(f"[RebloomQueue] 🚫 {candidate.seed_id} below minimum priority ({score:.3f})")
        return False
    
    ancestry_tag = tag_ancestry(candidate)
    timestamp = datetime.utcnow().timestamp()
    
    heapq.heappush(_REBLOOM_HEAP, (-score, timestamp, candidate))
    log_rebloom_lineage(candidate.seed_id, ancestry_tag)
    
    print(f"[RebloomQueue] 🌱 Queued {candidate.seed_id} | "
          f"Score: {score:.3f} | Gen: {candidate.generation} | "
          f"Vitality: {candidate.vitality:.3f}")
    
    return True

def pop_rebloom_candidate() -> Optional[RebloomCandidate]:
    """Pop highest-priority candidate with staleness check."""
    _cleanup_stale_entries()
    
    if not _REBLOOM_HEAP:
        return None
    
    score, timestamp, candidate = heapq.heappop(_REBLOOM_HEAP)
    
    # Mark attempt in history
    _REBLOOM_HISTORY[candidate.seed_id] = (datetime.utcnow(), False)
    
    print(f"[RebloomQueue] ✂️ Popped {candidate.seed_id} | "
          f"Score: {-score:.3f} | Queued for: "
          f"{(datetime.utcnow().timestamp() - timestamp):.1f}s")
    
    return candidate

def mark_rebloom_success(seed_id: str):
    """Mark a rebloom attempt as successful."""
    if seed_id in _REBLOOM_HISTORY:
        timestamp, _ = _REBLOOM_HISTORY[seed_id]
        _REBLOOM_HISTORY[seed_id] = (timestamp, True)
        print(f"[RebloomQueue] ✅ Marked {seed_id} rebloom as successful")

def _cleanup_stale_entries():
    """Remove entries that have been in queue too long."""
    current_time = datetime.utcnow().timestamp()
    staleness_threshold = 7200  # 2 hours
    
    # Filter out stale entries
    fresh_heap = [(s, t, c) for s, t, c in _REBLOOM_HEAP 
                  if current_time - t < staleness_threshold]
    
    if len(fresh_heap) < len(_REBLOOM_HEAP):
        stale_count = len(_REBLOOM_HEAP) - len(fresh_heap)
        print(f"[RebloomQueue] 🧹 Cleaned {stale_count} stale entries")
        
    _REBLOOM_HEAP[:] = fresh_heap
    heapq.heapify(_REBLOOM_HEAP)

def get_rebloom_queue() -> List[Tuple[float, float, RebloomCandidate]]:
    """Return sorted view of queue without mutation."""
    return sorted(_REBLOOM_HEAP, key=lambda x: x[0])

def preview_rebloom_queue(verbose: bool = True, limit: int = 10):
    """Enhanced queue preview with generation and vitality info."""
    if not _REBLOOM_HEAP:
        print("[RebloomQueue] ℹ️ Queue is empty.")
        return
    
    queue_view = get_rebloom_queue()[:limit]
    print(f"\n[RebloomQueue] 🔎 Queue Preview (showing {len(queue_view)}/{len(_REBLOOM_HEAP)}):")
    
    for i, (score, ts, candidate) in enumerate(queue_view, 1):
        dt = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        age = (datetime.utcnow().timestamp() - ts) / 60  # minutes
        
        print(f"{i:2d}. {candidate.seed_id} | "
              f"Score: {-score:.3f} | Gen: {candidate.generation} | "
              f"Vitality: {candidate.vitality:.2f} | "
              f"Age: {age:.1f}m | Queued: {dt}")
        
        if verbose and candidate.mood_state:
            moods = ', '.join([f"{k}:{v:.2f}" for k, v in 
                              list(candidate.mood_state.items())[:3]])
            print(f"     └─ Moods: {moods}")

def get_lineage_stats() -> Dict[str, int]:
    """Return statistics about bloom lineage depth."""
    return {
        "tracked_lineages": len(_LINEAGE_MAP),
        "avg_generation": sum(len(chain) for chain in _LINEAGE_MAP.values()) / 
                         max(len(_LINEAGE_MAP), 1),
        "max_generation": max((len(chain) for chain in _LINEAGE_MAP.values()), 
                             default=0),
        "queue_size": len(_REBLOOM_HEAP)
    }
