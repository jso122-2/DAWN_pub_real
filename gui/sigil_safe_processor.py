#!/usr/bin/env python3
"""
Safe Sigil Processor for DAWN GUI
Prevents undefined errors by validating and sanitizing sigil data
"""

import time
import random
import logging
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

class SafeSigilProcessor:
    """
    Processes and validates sigil data to prevent undefined errors in GUI
    """
    
    def __init__(self):
        self.default_symbols = ["🔥", "💧", "🌍", "🌪️", "🌟", "⚡", "🌙", "☀️", "❄️", "🌋"]
        self.valid_houses = ["fire", "water", "earth", "air", "void", "neutral"]
        self.house_symbols = {
            "fire": ["🔥", "🌋", "⚡", "☀️"],
            "water": ["💧", "🌊", "❄️", "🌙"],
            "earth": ["🌍", "🌱", "🏔️", "💎"],
            "air": ["🌪️", "☁️", "🕊️", "💨"],
            "void": ["🌌", "⚫", "🕳️", "🌑"],
            "neutral": ["⚪", "⭐", "✨", "🔮"]
        }
        
    def process_sigil_data(self, raw_data: Any) -> List[Dict[str, Any]]:
        """
        Safely process any sigil data into validated sigil objects
        
        Args:
            raw_data: Any type of input data that might contain sigils
            
        Returns:
            List of validated sigil dictionaries
        """
        try:
            logger.debug(f"Processing sigil data: {type(raw_data)}")
            
            # Handle None or empty
            if raw_data is None:
                logger.debug("Sigil data is None, returning empty list")
                return []
            
            # Handle different input types
            if isinstance(raw_data, list):
                return self._process_sigil_list(raw_data)
            elif isinstance(raw_data, dict):
                # Check if it's a single sigil or contains sigils
                if self._looks_like_sigil(raw_data):
                    validated = self._validate_single_sigil(raw_data, "processed_sigil")
                    return [validated] if validated else []
                else:
                    # Look for sigils field in the dict
                    sigils_field = raw_data.get("sigils", [])
                    return self.process_sigil_data(sigils_field)
            elif isinstance(raw_data, str):
                # Convert string to sigil
                converted = self._string_to_sigil(raw_data)
                return [converted] if converted else []
            else:
                logger.warning(f"Unknown sigil data type: {type(raw_data)}")
                return []
                
        except Exception as e:
            logger.error(f"Error processing sigil data: {e}")
            return []
    
    def _process_sigil_list(self, sigil_list: List[Any]) -> List[Dict[str, Any]]:
        """Process a list that might contain sigils"""
        validated_sigils = []
        
        for i, item in enumerate(sigil_list):
            try:
                if isinstance(item, dict):
                    validated = self._validate_single_sigil(item, f"list_sigil_{i}")
                    if validated:
                        validated_sigils.append(validated)
                elif isinstance(item, str):
                    converted = self._string_to_sigil(item, f"str_sigil_{i}")
                    if converted:
                        validated_sigils.append(converted)
                elif isinstance(item, (int, float)):
                    converted = self._number_to_sigil(item, f"num_sigil_{i}")
                    if converted:
                        validated_sigils.append(converted)
                else:
                    logger.debug(f"Skipping non-sigil item {i}: {type(item)}")
                    
            except Exception as e:
                logger.error(f"Error processing sigil item {i}: {e}")
                continue
        
        logger.debug(f"Processed {len(validated_sigils)} sigils from {len(sigil_list)} items")
        return validated_sigils
    
    def _validate_single_sigil(self, sigil_data: Dict[str, Any], default_id: str) -> Optional[Dict[str, Any]]:
        """Validate and sanitize a single sigil dictionary"""
        try:
            # Create safe sigil with all required fields
            safe_sigil = {
                "id": self._safe_string(sigil_data.get("id"), default_id),
                "symbol": self._safe_symbol(sigil_data.get("symbol")),
                "meaning": self._safe_string(sigil_data.get("meaning"), "Unknown sigil"),
                "house": self._safe_house(sigil_data.get("house")),
                "heat": self._safe_number(sigil_data.get("heat", 0.5), 0.0, 1.0),
                "decay": self._safe_number(sigil_data.get("decay", 0.8), 0.0, 1.0),
                "source": self._safe_string(sigil_data.get("source"), "system"),
                "timestamp": self._safe_timestamp(sigil_data.get("timestamp")),
                "x": self._safe_number(sigil_data.get("x"), 0.0, 1.0),
                "y": self._safe_number(sigil_data.get("y"), 0.0, 1.0)
            }
            
            # Generate position if not provided
            if safe_sigil["x"] is None:
                safe_sigil["x"] = random.uniform(0.1, 0.9)
            if safe_sigil["y"] is None:
                safe_sigil["y"] = random.uniform(0.1, 0.9)
            
            # Ensure symbol matches house if possible
            if safe_sigil["symbol"] == "⚪" and safe_sigil["house"] != "neutral":
                safe_sigil["symbol"] = random.choice(self.house_symbols.get(safe_sigil["house"], ["⚪"]))
            
            logger.debug(f"Validated sigil: {safe_sigil['id']} -> {safe_sigil['symbol']}")
            return safe_sigil
            
        except Exception as e:
            logger.error(f"Error validating sigil: {e}")
            return None
    
    def _string_to_sigil(self, text: str, sigil_id: str = None) -> Optional[Dict[str, Any]]:
        """Convert string to sigil"""
        if not text or not isinstance(text, str):
            return None
        
        # Use first emoji as symbol, or default
        symbol = text[0] if text and len(text) > 0 else "⚪"
        if not self._is_emoji(symbol):
            symbol = "⚪"
        
        return {
            "id": sigil_id or f"str_{hash(text) % 1000}",
            "symbol": symbol,
            "meaning": text[:50],  # Truncate long strings
            "house": "neutral",
            "heat": 0.5,
            "decay": 0.8,
            "source": "string_conversion",
            "timestamp": time.time(),
            "x": random.uniform(0.1, 0.9),
            "y": random.uniform(0.1, 0.9)
        }
    
    def _number_to_sigil(self, number: Union[int, float], sigil_id: str = None) -> Optional[Dict[str, Any]]:
        """Convert number to sigil"""
        try:
            value = float(number)
            if not (-1000 <= value <= 1000):  # Reasonable range
                return None
            
            # Map number to heat intensity
            heat = max(0.0, min(1.0, abs(value) / 10.0))
            
            return {
                "id": sigil_id or f"num_{int(abs(value))}",
                "symbol": "●",
                "meaning": f"Numeric value: {value:.2f}",
                "house": "neutral",
                "heat": heat,
                "decay": 0.8,
                "source": "numeric_conversion",
                "timestamp": time.time(),
                "x": random.uniform(0.1, 0.9),
                "y": random.uniform(0.1, 0.9)
            }
        except (ValueError, TypeError):
            return None
    
    def _looks_like_sigil(self, data: Dict[str, Any]) -> bool:
        """Check if a dictionary looks like a sigil object"""
        sigil_fields = ["symbol", "meaning", "house", "heat", "decay"]
        return any(field in data for field in sigil_fields)
    
    def _safe_string(self, value: Any, default: str = "") -> str:
        """Safely convert to string"""
        if value is None:
            return default
        try:
            return str(value)[:100]  # Limit length
        except:
            return default
    
    def _safe_symbol(self, value: Any) -> str:
        """Safely get symbol"""
        if value is None:
            return random.choice(self.default_symbols)
        
        try:
            symbol_str = str(value)
            if len(symbol_str) == 0:
                return "⚪"
            
            # Take first character/emoji
            first_char = symbol_str[0]
            if self._is_emoji(first_char) or first_char.isalnum():
                return first_char
            else:
                return "⚪"
        except:
            return "⚪"
    
    def _safe_house(self, value: Any) -> str:
        """Safely get house"""
        if value is None:
            return "neutral"
        
        try:
            house_str = str(value).lower()
            if house_str in self.valid_houses:
                return house_str
            else:
                return "neutral"
        except:
            return "neutral"
    
    def _safe_number(self, value: Any, min_val: float = 0.0, max_val: float = 1.0, default: float = None) -> float:
        """Safely convert to number in range"""
        if value is None:
            return default if default is not None else (min_val + max_val) / 2
        
        try:
            num = float(value)
            
            # Handle NaN and infinity
            if num != num:  # NaN check
                return default if default is not None else (min_val + max_val) / 2
            if num == float('inf') or num == float('-inf'):
                return max_val if num > 0 else min_val
            
            # Clamp to range
            return max(min_val, min(max_val, num))
            
        except (ValueError, TypeError):
            return default if default is not None else (min_val + max_val) / 2
    
    def _safe_timestamp(self, value: Any) -> float:
        """Safely get timestamp"""
        if value is None:
            return time.time()
        
        try:
            ts = float(value)
            # Check if reasonable timestamp (between 2020 and 2050)
            if 1577836800 <= ts <= 2524608000:  # 2020-01-01 to 2050-01-01
                return ts
            else:
                return time.time()
        except:
            return time.time()
    
    def _is_emoji(self, char: str) -> bool:
        """Check if character is likely an emoji"""
        if not char:
            return False
        try:
            # Simple emoji detection - check if it's in common emoji ranges
            code_point = ord(char[0]) if char else 0
            emoji_ranges = [
                (0x1F600, 0x1F64F),  # Emoticons
                (0x1F300, 0x1F5FF),  # Misc Symbols
                (0x1F680, 0x1F6FF),  # Transport
                (0x1F1E0, 0x1F1FF),  # Flags
                (0x2600, 0x26FF),    # Misc symbols
                (0x2700, 0x27BF),    # Dingbats
                (0xFE00, 0xFE0F),    # Variation Selectors
                (0x1F900, 0x1F9FF),  # Supplemental Symbols
            ]
            
            return any(start <= code_point <= end for start, end in emoji_ranges)
        except:
            return False
    
    def generate_fallback_sigils(self, count: int = 3) -> List[Dict[str, Any]]:
        """Generate fallback sigils when no valid data is available"""
        fallback_sigils = []
        
        for i in range(count):
            house = self.valid_houses[i % len(self.valid_houses)]
            symbol = random.choice(self.house_symbols.get(house, ["⚪"]))
            
            sigil = {
                "id": f"fallback_{i}",
                "symbol": symbol,
                "meaning": f"System fallback {i+1}",
                "house": house,
                "heat": random.uniform(0.2, 0.6),
                "decay": random.uniform(0.7, 0.9),
                "source": "fallback_generator",
                "timestamp": time.time(),
                "x": random.uniform(0.1, 0.9),
                "y": random.uniform(0.1, 0.9)
            }
            fallback_sigils.append(sigil)
        
        logger.info(f"Generated {count} fallback sigils")
        return fallback_sigils
    
    def ensure_minimum_sigils(self, sigils: List[Dict[str, Any]], minimum: int = 1) -> List[Dict[str, Any]]:
        """Ensure there are at least minimum number of sigils"""
        if len(sigils) >= minimum:
            return sigils
        
        needed = minimum - len(sigils)
        fallbacks = self.generate_fallback_sigils(needed)
        return sigils + fallbacks

# Convenience function for easy integration
def safe_process_sigils(raw_data: Any, minimum_sigils: int = 0) -> List[Dict[str, Any]]:
    """
    Convenience function to safely process sigil data
    
    Args:
        raw_data: Any input that might contain sigil data
        minimum_sigils: Minimum number of sigils to return (will generate fallbacks if needed)
        
    Returns:
        List of validated sigil dictionaries
    """
    processor = SafeSigilProcessor()
    validated_sigils = processor.process_sigil_data(raw_data)
    
    if minimum_sigils > 0:
        validated_sigils = processor.ensure_minimum_sigils(validated_sigils, minimum_sigils)
    
    return validated_sigils 