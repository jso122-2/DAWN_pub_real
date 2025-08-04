"""
DAWN Cognitive Systems
Advanced AI consciousness processing with symbolic anatomy integration
"""

# Simplified imports to avoid relative import issues
# Core consciousness components - simplified
DAWNConsciousness = None
AlignmentProbe = None
QualiaKernel = None
DAWNConversation = None
DAWNSpontaneity = None

# Symbolic anatomy components - simplified
FractalHeart = None
SomaCoil = None
GlyphLung = None
SymbolicRouter = None
get_symbolic_router = None
initialize_symbolic_routing = None

# Forecasting components - simplified
FORECASTING_AVAILABLE = False

__all__ = [
    # Core consciousness
    'DAWNConsciousness',
    'AlignmentProbe', 
    'QualiaKernel',
    'DAWNConversation',
    'DAWNSpontaneity',
    
    # Symbolic anatomy - NEW
    'FractalHeart',
    'SomaCoil', 
    'GlyphLung',
    'SymbolicRouter',
    'get_symbolic_router',
    'initialize_symbolic_routing',
    
    # Forecasting (if available)
    'FORECASTING_AVAILABLE'
]

# Add forecasting to exports if available
if FORECASTING_AVAILABLE:
    __all__.extend([
        'ForecastingEngine',
        'DAWNForecastingModels', 
        'ForecastingProcessor',
        'DAWNForecastTool'
    ])
