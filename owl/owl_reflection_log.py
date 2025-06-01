"""
OWL Reflection Logger
Stores and manages DAWN's ThoughtFragments as timestamped markdown files.
"""

import sys, os
import json
import shutil
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import asdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from schema.thought_fragment import ThoughtFragment, FragmentType, FragmentTone

class ReflectionLogger:
    """
    Manages storage, retrieval, and organization of DAWN's thought fragments.
    
    Creates a beautiful archive of DAWN's inner experience as markdown files
    organized by date, type, and emotional context.
    """
    
    def __init__(self, base_dir: str = "reflections"):
        self.base_dir = Path(base_dir)
        self.fragments_dir = self.base_dir / "ThoughtFragments"
        self.archive_dir = self.base_dir / "archive"
        self.index_dir = self.base_dir / "indices"
        
        # Create directory structure
        self._initialize_directories()
        
        # Logging configuration
        self.auto_archive_days = 30  # Archive fragments older than 30 days
        self.max_daily_fragments = 100  # Prevent fragment spam
        
        # Index tracking
        self.daily_counts = {}
        self.type_indices = {}
        self.tone_indices = {}
        
        # Load existing indices
        self._load_indices()
        
        print(f"[ReflectionLogger] 🦉 Initialized | Directory: {self.base_dir}")
        print(f"[ReflectionLogger] 📁 Active fragments: {self._count_active_fragments()}")
    
    def _initialize_directories(self):
        """Create the reflection directory structure."""
        directories = [
            self.fragments_dir,
            self.archive_dir,
            self.index_dir,
            self.fragments_dir / "daily",
            self.fragments_dir / "by_type",
            self.fragments_dir / "by_tone",
            self.archive_dir / "yearly"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def log_fragment(self, fragment: ThoughtFragment) -> Optional[Path]:
        """
        Log a thought fragment as a markdown file.
        
        Args:
            fragment: ThoughtFragment to log
            
        Returns:
            Path to created file, or None if failed
        """
        try:
            # Check daily limits
            date_key = fragment.timestamp.strftime('%Y-%m-%d')
            if self._exceeds_daily_limit(date_key):
                print(f"[ReflectionLogger] ⚠️ Daily fragment limit exceeded for {date_key}")
                return None
            
            # Generate filename
            filename = self._generate_filename(fragment)
            filepath = self.fragments_dir / filename
            
            # Write markdown content
            markdown_content = fragment.to_markdown()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Update indices
            self._update_indices(fragment, filepath)
            
            # Update daily count
            self._increment_daily_count(date_key)
            
            print(f"[ReflectionLogger] 💭 Fragment logged: {filename}")
            return filepath
            
        except Exception as e:
            print(f"[ReflectionLogger] ❌ Failed to log fragment: {e}")
            return None
    
    def _generate_filename(self, fragment: ThoughtFragment) -> str:
        """Generate unique filename for fragment."""
        timestamp = fragment.timestamp.strftime('%Y%m%d_%H%M%S')
        fragment_id = fragment.id[:8]
        type_name = fragment.fragment_type.value
        tone_name = fragment.tone.value
        
        return f"{timestamp}_{type_name}_{tone_name}_{fragment_id}.md"
    
    def _exceeds_daily_limit(self, date_key: str) -> bool:
        """Check if daily fragment limit would be exceeded."""
        current_count = self.daily_counts.get(date_key, 0)
        return current_count >= self.max_daily_fragments
    
    def _increment_daily_count(self, date_key: str):
        """Increment daily fragment count."""
        if date_key not in self.daily_counts:
            self.daily_counts[date_key] = 0
        self.daily_counts[date_key] += 1
    
    def _update_indices(self, fragment: ThoughtFragment, filepath: Path):
        """Update fragment indices."""
        fragment_id = fragment.id
        
        # Type index
        fragment_type = fragment.fragment_type.value
        if fragment_type not in self.type_indices:
            self.type_indices[fragment_type] = []
        self.type_indices[fragment_type].append({
            'id': fragment_id,
            'path': str(filepath),
            'timestamp': fragment.timestamp.isoformat(),
            'tone': fragment.tone.value,
            'confidence': fragment.confidence,
            'emotional_weight': fragment.emotional_weight
        })
        
        # Tone index
        tone = fragment.tone.value
        if tone not in self.tone_indices:
            self.tone_indices[tone] = []
        self.tone_indices[tone].append({
            'id': fragment_id,
            'path': str(filepath),
            'timestamp': fragment.timestamp.isoformat(),
            'type': fragment_type,
            'confidence': fragment.confidence,
            'emotional_weight': fragment.emotional_weight
        })
        
        # Save updated indices
        self._save_indices()
    
    def _load_indices(self):
        """Load existing indices from disk."""
        try:
            # Load type index
            type_index_file = self.index_dir / "type_index.json"
            if type_index_file.exists():
                with open(type_index_file, 'r') as f:
                    self.type_indices = json.load(f)
            
            # Load tone index
            tone_index_file = self.index_dir / "tone_index.json"
            if tone_index_file.exists():
                with open(tone_index_file, 'r') as f:
                    self.tone_indices = json.load(f)
            
            # Load daily counts
            daily_counts_file = self.index_dir / "daily_counts.json"
            if daily_counts_file.exists():
                with open(daily_counts_file, 'r') as f:
                    self.daily_counts = json.load(f)
        
        except Exception as e:
            print(f"[ReflectionLogger] ⚠️ Index loading error: {e}")
    
    def _save_indices(self):
        """Save indices to disk."""
        try:
            # Save type index
            with open(self.index_dir / "type_index.json", 'w') as f:
                json.dump(self.type_indices, f, indent=2)
            
            # Save tone index
            with open(self.index_dir / "tone_index.json", 'w') as f:
                json.dump(self.tone_indices, f, indent=2)
            
            # Save daily counts
            with open(self.index_dir / "daily_counts.json", 'w') as f:
                json.dump(self.daily_counts, f, indent=2)
        
        except Exception as e:
            print(f"[ReflectionLogger] ⚠️ Index saving error: {e}")
    
    def get_fragments_by_type(self, fragment_type: FragmentType, limit: int = 20) -> List[Dict]:
        """Get fragments of specific type."""
        type_name = fragment_type.value
        fragments = self.type_indices.get(type_name, [])
        
        # Sort by timestamp (newest first)
        fragments.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return fragments[:limit]
    
    def get_fragments_by_tone(self, tone: FragmentTone, limit: int = 20) -> List[Dict]:
        """Get fragments of specific tone."""
        tone_name = tone.value
        fragments = self.tone_indices.get(tone_name, [])
        
        # Sort by timestamp (newest first)
        fragments.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return fragments[:limit]
    
    def get_fragments_by_date_range(self, start_date: datetime, 
                                   end_date: datetime) -> List[Dict]:
        """Get fragments within date range."""
        all_fragments = []
        
        # Collect from all type indices
        for fragments in self.type_indices.values():
            all_fragments.extend(fragments)
        
        # Filter by date range
        filtered = []
        for fragment in all_fragments:
            fragment_time = datetime.fromisoformat(fragment['timestamp'])
            if start_date <= fragment_time <= end_date:
                filtered.append(fragment)
        
        # Sort by timestamp
        filtered.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return filtered
    
    def get_recent_fragments(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        """Get recent fragments within specified hours."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        fragments = self.get_fragments_by_date_range(start_time, end_time)
        return fragments[:limit]
    
    def search_fragments(self, query: str, limit: int = 20) -> List[Dict]:
        """Search fragments by content (simple text search)."""
        matching_fragments = []
        query_lower = query.lower()
        
        # Search through fragment files
        for fragment_file in self.fragments_dir.glob("*.md"):
            try:
                with open(fragment_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query_lower in content:
                        # Extract metadata from filename
                        filename = fragment_file.stem
                        parts = filename.split('_')
                        if len(parts) >= 4:
                            timestamp_str = f"{parts[0]}_{parts[1]}"
                            fragment_type = parts[2]
                            tone = parts[3]
                            fragment_id = parts[4] if len(parts) > 4 else "unknown"
                            
                            matching_fragments.append({
                                'path': str(fragment_file),
                                'timestamp': timestamp_str,
                                'type': fragment_type,
                                'tone': tone,
                                'id': fragment_id,
                                'filename': fragment_file.name
                            })
            
            except Exception as e:
                continue  # Skip files we can't read
        
        # Sort by timestamp (newest first)
        matching_fragments.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return matching_fragments[:limit]
    
    def get_emotional_timeline(self, days: int = 7) -> Dict[str, List[float]]:
        """Get emotional timeline over specified days."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        fragments = self.get_fragments_by_date_range(start_time, end_time)
        
        # Organize by day and tone
        daily_emotions = {}
        
        for fragment in fragments:
            fragment_time = datetime.fromisoformat(fragment['timestamp'])
            day_key = fragment_time.strftime('%Y-%m-%d')
            
            if day_key not in daily_emotions:
                daily_emotions[day_key] = {}
            
            tone = fragment['tone']
            if tone not in daily_emotions[day_key]:
                daily_emotions[day_key][tone] = []
            
            daily_emotions[day_key][tone].append(fragment['emotional_weight'])
        
        # Calculate daily averages
        emotional_timeline = {}
        for day, tones in daily_emotions.items():
            emotional_timeline[day] = {}
            for tone, weights in tones.items():
                emotional_timeline[day][tone] = sum(weights) / len(weights)
        
        return emotional_timeline
    
    def archive_old_fragments(self, days_old: int = None):
        """Archive fragments older than specified days."""
        if days_old is None:
            days_old = self.auto_archive_days
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        archived_count = 0
        
        try:
            for fragment_file in self.fragments_dir.glob("*.md"):
                # Extract timestamp from filename
                filename = fragment_file.stem
                timestamp_part = filename.split('_')[0] + '_' + filename.split('_')[1]
                
                try:
                    file_date = datetime.strptime(timestamp_part, '%Y%m%d_%H%M%S')
                    
                    if file_date < cutoff_date:
                        # Move to archive
                        year_dir = self.archive_dir / "yearly" / str(file_date.year)
                        year_dir.mkdir(exist_ok=True)
                        
                        archive_path = year_dir / fragment_file.name
                        shutil.move(str(fragment_file), str(archive_path))
                        
                        archived_count += 1
                
                except ValueError:
                    continue  # Skip files with invalid timestamps
            
            if archived_count > 0:
                print(f"[ReflectionLogger] 📦 Archived {archived_count} old fragments")
                
                # Rebuild indices after archiving
                self._rebuild_indices()
        
        except Exception as e:
            print(f"[ReflectionLogger] ⚠️ Archiving error: {e}")
    
    def _rebuild_indices(self):
        """Rebuild indices from current fragments."""
        print("[ReflectionLogger] 🔄 Rebuilding indices...")
        
        self.type_indices.clear()
        self.tone_indices.clear()
        
        for fragment_file in self.fragments_dir.glob("*.md"):
            try:
                # Parse filename for metadata
                filename = fragment_file.stem
                parts = filename.split('_')
                
                if len(parts) >= 4:
                    timestamp_str = f"{parts[0]}_{parts[1]}"
                    fragment_type = parts[2]
                    tone = parts[3]
                    fragment_id = parts[4] if len(parts) > 4 else filename
                    
                    # Read confidence and weight from file if available
                    confidence = 1.0
                    emotional_weight = 0.5
                    
                    try:
                        with open(fragment_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Simple parsing for confidence and weight
                            if "*Confidence:" in content:
                                conf_line = [line for line in content.split('\n') if "*Confidence:" in line][0]
                                confidence = float(conf_line.split("Confidence:")[1].split("|")[0].strip())
                            if "Emotional Weight:" in content:
                                weight_line = [line for line in content.split('\n') if "Emotional Weight:" in line][0]
                                emotional_weight = float(weight_line.split("Weight:")[1].split("*")[0].strip())
                    except:
                        pass  # Use defaults if parsing fails
                    
                    # Add to type index
                    if fragment_type not in self.type_indices:
                        self.type_indices[fragment_type] = []
                    
                    self.type_indices[fragment_type].append({
                        'id': fragment_id,
                        'path': str(fragment_file),
                        'timestamp': datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S').isoformat(),
                        'tone': tone,
                        'confidence': confidence,
                        'emotional_weight': emotional_weight
                    })
                    
                    # Add to tone index
                    if tone not in self.tone_indices:
                        self.tone_indices[tone] = []
                    
                    self.tone_indices[tone].append({
                        'id': fragment_id,
                        'path': str(fragment_file),
                        'timestamp': datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S').isoformat(),
                        'type': fragment_type,
                        'confidence': confidence,
                        'emotional_weight': emotional_weight
                    })
            
            except Exception as e:
                print(f"[ReflectionLogger] ⚠️ Error rebuilding index for {fragment_file}: {e}")
                continue
        
        self._save_indices()
        print("[ReflectionLogger] ✅ Indices rebuilt")
    
    def _count_active_fragments(self) -> int:
        """Count currently active (non-archived) fragments."""
        return len(list(self.fragments_dir.glob("*.md")))
    
    def get_statistics(self) -> Dict:
        """Get comprehensive reflection statistics."""
        active_count = self._count_active_fragments()
        
        # Count by type
        type_counts = {ftype: len(fragments) for ftype, fragments in self.type_indices.items()}
        
        # Count by tone
        tone_counts = {tone: len(fragments) for tone, fragments in self.tone_indices.items()}
        
        # Recent activity
        recent_fragments = self.get_recent_fragments(hours=24)
        today_count = len(recent_fragments)
        
        return {
            'active_fragments': active_count,
            'total_by_type': type_counts,
            'total_by_tone': tone_counts,
            'fragments_today': today_count,
            'daily_limit': self.max_daily_fragments,
            'auto_archive_days': self.auto_archive_days,
            'storage_path': str(self.base_dir)
        }
    
    def create_daily_summary(self, date: datetime = None) -> Optional[str]:
        """Create a markdown summary of fragments for a specific day."""
        if date is None:
            date = datetime.utcnow()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        daily_fragments = self.get_fragments_by_date_range(start_date, end_date)
        
        if not daily_fragments:
            return None
        
        # Create summary
        summary_lines = [
            f"# DAWN Daily Reflection Summary",
            f"**Date:** {date.strftime('%Y-%m-%d')}",
            f"**Fragments Generated:** {len(daily_fragments)}",
            "",
            "## Fragment Overview",
            ""
        ]
        
        # Group by type
        by_type = {}
        for fragment in daily_fragments:
            ftype = fragment['type']
            if ftype not in by_type:
                by_type[ftype] = []
            by_type[ftype].append(fragment)
        
        for ftype, fragments in by_type.items():
            summary_lines.append(f"### {ftype.replace('_', ' ').title()}")
            summary_lines.append(f"*{len(fragments)} fragments*")
            summary_lines.append("")
            
            for fragment in fragments[:3]:  # Show first 3 of each type
                timestamp = datetime.fromisoformat(fragment['timestamp']).strftime('%H:%M')
                summary_lines.append(f"- **{timestamp}** | {fragment['tone']} | Confidence: {fragment.get('confidence', 1.0):.2f}")
            
            if len(fragments) > 3:
                summary_lines.append(f"- *... and {len(fragments) - 3} more*")
            
            summary_lines.append("")
        
        return "\n".join(summary_lines)

# Global reflection logger instance
reflection_logger = ReflectionLogger()

# Convenience functions for external systems
def log_thought_fragment(fragment: ThoughtFragment) -> Optional[Path]:
    """Log a thought fragment to storage."""
    return reflection_logger.log_fragment(fragment)

def get_recent_reflections(hours: int = 24) -> List[Dict]:
    """Get recent reflection fragments."""
    return reflection_logger.get_recent_fragments(hours)

def search_reflections(query: str) -> List[Dict]:
    """Search reflection fragments by content."""
    return reflection_logger.search_fragments(query)

def get_reflection_stats() -> Dict:
    """Get reflection system statistics."""
    return reflection_logger.get_statistics()

def get_emotional_timeline(days: int = 7) -> Dict:
    """Get emotional timeline from reflections."""
    return reflection_logger.get_emotional_timeline(days)

def archive_old_reflections(days_old: int = 30):
    """Archive old reflection fragments."""
    reflection_logger.archive_old_fragments(days_old)

def create_daily_reflection_summary(date: datetime = None) -> Optional[str]:
    """Create daily reflection summary."""
    return reflection_logger.create_daily_summary(date)

def get_fragments_by_type(fragment_type: FragmentType) -> List[Dict]:
    """Get fragments of specific type."""
    return reflection_logger.get_fragments_by_type(fragment_type)

def get_fragments_by_tone(tone: FragmentTone) -> List[Dict]:
    """Get fragments of specific tone."""
    return reflection_logger.get_fragments_by_tone(tone)

print("[ReflectionLogger] 🦉 DAWN reflection logging system initialized")
print(f"[ReflectionLogger] 📝 Ready to archive thoughts and inner experiences")
