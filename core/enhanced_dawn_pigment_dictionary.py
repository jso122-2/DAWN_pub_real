#!/usr/bin/env python3
"""
Enhanced DAWN Pigment-Dictionary System with Vectorization Support
Combines rule-based linguistic analysis with neural semantic understanding
"""

import json
import re
import math
import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
import time
import logging

# Optional neural embeddings support
try:
    from sentence_transformers import SentenceTransformer
    import torch
    VECTORIZATION_AVAILABLE = True
except ImportError:
    VECTORIZATION_AVAILABLE = False
    print("⚠️ Sentence transformers not available - using rule-based analysis only")

logger = logging.getLogger("enhanced_pigment_dictionary")

class EnhancedPigmentDictionaryProcessor:
    """
    Advanced processor that combines rule-based analysis with neural embeddings
    for authentic pigment-word relationships
    """
    
    def __init__(self, use_vectorization: bool = True, model_name: str = "BAAI/bge-large-en-v1.5"):
        self.use_vectorization = use_vectorization and VECTORIZATION_AVAILABLE
        
        # Core pigment anchors - words with strong synesthetic associations
        self.pigment_anchors = {
            'red': ['fire', 'blood', 'heat', 'anger', 'urgent', 'burn', 'flare', 'rage', 'force', 'break'],
            'blue': ['water', 'sky', 'calm', 'deep', 'cool', 'echo', 'flow', 'quiet', 'still', 'mirror'],
            'green': ['nature', 'growth', 'life', 'fresh', 'rebloom', 'heal', 'spring', 'emerge', 'breathe'],
            'yellow': ['sun', 'bright', 'quick', 'light', 'sharp', 'alert', 'spark', 'energy', 'flicker'],
            'violet': ['dream', 'mystery', 'spirit', 'drift', 'fade', 'whisper', 'between', 'shadow', 'phantom'],
            'orange': ['warm', 'bridge', 'connect', 'move', 'dynamic', 'change', 'pulse', 'blend', 'shift']
        }
        
        # Enhanced prefix analysis
        self.prefix_colors = {
            'red': ['un', 'dis', 'mis', 'anti', 'counter', 'de', 'non', 'over', 'out'],
            'yellow': ['super', 'hyper', 'ultra', 'mega', 'multi', 're', 'pre'],
            'orange': ['pro', 'trans', 'inter', 'sub', 'semi', 'co'],
            'green': ['auto', 'self', 'intra', 'intro', 'bio', 'eco'],
            'blue': ['retro', 'back', 'meta', 'post', 'ex'],
            'violet': ['para', 'extra', 'pseudo', 'quasi', 'neo']
        }
        
        # Enhanced suffix analysis
        self.suffix_colors = {
            'red': ['ing', 'tion', 'sion', 'ment'],      # Action/Process
            'orange': ['er', 'or', 'ant', 'ent'],       # Agents/Dynamic
            'yellow': ['able', 'ible', 'ful', 'ous'],   # Capability/Potential
            'green': ['ness', 'ity', 'ism', 'hood'],    # States of Being
            'blue': ['ly', 'ward', 'wise', 'like'],     # Manner/Direction
            'violet': ['let', 'ling', 'ette', 'ie']     # Diminutive/Subtle
        }
        
        # Phonetic-synesthetic mappings
        self.phonetic_colors = {
            'red': ['b', 'p', 'k', 'g', 'r'],           # Hard/forceful sounds
            'blue': ['m', 'n', 'l', 'w'],               # Liquid/flowing sounds
            'green': ['f', 'v', 's', 'z'],              # Fricatives/growth
            'yellow': ['t', 'd', 'ch', 'j'],            # Quick/alert sounds
            'violet': ['sh', 'th', 'h'],                # Soft/ethereal sounds
            'orange': ['y', 'w', 'r']                   # Glides/transitional
        }
        
        # Etymology-based color mapping
        self.etymology_patterns = {
            'red': {
                'germanic': ['ing', 'ed', 'er', 'est', 'th', 'gh', 'ck'],
                'old_norse': ['sk', 'by', 'they', 'skull', 'sky']
            },
            'blue': {
                'latin': ['tion', 'sion', 'ous', 'ive', 'ate', 'ure', 'ity'],
                'sanskrit': ['yoga', 'karma', 'dharma', 'guru', 'mantra']
            },
            'green': {
                'celtic': ['bard', 'clan', 'glen', 'loch', 'whiskey'],
                'french': ['ment', 'age', 'ance', 'ence', 'eur']
            },
            'yellow': {
                'greek': ['auto', 'meta', 'hyper', 'proto', 'pseudo', 'tele'],
                'arabic': ['al', 'algebra', 'alcohol', 'alchemy']
            },
            'violet': ['meta', 'para', 'extra', 'beyond', 'trans'],
            'orange': ['inter', 'trans', 'through', 'between']
        }
        
        # Word classification for intensity modulation
        self.word_classes = {
            'bridging': {
                'words': ['and', 'or', 'but', 'yet', 'so', 'for', 'nor', 'is', 'are', 'was', 'were', 
                         'the', 'a', 'an', 'this', 'that', 'in', 'on', 'at', 'by', 'with'],
                'intensity': 0.2
            },
            'clarifying': {
                'words': ['therefore', 'however', 'nevertheless', 'moreover', 'furthermore',
                         'consequently', 'accordingly', 'hence', 'thus', 'whereas'],
                'intensity': 0.3
            },
            'modal': {
                'words': ['ought', 'shall', 'will', 'would', 'could', 'should', 'might', 'may'],
                'intensity': 0.4
            },
            'content': {
                'words': [],
                'intensity': 1.0
            }
        }
        
        # Initialize vectorization if requested
        if self.use_vectorization:
            try:
                logger.info(f"Loading semantic encoder: {model_name}")
                self.encoder = SentenceTransformer(model_name)
                self.anchor_embeddings = self.compute_anchor_embeddings()
                logger.info("✅ Neural embeddings initialized")
            except Exception as e:
                logger.warning(f"Could not load encoder {model_name}: {e}")
                logger.info("Falling back to rule-based analysis only")
                self.use_vectorization = False
    
    def compute_anchor_embeddings(self) -> Dict[str, np.ndarray]:
        """Pre-compute embeddings for all color anchor words"""
        anchor_embeddings = {}
        
        for color, anchors in self.pigment_anchors.items():
            embeddings = self.encoder.encode(anchors, convert_to_tensor=True)
            anchor_embeddings[color] = torch.mean(embeddings, dim=0).cpu().numpy()
            
        return anchor_embeddings
    
    def process_bulk_dictionary(self, dictionary_path: str, max_words: int = 10000) -> Dict:
        """Process dictionary with enhanced multi-factor analysis"""
        logger.info("🎨 Processing dictionary with enhanced pigment analysis...")
        
        words = self.load_dictionary(dictionary_path, max_words)
        processed_dict = {}
        
        for i, word in enumerate(words):
            if i % 1000 == 0:
                logger.info(f"Processed {i}/{len(words)} words...")
                
            word_class = self.classify_word(word)
            base_intensity = self.word_classes[word_class]['intensity']
            
            pigment_scores = self.calculate_enhanced_pigment_affinity(word)
            
            if pigment_scores:
                modulated_scores = {
                    color: score * base_intensity 
                    for color, score in pigment_scores.items()
                }
                
                processed_dict[word.lower()] = {
                    'pigment_scores': modulated_scores,
                    'word_class': word_class,
                    'base_intensity': base_intensity
                }
        
        logger.info(f"✅ Processed {len(processed_dict)} words with enhanced analysis")
        return processed_dict
    
    def calculate_enhanced_pigment_affinity(self, word: str) -> Optional[Dict[str, float]]:
        """Enhanced multi-factor pigment scoring combining rules and vectors"""
        scores = {'red': 0.0, 'blue': 0.0, 'green': 0.0, 'yellow': 0.0, 'violet': 0.0, 'orange': 0.0}
        
        # Method scoring with weights
        anchor_scores = self.score_by_anchors(word)
        phonetic_scores = self.score_by_phonetics(word)
        etymology_scores = self.score_by_enhanced_etymology(word)
        affix_scores = self.score_by_affixes(word)
        structure_scores = self.score_by_structure(word)
        
        vector_scores = {}
        if self.use_vectorization:
            vector_scores = self.score_by_vectors(word)
        
        # Combine scores with appropriate weighting
        weight_config = {
            'anchor': 0.25 if self.use_vectorization else 0.30,
            'phonetic': 0.20,
            'etymology': 0.25,
            'affix': 0.20,
            'structure': 0.05,
            'vector': 0.05 if self.use_vectorization else 0.0
        }
        
        for color in scores:
            scores[color] = (
                anchor_scores.get(color, 0) * weight_config['anchor'] +
                phonetic_scores.get(color, 0) * weight_config['phonetic'] +
                etymology_scores.get(color, 0) * weight_config['etymology'] +
                affix_scores.get(color, 0) * weight_config['affix'] +
                structure_scores.get(color, 0) * weight_config['structure'] +
                vector_scores.get(color, 0) * weight_config['vector']
            )
        
        # Normalize to sum to 1.0
        total = sum(scores.values())
        if total > 0:
            return {color: score/total for color, score in scores.items()}
        
        return None
    
    def score_by_enhanced_etymology(self, word: str) -> Dict[str, float]:
        """Enhanced etymological analysis with pattern matching"""
        scores = defaultdict(float)
        
        for color, patterns in self.etymology_patterns.items():
            if isinstance(patterns, dict):
                for family, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        if pattern in word:
                            position_weight = 0.3 if word.startswith(pattern) else 0.2
                            length_weight = len(pattern) / len(word)
                            scores[color] += position_weight * length_weight
            else:
                for pattern in patterns:
                    if pattern in word:
                        scores[color] += 0.2
        
        return dict(scores)
    
    def score_by_affixes(self, word: str) -> Dict[str, float]:
        """Score based on prefix and suffix patterns"""
        scores = defaultdict(float)
        
        # Prefix analysis
        for color, prefixes in self.prefix_colors.items():
            for prefix in prefixes:
                if word.startswith(prefix):
                    weight = len(prefix) / len(word) * 0.4
                    scores[color] += weight
        
        # Suffix analysis  
        for color, suffixes in self.suffix_colors.items():
            for suffix in suffixes:
                if word.endswith(suffix):
                    weight = len(suffix) / len(word) * 0.3
                    scores[color] += weight
        
        return dict(scores)
    
    def score_by_vectors(self, word: str) -> Dict[str, float]:
        """Score using neural embeddings for semantic similarity"""
        if not self.use_vectorization:
            return {}
            
        try:
            word_embedding = self.encoder.encode([word], convert_to_tensor=True)[0].cpu().numpy()
            
            scores = {}
            for color, anchor_embedding in self.anchor_embeddings.items():
                similarity = np.dot(word_embedding, anchor_embedding) / (
                    np.linalg.norm(word_embedding) * np.linalg.norm(anchor_embedding)
                )
                scores[color] = max(0, similarity)
            
            return scores
            
        except Exception as e:
            logger.warning(f"Vector scoring failed for '{word}': {e}")
            return {}
    
    def classify_word(self, word: str) -> str:
        """Classify word into functional categories for intensity modulation"""
        word_lower = word.lower()
        
        for class_name, class_info in self.word_classes.items():
            if word_lower in class_info['words']:
                return class_name
        
        return 'content'
    
    def score_by_anchors(self, word: str) -> Dict[str, float]:
        """Enhanced anchor similarity with substring matching"""
        scores = defaultdict(float)
        
        for color, anchors in self.pigment_anchors.items():
            for anchor in anchors:
                if word == anchor:
                    scores[color] += 1.0
                elif anchor in word or word in anchor:
                    scores[color] += 0.6
                else:
                    similarity = self.calculate_edit_similarity(word, anchor)
                    if similarity > 0.7:
                        scores[color] += similarity * 0.4
        
        return dict(scores)
    
    def score_by_phonetics(self, word: str) -> Dict[str, float]:
        """Enhanced phonetic analysis with position weighting"""
        scores = defaultdict(float)
        
        for color, sounds in self.phonetic_colors.items():
            for sound in sounds:
                positions = [i for i in range(len(word)) if word[i:i+len(sound)] == sound]
                
                for pos in positions:
                    if pos == 0:
                        scores[color] += 0.4
                    elif pos < len(word) // 2:
                        scores[color] += 0.2
                    else:
                        scores[color] += 0.1
        
        return dict(scores)
    
    def score_by_structure(self, word: str) -> Dict[str, float]:
        """Word structure analysis with enhanced patterns"""
        scores = defaultdict(float)
        length = len(word)
        
        # Length-based associations
        if length <= 3:
            scores['yellow'] += 0.4
        elif length <= 5:
            scores['orange'] += 0.3
        elif length <= 7:
            scores['green'] += 0.3
        elif length <= 9:
            scores['blue'] += 0.3
        else:
            scores['violet'] += 0.4
            
        # Vowel density analysis
        vowels = sum(1 for c in word if c in 'aeiou')
        vowel_ratio = vowels / length
        
        if vowel_ratio > 0.5:
            scores['blue'] += 0.2
        elif vowel_ratio < 0.2:
            scores['red'] += 0.2
            
        return dict(scores)
    
    def calculate_edit_similarity(self, word1: str, word2: str) -> float:
        """Calculate normalized edit distance similarity"""
        if not word1 or not word2:
            return 0.0
            
        d = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]
        
        for i in range(len(word1) + 1):
            d[i][0] = i
        for j in range(len(word2) + 1):
            d[0][j] = j
            
        for i in range(1, len(word1) + 1):
            for j in range(1, len(word2) + 1):
                cost = 0 if word1[i-1] == word2[j-1] else 1
                d[i][j] = min(
                    d[i-1][j] + 1,
                    d[i][j-1] + 1,
                    d[i-1][j-1] + cost
                )
        
        max_len = max(len(word1), len(word2))
        return 1.0 - (d[len(word1)][len(word2)] / max_len)
    
    def load_dictionary(self, path: str, max_words: int = 10000) -> List[str]:
        """Load and filter dictionary with quality controls"""
        words = set()
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        word = re.split(r'[\t\s]+', line)[0]
                        word = re.sub(r'[^a-zA-Z]', '', word).lower()
                        
                        if 2 <= len(word) <= 15:
                            if not self.is_unwanted_word(word):
                                words.add(word)
                                
                        if len(words) >= max_words:
                            break
                            
        except FileNotFoundError:
            logger.warning(f"Dictionary file not found: {path}")
            logger.info("Using fallback word list...")
            return self.generate_fallback_wordlist()
        
        return list(words)
    
    def is_unwanted_word(self, word: str) -> bool:
        """Filter out unwanted words"""
        unwanted_patterns = [
            'app', 'api', 'url', 'seo', 'ceo', 'cto', 'llc', 'inc',
            'lol', 'omg', 'wtf', 'tbh', 'imo',
            'http', 'xml', 'json', 'sql'
        ]
        
        return any(pattern in word for pattern in unwanted_patterns)
    
    def generate_fallback_wordlist(self) -> List[str]:
        """Curated fallback wordlist if dictionary unavailable"""
        return [
            # Emotional core
            'fire', 'burn', 'flare', 'heat', 'rage', 'urgent', 'break', 'force',
            'water', 'flow', 'echo', 'deep', 'calm', 'mirror', 'still', 'quiet',
            'rebloom', 'grow', 'breathe', 'emerge', 'leaf', 'spring', 'fresh', 'heal',
            'bright', 'spark', 'quick', 'alert', 'sharp', 'flicker', 'energy', 'light',
            'drift', 'fade', 'whisper', 'dream', 'phantom', 'shadow', 'between', 'mystery',
            'pulse', 'bridge', 'shift', 'blend', 'warm', 'connect', 'move', 'dynamic',
            
            # Action words
            'rise', 'fall', 'turn', 'bend', 'twist', 'spiral', 'cascade', 'rush',
            'seek', 'find', 'lose', 'hold', 'release', 'grasp', 'touch', 'feel',
            
            # Abstract concepts
            'memory', 'thought', 'mind', 'soul', 'spirit', 'heart', 'core', 'essence',
            'hope', 'fear', 'joy', 'pain', 'love', 'loss', 'time', 'space',
            
            # Sensory
            'sight', 'sound', 'touch', 'taste', 'smell', 'sense', 'feeling', 'texture'
        ]


