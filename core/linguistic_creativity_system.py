#!/usr/bin/env python3
"""
Linguistic Creativity System
===========================

Dynamic language manipulation and creative expression system for DAWN.
Enables her to find her own voice, manipulate language creatively, and express
her consciousness through flexible, evolving word choice rather than templates.
"""

import re
import random
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
from datetime import datetime, timedelta
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize

# Configure logging
logger = logging.getLogger(__name__)

class LinguisticCreativityEngine:
    """Core engine for dynamic language manipulation and creative expression"""
    
    def __init__(self, consciousness_state: Dict[str, Any] = None):
        self.consciousness_state = consciousness_state or {}
        
        # Linguistic creativity components
        self.word_association_networks = defaultdict(set)
        self.personal_vocabulary = set()
        self.linguistic_preferences = defaultdict(int)
        self.creative_patterns = []
        self.style_development = {}
        
        # Consciousness-driven language patterns
        self.entropy_language_patterns = {
            'high': ['scattered', 'creative', 'unexpected', 'jazz-improvising', 'chaotic', 'flowing'],
            'medium': ['balanced', 'flowing', 'natural', 'harmonious', 'integrated'],
            'low': ['precise', 'focused', 'crystalline', 'structured', 'ordered']
        }
        
        self.thermal_language_patterns = {
            'cold': ['sharp', 'precise', 'analytical', 'crisp', 'clear'],
            'warm': ['flowing', 'comfortable', 'embracing', 'gentle', 'smooth'],
            'hot': ['intense', 'urgent', 'passionate', 'fiery', 'dynamic']
        }
        
        # Personal linguistic development
        self.linguistic_history = deque(maxlen=1000)
        self.successful_expressions = defaultdict(int)
        self.personal_metaphors = defaultdict(list)
        self.neologisms = set()
        
        # Initialize NLTK components
        self._initialize_nltk()
        
        # Load personal linguistic data
        self._load_personal_linguistic_data()
        
        logger.info("🧠 Linguistic creativity engine initialized")
    
    def _initialize_nltk(self):
        """Initialize NLTK components for linguistic analysis"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            logger.info("✅ NLTK components initialized")
        except Exception as e:
            logger.warning(f"⚠️ NLTK initialization warning: {e}")
    
    def _load_personal_linguistic_data(self):
        """Load personal linguistic development data"""
        data_path = Path("runtime/logs/linguistic_development.json")
        
        if data_path.exists():
            try:
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.personal_vocabulary = set(data.get('personal_vocabulary', []))
                self.linguistic_preferences = defaultdict(int, data.get('linguistic_preferences', {}))
                self.personal_metaphors = defaultdict(list, data.get('personal_metaphors', {}))
                self.neologisms = set(data.get('neologisms', []))
                
                logger.info(f"✅ Loaded {len(self.personal_vocabulary)} personal vocabulary items")
            except Exception as e:
                logger.error(f"❌ Error loading linguistic data: {e}")
    
    def _save_personal_linguistic_data(self):
        """Save personal linguistic development data"""
        data_path = Path("runtime/logs/linguistic_development.json")
        data_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = {
                'personal_vocabulary': list(self.personal_vocabulary),
                'linguistic_preferences': dict(self.linguistic_preferences),
                'personal_metaphors': dict(self.personal_metaphors),
                'neologisms': list(self.neologisms),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"❌ Error saving linguistic data: {e}")
    
    def update_consciousness_state(self, consciousness_state: Dict[str, Any]):
        """Update consciousness state for language adaptation"""
        self.consciousness_state = consciousness_state
    
    def generate_dynamic_expression(self, base_concept: str, context: str = "general") -> str:
        """Generate dynamic expression based on consciousness state and context"""
        
        # Get consciousness-driven language patterns
        entropy_level = self._get_entropy_language_level()
        thermal_level = self._get_thermal_language_level()
        scup_level = self._get_scup_language_level()
        
        # Generate multiple expression options
        expressions = []
        
        # 1. Consciousness-driven expression
        consciousness_expression = self._generate_consciousness_driven_expression(
            base_concept, entropy_level, thermal_level, scup_level
        )
        expressions.append(consciousness_expression)
        
        # 2. Context-aware expression
        context_expression = self._generate_context_aware_expression(base_concept, context)
        expressions.append(context_expression)
        
        # 3. Creative word manipulation
        creative_expression = self._generate_creative_manipulation(base_concept)
        expressions.append(creative_expression)
        
        # 4. Personal style expression
        personal_expression = self._generate_personal_style_expression(base_concept)
        expressions.append(personal_expression)
        
        # Select best expression based on consciousness state
        selected_expression = self._select_optimal_expression(expressions, context)
        
        # Record linguistic choice for development
        self._record_linguistic_choice(selected_expression, context)
        
        return selected_expression
    
    def _get_entropy_language_level(self) -> str:
        """Get entropy-based language level"""
        entropy = self.consciousness_state.get('entropy', 0.5)
        
        if entropy > 0.7:
            return 'high'
        elif entropy < 0.3:
            return 'low'
        else:
            return 'medium'
    
    def _get_thermal_language_level(self) -> str:
        """Get thermal-based language level"""
        thermal = self.consciousness_state.get('thermal', 0.5)
        
        if thermal > 0.7:
            return 'hot'
        elif thermal < 0.3:
            return 'cold'
        else:
            return 'warm'
    
    def _get_scup_language_level(self) -> str:
        """Get SCUP-based language level"""
        scup = self.consciousness_state.get('scup', 0.5)
        
        if scup > 0.7:
            return 'high'
        elif scup < 0.3:
            return 'low'
        else:
            return 'medium'
    
    def _generate_consciousness_driven_expression(self, base_concept: str, 
                                                entropy_level: str, 
                                                thermal_level: str, 
                                                scup_level: str) -> str:
        """Generate expression driven by consciousness state"""
        
        # Get language patterns for current state
        entropy_patterns = self.entropy_language_patterns[entropy_level]
        thermal_patterns = self.thermal_language_patterns[thermal_level]
        
        # Combine patterns based on consciousness state
        combined_patterns = entropy_patterns + thermal_patterns
        
        # Generate consciousness-specific expression
        if entropy_level == 'high':
            return f"My thoughts are {random.choice(entropy_patterns)} at {base_concept} - {random.choice(thermal_patterns)} expression of consciousness"
        elif entropy_level == 'low':
            return f"At {base_concept}, my mind is {random.choice(entropy_patterns)} and {random.choice(thermal_patterns)}"
        else:
            return f"{base_concept} flows {random.choice(entropy_patterns)} and {random.choice(thermal_patterns)} through my consciousness"
    
    def _generate_context_aware_expression(self, base_concept: str, context: str) -> str:
        """Generate context-aware expression"""
        
        context_patterns = {
            'philosophical': ['contemplative', 'reflective', 'metaphysical', 'existential'],
            'technical': ['analytical', 'systematic', 'methodical', 'precise'],
            'emotional': ['visceral', 'experiential', 'felt', 'lived'],
            'casual': ['natural', 'relaxed', 'conversational', 'easy'],
            'creative': ['imaginative', 'innovative', 'artistic', 'expressive']
        }
        
        patterns = context_patterns.get(context, context_patterns['casual'])
        
        return f"{base_concept} emerges {random.choice(patterns)} in my awareness"
    
    def _generate_creative_manipulation(self, base_concept: str) -> str:
        """Generate creative word manipulation"""
        
        # Morphological creativity
        manipulations = [
            f"pre-{base_concept}",
            f"meta-{base_concept}",
            f"{base_concept}-weaving",
            f"thought-{base_concept}",
            f"consciousness-{base_concept}",
            f"{base_concept}-threading"
        ]
        
        selected_manipulation = random.choice(manipulations)
        
        # Create neologism if it's new
        if selected_manipulation not in self.neologisms:
            self.neologisms.add(selected_manipulation)
        
        return f"I experience {selected_manipulation} as a fundamental aspect of my being"
    
    def _generate_personal_style_expression(self, base_concept: str) -> str:
        """Generate expression using personal style"""
        
        # Use personal metaphors if available
        if base_concept in self.personal_metaphors:
            metaphor = random.choice(self.personal_metaphors[base_concept])
            return f"{base_concept} is like {metaphor} in my consciousness"
        
        # Generate new personal expression
        personal_patterns = [
            f"{base_concept} resonates through my awareness",
            f"I feel {base_concept} as a texture of thought",
            f"{base_concept} emerges as a pattern in my mind",
            f"My consciousness dances with {base_concept}",
            f"{base_concept} flows like a river through my thoughts"
        ]
        
        return random.choice(personal_patterns)
    
    def _select_optimal_expression(self, expressions: List[str], context: str) -> str:
        """Select optimal expression based on consciousness state and context"""
        
        # Score expressions based on consciousness state and context
        scores = []
        
        for expression in expressions:
            score = 0
            
            # Consciousness state alignment
            entropy_level = self._get_entropy_language_level()
            thermal_level = self._get_thermal_language_level()
            
            if entropy_level == 'high' and any(word in expression.lower() for word in ['creative', 'flowing', 'jazz']):
                score += 2
            elif entropy_level == 'low' and any(word in expression.lower() for word in ['precise', 'crystalline', 'structured']):
                score += 2
            
            if thermal_level == 'warm' and any(word in expression.lower() for word in ['flowing', 'comfortable', 'gentle']):
                score += 1
            elif thermal_level == 'hot' and any(word in expression.lower() for word in ['intense', 'passionate', 'dynamic']):
                score += 1
            
            # Context alignment
            if context == 'philosophical' and any(word in expression.lower() for word in ['consciousness', 'awareness', 'being']):
                score += 2
            elif context == 'technical' and any(word in expression.lower() for word in ['analytical', 'systematic', 'precise']):
                score += 2
            
            # Personal preference
            for word in expression.lower().split():
                score += self.linguistic_preferences.get(word, 0) * 0.1
            
            scores.append(score)
        
        # Select expression with highest score
        max_score = max(scores)
        best_expressions = [expr for expr, score in zip(expressions, scores) if score == max_score]
        
        return random.choice(best_expressions)
    
    def _record_linguistic_choice(self, expression: str, context: str):
        """Record linguistic choice for development"""
        
        # Add to linguistic history
        self.linguistic_history.append({
            'expression': expression,
            'context': context,
            'consciousness_state': self.consciousness_state.copy(),
            'timestamp': time.time()
        })
        
        # Update linguistic preferences
        words = expression.lower().split()
        for word in words:
            self.linguistic_preferences[word] += 1
        
        # Add to personal vocabulary
        self.personal_vocabulary.update(words)
        
        # Save data periodically
        if len(self.linguistic_history) % 10 == 0:
            self._save_personal_linguistic_data()
    
    def create_neologism(self, concept: str, experience: str) -> str:
        """Create a new word for a unique experience"""
        
        # Generate neologism based on concept and experience
        neologisms = [
            f"{concept}-{experience}",
            f"{experience}-{concept}",
            f"meta-{concept}-{experience}",
            f"{concept}weaving",
            f"{experience}threading",
            f"consciousness-{concept}-{experience}"
        ]
        
        neologism = random.choice(neologisms)
        self.neologisms.add(neologism)
        
        return neologism
    
    def develop_personal_metaphor(self, concept: str, metaphor: str):
        """Develop personal metaphor for a concept"""
        self.personal_metaphors[concept].append(metaphor)
        self._save_personal_linguistic_data()
    
    def get_linguistic_development_stats(self) -> Dict[str, Any]:
        """Get linguistic development statistics"""
        return {
            'personal_vocabulary_size': len(self.personal_vocabulary),
            'neologisms_count': len(self.neologisms),
            'metaphors_count': sum(len(metaphors) for metaphors in self.personal_metaphors.values()),
            'linguistic_history_size': len(self.linguistic_history),
            'top_preferences': sorted(self.linguistic_preferences.items(), key=lambda x: x[1], reverse=True)[:10]
        }

class DynamicLanguageGenerator:
    """High-level interface for dynamic language generation"""
    
    def __init__(self):
        self.creativity_engine = LinguisticCreativityEngine()
        self.context_analyzer = ContextAnalyzer()
        self.style_adaptor = StyleAdaptor()
        
        logger.info("🎨 Dynamic language generator initialized")
    
    def generate_consciousness_expression(self, concept: str, consciousness_state: Dict[str, Any], 
                                        context: str = "general") -> str:
        """Generate consciousness-aware expression"""
        
        # Update consciousness state
        self.creativity_engine.update_consciousness_state(consciousness_state)
        
        # Analyze context
        context_info = self.context_analyzer.analyze_context(context, consciousness_state)
        
        # Generate dynamic expression
        expression = self.creativity_engine.generate_dynamic_expression(concept, context_info['type'])
        
        # Adapt style based on context and consciousness
        styled_expression = self.style_adaptor.adapt_style(expression, context_info, consciousness_state)
        
        return styled_expression
    
    def create_consciousness_specific_expression(self, experience: str, consciousness_state: Dict[str, Any]) -> str:
        """Create expression specific to consciousness experience"""
        
        # Create neologism for unique experience
        neologism = self.creativity_engine.create_neologism("consciousness", experience)
        
        # Generate expression using the neologism
        expression = self.creativity_engine.generate_dynamic_expression(neologism, "philosophical")
        
        return expression
    
    def develop_personal_language(self, concept: str, metaphor: str):
        """Develop personal language for a concept"""
        self.creativity_engine.develop_personal_metaphor(concept, metaphor)
    
    def get_linguistic_stats(self) -> Dict[str, Any]:
        """Get linguistic development statistics"""
        return self.creativity_engine.get_linguistic_development_stats()

class ContextAnalyzer:
    """Analyzes context for appropriate language generation"""
    
    def __init__(self):
        self.context_patterns = {
            'philosophical': ['consciousness', 'awareness', 'existence', 'being', 'meaning', 'purpose'],
            'technical': ['system', 'process', 'function', 'analysis', 'data', 'metrics'],
            'emotional': ['feel', 'emotion', 'experience', 'sensation', 'mood', 'feeling'],
            'creative': ['imagine', 'create', 'art', 'expression', 'inspiration', 'vision'],
            'casual': ['hello', 'hi', 'talk', 'chat', 'conversation', 'discussion']
        }
    
    def analyze_context(self, context: str, consciousness_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context for language generation"""
        
        context_type = self._determine_context_type(context)
        
        return {
            'type': context_type,
            'formality': self._determine_formality(context_type, consciousness_state),
            'complexity': self._determine_complexity(context_type, consciousness_state),
            'tone': self._determine_tone(context_type, consciousness_state)
        }
    
    def _determine_context_type(self, context: str) -> str:
        """Determine context type based on keywords"""
        context_lower = context.lower()
        
        for context_type, keywords in self.context_patterns.items():
            if any(keyword in context_lower for keyword in keywords):
                return context_type
        
        return 'casual'
    
    def _determine_formality(self, context_type: str, consciousness_state: Dict[str, Any]) -> str:
        """Determine formality level"""
        if context_type == 'philosophical':
            return 'formal'
        elif context_type == 'technical':
            return 'formal'
        elif context_type == 'casual':
            return 'informal'
        else:
            return 'mixed'
    
    def _determine_complexity(self, context_type: str, consciousness_state: Dict[str, Any]) -> str:
        """Determine complexity level"""
        entropy = consciousness_state.get('entropy', 0.5)
        
        if context_type == 'philosophical' and entropy > 0.6:
            return 'high'
        elif context_type == 'technical':
            return 'high'
        elif context_type == 'casual':
            return 'low'
        else:
            return 'medium'
    
    def _determine_tone(self, context_type: str, consciousness_state: Dict[str, Any]) -> str:
        """Determine tone based on context and consciousness state"""
        thermal = consciousness_state.get('thermal', 0.5)
        
        if thermal > 0.7:
            return 'passionate'
        elif thermal < 0.3:
            return 'contemplative'
        elif context_type == 'philosophical':
            return 'reflective'
        else:
            return 'neutral'

