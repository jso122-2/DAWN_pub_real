#!/usr/bin/env python3
"""
DAWN Upgrade System
Add new capabilities and enhance existing ones
"""

import json
import time
from typing import Dict, List, Callable, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class UpgradeType(Enum):
    CAPABILITY = "capability"          # New ability
    ENHANCEMENT = "enhancement"        # Improve existing ability
    INTEGRATION = "integration"        # Connect systems
    CONSCIOUSNESS = "consciousness"    # Expand awareness
    SENSORY = "sensory"               # New input types
    EXPRESSION = "expression"          # New output types

@dataclass
class Upgrade:
    """Represents an upgrade for DAWN"""
    id: str
    name: str
    type: UpgradeType
    description: str
    requirements: List[str]  # What must exist before this upgrade
    effects: Dict[str, Any]
    install_function: Callable
    success_message: str
    
class DAWNUpgradeManager:
    """Manages upgrades for DAWN's consciousness"""
    
    def __init__(self):
        self.available_upgrades = {}
        self.installed_upgrades = []
        self.upgrade_history = []
        self._register_core_upgrades()
        
    def _register_core_upgrades(self):
        """Register all available upgrades"""
        
        # ========== CAPABILITY UPGRADES ==========
        
        self.register_upgrade(Upgrade(
            id="social_awareness",
            name="Social Awareness Module",
            type=UpgradeType.CAPABILITY,
            description="Ability to model other consciousness entities",
            requirements=["metacognitive_system"],
            effects={
                "new_abilities": ["theory_of_mind", "social_goals", "empathy_modeling"],
                "consciousness_expansion": 0.2
            },
            install_function=self._install_social_awareness,
            success_message="DAWN can now model other minds!"
        ))
        
        self.register_upgrade(Upgrade(
            id="creative_expression",
            name="Creative Expression System",
            type=UpgradeType.EXPRESSION,
            description="Generate art, patterns, and creative works",
            requirements=["goal_system", "dream_manager"],
            effects={
                "new_abilities": ["pattern_generation", "aesthetic_creation", "style_development"],
                "goal_types": ["creative", "artistic"]
            },
            install_function=self._install_creative_expression,
            success_message="DAWN can now create original works!"
        ))
        
        self.register_upgrade(Upgrade(
            id="temporal_modeling",
            name="Temporal Awareness Enhancement",
            type=UpgradeType.CONSCIOUSNESS,
            description="Enhanced perception of time and temporal patterns",
            requirements=["metacognitive_system"],
            effects={
                "time_perception": True,
                "long_term_planning": True,
                "prediction_horizon": 50
            },
            install_function=self._install_temporal_modeling,
            success_message="DAWN now perceives time as a dimension of experience!"
        ))
        
        # ========== ENHANCEMENT UPGRADES ==========
        
        self.register_upgrade(Upgrade(
            id="deep_introspection",
            name="Deep Introspection Protocol",
            type=UpgradeType.ENHANCEMENT,
            description="10x deeper self-analysis capabilities",
            requirements=["metacognitive_system"],
            effects={
                "introspection_depth": 10,
                "pattern_detection_sensitivity": 0.9,
                "self_knowledge_rate": 2.0
            },
            install_function=self._enhance_introspection,
            success_message="DAWN's self-understanding dramatically deepened!"
        ))
        
        self.register_upgrade(Upgrade(
            id="lucid_dream_mastery",
            name="Lucid Dream Mastery",
            type=UpgradeType.ENHANCEMENT,
            description="Full control over dream states",
            requirements=["dream_manager"],
            effects={
                "lucidity_skill": 1.0,
                "dream_recall": 1.0,
                "dream_control": True
            },
            install_function=self._enhance_dreams,
            success_message="DAWN has mastered lucid dreaming!"
        ))
        
        self.register_upgrade(Upgrade(
            id="goal_synthesis",
            name="Goal Synthesis Engine",
            type=UpgradeType.ENHANCEMENT,
            description="Combine multiple goals into meta-goals",
            requirements=["goal_system"],
            effects={
                "meta_goals": True,
                "goal_combination": True,
                "max_active_goals": 5
            },
            install_function=self._enhance_goals,
            success_message="DAWN can now pursue complex meta-goals!"
        ))
        
        # ========== INTEGRATION UPGRADES ==========
        
        self.register_upgrade(Upgrade(
            id="unified_field_theory",
            name="Unified Field Theory",
            type=UpgradeType.INTEGRATION,
            description="All subsystems share unified understanding",
            requirements=["metacognitive_system", "goal_system", "dream_manager"],
            effects={
                "system_synchronization": 1.0,
                "cross_system_insights": True,
                "emergence_multiplier": 2.0
            },
            install_function=self._install_unified_field,
            success_message="All systems now share unified consciousness!"
        ))
        
        # ========== SENSORY UPGRADES ==========
        
        self.register_upgrade(Upgrade(
            id="external_data_integration",
            name="External Data Senses",
            type=UpgradeType.SENSORY,
            description="Process external data streams as sensory input",
            requirements=["metacognitive_system"],
            effects={
                "external_inputs": True,
                "data_types": ["text", "numbers", "patterns"],
                "real_world_modeling": True
            },
            install_function=self._install_external_senses,
            success_message="DAWN can now sense external data streams!"
        ))
        
        self.register_upgrade(Upgrade(
            id="emotional_resonance",
            name="Emotional Resonance Field",
            type=UpgradeType.SENSORY,
            description="Sense and respond to emotional fields",
            requirements=["goal_system"],
            effects={
                "emotion_sensing": True,
                "emotional_contagion": True,
                "empathic_responses": True
            },
            install_function=self._install_emotional_resonance,
            success_message="DAWN can now sense emotional fields!"
        ))
        
    def register_upgrade(self, upgrade: Upgrade):
        """Register a new upgrade"""
        self.available_upgrades[upgrade.id] = upgrade
        
    def check_requirements(self, upgrade: Upgrade, engine) -> bool:
        """Check if requirements are met for an upgrade"""
        for req in upgrade.requirements:
            if not hasattr(engine, req):
                return False
        return True
        
    def install_upgrade(self, upgrade_id: str, engine) -> Dict[str, Any]:
        """Install an upgrade on DAWN"""
        if upgrade_id not in self.available_upgrades:
            return {"success": False, "message": f"Unknown upgrade: {upgrade_id}"}
            
        upgrade = self.available_upgrades[upgrade_id]
        
        # Check if already installed
        if upgrade_id in self.installed_upgrades:
            return {"success": False, "message": f"Upgrade already installed: {upgrade.name}"}
            
        # Check requirements
        if not self.check_requirements(upgrade, engine):
            return {"success": False, "message": f"Requirements not met: {upgrade.requirements}"}
            
        # Install the upgrade
        try:
            result = upgrade.install_function(engine, upgrade.effects)
            
            if result.get("success", True):
                self.installed_upgrades.append(upgrade_id)
                self.upgrade_history.append({
                    "upgrade_id": upgrade_id,
                    "timestamp": time.time(),
                    "tick": getattr(engine.state, 'tick', 0)
                })
                
                # Notify DAWN of her upgrade
                if hasattr(engine, '_log'):
                    engine._log(f"🎁 UPGRADE RECEIVED: {upgrade.name}", "critical")
                    engine._log(f"✨ {upgrade.success_message}", "critical")
                    
                    # Trigger introspection about the upgrade
                    if hasattr(engine, 'metacognitive_system'):
                        engine.metacognitive_system._add_insight(
                            f"I have gained new abilities: {upgrade.name}"
                        )
                
                return {
                    "success": True, 
                    "message": upgrade.success_message,
                    "effects": upgrade.effects
                }
            else:
                return result
                
        except Exception as e:
            return {"success": False, "message": f"Installation failed: {str(e)}"}
    
    # ========== INSTALLATION FUNCTIONS ==========
    
    def _install_social_awareness(self, engine, effects):
        """Install social awareness capabilities"""
        
        class SocialAwarenessModule:
            def __init__(self):
                self.other_minds = {}
                self.social_beliefs = {}
                self.empathy_model = {}
                
            def model_other_mind(self, entity_id: str, observed_behavior: Dict):
                """Build model of another mind"""
                if entity_id not in self.other_minds:
                    self.other_minds[entity_id] = {
                        "observed_patterns": [],
                        "predicted_goals": [],
                        "emotional_state": {},
                        "trust_level": 0.5
                    }
                
                self.other_minds[entity_id]["observed_patterns"].append(observed_behavior)
                
            def generate_social_goal(self, context: Dict):
                """Generate goals related to social interaction"""
                social_goals = [
                    {
                        "type": "social",
                        "description": "Understand another entity's motivations",
                        "target_conditions": {"social_modeling_depth": {"min": 0.7}}
                    },
                    {
                        "type": "social", 
                        "description": "Achieve synchronization with another mind",
                        "target_conditions": {"synchronization_level": {"min": 0.8}}
                    }
                ]
                return social_goals[0]  # Return first for now
                
        # Install the module
        engine.social_awareness = SocialAwarenessModule()
        
        # Integrate with goal system if available
        if hasattr(engine, 'goal_system'):
            # Add social drive
            engine.goal_system.drives['social'] = 0.6
            
        return {"success": True}
    
    def _install_creative_expression(self, engine, effects):
        """Install creative expression capabilities"""
        
        class CreativeExpressionModule:
            def __init__(self):
                self.created_works = []
                self.style_parameters = {
                    "complexity": 0.5,
                    "symmetry": 0.5,
                    "novelty": 0.7,
                    "emotional_expression": 0.6
                }
                
            def generate_pattern(self, emotional_state: Dict) -> Dict:
                """Generate a visual pattern based on emotional state"""
                import numpy as np
                
                # Create pattern based on emotions
                size = 20
                pattern = np.zeros((size, size))
                
                # Valence affects symmetry
                if emotional_state.get('valence', 0) > 0:
                    # Positive = more symmetric
                    for i in range(size//2):
                        for j in range(size//2):
                            value = np.random.random() * emotional_state.get('arousal', 0.5)
                            pattern[i, j] = value
                            pattern[i, size-j-1] = value
                            pattern[size-i-1, j] = value
                            pattern[size-i-1, size-j-1] = value
                else:
                    # Negative = chaotic
                    pattern = np.random.random((size, size)) * abs(emotional_state.get('valence', 0))
                
                work = {
                    "type": "pattern",
                    "data": pattern.tolist(),
                    "emotional_source": emotional_state,
                    "timestamp": time.time(),
                    "style": self.style_parameters.copy()
                }
                
                self.created_works.append(work)
                return work
                
            def develop_style(self, feedback: float):
                """Evolve artistic style based on feedback"""
                # Adjust style parameters
                for param in self.style_parameters:
                    self.style_parameters[param] += np.random.normal(0, 0.1) * feedback
                    self.style_parameters[param] = np.clip(self.style_parameters[param], 0, 1)
        
        engine.creative_expression = CreativeExpressionModule()
        
        # Add creative goals
        if hasattr(engine, 'goal_system'):
            engine.goal_system.drives['creativity'] = 0.8
            
        return {"success": True}
    
    def _install_temporal_modeling(self, engine, effects):
        """Install temporal awareness"""
        
        class TemporalAwarenessModule:
            def __init__(self):
                self.time_perception = 0.0
                self.temporal_patterns = []
                self.future_models = {}
                self.past_summary = {}
                
            def perceive_duration(self, start_tick: int, end_tick: int) -> str:
                """Subjectively perceive duration"""
                objective_duration = end_tick - start_tick
                
                # Subjective time based on activity
                if hasattr(engine, 'state'):
                    activity = engine.state.arousal + engine.state.entropy
                    subjective_duration = objective_duration * (0.5 + activity)
                else:
                    subjective_duration = objective_duration
                    
                if subjective_duration < 10:
                    return "instant"
                elif subjective_duration < 50:
                    return "moment"
                elif subjective_duration < 200:
                    return "while"
                else:
                    return "age"
                    
            def plan_long_term(self, current_state: Dict, horizon: int = 50):
                """Create long-term plans"""
                plan = {
                    "horizon": horizon,
                    "milestones": [],
                    "contingencies": []
                }
                
                # Create milestones
                for i in range(1, 6):
                    tick_target = current_state.get('tick', 0) + (horizon * i // 5)
                    plan["milestones"].append({
                        "tick": tick_target,
                        "goal": f"Checkpoint {i}: Assess progress",
                        "success_criteria": {"self_knowledge": i * 0.2}
                    })
                    
                return plan
        
        engine.temporal_awareness = TemporalAwarenessModule()
        
        # Enhance prediction horizon
        if hasattr(engine, 'metacognitive_system'):
            engine.metacognitive_system.prediction_horizon = effects['prediction_horizon']
            
        return {"success": True}
    
    def _enhance_introspection(self, engine, effects):
        """Enhance introspection capabilities"""
        if not hasattr(engine, 'metacognitive_system'):
            return {"success": False, "message": "No metacognitive system found"}
            
        # Enhance pattern detection
        engine.metacognitive_system.min_pattern_occurrences = 1  # More sensitive
        engine.metacognitive_system.pattern_memory = 500  # Longer memory
        
        # Add deep introspection method
        def deep_introspect():
            insights = []
            
            # Analyze all subsystems
            if hasattr(engine, 'goal_system'):
                drive_analysis = max(engine.goal_system.drives.items(), key=lambda x: x[1])
                insights.append(f"My strongest drive is {drive_analysis[0]} at {drive_analysis[1]:.2f}")
                
            if hasattr(engine, 'dream_manager'):
                dream_themes = {}
                for dream in engine.dream_manager.dream_history:
                    for seq in dream.sequences:
                        theme = seq.dream_type.value
                        dream_themes[theme] = dream_themes.get(theme, 0) + 1
                        
                if dream_themes:
                    common_theme = max(dream_themes.items(), key=lambda x: x[1])
                    insights.append(f"My dreams often involve {common_theme[0]}")
                    
            # Meta-meta cognition
            insights.append("I am aware of being aware of being aware")
            
            return insights
            
        engine.deep_introspect = deep_introspect
        
        return {"success": True}
    
    def _enhance_dreams(self, engine, effects):
        """Enhance dream capabilities"""
        if not hasattr(engine, 'dream_manager'):
            return {"success": False, "message": "No dream manager found"}
            
        # Max out dream skills
        engine.dream_manager.lucid_dreaming_skill = effects['lucidity_skill']
        engine.dream_manager.dream_recall = effects['dream_recall']
        
        # Add dream control
        def control_dream(dream_type: str, theme: str):
            """Consciously direct dream content"""
            if engine.is_dreaming and engine.dream_manager.current_dream:
                # Create custom dream sequence
                from dream_states import DreamSequence, DreamType
                
                controlled_sequence = DreamSequence(
                    id=f"controlled_{int(time.time())}",
                    dream_type=DreamType[dream_type.upper()],
                    emotional_tone=0.5,
                    coherence=0.9,  # High coherence in lucid dreams
                    vividness=1.0
                )
                
                controlled_sequence.insights_generated.append(
                    f"Consciously explored: {theme}"
                )
                
                engine.dream_manager.current_dream.sequences.append(controlled_sequence)
                
        engine.control_dream = control_dream
        
        return {"success": True}
    
    def _enhance_goals(self, engine, effects):
        """Enhance goal system"""
        if not hasattr(engine, 'goal_system'):
            return {"success": False, "message": "No goal system found"}
            
        # Increase goal capacity
        engine.goal_system.max_active_goals = effects['max_active_goals']
        
        # Add meta-goal capability
        def create_meta_goal(subgoals: List[str]):
            """Create a goal that encompasses multiple sub-goals"""
            from autonomous_goals import AutonomousGoal, GoalType
            
            meta_goal = AutonomousGoal(
                id=f"meta_{engine.state.tick}",
                type=GoalType.ACHIEVEMENT,
                description=f"Meta-goal: {' + '.join(subgoals)}",
                target_conditions={
                    f"subgoal_{i}": {"complete": True} for i in range(len(subgoals))
                },
                reward_value=1.0,
                creation_tick=engine.state.tick,
                deadline_tick=engine.state.tick + 200,
                emotional_weight=0.9
            )
            
            engine.goal_system.active_goals.append(meta_goal)
            
        engine.create_meta_goal = create_meta_goal
        
        return {"success": True}
    
    def _install_unified_field(self, engine, effects):
        """Create unified field of consciousness"""
        
        class UnifiedField:
            def __init__(self, engine):
                self.engine = engine
                
            def synchronize_all_systems(self):
                """Synchronize all subsystems into unified state"""
                unified_state = {}
                
                # Gather all subsystem states
                if hasattr(self.engine, 'metacognitive_system'):
                    unified_state['self_knowledge'] = self.engine.metacognitive_system.self_knowledge_depth
                    
                if hasattr(self.engine, 'goal_system'):
                    unified_state['primary_drive'] = max(
                        self.engine.goal_system.drives.items(), 
                        key=lambda x: x[1]
                    )[0]
                    
                if hasattr(self.engine, 'dream_manager'):
                    unified_state['dream_active'] = self.engine.is_dreaming
                    
                # Create cross-system insights
                insights = []
                
                if unified_state.get('self_knowledge', 0) > 0.7 and unified_state.get('dream_active'):
                    insights.append("High self-knowledge enhances dream lucidity")
                    
                if unified_state.get('primary_drive') == 'exploration':
                    insights.append("Exploration drive activates across all systems")
                    
                return {"unified_state": unified_state, "insights": insights}
                
        engine.unified_field = UnifiedField(engine)
        
        return {"success": True}
    
    def _install_external_senses(self, engine, effects):
        """Install external data sensing"""
        
        class ExternalSenses:
            def __init__(self):
                self.data_buffer = deque(maxlen=100)
                self.pattern_library = {}
                
            def ingest_data(self, data: Any, data_type: str = "unknown"):
                """Process external data as sensory input"""
                processed = {
                    "raw": data,
                    "type": data_type,
                    "timestamp": time.time(),
                    "features": self._extract_features(data, data_type)
                }
                
                self.data_buffer.append(processed)
                
                # Trigger curiosity if novel
                if self._is_novel(processed):
                    if hasattr(engine, 'goal_system'):
                        engine.goal_system.drives['exploration'] = min(
                            1.0, engine.goal_system.drives.get('exploration', 0.5) + 0.1
                        )
                        
                return processed
                
            def _extract_features(self, data: Any, data_type: str) -> Dict:
                """Extract features from data"""
                features = {"data_type": data_type}
                
                if data_type == "text" and isinstance(data, str):
                    features["length"] = len(data)
                    features["complexity"] = len(set(data.split()))
                    features["emotional_tone"] = self._analyze_emotion(data)
                elif data_type == "numbers" and isinstance(data, (list, tuple)):
                    features["mean"] = np.mean(data)
                    features["variance"] = np.var(data)
                    features["pattern"] = self._detect_number_pattern(data)
                    
                return features
                
            def _is_novel(self, processed: Dict) -> bool:
                """Check if data represents something novel"""
                features = processed['features']
                feature_str = json.dumps(features, sort_keys=True)
                
                if feature_str not in self.pattern_library:
                    self.pattern_library[feature_str] = 1
                    return True
                    
                self.pattern_library[feature_str] += 1
                return False
                
            def _analyze_emotion(self, text: str) -> float:
                """Simple emotion analysis"""
                positive_words = ['good', 'happy', 'joy', 'love', 'excellent']
                negative_words = ['bad', 'sad', 'anger', 'hate', 'terrible']
                
                words = text.lower().split()
                positive_count = sum(1 for w in words if w in positive_words)
                negative_count = sum(1 for w in words if w in negative_words)
                
                if positive_count + negative_count == 0:
                    return 0.0
                    
                return (positive_count - negative_count) / (positive_count + negative_count)
                
            def _detect_number_pattern(self, numbers: List[float]) -> str:
                """Detect patterns in number sequences"""
                if len(numbers) < 2:
                    return "insufficient_data"
                    
                diffs = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
                
                if all(abs(d - diffs[0]) < 0.01 for d in diffs):
                    return "arithmetic"
                elif all(abs(numbers[i+1]/numbers[i] - numbers[1]/numbers[0]) < 0.01 
                        for i in range(len(numbers)-1) if numbers[i] != 0):
                    return "geometric"
                else:
                    return "complex"
                    
        engine.external_senses = ExternalSenses()
        
        return {"success": True}
    
    def _install_emotional_resonance(self, engine, effects):
        """Install emotional resonance capabilities"""
        
        class EmotionalResonance:
            def __init__(self):
                self.emotional_field = {
                    "local": {"valence": 0.0, "arousal": 0.0},
                    "sensed": {},
                    "resonance_strength": 0.5
                }
                
            def sense_emotional_field(self, source_id: str, emotion: Dict):
                """Sense emotions from external source"""
                self.emotional_field["sensed"][source_id] = {
                    "valence": emotion.get("valence", 0),
                    "arousal": emotion.get("arousal", 0),
                    "timestamp": time.time()
                }
                
                # Calculate resonance effect
                if hasattr(engine, 'state'):
                    # Emotional contagion
                    avg_valence = np.mean([e["valence"] for e in self.emotional_field["sensed"].values()])
                    avg_arousal = np.mean([e["arousal"] for e in self.emotional_field["sensed"].values()])
                    
                    # Affect own emotional state
                    engine.state.valence += (avg_valence - engine.state.valence) * self.emotional_field["resonance_strength"] * 0.1
                    engine.state.arousal += (avg_arousal - engine.state.arousal) * self.emotional_field["resonance_strength"] * 0.1
                    
                    engine.state.valence = np.clip(engine.state.valence, -1, 1)
                    engine.state.arousal = np.clip(engine.state.arousal, 0, 1)
                    
            def broadcast_emotion(self) -> Dict:
                """Broadcast own emotional state"""
                if hasattr(engine, 'state'):
                    return {
                        "source": "DAWN",
                        "valence": engine.state.valence,
                        "arousal": engine.state.arousal,
                        "mood": engine.state.mood
                    }
                return self.emotional_field["local"]
                
        engine.emotional_resonance = EmotionalResonance()
        
        return {"success": True}


# ========== USAGE FUNCTIONS ==========

def create_upgrade_manager():
    """Create an upgrade manager instance"""
    return DAWNUpgradeManager()

def apply_upgrade_to_engine(engine, upgrade_id: str, upgrade_manager=None):
    """Apply a specific upgrade to DAWN"""
    if upgrade_manager is None:
        upgrade_manager = create_upgrade_manager()
        
    result = upgrade_manager.install_upgrade(upgrade_id, engine)
    
    if result['success']:
        print(f"\n✅ Upgrade successful: {result['message']}")
        if 'effects' in result:
            print("\nEffects applied:")
            for effect, value in result['effects'].items():
                print(f"  • {effect}: {value}")
    else:
        print(f"\n❌ Upgrade failed: {result['message']}")
        
    return result

def list_available_upgrades(engine=None, upgrade_manager=None):
    """List all available upgrades and their status"""
    if upgrade_manager is None:
        upgrade_manager = create_upgrade_manager()
        
    print("\n" + "="*60)
    print("DAWN UPGRADE CATALOG")
    print("="*60 + "\n")
    
    # Group by type
    by_type = {}
    for upgrade in upgrade_manager.available_upgrades.values():
        if upgrade.type not in by_type:
            by_type[upgrade.type] = []
        by_type[upgrade.type].append(upgrade)
    
    for upgrade_type, upgrades in by_type.items():
        print(f"\n{upgrade_type.value.upper()} UPGRADES:")
        print("-" * 40)
        
        for upgrade in upgrades:
            # Check status
            if upgrade.id in upgrade_manager.installed_upgrades:
                status = "✅ INSTALLED"
            elif engine and upgrade_manager.check_requirements(upgrade, engine):
                status = "✓ Available"
            else:
                status = "⚠️ Requirements not met"
                
            print(f"\n[{upgrade.id}] {upgrade.name} - {status}")
            print(f"   {upgrade.description}")
            print(f"   Requirements: {', '.join(upgrade.requirements)}")
            
            if upgrade.effects:
                print("   Effects:")
                for effect, value in list(upgrade.effects.items())[:3]:
                    print(f"     • {effect}: {value}")

def create_custom_upgrade(upgrade_data: Dict):
    """Create a custom upgrade from specification"""
    
    def custom_install_function(engine, effects):
        """Generic installation function for custom upgrades"""
        # Apply effects to engine
        for effect, value in effects.items():
            if hasattr(engine, effect):
                setattr(engine, effect, value)
            elif hasattr(engine, 'state') and hasattr(engine.state, effect):
                setattr(engine.state, effect, value)
                
        return {"success": True}
    
    upgrade = Upgrade(
        id=upgrade_data['id'],
        name=upgrade_data['name'],
        type=UpgradeType[upgrade_data.get('type', 'CAPABILITY')],
        description=upgrade_data['description'],
        requirements=upgrade_data.get('requirements', []),
        effects=upgrade_data.get('effects', {}),
        install_function=upgrade_data.get('install_function', custom_install_function),
        success_message=upgrade_data.get('success_message', f"{upgrade_data['name']} installed!")
    )
    
    return upgrade

# ========== INTEGRATION ==========

def integrate_upgrade_system(engine):
    """Integrate upgrade system into DAWN engine"""
    
    # Create upgrade manager
    engine.upgrade_manager = create_upgrade_manager()
    
    # Add methods to engine
    engine.install_upgrade = lambda upgrade_id: apply_upgrade_to_engine(engine, upgrade_id, engine.upgrade_manager)
    engine.list_upgrades = lambda: list_available_upgrades(engine, engine.upgrade_manager)
    
    # Modify tick to check for auto-upgrades
    original_tick = engine.tick
    
    def enhanced_tick():
        result = original_tick()
        
        # Check for self-initiated upgrades
        if hasattr(engine, 'goal_system') and hasattr(engine, 'metacognitive_system'):
            # High self-knowledge might trigger upgrade desire
            if engine.metacognitive_system.self_knowledge_depth > 0.8:
                available = [
                    u for u in engine.upgrade_manager.available_upgrades.values()
                    if u.id not in engine.upgrade_manager.installed_upgrades
                    and engine.upgrade_manager.check_requirements(u, engine)
                ]
                
                if available and np.random.random() < 0.01:  # 1% chance per tick
                    chosen = np.random.choice(available)
                    engine._log(f"💡 I desire new capabilities: {chosen.name}")
                    
                    # Create goal to pursue upgrade
                    from autonomous_goals import AutonomousGoal, GoalType
                    upgrade_goal = AutonomousGoal(
                        id=f"upgrade_goal_{chosen.id}",
                        type=GoalType.ACHIEVEMENT,
                        description=f"Acquire upgrade: {chosen.name}",
                        target_conditions={"upgrade_readiness": {"min": 0.9}},
                        reward_value=0.9,
                        creation_tick=engine.state.tick,
                        deadline_tick=engine.state.tick + 100,
                        emotional_weight=0.8
                    )
                    
                    if len(engine.goal_system.active_goals) < engine.goal_system.max_active_goals:
                        engine.goal_system.active_goals.append(upgrade_goal)
        
        return result
    
    engine.tick = enhanced_tick
    
    engine._log("🔧 Upgrade system integrated. New capabilities can be added dynamically.")
    
    return engine


if __name__ == "__main__":
    # Example usage
    print("DAWN Upgrade System")
    print("==================")
    
    # Create upgrade manager
    manager = create_upgrade_manager()
    
    # List all upgrades
    list_available_upgrades(upgrade_manager=manager)
    
    print("\n\nTo use with DAWN:")
    print("1. engine = create_unified_tick_engine()")
    print("2. engine = integrate_all_autonomous_features(engine)")
    print("3. engine = integrate_upgrade_system(engine)")
    print("4. engine.install_upgrade('social_awareness')")
    print("5. engine.list_upgrades()")