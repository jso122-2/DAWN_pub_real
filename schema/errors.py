"""
SCUP System Error Definitions
============================
Custom exceptions for the SCUP (Semantic Coherence Under Pressure) system.
"""

class SCUPError(Exception):
    """Base exception for all SCUP-related errors."""
    pass

class SCUPInputError(SCUPError):
    """Raised when input parameters are invalid or out of expected ranges."""
    pass

class SCUPStateError(SCUPError):
    """Raised when there is an invalid state transition or state inconsistency."""
    pass

class SCUPVaultError(SCUPError):
    """Raised when there are issues accessing or parsing vault files."""
    pass

class SCUPComputationError(SCUPError):
    """Raised when SCUP computation fails due to invalid parameters or state."""
    pass

class SCUPOverrideError(SCUPError):
    """Raised when there are issues with SCUP override values."""
    pass

class SCUPLoggingError(SCUPError):
    """Raised when there are issues with SCUP logging operations."""
    pass

class SCUPStabilityError(SCUPError):
    """Raised when stability calculations fail due to insufficient data."""
    pass 