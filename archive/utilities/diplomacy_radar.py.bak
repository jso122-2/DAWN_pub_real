# /visual/diplomacy_radar.py

import matplotlib.pyplot as plt
import numpy as np

def plot_tracer_diplomacy(seed_id, tracer_signals):
    """
    Create spider web plot of tracer influence during sigil routing.
    """
    tracers = [t for t, _, _ in tracer_signals]
    scores = [w for _, _, w in tracer_signals]

    angles = np.linspace(0, 2 * np.pi, len(tracers), endpoint=False).tolist()
    scores += scores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw={'polar': True})
    ax.plot(angles, scores, 'o-', linewidth=2)
    ax.fill(angles, scores, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), tracers)
    ax.set_title(f"Tracer Diplomacy Radar: {seed_id}")
    plt.show()
