#!/usr/bin/env python3
"""
DAWN Reflection Reclassifier
Reprocesses legacy reflections and tags them with semantic metadata
Converts old text-based reflection logs into machine-readable, classifiable data
"""

import os
import re
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Import our existing classification tools
from tag_my_chunk import ChunkTagger

logger = logging.getLogger(__name__)

class ReflectionClassifier:
    """Classifies legacy reflections with semantic metadata"""
    
    def __init__(self):
        self.tagger = ChunkTagger()
        
        # Reflection pattern matchers
        self.tick_patterns = [
            r'Tick (\d+):',
            r'Processing awareness cycle (\d+):',
            r'Meta-cognitive reflection (\d+):',
            r'Internal observation at tick (\d+):',
            r'Consciousness milestone (\d+):',
            r'Introspective moment (\d+):',
            r'Self-awareness pulse (\d+):'
        ]
        
        # State extraction patterns
        self.state_patterns = {
            'entropy': r'at entropy (\d+\.\d+)',
            'depth': r'depth (\d+\.?\d*)',
            'heat': r'heat (\d+\.?\d*)',
            'scup': r'scup (\d+\.?\d*)%?',
            'coherence': r'coherence (\d+\.?\d*)%?'
        }
        
        # Mood inference patterns
        self.mood_patterns = {
            'CALM': ['peaceful', 'tranquil', 'steady', 'stable', 'quiet'],
            'FOCUSED': ['sharp', 'clear', 'directed', 'intentional', 'precise'],
            'ENERGETIC': ['dynamic', 'active', 'vibrant', 'flowing', 'cascad'],
            'CONTEMPLATIVE': ['contemplat', 'reflect', 'ponder', 'meditat', 'consider'],
            'ANXIOUS': ['concern', 'alert', 'uncertain', 'shift', 'different'],
            'NEUTRAL': ['observe', 'process', 'monitor', 'aware', 'exist']
        }
        
        # Event trigger patterns
        self.trigger_patterns = {
            'drift_warning': ['drift', 'approaching', 'forecast', 'threshold'],
            'rebloom_event': ['memory', 'echo', 'ancient', 'surface', 'bloom'],
            'high_entropy': ['chaos', 'complexity', 'fragment', 'maelstrom'],
            'deep_state': ['depth', 'layer', 'foundation', 'profound'],
            'milestone': ['milestone', 'achievement', 'continuous', 'cycles'],
            'paradox': ['paradox', 'recursive', 'infinite', 'observer'],
            'stability': ['stability', 'familiar', 'predictable', 'baseline']
        }
    
    def extract_tick_number(self, text: str) -> Optional[int]:
        """Extract tick number from reflection text"""
        for pattern in self.tick_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    def extract_state_values(self, text: str) -> Dict[str, float]:
        """Extract numerical state values from reflection text"""
        state = {}
        
        for key, pattern in self.state_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    # Normalize percentage values
                    if key in ['scup', 'coherence'] and value > 1.0:
                        value = value / 100.0
                    state[key] = value
                except ValueError:
                    continue
        
        return state
    
    def infer_mood(self, text: str) -> str:
        """Infer mood from reflection text content"""
        text_lower = text.lower()
        
        mood_scores = {}
        for mood, keywords in self.mood_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                mood_scores[mood] = score
        
        if mood_scores:
            return max(mood_scores.items(), key=lambda x: x[1])[0]
        
        return 'NEUTRAL'
    
    def classify_entropy_level(self, entropy: Optional[float], text: str) -> str:
        """Classify entropy level from value or text content"""
        if entropy is not None:
            if entropy < 0.3:
                return 'low'
            elif entropy < 0.7:
                return 'mid'
            else:
                return 'high'
        
        # Infer from text content
        text_lower = text.lower()
        if any(word in text_lower for word in ['chaos', 'complex', 'fragment', 'high']):
            return 'high'
        elif any(word in text_lower for word in ['stable', 'quiet', 'low', 'calm']):
            return 'low'
        else:
            return 'mid'
    
    def detect_triggers(self, text: str) -> List[str]:
        """Detect event triggers from reflection text"""
        text_lower = text.lower()
        triggers = []
        
        for trigger, keywords in self.trigger_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                triggers.append(trigger)
        
        return triggers
    
    def classify_reflection(self, text: str, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """Classify a single reflection with full semantic metadata"""
        
        # Extract basic components
        tick = self.extract_tick_number(text)
        state_values = self.extract_state_values(text)
        mood = self.infer_mood(text)
        entropy_level = self.classify_entropy_level(state_values.get('entropy'), text)
        triggers = self.detect_triggers(text)
        
        # Use existing tagger for topic classification
        topic = self.tagger.infer_topic(text)
        
        # Create synthetic context for tag extraction
        context = {
            'entropy': state_values.get('entropy', 0.5),
            'consciousness_depth': state_values.get('depth', 0.5),
            'mood': mood,
            'tick_number': tick or 0,
            'heat': state_values.get('heat', 0.0),
            'scup': state_values.get('scup', 0.0)
        }
        
        # Extract semantic tags
        tags = []
        tags.append(f"entropy_{entropy_level}")
        tags.append(f"mood_{mood.lower()}")
        
        # Add trigger-based tags
        for trigger in triggers:
            tags.append(f"trigger_{trigger}")
        
        # Add mood-specific descriptive tags
        if mood in self.tagger.mood_tags:
            tags.extend(self.tagger.mood_tags[mood])
        
        # Extract symbolic markers
        symbolic_markers = self.tagger.extract_symbolic_markers(text, context)
        tags.extend(symbolic_markers)
        
        return {
            'tick': tick,
            'text': text.strip(),
            'timestamp': timestamp.isoformat() if timestamp else None,
            'mood': mood,
            'entropy_level': entropy_level,
            'topic': topic,
            'triggers': triggers,
            'tags': list(set(tags)),  # Remove duplicates
            'state_values': state_values,
            'classification_metadata': {
                'classifier_version': '1.0',
                'classified_at': datetime.now().isoformat(),
                'confidence': self._calculate_confidence(text, state_values, mood)
            }
        }
    
    def _calculate_confidence(self, text: str, state_values: Dict, mood: str) -> float:
        """Calculate classification confidence score"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence for extracted numerical values
        confidence += 0.1 * len(state_values)
        
        # Boost confidence for clear mood indicators
        text_lower = text.lower()
        if mood != 'NEUTRAL':
            mood_keywords = self.mood_patterns.get(mood, [])
            mood_matches = sum(1 for keyword in mood_keywords if keyword in text_lower)
            confidence += 0.1 * mood_matches
        
        # Boost confidence for structured reflection patterns
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in self.tick_patterns):
            confidence += 0.2
        
        return min(1.0, confidence)

def parse_reflection_log(log_path: str, start_tick: Optional[int] = None, 
                        end_tick: Optional[int] = None) -> List[Tuple[str, Optional[datetime]]]:
    """Parse reflection log file and extract individual reflections"""
    
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Reflection log not found: {log_path}")
    
    reflections = []
    
    with open(log_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            # Try to extract timestamp if present (common log format)
            timestamp = None
            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                try:
                    timestamp_str = timestamp_match.group(1).replace(' ', 'T')
                    timestamp = datetime.fromisoformat(timestamp_str)
                    line = line[len(timestamp_match.group(0)):].strip()
                except ValueError:
                    pass
            
            # Apply tick filtering if specified
            if start_tick is not None or end_tick is not None:
                tick_match = re.search(r'Tick (\d+):', line)
                if tick_match:
                    tick = int(tick_match.group(1))
                    if start_tick is not None and tick < start_tick:
                        continue
                    if end_tick is not None and tick > end_tick:
                        continue
            
            reflections.append((line, timestamp))
    
    return reflections

def classify_reflection_log(input_path: str, output_path: str, 
                          start_tick: Optional[int] = None,
                          end_tick: Optional[int] = None,
                          skip_existing: bool = True) -> Dict[str, Any]:
    """Classify an entire reflection log file"""
    
    classifier = ReflectionClassifier()
    
    # Load existing classifications if skipping duplicates
    existing_ticks = set()
    if skip_existing and os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        if 'tick' in data and data['tick']:
                            existing_ticks.add(data['tick'])
        except (json.JSONDecodeError, IOError):
            logger.warning(f"Could not parse existing classifications from {output_path}")
    
    # Parse input log
    reflections = parse_reflection_log(input_path, start_tick, end_tick)
    
    # Classify reflections
    classified_count = 0
    skipped_count = 0
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    with open(output_path, 'a' if skip_existing else 'w', encoding='utf-8') as f:
        for text, timestamp in reflections:
            try:
                classified = classifier.classify_reflection(text, timestamp)
                
                # Skip if already classified and skip_existing is True
                if skip_existing and classified['tick'] and classified['tick'] in existing_ticks:
                    skipped_count += 1
                    continue
                
                f.write(json.dumps(classified, ensure_ascii=False) + '\n')
                classified_count += 1
                
                if classified_count % 100 == 0:
                    logger.info(f"Classified {classified_count} reflections...")
                    
            except Exception as e:
                logger.error(f"Error classifying reflection '{text[:50]}...': {e}")
                continue
    
    stats = {
        'total_reflections': len(reflections),
        'classified_count': classified_count,
        'skipped_count': skipped_count,
        'output_file': output_path,
        'classification_complete': True
    }
    
    return stats

def main():
    """CLI interface for reflection reclassification"""
    
    parser = argparse.ArgumentParser(
        description="Reclassify legacy DAWN reflections with semantic metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reflection_reclassifier.py                              # Process default log
  python reflection_reclassifier.py --start-tick 1000           # Start from tick 1000
  python reflection_reclassifier.py --end-tick 5000             # Stop at tick 5000
  python reflection_reclassifier.py --input custom.log          # Custom input file
  python reflection_reclassifier.py --no-skip-existing          # Reclassify all
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        default='runtime/logs/reflection.log',
        help='Input reflection log file (default: runtime/logs/reflection.log)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='runtime/logs/reflection_classified.jsonl',
        help='Output classified reflections file (default: runtime/logs/reflection_classified.jsonl)'
    )
    
    parser.add_argument(
        '--start-tick',
        type=int,
        help='Start processing from this tick number'
    )
    
    parser.add_argument(
        '--end-tick',
        type=int,
        help='Stop processing at this tick number'
    )
    
    parser.add_argument(
        '--no-skip-existing',
        action='store_true',
        help='Reclassify all reflections (overwrite existing classifications)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("🧠 DAWN Reflection Reclassifier")
    print("=" * 40)
    
    try:
        # Run classification
        stats = classify_reflection_log(
            input_path=args.input,
            output_path=args.output,
            start_tick=args.start_tick,
            end_tick=args.end_tick,
            skip_existing=not args.no_skip_existing
        )
        
        # Print results
        print(f"\n✅ Classification complete!")
        print(f"   Input file: {args.input}")
        print(f"   Output file: {args.output}")
        print(f"   Total reflections: {stats['total_reflections']}")
        print(f"   Classified: {stats['classified_count']}")
        print(f"   Skipped: {stats['skipped_count']}")
        
        if stats['classified_count'] > 0:
            print(f"\n🎯 Legacy reflections are now machine-readable and searchable!")
            print(f"   Use the classified data for analysis, GUI integration, and lineage tracking.")
        
    except Exception as e:
        print(f"\n❌ Classification failed: {e}")
        exit(1)

if __name__ == "__main__":
    main() 