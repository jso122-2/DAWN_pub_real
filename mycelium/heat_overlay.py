import pandas as pd
import matplotlib.pyplot as plt
import json
import sys
import os
from datetime import datetime

# --- Classification Utility ---
def classify_nutrient_level(val: float) -> str:
    if val < 0.3: return "low"
    elif val < 0.7: return "medium"
    return "high"

# --- Programmatic Logic for Tracers or Autonomous Hooks ---
def get_nutrient_heat(depth: int, normalize_by: int = 10, fallback: float = 0.0) -> float:
    """
    Return normalized nutrient intensity for a given rebloom depth.
    Reads from logs/mycelium_logs/nutrient_log.json.
    """
    path = "logs/mycelium_logs/nutrient_log.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            nutrient_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"[Mycelium] ⚠️ Missing or invalid nutrient log at {path}")
        return fallback

    count = nutrient_data.get(str(depth), 0)
    heat_value = min(1.0, count / normalize_by)
    print(f"[Mycelium] 🌡️ Depth {depth} → Heat = {heat_value:.3f}")
    return heat_value

# --- Render Overlay Visualization ---
def render_heat_overlay(csv_path: str = "juliet_flowers/cluster_report/nutrient_flow_log.csv",
                        output_dir: str = "juliet_flowers/cluster_report"):
    """
    Visualize nutrient pressure zones over time from CSV log.
    """
    try:
        df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    except Exception as e:
        print(f"[Mycelium] ❌ Failed to read CSV: {e}")
        return

    if "pressure_zone" not in df.columns:
        df["pressure_zone"] = df["flow_strength"].apply(classify_nutrient_level)

    df.sort_values("timestamp", inplace=True)

    zone_colors = {"low": "green", "medium": "gold", "high": "red"}

    plt.figure(figsize=(12, 5))
    for zone, group in df.groupby("pressure_zone"):
        plt.scatter(group["timestamp"], group["flow_strength"],
                    c=zone_colors.get(zone, "gray"), label=zone, alpha=0.7)

    plt.legend()
    plt.ylabel("Nutrient Flow Strength")
    plt.title("🕸️ Root Pressure Zones – Nutrient Map Overlay")
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "mycelium_pressure_overlay.png")
    plt.savefig(out_path)
    print(f"[Mycelium] ✅ Saved overlay: {out_path}")
    plt.close()

# --- Command Line Entrypoint ---
if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[2] != "--out-dir":
        print("❌ Usage: python heat_overlay.py <csv_path> --out-dir <output_folder>")
        sys.exit(1)

    render_heat_overlay(csv_path=sys.argv[1], output_dir=sys.argv[3])