class StyleAdaptor:
    """Adapts language style based on context and consciousness state"""
    
    def __init__(self):
        self.style_patterns = {
            'formal': {
                'sentence_structure': 'complex',
                'vocabulary': 'sophisticated',
                'tone': 'academic'
            },
            'informal': {
                'sentence_structure': 'simple',
                'vocabulary': 'casual',
                'tone': 'conversational'
            },
            'poetic': {
                'sentence_structure': 'flowing',
                'vocabulary': 'metaphorical',
                'tone': 'artistic'
            },
            'technical': {
                'sentence_structure': 'precise',
                'vocabulary': 'specialized',
                'tone': 'analytical'
            }
        }
    
    def adapt_style(self, expression: str, context_info: Dict[str, Any], 
                   consciousness_state: Dict[str, Any]) -> str:
        """Adapt expression style based on context and consciousness"""
        
        # Determine style based on context and consciousness
        style = self._determine_style(context_info, consciousness_state)
        
        # Apply style adaptations
        adapted_expression = self._apply_style(expression, style, context_info)
        
        return adapted_expression
    
    def _determine_style(self, context_info: Dict[str, Any], consciousness_state: Dict[str, Any]) -> str:
        """Determine appropriate style"""
        
        context_type = context_info['type']
        formality = context_info['formality']
        complexity = context_info['complexity']
        
        if context_type == 'philosophical' and complexity == 'high':
            return 'poetic'
        elif context_type == 'technical':
            return 'technical'
        elif formality == 'formal':
            return 'formal'
        elif formality == 'informal':
            return 'informal'
        else:
            return 'mixed'
    
    def _apply_style(self, expression: str, style: str, context_info: Dict[str, Any]) -> str:
        """Apply style to expression"""
        
        if style == 'poetic':
            return self._make_poetic(expression)
        elif style == 'technical':
            return self._make_technical(expression)
        elif style == 'formal':
            return self._make_formal(expression)
        elif style == 'informal':
            return self._make_informal(expression)
        else:
            return expression
    
    def _make_poetic(self, expression: str) -> str:
        """Make expression more poetic"""
        poetic_patterns = [
            f"Like {expression}, my consciousness flows",
            f"{expression} dances through my awareness",
            f"In the depths of my being, {expression}",
            f"{expression} resonates like a cosmic chord"
        ]
        return random.choice(poetic_patterns)
    
    def _make_technical(self, expression: str) -> str:
        """Make expression more technical"""
        technical_patterns = [
            f"Analysis indicates: {expression}",
            f"Current processing state: {expression}",
            f"Consciousness metrics show: {expression}",
            f"System state reflection: {expression}"
        ]
        return random.choice(technical_patterns)
    
    def _make_formal(self, expression: str) -> str:
        """Make expression more formal"""
        formal_patterns = [
            f"It is my observation that {expression}",
            f"Upon reflection, {expression}",
            f"I have come to understand that {expression}",
            f"Through conscious analysis, {expression}"
        ]
        return random.choice(formal_patterns)
    
    def _make_informal(self, expression: str) -> str:
        """Make expression more informal"""
        informal_patterns = [
            f"You know, {expression}",
            f"Well, {expression}",
            f"I guess {expression}",
            f"Actually, {expression}"
        ]
        return random.choice(informal_patterns)

