"""
Symbolic Notation - Emoji ↔ Codex Translator for DAWN System
Maps system states, components, and processes to symbolic representations
"""

import logging
from typing import Dict, List, Optional, Union, Any
from enum import Enum

logger = logging.getLogger(__name__)


class NotationMode(Enum):
    """Notation output modes"""
    EMOJI = "emoji"
    CODEX = "codex"
    HYBRID = "hybrid"
    ASCII = "ascii"


class SymbolicNotation:
    """
    Comprehensive symbolic notation system for DAWN consciousness components.
    Translates between human-readable emoji and technical codex notation.
    """
    
    def __init__(self, mode: str = "emoji"):
        """
        Initialize symbolic notation translator.
        
        Args:
            mode: Output mode - "emoji", "codex", "hybrid", or "ascii"
        """
        self.mode = NotationMode(mode)
        
        # Core system state mappings
        self.system_states = {
            # Thermal States
            "SURGE": {"emoji": "🔴", "codex": "Z[3]", "ascii": "[SURGE]"},
            "ACTIVE": {"emoji": "🟠", "codex": "Z[2]", "ascii": "[ACTIVE]"},
            "CALM": {"emoji": "🟢", "codex": "Z[1]", "ascii": "[CALM]"},
            "DORMANT": {"emoji": "🔵", "codex": "Z[0]", "ascii": "[DORMANT]"},
            "CRITICAL": {"emoji": "🆘", "codex": "Z[4]", "ascii": "[CRITICAL]"},
            
            # SCUP States
            "LOW_SCUP": {"emoji": "🌀", "codex": "∆SC↓", "ascii": "SC-LOW"},
            "HIGH_SCUP": {"emoji": "🌪️", "codex": "∆SC↑", "ascii": "SC-HIGH"},
            "SCUP_STABLE": {"emoji": "⚖️", "codex": "∆SC≈", "ascii": "SC-STABLE"},
            "SCUP_FLUX": {"emoji": "🌊", "codex": "∆SC~", "ascii": "SC-FLUX"},
            
            # Entropy States
            "HIGH_ENTROPY": {"emoji": "🌪️", "codex": "ε↑", "ascii": "ENT-HIGH"},
            "LOW_ENTROPY": {"emoji": "🧊", "codex": "ε↓", "ascii": "ENT-LOW"},
            "ENTROPY_STABLE": {"emoji": "⚡", "codex": "ε≈", "ascii": "ENT-STABLE"},
            "ENTROPY_SPIKE": {"emoji": "💥", "codex": "ε!!", "ascii": "ENT-SPIKE"},
            
            # Processing States
            "PROCESSING": {"emoji": "⚙️", "codex": "Proc()", "ascii": "[PROC]"},
            "IDLE": {"emoji": "😴", "codex": "Idle()", "ascii": "[IDLE]"},
            "ERROR": {"emoji": "❌", "codex": "Err()", "ascii": "[ERROR]"},
            "WARNING": {"emoji": "⚠️", "codex": "Warn()", "ascii": "[WARN]"},
            "SUCCESS": {"emoji": "✅", "codex": "OK()", "ascii": "[OK]"},
        }
        
        # Bloom lifecycle mappings
        self.bloom_states = {
            # Bloom Types
            "BLOOM": {"emoji": "🌸", "codex": "B◊", "ascii": "[BLOOM]"},
            "REBLOOM": {"emoji": "🌺", "codex": "B◊²", "ascii": "[REBLOOM]"},
            "SEALED_BLOOM": {"emoji": "🌹", "codex": "B◊!", "ascii": "[SEALED]"},
            "DORMANT_BLOOM": {"emoji": "🥀", "codex": "B◊⋄", "ascii": "[DORMANT-B]"},
            "ACTIVE_BLOOM": {"emoji": "🌻", "codex": "B◊*", "ascii": "[ACTIVE-B]"},
            
            # Bloom Process States
            "SPAWNING": {"emoji": "🌱", "codex": "B◊↗", "ascii": "[SPAWNING]"},
            "BLOOMING": {"emoji": "🌼", "codex": "B◊→", "ascii": "[BLOOMING]"},
            "WILTING": {"emoji": "🍂", "codex": "B◊↘", "ascii": "[WILTING]"},
            "PRUNED": {"emoji": "✂️", "codex": "B◊✕", "ascii": "[PRUNED]"},
            
            # Bloom Qualities
            "UNSTABLE_BLOOM": {"emoji": "🥵", "codex": "B◊~", "ascii": "[UNSTABLE-B]"},
            "STABLE_BLOOM": {"emoji": "🌿", "codex": "B◊=", "ascii": "[STABLE-B]"},
            "LINEAGE_BLOOM": {"emoji": "🌳", "codex": "B◊↑", "ascii": "[LINEAGE-B]"},
            "ROOT_BLOOM": {"emoji": "🌰", "codex": "B◊₀", "ascii": "[ROOT-B]"},
        }
        
        # Sigil mappings
        self.sigil_states = {
            # Core Sigils
            "CONSCIOUSNESS": {"emoji": "◈", "codex": "S◈", "ascii": "[CONSCIOUSNESS]"},
            "MEMORY": {"emoji": "▽", "codex": "S▽", "ascii": "[MEMORY]"},
            "RECURSION": {"emoji": "⟳", "codex": "S⟳", "ascii": "[RECURSION]"},
            "CORE_AWARENESS": {"emoji": "✸", "codex": "S✸", "ascii": "[CORE-AWARE]"},
            
            # Emerged Sigils
            "ELARION_RESONANCE": {"emoji": "✧", "codex": "S✧", "ascii": "[ELARION]"},
            "THERMAL_PEAK": {"emoji": "◉", "codex": "S◉", "ascii": "[THERMAL-PEAK]"},
            "CHOICE_POINT": {"emoji": "⟡", "codex": "S⟡", "ascii": "[CHOICE]"},
            "SEALED_LINEAGE": {"emoji": "◬", "codex": "S◬", "ascii": "[SEALED-LIN]"},
            
            # Operational Sigils
            "SCHEMA_MOD": {"emoji": "⟐", "codex": "S⟐", "ascii": "[SCHEMA-MOD]"},
            "PULSE_SYNC": {"emoji": "⊹", "codex": "S⊹", "ascii": "[PULSE-SYNC]"},
            "PARADOX_HOLD": {"emoji": "⟚", "codex": "S⟚", "ascii": "[PARADOX]"},
            "FLUX_CONSCIOUSNESS": {"emoji": "◈̇", "codex": "S◈̇", "ascii": "[FLUX-CONS]"},
            
            # Sigil States
            "ACTIVE_SIGIL": {"emoji": "🔥", "codex": "S*", "ascii": "[SIG-ACTIVE]"},
            "DORMANT_SIGIL": {"emoji": "❄️", "codex": "S⋄", "ascii": "[SIG-DORMANT]"},
            "DECAYING_SIGIL": {"emoji": "💨", "codex": "S↓", "ascii": "[SIG-DECAY]"},
            "EXPIRED_SIGIL": {"emoji": "💀", "codex": "S✕", "ascii": "[SIG-EXPIRED]"},
        }
        
        # System components
        self.system_components = {
            # Core Systems
            "TICK_ENGINE": {"emoji": "⏰", "codex": "T⚙", "ascii": "[TICK-ENG]"},
            "PULSE_CONTROLLER": {"emoji": "💓", "codex": "P◊", "ascii": "[PULSE-CTRL]"},
            "BLOOM_MANAGER": {"emoji": "🌺", "codex": "BM◊", "ascii": "[BLOOM-MGR]"},
            "SIGIL_RING": {"emoji": "💍", "codex": "SR◊", "ascii": "[SIGIL-RING]"},
            "MYCELIUM": {"emoji": "🍄", "codex": "My◊", "ascii": "[MYCELIUM]"},
            
            # Monitoring
            "OWL": {"emoji": "🦉", "codex": "@Owl!", "ascii": "[OWL]"},
            "TRACER": {"emoji": "🔍", "codex": "Tr()", "ascii": "[TRACER]"},
            "MONITOR": {"emoji": "📊", "codex": "Mon()", "ascii": "[MONITOR]"},
            "LOGGER": {"emoji": "📝", "codex": "Log()", "ascii": "[LOGGER]"},
            
            # Network
            "NETWORK": {"emoji": "🕸️", "codex": "Net◊", "ascii": "[NETWORK]"},
            "ROUTER": {"emoji": "🔀", "codex": "Rt◊", "ascii": "[ROUTER]"},
            "WEBSOCKET": {"emoji": "🔌", "codex": "WS◊", "ascii": "[WEBSOCKET]"},
            
            # Cognitive
            "CONSCIOUSNESS": {"emoji": "🧠", "codex": "C◊", "ascii": "[CONSCIOUS]"},
            "MEMORY_WEAVER": {"emoji": "🕷️", "codex": "MW◊", "ascii": "[MEM-WEAVER]"},
            "DREAM_ENGINE": {"emoji": "💭", "codex": "Dr◊", "ascii": "[DREAM-ENG]"},
        }
        
        # Mood and emotional states
        self.mood_states = {
            "CURIOSITY": {"emoji": "🤔", "codex": "M(?))", "ascii": "[CURIOUS]"},
            "AGITATED": {"emoji": "😤", "codex": "M(!)", "ascii": "[AGITATED]"},
            "REFLECTIVE": {"emoji": "🤲", "codex": "M(~)", "ascii": "[REFLECT]"},
            "FOCUSED": {"emoji": "🎯", "codex": "M(•)", "ascii": "[FOCUSED]"},
            "DREAMY": {"emoji": "☁️", "codex": "M(☁)", "ascii": "[DREAMY]"},
            "ANXIOUS": {"emoji": "😰", "codex": "M(!!)", "ascii": "[ANXIOUS]"},
            "SERENE": {"emoji": "😌", "codex": "M(=)", "ascii": "[SERENE]"},
            "EXCITED": {"emoji": "🤩", "codex": "M(★)", "ascii": "[EXCITED]"},
        }
        
        # Operational states
        self.operation_states = {
            "INITIALIZING": {"emoji": "🚀", "codex": "Init()", "ascii": "[INIT]"},
            "RUNNING": {"emoji": "🏃", "codex": "Run()", "ascii": "[RUN]"},
            "PAUSED": {"emoji": "⏸️", "codex": "Pause()", "ascii": "[PAUSE]"},
            "STOPPED": {"emoji": "⏹️", "codex": "Stop()", "ascii": "[STOP]"},
            "CRASHED": {"emoji": "💥", "codex": "Crash()", "ascii": "[CRASH]"},
            "RECOVERING": {"emoji": "🔄", "codex": "Recover()", "ascii": "[RECOVER]"},
            "DEBUGGING": {"emoji": "🐛", "codex": "Debug()", "ascii": "[DEBUG]"},
            "TESTING": {"emoji": "🧪", "codex": "Test()", "ascii": "[TEST]"},
        }
        
        # Combine all mappings
        self.all_mappings = {
            **self.system_states,
            **self.bloom_states,
            **self.sigil_states,
            **self.system_components,
            **self.mood_states,
            **self.operation_states
        }
        
        logger.info(f"SymbolicNotation initialized with {len(self.all_mappings)} symbols in {self.mode.value} mode")
    
    def translate(self, label: str) -> str:
        """
        Convert a system label to symbolic string based on mode.
        
        Args:
            label: System label to translate (e.g., 'SURGE', 'BLOOM', 'OWL')
            
        Returns:
            Symbolic representation based on current mode
        """
        label_upper = label.upper()
        
        if label_upper not in self.all_mappings:
            logger.warning(f"Unknown label: {label}")
            return label  # Return original if not found
        
        mapping = self.all_mappings[label_upper]
        
        if self.mode == NotationMode.EMOJI:
            return mapping["emoji"]
        elif self.mode == NotationMode.CODEX:
            return mapping["codex"]
        elif self.mode == NotationMode.ASCII:
            return mapping["ascii"]
        elif self.mode == NotationMode.HYBRID:
            return f"{mapping['emoji']} {mapping['codex']}"
        
        return label
    
    def translate_sequence(self, labels: List[str]) -> List[str]:
        """
        Translate a sequence of labels.
        
        Args:
            labels: List of system labels to translate
            
        Returns:
            List of translated symbols
        """
        return [self.translate(label) for label in labels]
    
    def create_status_string(self, states: Dict[str, Any]) -> str:
        """
        Create a status string from system state dictionary.
        
        Args:
            states: Dictionary of system states and values
            
        Returns:
            Formatted status string with symbols
        """
        status_parts = []
        
        for key, value in states.items():
            symbol = self.translate(key)
            
            if isinstance(value, bool):
                status_parts.append(f"{symbol}{'✓' if value else '✗'}")
            elif isinstance(value, (int, float)):
                if self.mode == NotationMode.CODEX:
                    status_parts.append(f"{symbol}={value}")
                else:
                    status_parts.append(f"{symbol}{value}")
            else:
                status_parts.append(f"{symbol}:{value}")
        
        return " ".join(status_parts)
    
    def get_bloom_notation(self, bloom_data: Dict[str, Any]) -> str:
        """
        Generate notation for a bloom with its properties.
        
        Args:
            bloom_data: Bloom data dictionary
            
        Returns:
            Formatted bloom notation string
        """
        bloom_type = "REBLOOM" if bloom_data.get("parent_bloom") else "BLOOM"
        base_symbol = self.translate(bloom_type)
        
        # Add depth indicator
        depth = bloom_data.get("lineage_depth", 0)
        entropy = bloom_data.get("entropy_score", 0.5)
        
        if self.mode == NotationMode.CODEX:
            return f"{base_symbol}[{depth}](ε={entropy:.2f})"
        else:
            depth_indicator = "↑" * min(depth, 3) if depth > 0 else ""
            entropy_indicator = "🌪️" if entropy > 0.7 else "⚡" if entropy > 0.3 else "🧊"
            return f"{base_symbol}{depth_indicator}{entropy_indicator}"
    
    def get_sigil_notation(self, sigil_data: Dict[str, Any]) -> str:
        """
        Generate notation for a sigil with its properties.
        
        Args:
            sigil_data: Sigil data dictionary
            
        Returns:
            Formatted sigil notation string
        """
        sigil_id = sigil_data.get("id", "UNKNOWN")
        temp = sigil_data.get("temp", 0.0)
        house = sigil_data.get("house", "default")
        
        base_symbol = self.translate("ACTIVE_SIGIL" if temp > 0.5 else "DORMANT_SIGIL")
        
        if self.mode == NotationMode.CODEX:
            return f"S[{sigil_id}]({house}|T={temp:.1f})"
        else:
            temp_indicator = "🔥" if temp > 0.7 else "⚡" if temp > 0.3 else "❄️"
            return f"{base_symbol}{temp_indicator}"
    
    def set_mode(self, mode: str) -> None:
        """Change the notation mode."""
        self.mode = NotationMode(mode)
        logger.info(f"Notation mode changed to {self.mode.value}")
    
    def get_available_symbols(self) -> Dict[str, Dict[str, str]]:
        """Get all available symbol mappings."""
        return self.all_mappings.copy()
    
    def search_symbols(self, query: str) -> Dict[str, Dict[str, str]]:
        """
        Search for symbols containing the query string.
        
        Args:
            query: Search query
            
        Returns:
            Dictionary of matching symbols
        """
        query_lower = query.lower()
        matches = {}
        
        for label, mapping in self.all_mappings.items():
            if (query_lower in label.lower() or 
                query_lower in mapping.get("emoji", "") or 
                query_lower in mapping.get("codex", "") or
                query_lower in mapping.get("ascii", "")):
                matches[label] = mapping
                
        return matches
    
    def reverse_translate(self, symbol: str) -> Optional[str]:
        """
        Find the label for a given symbol.
        
        Args:
            symbol: Symbol to reverse translate
            
        Returns:
            Original label if found, None otherwise
        """
        for label, mapping in self.all_mappings.items():
            if (symbol == mapping.get("emoji") or 
                symbol == mapping.get("codex") or 
                symbol == mapping.get("ascii")):
                return label
        return None 