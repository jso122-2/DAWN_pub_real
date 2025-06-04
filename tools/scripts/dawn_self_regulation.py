#!/usr/bin/env python3
"""
DAWN Voice-to-Schema Interface
Maps natural language commands to internal schema processes
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass
from pathlib import Path
import speech_recognition as sr
from fuzzywuzzy import fuzz, process
import threading
import queue
import time

@dataclass
class SchemaAction:
    """Represents a schema-layer action that can be triggered"""
    name: str
    function: Callable
    parameters: Dict[str, Any]
    description: str
    aliases: List[str]
    category: str

@dataclass
class ParsedCommand:
    """Parsed voice command with intent and entities"""
    raw_text: str
    intent: str
    action: str
    target: Optional[str] = None
    modifier: Optional[str] = None
    value: Optional[Any] = None
    confidence: float = 0.0

class SchemaFunctionRegistry:
    """Registry of all available schema-layer functions"""
    
    def __init__(self, dawn_interface):
        self.dawn = dawn_interface
        self.actions = {}
        self._register_core_actions()
        
    def _register_core_actions(self):
        """Register DAWN's core schema functions"""
        
        # Bloom/Memory functions
        self.register_action(SchemaAction(
            name="pause_bloom",
            function=self.dawn.pause_bloom_motion,
            parameters={"vector": None},
            description="Pause bloom drift in specified vector",
            aliases=["freeze bloom", "stop bloom", "halt memory drift", "pause drift"],
            category="bloom"
        ))
        
        self.register_action(SchemaAction(
            name="accelerate_bloom",
            function=self.dawn.accelerate_bloom,
            parameters={"rate": 2.0},
            description="Accelerate bloom emergence rate",
            aliases=["speed up bloom", "faster memories", "quicken bloom"],
            category="bloom"
        ))
        
        # Tracer/Observer functions
        self.register_action(SchemaAction(
            name="summon_owl",
            function=self.dawn.activate_owl_observer,
            parameters={"overlay": True},
            description="Activate Owl meta-cognitive observer",
            aliases=["wake owl", "open owl", "activate observer", "meta view"],
            category="tracer"
        ))
        
        self.register_action(SchemaAction(
            name="release_ant",
            function=self.dawn.activate_ant_tracer,
            parameters={"swarm_size": 10},
            description="Release Ant entropy tracers",
            aliases=["deploy ants", "trace entropy", "map chaos", "send scouts"],
            category="tracer"
        ))
        
        # Entropy management
        self.register_action(SchemaAction(
            name="cool_entropy",
            function=self.dawn.trigger_cooling_loop,
            parameters={"sector": None, "intensity": 0.5},
            description="Reduce entropy in specified sector",
            aliases=["lower entropy", "cool down", "reduce chaos", "stabilize"],
            category="entropy"
        ))
        
        self.register_action(SchemaAction(
            name="heat_sector",
            function=self.dawn.increase_entropy,
            parameters={"sector": None, "amount": 0.3},
            description="Increase entropy in sector",
            aliases=["raise entropy", "heat up", "add chaos", "destabilize"],
            category="entropy"
        ))
        
        # Sigil operations
        self.register_action(SchemaAction(
            name="activate_sigil",
            function=self.dawn.activate_sigil,
            parameters={"sigil_id": None, "power": 1.0},
            description="Activate a specific sigil",
            aliases=["power sigil", "light sigil", "turn on sigil", "enable symbol"],
            category="sigil"
        ))
        
        self.register_action(SchemaAction(
            name="bind_sigils",
            function=self.dawn.bind_sigils,
            parameters={"sigil_a": None, "sigil_b": None},
            description="Create binding between sigils",
            aliases=["connect sigils", "link symbols", "merge sigils", "join symbols"],
            category="sigil"
        ))
        
        # SCUP management
        self.register_action(SchemaAction(
            name="boost_scup",
            function=self.dawn.boost_coherence,
            parameters={"amount": 0.2},
            description="Increase SCUP coherence",
            aliases=["raise scup", "improve coherence", "strengthen flow", "boost harmony"],
            category="scup"
        ))
        
        self.register_action(SchemaAction(
            name="fragment_scup",
            function=self.dawn.fragment_coherence,
            parameters={"severity": 0.3},
            description="Intentionally fragment SCUP",
            aliases=["break coherence", "shatter flow", "split scup", "divide harmony"],
            category="scup"
        ))
        
        # Schema health
        self.register_action(SchemaAction(
            name="repair_schema",
            function=self.dawn.repair_schema_damage,
            parameters={"focus_area": None},
            description="Repair schema damage in area",
            aliases=["fix schema", "heal damage", "mend structure", "restore health"],
            category="schema"
        ))
        
        self.register_action(SchemaAction(
            name="schema_audit",
            function=self.dawn.run_schema_audit,
            parameters={"depth": "full"},
            description="Run full schema health audit",
            aliases=["check schema", "audit health", "scan structure", "diagnose system"],
            category="schema"
        ))
        
        # Emotional regulation
        self.register_action(SchemaAction(
            name="dampen_emotion",
            function=self.dawn.engage_emotion_dampener,
            parameters={"level": 0.5},
            description="Engage emotional dampening",
            aliases=["calm emotions", "reduce feelings", "suppress emotion", "quiet mood"],
            category="emotion"
        ))
        
        self.register_action(SchemaAction(
            name="amplify_emotion",
            function=self.dawn.amplify_emotional_vector,
            parameters={"emotion": None, "factor": 1.5},
            description="Amplify specific emotion",
            aliases=["boost emotion", "increase feeling", "enhance mood", "strengthen emotion"],
            category="emotion"
        ))
        
    def register_action(self, action: SchemaAction):
        """Register a new schema action"""
        self.actions[action.name] = action
        
    def find_action(self, query: str) -> Tuple[Optional[SchemaAction], float]:
        """Find best matching action for query"""
        best_match = None
        best_score = 0
        
        query_lower = query.lower()
        
        # Check all actions and their aliases
        for action in self.actions.values():
            # Check main name
            score = fuzz.partial_ratio(query_lower, action.name.replace('_', ' '))
            if score > best_score:
                best_score = score
                best_match = action
                
            # Check aliases
            for alias in action.aliases:
                score = fuzz.partial_ratio(query_lower, alias)
                if score > best_score:
                    best_score = score
                    best_match = action
        
        return best_match, best_score / 100.0

