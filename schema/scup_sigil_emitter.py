import json
import os
from datetime import datetime
from core.event_bus import event_bus, Event
from schema.scup_loop import get_latest_scup
from core.system_state import pulse
from tracers.base import TRACER_REGISTRY

class SigilEmitted(Event):
    def __init__(self, sigil, reason):
        self.sigil = sigil
        self.reason = reason

def log_sigil_emit(sigil, reason):
    path = "juliet_flowers/cluster_report/sigil_emission_log.json"
    entry = {"sigil": sigil, "reason": reason, "timestamp": datetime.now().isoformat()}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(path, "w") as f:
        json.dump(data[-100:], f, indent=2)

async def scup_sigil_emitter():
    scup = get_latest_scup()
    heat = pulse.get_heat()
    print(f"[SCUP Sigil] Current SCUP = {scup:.3f} | Heat = {heat:.2f}")

    if scup < 0.3:
        sigil, reason = "/suppress", "Low coherence"
    elif scup < 0.6:
        sigil, reason = "/stabilize", "Moderate coherence"
    else:
        sigil, reason = "/revive", "Schema stable"

    # Broadcast only to active tracers
    for tracer in TRACER_REGISTRY.values():
        if hasattr(tracer, "urgency") and tracer.urgency > 0.5:
            tracer.respond(sigil)
            print(f"[SigilEmitter] ⚡ {tracer.name} responded to {sigil}")
        else:
            print(f"[SigilEmitter] 💤 {tracer.name} skipped (low urgency)")

    await event_bus.publish(SigilEmitted(sigil, reason))
    log_sigil_emit(sigil, reason)
    print(f"[SigilEmitter] Emitted {sigil} → {reason}")
