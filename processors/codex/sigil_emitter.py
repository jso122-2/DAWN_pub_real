from helix_import_architecture import helix_import
from substrate import pulse_heat
# File Path: /src/codex/sigil_emitter.py

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from core.event_bus import event_bus, Event
from codex.sigils import invoke_sigil
from schema.scup_loop import get_latest_scup


# Configuration
SIGIL_LOG_PATH = "juliet_flowers/cluster_report/sigil_emission_log.json"
MAX_LOG_ENTRIES = 100

# SCUP thresholds for sigil selection
SCUP_THRESHOLDS = {
    "critical": 0.3,
    "moderate": 0.6,
    "healthy": 0.8
}

# Sigil mapping based on SCUP ranges
SIGIL_MAP = {
    "critical": {
        "sigil": "/suppress",
        "reason": "SCUP critical: semantic instability detected"
    },
    "low": {
        "sigil": "/stabilize", 
        "reason": "SCUP low: partial coherence, stabilization needed"
    },
    "moderate": {
        "sigil": "/balance",
        "reason": "SCUP moderate: maintaining equilibrium"
    },
    "healthy": {
        "sigil": "/revive",
        "reason": "SCUP healthy: schema stable, growth possible"
    },
    "optimal": {
        "sigil": "/transcend",
        "reason": "SCUP optimal: peak coherence achieved"
    }
}


def log_sigil_emit(sigil: str, reason: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Log sigil emission with enhanced metadata
    
    Args:
        sigil: The sigil being emitted
        reason: Reason for emission
        metadata: Additional context data
    """
    entry = {
        "sigil": sigil,
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(SIGIL_LOG_PATH), exist_ok=True)
    
    # Load existing data
    try:
        if os.path.exists(SIGIL_LOG_PATH):
            with open(SIGIL_LOG_PATH, "r") as f:
                data = json.load(f)
        else:
            data = []
    except (json.JSONDecodeError, IOError):
        print(f"[SigilEmitter] ⚠️ Could not read log file, starting fresh")
        data = []
    
    # Append and trim to max entries
    data.append(entry)
    data = data[-MAX_LOG_ENTRIES:]
    
    # Write back
    try:
        with open(SIGIL_LOG_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"[SigilEmitter] ❌ Failed to write log: {e}")


class SigilEmitted(Event):
    """Event fired when a sigil is emitted"""
    def __init__(self, sigil: str, reason: str, scup: float, heat: float):
        self.sigil = sigil
        self.reason = reason
        self.scup = scup
        self.heat = heat
        self.timestamp = datetime.now()


def determine_sigil_from_scup(scup: float) -> tuple[str, str]:
    """
    Determine which sigil to emit based on SCUP value
    
    Args:
        scup: Current SCUP value (0.0 to 1.0)
        
    Returns:
        Tuple of (sigil, reason)
    """
    if scup < SCUP_THRESHOLDS["critical"]:
        return SIGIL_MAP["critical"]["sigil"], SIGIL_MAP["critical"]["reason"]
    elif scup < SCUP_THRESHOLDS["moderate"]:
        return SIGIL_MAP["low"]["sigil"], SIGIL_MAP["low"]["reason"]
    elif scup < SCUP_THRESHOLDS["healthy"]:
        return SIGIL_MAP["moderate"]["sigil"], SIGIL_MAP["moderate"]["reason"]
    elif scup < 0.9:
        return SIGIL_MAP["healthy"]["sigil"], SIGIL_MAP["healthy"]["reason"]
    else:
        return SIGIL_MAP["optimal"]["sigil"], SIGIL_MAP["optimal"]["reason"]


async def emit_sigil_from_scup(pulse=None) -> Dict[str, Any]:
    """
    Emit sigil based on current SCUP and thermal state
    
    Args:
        pulse: Optional pulse heat system instance
        
    Returns:
        Dict containing emission details
    """
    # Get current metrics
    scup = get_latest_scup()
    
    # Get heat from pulse if available
    try:
        if pulse and hasattr(pulse, 'get_heat'):
            heat = pulse.get_heat()
        else:
            # Try to get from global pulse
            import builtins
            global_pulse = getattr(builtins, 'pulse', None)
            heat = global_pulse.get_heat() if global_pulse and hasattr(global_pulse, 'get_heat') else 1.0
    except Exception:
        heat = 1.0
    
    # Determine sigil based on SCUP
    sigil, reason = determine_sigil_from_scup(scup)
    
    # Apply thermal modulation
    if heat > 8.0:
        # Override with suppression if overheating
        sigil = "/suppress"
        reason = f"Thermal override: heat critical ({heat:.1f})"
    elif heat > 6.0 and sigil == "/transcend":
        # Don't allow transcendence when hot
        sigil = "/balance"
        reason = f"Thermal limitation: heat elevated ({heat:.1f})"
    
    # Emit the sigil
    print(f"[SigilEmitter] 🧭 Emitting {sigil} → {reason}")
    print(f"[SigilEmitter] 📊 SCUP: {scup:.3f} | Heat: {heat:.2f}")
    
    # Invoke sigil
    try:
        invoke_sigil(sigil)
    except Exception as e:
        print(f"[SigilEmitter] ❌ Failed to invoke sigil: {e}")
    
    # Log emission
    metadata = {
        "scup": scup,
        "heat": heat,
        "thermal_override": heat > 8.0
    }
    log_sigil_emit(sigil, reason, metadata)
    
    # Publish event
    try:
        await event_bus.publish(SigilEmitted(sigil, reason, scup, heat))
    except Exception as e:
        print(f"[SigilEmitter] ⚠️ Failed to publish event: {e}")
    
    return {
        "sigil": sigil,
        "reason": reason,
        "scup": scup,
        "heat": heat,
        "timestamp": datetime.now().isoformat()
    }


# Maintain backward compatibility
async def scup_sigil_emitter(pulse=None) -> Dict[str, Any]:
    """
    Backward compatible alias for emit_sigil_from_scup
    Used by owl_auditor.py
    """
    return await emit_sigil_from_scup(pulse)


def get_sigil_emission_stats() -> Dict[str, Any]:
    """
    Get statistics about recent sigil emissions
    
    Returns:
        Dict with emission statistics
    """
    try:
        if not os.path.exists(SIGIL_LOG_PATH):
            return {"total_emissions": 0, "recent_emissions": []}
        
        with open(SIGIL_LOG_PATH, "r") as f:
            data = json.load(f)
        
        # Count sigil types
        sigil_counts = {}
        for entry in data:
            sigil = entry.get("sigil", "unknown")
            sigil_counts[sigil] = sigil_counts.get(sigil, 0) + 1
        
        # Get recent emissions
        recent = data[-10:] if len(data) > 10 else data
        
        return {
            "total_emissions": len(data),
            "sigil_counts": sigil_counts,
            "recent_emissions": recent,
            "most_common_sigil": max(sigil_counts.items(), key=lambda x: x[1])[0] if sigil_counts else None
        }
        
    except Exception as e:
        print(f"[SigilEmitter] ❌ Failed to get stats: {e}")
        return {"error": str(e)}


# Module initialization
print("[SigilEmitter] 🧭 Sigil emission system initialized")