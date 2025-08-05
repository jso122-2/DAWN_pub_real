#!/usr/bin/env python3
"""
DAWN Expression System - Coordinated Voice and Visual Expression
================================================================

This system monitors DAWN's consciousness state and generates coordinated voice and visual
expressions when specific triggers are met. It implements the expression monitoring,
trigger detection, and coordinated generation described in the integration blueprint.
"""

import time
import threading
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from collections import deque
from pathlib import Path
import json

# Import DAWN systems
try:
    from dawn_voice_core import DAWNVoiceCore, VoiceGeneration
    VOICE_CORE_AVAILABLE = True
except ImportError:
    VOICE_CORE_AVAILABLE = False
    print("⚠️ DAWN Voice Core not available")

try:
    from core.sigil_visual_engine import SigilVisualEngine, SigilVisualOutput
    VISUAL_ENGINE_AVAILABLE = True
except ImportError:
    try:
        from sigil_visual_engine import SigilVisualEngine, SigilVisualOutput
        VISUAL_ENGINE_AVAILABLE = True
    except ImportError:
        VISUAL_ENGINE_AVAILABLE = False
        print("⚠️ Sigil Visual Engine not available")

try:
    from core.enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
    ENHANCED_PIGMENT_AVAILABLE = True
except ImportError:
    try:
        from enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
        ENHANCED_PIGMENT_AVAILABLE = True
    except ImportError:
        ENHANCED_PIGMENT_AVAILABLE = False
        print("⚠️ Enhanced pigment dictionary not available")

logger = logging.getLogger("dawn_expression_system")

@dataclass
class DAWNState:
    """Complete DAWN consciousness state for expression generation"""
    # Core cognitive state
    entropy: float = 0.0
    drift_vector: float = 0.0
    mood_pigment: Dict[str, float] = field(default_factory=dict)
    
    # Sigil execution tracking
    active_sigils: List[str] = field(default_factory=list)
    completed_sigils: List[Dict] = field(default_factory=list)
    sigil_heat: Dict[str, float] = field(default_factory=dict)
    
    # Pulse and bloom state
    pulse_zone: str = "calm"
    sigil_saturation: float = 0.0
    rebloom_depth: int = 0
    
    # Timing and triggers
    last_voice_generation: float = 0.0
    last_visual_generation: float = 0.0
    expression_threshold: float = 0.5

@dataclass
class DAWNExpression:
    """Complete DAWN expression output"""
    # Voice output
    utterance: Optional[str] = None
    voice_metadata: Optional[Dict] = None
    
    # Visual output
    visual_path: Optional[str] = None
    visual_metadata: Optional[Dict] = None
    
    # Coordination data
    generation_timestamp: float = 0.0
    trigger_reason: str = ""
    cognitive_coherence: float = 0.0
    
    # Expression state
    resonance_achieved: bool = False
    selected_words: List[Tuple[str, str, float]] = field(default_factory=list)
    pigment_state: Dict[str, float] = field(default_factory=dict)