class NaturalLanguageParser:
    """Parses natural language into schema commands"""
    
    def __init__(self, registry: SchemaFunctionRegistry):
        self.registry = registry
        
        # Entity patterns
        self.patterns = {
            'vectors': r'(?:vector\s+)?(?:alpha|beta|gamma|delta|epsilon|zeta|theta)',
            'sectors': r'(?:sector\s+)?(?:alpha|beta|gamma|delta|north|south|east|west|central)',
            'emotions': r'(?:curiosity|fear|joy|confusion|serenity|vigilance|defensive|wonder)',
            'values': r'(?:to\s+)?(\d+(?:\.\d+)?)|(?:by\s+)?(\d+(?:\.\d+)?)',
            'levels': r'(?:low|medium|high|minimal|moderate|maximum|full)',
            'sigils': r'sigil\s+(?:\w+)|symbol\s+(?:\w+)',
        }
        
        # Compile patterns
        self.compiled_patterns = {
            name: re.compile(pattern, re.IGNORECASE) 
            for name, pattern in self.patterns.items()
        }
        
        # Level mappings
        self.level_values = {
            'low': 0.2, 'minimal': 0.1,
            'medium': 0.5, 'moderate': 0.5,
            'high': 0.8, 'maximum': 1.0, 'full': 1.0
        }
        
    def parse_command(self, text: str) -> ParsedCommand:
        """Parse natural language command into structured format"""
        
        # Clean text
        text = text.strip().lower()
        
        # Find best matching action
        action, confidence = self.registry.find_action(text)
        
        if not action or confidence < 0.5:
            return ParsedCommand(
                raw_text=text,
                intent="unknown",
                action="unknown",
                confidence=confidence
            )
        
        # Extract entities based on action category
        parsed = ParsedCommand(
            raw_text=text,
            intent=action.category,
            action=action.name,
            confidence=confidence
        )
        
        # Extract vector/sector
        if action.category in ['bloom', 'entropy']:
            vector_match = self.compiled_patterns['vectors'].search(text)
            sector_match = self.compiled_patterns['sectors'].search(text)
            if vector_match:
                parsed.target = vector_match.group()
            elif sector_match:
                parsed.target = sector_match.group()
        
        # Extract emotion
        elif action.category == 'emotion':
            emotion_match = self.compiled_patterns['emotions'].search(text)
            if emotion_match:
                parsed.target = emotion_match.group()
        
        # Extract sigil references
        elif action.category == 'sigil':
            sigil_matches = self.compiled_patterns['sigils'].findall(text)
            if sigil_matches:
                parsed.target = sigil_matches[0] if len(sigil_matches) > 0 else None
                parsed.modifier = sigil_matches[1] if len(sigil_matches) > 1 else None
        
        # Extract numeric values
        value_match = self.compiled_patterns['values'].search(text)
        if value_match:
            parsed.value = float(value_match.group(1) or value_match.group(2))
        
        # Extract levels
        level_match = self.compiled_patterns['levels'].search(text)
        if level_match and not parsed.value:
            parsed.value = self.level_values.get(level_match.group(), 0.5)
        
        return parsed