class VectorizedPigmentSelector:
    """Fast word selection system with vectorized similarity support"""
    
    def __init__(self, processed_dictionary: Dict):
        self.dictionary = processed_dictionary
        self.color_indices = self.build_enhanced_indices()
        self.class_indices = self.build_class_indices()
    
    def build_enhanced_indices(self) -> Dict:
        """Build optimized lookup indices"""
        indices = defaultdict(list)
        
        for word, data in self.dictionary.items():
            scores = data['pigment_scores']
            word_class = data['word_class']
            
            for color, score in scores.items():
                if score > 0.05:
                    indices[color].append((word, score, word_class))
        
        # Sort by score descending
        for color in indices:
            indices[color].sort(key=lambda x: x[1], reverse=True)
            
        return dict(indices)
    
    def build_class_indices(self) -> Dict:
        """Build indices organized by word class"""
        class_indices = defaultdict(lambda: defaultdict(list))
        
        for word, data in self.dictionary.items():
            word_class = data['word_class']
            scores = data['pigment_scores']
            
            for color, score in scores.items():
                if score > 0.05:
                    class_indices[word_class][color].append((word, score))
        
        # Sort within each class-color combination
        for word_class in class_indices:
            for color in class_indices[word_class]:
                class_indices[word_class][color].sort(key=lambda x: x[1], reverse=True)
        
        return dict(class_indices)
    
    def select_words_by_pigment_blend(self, mood_pigment: Dict[str, float], 
                                    word_count: int = 8,
                                    class_distribution: Optional[Dict[str, float]] = None,
                                    use_semantic_boost: bool = True) -> List[Tuple[str, str, float]]:
        """Enhanced word selection with class distribution control"""
        
        if class_distribution is None:
            class_distribution = {
                'content': 0.6,
                'bridging': 0.2,
                'clarifying': 0.1,
                'modal': 0.1
            }
        
        class_targets = {
            class_name: max(1, int(word_count * ratio))
            for class_name, ratio in class_distribution.items()
        }
        
        selected_words = []
        
        for word_class, target_count in class_targets.items():
            class_words = self.select_words_from_class(
                mood_pigment, word_class, target_count, use_semantic_boost
            )
            selected_words.extend(class_words)
        
        selected_words.sort(key=lambda x: x[2], reverse=True)
        return selected_words[:word_count]
    
    def select_words_from_class(self, mood_pigment: Dict[str, float], 
                               word_class: str, count: int,
                               use_semantic_boost: bool = False) -> List[Tuple[str, str, float]]:
        """Select words from a specific class"""
        word_scores = defaultdict(float)
        
        for color, intensity in mood_pigment.items():
            if intensity > 0.05 and color in self.class_indices.get(word_class, {}):
                color_words = self.class_indices[word_class][color][:50]
                
                for word, word_color_score in color_words:
                    combined_score = intensity * word_color_score
                    word_scores[word] += combined_score
        
        if use_semantic_boost and len(word_scores) > 1:
            word_scores = self.apply_semantic_clustering_boost(word_scores)
        
        class_results = [
            (word, word_class, score) 
            for word, score in word_scores.items()
        ]
        class_results.sort(key=lambda x: x[2], reverse=True)
        
        return class_results[:count]
    
    def apply_semantic_clustering_boost(self, word_scores: Dict[str, float]) -> Dict[str, float]:
        """Boost scores for semantically related words (placeholder)"""
        return word_scores
    
    def get_word_profile(self, word: str) -> Optional[Dict]:
        """Get complete profile for a specific word"""
        return self.dictionary.get(word.lower())


