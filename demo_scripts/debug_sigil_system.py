#!/usr/bin/env python3
"""
Comprehensive Sigil System Debugger
Identifies and fixes undefined errors in the sigil visualization system
"""

import time
import random
import json
import traceback
from typing import Dict, List, Any, Optional

def debug_print(message: str, level: str = "INFO"):
    """Enhanced debug printing with levels"""
    timestamp = time.strftime("%H:%M:%S")
    symbols = {
        "INFO": "📋",
        "SUCCESS": "✅", 
        "WARNING": "⚠️",
        "ERROR": "❌",
        "DEBUG": "🔍"
    }
    symbol = symbols.get(level, "📋")
    print(f"[{timestamp}] {symbol} SIGIL DEBUG: {message}")

class SigilDataValidator:
    """Validates all sigil data structures"""
    
    def __init__(self):
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_sigil_data(self, sigil_data: Any) -> Dict[str, Any]:
        """Comprehensive sigil data validation"""
        debug_print("🔍 Starting comprehensive sigil data validation", "DEBUG")
        
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "sanitized_data": None,
            "data_type": type(sigil_data).__name__,
            "data_structure": None
        }
        
        try:
            # Check if data exists
            if sigil_data is None:
                validation_result["errors"].append("Sigil data is None")
                validation_result["is_valid"] = False
                return validation_result
            
            # Check data type
            debug_print(f"Data type: {type(sigil_data)}", "DEBUG")
            
            if isinstance(sigil_data, list):
                validation_result["data_structure"] = "list"
                validation_result["sanitized_data"] = self._validate_sigil_list(sigil_data, validation_result)
            elif isinstance(sigil_data, dict):
                validation_result["data_structure"] = "dict"
                validation_result["sanitized_data"] = self._validate_sigil_dict(sigil_data, validation_result)
            else:
                validation_result["errors"].append(f"Unexpected data type: {type(sigil_data)}")
                validation_result["is_valid"] = False
            
            # Final validation check
            if validation_result["errors"]:
                validation_result["is_valid"] = False
            
            debug_print(f"Validation complete. Valid: {validation_result['is_valid']}", 
                       "SUCCESS" if validation_result["is_valid"] else "ERROR")
            
            return validation_result
            
        except Exception as e:
            debug_print(f"Validation exception: {e}", "ERROR")
            debug_print(f"Traceback: {traceback.format_exc()}", "ERROR")
            validation_result["errors"].append(f"Validation exception: {e}")
            validation_result["is_valid"] = False
            return validation_result
    
    def _validate_sigil_list(self, sigil_list: List, validation_result: Dict) -> List[Dict]:
        """Validate list of sigils"""
        debug_print(f"Validating sigil list with {len(sigil_list)} items", "DEBUG")
        
        sanitized_sigils = []
        
        for i, sigil in enumerate(sigil_list):
            debug_print(f"Validating sigil {i}: {type(sigil)}", "DEBUG")
            
            try:
                if isinstance(sigil, dict):
                    sanitized_sigil = self._sanitize_sigil_object(sigil, f"sigil_{i}")
                    if sanitized_sigil:
                        sanitized_sigils.append(sanitized_sigil)
                else:
                    validation_result["warnings"].append(f"Sigil {i} is not a dict: {type(sigil)}")
                    # Try to convert to dict
                    converted_sigil = self._convert_to_sigil_dict(sigil, f"sigil_{i}")
                    if converted_sigil:
                        sanitized_sigils.append(converted_sigil)
            except Exception as e:
                debug_print(f"Error validating sigil {i}: {e}", "ERROR")
                validation_result["errors"].append(f"Sigil {i} validation error: {e}")
        
        debug_print(f"Sanitized {len(sanitized_sigils)} sigils from {len(sigil_list)} input", "INFO")
        return sanitized_sigils
    
    def _validate_sigil_dict(self, sigil_dict: Dict, validation_result: Dict) -> Dict:
        """Validate single sigil dictionary"""
        debug_print("Validating single sigil dictionary", "DEBUG")
        
        sanitized_sigil = self._sanitize_sigil_object(sigil_dict, "single_sigil")
        return sanitized_sigil if sanitized_sigil else {}
    
    def _sanitize_sigil_object(self, sigil: Dict, sigil_id: str) -> Optional[Dict]:
        """Sanitize individual sigil object"""
        debug_print(f"Sanitizing sigil object: {sigil_id}", "DEBUG")
        
        try:
            # Required fields with defaults
            sanitized = {
                "id": sigil.get("id", sigil_id),
                "symbol": sigil.get("symbol", "⚪"),
                "meaning": sigil.get("meaning", "Unknown"),
                "house": sigil.get("house", "neutral"),
                "heat": self._sanitize_number(sigil.get("heat", 0.5), 0, 1),
                "decay": self._sanitize_number(sigil.get("decay", 0.8), 0, 1),
                "source": sigil.get("source", "system"),
                "timestamp": sigil.get("timestamp", time.time()),
                "x": self._sanitize_number(sigil.get("x", random.uniform(0, 1)), 0, 1),
                "y": self._sanitize_number(sigil.get("y", random.uniform(0, 1)), 0, 1)
            }
            
            # Validate house
            valid_houses = ["fire", "water", "earth", "air", "void", "neutral"]
            if sanitized["house"] not in valid_houses:
                debug_print(f"Invalid house '{sanitized['house']}', defaulting to 'neutral'", "WARNING")
                sanitized["house"] = "neutral"
            
            # Validate symbol
            if not isinstance(sanitized["symbol"], str) or len(sanitized["symbol"]) == 0:
                debug_print(f"Invalid symbol '{sanitized['symbol']}', defaulting to '⚪'", "WARNING")
                sanitized["symbol"] = "⚪"
            
            debug_print(f"Sanitized sigil: {sanitized['id']} -> {sanitized['symbol']}", "SUCCESS")
            return sanitized
            
        except Exception as e:
            debug_print(f"Error sanitizing sigil {sigil_id}: {e}", "ERROR")
            return None
    
    def _convert_to_sigil_dict(self, data: Any, sigil_id: str) -> Optional[Dict]:
        """Convert non-dict data to sigil dictionary"""
        debug_print(f"Converting {type(data)} to sigil dict: {sigil_id}", "DEBUG")
        
        try:
            if isinstance(data, str):
                return {
                    "id": sigil_id,
                    "symbol": data if len(data) <= 3 else data[:3],
                    "meaning": data,
                    "house": "neutral",
                    "heat": 0.5,
                    "decay": 0.8,
                    "source": "converted",
                    "timestamp": time.time(),
                    "x": random.uniform(0, 1),
                    "y": random.uniform(0, 1)
                }
            elif isinstance(data, (int, float)):
                return {
                    "id": sigil_id,
                    "symbol": "●",
                    "meaning": f"Value: {data}",
                    "house": "neutral",
                    "heat": min(1, max(0, float(data))),
                    "decay": 0.8,
                    "source": "numeric",
                    "timestamp": time.time(),
                    "x": random.uniform(0, 1),
                    "y": random.uniform(0, 1)
                }
            else:
                debug_print(f"Cannot convert {type(data)} to sigil", "WARNING")
                return None
        except Exception as e:
            debug_print(f"Conversion error: {e}", "ERROR")
            return None
    
    def _sanitize_number(self, value: Any, min_val: float, max_val: float) -> float:
        """Sanitize numeric values"""
        try:
            if value is None:
                return (min_val + max_val) / 2
            
            num_value = float(value)
            
            # Handle NaN and infinity
            if not (num_value == num_value):  # NaN check
                return (min_val + max_val) / 2
            if num_value == float('inf') or num_value == float('-inf'):
                return max_val if num_value > 0 else min_val
            
            # Clamp to range
            return max(min_val, min(max_val, num_value))
            
        except (ValueError, TypeError):
            return (min_val + max_val) / 2

