# /src/tracers/beetle.py

from tracers.base import Tracer
from bloom.registry import get_active_blooms
from owl.entropy import get_entropy_score
from semantic.edge_scanner import scan_edge_volatility, detect_glow_trace
from owl.owl_tracer_log import owl_log
import json
import os

GLOW_TRACE_LOG_PATH = "owl/glow_trace_log.json"

class BeetleTracer(Tracer):
    def __init__(self):
        super().__init__(
            name="Beetle",
            role="edge instability tracker + glow trace logger",
            watch=["/edge_flicker", "/glow_trace"],
            act=self.respond
        )

    def respond(self, sigil):
        print(f"[BeetleTracer] 🪲 Responding to sigil: {sigil}")
        if sigil == "/edge_flicker":
            self.scan_for_edge_volatility()
        elif sigil == "/glow_trace":
            self.log_glow_traces()

    def scan_for_edge_volatility(self):
        blooms = get_active_blooms()
        for bloom in blooms:
            edge_score = scan_edge_volatility(bloom)
            entropy = get_entropy_score(bloom)

            if edge_score > 0.7 or entropy > 0.85:
                msg = f"⚡ Unstable edge: {bloom.seed_id} | edge={edge_score:.2f}, entropy={entropy:.2f}"
                print(f"[Edge Alert] {msg}")
                owl_log(f"[Beetle] {msg}")
                bloom.mark_for_review("Beetle: high edge volatility")
            elif edge_score > 0.5:
                print(f"[Edge Watch] 👁️ Monitoring soft edge: {bloom.seed_id}")
                owl_log(f"[Beetle] Soft edge monitored: {bloom.seed_id} (edge={edge_score:.2f})")
                bloom.edge_watch_flag = True

    def log_glow_traces(self):
        detected_ids = []
        blooms = get_active_blooms()
        for bloom in blooms:
            if detect_glow_trace(bloom):
                print(f"[Glow Trace] ✨ Flicker detected: {bloom.seed_id}")
                owl_log(f"[Beetle] ✨ Glow trace detected in bloom {bloom.seed_id}")
                bloom.glow_trace_log.append("Glow trace detected by Beetle")
                detected_ids.append(bloom.seed_id)

        if detected_ids:
            self._append_glow_log(detected_ids)

    def _append_glow_log(self, bloom_ids):
        os.makedirs(os.path.dirname(GLOW_TRACE_LOG_PATH), exist_ok=True)
        try:
            if os.path.exists(GLOW_TRACE_LOG_PATH):
                with open(GLOW_TRACE_LOG_PATH, "r") as f:
                    data = json.load(f)
            else:
                data = []

            data.extend(bloom_ids)

            with open(GLOW_TRACE_LOG_PATH, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[BeetleTracer] ⚠️ Failed to write glow trace log: {e}")
