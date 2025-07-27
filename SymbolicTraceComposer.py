#!/usr/bin/env python3
"""
DAWN Symbolic Trace Composer - Semantic Replay Archive System
=============================================================

Snapshot generator that composes all relevant cognitive logs into a single
semantic replay bundle. Creates DAWN's "semantic black box" for postmortems,
demos, and introspective rewinds.

Features:
- Comprehensive log aggregation from all cognitive systems
- Timestamped semantic snapshots
- Optional compression and archiving
- Tick-specific or time-range snapshots
- Replay-ready JSON format
- Integration with all DAWN cognitive systems
"""

import json
import time
import zipfile
import argparse
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class CognitiveSnapshot:
    """Complete cognitive state snapshot"""
    tick_id: int
    timestamp: float
    datetime_iso: str
    entropy: float
    mood: str
    coherence: float
    heat: float
    complexity: float
    memory_activity: float
    forecast_reliability: float
    
    # Component data
    reflections: List[Dict[str, Any]]
    rebloom_lineage: List[Dict[str, Any]]
    symbolic_roots: List[Dict[str, Any]]
    tracer_alerts: List[Dict[str, Any]]
    spoken_events: List[Dict[str, Any]]
    voice_modulations: List[Dict[str, Any]]
    mycelium_graph: Optional[Dict[str, Any]]
    
    # Metadata
    snapshot_source: str
    component_status: Dict[str, bool]
    log_file_sizes: Dict[str, int]