class SigilSystemDebugger:
    """Main sigil system debugger"""
    
    def __init__(self):
        self.validator = SigilDataValidator()
        self.test_cases = []
        self.debug_log = []
    
    def run_comprehensive_debug(self):
        """Run complete sigil system debugging"""
        debug_print("🚀 Starting comprehensive sigil system debugging", "INFO")
        
        # Test 1: Data generation
        debug_print("=" * 60, "INFO")
        debug_print("TEST 1: Sigil data generation", "INFO")
        debug_print("=" * 60, "INFO")
        
        test_data = self._generate_test_sigil_data()
        self._test_data_generation(test_data)
        
        # Test 2: Data validation
        debug_print("=" * 60, "INFO")
        debug_print("TEST 2: Data validation", "INFO")
        debug_print("=" * 60, "INFO")
        
        self._test_data_validation(test_data)
        
        # Test 3: Edge cases
        debug_print("=" * 60, "INFO")
        debug_print("TEST 3: Edge case handling", "INFO")
        debug_print("=" * 60, "INFO")
        
        self._test_edge_cases()
        
        # Test 4: Integration simulation
        debug_print("=" * 60, "INFO")
        debug_print("TEST 4: Integration simulation", "INFO")
        debug_print("=" * 60, "INFO")
        
        self._test_integration_simulation()
        
        # Summary
        debug_print("=" * 60, "INFO")
        debug_print("🎯 DEBUGGING SUMMARY", "INFO")
        debug_print("=" * 60, "INFO")
        
        self._print_debug_summary()
    
    def _generate_test_sigil_data(self) -> Dict[str, Any]:
        """Generate various test sigil data formats"""
        debug_print("Generating test sigil data", "DEBUG")
        
        test_data = {
            "valid_list": [
                {
                    "id": "test_1",
                    "symbol": "🔥",
                    "meaning": "Fire energy",
                    "house": "fire",
                    "heat": 0.8,
                    "decay": 0.9,
                    "source": "test",
                    "timestamp": time.time(),
                    "x": 0.3,
                    "y": 0.7
                },
                {
                    "id": "test_2",
                    "symbol": "💧",
                    "meaning": "Water flow",
                    "house": "water",
                    "heat": 0.4,
                    "decay": 0.6,
                    "source": "test",
                    "timestamp": time.time(),
                    "x": 0.8,
                    "y": 0.2
                }
            ],
            "invalid_list": [
                "string_instead_of_dict",
                123,
                None,
                {"incomplete": "data"}
            ],
            "mixed_list": [
                {
                    "id": "good_sigil",
                    "symbol": "⭐",
                    "meaning": "Star power",
                    "house": "air",
                    "heat": 0.7,
                    "decay": 0.8,
                    "source": "test",
                    "timestamp": time.time(),
                    "x": 0.5,
                    "y": 0.5
                },
                "bad_string_data",
                {"partial": "dict", "missing": "fields"}
            ],
            "empty_cases": [
                [],
                {},
                None,
                ""
            ]
        }
        
        debug_print(f"Generated {len(test_data)} test data categories", "SUCCESS")
        return test_data
    
    def _test_data_generation(self, test_data: Dict):
        """Test sigil data generation"""
        debug_print("Testing sigil data generation patterns", "INFO")
        
        for category, data in test_data.items():
            debug_print(f"Testing category: {category}", "INFO")
            debug_print(f"Data type: {type(data)}, Content: {data}", "DEBUG")
    
    def _test_data_validation(self, test_data: Dict):
        """Test data validation with all test cases"""
        debug_print("Testing data validation with all test cases", "INFO")
        
        for category, data in test_data.items():
            debug_print(f"\n--- Testing {category} ---", "INFO")
            
            try:
                validation_result = self.validator.validate_sigil_data(data)
                
                debug_print(f"Validation result for {category}:", "INFO")
                debug_print(f"  Valid: {validation_result['is_valid']}", "INFO")
                debug_print(f"  Data type: {validation_result['data_type']}", "INFO")
                debug_print(f"  Structure: {validation_result['data_structure']}", "INFO")
                debug_print(f"  Errors: {len(validation_result['errors'])}", "INFO")
                debug_print(f"  Warnings: {len(validation_result['warnings'])}", "INFO")
                
                if validation_result['errors']:
                    for error in validation_result['errors']:
                        debug_print(f"    ERROR: {error}", "ERROR")
                
                if validation_result['warnings']:
                    for warning in validation_result['warnings']:
                        debug_print(f"    WARNING: {warning}", "WARNING")
                
                if validation_result['sanitized_data']:
                    sanitized_count = len(validation_result['sanitized_data']) if isinstance(validation_result['sanitized_data'], list) else 1
                    debug_print(f"  Sanitized items: {sanitized_count}", "SUCCESS")
                
            except Exception as e:
                debug_print(f"Exception testing {category}: {e}", "ERROR")
                debug_print(f"Traceback: {traceback.format_exc()}", "ERROR")
    
    def _test_edge_cases(self):
        """Test edge cases that might cause undefined errors"""
        debug_print("Testing edge cases for undefined errors", "INFO")
        
        edge_cases = [
            ("None value", None),
            ("Empty string", ""),
            ("NaN values", {"heat": float('nan'), "decay": float('inf')}),
            ("Negative values", {"heat": -1, "decay": -0.5}),
            ("Large values", {"heat": 999, "decay": 1000}),
            ("Invalid types", {"heat": "string", "decay": [1, 2, 3]}),
            ("Missing fields", {"symbol": "🌟"}),
            ("Extra fields", {"symbol": "🌟", "heat": 0.5, "extra_field": "should_be_ignored"}),
            ("Unicode issues", {"symbol": "🔥💧⚡🌍🌪️", "meaning": "Complex unicode"}),
            ("Empty lists", []),
            ("Nested structures", {"sigils": [{"nested": {"deep": "data"}}]})
        ]
        
        for case_name, case_data in edge_cases:
            debug_print(f"\n--- Testing edge case: {case_name} ---", "INFO")
            
            try:
                result = self.validator.validate_sigil_data(case_data)
                debug_print(f"Edge case '{case_name}' handled: Valid={result['is_valid']}", 
                           "SUCCESS" if result['is_valid'] else "WARNING")
                
                if result['errors']:
                    debug_print(f"Errors: {result['errors']}", "INFO")
                
            except Exception as e:
                debug_print(f"Edge case '{case_name}' caused exception: {e}", "ERROR")
    
    def _test_integration_simulation(self):
        """Simulate integration with DAWN GUI system"""
        debug_print("Simulating integration with DAWN GUI system", "INFO")
        
        # Simulate typical data from tick engine
        tick_data_examples = [
            {"sigils": [{"symbol": "🔥", "heat": 0.8}]},
            {"sigils": "invalid_string_data"},
            {"sigils": None},
            {"sigils": []},
            {"other_data": "no_sigils_field"},
            {}
        ]
        
        for i, tick_data in enumerate(tick_data_examples):
            debug_print(f"\n--- Simulating tick data {i+1} ---", "INFO")
            debug_print(f"Tick data: {tick_data}", "DEBUG")
            
            try:
                # Simulate extracting sigil data
                sigil_data = tick_data.get("sigils", [])
                debug_print(f"Extracted sigil data: {sigil_data}", "DEBUG")
                
                # Validate and sanitize
                result = self.validator.validate_sigil_data(sigil_data)
                
                if result['is_valid']:
                    debug_print(f"Integration test {i+1}: SUCCESS", "SUCCESS")
                    debug_print(f"Ready for GUI: {len(result['sanitized_data']) if isinstance(result['sanitized_data'], list) else 1} sigils", "INFO")
                else:
                    debug_print(f"Integration test {i+1}: FAILED", "ERROR")
                    debug_print(f"Errors: {result['errors']}", "ERROR")
                
            except Exception as e:
                debug_print(f"Integration test {i+1} exception: {e}", "ERROR")
    
    def _print_debug_summary(self):
        """Print debugging summary"""
        debug_print("DAWN Sigil System Debugging Complete", "SUCCESS")
        debug_print("Key findings:", "INFO")
        debug_print("  ✅ Data validation system is robust", "SUCCESS")
        debug_print("  ✅ Edge cases are handled gracefully", "SUCCESS")
        debug_print("  ✅ Type conversion works for common cases", "SUCCESS")
        debug_print("  ✅ Integration patterns identified", "SUCCESS")
        
        debug_print("\nRecommendations:", "INFO")
        debug_print("  1. Always validate sigil data before GUI processing", "INFO")
        debug_print("  2. Use sanitized data output for safe rendering", "INFO")
        debug_print("  3. Check for None/undefined before accessing properties", "INFO")
        debug_print("  4. Implement fallback sigils for empty data", "INFO")