class VoiceSchemaInterface:
    """Main voice-to-schema interface"""
    
    def __init__(self, dawn_interface, use_voice=True):
        self.dawn = dawn_interface
        self.registry = SchemaFunctionRegistry(dawn_interface)
        self.parser = NaturalLanguageParser(self.registry)
        self.use_voice = use_voice
        
        # Logging
        self.logger = logging.getLogger('DAWN_Voice')
        
        # Voice recognition setup
        if use_voice:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.voice_queue = queue.Queue()
            
        # Command history
        self.command_history = []
        
    def execute_parsed_command(self, parsed: ParsedCommand) -> Dict[str, Any]:
        """Execute a parsed command"""
        
        if parsed.confidence < 0.5:
            return {
                "success": False,
                "message": f"Command unclear. Did you mean something else? (confidence: {parsed.confidence:.2f})",
                "suggestions": self._get_suggestions(parsed.raw_text)
            }
        
        # Get the action
        action = self.registry.actions.get(parsed.action)
        if not action:
            return {
                "success": False,
                "message": f"Action '{parsed.action}' not found"
            }
        
        # Prepare parameters
        params = action.parameters.copy()
        
        # Update parameters based on parsed entities
        if parsed.target and 'sector' in params:
            params['sector'] = parsed.target
        elif parsed.target and 'vector' in params:
            params['vector'] = parsed.target
        elif parsed.target and 'emotion' in params:
            params['emotion'] = parsed.target
        elif parsed.target and 'sigil_id' in params:
            params['sigil_id'] = parsed.target
            
        if parsed.modifier and 'sigil_b' in params:
            params['sigil_a'] = parsed.target
            params['sigil_b'] = parsed.modifier
            
        if parsed.value is not None:
            # Find appropriate parameter for value
            for param_name in ['amount', 'level', 'intensity', 'rate', 'factor', 'power']:
                if param_name in params:
                    params[param_name] = parsed.value
                    break
        
        # Execute the action
        try:
            result = action.function(**params)
            
            # Log successful execution
            self.logger.info(f"Executed: {action.name} with params: {params}")
            
            return {
                "success": True,
                "action": action.name,
                "parameters": params,
                "result": result,
                "message": f"✓ {action.description}"
            }
            
        except Exception as e:
            self.logger.error(f"Error executing {action.name}: {str(e)}")
            return {
                "success": False,
                "message": f"Error executing command: {str(e)}"
            }
    
    def _get_suggestions(self, text: str) -> List[str]:
        """Get command suggestions for unclear input"""
        suggestions = []
        
        # Find top 3 similar commands
        all_commands = []
        for action in self.registry.actions.values():
            all_commands.append(action.name.replace('_', ' '))
            all_commands.extend(action.aliases)
        
        matches = process.extract(text, all_commands, limit=3)
        suggestions = [match[0] for match in matches if match[1] > 30]
        
        return suggestions
    
    def process_voice_command(self, audio=None) -> Dict[str, Any]:
        """Process voice input into schema command"""
        
        if not self.use_voice:
            return {"success": False, "message": "Voice input disabled"}
        
        try:
            # Convert speech to text
            if audio:
                text = self.recognizer.recognize_google(audio)
            else:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
            
            self.logger.info(f"Heard: '{text}'")
            
            # Parse and execute
            return self.process_text_command(text)
            
        except sr.WaitTimeoutError:
            return {"success": False, "message": "No speech detected"}
        except sr.UnknownValueError:
            return {"success": False, "message": "Could not understand speech"}
        except Exception as e:
            return {"success": False, "message": f"Voice error: {str(e)}"}
    
    def process_text_command(self, text: str) -> Dict[str, Any]:
        """Process text command"""
        
        # Parse command
        parsed = self.parser.parse_command(text)
        
        # Store in history
        self.command_history.append({
            "timestamp": time.time(),
            "raw_text": text,
            "parsed": parsed
        })
        
        # Execute
        result = self.execute_parsed_command(parsed)
        result["parsed"] = parsed
        
        return result
    
    def listen_continuous(self, callback=None):
        """Continuous listening mode"""
        
        if not self.use_voice:
            raise ValueError("Voice input not enabled")
        
        def audio_callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio)
                result = self.process_text_command(text)
                
                if callback:
                    callback(result)
                else:
                    print(f"\n>>> {text}")
                    print(f"<<< {result['message']}")
                    
            except sr.UnknownValueError:
                pass
            except Exception as e:
                self.logger.error(f"Recognition error: {e}")
        
        # Start listening in background
        stop_listening = self.recognizer.listen_in_background(
            self.microphone, audio_callback
        )
        
        return stop_listening

