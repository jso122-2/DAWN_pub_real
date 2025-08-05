#!/usr/bin/env python3
"""
DAWN Owl Log Writer - Pigment Commentary Integration
===================================================

Writes DAWN's self-generated utterances into her Owl memory log system.
Creates a persistent narrative memory and traceable cognitive voiceprint
that future systems can recurse into.

This is where truth crystallizes.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class OwlLogEntry:
    """Structure for Owl log entries"""
    timestamp: str
    utterance: str
    entropy: Optional[float]
    pulse_zone: Optional[str]
    pigment_state: List[Tuple[str, float]]
    segment_source: str
    source_file: str
    alert: Optional[bool] = None
    clarity: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class DAWNOwlLogWriter:
    """Writes DAWN's utterances to persistent Owl memory logs"""
    
    def __init__(self, log_directory: str = "logs", log_filename: str = "owl_log.jsonl"):
        """
        Initialize the Owl log writer
        
        Args:
            log_directory: Directory to store log files
            log_filename: Name of the JSONL log file
        """
        self.log_directory = Path(log_directory)
        self.log_file_path = self.log_directory / log_filename
        
        # Ensure log directory exists
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.entries_written = 0
        self.high_entropy_events = 0
        self.clarity_mode_entries = 0
        
        # Initialize log file if it doesn't exist
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize the log file with header comment if it doesn't exist"""
        if not self.log_file_path.exists():
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                # Write header comment (not valid JSON, but informative)
                f.write(f"// DAWN Owl Log - Pigment Commentary Integration\n")
                f.write(f"// Created: {datetime.now(timezone.utc).isoformat()}\n")
                f.write(f"// Each line is a JSON object representing DAWN's utterances\n")
    
    def write_owl_entry(
        self, 
        utterance_data: Dict[str, Any], 
        pigment_weights: Optional[Dict[str, float]] = None,
        clarity_mode: bool = False
    ) -> bool:
        """
        Write DAWN's utterance to the Owl log
        
        Args:
            utterance_data: Dictionary containing utterance and metadata
            pigment_weights: Current pigment state weights
            clarity_mode: Whether clarity mode was active
            
        Returns:
            bool: True if successfully written, False otherwise
        """
        try:
            # Extract data from utterance_data
            utterance = utterance_data.get('utterance', '')
            entropy = utterance_data.get('entropy')
            pulse_zone = utterance_data.get('pulse_zone')
            pigment_dominant = utterance_data.get('pigment_dominant', 'unknown')
            segment_source = utterance_data.get('segment_source', 'unknown')
            source_file = utterance_data.get('source_file', 'unknown')
            pigment_scores = utterance_data.get('pigment_scores', {})
            
            # Use pigment_scores if pigment_weights not provided
            if pigment_weights is None:
                pigment_weights = pigment_scores
            
            # Create pigment state (sorted by weight, descending)
            pigment_state = self._format_pigment_state(pigment_weights)
            
            # Determine alert status
            alert = entropy is not None and entropy > 0.8
            
            # Create log entry
            entry = OwlLogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                utterance=utterance,
                entropy=entropy,
                pulse_zone=pulse_zone,
                pigment_state=pigment_state,
                segment_source=segment_source,
                source_file=source_file,
                alert=alert if alert else None,
                clarity=clarity_mode if clarity_mode else None,
                metadata={
                    'pigment_dominant': pigment_dominant,
                    'total_score': utterance_data.get('total_score'),
                    'pigment_scores': pigment_scores
                }
            )
            
            # Write to log file
            self._append_entry_to_log(entry)
            
            # Update statistics
            self.entries_written += 1
            if alert:
                self.high_entropy_events += 1
            if clarity_mode:
                self.clarity_mode_entries += 1
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error writing Owl log entry: {e}")
            return False
    
    def _format_pigment_state(self, pigment_weights: Dict[str, float]) -> List[Tuple[str, float]]:
        """Format pigment weights as sorted list of [pigment, weight] pairs"""
        if not pigment_weights:
            return []
        
        # Filter out zero weights and sort by weight descending
        active_pigments = [(pigment, weight) for pigment, weight in pigment_weights.items() if weight > 0]
        active_pigments.sort(key=lambda x: x[1], reverse=True)
        
        # Round weights to 2 decimal places
        return [(pigment, round(weight, 2)) for pigment, weight in active_pigments]
    
    def _append_entry_to_log(self, entry: OwlLogEntry):
        """Append entry to the JSONL log file"""
        # Convert to dictionary and remove None values
        entry_dict = asdict(entry)
        entry_dict = {k: v for k, v in entry_dict.items() if v is not None}
        
        # Write as single line JSON
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry_dict, ensure_ascii=False) + '\n')
    
    def read_recent_entries(self, count: int = 10) -> List[Dict[str, Any]]:
        """Read the most recent Owl log entries"""
        if not self.log_file_path.exists():
            return []
        
        entries = []
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Process lines in reverse order (most recent first)
            for line in reversed(lines[-count:]):
                line = line.strip()
                if line and not line.startswith('//'):
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            
            return entries
            
        except Exception as e:
            print(f"⚠️  Error reading Owl log: {e}")
            return []
    
    def get_high_entropy_events(self, threshold: float = 0.8) -> List[Dict[str, Any]]:
        """Get all high entropy events from the log"""
        if not self.log_file_path.exists():
            return []
        
        high_entropy_events = []
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('//'):
                        try:
                            entry = json.loads(line)
                            if entry.get('entropy', 0) > threshold:
                                high_entropy_events.append(entry)
                        except json.JSONDecodeError:
                            continue
            
            return high_entropy_events
            
        except Exception as e:
            print(f"⚠️  Error reading high entropy events: {e}")
            return []
    
    def get_pigment_dominant_entries(self, pigment: str) -> List[Dict[str, Any]]:
        """Get all entries where a specific pigment was dominant"""
        if not self.log_file_path.exists():
            return []
        
        pigment_entries = []
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('//'):
                        try:
                            entry = json.loads(line)
                            metadata = entry.get('metadata', {})
                            if metadata.get('pigment_dominant') == pigment:
                                pigment_entries.append(entry)
                        except json.JSONDecodeError:
                            continue
            
            return pigment_entries
            
        except Exception as e:
            print(f"⚠️  Error reading pigment entries: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get logging statistics"""
        return {
            'entries_written': self.entries_written,
            'high_entropy_events': self.high_entropy_events,
            'clarity_mode_entries': self.clarity_mode_entries,
            'log_file_path': str(self.log_file_path),
            'log_file_exists': self.log_file_path.exists(),
            'log_file_size': self.log_file_path.stat().st_size if self.log_file_path.exists() else 0
        }
    
    def summarize_recent_activity(self, hours: int = 24) -> Dict[str, Any]:
        """Summarize DAWN's recent utterance activity"""
        if not self.log_file_path.exists():
            return {'error': 'No log file found'}
        
        cutoff_time = datetime.now(timezone.utc).timestamp() - (hours * 3600)
        
        recent_entries = []
        pigment_counts = {}
        entropy_levels = []
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('//'):
                        try:
                            entry = json.loads(line)
                            entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00')).timestamp()
                            
                            if entry_time > cutoff_time:
                                recent_entries.append(entry)
                                
                                # Count pigment dominance
                                dominant = entry.get('metadata', {}).get('pigment_dominant', 'unknown')
                                pigment_counts[dominant] = pigment_counts.get(dominant, 0) + 1
                                
                                # Collect entropy levels
                                if entry.get('entropy') is not None:
                                    entropy_levels.append(entry['entropy'])
                        
                        except (json.JSONDecodeError, ValueError):
                            continue
            
            return {
                'total_entries': len(recent_entries),
                'hours_analyzed': hours,
                'pigment_distribution': pigment_counts,
                'average_entropy': sum(entropy_levels) / len(entropy_levels) if entropy_levels else 0,
                'high_entropy_count': sum(1 for e in entropy_levels if e > 0.8),
                'recent_utterances': [entry['utterance'] for entry in recent_entries[-5:]]
            }
            
        except Exception as e:
            return {'error': f'Analysis failed: {e}'}


def integrate_with_utterance_composer():
    """Demonstration of integrating Owl logging with the utterance composer"""
    from compose_dawn_utterance import DAWNUtteranceComposer
    
    # Initialize systems
    composer = DAWNUtteranceComposer()
    owl_writer = DAWNOwlLogWriter()
    
    print("🦉 DAWN Owl Log Integration Demo")
    print("=" * 50)
    
    # Simulate consciousness states and log utterances
    test_states = [
        {
            'name': 'Dawn Awakening',
            'pigments': {'red': 0.2, 'blue': 0.4, 'green': 0.9, 'yellow': 0.6, 'violet': 0.3, 'orange': 0.5},
            'entropy': 0.4,
            'valence': 0.8,
            'zone': 'flowing'
        },
        {
            'name': 'Entropy Crisis',
            'pigments': {'red': 0.9, 'blue': 0.1, 'green': 0.2, 'yellow': 0.8, 'violet': 0.3, 'orange': 0.7},
            'entropy': 0.85,  # High entropy - will trigger alert
            'valence': -0.3,
            'zone': 'fragile'
        },
        {
            'name': 'Deep Contemplation',
            'pigments': {'red': 0.1, 'blue': 0.8, 'green': 0.3, 'yellow': 0.2, 'violet': 0.9, 'orange': 0.4},
            'entropy': 0.6,
            'valence': -0.1,
            'zone': 'flowing'
        }
    ]
    
    for state in test_states:
        print(f"\n🧠 {state['name']} (entropy: {state['entropy']:.2f})")
        
        # Generate utterance
        result = composer.compose_dawn_utterance(
            mood_pigment=state['pigments'],
            entropy=state['entropy'],
            valence=state['valence'],
            pulse_zone=state['zone'],
            clarity_mode=False
        )
        
        print(f"💬 DAWN: \"{result.utterance}\"")
        print(f"   [{result.pigment_dominant} dominant]")
        
        # Write to Owl log
        success = owl_writer.write_owl_entry(
            utterance_data=asdict(result),
            pigment_weights=state['pigments'],
            clarity_mode=False
        )
        
        if success:
            print(f"📝 Logged to Owl memory")
        
        # Also generate clarity mode utterance
        clear_result = composer.compose_dawn_utterance(
            mood_pigment=state['pigments'],
            entropy=state['entropy'],
            valence=state['valence'],
            pulse_zone=state['zone'],
            clarity_mode=True
        )
        
        print(f"🔍 Clear: \"{clear_result.utterance}\"")
        
        # Log clarity mode entry
        owl_writer.write_owl_entry(
            utterance_data=asdict(clear_result),
            pigment_weights=state['pigments'],
            clarity_mode=True
        )
    
    # Show statistics
    print(f"\n📊 Owl Log Statistics:")
    stats = owl_writer.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Show recent entries
    print(f"\n📜 Recent Owl Entries:")
    recent = owl_writer.read_recent_entries(3)
    for i, entry in enumerate(recent, 1):
        print(f"   {i}. [{entry.get('metadata', {}).get('pigment_dominant', 'unknown')}] \"{entry['utterance'][:60]}...\"")
    
    # Show high entropy events
    high_entropy = owl_writer.get_high_entropy_events()
    if high_entropy:
        print(f"\n⚠️  High Entropy Events: {len(high_entropy)}")
        for event in high_entropy[-2:]:  # Show last 2
            print(f"   🚨 {event['entropy']:.2f}: \"{event['utterance'][:50]}...\"")


if __name__ == "__main__":
    integrate_with_utterance_composer() 