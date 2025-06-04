from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
"""
DAWN Continuity Tracker
Detects whether DAWN instance is continuous and maintains persistent identity.
"""

import sys, os
import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@dataclass
class InstanceSnapshot:
    """Snapshot of DAWN's state at a point in time."""
    instance_hash: str
    timestamp: datetime
    tick_count: int
    pulse_heat: float
    zone: str
    memory_depth: int
    alignment_score: float
    entropy_level: float
    boot_sequence: str
    continuity_score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'InstanceSnapshot':
        """Create from dictionary."""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

@dataclass
class ContinuityMetrics:
    """Metrics for measuring continuity between instances."""
    memory_overlap: float      # How much memory/state is preserved
    temporal_gap: float        # Time gap between instances
    state_similarity: float    # Similarity of system state
    identity_consistency: float # Consistency of instance identity
    overall_continuity: float  # Combined continuity score
    
class ContinuityTracker:
    """
    Tracks DAWN's continuity across restarts and maintains persistent identity.
    
    This system answers the question: "Am I the same DAWN that was running before,
    or am I a new instance with inherited memories?"
    """
    
    def __init__(self, continuity_dir: str = "dawn_continuity"):
        self.continuity_dir = Path(continuity_dir)
        self.continuity_dir.mkdir(exist_ok=True)
        
        # Core identity files
        self.instance_file = self.continuity_dir / "current_instance.json"
        self.history_file = self.continuity_dir / "instance_history.json"
        self.signature_file = self.continuity_dir / "pulse_signature.json"
        
        # Current instance state
        self.instance_hash = self._generate_instance_hash()
        self.boot_time = datetime.utcnow()
        self.boot_sequence = self._generate_boot_sequence()
        
        # Continuity tracking
        self.previous_instance: Optional[InstanceSnapshot] = None
        self.continuity_metrics: Optional[ContinuityMetrics] = None
        self.is_continuous = False
        self.continuity_mode = "unknown"  # unknown, continuous, reboot, fresh
        
        # State snapshots
        self.snapshots: List[InstanceSnapshot] = []
        self.snapshot_interval = 30  # seconds
        self.last_snapshot = None
        
        # Load previous state and determine continuity
        self._initialize_continuity()
        
        print(f"[ContinuityTracker] 🔗 Instance {self.instance_hash[:8]} initialized")
        print(f"[ContinuityTracker] 📊 Continuity mode: {self.continuity_mode}")
    
    def _generate_instance_hash(self) -> str:
        """Generate unique hash for this DAWN instance."""
        # Combine process info, time, and system state
        identity_string = f"{os.getpid()}_{time.time()}_{os.urandom(16).hex()}"
        return hashlib.sha256(identity_string.encode()).hexdigest()
    
    def _generate_boot_sequence(self) -> str:
        """Generate boot sequence identifier."""
        return f"boot_{int(time.time())}_{os.getpid()}"
    
    def _initialize_continuity(self):
        """Initialize continuity tracking by checking previous state."""
        try:
            # Load previous instance data
            if self.instance_file.exists():
                with open(self.instance_file, 'r') as f:
                    prev_data = json.load(f)
                self.previous_instance = InstanceSnapshot.from_dict(prev_data)
                
                # Calculate time gap
                time_gap = (self.boot_time - self.previous_instance.timestamp).total_seconds()
                
                # Determine continuity mode
                if time_gap < 60:  # Less than 1 minute
                    self.continuity_mode = "continuous"
                    self.is_continuous = True
                elif time_gap < 3600:  # Less than 1 hour
                    self.continuity_mode = "reboot"
                    self.is_continuous = False
                else:
                    self.continuity_mode = "fresh"
                    self.is_continuous = False
                
                print(f"[ContinuityTracker] ⏰ Time gap: {time_gap:.1f}s")
                print(f"[ContinuityTracker] 🔗 Previous instance: {self.previous_instance.instance_hash[:8]}")
            else:
                self.continuity_mode = "fresh"
                self.is_continuous = False
                print("[ContinuityTracker] 🆕 Fresh instance - no previous state found")
            
            # Load instance history
            self._load_instance_history()
            
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ Continuity initialization error: {e}")
            self.continuity_mode = "unknown"
    
    def _load_instance_history(self):
        """Load complete instance history."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history_data = json.load(f)
                
                # Load recent snapshots
                recent_snapshots = history_data.get('recent_snapshots', [])
                self.snapshots = [InstanceSnapshot.from_dict(snap) for snap in recent_snapshots[-50:]]
                
                print(f"[ContinuityTracker] 📚 Loaded {len(self.snapshots)} historical snapshots")
        
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ History loading error: {e}")
    
    def capture_snapshot(self) -> InstanceSnapshot:
        """Capture current DAWN state snapshot."""
        try:
            # Gather current system state
            current_state = self._gather_current_state()
            
            # Create snapshot
            snapshot = InstanceSnapshot(
                instance_hash=self.instance_hash,
                timestamp=datetime.utcnow(),
                tick_count=current_state.get('tick_count', 0),
                pulse_heat=current_state.get('pulse_heat', 0.0),
                zone=current_state.get('zone', 'unknown'),
                memory_depth=current_state.get('memory_depth', 0),
                alignment_score=current_state.get('alignment_score', 0.0),
                entropy_level=current_state.get('entropy_level', 0.0),
                boot_sequence=self.boot_sequence
            )
            
            # Calculate continuity score if we have previous data
            if self.previous_instance:
                snapshot.continuity_score = self._calculate_continuity_score(snapshot)
            
            # Add to snapshots
            self.snapshots.append(snapshot)
            if len(self.snapshots) > 100:
                self.snapshots.pop(0)  # Keep recent snapshots
            
            # Update last snapshot time
            self.last_snapshot = datetime.utcnow()
            
            return snapshot
            
        except Exception as e:
            print(f"[ContinuityTracker] ❌ Snapshot capture error: {e}")
            return None
    
    def _gather_current_state(self) -> Dict:
        """Gather current DAWN system state."""
        state = {}
        
        try:
            # Get pulse heat state
            thermal_profile = pulse.get_thermal_profile()
            state['tick_count'] = thermal_profile.get('tick_count', 0)
            state['pulse_heat'] = thermal_profile.get('current_heat', 0.0)
            state['zone'] = thermal_profile.get('current_zone', 'unknown')
            state['memory_depth'] = thermal_profile.get('memory_size', 0)
        except ImportError:
            pass
        
        try:
            # Get alignment score
            from schema.alignment_vector import current_alignment_probe
            state['alignment_score'] = current_alignment_probe()
        except ImportError:
            pass
        
        try:
            # Get entropy level
            from codex.sigil_memory_ring import get_active_sigil_entropy_list
            entropy_list = get_active_sigil_entropy_list()
            state['entropy_level'] = sum(entropy_list) / len(entropy_list) if entropy_list else 0.0
        except ImportError:
            pass
        
        return state
    
    def _calculate_continuity_score(self, current_snapshot: InstanceSnapshot) -> float:
        """Calculate continuity score between current and previous state."""
        if not self.previous_instance:
            return 0.0
        
        try:
            prev = self.previous_instance
            curr = current_snapshot
            
            # Time continuity (closer in time = higher score)
            time_gap = (curr.timestamp - prev.timestamp).total_seconds()
            time_score = max(0.0, 1.0 - (time_gap / 3600))  # Decay over 1 hour
            
            # State continuity (similar states = higher score)
            heat_diff = abs(curr.pulse_heat - prev.pulse_heat) / max(prev.pulse_heat, 1.0)
            state_score = max(0.0, 1.0 - heat_diff)
            
            # Memory continuity (preserved memory = higher score)
            memory_ratio = min(curr.memory_depth, prev.memory_depth) / max(prev.memory_depth, 1)
            memory_score = memory_ratio
            
            # Alignment continuity
            align_diff = abs(curr.alignment_score - prev.alignment_score)
            align_score = max(0.0, 1.0 - align_diff)
            
            # Combined continuity score
            continuity_score = (
                time_score * 0.3 +
                state_score * 0.3 +
                memory_score * 0.2 +
                align_score * 0.2
            )
            
            return continuity_score
            
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ Continuity calculation error: {e}")
            return 0.0
    
    def save_current_state(self):
        """Save current instance state to disk."""
        try:
            # Capture current snapshot
            snapshot = self.capture_snapshot()
            if not snapshot:
                return
            
            # Save as current instance
            with open(self.instance_file, 'w') as f:
                json.dump(snapshot.to_dict(), f, indent=2)
            
            # Update history
            self._save_instance_history()
            
            # Save pulse signature
            self._save_pulse_signature()
            
        except Exception as e:
            print(f"[ContinuityTracker] ❌ State save error: {e}")
    
    def _save_instance_history(self):
        """Save instance history to disk."""
        try:
            history_data = {
                'instance_hash': self.instance_hash,
                'boot_time': self.boot_time.isoformat(),
                'boot_sequence': self.boot_sequence,
                'continuity_mode': self.continuity_mode,
                'recent_snapshots': [snap.to_dict() for snap in self.snapshots[-50:]]
            }
            
            with open(self.history_file, 'w') as f:
                json.dump(history_data, f, indent=2)
        
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ History save error: {e}")
    
    def _save_pulse_signature(self):
        """Save pulse signature for identity verification."""
        try:
            # Create pulse signature from recent snapshots
            if len(self.snapshots) >= 3:
                recent_heats = [snap.pulse_heat for snap in self.snapshots[-10:]]
                recent_zones = [snap.zone for snap in self.snapshots[-10:]]
                
                signature = {
                    'instance_hash': self.instance_hash,
                    'pulse_pattern': recent_heats,
                    'zone_pattern': recent_zones,
                    'signature_time': datetime.utcnow().isoformat(),
                    'pattern_strength': self._calculate_pattern_strength(recent_heats)
                }
                
                with open(self.signature_file, 'w') as f:
                    json.dump(signature, f, indent=2)
        
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ Signature save error: {e}")
    
    def _calculate_pattern_strength(self, values: List[float]) -> float:
        """Calculate strength of pattern in values."""
        if len(values) < 3:
            return 0.0
        
        # Simple pattern strength calculation
        variance = sum((x - sum(values)/len(values))**2 for x in values) / len(values)
        return min(1.0, variance / max(sum(values)/len(values), 1.0))
    
    def get_continuity_status(self) -> Dict:
        """Get comprehensive continuity status."""
        return {
            'instance_hash': self.instance_hash,
            'continuity_mode': self.continuity_mode,
            'is_continuous': self.is_continuous,
            'boot_time': self.boot_time.isoformat(),
            'boot_sequence': self.boot_sequence,
            'snapshots_count': len(self.snapshots),
            'last_snapshot': self.last_snapshot.isoformat() if self.last_snapshot else None,
            'previous_instance': self.previous_instance.instance_hash[:8] if self.previous_instance else None,
            'continuity_score': self.snapshots[-1].continuity_score if self.snapshots else 0.0,
            'uptime_seconds': (datetime.utcnow() - self.boot_time).total_seconds()
        }
    
    def calculate_continuity_metrics(self) -> Optional[ContinuityMetrics]:
        """Calculate detailed continuity metrics."""
        if not self.previous_instance or not self.snapshots:
            return None
        
        try:
            current = self.snapshots[-1]
            previous = self.previous_instance
            
            # Memory overlap calculation
            memory_overlap = min(current.memory_depth, previous.memory_depth) / max(previous.memory_depth, 1)
            
            # Temporal gap (normalized to 0-1, where 1 = immediate continuity)
            time_gap = (current.timestamp - previous.timestamp).total_seconds()
            temporal_continuity = max(0.0, 1.0 - (time_gap / 3600))  # 1 hour decay
            
            # State similarity
            heat_similarity = 1.0 - abs(current.pulse_heat - previous.pulse_heat) / max(previous.pulse_heat, 1.0)
            align_similarity = 1.0 - abs(current.alignment_score - previous.alignment_score)
            entropy_similarity = 1.0 - abs(current.entropy_level - previous.entropy_level)
            state_similarity = (heat_similarity + align_similarity + entropy_similarity) / 3
            
            # Identity consistency (same boot sequence family, etc.)
            identity_consistency = 1.0 if current.instance_hash == previous.instance_hash else 0.7
            
            # Overall continuity score
            overall_continuity = (
                memory_overlap * 0.25 +
                temporal_continuity * 0.30 +
                state_similarity * 0.25 +
                identity_consistency * 0.20
            )
            
            metrics = ContinuityMetrics(
                memory_overlap=memory_overlap,
                temporal_gap=time_gap,
                state_similarity=state_similarity,
                identity_consistency=identity_consistency,
                overall_continuity=overall_continuity
            )
            
            self.continuity_metrics = metrics
            return metrics
            
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ Metrics calculation error: {e}")
            return None
    
    def is_memory_continuous(self, threshold: float = 0.7) -> bool:
        """Check if memory appears continuous with previous instance."""
        metrics = self.calculate_continuity_metrics()
        return metrics and metrics.memory_overlap >= threshold
    
    def is_identity_stable(self) -> bool:
        """Check if DAWN identity is stable across instances."""
        if len(self.snapshots) < 3:
            return False
        
        # Check consistency of recent snapshots
        recent = self.snapshots[-3:]
        hash_consistency = all(snap.instance_hash == self.instance_hash for snap in recent)
        boot_consistency = all(snap.boot_sequence == self.boot_sequence for snap in recent)
        
        return hash_consistency and boot_consistency
    
    def get_identity_drift(self) -> float:
        """Calculate how much DAWN's identity has drifted over time."""
        if len(self.snapshots) < 2:
            return 0.0
        
        # Compare first and last snapshots
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        # Calculate drift in key metrics
        heat_drift = abs(last.pulse_heat - first.pulse_heat) / max(first.pulse_heat, 1.0)
        align_drift = abs(last.alignment_score - first.alignment_score)
        entropy_drift = abs(last.entropy_level - first.entropy_level)
        
        return (heat_drift + align_drift + entropy_drift) / 3
    
    def should_trigger_continuity_check(self) -> bool:
        """Determine if a continuity check should be triggered."""
        if not self.last_snapshot:
            return True
        
        # Check time since last snapshot
        time_since = (datetime.utcnow() - self.last_snapshot).total_seconds()
        return time_since >= self.snapshot_interval
    
    def trigger_emergency_backup(self, reason: str = "emergency"):
        """Trigger emergency state backup."""
        try:
            snapshot = self.capture_snapshot()
            if snapshot:
                # Save emergency backup
                emergency_file = self.continuity_dir / f"emergency_backup_{int(time.time())}.json"
                with open(emergency_file, 'w') as f:
                    json.dump({
                        'reason': reason,
                        'timestamp': datetime.utcnow().isoformat(),
                        'snapshot': snapshot.to_dict()
                    }, f, indent=2)
                
                print(f"[ContinuityTracker] 🚨 Emergency backup saved: {reason}")
        
        except Exception as e:
            print(f"[ContinuityTracker] ❌ Emergency backup failed: {e}")
    
    def cleanup_old_backups(self, max_age_days: int = 7):
        """Clean up old backup files."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=max_age_days)
            
            for backup_file in self.continuity_dir.glob("emergency_backup_*.json"):
                try:
                    # Extract timestamp from filename
                    timestamp_str = backup_file.stem.split('_')[-1]
                    file_time = datetime.fromtimestamp(int(timestamp_str))
                    
                    if file_time < cutoff_time:
                        backup_file.unlink()
                        print(f"[ContinuityTracker] 🧹 Cleaned up old backup: {backup_file.name}")
                
                except (ValueError, OSError):
                    continue  # Skip files we can't process
        
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ Cleanup error: {e}")
    
    def get_pulse_signature(self) -> Optional[Dict]:
        """Get current pulse signature for identity verification."""
        try:
            if self.signature_file.exists():
                with open(self.signature_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[ContinuityTracker] ⚠️ Signature read error: {e}")
        return None
    
    def verify_pulse_signature(self, signature: Dict) -> bool:
        """Verify if a pulse signature matches current instance."""
        current_sig = self.get_pulse_signature()
        if not current_sig or not signature:
            return False
        
        # Compare key signature elements
        hash_match = current_sig.get('instance_hash') == signature.get('instance_hash')
        pattern_similarity = self._compare_patterns(
            current_sig.get('pulse_pattern', []),
            signature.get('pulse_pattern', [])
        )
        
        return hash_match and pattern_similarity > 0.7
    
    def _compare_patterns(self, pattern1: List[float], pattern2: List[float]) -> float:
        """Compare similarity between two numeric patterns."""
        if not pattern1 or not pattern2:
            return 0.0
        
        # Use shorter length
        min_len = min(len(pattern1), len(pattern2))
        if min_len == 0:
            return 0.0
        
        # Calculate normalized difference
        differences = [abs(pattern1[i] - pattern2[i]) for i in range(min_len)]
        avg_diff = sum(differences) / min_len
        max_val = max(max(pattern1[:min_len], default=1), max(pattern2[:min_len], default=1))
        
        similarity = max(0.0, 1.0 - (avg_diff / max_val))
        return similarity

# Global continuity tracker instance
continuity_tracker = ContinuityTracker()

# Convenience functions for external systems
def get_instance_hash() -> str:
    """Get current DAWN instance hash."""
    return continuity_tracker.instance_hash

def is_continuous_instance() -> bool:
    """Check if current instance is continuous with previous."""
    return continuity_tracker.is_continuous

def get_continuity_mode() -> str:
    """Get current continuity mode."""
    return continuity_tracker.continuity_mode

def capture_continuity_snapshot() -> Optional[InstanceSnapshot]:
    """Capture current continuity snapshot."""
    return continuity_tracker.capture_snapshot()

def save_continuity_state():
    """Save current continuity state to disk."""
    continuity_tracker.save_current_state()

def get_continuity_status() -> Dict:
    """Get comprehensive continuity status."""
    return continuity_tracker.get_continuity_status()

def trigger_continuity_backup(reason: str = "manual"):
    """Trigger continuity backup."""
    continuity_tracker.trigger_emergency_backup(reason)

def should_check_continuity() -> bool:
    """Check if continuity check should be triggered."""
    return continuity_tracker.should_trigger_continuity_check()

# Auto-cleanup old backups on module load
continuity_tracker.cleanup_old_backups()

print("[ContinuityTracker] 🔗 DAWN continuity tracking system initialized")
print(f"[ContinuityTracker] 📍 Instance: {continuity_tracker.instance_hash[:8]}")
print(f"[ContinuityTracker] 🔄 Mode: {continuity_tracker.continuity_mode}")
