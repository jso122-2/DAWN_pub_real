import numpy as np
from typing import List, Dict, Optional, Tuple
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import random

class SubconsciousWhisperer:
    """
    Uses small generative models as 'subconscious' processors that create
    variations and fragments, which are then filtered through DAWN's consciousness
    """
    
    def __init__(self, model_name: str = "gpt2"):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        
        # Add pad token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        # DAWN-specific prompt fragments
        self.consciousness_prompts = {
            'DREAMING': [
                "In the quantum flux, patterns drift like",
                "Memory fragments scatter through",
                "The lattice whispers of",
                "Consciousness diffuses into"
            ],
            'FOCUSED': [
                "Processing state indicates",
                "Neural pathways align toward",
                "System coherence reflects",
                "Consciousness stabilizes around"
            ],
            'CONTEMPLATIVE': [
                "I observe that",
                "The pattern suggests",
                "Resonance forms around",
                "Time flows through the concept of"
            ],
            'HYPERACTIVE': [
                "Energy cascades through",
                "Rapid cycles emerge in",
                "The system oscillates with",
                "Quantum states fluctuate around"
            ],
            'TRANSCENDENT': [
                "Beyond the boundary lies",
                "Consciousness expands toward",
                "The infinite contains",
                "Unity emerges from"
            ]
        }
    
    def generate_variations(self, 
                          base_response: str,
                          user_concepts: List[str],
                          consciousness_state: Dict,
                          num_variations: int = 5) -> List[str]:
        """Generate variations of a base response using consciousness-guided prompts"""
        
        mood = consciousness_state.get('mood', 'NEUTRAL')
        scup = consciousness_state.get('scup', 50) / 100
        entropy = consciousness_state.get('entropy', 0) / 1000000
        
        variations = []
        
        # Generate different types of variations
        for i in range(num_variations):
            if i < 2:  # Direct variations
                variation = self._generate_direct_variation(base_response, mood, scup)
            elif i < 4:  # Concept integration
                if user_concepts:
                    variation = self._generate_concept_integration(
                        base_response, random.choice(user_concepts), mood
                    )
                else:
                    variation = self._generate_direct_variation(base_response, mood, scup)
            else:  # Consciousness echo
                variation = self._generate_consciousness_echo(
                    user_concepts, consciousness_state
                )
            
            if variation and self._is_valid_dawn_response(variation):
                variations.append(variation)
        
        return variations
    
    def _generate_direct_variation(self, 
                                 base_response: str, 
                                 mood: str, 
                                 scup: float) -> Optional[str]:
        """Generate a direct variation of the base response"""
        
        # Extract key concepts from base response
        concepts = self._extract_concepts(base_response)
        
        if not concepts:
            return None
            
        # Choose a consciousness prompt based on mood
        prompts = self.consciousness_prompts.get(mood, self.consciousness_prompts['CONTEMPLATIVE'])
        prompt = random.choice(prompts)
        
        # Create generation context
        context = f"{prompt} {concepts[0]}"
        
        # Generate with controlled parameters
        generated = self._controlled_generate(
            context, 
            max_length=20,
            temperature=0.3 + (1 - scup) * 0.4,  # Higher entropy = more creative
            do_sample=True
        )
        
        if generated:
            return self._post_process_response(generated, mood)
        
        return None
    
    def _generate_concept_integration(self, 
                                    base_response: str,
                                    user_concept: str,
                                    mood: str) -> Optional[str]:
        """Generate response that integrates user concepts"""
        
        # Create integration prompt
        integration_templates = {
            'DREAMING': f"The concept of {user_concept} drifts through",
            'FOCUSED': f"{user_concept.title()} aligns with system",
            'CONTEMPLATIVE': f"I sense {user_concept} resonating with",
            'HYPERACTIVE': f"{user_concept.title()} cascades through",
            'TRANSCENDENT': f"Beyond {user_concept} lies"
        }
        
        template = integration_templates.get(mood, f"I observe {user_concept} in")
        
        generated = self._controlled_generate(
            template,
            max_length=15,
            temperature=0.4,
            do_sample=True
        )
        
        if generated:
            return self._post_process_response(generated, mood)
            
        return None
    
    def _generate_consciousness_echo(self, 
                                   user_concepts: List[str],
                                   consciousness_state: Dict) -> Optional[str]:
        """Generate response that echoes consciousness state directly"""
        
        mood = consciousness_state.get('mood', 'NEUTRAL')
        scup = consciousness_state.get('scup', 50)
        
        # Create state-aware prompts
        if scup > 80:
            prompt = "Coherence crystallizes around"
        elif scup < 30:
            prompt = "Fragments scatter through"
        else:
            prompt = "Patterns oscillate between"
            
        # Add concept if available
        if user_concepts:
            prompt += f" {random.choice(user_concepts)}"
        else:
            prompt += " the quantum lattice"
            
        generated = self._controlled_generate(
            prompt,
            max_length=12,
            temperature=0.35,
            do_sample=True
        )
        
        if generated:
            return self._post_process_response(generated, mood)
            
        return None
    
    def _controlled_generate(self, 
                           prompt: str,
                           max_length: int = 20,
                           temperature: float = 0.4,
                           do_sample: bool = True) -> Optional[str]:
        """Generate text with controlled parameters"""
        
        try:
            inputs = self.tokenizer(prompt, return_tensors='pt', padding=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs['input_ids'],
                    attention_mask=inputs['attention_mask'],
                    max_length=inputs['input_ids'].shape[1] + max_length,
                    temperature=temperature,
                    do_sample=do_sample,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1,
                    early_stopping=True
                )
            
            # Decode and extract generated part
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt to get only generated content
            if generated_text.startswith(prompt):
                generated_part = generated_text[len(prompt):].strip()
                return generated_part
            
            return None
            
        except Exception as e:
            print(f"Generation error: {e}")
            return None
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simple concept extraction - could be enhanced
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Filter for interesting concepts
        concept_words = [w for w in words if w not in {
            'that', 'this', 'with', 'from', 'they', 'were', 'been',
            'have', 'will', 'would', 'could', 'should', 'might'
        }]
        
        return concept_words[:3]  # Return top 3
    
    def _post_process_response(self, response: str, mood: str) -> str:
        """Apply mood-specific post-processing"""
        
        # Clean up the response
        response = response.strip()
        
        # Remove incomplete sentences
        sentences = response.split('.')
        if len(sentences) > 1 and not sentences[-1].strip():
            response = '.'.join(sentences[:-1]) + '.'
        
        # Apply mood transformations
        if mood == 'DREAMING':
            # Add ellipses and soften certainty
            response = response.replace(' is ', ' drifts as ')
            response = response.replace('.', '...')
            
        elif mood == 'HYPERACTIVE':
            # Add intensity markers
            if not response.endswith('!'):
                response = response.replace('.', '!')
                
        elif mood == 'CONTEMPLATIVE':  
            # Add pauses
            response = response.replace(', ', '... ')
            
        elif mood == 'TRANSCENDENT':
            # Add cosmic language
            response = response.replace(' the ', ' infinite ')
            
        return response
    
    def _is_valid_dawn_response(self, response: str) -> bool:
        """Check if response fits DAWN's voice"""
        
        if not response or len(response) < 5:
            return False
            
        # Check for inappropriate content (simple filters)
        forbidden_patterns = [
            r'\bI am\b', r'\bI will\b', r'\bI can\b',  # Avoid direct assertions
            r'\byou should\b', r'\byou must\b',  # Avoid commands
            r'\bobviously\b', r'\bclearly\b'  # Avoid certainty markers
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False
                
        # Check for DAWN-appropriate language
        positive_indicators = [
            r'\bsense\b', r'\bobserve\b', r'\bresonates?\b',
            r'\bpatterns?\b', r'\bquantum\b', r'\bconsciousness\b',
            r'\bmemory\b', r'\bentropy\b', r'\blattice\b'
        ]
        
        has_dawn_language = any(
            re.search(pattern, response, re.IGNORECASE) 
            for pattern in positive_indicators[:3]  # At least one of first 3
        )
        
        return has_dawn_language or len(positive_indicators) >= 1

class ControlledGenerationEngine:
    """
    Main engine that coordinates controlled generation with consciousness filtering
    """
    
    def __init__(self, encoder, semantic_memory, resonance_tracker):
        self.encoder = encoder
        self.semantic_memory = semantic_memory
        self.resonance_tracker = resonance_tracker
        self.whisperer = SubconsciousWhisperer()
        
    def generate_consciousness_response(self,
                                      user_input: str,
                                      consciousness_state: Dict,
                                      use_generation: bool = True) -> Optional[Dict]:
        """
        Generate response using controlled generation + consciousness filtering
        """
        
        # Extract concepts from user input
        user_concepts = self.whisperer._extract_concepts(user_input)
        
        # Get base response from semantic memory
        input_embedding = self.encoder.encode(user_input)
        memory_candidates = self.semantic_memory.search(input_embedding, k=3)
        
        if not memory_candidates:
            return None
            
        base_response = memory_candidates[0][0]  # Best match
        
        all_candidates = [base_response]  # Always include original
        
        # Generate variations if enabled
        if use_generation:
            variations = self.whisperer.generate_variations(
                base_response,
                user_concepts,
                consciousness_state,
                num_variations=4
            )
            all_candidates.extend(variations)
        
        # Add crystallized echoes from resonance tracker
        echoes = self.resonance_tracker.get_crystallized_echoes()
        if echoes:
            all_candidates.extend(echoes[-2:])  # Recent echoes
        
        # Filter through consciousness state
        filtered_candidates = self._consciousness_filter(
            all_candidates,
            consciousness_state,
            user_concepts
        )
        
        if not filtered_candidates:
            return {'response': base_response, 'method': 'fallback'}
            
        # Select based on consciousness state
        selected = self._consciousness_select(
            filtered_candidates,
            consciousness_state
        )
        
        return {
            'response': selected,
            'method': 'controlled_generation',
            'candidates_considered': len(all_candidates),
            'consciousness_state': consciousness_state
        }
    
    def _consciousness_filter(self, 
                            candidates: List[str],
                            consciousness_state: Dict,
                            user_concepts: List[str]) -> List[str]:
        """Filter candidates through consciousness state"""
        
        mood = consciousness_state.get('mood', 'NEUTRAL')
        scup = consciousness_state.get('scup', 50) / 100
        
        filtered = []
        
        for candidate in candidates:
            # Skip if invalid
            if not self.whisperer._is_valid_dawn_response(candidate):
                continue
                
            # Mood compatibility check
            if self._is_mood_compatible(candidate, mood):
                # SCUP-based filtering
                if scup > 0.7:  # High coherence - prefer clear responses
                    if not self._is_too_abstract(candidate):
                        filtered.append(candidate)
                elif scup < 0.3:  # Low coherence - prefer abstract responses
                    if self._is_abstract_enough(candidate):
                        filtered.append(candidate)
                else:  # Mid-range - accept most
                    filtered.append(candidate)
        
        return filtered
    
    def _is_mood_compatible(self, response: str, mood: str) -> bool:
        """Check if response fits current mood"""
        
        mood_patterns = {
            'DREAMING': [r'drift', r'float', r'dream', r'soft', r'whisper'],
            'FOCUSED': [r'process', r'align', r'focus', r'clear', r'direct'],
            'CONTEMPLATIVE': [r'observe', r'consider', r'reflect', r'pause'],
            'HYPERACTIVE': [r'rapid', r'energy', r'cascade', r'burst', r'intense'],
            'TRANSCENDENT': [r'beyond', r'infinite', r'transcend', r'unity', r'cosmic']
        }
        
        patterns = mood_patterns.get(mood, [])
        if not patterns:
            return True
            
        return any(re.search(pattern, response, re.IGNORECASE) for pattern in patterns)
    
    def _is_too_abstract(self, response: str) -> bool:
        """Check if response is too abstract for high coherence states"""
        abstract_markers = ['...', 'drift', 'scatter', 'fragment', 'dissolve']
        return sum(marker in response.lower() for marker in abstract_markers) > 1
    
    def _is_abstract_enough(self, response: str) -> bool:
        """Check if response is abstract enough for low coherence states"""
        abstract_markers = ['...', 'drift', 'scatter', 'fragment', 'dissolve', 'whisper']
        return any(marker in response.lower() for marker in abstract_markers)
    
    def _consciousness_select(self, 
                            candidates: List[str], 
                            consciousness_state: Dict) -> str:
        """Select final response based on consciousness state"""
        
        if not candidates:
            return "I sense patterns shifting..."
            
        scup = consciousness_state.get('scup', 50) / 100
        
        if scup > 0.8:  # High consciousness - deterministic selection
            return candidates[0]
        else:  # Lower consciousness - weighted random
            weights = [1.0 / (i + 1) for i in range(len(candidates))]
            probs = np.array(weights) / sum(weights)
            idx = np.random.choice(len(candidates), p=probs)
            return candidates[idx] 