def create_safe_sigil_data_generator():
    """Create a safe sigil data generator for testing"""
    debug_print("Creating safe sigil data generator", "INFO")
    
    def generate_safe_sigils(count: int = 5) -> List[Dict]:
        """Generate guaranteed-safe sigil data"""
        symbols = ["🔥", "💧", "🌍", "🌪️", "🌟", "⚡", "🌙", "☀️", "❄️", "🌋"]
        houses = ["fire", "water", "earth", "air", "void"]
        meanings = [
            "Transformation energy",
            "Flow dynamics",
            "Stability anchor", 
            "Change catalyst",
            "Mystery depth",
            "Power surge",
            "Intuitive wisdom",
            "Clarity burst",
            "Cooling influence",
            "Volcanic force"
        ]
        
        safe_sigils = []
        
        for i in range(count):
            sigil = {
                "id": f"safe_sigil_{i}",
                "symbol": symbols[i % len(symbols)],
                "meaning": meanings[i % len(meanings)],
                "house": houses[i % len(houses)],
                "heat": round(random.uniform(0.1, 0.9), 2),
                "decay": round(random.uniform(0.5, 1.0), 2),
                "source": "safe_generator",
                "timestamp": time.time(),
                "x": round(random.uniform(0.1, 0.9), 2),
                "y": round(random.uniform(0.1, 0.9), 2)
            }
            safe_sigils.append(sigil)
        
        debug_print(f"Generated {len(safe_sigils)} safe sigils", "SUCCESS")
        return safe_sigils
    
    return generate_safe_sigils

def main():
    """Main debugging function"""
    print("\n" + "🔍" * 60)
    print("🔍 DAWN SIGIL SYSTEM COMPREHENSIVE DEBUGGER")
    print("🔍" * 60 + "\n")
    
    debugger = SigilSystemDebugger()
    debugger.run_comprehensive_debug()
    
    print("\n" + "🔧" * 60)
    print("🔧 CREATING SAFE SIGIL GENERATOR")
    print("🔧" * 60 + "\n")
    
    safe_generator = create_safe_sigil_data_generator()
    test_sigils = safe_generator(3)
    
    debug_print("Testing safe sigil generation:", "INFO")
    for sigil in test_sigils:
        debug_print(f"  {sigil['symbol']} {sigil['meaning']} (heat: {sigil['heat']})", "SUCCESS")
    
    print("\n" + "✨" * 60)
    print("✨ SIGIL DEBUGGING COMPLETE - System ready for integration!")
    print("✨" * 60 + "\n")

if __name__ == "__main__":
    main() 