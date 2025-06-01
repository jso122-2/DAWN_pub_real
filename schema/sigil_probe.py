# /codex/sigil_probe.py

from core.schema_anomaly_logger import log_anomaly
from codex.sigil_memory_ring import sigil_memory_ring

def probe_sigil(name, fallback_entropy=0.0):
    if name not in sigil_memory_ring:
        log_anomaly("SigilPhantomAccess", f"DAWN requested sigil '{name}' before registration.")
        return fallback_entropy
    
    sigil = sigil_memory_ring[name]
    log_anomaly("SigilAccess", f"Sigil '{name}' accessed | Entropy: {sigil.entropy:.3f}")
    return sigil.entropy
