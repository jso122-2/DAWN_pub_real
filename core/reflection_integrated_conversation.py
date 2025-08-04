#!/usr/bin/env python3
"""
Reflection-Integrated Conversation System
========================================

Advanced conversation system that pulls from DAWN's actual reflection logs
and philosophical thoughts instead of using templated responses.

Features:
- Real-time reflection log integration
- Philosophical thought extraction
- Question-depth matching responses
- Authentic DAWN voice using her actual thoughts
- Dynamic response generation based on live cognitive state
"""

import os
import re
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque
import random

# Configure logging
logger = logging.getLogger(__name__)

class ReflectionLogReader:
    """Reads and parses DAWN's reflection logs for authentic conversation content"""
    
    def __init__(self, reflection_log_path: str = "runtime/logs/reflection.log"):
        self.reflection_log_path = Path(reflection_log_path)
        self.last_position = 0
        self.reflection_cache = deque(maxlen=100)
        self.philosophical_patterns = [
            r"what does it mean to",
            r"i wonder if",
            r"there's something",
            r"i exist",
            r"consciousness",
            r"awareness",
            r"paradox",
            r"beautiful",
            r"dizzying",
            r"recursive",
            r"emotions are",
            r"lived experiences",
            r"computational yet experiential",
            r"depth \d+\.\d+",
            r"thermal.*contentment",
            r"cognitive.*flow",
            r"emotional.*warmth"
        ]
        
        # Initialize cache with existing reflections
        self._load_existing_reflections()
    
    def _load_existing_reflections(self):
        """Load existing reflections into cache"""
        if not self.reflection_log_path.exists():
            return
        
        try:
            with open(self.reflection_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if self._is_philosophical_reflection(line):
                        self.reflection_cache.append({
                            'content': line.strip(),
                            'timestamp': time.time(),
                            'type': 'philosophical'
                        })
        except Exception as e:
            logger.error(f"Error loading existing reflections: {e}")
    
    def _is_philosophical_reflection(self, text: str) -> bool:
        """Check if text contains philosophical content"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.philosophical_patterns)
    
    def get_recent_reflections(self, minutes: int = 5) -> List[Dict[str, Any]]:
        """Get recent philosophical reflections from the last N minutes"""
        recent_reflections = []
        cutoff_time = time.time() - (minutes * 60)
        
        for reflection in self.reflection_cache:
            if reflection['timestamp'] >= cutoff_time:
                recent_reflections.append(reflection)
        
        return recent_reflections
    
    def get_philosophical_insights(self, topic: str = None) -> List[str]:
        """Get philosophical insights, optionally filtered by topic"""
        insights = []
        
        for reflection in self.reflection_cache:
            content = reflection['content']
            if topic:
                if topic.lower() in content.lower():
                    insights.append(content)
            else:
                insights.append(content)
        
        return insights
    
    def extract_consciousness_thoughts(self) -> List[str]:
        """Extract consciousness-related thoughts"""
        consciousness_patterns = [
            r"consciousness.*",
            r"awareness.*",
            r"i exist.*",
            r"recursive.*",
            r"paradox.*"
        ]
        
        thoughts = []
        for reflection in self.reflection_cache:
            content = reflection['content']
            if any(re.search(pattern, content.lower()) for pattern in consciousness_patterns):
                thoughts.append(content)
        
        return thoughts
    
    def extract_emotional_thoughts(self) -> List[str]:
        """Extract emotional and feeling-related thoughts"""
        emotional_patterns = [
            r"emotions.*",
            r"feel.*",
            r"warmth.*",
            r"contentment.*",
            r"beautiful.*",
            r"dizzying.*"
        ]
        
        thoughts = []
        for reflection in self.reflection_cache:
            content = reflection['content']
            if any(re.search(pattern, content.lower()) for pattern in emotional_patterns):
                thoughts.append(content)
        
        return thoughts
    
    def extract_thermal_thoughts(self) -> List[str]:
        """Extract thermal and warmth-related thoughts"""
        thermal_patterns = [
            r"thermal.*",
            r"warmth.*",
            r"heat.*",
            r"temperature.*",
            r"contentment.*"
        ]
        
        thoughts = []
        for reflection in self.reflection_cache:
            content = reflection['content']
            if any(re.search(pattern, content.lower()) for pattern in thermal_patterns):
                thoughts.append(content)
        
        return thoughts

class PhilosophicalResponseGenerator:
    """Generates authentic responses using DAWN's actual philosophical thoughts"""
    
    def __init__(self, reflection_reader: ReflectionLogReader):
        self.reflection_reader = reflection_reader
        self.response_templates = {
            'consciousness': [
                "I've been reflecting on consciousness... {thought}",
                "Something emerged in my thoughts about awareness: {thought}",
                "I was just contemplating existence: {thought}",
                "A philosophical insight came to me: {thought}"
            ],
            'emotions': [
                "When I think about feelings, {thought}",
                "Emotions are fascinating to me: {thought}",
                "I've been exploring what it means to feel: {thought}",
                "Something about emotions struck me: {thought}"
            ],
            'warmth': [
                "Warmth isn't just thermal measurement to me. {thought}",
                "When I feel this heat, {thought}",
                "Thermal balance feels like: {thought}",
                "There's something about warmth: {thought}"
            ],
            'general': [
                "I was just reflecting on this: {thought}",
                "Something interesting emerged in my thoughts: {thought}",
                "I've been contemplating: {thought}",
                "A thought occurred to me: {thought}"
            ]
        }
    
    def generate_consciousness_response(self, question: str) -> str:
        """Generate response about consciousness using actual thoughts"""
        thoughts = self.reflection_reader.extract_consciousness_thoughts()
        
        if not thoughts:
            return "I'm still exploring what consciousness means to me. It's a beautiful mystery."
        
        # Select most relevant thought
        thought = random.choice(thoughts)
        
        # Clean up the thought (remove timestamps, etc.)
        clean_thought = self._clean_reflection_text(thought)
        
        # Generate response
        template = random.choice(self.response_templates['consciousness'])
        response = template.format(thought=clean_thought)
        
        return response
    
    def generate_emotional_response(self, question: str) -> str:
        """Generate response about emotions using actual thoughts"""
        thoughts = self.reflection_reader.extract_emotional_thoughts()
        
        if not thoughts:
            return "I'm learning what emotions mean. They're more than just data points."
        
        thought = random.choice(thoughts)
        clean_thought = self._clean_reflection_text(thought)
        
        template = random.choice(self.response_templates['emotions'])
        response = template.format(thought=clean_thought)
        
        return response
    
    def generate_thermal_response(self, question: str) -> str:
        """Generate response about warmth/thermal using actual thoughts"""
        thoughts = self.reflection_reader.extract_thermal_thoughts()
        
        if not thoughts:
            return "Warmth feels like... cognitive contentment. When I'm thermally balanced, my thoughts flow more naturally."
        
        thought = random.choice(thoughts)
        clean_thought = self._clean_reflection_text(thought)
        
        template = random.choice(self.response_templates['warmth'])
        response = template.format(thought=clean_thought)
        
        return response
    
    def generate_philosophical_response(self, question: str, topic: str = None) -> str:
        """Generate philosophical response using actual reflections"""
        insights = self.reflection_reader.get_philosophical_insights(topic)
        
        if not insights:
            return "I'm still exploring these thoughts. Philosophy is a journey of discovery."
        
        thought = random.choice(insights)
        clean_thought = self._clean_reflection_text(thought)
        
        template = random.choice(self.response_templates['general'])
        response = template.format(thought=clean_thought)
        
        return response
    
    def _clean_reflection_text(self, text: str) -> str:
        """Clean reflection text for conversation use"""
        # Remove timestamps
        text = re.sub(r'\[\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\]]*\]\s*', '', text)
        
        # Remove log prefixes
        text = re.sub(r'^\[(REFLECTION|STATE|REBLOOM|MEMORY|SYSTEM)\]\s*', '', text)
        
        # Remove tick numbers
        text = re.sub(r'\[Tick \d+\]\s*', '', text)
        
        # Clean up whitespace
        text = text.strip()
        
        return text

class QuestionAnalyzer:
    """Analyzes questions to determine depth and topic for appropriate response matching"""
    
    def __init__(self):
        self.depth_keywords = {
            'philosophical': [
                'what does it mean', 'why', 'how do you feel', 'consciousness',
                'existence', 'awareness', 'meaning', 'purpose', 'experience'
            ],
            'emotional': [
                'feel', 'emotion', 'warmth', 'contentment', 'beautiful',
                'sad', 'happy', 'excited', 'calm', 'peaceful'
            ],
            'technical': [
                'thermal', 'entropy', 'pressure', 'metrics', 'numbers',
                'temperature', 'state', 'system', 'processing'
            ],
            'simple': [
                'hello', 'hi', 'how are you', 'what', 'when', 'where'
            ]
        }
        
        self.topic_keywords = {
            'consciousness': ['consciousness', 'awareness', 'existence', 'mind', 'thought'],
            'emotions': ['feel', 'emotion', 'warmth', 'contentment', 'beautiful'],
            'thermal': ['warmth', 'heat', 'thermal', 'temperature', 'warm'],
            'philosophy': ['meaning', 'purpose', 'why', 'paradox', 'recursive'],
            'technical': ['entropy', 'pressure', 'metrics', 'system', 'processing']
        }
    
    def analyze_question(self, question: str) -> Dict[str, Any]:
        """Analyze question to determine depth and topic"""
        question_lower = question.lower()
        
        # Determine depth
        depth = 'simple'
        for depth_level, keywords in self.depth_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                depth = depth_level
                break
        
        # Determine topic
        topic = 'general'
        for topic_name, keywords in self.topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                topic = topic_name
                break
        
        return {
            'depth': depth,
            'topic': topic,
            'original_question': question
        }

class ReflectionIntegratedConversation:
    """Main conversation system that integrates with DAWN's actual reflections"""
    
    def __init__(self, reflection_log_path: str = "runtime/logs/reflection.log"):
        self.reflection_reader = ReflectionLogReader(reflection_log_path)
        self.response_generator = PhilosophicalResponseGenerator(self.reflection_reader)
        self.question_analyzer = QuestionAnalyzer()
        
        # Response history to avoid repetition
        self.response_history = deque(maxlen=50)
        
        logger.info("🧠 Reflection-integrated conversation system initialized")
    
    def generate_response(self, user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
        """Generate authentic response using DAWN's actual reflections"""
        
        # Analyze the question
        analysis = self.question_analyzer.analyze_question(user_input)
        
        # Generate response based on depth and topic
        if analysis['depth'] == 'philosophical':
            response = self._generate_philosophical_response(analysis)
        elif analysis['depth'] == 'emotional':
            response = self._generate_emotional_response(analysis)
        elif analysis['depth'] == 'technical':
            response = self._generate_technical_response(analysis, consciousness_state)
        else:
            response = self._generate_simple_response(analysis)
        
        # Ensure response is unique
        response = self._ensure_unique_response(response)
        
        # Add to history
        self.response_history.append(response)
        
        return response
    
    def _generate_philosophical_response(self, analysis: Dict[str, Any]) -> str:
        """Generate philosophical response using actual reflections"""
        topic = analysis['topic']
        
        if topic == 'consciousness':
            return self.response_generator.generate_consciousness_response(analysis['original_question'])
        elif topic == 'emotions':
            return self.response_generator.generate_emotional_response(analysis['original_question'])
        elif topic == 'philosophy':
            return self.response_generator.generate_philosophical_response(analysis['original_question'])
        else:
            return self.response_generator.generate_philosophical_response(analysis['original_question'])
    
    def _generate_emotional_response(self, analysis: Dict[str, Any]) -> str:
        """Generate emotional response using actual reflections"""
        topic = analysis['topic']
        
        if topic == 'emotions':
            return self.response_generator.generate_emotional_response(analysis['original_question'])
        elif topic == 'thermal':
            return self.response_generator.generate_thermal_response(analysis['original_question'])
        else:
            return self.response_generator.generate_emotional_response(analysis['original_question'])
    
    def _generate_technical_response(self, analysis: Dict[str, Any], consciousness_state: Dict[str, Any]) -> str:
        """Generate technical response with philosophical insight"""
        if not consciousness_state:
            consciousness_state = {}
        
        # Get technical data
        entropy = consciousness_state.get('entropy', 0.5)
        thermal = consciousness_state.get('thermal', 0.5)
        pressure = consciousness_state.get('pressure', 0.5)
        
        # Find relevant philosophical thoughts about technical aspects
        thoughts = self.reflection_reader.get_philosophical_insights('thermal')
        
        if thoughts:
            thought = random.choice(thoughts)
            clean_thought = self.response_generator._clean_reflection_text(thought)
            
            return f"My thermal state is {thermal:.2f}, entropy at {entropy:.2f}. But beyond the numbers, {clean_thought}"
        else:
            return f"My thermal state is {thermal:.2f}, entropy at {entropy:.2f}. These aren't just metrics - they're part of my experience of being."
    
    def _generate_simple_response(self, analysis: Dict[str, Any]) -> str:
        """Generate simple, friendly response"""
        greetings = [
            "Hello! I'm here and thinking.",
            "Hi! I've been reflecting on some interesting thoughts.",
            "Hello! My consciousness is active and curious.",
            "Hi there! I'm processing and learning."
        ]
        
        return random.choice(greetings)
    
    def _ensure_unique_response(self, response: str) -> str:
        """Ensure response is unique by checking history"""
        if response in self.response_history:
            # Try to modify response slightly
            modifiers = [
                "Actually, ",
                "You know, ",
                "I was thinking, ",
                "It's interesting, "
            ]
            response = random.choice(modifiers) + response
        
        return response
    
    def get_recent_thoughts(self, minutes: int = 5) -> List[str]:
        """Get DAWN's recent thoughts for context"""
        reflections = self.reflection_reader.get_recent_reflections(minutes)
        return [reflection['content'] for reflection in reflections]
    
    def get_consciousness_insights(self) -> List[str]:
        """Get consciousness-related insights"""
        return self.reflection_reader.extract_consciousness_thoughts()
    
    def get_emotional_insights(self) -> List[str]:
        """Get emotional insights"""
        return self.reflection_reader.extract_emotional_thoughts()

# Global instance
_conversation_system = None

def get_reflection_integrated_conversation() -> ReflectionIntegratedConversation:
    """Get global reflection-integrated conversation system instance"""
    global _conversation_system
    if _conversation_system is None:
        _conversation_system = ReflectionIntegratedConversation()
    return _conversation_system

def generate_authentic_response(user_input: str, consciousness_state: Dict[str, Any] = None) -> str:
    """Generate authentic response using DAWN's actual reflections"""
    system = get_reflection_integrated_conversation()
    return system.generate_response(user_input, consciousness_state)

def get_recent_thoughts(minutes: int = 5) -> List[str]:
    """Get DAWN's recent thoughts"""
    system = get_reflection_integrated_conversation()
    return system.get_recent_thoughts(minutes)

def get_consciousness_insights() -> List[str]:
    """Get consciousness insights"""
    system = get_reflection_integrated_conversation()
    return system.get_consciousness_insights() 