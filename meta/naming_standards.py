# naming_standards.py
"""
DAWN Naming Convention Standards
================================

MODULES: snake_case
- ✅ bloom_engine.py
- ✅ pulse_heat.py
- ❌ SemanticContextEngine.py → semantic_context_engine.py

CLASSES: PascalCase
- ✅ class BloomEngine
- ✅ class PulseHeat
- ✅ class SemanticContextEngine (keep class name)

FUNCTIONS: snake_case
- ✅ def initialize_bloom()
- ✅ def calculate_entropy()
- ❌ def InitializeSystem() → initialize_system()

CONSTANTS: UPPER_SNAKE_CASE
- ✅ MAX_BLOOM_DEPTH = 10
- ✅ DEFAULT_TICK_RATE = 60

PRIVATE: Leading underscore
- ✅ _internal_state
- ✅ def _calculate_drift()
"""