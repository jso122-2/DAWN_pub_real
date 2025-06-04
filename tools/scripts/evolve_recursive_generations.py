
from bloom.recursive_synthesis import recursive_synthesis
from visual.synthesis_entropy_chart import plot_entropy_trend
from visual.synthesis_lineage_animator import animate_synthesis_lineage

def evolve_recursive_generations(generations=3):
    print(f"🧪 Beginning recursive synthesis across {generations} generations...\n")
    for gen in range(generations):
        print(f"--- Generation {gen + 1} ---")
        recursive_synthesis()
    print("\n✅ All generations synthesized.")
    print("📈 Updating charts and visuals...")
    plot_entropy_trend()
    animate_synthesis_lineage()

if __name__ == "__main__":
    evolve_recursive_generations()
