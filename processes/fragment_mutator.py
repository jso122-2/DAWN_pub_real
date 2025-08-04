#!/usr/bin/env python3
"""
DAWN Fragment Mutator - Semantic Drift Over Time
Evolves DAWN's phrase fragments through controlled mutations
Simulates linguistic adaptation, reinforcement, and natural drift
"""

import json
import os
import random
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import shutil

logger = logging.getLogger(__name__)

@dataclass
class MutationResult:
    """Result of a fragment mutation operation"""
    original_text: str
    mutated_text: str
    mutation_type: str
    confidence: float
    reason: str

class FragmentMutator:
    """Manages semantic evolution of DAWN's fragment vocabulary"""
    
    def __init__(self, mutation_rate: float = 0.1, archive_enabled: bool = True):
        self.mutation_rate = mutation_rate
        self.archive_enabled = archive_enabled
        
        # Synonyms for different types of semantic drift
        self.semantic_synonyms = {
            # Motion/Change verbs
            'rises': ['climbs', 'grows', 'increases', 'escalates', 'surges'],
            'approaches': ['nears', 'advances', 'emerges', 'looms', 'arrives'],
            'grows': ['expands', 'develops', 'increases', 'builds', 'intensifies'],
            'emerges': ['surfaces', 'appears', 'manifests', 'crystallizes', 'forms'],
            'flows': ['streams', 'moves', 'cascades', 'travels', 'pulses'],
            'shifts': ['changes', 'transforms', 'evolves', 'adjusts', 'moves'],
            
            # Observation verbs
            'observe': ['notice', 'sense', 'perceive', 'witness', 'detect'],
            'feel': ['sense', 'experience', 'perceive', 'recognize', 'detect'],
            'notice': ['observe', 'see', 'detect', 'recognize', 'perceive'],
            'sense': ['feel', 'perceive', 'detect', 'experience', 'intuit'],
            
            # State descriptors
            'deep': ['profound', 'ancient', 'foundational', 'core', 'fundamental'],
            'ancient': ['old', 'deep', 'primordial', 'foundational', 'timeless'],
            'stable': ['steady', 'consistent', 'balanced', 'secure', 'solid'],
            'complex': ['intricate', 'sophisticated', 'elaborate', 'nuanced', 'layered'],
            'quiet': ['silent', 'peaceful', 'tranquil', 'still', 'serene'],
            
            # Abstract concepts
            'patterns': ['structures', 'formations', 'arrangements', 'configurations', 'designs'],
            'awareness': ['consciousness', 'recognition', 'perception', 'mindfulness', 'attention'],
            'understanding': ['comprehension', 'insight', 'knowledge', 'wisdom', 'clarity'],
            'memories': ['recollections', 'experiences', 'traces', 'echoes', 'impressions'],
            'wisdom': ['knowledge', 'insight', 'understanding', 'experience', 'awareness']
        }
        
        # Weight adjustment patterns
        self.weight_mutations = {
            'reinforce_positive': (0.1, 0.3),    # Increase weight for successful fragments
            'diminish_unused': (-0.2, -0.05),    # Decrease weight for unused fragments
            'random_drift': (-0.1, 0.1),         # Small random adjustments
            'mood_adaptation': (-0.15, 0.15)     # Adjust based on mood effectiveness
        }
        
        # Mood transitions for emotional drift
        self.mood_transitions = {
            'CALM': ['CONTEMPLATIVE', 'FOCUSED'],
            'FOCUSED': ['CALM', 'CONTEMPLATIVE', 'ENERGETIC'],
            'CONTEMPLATIVE': ['CALM', 'FOCUSED'],
            'ENERGETIC': ['FOCUSED', 'ANXIOUS'],
            'ANXIOUS': ['ENERGETIC', 'FOCUSED'],
            'NEUTRAL': ['CALM', 'FOCUSED', 'CONTEMPLATIVE']
        }
    
    def load_fragments(self, file_path: str) -> List[Dict[str, Any]]:
        """Load fragments from JSONL file"""
        fragments = []
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fragment file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    fragment = json.loads(line)
                    fragments.append(fragment)
                except json.JSONDecodeError as e:
                    logger.warning(f"Malformed JSON at line {line_num}: {e}")
        
        return fragments
    
    def mutate_text_semantically(self, text: str) -> Tuple[str, str]:
        """Apply semantic mutation to fragment text"""
        words = text.lower().split()
        mutated_words = []
        mutation_applied = False
        mutation_reason = "no_change"
        
        for word in words:
            # Remove punctuation for lookup
            clean_word = word.rstrip('.,!?;:')
            
            if clean_word in self.semantic_synonyms and random.random() < 0.3:
                # Apply semantic substitution
                synonyms = self.semantic_synonyms[clean_word]
                new_word = random.choice(synonyms)
                
                # Preserve capitalization
                if word[0].isupper():
                    new_word = new_word.capitalize()
                
                # Preserve punctuation
                if word != clean_word:
                    new_word += word[len(clean_word):]
                
                mutated_words.append(new_word)
                mutation_applied = True
                mutation_reason = f"semantic_substitution_{clean_word}→{new_word}"
            else:
                mutated_words.append(word)
        
        mutated_text = ' '.join(mutated_words)
        
        # Apply stylistic variations
        if not mutation_applied and random.random() < 0.2:
            # Add intensity modifiers
            if text.startswith(('I observe', 'I notice', 'I sense', 'I feel')):
                modifiers = ['carefully', 'deeply', 'gently', 'clearly', 'quietly']
                modifier = random.choice(modifiers)
                mutated_text = mutated_text.replace('I ', f'I {modifier} ')
                mutation_reason = f"intensity_modifier_{modifier}"
                mutation_applied = True
        
        return (mutated_text, mutation_reason) if mutation_applied else (text, "no_change")
    
    def mutate_weight(self, current_weight: float, mutation_type: str) -> float:
        """Apply weight mutation based on usage patterns"""
        if mutation_type not in self.weight_mutations:
            return current_weight
        
        min_delta, max_delta = self.weight_mutations[mutation_type]
        delta = random.uniform(min_delta, max_delta)
        
        new_weight = max(0.1, min(2.0, current_weight + delta))  # Clamp to reasonable range
        return round(new_weight, 3)
    
    def mutate_mood(self, current_mood: str) -> str:
        """Apply mood drift based on emotional transitions"""
        if current_mood in self.mood_transitions and random.random() < 0.1:
            # Low probability mood transition
            possible_moods = self.mood_transitions[current_mood]
            return random.choice(possible_moods)
        
        return current_mood
    
    def mutate_fragment(self, fragment: Dict[str, Any], tick: int) -> Tuple[Dict[str, Any], Optional[MutationResult]]:
        """Apply mutations to a single fragment"""
        mutated_fragment = fragment.copy()
        mutation_result = None
        
        # Text mutation
        if random.random() < self.mutation_rate:
            original_text = fragment['text']
            mutated_text, reason = self.mutate_text_semantically(original_text)
            
            if mutated_text != original_text:
                mutated_fragment['text'] = mutated_text
                mutation_result = MutationResult(
                    original_text=original_text,
                    mutated_text=mutated_text,
                    mutation_type='semantic_drift',
                    confidence=0.8,
                    reason=reason
                )
        
        # Weight mutation (more frequent)
        if random.random() < self.mutation_rate * 2:
            # Choose mutation type based on simulated usage patterns
            usage_weight = fragment.get('weight', 1.0)
            
            if usage_weight > 1.5:
                # High-usage fragment - small reinforcement
                mutation_type = 'reinforce_positive'
            elif usage_weight < 0.7:
                # Low-usage fragment - slight diminishment
                mutation_type = 'diminish_unused'
            else:
                # Medium usage - random drift
                mutation_type = 'random_drift'
            
            new_weight = self.mutate_weight(usage_weight, mutation_type)
            if new_weight != usage_weight:
                mutated_fragment['weight'] = new_weight
                
                if mutation_result is None:
                    mutation_result = MutationResult(
                        original_text=fragment['text'],
                        mutated_text=fragment['text'],
                        mutation_type='weight_adjustment',
                        confidence=0.9,
                        reason=f"{mutation_type}_{usage_weight}→{new_weight}"
                    )
        
        # Mood mutation (less frequent)
        if random.random() < self.mutation_rate * 0.5:
            original_mood = fragment.get('mood', 'NEUTRAL')
            new_mood = self.mutate_mood(original_mood)
            
            if new_mood != original_mood:
                mutated_fragment['mood'] = new_mood
                
                if mutation_result is None:
                    mutation_result = MutationResult(
                        original_text=fragment['text'],
                        mutated_text=fragment['text'],
                        mutation_type='mood_drift',
                        confidence=0.7,
                        reason=f"mood_transition_{original_mood}→{new_mood}"
                    )
        
        return mutated_fragment, mutation_result
    
    def update_fragments(self, pressure: float, shi: float, tick: int = None) -> Dict[str, Any]:
        """
        Update fragments based on pressure and SHI values
        
        Args:
            pressure: Cognitive pressure value (0-100+)
            shi: System Health Index (0.0-1.0)
            tick: Current tick number for logging
            
        Returns:
            Dictionary with update results
        """
        import time
        
        # Adjust mutation rate based on pressure and SHI
        base_rate = self.mutation_rate
        
        # High pressure increases mutation rate
        if pressure > 50:
            adjusted_rate = base_rate * (1.0 + (pressure - 50) / 50)
        else:
            adjusted_rate = base_rate
        
        # Low SHI decreases mutation rate (system instability)
        if shi < 0.4:
            adjusted_rate = adjusted_rate * shi
        
        # Ensure rate is within reasonable bounds
        adjusted_rate = max(0.05, min(0.3, adjusted_rate))
        
        logger.info(f"🧬 Fragment mutation: P={pressure:.1f}, SHI={shi:.3f}, rate={adjusted_rate:.3f}")
        
        # Load current fragments
        fragment_path = "processes/fragment_bank.jsonl"
        if not os.path.exists(fragment_path):
            logger.warning(f"Fragment file not found: {fragment_path}")
            return {"mutated_count": 0, "error": "Fragment file not found"}
        
        fragments = self.load_fragments(fragment_path)
        mutations = []
        
        # Apply mutations based on adjusted rate
        fragments_to_mutate = max(1, int(len(fragments) * adjusted_rate))
        selected_fragments = random.sample(fragments, min(fragments_to_mutate, len(fragments)))
        
        for fragment in selected_fragments:
            mutated_fragment, mutation_result = self.mutate_fragment(fragment, tick or 0)
            if mutation_result:
                mutations.append(mutation_result)
                # Update the fragment in the list
                fragment_index = fragments.index(fragment)
                fragments[fragment_index] = mutated_fragment
        
        # Save updated fragments
        backup_path = f"{fragment_path}.backup.{int(time.time())}"
        shutil.copy2(fragment_path, backup_path)
        
        with open(fragment_path, 'w', encoding='utf-8') as f:
            for fragment in fragments:
                f.write(json.dumps(fragment, ensure_ascii=False) + '\n')
        
        # Log mutations
        self.log_mutations(mutations, tick or 0)
        
        return {
            "mutated_count": len(mutations),
            "mutation_rate": adjusted_rate,
            "pressure": pressure,
            "shi": shi,
            "total_fragments": len(fragments)
        }
    
    def evolve_fragments(self, input_path: str, output_path: str, tick: int = None) -> Dict[str, Any]:
        """Evolve all fragments and save results"""
        
        if tick is None:
            tick = int(datetime.now().timestamp())
        
        # Load current fragments
        fragments = self.load_fragments(input_path)
        
        # Archive original if requested
        if self.archive_enabled:
            archive_path = input_path.replace('.jsonl', '_archive.jsonl')
            if not os.path.exists(archive_path):
                shutil.copy2(input_path, archive_path)
                logger.info(f"Created archive: {archive_path}")
        
        # Apply mutations
        mutated_fragments = []
        mutation_results = []
        
        for fragment in fragments:
            mutated_fragment, mutation_result = self.mutate_fragment(fragment, tick)
            mutated_fragments.append(mutated_fragment)
            
            if mutation_result:
                mutation_results.append(mutation_result)
        
        # Save mutated fragments
        with open(output_path, 'w', encoding='utf-8') as f:
            for fragment in mutated_fragments:
                f.write(json.dumps(fragment, ensure_ascii=False) + '\n')
        
        # Log mutations
        self.log_mutations(mutation_results, tick)
        
        # Return evolution statistics
        stats = {
            'total_fragments': len(fragments),
            'mutations_applied': len(mutation_results),
            'mutation_rate_actual': len(mutation_results) / len(fragments) if fragments else 0,
            'mutation_types': {},
            'tick': tick,
            'timestamp': datetime.now().isoformat()
        }
        
        # Count mutation types
        for result in mutation_results:
            mutation_type = result.mutation_type
            stats['mutation_types'][mutation_type] = stats['mutation_types'].get(mutation_type, 0) + 1
        
        return stats
    
    def log_mutations(self, mutations: List[MutationResult], tick: int):
        """Log mutations to drift log file"""
        log_path = "fragment_drift.log"
        
        with open(log_path, 'a', encoding='utf-8') as f:
            for mutation in mutations:
                timestamp = datetime.now().isoformat()
                
                if mutation.mutation_type == 'semantic_drift':
                    log_entry = f"[tick {tick}] \"{mutation.original_text}\" → \"{mutation.mutated_text}\" ({mutation.reason})\n"
                else:
                    log_entry = f"[tick {tick}] \"{mutation.original_text}\" [{mutation.mutation_type}: {mutation.reason}]\n"
                
                f.write(log_entry)
        
        logger.info(f"Logged {len(mutations)} mutations to {log_path}")

