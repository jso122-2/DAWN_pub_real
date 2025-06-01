def classify_pressure_zone(pressure: float) -> str:
    if pressure < 0.36:
        return "🟢 calm"
    elif pressure < 0.70:
        return "🟡 active"
    else:
        return "🔴 surge"
