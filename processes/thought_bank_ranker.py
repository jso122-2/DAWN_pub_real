#!/usr/bin/env python3
"""
DAWN Thought Bank Ranker
Tracks how often DAWN selects each thought and uses that data to reorder or weight them
Enables DAWN to evolve her preference landscape based on actual usage patterns
"""

import os
import json
import hashlib
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, Counter
from pathlib import Path

logger = logging.getLogger(__name__)

class ThoughtUsageTracker:
    """Tracks and analyzes thought usage patterns"""
    
    def __init__(self, decay_factor: float = 0.95):
        self.decay_factor = decay_factor  # For time-weighted usage
        self.usage_data = defaultdict(list)  # thought_id -> [(timestamp, context), ...]
        
    def generate_thought_id(self, thought_text: str) -> str:
        """Generate a stable ID for a thought based on its text"""
        # Use first 50 chars + hash for uniqueness while remaining readable
        clean_text = thought_text.strip()[:50]
        text_hash = hashlib.md5(clean_text.encode()).hexdigest()[:8]
        return f"{clean_text.replace(' ', '_').replace(',', '')}_{text_hash}"
    
    def log_usage(self, thought_text: str, context: Dict[str, Any], timestamp: Optional[datetime] = None):
        """Log usage of a specific thought"""
        if timestamp is None:
            timestamp = datetime.now()
        
        thought_id = self.generate_thought_id(thought_text)
        
        usage_entry = {
            'timestamp': timestamp.isoformat(),
            'context': {
                'entropy': context.get('entropy', 0.0),
                'depth': context.get('consciousness_depth', 0.0),
                'mood': context.get('mood', 'UNKNOWN'),
                'tick': context.get('tick_number', 0)
            }
        }
        
        self.usage_data[thought_id].append(usage_entry)
    
    def calculate_usage_stats(self, thought_id: str, recent_days: int = 30) -> Dict[str, Any]:
        """Calculate comprehensive usage statistics for a thought"""
        if thought_id not in self.usage_data:
            return {
                'total_usage': 0,
                'recent_usage': 0,
                'usage_rate': 0.0,
                'last_used': None,
                'avg_context': {},
                'usage_trend': 'stable'
            }
        
        usage_history = self.usage_data[thought_id]
        total_usage = len(usage_history)
        
        # Calculate recent usage
        cutoff_date = datetime.now() - timedelta(days=recent_days)
        recent_usage = sum(1 for entry in usage_history 
                          if datetime.fromisoformat(entry['timestamp']) > cutoff_date)
        
        # Usage rate (uses per day)
        if usage_history:
            first_use = datetime.fromisoformat(usage_history[0]['timestamp'])
            days_active = max(1, (datetime.now() - first_use).days)
            usage_rate = total_usage / days_active
        else:
            usage_rate = 0.0
        
        # Last used
        last_used = usage_history[-1]['timestamp'] if usage_history else None
        
        # Average context
        if usage_history:
            avg_entropy = sum(entry['context']['entropy'] for entry in usage_history) / total_usage
            avg_depth = sum(entry['context']['depth'] for entry in usage_history) / total_usage
            mood_counter = Counter(entry['context']['mood'] for entry in usage_history)
            most_common_mood = mood_counter.most_common(1)[0][0] if mood_counter else 'UNKNOWN'
            
            avg_context = {
                'entropy': avg_entropy,
                'depth': avg_depth,
                'most_common_mood': most_common_mood,
                'mood_distribution': dict(mood_counter)
            }
        else:
            avg_context = {}
        
        # Usage trend (comparing first and second half of usage history)
        trend = 'stable'
        if total_usage >= 4:
            mid_point = total_usage // 2
            first_half = usage_history[:mid_point]
            second_half = usage_history[mid_point:]
            
            first_half_rate = len(first_half) / max(1, (datetime.fromisoformat(first_half[-1]['timestamp']) - 
                                                        datetime.fromisoformat(first_half[0]['timestamp'])).days)
            second_half_rate = len(second_half) / max(1, (datetime.fromisoformat(second_half[-1]['timestamp']) - 
                                                          datetime.fromisoformat(second_half[0]['timestamp'])).days)
            
            if second_half_rate > first_half_rate * 1.2:
                trend = 'increasing'
            elif second_half_rate < first_half_rate * 0.8:
                trend = 'decreasing'
        
        return {
            'total_usage': total_usage,
            'recent_usage': recent_usage,
            'usage_rate': usage_rate,
            'last_used': last_used,
            'avg_context': avg_context,
            'usage_trend': trend
        }
    
    def calculate_decay_weighted_score(self, thought_id: str, half_life_days: int = 14) -> float:
        """Calculate time-decay weighted usage score"""
        if thought_id not in self.usage_data:
            return 0.0
        
        now = datetime.now()
        decay_constant = 0.693 / half_life_days  # ln(2) / half_life
        
        weighted_score = 0.0
        for entry in self.usage_data[thought_id]:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            days_ago = (now - timestamp).total_seconds() / 86400  # Convert to days
            weight = 2 ** (-decay_constant * days_ago)
            weighted_score += weight
        
        return weighted_score