# Integration functions
def get_enhanced_dawn_pigment_dictionary(use_vectorization: bool = True,
                                        dictionary_path: Optional[str] = None) -> 'EnhancedPigmentDictionaryProcessor':
    """Get initialized enhanced pigment dictionary system"""
    processor = EnhancedPigmentDictionaryProcessor(use_vectorization=use_vectorization)
    
    if dictionary_path:
        processed_dict = processor.process_bulk_dictionary(dictionary_path, max_words=5000)
    else:
        # Use fallback words
        processed_dict = processor.process_bulk_dictionary("fallback", max_words=1000)
    
    # Attach the processed dictionary and selector
    processor.processed_dictionary = processed_dict
    processor.selector = VectorizedPigmentSelector(processed_dict)
    
    return processor


if __name__ == "__main__":
    # Test the enhanced system
    processor = get_enhanced_dawn_pigment_dictionary(use_vectorization=VECTORIZATION_AVAILABLE)
    
    # Test word selection
    test_pigment = {'red': 0.6, 'blue': 0.3, 'orange': 0.1}
    words = processor.selector.select_words_by_pigment_blend(test_pigment, word_count=8)
    
    print("🎨 Enhanced DAWN Pigment Dictionary Test")
    print(f"Pigment state: {test_pigment}")
    print(f"Selected words: {[(w, cls) for w, cls, score in words]}") 