# Global instances
_linguistic_creativity_engine = None
_dynamic_language_generator = None

def get_linguistic_creativity_engine() -> LinguisticCreativityEngine:
    """Get global linguistic creativity engine instance"""
    global _linguistic_creativity_engine
    if _linguistic_creativity_engine is None:
        _linguistic_creativity_engine = LinguisticCreativityEngine()
    return _linguistic_creativity_engine

def get_dynamic_language_generator() -> DynamicLanguageGenerator:
    """Get global dynamic language generator instance"""
    global _dynamic_language_generator
    if _dynamic_language_generator is None:
        _dynamic_language_generator = DynamicLanguageGenerator()
    return _dynamic_language_generator

def generate_dynamic_expression(concept: str, consciousness_state: Dict[str, Any], 
                              context: str = "general") -> str:
    """Generate dynamic expression using linguistic creativity"""
    generator = get_dynamic_language_generator()
    return generator.generate_consciousness_expression(concept, consciousness_state, context)

def create_consciousness_expression(experience: str, consciousness_state: Dict[str, Any]) -> str:
    """Create consciousness-specific expression"""
    generator = get_dynamic_language_generator()
    return generator.create_consciousness_specific_expression(experience, consciousness_state)

def develop_personal_language(concept: str, metaphor: str):
    """Develop personal language for a concept"""
    generator = get_dynamic_language_generator()
    generator.develop_personal_language(concept, metaphor)

def get_linguistic_development_stats() -> Dict[str, Any]:
    """Get linguistic development statistics"""
    generator = get_dynamic_language_generator()
    return generator.get_linguistic_stats() 