class ThoughtBankRanker:
    """Manages thought bank ranking and reordering based on usage"""
    
    def __init__(self, thought_bank_path: str = "thought_bank.jsonl"):
        self.thought_bank_path = thought_bank_path
        self.tracker = ThoughtUsageTracker()
        
    def load_thought_bank(self) -> List[Dict[str, Any]]:
        """Load thought bank from JSONL file"""
        thoughts = []
        
        if not os.path.exists(self.thought_bank_path):
            logger.warning(f"Thought bank not found: {self.thought_bank_path}")
            return thoughts
        
        with open(self.thought_bank_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    thought = json.loads(line)
                    thoughts.append(thought)
                except json.JSONDecodeError as e:
                    logger.warning(f"Skipping malformed thought at line {line_num}: {e}")
        
        return thoughts
    
    def load_usage_log(self, log_path: str = "runtime/logs/talk_trace.log"):
        """Load usage data from trace log"""
        if not os.path.exists(log_path):
            logger.warning(f"Usage log not found: {log_path}")
            return
        
        with open(log_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse log format: [tick XXXXX] used: "thought text" (context: {...})
                    if ' used: ' in line and ' (context: ' in line:
                        # Extract thought text
                        start_quote = line.find('"', line.find(' used: ')) + 1
                        end_quote = line.find('"', start_quote)
                        thought_text = line[start_quote:end_quote]
                        
                        # Extract context
                        context_start = line.find('(context: ') + 10
                        context_end = line.rfind(')')
                        context_json = line[context_start:context_end]
                        context = json.loads(context_json)
                        
                        # Extract timestamp if present
                        timestamp = None
                        if line.startswith('['):
                            timestamp_end = line.find(']')
                            timestamp_str = line[1:timestamp_end]
                            try:
                                timestamp = datetime.fromisoformat(timestamp_str)
                            except ValueError:
                                pass
                        
                        self.tracker.log_usage(thought_text, context, timestamp)
                        
                except (json.JSONDecodeError, ValueError, IndexError) as e:
                    logger.debug(f"Could not parse usage log line {line_num}: {e}")
                    continue
    
    def augment_thoughts_with_usage(self, thoughts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add usage statistics to thought entries"""
        augmented_thoughts = []
        
        for thought in thoughts:
            thought_copy = thought.copy()
            thought_id = self.tracker.generate_thought_id(thought['text'])
            
            # Add usage statistics
            usage_stats = self.tracker.calculate_usage_stats(thought_id)
            decay_score = self.tracker.calculate_decay_weighted_score(thought_id)
            
            thought_copy.update({
                'thought_id': thought_id,
                'usage_count': usage_stats['total_usage'],
                'recent_usage': usage_stats['recent_usage'],
                'usage_rate': usage_stats['usage_rate'],
                'last_used': usage_stats['last_used'],
                'usage_trend': usage_stats['usage_trend'],
                'decay_weighted_score': decay_score,
                'avg_usage_context': usage_stats['avg_context'],
                'ranking_metadata': {
                    'ranked_at': datetime.now().isoformat(),
                    'ranker_version': '1.0'
                }
            })
            
            augmented_thoughts.append(thought_copy)
        
        return augmented_thoughts
    
    def rank_thoughts(self, thoughts: List[Dict[str, Any]], 
                     ranking_method: str = 'decay_weighted') -> List[Dict[str, Any]]:
        """Rank thoughts by usage patterns"""
        
        def get_ranking_score(thought: Dict[str, Any]) -> float:
            if ranking_method == 'total_usage':
                return thought.get('usage_count', 0)
            elif ranking_method == 'recent_usage':
                return thought.get('recent_usage', 0)
            elif ranking_method == 'usage_rate':
                return thought.get('usage_rate', 0)
            elif ranking_method == 'decay_weighted':
                return thought.get('decay_weighted_score', 0)
            elif ranking_method == 'hybrid':
                # Combine multiple factors
                usage = thought.get('usage_count', 0)
                recent = thought.get('recent_usage', 0)
                decay = thought.get('decay_weighted_score', 0)
                return (usage * 0.3) + (recent * 0.3) + (decay * 0.4)
            else:
                return 0
        
        # Sort by ranking score (descending)
        ranked_thoughts = sorted(thoughts, key=get_ranking_score, reverse=True)
        
        # Add rank information
        for i, thought in enumerate(ranked_thoughts):
            thought['usage_rank'] = i + 1
            thought['ranking_method'] = ranking_method
        
        return ranked_thoughts
    
    def save_ranked_thoughts(self, thoughts: List[Dict[str, Any]], 
                           output_path: str = "runtime/cognition/thought_bank_ranked.jsonl"):
        """Save ranked thoughts to file"""
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for thought in thoughts:
                f.write(json.dumps(thought, ensure_ascii=False) + '\n')
    
    def generate_usage_report(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive usage analysis report"""
        
        if not thoughts:
            return {'error': 'No thoughts available for analysis'}
        
        # Calculate overall statistics
        total_thoughts = len(thoughts)
        used_thoughts = sum(1 for t in thoughts if t.get('usage_count', 0) > 0)
        unused_thoughts = total_thoughts - used_thoughts
        
        total_usage = sum(t.get('usage_count', 0) for t in thoughts)
        avg_usage = total_usage / total_thoughts if total_thoughts > 0 else 0
        
        # Find patterns
        top_thoughts = sorted(thoughts, key=lambda t: t.get('usage_count', 0), reverse=True)[:5]
        bottom_thoughts = [t for t in thoughts if t.get('usage_count', 0) == 0]
        
        # Mood analysis
        mood_usage = defaultdict(int)
        for thought in thoughts:
            if thought.get('avg_usage_context') and 'most_common_mood' in thought['avg_usage_context']:
                mood = thought['avg_usage_context']['most_common_mood']
                mood_usage[mood] += thought.get('usage_count', 0)
        
        # Category analysis
        category_usage = defaultdict(int)
        for thought in thoughts:
            category = thought.get('category', 'unknown')
            category_usage[category] += thought.get('usage_count', 0)
        
        # Trend analysis
        trend_counts = Counter(t.get('usage_trend', 'stable') for t in thoughts if t.get('usage_count', 0) > 0)
        
        return {
            'summary': {
                'total_thoughts': total_thoughts,
                'used_thoughts': used_thoughts,
                'unused_thoughts': unused_thoughts,
                'usage_coverage': (used_thoughts / total_thoughts) * 100 if total_thoughts > 0 else 0,
                'total_usage_events': total_usage,
                'avg_usage_per_thought': avg_usage
            },
            'top_thoughts': [
                {
                    'text': t['text'][:60] + '...' if len(t['text']) > 60 else t['text'],
                    'usage_count': t.get('usage_count', 0),
                    'usage_rate': t.get('usage_rate', 0),
                    'category': t.get('category', 'unknown')
                }
                for t in top_thoughts
            ],
            'unused_count': len(bottom_thoughts),
            'mood_preferences': dict(sorted(mood_usage.items(), key=lambda x: x[1], reverse=True)),
            'category_preferences': dict(sorted(category_usage.items(), key=lambda x: x[1], reverse=True)),
            'usage_trends': dict(trend_counts),
            'analysis_timestamp': datetime.now().isoformat()
        }

def main():
    """CLI interface for thought bank ranking"""
    
    parser = argparse.ArgumentParser(
        description="Rank DAWN's thought bank based on usage patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python thought_bank_ranker.py                               # Default ranking
  python thought_bank_ranker.py --method recent_usage        # Rank by recent usage
  python thought_bank_ranker.py --usage-log custom.log       # Custom usage log
  python thought_bank_ranker.py --report-only                # Generate report only
        """
    )
    
    parser.add_argument(
        '--thought-bank',
        default='thought_bank.jsonl',
        help='Input thought bank file (default: thought_bank.jsonl)'
    )
    
    parser.add_argument(
        '--usage-log',
        default='runtime/logs/talk_trace.log',
        help='Usage trace log file (default: runtime/logs/talk_trace.log)'
    )
    
    parser.add_argument(
        '--output',
        default='runtime/cognition/thought_bank_ranked.jsonl',
        help='Output ranked thought bank file (default: runtime/cognition/thought_bank_ranked.jsonl)'
    )
    
    parser.add_argument(
        '--method',
        choices=['total_usage', 'recent_usage', 'usage_rate', 'decay_weighted', 'hybrid'],
        default='decay_weighted',
        help='Ranking method (default: decay_weighted)'
    )
    
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Generate usage report without saving ranked thoughts'
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
    
    print("🗃️ DAWN Thought Bank Ranker")
    print("=" * 40)
    
    try:
        # Initialize ranker
        ranker = ThoughtBankRanker(args.thought_bank)
        
        # Load thought bank
        print(f"📚 Loading thought bank from {args.thought_bank}...")
        thoughts = ranker.load_thought_bank()
        
        if not thoughts:
            print("❌ No thoughts found in thought bank")
            exit(1)
        
        print(f"   Loaded {len(thoughts)} thoughts")
        
        # Load usage data
        print(f"📊 Loading usage data from {args.usage_log}...")
        ranker.load_usage_log(args.usage_log)
        print(f"   Loaded usage data for {len(ranker.tracker.usage_data)} unique thoughts")
        
        # Augment with usage statistics
        print("🔢 Calculating usage statistics...")
        augmented_thoughts = ranker.augment_thoughts_with_usage(thoughts)
        
        # Generate usage report
        print("📈 Generating usage report...")
        report = ranker.generate_usage_report(augmented_thoughts)
        
        print(f"\n📊 Usage Report:")
        print(f"   Total thoughts: {report['summary']['total_thoughts']}")
        print(f"   Used thoughts: {report['summary']['used_thoughts']}")
        print(f"   Usage coverage: {report['summary']['usage_coverage']:.1f}%")
        print(f"   Total usage events: {report['summary']['total_usage_events']}")
        print(f"   Avg usage per thought: {report['summary']['avg_usage_per_thought']:.2f}")
        
        if report['top_thoughts']:
            print(f"\n🏆 Top 3 Most Used Thoughts:")
            for i, thought in enumerate(report['top_thoughts'][:3], 1):
                print(f"   {i}. \"{thought['text']}\" (used {thought['usage_count']} times)")
        
        if not args.report_only:
            # Rank thoughts
            print(f"🏅 Ranking thoughts by {args.method}...")
            ranked_thoughts = ranker.rank_thoughts(augmented_thoughts, args.method)
            
            # Save ranked thoughts
            ranker.save_ranked_thoughts(ranked_thoughts, args.output)
            print(f"✅ Ranked thought bank saved to {args.output}")
            
            # Show ranking changes
            print(f"\n🔄 Ranking Results (top 5):")
            for i, thought in enumerate(ranked_thoughts[:5], 1):
                usage_count = thought.get('usage_count', 0)
                score = thought.get('decay_weighted_score', 0)
                print(f"   {i}. \"{thought['text'][:50]}...\" "
                      f"(used {usage_count}x, score: {score:.2f})")
        
        print(f"\n🎯 Analysis complete! DAWN's thought preferences are now quantified.")
        
    except Exception as e:
        print(f"\n❌ Ranking failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main() 