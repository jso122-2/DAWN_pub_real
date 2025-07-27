"""
DAWN Cognitive Systems
Advanced AI consciousness processing with symbolic anatomy integration
"""

# Core consciousness components  
from .consciousness import DAWNConsciousness
from .alignment_probe import AlignmentProbe
from .qualia_kernel import QualiaKernel
from .conversation import DAWNConversation
from .spontaneity import DAWNSpontaneity

# Symbolic anatomy components - NEW
from .symbolic_anatomy import FractalHeart, SomaCoil, GlyphLung
from .symbolic_router import SymbolicRouter, get_symbolic_router, initialize_symbolic_routing

# Forecasting components
try:
    from .forecasting_engine import ForecastingEngine
    from .forecasting_models import DAWNForecastingModels  
    from .forecasting_processor import ForecastingProcessor
    from .forecast_tool import DAWNForecastTool
    FORECASTING_AVAILABLE = True
except ImportError:
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