class SymbolicTraceComposer:
    """
    Composes comprehensive cognitive state snapshots from all DAWN systems.
    Creates semantic replay archives for analysis and demonstration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the symbolic trace composer"""
        self.config = config or {}
        
        # Base paths
        self.runtime_logs = Path("runtime/logs")
        self.runtime_memory = Path("runtime/memory")
        self.runtime_snapshots = Path("runtime/snapshots")
        
        # Ensure snapshot directory exists
        self.runtime_snapshots.mkdir(parents=True, exist_ok=True)
        
        # Log file paths
        self.log_files = {
            'reflection': self.runtime_logs / "reflection.log",
            'event_stream': self.runtime_logs / "event_stream.log",
            'tracer_alerts': self.runtime_logs / "tracer_alerts.log",
            'root_trace': self.runtime_logs / "root_trace.log",
            'spoken_trace': self.runtime_logs / "spoken_trace.log",
            'voice_modulation': self.runtime_logs / "voice_modulation.log",
            'rebloom_lineage': self.runtime_memory / "lineage_log.jsonl",
            'mycelium_graph': self.runtime_memory / "mycelium_graph.json"
        }
        
        print("📦 Symbolic Trace Composer initialized")
    
    def create_snapshot(self, tick_id: Optional[int] = None, 
                       time_range: Optional[Tuple[float, float]] = None,
                       include_voice: bool = True,
                       compress: bool = False) -> str:
        """
        Create a comprehensive cognitive snapshot.
        
        Args:
            tick_id: Specific tick to snapshot (if None, uses latest)
            time_range: Time range tuple (start, end) in Unix timestamps
            include_voice: Whether to include voice/TTS data
            compress: Whether to create a compressed archive
            
        Returns:
            str: Path to created snapshot file
        """
        print(f"📦 Creating cognitive snapshot...")
        
        # Determine snapshot parameters
        if tick_id is None:
            tick_id = self._get_latest_tick()
        
        if time_range is None:
            # Default to last hour or around target tick
            end_time = time.time()
            start_time = end_time - 3600  # 1 hour
            time_range = (start_time, end_time)
        
        print(f"   Target tick: {tick_id}")
        print(f"   Time range: {datetime.fromtimestamp(time_range[0])} to {datetime.fromtimestamp(time_range[1])}")
        
        # Collect data from all sources
        snapshot_data = self._collect_comprehensive_data(tick_id, time_range, include_voice)
        
        # Create snapshot object
        snapshot = self._build_snapshot_object(snapshot_data, tick_id)
        
        # Generate filename
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"semantic_trace_{tick_id}_{timestamp_str}.json"
        snapshot_path = self.runtime_snapshots / filename
        
        # Write snapshot
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(snapshot), f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Snapshot written: {snapshot_path}")
        
        # Create compressed archive if requested
        if compress:
            archive_path = self._create_compressed_archive(snapshot_path, snapshot_data)
            print(f"   📦 Archive created: {archive_path}")
            return str(archive_path)
        
        return str(snapshot_path)
    
    def _get_latest_tick(self) -> int:
        """Get the latest tick ID from available logs"""
        latest_tick = 0
        
        # Check event stream for latest tick
        if self.log_files['event_stream'].exists():
            try:
                with open(self.log_files['event_stream'], 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                entry = json.loads(line.strip())
                                tick_id = entry.get('tick_id', 0)
                                if tick_id > latest_tick:
                                    latest_tick = tick_id
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                print(f"⚠️ Error reading event stream: {e}")
        
        # Check tracer alerts for latest tick
        if self.log_files['tracer_alerts'].exists():
            try:
                with open(self.log_files['tracer_alerts'], 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                entry = json.loads(line.strip())
                                tick_id = entry.get('tick_id', 0)
                                if tick_id > latest_tick:
                                    latest_tick = tick_id
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                print(f"⚠️ Error reading tracer alerts: {e}")
        
        return max(latest_tick, int(time.time()) % 100000)  # Fallback to time-based tick
    
    def _collect_comprehensive_data(self, tick_id: int, time_range: Tuple[float, float], 
                                   include_voice: bool) -> Dict[str, Any]:
        """Collect data from all cognitive log sources"""
        start_time, end_time = time_range
        data = {}
        
        print(f"   📂 Collecting comprehensive cognitive data...")
        
        # Collect reflections
        data['reflections'] = self._collect_reflections(start_time, end_time)
        print(f"      Reflections: {len(data['reflections'])}")
        
        # Collect event stream
        data['event_stream'] = self._collect_event_stream(tick_id, start_time, end_time)
        print(f"      Event stream: {len(data['event_stream'])}")
        
        # Collect tracer alerts
        data['tracer_alerts'] = self._collect_tracer_alerts(tick_id, start_time, end_time)
        print(f"      Tracer alerts: {len(data['tracer_alerts'])}")
        
        # Collect symbolic roots
        data['symbolic_roots'] = self._collect_symbolic_roots(tick_id, start_time, end_time)
        print(f"      Symbolic roots: {len(data['symbolic_roots'])}")
        
        # Collect rebloom lineage
        data['rebloom_lineage'] = self._collect_rebloom_lineage(start_time, end_time)
        print(f"      Rebloom lineage: {len(data['rebloom_lineage'])}")
        
        # Collect voice data if requested
        if include_voice:
            data['spoken_events'] = self._collect_spoken_events(start_time, end_time)
            data['voice_modulations'] = self._collect_voice_modulations(start_time, end_time)
            print(f"      Voice events: {len(data['spoken_events'])}")
            print(f"      Voice modulations: {len(data['voice_modulations'])}")
        else:
            data['spoken_events'] = []
            data['voice_modulations'] = []
        
        # Collect mycelium graph
        data['mycelium_graph'] = self._collect_mycelium_graph()
        print(f"      Mycelium graph: {'Present' if data['mycelium_graph'] else 'None'}")
        
        # Collect component status
        data['component_status'] = self._get_component_status()
        data['log_file_sizes'] = self._get_log_file_sizes()
        
        return data
    
    def _collect_reflections(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect reflection log entries"""
        reflections = []
        
        if not self.log_files['reflection'].exists():
            return reflections
        
        try:
            with open(self.log_files['reflection'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        # Parse reflection entries (may be various formats)
                        reflection_entry = {
                            'timestamp': time.time(),
                            'content': line.strip(),
                            'source': 'reflection_log'
                        }
                        
                        # Try to extract timestamp if present
                        if 'REFLECTION:' in line:
                            parts = line.split('REFLECTION:', 1)
                            if len(parts) > 1:
                                reflection_entry['content'] = parts[1].strip()
                        
                        reflections.append(reflection_entry)
        except Exception as e:
            print(f"⚠️ Error collecting reflections: {e}")
        
        return reflections
    
    def _collect_event_stream(self, tick_id: int, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect event stream entries"""
        events = []
        
        if not self.log_files['event_stream'].exists():
            return events
        
        try:
            with open(self.log_files['event_stream'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            entry_time = entry.get('timestamp', 0)
                            entry_tick = entry.get('tick_id', 0)
                            
                            # Include if in time range or matches tick
                            if (start_time <= entry_time <= end_time) or (entry_tick == tick_id):
                                events.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error collecting event stream: {e}")
        
        return events
    
    def _collect_tracer_alerts(self, tick_id: int, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect tracer alert entries"""
        alerts = []
        
        if not self.log_files['tracer_alerts'].exists():
            return alerts
        
        try:
            with open(self.log_files['tracer_alerts'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            entry_time = entry.get('timestamp', 0)
                            entry_tick = entry.get('tick_id', 0)
                            
                            if (start_time <= entry_time <= end_time) or (entry_tick == tick_id):
                                alerts.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error collecting tracer alerts: {e}")
        
        return alerts
    
    def _collect_symbolic_roots(self, tick_id: int, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect symbolic root events"""
        roots = []
        
        if not self.log_files['root_trace'].exists():
            return roots
        
        try:
            with open(self.log_files['root_trace'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            entry_time = entry.get('timestamp', 0)
                            entry_tick = entry.get('tick', 0)
                            
                            if (start_time <= entry_time <= end_time) or (entry_tick == tick_id):
                                roots.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error collecting symbolic roots: {e}")
        
        return roots
    
    def _collect_rebloom_lineage(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect rebloom lineage entries"""
        lineage = []
        
        if not self.log_files['rebloom_lineage'].exists():
            return lineage
        
        try:
            with open(self.log_files['rebloom_lineage'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            entry_time = entry.get('timestamp', 0)
                            
                            if start_time <= entry_time <= end_time:
                                lineage.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error collecting rebloom lineage: {e}")
        
        return lineage
    
    def _collect_spoken_events(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect spoken event entries"""
        spoken = []
        
        if not self.log_files['spoken_trace'].exists():
            return spoken
        
        try:
            with open(self.log_files['spoken_trace'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            entry_time = entry.get('timestamp', 0)
                            
                            if start_time <= entry_time <= end_time:
                                spoken.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error collecting spoken events: {e}")
        
        return spoken
    
    def _collect_voice_modulations(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Collect voice modulation entries"""
        modulations = []
        
        if not self.log_files['voice_modulation'].exists():
            return modulations
        
        try:
            with open(self.log_files['voice_modulation'], 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            entry_time = entry.get('timestamp', 0)
                            
                            if start_time <= entry_time <= end_time:
                                modulations.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error collecting voice modulations: {e}")
        
        return modulations
    
    def _collect_mycelium_graph(self) -> Optional[Dict[str, Any]]:
        """Collect current mycelium graph"""
        if not self.log_files['mycelium_graph'].exists():
            return None
        
        try:
            with open(self.log_files['mycelium_graph'], 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error collecting mycelium graph: {e}")
            return None
    
    def _get_component_status(self) -> Dict[str, bool]:
        """Get status of all cognitive components"""
        return {
            'reflection_log': self.log_files['reflection'].exists(),
            'event_stream': self.log_files['event_stream'].exists(),
            'tracer_alerts': self.log_files['tracer_alerts'].exists(),
            'root_trace': self.log_files['root_trace'].exists(),
            'spoken_trace': self.log_files['spoken_trace'].exists(),
            'voice_modulation': self.log_files['voice_modulation'].exists(),
            'rebloom_lineage': self.log_files['rebloom_lineage'].exists(),
            'mycelium_graph': self.log_files['mycelium_graph'].exists()
        }
    
    def _get_log_file_sizes(self) -> Dict[str, int]:
        """Get sizes of all log files"""
        sizes = {}
        for name, path in self.log_files.items():
            if path.exists():
                sizes[name] = path.stat().st_size
            else:
                sizes[name] = 0
        return sizes
    
    def _build_snapshot_object(self, data: Dict[str, Any], tick_id: int) -> CognitiveSnapshot:
        """Build the complete snapshot object"""
        # Extract state information from latest event
        latest_state = self._extract_latest_state(data['event_stream'])
        
        return CognitiveSnapshot(
            tick_id=tick_id,
            timestamp=time.time(),
            datetime_iso=datetime.now().isoformat(),
            entropy=latest_state.get('entropy', 0.5),
            mood=latest_state.get('mood', 'NEUTRAL'),
            coherence=latest_state.get('coherence', 0.8),
            heat=latest_state.get('heat', 0.3),
            complexity=latest_state.get('complexity', 0.5),
            memory_activity=latest_state.get('memory_activity', 0.0),
            forecast_reliability=latest_state.get('forecast_reliability', 0.7),
            reflections=data['reflections'],
            rebloom_lineage=data['rebloom_lineage'],
            symbolic_roots=data['symbolic_roots'],
            tracer_alerts=data['tracer_alerts'],
            spoken_events=data['spoken_events'],
            voice_modulations=data['voice_modulations'],
            mycelium_graph=data['mycelium_graph'],
            snapshot_source="SymbolicTraceComposer",
            component_status=data['component_status'],
            log_file_sizes=data['log_file_sizes']
        )
    
    def _extract_latest_state(self, event_stream: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract latest cognitive state from event stream"""
        if not event_stream:
            return {}
        
        # Find the most recent event with state information
        latest_event = max(event_stream, key=lambda x: x.get('timestamp', 0))
        
        # Try to extract state from various event types
        if 'runtime_state' in latest_event:
            return latest_event['runtime_state']
        
        # Build state from available data
        state = {}
        for event in reversed(event_stream[-10:]):  # Check last 10 events
            if 'entropy' in event and 'entropy' not in state:
                state['entropy'] = event['entropy']
            if 'heat' in event and 'heat' not in state:
                state['heat'] = event['heat']
            if 'coherence' in event and 'coherence' not in state:
                state['coherence'] = event['coherence']
        
        return state
    
    def _create_compressed_archive(self, snapshot_path: Path, data: Dict[str, Any]) -> str:
        """Create compressed archive with snapshot and log files"""
        archive_name = snapshot_path.stem + ".zip"
        archive_path = self.runtime_snapshots / archive_name
        
        print(f"   📦 Creating compressed archive...")
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add the main snapshot file
            zf.write(snapshot_path, snapshot_path.name)
            
            # Add relevant log files
            for name, path in self.log_files.items():
                if path.exists() and path.stat().st_size > 0:
                    # Add with a folder structure
                    arcname = f"logs/{name}{path.suffix}"
                    zf.write(path, arcname)
        
        return str(archive_path)
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available snapshots"""
        snapshots = []
        
        for snapshot_file in self.runtime_snapshots.glob("semantic_trace_*.json"):
            try:
                stat = snapshot_file.stat()
                snapshots.append({
                    'filename': snapshot_file.name,
                    'path': str(snapshot_file),
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception as e:
                print(f"⚠️ Error reading snapshot {snapshot_file}: {e}")
        
        # Sort by creation time, newest first
        snapshots.sort(key=lambda x: x['created'], reverse=True)
        return snapshots
    
    def load_snapshot(self, snapshot_path: str) -> Optional[CognitiveSnapshot]:
        """Load a snapshot from file"""
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Reconstruct snapshot object
            return CognitiveSnapshot(**data)
            
        except Exception as e:
            print(f"❌ Error loading snapshot {snapshot_path}: {e}")
            return None

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Create DAWN cognitive snapshots")
    parser.add_argument("--tick", type=int, help="Specific tick to snapshot")
    parser.add_argument("--hours", type=float, default=1.0, help="Hours of history to include")
    parser.add_argument("--no-voice", action="store_true", help="Exclude voice data")
    parser.add_argument("--compress", action="store_true", help="Create compressed archive")
    parser.add_argument("--list", action="store_true", help="List existing snapshots")
    
    args = parser.parse_args()
    
    composer = SymbolicTraceComposer()
    
    if args.list:
        snapshots = composer.list_snapshots()
        print(f"\n📦 Available Snapshots ({len(snapshots)}):")
        print("-" * 60)
        
        for snapshot in snapshots:
            size_mb = snapshot['size'] / (1024 * 1024)
            print(f"📄 {snapshot['filename']}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"   Created: {snapshot['created']}")
            print()
        
        return
    
    # Create snapshot
    time_range = (time.time() - (args.hours * 3600), time.time())
    
    snapshot_path = composer.create_snapshot(
        tick_id=args.tick,
        time_range=time_range,
        include_voice=not args.no_voice,
        compress=args.compress
    )
    
    print(f"\n✅ Cognitive snapshot created: {snapshot_path}")
    
    # Show snapshot info
    if snapshot_path.endswith('.json'):
        snapshot = composer.load_snapshot(snapshot_path)
        if snapshot:
            print(f"\n📊 Snapshot Summary:")
            print(f"   Tick: {snapshot.tick_id}")
            print(f"   Entropy: {snapshot.entropy:.3f}")
            print(f"   Mood: {snapshot.mood}")
            print(f"   Reflections: {len(snapshot.reflections)}")
            print(f"   Tracer Alerts: {len(snapshot.tracer_alerts)}")
            print(f"   Symbolic Roots: {len(snapshot.symbolic_roots)}")
            print(f"   Voice Events: {len(snapshot.spoken_events)}")

if __name__ == "__main__":
    main() 