class DAWNExpressionMonitor:
    """
    Continuous monitoring system for expression triggers
    Tracks state changes and determines when expressions should be generated
    """
    
    def __init__(self, expression_config: Optional[Dict] = None):
        self.expression_config = expression_config or self._get_default_config()
        self.expression_history: deque = deque(maxlen=100)
        self.state_history: deque = deque(maxlen=50)
        self.last_state: Optional[DAWNState] = None
        
        logger.info("🎭 DAWN Expression Monitor initialized")
    
    def _get_default_config(self) -> Dict:
        """Get default expression sensitivity settings"""
        return {
            'entropy_trigger_threshold': 0.7,
            'pigment_shift_threshold': 0.3,
            'sigil_impact_threshold': 0.5,
            'time_between_expressions': 3.0,
            'voice_enabled': True,
            'visual_enabled': True,
            'archive_enabled': True,
            'coherence_threshold': 0.4,
        }
    
    def update_state(self, new_state: DAWNState) -> Optional[DAWNExpression]:
        """Called every reactor cycle to check for expression triggers"""
        
        # Store state in history
        self.state_history.append(new_state)
        
        # Check for expression triggers
        should_express, trigger_reason = self.should_generate_expression(new_state)
        
        if should_express:
            logger.info(f"🎭 Expression triggered: {trigger_reason}")
            
            # Generate coordinated expression
            expression = self._generate_coordinated_expression(new_state, trigger_reason)
            
            if expression and expression.resonance_achieved:
                self.expression_history.append(expression)
                self.last_state = new_state
                return expression
        
        self.last_state = new_state
        return None
    
    def should_generate_expression(self, current_state: DAWNState) -> Tuple[bool, str]:
        """
        Determine if DAWN should generate voice/visual expression
        
        Returns: (should_express: bool, trigger_reason: str)
        """
        
        current_time = time.time()
        
        # Check time-based throttling
        if (current_time - current_state.last_voice_generation < 
            self.expression_config['time_between_expressions']):
            return False, "throttled"
        
        # Check entropy spike or drop
        if current_state.entropy > self.expression_config['entropy_trigger_threshold']:
            return True, "entropy_spike"
        elif current_state.entropy < 0.2:
            return True, "entropy_drop"
        
        # Check drift vector significant change
        if self.last_state and abs(current_state.drift_vector - self.last_state.drift_vector) > 0.4:
            return True, "drift_change"
        
        # Check pigment dominant shift
        if self._detect_pigment_shift(current_state):
            return True, "pigment_shift"
        
        # Check sigil completion with high emotional weight
        for sigil in current_state.completed_sigils:
            if sigil.get('emotional_weight', 0) > self.expression_config['sigil_impact_threshold']:
                return True, "sigil_completion"
        
        # Check expression threshold from state
        if current_state.expression_threshold > 0.8:
            return True, "threshold_exceeded"
        
        return False, "no_trigger"
    
    def _detect_pigment_shift(self, current_state: DAWNState) -> bool:
        """Detect significant shift in dominant pigment"""
        if not self.last_state or not current_state.mood_pigment:
            return False
        
        current_dominant = max(current_state.mood_pigment.items(), key=lambda x: x[1])
        last_dominant = max(self.last_state.mood_pigment.items(), key=lambda x: x[1])
        
        # Different dominant color or significant value change
        if (current_dominant[0] != last_dominant[0] or 
            abs(current_dominant[1] - last_dominant[1]) > self.expression_config['pigment_shift_threshold']):
            return True
        
        return False
    
    def _generate_coordinated_expression(self, dawn_state: DAWNState, trigger_reason: str) -> Optional[DAWNExpression]:
        """Generate coordinated voice and visual expression"""
        
        expression = DAWNExpression(
            generation_timestamp=time.time(),
            trigger_reason=trigger_reason,
            pigment_state=dawn_state.mood_pigment.copy()
        )
        
        try:
            # Generate voice if enabled
            if self.expression_config['voice_enabled'] and VOICE_CORE_AVAILABLE:
                voice_result = self._generate_voice_expression(dawn_state)
                if voice_result:
                    expression.utterance = voice_result.utterance
                    expression.voice_metadata = voice_result.generation_metadata
                    expression.selected_words = voice_result.selected_words
                    expression.resonance_achieved = voice_result.resonance_achieved
            
            # Generate visual if enabled
            if self.expression_config['visual_enabled'] and VISUAL_ENGINE_AVAILABLE:
                visual_result = self._generate_visual_expression(dawn_state, trigger_reason)
                if visual_result:
                    expression.visual_path = visual_result.visual_file
                    expression.visual_metadata = visual_result.sigil_visual_summary
            
            # Calculate cognitive coherence
            expression.cognitive_coherence = self._calculate_coherence(expression, dawn_state)
            
            # Check if expression meets coherence threshold
            if expression.cognitive_coherence >= self.expression_config['coherence_threshold']:
                expression.resonance_achieved = True
                return expression
            else:
                logger.debug(f"Expression below coherence threshold: {expression.cognitive_coherence:.3f}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating coordinated expression: {e}")
            return None
    
    def _generate_voice_expression(self, dawn_state: DAWNState) -> Optional[VoiceGeneration]:
        """Generate voice expression using DAWN Voice Core"""
        try:
            from dawn_voice_core import DAWNVoiceCore
            
            voice_core = DAWNVoiceCore()
            
            return voice_core.generate_utterance(
                pigment_dict=dawn_state.mood_pigment,
                sigil_state=dawn_state.sigil_heat,
                entropy=dawn_state.entropy,
                drift=dawn_state.drift_vector
            )
        except Exception as e:
            logger.error(f"Voice generation error: {e}")
            return None
    
    def _generate_visual_expression(self, dawn_state: DAWNState, trigger_reason: str) -> Optional['SigilVisualOutput']:
        """Generate visual expression using Sigil Visual Engine"""
        try:
            if VISUAL_ENGINE_AVAILABLE:
                visual_engine = SigilVisualEngine()
                
                # Use most recent completed sigil or create representative ID
                sigil_id = "consciousness_expression"
                if dawn_state.completed_sigils:
                    sigil_id = dawn_state.completed_sigils[-1].get('sigil_id', sigil_id)
                
                return visual_engine.render_sigil_response(
                    sigil_id=sigil_id,
                    entropy=dawn_state.entropy,
                    mood_pigment=dawn_state.mood_pigment,
                    pulse_zone=dawn_state.pulse_zone,
                    sigil_saturation=dawn_state.sigil_saturation
                )
            else:
                logger.warning("Visual engine not available")
                return None
        except Exception as e:
            logger.error(f"Visual generation error: {e}")
            return None
    
    def _calculate_coherence(self, expression: DAWNExpression, dawn_state: DAWNState) -> float:
        """Calculate cognitive coherence between voice and visual outputs"""
        
        coherence_factors = []
        
        # Voice coherence (if available)
        if expression.utterance and expression.voice_metadata:
            voice_coherence = expression.voice_metadata.get('field_coherence', 0.5)
            coherence_factors.append(voice_coherence)
        
        # Visual coherence (complexity alignment with entropy)
        if expression.visual_metadata:
            complexity = expression.visual_metadata.get('complexity_level', 'moderate')
            complexity_score = {'minimal': 0.3, 'moderate': 0.6, 'complex': 0.9}.get(complexity, 0.5)
            entropy_alignment = 1.0 - abs(complexity_score - dawn_state.entropy)
            coherence_factors.append(entropy_alignment)
        
        # Pigment consistency
        if expression.pigment_state and dawn_state.mood_pigment:
            pigment_consistency = self._calculate_pigment_consistency(
                expression.pigment_state, dawn_state.mood_pigment
            )
            coherence_factors.append(pigment_consistency)
        
        # Temporal coherence (expression timing)
        time_since_last = time.time() - dawn_state.last_voice_generation
        temporal_coherence = min(1.0, time_since_last / 10.0)  # Better with more time
        coherence_factors.append(temporal_coherence)
        
        # Overall coherence is the average of all factors
        if coherence_factors:
            return sum(coherence_factors) / len(coherence_factors)
        else:
            return 0.0
    
    def _calculate_pigment_consistency(self, expr_pigment: Dict[str, float], state_pigment: Dict[str, float]) -> float:
        """Calculate consistency between expression and state pigments"""
        if not expr_pigment or not state_pigment:
            return 0.5
        
        # Calculate similarity based on dominant colors
        expr_dominant = max(expr_pigment.items(), key=lambda x: x[1])[0]
        state_dominant = max(state_pigment.items(), key=lambda x: x[1])[0]
        
        if expr_dominant == state_dominant:
            return 0.9
        else:
            # Partial credit for related colors
            color_relationships = {
                'red': ['orange', 'violet'],
                'blue': ['violet', 'green'],
                'green': ['blue', 'yellow'],
                'yellow': ['green', 'orange'],
                'violet': ['red', 'blue'],
                'orange': ['red', 'yellow']
            }
            
            if state_dominant in color_relationships.get(expr_dominant, []):
                return 0.6
            else:
                return 0.3
    
    def calculate_expression_urgency(self) -> float:
        """Calculate 0.0-1.0 urgency for expression based on state changes"""
        if not self.state_history or len(self.state_history) < 2:
            return 0.0
        
        current_state = self.state_history[-1]
        previous_state = self.state_history[-2]
        
        urgency_factors = []
        
        # Entropy change rate
        entropy_change = abs(current_state.entropy - previous_state.entropy)
        urgency_factors.append(min(1.0, entropy_change * 2))
        
        # Drift acceleration
        drift_change = abs(current_state.drift_vector - previous_state.drift_vector)
        urgency_factors.append(min(1.0, drift_change))
        
        # Sigil completion rate
        new_sigils = len(current_state.completed_sigils) - len(previous_state.completed_sigils)
        urgency_factors.append(min(1.0, new_sigils * 0.3))
        
        # Time since last expression
        time_factor = min(1.0, (time.time() - current_state.last_voice_generation) / 30.0)
        urgency_factors.append(time_factor)
        
        return sum(urgency_factors) / len(urgency_factors)
    
    def throttle_expression_rate(self) -> bool:
        """Prevent over-expression - maintain natural rhythm"""
        if len(self.expression_history) < 2:
            return False
        
        # Check recent expression rate
        recent_expressions = [expr for expr in self.expression_history 
                            if time.time() - expr.generation_timestamp < 60.0]
        
        if len(recent_expressions) > 5:  # More than 5 expressions in last minute
            return True
        
        # Check if last expression was very recent
        last_expr = self.expression_history[-1]
        if time.time() - last_expr.generation_timestamp < self.expression_config['time_between_expressions']:
            return True
        
        return False