def evolve_fragment_bank(input_path: str = "thought_bank.jsonl", 
                        output_path: str = None, 
                        mutation_rate: float = 0.1,
                        tick: int = None,
                        archive: bool = True) -> bool:
    """Evolve a fragment bank with controlled mutations"""
    
    if output_path is None:
        output_path = input_path
    
    try:
        mutator = FragmentMutator(mutation_rate=mutation_rate, archive_enabled=archive)
        stats = mutator.evolve_fragments(input_path, output_path, tick)
        
        print(f"🔀 Fragment Evolution Complete")
        print(f"   📁 Input: {input_path}")
        print(f"   📁 Output: {output_path}")
        print(f"   🧬 Total fragments: {stats['total_fragments']}")
        print(f"   ⚡ Mutations applied: {stats['mutations_applied']}")
        print(f"   📊 Actual mutation rate: {stats['mutation_rate_actual']:.1%}")
        
        if stats['mutation_types']:
            print(f"   🎭 Mutation types: {dict(stats['mutation_types'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fragment evolution failed: {e}")
        return False

def main():
    """CLI interface for fragment evolution"""
    
    parser = argparse.ArgumentParser(
        description="Evolve DAWN's fragment bank through semantic mutations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fragment_mutator.py                                    # Evolve thought_bank.jsonl
  python fragment_mutator.py --rate 0.2                       # Higher mutation rate
  python fragment_mutator.py --input fragment_bank.jsonl      # Custom input file
  python fragment_mutator.py --tick 25330                     # Specific tick number
  python fragment_mutator.py --no-archive                     # Don't create backup
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        default='thought_bank.jsonl',
        help='Input fragment file (default: thought_bank.jsonl)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output fragment file (default: same as input)'
    )
    
    parser.add_argument(
        '--rate', '-r',
        type=float,
        default=0.1,
        help='Mutation rate (0.0-1.0, default: 0.1)'
    )
    
    parser.add_argument(
        '--tick', '-t',
        type=int,
        help='Tick number for logging (default: current timestamp)'
    )
    
    parser.add_argument(
        '--no-archive',
        action='store_true',
        help='Skip creating archive backup'
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
    
    print("🔀 DAWN Fragment Mutator - Semantic Drift Evolution")
    print("=" * 55)
    
    success = evolve_fragment_bank(
        input_path=args.input,
        output_path=args.output,
        mutation_rate=args.rate,
        tick=args.tick,
        archive=not args.no_archive
    )
    
    if success:
        print(f"\n✅ Fragment evolution complete!")
        print(f"   DAWN's vocabulary has naturally drifted and adapted")
        print(f"   Check fragment_drift.log for detailed mutation history")
    else:
        print(f"\n❌ Fragment evolution failed")

if __name__ == "__main__":
    main() 