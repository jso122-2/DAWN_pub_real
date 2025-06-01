import os
import json
from bloom.juliet_cluster import cluster_by_bloom_factor, save_cluster_report
from rebloom_depth_stats import compute_rebloom_depth
from cluster_linker import link_clusters
from fractal.bloom_visualizer import plot_julia
from cluster_graph import visualize_cluster_graph

def inspect_bloom_clusters(threshold=1.0):
    clusters = cluster_by_bloom_factor(threshold=threshold)
    rebloom_depths = compute_rebloom_depth()
    report = save_cluster_report(clusters, rebloom_depths=rebloom_depths)
    visualize_cluster_graph()

    for i, cluster in enumerate(clusters):
        avg = sum(f["fractal_signature"]["bloom_factor"] for f in cluster) / len(cluster)
        mood_counts = defaultdict(int)
        for f in cluster:
            mood_counts[f["mood"]] += 1
        dominant_mood = max(mood_counts, key=mood_counts.get)

        c = complex(0.355, avg / 20.0)
        plot_julia(c, filename=f"Cluster_{i+1}.png", mood=dominant_mood)


    linked_clusters = link_clusters(report)
    print("\n🔗 Cross-Cluster Links:")
    for link in linked_clusters:
        print(f"→ {link['from']} ↔ {link['to']} | score={link['score']} | shared={link['shared_seeds']}")

    return clusters

def load_clusters(path="juliet_flowers/cluster_report/cluster_report.json"):
    if not os.path.exists(path):
        print(f"[Cluster] ❌ No cluster report found at {path}")
        return []
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    inspect_bloom_clusters(threshold=1.0)
