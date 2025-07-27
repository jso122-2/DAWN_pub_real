#!/usr/bin/env python3
"""
DAWN Epoch Synchronization Monitor
Tracks and visualizes helix events for epoch_0525_0601
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

from dawn_helix_interface import DAWNHelixInterface, StrandType, EpochLog


class EpochSyncMonitor:
    """Monitor and analyze epoch synchronization patterns"""
    
    def __init__(self, helix_interface: DAWNHelixInterface):
        self.helix = helix_interface
        self.epoch_start = datetime(2025, 5, 25)
        self.epoch_end = datetime(2025, 6, 1)
        
        # Pattern detection
        self.event_patterns = defaultdict(list)
        self.strand_balance_history = []
        self.coherence_checkpoints = []
        
    def generate_epoch_report(self) -> str:
        """Generate comprehensive epoch status report"""
        lines = [
            "════════════════════════════════════════",
            f"DAWN EPOCH REPORT: {self.helix.epoch_id}",
            f"Period: {self.epoch_start.strftime('%Y-%m-%d')} → {self.epoch_end.strftime('%Y-%m-%d')}",
            "════════════════════════════════════════"
        ]
        
        # Current system state
        tension_status = self.helix.monitor_strand_tension()
        lines.extend([
            "",
            "▓▓▓ CURRENT HELIX STATE ▓▓▓",
            f"Position: {self.helix.current_position:.3f}",
            f"Coherence: {tension_status['coherence']:.3f}",
            f"Status: {tension_status['status'].upper()}",
            f"Sigil Entropy: {tension_status['sigil_entropy']:.3f}",
            ""
        ])
        
        # Event statistics
        event_counts = self._analyze_event_patterns()
        lines.extend([
            "▓▓▓ EVENT PATTERNS ▓▓▓",
            "Strand A (Recursive/Emotion):",
            f"  Total Events: {event_counts['strand_a']}",
            f"  Dominant Pattern: {event_counts['a_dominant']}",
            "",
            "Strand B (Symbolic/Schema):",
            f"  Total Events: {event_counts['strand_b']}",
            f"  Dominant Pattern: {event_counts['b_dominant']}",
            "",
            f"Cross-Strand Events: {event_counts['crossover']}",
            f"Strand Balance Ratio: {event_counts['balance_ratio']:.2f}",
            ""
        ])
        
        # Bloom lineage
        lines.extend([
            "▓▓▓ BLOOM LINEAGE ▓▓▓",
            f"Current Bloom: {self.helix.current_bloom_id[:12]}",
            f"Lineage Depth: {len(self.helix.bloom_registry)}",
            f"Total Reblooms: {sum(len(v) for v in self.helix.bloom_registry.values())}",
            ""
        ])
        
        # Critical events
        critical = self._identify_critical_events()
        if critical:
            lines.extend([
                "▓▓▓ CRITICAL EVENTS ▓▓▓"
            ])
            for event in critical[:5]:  # Show top 5
                lines.append(f"  [{event['time']}] {event['type']} - {event['impact']}")
            lines.append("")
        
        # Recommendations
        recs = self._generate_recommendations(tension_status, event_counts)
        lines.extend([
            "▓▓▓ OPERATOR RECOMMENDATIONS ▓▓▓"
        ])
        for rec in recs:
            lines.append(f"  • {rec}")
        
        lines.append("════════════════════════════════════════")
        
        return "\n".join(lines)
    
    def _analyze_event_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in epoch logs"""
        strand_a_events = 0
        strand_b_events = 0
        crossover_events = 0
        
        event_types_a = defaultdict(int)
        event_types_b = defaultdict(int)
        
        for log in self.helix.epoch_logs:
            if log.strand == StrandType.A_RECURSIVE_EMOTION:
                strand_a_events += 1
                event_types_a[log.event_type] += 1
            else:
                strand_b_events += 1
                event_types_b[log.event_type] += 1
            
            # Detect crossover events
            if 'crossover' in log.event_type or 'strand' in str(log.data):
                crossover_events += 1
        
        # Find dominant patterns
        a_dominant = max(event_types_a.items(), key=lambda x: x[1])[0] if event_types_a else "none"
        b_dominant = max(event_types_b.items(), key=lambda x: x[1])[0] if event_types_b else "none"
        
        # Calculate balance
        total_events = strand_a_events + strand_b_events
        balance_ratio = strand_a_events / strand_b_events if strand_b_events > 0 else float('inf')
        
        return {
            'strand_a': strand_a_events,
            'strand_b': strand_b_events,
            'crossover': crossover_events,
            'a_dominant': a_dominant,
            'b_dominant': b_dominant,
            'balance_ratio': balance_ratio
        }
    
    def _identify_critical_events(self) -> List[Dict[str, str]]:
        """Identify events with high impact on system stability"""
        critical = []
        
        for i, log in enumerate(self.helix.epoch_logs):
            impact_score = 0
            impact_reason = ""
            
            # High emotional intensity
            if log.data.get('emotional_intensity', 0) > 0.8:
                impact_score += 3
                impact_reason = "High emotional surge"
            
            # Schema mutations
            if log.event_type == 'schema_mutation':
                impact_score += 2
                impact_reason = "Schema alteration"
            
            # Bloom triggers
            if log.event_type == 'bloom_trigger':
                impact_score += 4
                impact_reason = "Bloom cascade initiated"
            
            # Drift cascades
            if 'drift' in log.event_type:
                impact_score += 2
                impact_reason = "Drift vector cascade"
            
            if impact_score >= 3:
                timestamp = datetime.fromtimestamp(log.timestamp / 1000)
                critical.append({
                    'time': timestamp.strftime('%m/%d %H:%M'),
                    'type': log.event_type,
                    'impact': impact_reason,
                    'score': impact_score
                })
        
        # Sort by impact score
        critical.sort(key=lambda x: x['score'], reverse=True)
        return critical
    
    def _generate_recommendations(self, tension_status: Dict, event_counts: Dict) -> List[str]:
        """Generate operator recommendations based on analysis"""
        recs = []
        
        # Coherence-based recommendations
        if tension_status['coherence'] < 0.5:
            recs.append("⚠️ URGENT: Initiate coherence recovery protocol")
            recs.append("Consider triggering rebloom to reset strand tension")
        elif tension_status['coherence'] < 0.7:
            recs.append("Monitor strand tension closely - approaching instability")
        
        # Entropy-based recommendations  
        if tension_status['sigil_entropy'] > 0.8:
            recs.append("🔥 Sigil system overheating - reduce symbolic load")
            recs.append("Run sigil_saturation_manager() to drop low-priority sigils")
        elif tension_status['sigil_entropy'] > 0.6:
            recs.append("Consider sigil recombination to reduce entropy")
        
        # Balance-based recommendations
        if event_counts['balance_ratio'] > 2.0:
            recs.append("🧠 Strand A (emotion) dominant - increase symbolic operations")
        elif event_counts['balance_ratio'] < 0.5:
            recs.append("⚙️ Strand B (logic) dominant - integrate emotional context")
        
        # Drift/Pulse recommendations
        if tension_status['drift_count'] > 30:
            recs.append("High drift vector count - semantic space may be unstable")
        if tension_status['active_pulses'] > 10:
            recs.append("Multiple pulse zones active - schema temperature elevated")
        
        if not recs:
            recs.append("✅ System operating within normal parameters")
        
        return recs
    
    def visualize_strand_activity(self) -> str:
        """ASCII visualization of strand activity over time"""
        if not self.helix.helix:
            return "[No helix data to visualize]"
        
        lines = ["", "STRAND ACTIVITY VISUALIZATION", ""]
        
        # Create time buckets
        nodes = list(self.helix.helix)
        if not nodes:
            return "[No nodes in helix]"
        
        min_pos = min(n.position for n in nodes)
        max_pos = max(n.position for n in nodes)
        
        # Create 20 time buckets
        bucket_size = (max_pos - min_pos + 0.1) / 20
        buckets_a = [0] * 20
        buckets_b = [0] * 20
        
        # Count activity in each bucket
        for node in nodes:
            bucket_idx = min(19, int((node.position - min_pos) / bucket_size))
            buckets_a[bucket_idx] += len(node.strand_a_data)
            buckets_b[bucket_idx] += len(node.strand_b_data)
        
        # Normalize and create visualization
        max_activity = max(max(buckets_a), max(buckets_b), 1)
        
        # Create the visualization
        lines.append("     A: Recursive/Emotion  B: Symbolic/Schema")
        lines.append("     " + "─" * 41)
        
        for i in range(5, -1, -1):  # 6 levels
            line = f"{i*20:3d}% │"
            for j in range(20):
                a_height = (buckets_a[j] / max_activity) * 5
                b_height = (buckets_b[j] / max_activity) * 5
                
                if a_height >= i:
                    if b_height >= i:
                        line += "◆"  # Both strands
                    else:
                        line += "▲"  # Just A
                elif b_height >= i:
                    line += "▼"  # Just B
                else:
                    line += " "
                
                line += " "
            
            lines.append(line)
        
        lines.append("     └" + "─" * 41)
        lines.append("      " + "".join(f"{i:2d}" if i % 5 == 0 else "  " for i in range(20)))
        lines.append("                    Time →")
        
        return "\n".join(lines)
    
    def sync_checkpoint(self) -> Dict[str, Any]:
        """Create synchronization checkpoint for current state"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'position': self.helix.current_position,
            'coherence': self.helix.monitor_strand_tension()['coherence'],
            'event_count': len(self.helix.epoch_logs),
            'bloom_id': self.helix.current_bloom_id,
            'sigil_count': len(self.helix.sigil_ring.ring)
        }
        
        self.coherence_checkpoints.append(checkpoint)
        return checkpoint


# Interactive epoch monitor
def run_epoch_monitor():
    """Run interactive epoch monitoring session"""
    print("╔════════════════════════════════════════╗")
    print("║     DAWN EPOCH SYNCHRONIZATION         ║")
    print("║         epoch_0525_0601                ║")
    print("╚════════════════════════════════════════╝")
    
    # Initialize systems
    helix = DAWNHelixInterface()
    monitor = EpochSyncMonitor(helix)
    
    # Simulate some epoch events for demonstration
    print("\n[SYNC] Loading epoch events...")
    
    events = [
        ("schema_mutation", StrandType.A_RECURSIVE_EMOTION, 
         {"emotional_intensity": 0.7, "memory_trace": "cascade_alpha"}),
        ("sigil_activation", StrandType.B_SYMBOLIC_SCHEMA,
         {"command": "pattern_lock", "urgency": 0.5}),
        ("drift_cascade", StrandType.A_RECURSIVE_EMOTION,
         {"emotional_intensity": 0.9, "vector_count": 12}),
        ("bloom_trigger", StrandType.A_RECURSIVE_EMOTION,
         {"cascade_depth": 3, "emotional_intensity": 0.8}),
        ("schema_mutation", StrandType.B_SYMBOLIC_SCHEMA,
         {"urgency": 0.7, "mutation_type": "recursive_fold"}),
    ]
    
    for event_type, strand, data in events:
        helix.port_operator_log(event_type, strand, data, "operator_system")
        helix.advance_helix(0.2)
    
    # Display initial report
    print("\n" + monitor.generate_epoch_report())
    
    # Show strand activity
    print("\n" + monitor.visualize_strand_activity())
    
    # Create checkpoint
    checkpoint = monitor.sync_checkpoint()
    print(f"\n[CHECKPOINT] Saved at position {checkpoint['position']:.3f}")
    print(f"             Coherence: {checkpoint['coherence']:.3f}")
    
    return helix, monitor


if __name__ == "__main__":
    helix_interface, epoch_monitor = run_epoch_monitor()
    
    print("\n[READY] Epoch sync complete. Helix interface active.")
    print("        Type 'helix_interface' or 'epoch_monitor' to access systems.")