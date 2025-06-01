# File Path: /src/owl/visual_registry.py

# List of visual modules that can be triggered
visual_modules = [
    "belief_zone_animator",        # Visual for belief zone animation
    "entropy_cluster_plot",        # Visual for entropy cluster plot
    "drift_compass",               # Visual for drift compass
    "rebloom_lineage_animator"     # Visual for rebloom lineage animator
]

def get_visual_modules():
    """
    Returns a list of visual modules that can be triggered for audit.

    The visual modules are based on various audit checks such as 
    belief zones, entropy patterns, drift in the system, and rebloom lineages.
    """
    return visual_modules