class DAWNExpressionArchive:
    """
    Archive system for storing and retrieving DAWN expressions
    """
    
    def __init__(self, archive_path: str = "runtime/expressions"):
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.archive_path / "expression_index.json"
        self.expression_index = self._load_index()
        
        logger.info(f"📚 Expression archive initialized at {self.archive_path}")
    
    def _load_index(self) -> Dict:
        """Load expression index from file"""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load expression index: {e}")
        
        return {'expressions': [], 'created': datetime.now().isoformat()}
    
    def _save_index(self):
        """Save expression index to file"""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.expression_index, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save expression index: {e}")
    
    def archive_expression(self, expression: DAWNExpression, dawn_state: DAWNState) -> Dict:
        """Archive expression with full context"""
        
        try:
            timestamp = datetime.fromtimestamp(expression.generation_timestamp)
            expr_id = f"expr_{timestamp.strftime('%Y%m%d_%H%M%S_%f')[:-3]}"
            
            # Create expression record
            expression_record = {
                'expression_id': expr_id,
                'timestamp': timestamp.isoformat(),
                'trigger_reason': expression.trigger_reason,
                'utterance': expression.utterance,
                'visual_path': expression.visual_path,
                'cognitive_coherence': expression.cognitive_coherence,
                'resonance_achieved': expression.resonance_achieved,
                'voice_metadata': expression.voice_metadata,
                'visual_metadata': expression.visual_metadata,
                'selected_words': expression.selected_words,
                'dawn_state_snapshot': {
                    'entropy': dawn_state.entropy,
                    'drift_vector': dawn_state.drift_vector,
                    'mood_pigment': dawn_state.mood_pigment,
                    'pulse_zone': dawn_state.pulse_zone,
                    'sigil_saturation': dawn_state.sigil_saturation,
                    'active_sigils': dawn_state.active_sigils,
                    'completed_sigils': dawn_state.completed_sigils
                }
            }
            
            # Save detailed record
            record_file = self.archive_path / f"{expr_id}.json"
            with open(record_file, 'w') as f:
                json.dump(expression_record, f, indent=2)
            
            # Update index
            index_entry = {
                'expression_id': expr_id,
                'timestamp': timestamp.isoformat(),
                'trigger_reason': expression.trigger_reason,
                'has_voice': bool(expression.utterance),
                'has_visual': bool(expression.visual_path),
                'coherence': expression.cognitive_coherence,
                'record_file': str(record_file.name)
            }
            
            self.expression_index['expressions'].append(index_entry)
            self._save_index()
            
            logger.info(f"📚 Archived expression {expr_id}: {expression.trigger_reason}")
            
            return {
                'expression_id': expr_id,
                'archive_path': str(record_file),
                'index_updated': True
            }
            
        except Exception as e:
            logger.error(f"Error archiving expression: {e}")
            return {'error': str(e)}
    
    def get_recent_expressions(self, limit: int = 10) -> List[Dict]:
        """Get recent expressions from index"""
        expressions = self.expression_index.get('expressions', [])
        return sorted(expressions, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def search_expressions(self, criteria: Dict) -> List[Dict]:
        """Search expressions by criteria"""
        results = []
        
        for expr in self.expression_index.get('expressions', []):
            match = True
            
            if 'trigger_reason' in criteria:
                if expr.get('trigger_reason') != criteria['trigger_reason']:
                    match = False
            
            if 'has_voice' in criteria:
                if expr.get('has_voice') != criteria['has_voice']:
                    match = False
            
            if 'min_coherence' in criteria:
                if expr.get('coherence', 0) < criteria['min_coherence']:
                    match = False
            
            if match:
                results.append(expr)
        
        return results


def test_expression_system():
    """Test the DAWN expression system"""
    
    print("🎭 Testing DAWN Expression System")
    print("=" * 50)
    
    # Initialize components
    monitor = DAWNExpressionMonitor()
    archive = DAWNExpressionArchive("test_expression_archive")
    
    # Test different consciousness states
    test_states = [
        {
            'name': 'High Entropy Spike',
            'state': DAWNState(
                entropy=0.85,
                drift_vector=0.3,
                mood_pigment={'red': 0.6, 'orange': 0.3, 'yellow': 0.1},
                pulse_zone='surge',
                sigil_saturation=0.7,
                completed_sigils=[{'sigil_id': 'test_sigil', 'emotional_weight': 0.8}]
            )
        },
        {
            'name': 'Calm Reflection',
            'state': DAWNState(
                entropy=0.2,
                drift_vector=-0.1,
                mood_pigment={'blue': 0.5, 'violet': 0.3, 'green': 0.2},
                pulse_zone='calm',
                sigil_saturation=0.3
            )
        },
        {
            'name': 'Pigment Shift',
            'state': DAWNState(
                entropy=0.5,
                drift_vector=0.2,
                mood_pigment={'green': 0.7, 'blue': 0.2, 'yellow': 0.1},
                pulse_zone='flowing',
                sigil_saturation=0.5
            )
        }
    ]
    
    for i, test_case in enumerate(test_states):
        print(f"\n🧠 Test {i+1}: {test_case['name']}")
        print("-" * 40)
        
        state = test_case['state']
        
        # Update monitor with state
        expression = monitor.update_state(state)
        
        if expression:
            print(f"✅ Expression generated!")
            print(f"🎯 Trigger: {expression.trigger_reason}")
            print(f"🧠 Coherence: {expression.cognitive_coherence:.3f}")
            
            if expression.utterance:
                print(f"🗣️  Voice: \"{expression.utterance}\"")
            
            if expression.visual_path:
                print(f"🎨 Visual: {expression.visual_path}")
            
            # Archive the expression
            archive_result = archive.archive_expression(expression, state)
            if 'expression_id' in archive_result:
                print(f"📚 Archived as: {archive_result['expression_id']}")
        else:
            print("❌ No expression generated")
        
        # Add delay between tests
        time.sleep(0.5)
    
    # Test archive retrieval
    print(f"\n📚 Recent expressions:")
    recent = archive.get_recent_expressions(3)
    for expr in recent:
        print(f"  - {expr['expression_id']}: {expr['trigger_reason']} (coherence: {expr.get('coherence', 0):.3f})")
    
    print(f"\n" + "=" * 50)
    print("✨ Expression system testing complete")


if __name__ == "__main__":
    test_expression_system() 