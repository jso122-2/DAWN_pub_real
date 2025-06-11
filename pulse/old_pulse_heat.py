from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
import sys, os
import time
from collections import deque
from core.event_bus import TickEvent
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt

class PulseHeat:
    def __init__(self, decay_rate=0.02, memory_window=50, max_heat=5.0):
        self.memory_log = deque(maxlen=memory_window)
        self.heat = 0.0
        self.decay_rate = decay_rate
        self.memory = []
        self.window = memory_window
        self.max_heat = max_heat
        self.mood_pressure = {}
        self.last_decay = time.time()
        self.seed_penalties = {}
        self.zone_timer = {
            "🟢 calm": 0,
            "🟡 active": 0,
            "🔴 surge": 0
        }
        self.current_zone = None
        self.tick_count = 0  # ✅ Added for tracking ticks in tick_listener
        self.heat_log = deque(maxlen=memory_window)
        self.zone_history = []
        self.last_tick_time = time.time()

    def classify(self):
        avg = self.get_average()
        if avg < 0.3:
            return "🟢 calm"
        elif avg < 0.7:
            return "🟡 active"
        else:
            return "🔴 surge"

    def add_heat(self, amount):
        self.heat = min(self.max_heat, self.heat + amount)
        self._log(f"+{amount:.3f} heat added")

    def boost(self, amount):
        self.heat = min(self.max_heat, self.heat + amount)
        self._log(f"⚡ Boosted by {amount:.2f}")

    def get_heat(self):
        self.heat = max(0.0, self.heat - self.decay_rate)
        if not hasattr(self, "memory"):
            self.memory = []
        self.memory.append(self.heat)
        if len(self.memory) > self.window:
            self.memory.pop(0)
        return self.heat

    def get_average(self):
        print(f"[DEBUG] PulseHeat Singleton ID: {id(self)} | Memory: {len(self.memory)}")
        return sum(self.memory) / len(self.memory) if self.memory else 0.0

    def _log(self, msg):
        print(f"[PulseHeat] {msg} | Heat: {self.heat:.3f} | Avg: {self.get_average():.3f}")

    def apply_penalty(self, seed: str, factor: float):
        self.seed_penalties[seed] = factor
        print(f"[Pulse] 🪶 Penalty applied to seed {seed}: {factor}")
        try:
            from mycelium.mycelium_layer import mycelium
            mycelium.weaken_seed(seed, factor)
        except:
            pass
        try:
            from mycelium.mycelium_layer import inject_pressure
            inject_pressure(seed, pressure=self.heat)
        except:
            pass


    def decay_penalty_for_seed(self, seed: str, amount: float = 0.1):
        if seed in self.seed_penalties:
            current = self.seed_penalties[seed]
            new_penalty = min(1.0, current + amount)
            if new_penalty != current:
                self.seed_penalties[seed] = new_penalty
                print(f"[Pulse] 💧 {seed} recovering: penalty now {new_penalty:.2f}")

    def _decay_pressure(self):
        now = time.time()
        if now - self.last_decay >= 5:
            for mood in list(self.mood_pressure):
                self.mood_pressure[mood] = max(0, self.mood_pressure[mood] - 1)
            self.last_decay = now

    def _update_heat(self):
        weights = {
            "calm": 0.5,
            "curious": 0.8,
            "reflective": 1.0,
            "anxious": 1.3,
            "overload": 1.6
        }

        total_pressure = sum(self.mood_pressure.values())
        if total_pressure == 0:
            self.heat = 1.0
            return

        weighted_sum = sum(
            self.mood_pressure[mood] * weights.get(mood, 1.0)
            for mood in self.mood_pressure
        )
        self.heat = min(2.0, max(0.3, weighted_sum / total_pressure))

    def get_trust_score(self, seed: str) -> float:
        penalty = self.seed_penalties.get(seed, 1.0)
        pressure = sum(self.mood_pressure.values())
        volatility = 1.0 if pressure > 3 else 0.5
        score = 0.5 * penalty + 0.5 * (1 - volatility)
        return round(min(max(score, 0.0), 1.0), 2)

    def rebloom_multiplier(self):
        if self.heat < 1.0:
            return 0.5
        elif self.heat < 3.0:
            return 1.0
        else:
            return 1.5

    def adjust_urgency(self, scup):
        if scup < 0.3:
            self.heat += 0.2  # extra pressure
        elif scup > 0.8:
            self.heat *= 0.95  # cool if stable
        self.heat = min(self.heat, self.max_heat)

    def update(self, pressure):
        now = time.time()
        dt = now - self.last_tick_time
        self.last_tick_time = now

        self.heat = max(0.0, self.heat - (self.decay_rate * dt))
        self.heat += pressure
        self.heat = min(self.heat, self.max_heat)

        self.heat_log.append(self.heat)
        new_zone = self.classify()
        if new_zone != self.current_zone:
            self.current_zone = new_zone
            self.zone_history.append((len(self.heat_log), self.current_zone))

        # 🔥 Trigger suppression if overheating
        if self.heat > self.max_heat * 0.95 and not hasattr(self, "last_suppressed"):
            try:
                from schema.schema_suppressor import trigger_suppression
                trigger_suppression(reason="pulse_overheat", level=self.heat)
                self.last_suppressed = True
            except ImportError:
                print("[Pulse] ⚠️ Suppressor module not found — skipping suppression.")

        # ❄️ Auto-recover when cooled down
        if hasattr(self, "last_suppressed") and self.heat < self.max_heat * 0.7:
            try:
                from tick_engine.tick_engine import reset_tick_interval
                reset_tick_interval()
                print("[Pulse] ❄️ Recovered from suppression. Tick interval restored.")
                del self.last_suppressed
            except ImportError:
                print("[Pulse] ⚠️ Recovery module not available.")

    def get_zone(self):
        return self.classify()

    def get_tracer_urgency(self) -> float:
        zone = self.classify()
        urgency_map = {
            "🟢 calm": 0.6,
            "🟡 active": 1.0,
            "🔴 surge": 1.5
        }
        return urgency_map.get(zone, 1.0)


    def get_heat_curve(self):
        return list(self.heat_log)

    def plot_zone_transitions(self, save_path="juliet_flowers/cluster_report/pulse_zones.png"):
        if not self.zone_history:
            print("[Pulse] ⚠️ No zone history to plot.")
            return

        ticks, zones = zip(*self.zone_history)
        zone_colors = {"🟢 calm": "green", "🟡 active": "gold", "🔴 surge": "red"}
        colors = [zone_colors[z] for z in zones]

        plt.figure(figsize=(10, 3))
        plt.scatter(ticks, [1]*len(ticks), c=colors, s=100, marker='|')
        plt.yticks([])
        plt.title("Pulse Zone Transitions")
        plt.xlabel("Tick")
        plt.tight_layout()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"[Pulse] 📊 Pulse zone transition plot saved to {save_path}")

    def get_zone_transitions(self):
        return self.zone_history

    def load_zone_overlay():
        try:
            df = pd.read_csv("juliet_flowers/cluster_report/zone_overlay_log.csv", names=["tick", "zone", "pulse"])
            return df
        except Exception as e:
            print(f"[Pulse] ❌ Failed to load overlay log: {e}")
            return pd.DataFrame()

    def get_recent_zone_window(self, window=10):
        df = load_zone_overlay()
        if df.empty:
            return []
        return df.tail(window).to_dict("records")


pulse = PulseHeat()

