import sys, os
import time
from collections import deque
from core.event_bus import TickEvent

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
        # 🧼 Unified logging entry for memory record
        from juliet.juliet_logger import record_juliet_memory
        log_entry = {
            "tick": self.tick_count,
            "heat": round(self.heat, 3),
            "zone": self.get_zone(),
            "message": msg
        }
        record_juliet_memory(log_entry)
        print(f"[PulseHeat] {msg} | Heat: {self.heat:.3f} | Avg: {self.get_average():.3f}")

    def apply_penalty(self, seed: str, factor: float):
        self.seed_penalties[seed] = factor
        print(f"[Pulse] 🪶 Penalty applied to seed {seed}: {factor}")
        try:
            from mycelium.mycelium_layer import mycelium
            mycelium.weaken_seed(seed, factor)
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
        # 🔁 Let memory shape decay rate dynamically
        if len(self.memory) >= 5:
            recent_avg = sum(self.memory[-5:]) / 5
            if recent_avg > 1.5:
                self.decay_rate = min(0.05, self.decay_rate + 0.005)  # slow decay when overactive
            elif recent_avg < 0.5:
                self.decay_rate = max(0.01, self.decay_rate - 0.005)  # speed decay when underused
        if scup < 0.3:
            self.heat += 0.2  # extra pressure
        elif scup > 0.8:
            self.heat *= 0.95  # cool if stable
        self.heat = min(self.heat, self.max_heat)

    def update(self, pressure):
        self.tick_count += 1
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

    def get_zone(self):
        return self.current_zone

    def get_heat_curve(self):
        return list(self.heat_log)

    def plot_heatmap(self, save_path="juliet_flowers/cluster_report/pulse_heatmap.png"):
        if not self.heat_log:
            print("[Pulse] ⚠️ No heat log to plot.")
            return

        plt.figure(figsize=(10, 3))
        plt.plot(list(range(len(self.heat_log))), list(self.heat_log), color="firebrick", linewidth=2)
        plt.title("Pulse Heat Over Time")
        plt.xlabel("Tick")
        plt.ylabel("Heat")
        plt.grid(True)
        plt.tight_layout()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"[Pulse] 🌡️ Heat curve saved to {save_path}")

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
