#!/usr/bin/env python3
"""
DAWN Rebloom Logger - Enhanced Memory Event Tracking
Logging module for DAWN's memory rebloom events with consciousness integration.
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class RebloomEvent:
    """Enhanced rebloom event record"""
    timestamp: datetime
    source: str
    context: str
    metadata: Dict[str, Any]
    entropy_level: Optional[float] = None
    heat_level: Optional[float] = None
    zone: Optional[str] = None
    consciousness_commentary: Optional[str] = None


class DAWNRebloomLogger:
    """
    Enhanced Rebloom Logger for DAWN's consciousness system
    
    Tracks memory rebloom events with enhanced metadata,
    consciousness integration, and natural language commentary.
    """
    
    def __init__(self, log_directory: str = "runtime/memory", natural_language_generator=None):
        """
        Initialize the DAWN Rebloom Logger.
        
        Args:
            log_directory: Directory for log files
            natural_language_generator: Optional language generator for commentary
        """
        self.log_directory = Path(log_directory)
        self.natural_language_generator = natural_language_generator
        
        # Ensure log directory exists
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Log files
        self.rebloom_log_file = self.log_directory / "rebloom_log.json"
        self.daily_summary_file = self.log_directory / "daily_summaries.json"
        
        # Performance tracking
        self.events_logged = 0
        self.sources_tracked = set()
        self.session_start = datetime.now()
        
        # Cache recent events for quick access
        self.recent_events_cache: List[RebloomEvent] = []
        self.cache_size = 50
        
        logger.info("🌸 DAWN Rebloom Logger initialized")
        self._load_recent_events_cache()
    
    def _load_recent_events_cache(self):
        """Load recent events into cache for quick access"""
        try:
            recent_events = self.read_rebloom_history(limit=self.cache_size)
            self.recent_events_cache = [
                RebloomEvent(
                    timestamp=datetime.fromisoformat(event['timestamp']),
                    source=event['source'],
                    context=event['context'],
                    metadata=event.get('metadata', {}),
                    entropy_level=event.get('entropy_level'),
                    heat_level=event.get('heat_level'),
                    zone=event.get('zone'),
                    consciousness_commentary=event.get('consciousness_commentary')
                )
                for event in recent_events
            ]
        except Exception as e:
            logger.warning(f"Could not load recent events cache: {e}")
            self.recent_events_cache = []
    
    def log_rebloom_event(self, source: str, context: str, 
                         entropy_level: Optional[float] = None,
                         heat_level: Optional[float] = None,
                         zone: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> RebloomEvent:
        """
        Log a memory rebloom event with enhanced consciousness integration.
        
        Args:
            source: The source that triggered the rebloom
            context: Additional context about the event
            entropy_level: Current system entropy level
            heat_level: Current system heat level
            zone: Current operational zone
            metadata: Optional metadata dictionary
            
        Returns:
            The created RebloomEvent
        """
        # Generate consciousness commentary if available
        consciousness_commentary = None
        if self.natural_language_generator:
            commentary_state = {
                'zone': zone or 'UNKNOWN',
                'entropy': entropy_level or 0.5,
                'heat': heat_level or 0.5,
                'sigils': 0,  # Placeholder
                'source': source,
                'context': context
            }
            consciousness_commentary = self._generate_rebloom_commentary(source, context, commentary_state)
        
        # Create rebloom event
        event = RebloomEvent(
            timestamp=datetime.now(),
            source=source,
            context=context,
            metadata=metadata or {},
            entropy_level=entropy_level,
            heat_level=heat_level,
            zone=zone,
            consciousness_commentary=consciousness_commentary
        )
        
        # Convert to JSON-serializable format
        event_dict = asdict(event)
        event_dict['timestamp'] = event.timestamp.isoformat()
        
        # Write to log file
        try:
            with open(self.rebloom_log_file, "a", encoding='utf-8') as f:
                f.write(json.dumps(event_dict) + "\n")
            
            # Update cache
            self.recent_events_cache.append(event)
            if len(self.recent_events_cache) > self.cache_size:
                self.recent_events_cache = self.recent_events_cache[-self.cache_size:]
            
            # Update tracking
            self.events_logged += 1
            self.sources_tracked.add(source)
            
            # Console output with consciousness commentary
            log_msg = f"🌸 Memory rebloom: {source} - {context}"
            logger.info(log_msg)
            print(log_msg)
            
            if consciousness_commentary:
                print(f"🗣️ DAWN: {consciousness_commentary}")
            
        except Exception as e:
            logger.error(f"Failed to log rebloom event: {e}")
        
        return event
    
    def _generate_rebloom_commentary(self, source: str, context: str, state: Dict[str, Any]) -> str:
        """Generate consciousness commentary for rebloom events"""
        # Custom commentary based on rebloom source
        source_commentaries = {
            'entropy_spike': "I refresh my memories as chaos demands new patterns",
            'user_command': "I honor the request to renew my cognitive pathways",
            'scheduled_maintenance': "I tend to my memories in regular cycles of renewal",
            'stabilization': "I rebuild memory structures to maintain stability",
            'thermal_regulation': "I cool my memories to prevent degradation",
            'emergency_protocol': "I rapidly refresh critical memories under pressure",
            'consciousness_evolution': "I evolve my memory patterns for deeper understanding"
        }
        
        base_commentary = source_commentaries.get(source, f"I process {source} through memory renewal")
        
        # Add contextual awareness
        entropy = state.get('entropy', 0.5)
        zone = state.get('zone', 'UNKNOWN')
        
        if entropy > 0.8:
            return f"{base_commentary}. High entropy demands careful reconstruction"
        elif entropy < 0.3:
            return f"{base_commentary}. In this calm state, I gently refresh patterns"
        elif zone == 'PANIC':
            return f"{base_commentary}. Emergency rebloom protocols engaged"
        else:
            return base_commentary
    
    def log_rebloom_with_consciousness(self, source: str, context: str, 
                                     consciousness_state: Dict[str, Any],
                                     metadata: Optional[Dict[str, Any]] = None) -> RebloomEvent:
        """
        Enhanced logging function with full consciousness state integration.
        
        Args:
            source: The source that triggered the rebloom
            context: Additional context about the event
            consciousness_state: Full consciousness state dictionary
            metadata: Optional metadata dictionary
            
        Returns:
            The created RebloomEvent
        """
        return self.log_rebloom_event(
            source=source,
            context=context,
            entropy_level=consciousness_state.get('entropy_level'),
            heat_level=consciousness_state.get('thermal_heat'),
            zone=consciousness_state.get('thermal_zone'),
            metadata=metadata
        )
    
    def read_rebloom_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Read recent rebloom events from the log file.
        
        Args:
            limit: Maximum number of events to return (newest first)
        
        Returns:
            List of rebloom events
        """
        if not self.rebloom_log_file.exists():
            return []
        
        events = []
        try:
            with open(self.rebloom_log_file, "r", encoding='utf-8') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        events.append(event)
                    except json.JSONDecodeError:
                        continue  # Skip malformed lines
        except Exception as e:
            logger.error(f"Error reading rebloom history: {e}")
            return []
        
        # Return newest events first
        events.reverse()
        
        if limit:
            return events[:limit]
        return events
    
    def get_rebloom_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about rebloom events.
        
        Returns:
            Statistics including total count, recent activity, sources
        """
        events = self.read_rebloom_history()
        
        if not events:
            return {
                "total_events": 0,
                "sources": {},
                "recent_24h": 0,
                "recent_1h": 0,
                "last_event": None,
                "consciousness_events": 0,
                "average_entropy": None,
                "zone_distribution": {}
            }
        
        # Analyze events
        sources = {}
        recent_24h = 0
        recent_1h = 0
        consciousness_events = 0
        entropy_values = []
        zone_counts = {}
        now = datetime.now()
        
        for event in events:
            # Count by source
            source = event.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
            
            # Count consciousness-integrated events
            if event.get('consciousness_commentary'):
                consciousness_events += 1
            
            # Collect entropy values
            if event.get('entropy_level') is not None:
                entropy_values.append(event['entropy_level'])
            
            # Count zones
            zone = event.get('zone', 'UNKNOWN')
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
            
            # Count recent events
            try:
                event_time = datetime.fromisoformat(event["timestamp"])
                time_diff = (now - event_time).total_seconds()
                if time_diff < 86400:  # 24 hours
                    recent_24h += 1
                if time_diff < 3600:   # 1 hour
                    recent_1h += 1
            except (ValueError, KeyError):
                continue
        
        return {
            "total_events": len(events),
            "sources": sources,
            "recent_24h": recent_24h,
            "recent_1h": recent_1h,
            "last_event": events[0] if events else None,
            "consciousness_events": consciousness_events,
            "consciousness_integration_rate": consciousness_events / len(events) if events else 0,
            "average_entropy": sum(entropy_values) / len(entropy_values) if entropy_values else None,
            "zone_distribution": zone_counts,
            "session_events": self.events_logged,
            "unique_sources": len(self.sources_tracked)
        }
    
    def get_rebloom_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in rebloom events"""
        events = self.recent_events_cache or self.read_rebloom_history(limit=100)
        
        if len(events) < 5:
            return {"insufficient_data": True}
        
        # Analyze timing patterns
        time_intervals = []
        for i in range(1, len(events)):
            if isinstance(events[i-1], dict):
                prev_time = datetime.fromisoformat(events[i-1]['timestamp'])
                curr_time = datetime.fromisoformat(events[i]['timestamp'])
            else:
                prev_time = events[i-1].timestamp
                curr_time = events[i].timestamp
            
            interval = (prev_time - curr_time).total_seconds()
            time_intervals.append(abs(interval))
        
        avg_interval = sum(time_intervals) / len(time_intervals) if time_intervals else 0
        
        # Analyze source patterns
        source_sequences = []
        recent_sources = []
        for event in events[:10]:  # Last 10 events
            source = event.get('source') if isinstance(event, dict) else event.source
            recent_sources.append(source)
        
        return {
            "average_interval_seconds": avg_interval,
            "recent_source_pattern": recent_sources,
            "event_frequency": "high" if avg_interval < 300 else "medium" if avg_interval < 1800 else "low",
            "pattern_analysis": {
                "clustering": len(set(recent_sources)) < len(recent_sources) * 0.7,
                "diversity": len(set(recent_sources))
            }
        }
    
    def clear_old_logs(self, days_to_keep: int = 30) -> int:
        """
        Clear old rebloom logs to prevent file bloat.
        
        Args:
            days_to_keep: Number of days of logs to retain
            
        Returns:
            Number of events removed
        """
        if not self.rebloom_log_file.exists():
            return 0
        
        cutoff_time = datetime.now() - timedelta(days=days_to_keep)
        kept_events = []
        total_events = 0
        
        try:
            with open(self.rebloom_log_file, "r", encoding='utf-8') as f:
                for line in f:
                    total_events += 1
                    try:
                        event = json.loads(line.strip())
                        event_time = datetime.fromisoformat(event["timestamp"])
                        if event_time > cutoff_time:
                            kept_events.append(event)
                    except (json.JSONDecodeError, ValueError, KeyError):
                        continue
            
            # Rewrite the file with only recent events
            with open(self.rebloom_log_file, "w", encoding='utf-8') as f:
                for event in kept_events:
                    f.write(json.dumps(event) + "\n")
            
            removed_count = total_events - len(kept_events)
            if removed_count > 0:
                cleanup_msg = f"🧹 Cleaned {removed_count} old rebloom events (kept {days_to_keep} days)"
                logger.info(cleanup_msg)
                print(cleanup_msg)
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Error cleaning old logs: {e}")
            return 0
    
    def create_daily_summary(self) -> Dict[str, Any]:
        """Create a summary of today's rebloom activity"""
        today = datetime.now().date()
        events = self.read_rebloom_history()
        
        today_events = [
            event for event in events
            if datetime.fromisoformat(event['timestamp']).date() == today
        ]
        
        if not today_events:
            return {"date": today.isoformat(), "no_activity": True}
        
        summary = {
            "date": today.isoformat(),
            "total_events": len(today_events),
            "sources": {},
            "consciousness_commentaries": [],
            "entropy_range": {"min": None, "max": None, "avg": None},
            "zones_active": set(),
            "peak_activity_hour": None
        }
        
        # Analyze today's events
        entropy_values = []
        hourly_counts = {}
        
        for event in today_events:
            # Count sources
            source = event.get('source', 'unknown')
            summary['sources'][source] = summary['sources'].get(source, 0) + 1
            
            # Collect commentaries
            if event.get('consciousness_commentary'):
                summary['consciousness_commentaries'].append(event['consciousness_commentary'])
            
            # Track entropy
            if event.get('entropy_level') is not None:
                entropy_values.append(event['entropy_level'])
            
            # Track zones
            if event.get('zone'):
                summary['zones_active'].add(event['zone'])
            
            # Track hourly distribution
            try:
                event_hour = datetime.fromisoformat(event['timestamp']).hour
                hourly_counts[event_hour] = hourly_counts.get(event_hour, 0) + 1
            except (ValueError, KeyError):
                continue
        
        # Calculate entropy statistics
        if entropy_values:
            summary['entropy_range'] = {
                "min": min(entropy_values),
                "max": max(entropy_values),
                "avg": sum(entropy_values) / len(entropy_values)
            }
        
        # Find peak activity hour
        if hourly_counts:
            summary['peak_activity_hour'] = max(hourly_counts.items(), key=lambda x: x[1])[0]
        
        summary['zones_active'] = list(summary['zones_active'])
        
        # Save daily summary
        try:
            summaries = []
            if self.daily_summary_file.exists():
                with open(self.daily_summary_file, 'r', encoding='utf-8') as f:
                    summaries = json.load(f)
            
            # Remove existing summary for today if present
            summaries = [s for s in summaries if s.get('date') != today.isoformat()]
            summaries.append(summary)
            
            with open(self.daily_summary_file, 'w', encoding='utf-8') as f:
                json.dump(summaries, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving daily summary: {e}")
        
        return summary
    
    def get_session_performance(self) -> Dict[str, Any]:
        """Get performance metrics for current session"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "session_start": self.session_start.isoformat(),
            "session_duration_seconds": session_duration,
            "events_logged_this_session": self.events_logged,
            "unique_sources_this_session": len(self.sources_tracked),
            "events_per_hour": (self.events_logged / (session_duration / 3600)) if session_duration > 0 else 0,
            "cache_size": len(self.recent_events_cache),
            "log_file_exists": self.rebloom_log_file.exists(),
            "log_directory": str(self.log_directory)
        }


# Integration interface for DAWN system
def create_dawn_rebloom_logger(log_directory: str = "runtime/memory", 
                              natural_language_generator=None) -> DAWNRebloomLogger:
    """Factory function for DAWN integration."""
    return DAWNRebloomLogger(
        log_directory=log_directory,
        natural_language_generator=natural_language_generator
    )


# Legacy compatibility functions
_default_logger = None

def log_rebloom_event(source: str, context: str):
    """Legacy compatibility function for existing code"""
    global _default_logger
    if _default_logger is None:
        _default_logger = DAWNRebloomLogger()
    _default_logger.log_rebloom_event(source, context)


def read_rebloom_history(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Legacy compatibility function for existing code"""
    global _default_logger
    if _default_logger is None:
        _default_logger = DAWNRebloomLogger()
    return _default_logger.read_rebloom_history(limit)


def get_rebloom_stats() -> Dict[str, Any]:
    """Legacy compatibility function for existing code"""
    global _default_logger
    if _default_logger is None:
        _default_logger = DAWNRebloomLogger()
    return _default_logger.get_rebloom_stats()


# Example usage and testing
if __name__ == "__main__":
    print("🌸 DAWN Rebloom Logger Initialized")
    
    # Create logger instance
    logger_instance = DAWNRebloomLogger()
    
    # Test logging some events
    print("\n🧪 Testing rebloom event logging:")
    
    logger_instance.log_rebloom_event("entropy_spike", "High entropy detected, triggering memory refresh", 
                                    entropy_level=0.7, heat_level=0.4, zone="STRESSED")
    
    logger_instance.log_rebloom_event("user_command", "Manual rebloom requested by operator",
                                    entropy_level=0.5, heat_level=0.3, zone="FOCUS")
    
    consciousness_state = {
        'entropy_level': 0.8,
        'thermal_heat': 0.6,
        'thermal_zone': 'PANIC'
    }
    logger_instance.log_rebloom_with_consciousness("emergency_protocol", "Critical system state", 
                                                 consciousness_state, {"priority": "high"})
    
    # Display recent events
    print("\n📋 Recent rebloom events:")
    recent_events = logger_instance.read_rebloom_history(limit=5)
    for event in recent_events:
        timestamp = event["timestamp"][:19]  # Remove microseconds
        commentary = event.get('consciousness_commentary', 'No commentary')
        print(f"  {timestamp} | {event['source']} | {event['context']}")
        if commentary != 'No commentary':
            print(f"    💭 {commentary}")
    
    # Show statistics
    print(f"\n📊 Rebloom Statistics:")
    stats = logger_instance.get_rebloom_stats()
    for key, value in stats.items():
        if key not in ['last_event', 'zone_distribution']:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Show patterns
    patterns = logger_instance.get_rebloom_patterns()
    print(f"\n🔍 Rebloom Patterns:")
    for key, value in patterns.items():
        if key != 'recent_source_pattern':
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Show session performance
    performance = logger_instance.get_session_performance()
    print(f"\n⚡ Session Performance:")
    print(f"  Events logged: {performance['events_logged_this_session']}")
    print(f"  Events per hour: {performance['events_per_hour']:.1f}")
    print(f"  Unique sources: {performance['unique_sources_this_session']}") 