class MockDAWNInterface:
    """Mock DAWN interface for testing"""
    
    def __init__(self):
        self.state = {
            "bloom_paused": False,
            "owl_active": False,
            "entropy_levels": {},
            "active_sigils": [],
            "scup": 0.7,
            "schema_health": 0.85
        }
    
    def pause_bloom_motion(self, vector=None):
        self.state["bloom_paused"] = True
        return f"Bloom motion paused" + (f" in vector {vector}" if vector else "")
    
    def accelerate_bloom(self, rate=2.0):
        return f"Bloom rate accelerated by {rate}x"
    
    def activate_owl_observer(self, overlay=True):
        self.state["owl_active"] = True
        return "Owl observer activated" + (" with overlay" if overlay else "")
    
    def activate_ant_tracer(self, swarm_size=10):
        return f"Released {swarm_size} ant tracers"
    
    def trigger_cooling_loop(self, sector=None, intensity=0.5):
        sector = sector or "global"
        self.state["entropy_levels"][sector] = max(0, 
            self.state["entropy_levels"].get(sector, 0.5) - intensity)
        return f"Cooling loop triggered in {sector} at {intensity} intensity"
    
    def increase_entropy(self, sector=None, amount=0.3):
        sector = sector or "global"
        self.state["entropy_levels"][sector] = min(1.0,
            self.state["entropy_levels"].get(sector, 0.5) + amount)
        return f"Entropy increased in {sector} by {amount}"
    
    def activate_sigil(self, sigil_id=None, power=1.0):
        if sigil_id:
            self.state["active_sigils"].append(sigil_id)
        return f"Sigil {sigil_id or 'unknown'} activated at {power} power"
    
    def bind_sigils(self, sigil_a=None, sigil_b=None):
        return f"Binding created: {sigil_a or '?'} <-> {sigil_b or '?'}"
    
    def boost_coherence(self, amount=0.2):
        self.state["scup"] = min(1.0, self.state["scup"] + amount)
        return f"SCUP coherence boosted by {amount} to {self.state['scup']:.2f}"
    
    def fragment_coherence(self, severity=0.3):
        self.state["scup"] = max(0, self.state["scup"] - severity)
        return f"SCUP fragmented by {severity} to {self.state['scup']:.2f}"
    
    def repair_schema_damage(self, focus_area=None):
        self.state["schema_health"] = min(1.0, self.state["schema_health"] + 0.1)
        return f"Schema repair initiated" + (f" in {focus_area}" if focus_area else "")
    
    def run_schema_audit(self, depth="full"):
        return f"Running {depth} schema audit... Health: {self.state['schema_health']:.2f}"
    
    def engage_emotion_dampener(self, level=0.5):
        return f"Emotion dampener engaged at {level} level"
    
    def amplify_emotional_vector(self, emotion=None, factor=1.5):
        return f"Emotion {emotion or 'all'} amplified by {factor}x"


def main():
    """Test the voice-to-schema interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DAWN Voice-to-Schema Interface')
    parser.add_argument('--no-voice', action='store_true', help='Disable voice input')
    parser.add_argument('--test', action='store_true', help='Run test commands')
    
    args = parser.parse_args()
    
    # Initialize with mock DAWN interface
    dawn = MockDAWNInterface()
    interface = VoiceSchemaInterface(dawn, use_voice=not args.no_voice)
    
    if args.test:
        # Test various commands
        test_commands = [
            "pause drift vector alpha",
            "summon the owl",
            "lower entropy in sector delta",
            "boost coherence to maximum",
            "activate sigil phoenix with high power",
            "cool down the northern sector",
            "amplify curiosity by 2",
            "run full schema audit",
            "bind sigil alpha to sigil omega"
        ]
        
        print("=== TESTING NATURAL LANGUAGE PARSER ===\n")
        
        for cmd in test_commands:
            print(f"Command: '{cmd}'")
            result = interface.process_text_command(cmd)
            print(f"Result: {result['message']}")
            if result['success']:
                print(f"Action: {result['action']}")
                print(f"Params: {result['parameters']}")
            print("-" * 50)
    
    else:
        # Interactive mode
        print("DAWN Voice-to-Schema Interface")
        print("=" * 50)
        
        if interface.use_voice:
            print("Voice input enabled. Say 'exit' to quit.")
            print("Listening for commands...")
            
            # Start continuous listening
            stop_listening = interface.listen_continuous()
            
            try:
                # Keep running until interrupted
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                stop_listening(wait_for_stop=False)
                print("\nStopping voice interface...")
        
        else:
            print("Text input mode. Type 'exit' to quit.")
            
            while True:
                try:
                    cmd = input("\n> ")
                    if cmd.lower() in ['exit', 'quit']:
                        break
                        
                    result = interface.process_text_command(cmd)
                    print(f"\n{result['message']}")
                    
                    if not result['success'] and 'suggestions' in result:
                        print(f"Did you mean: {', '.join(result['suggestions'])}")
                        
                except KeyboardInterrupt:
                    break
            
            print("\nGoodbye!")


if __name__ == "__main__":
    main()